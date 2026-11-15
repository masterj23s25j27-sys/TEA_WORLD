from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Review

def product_list(request):
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    grade = request.GET.get('grade', '')
    sort_by = request.GET.get('sort', 'name')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query) | products.filter(description__icontains=query) | products.filter(origin__icontains=query)

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if grade:
        products = products.filter(grade=grade)

    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('name')

    categories = Category.objects.all()
    grades = Product.GRADE_CHOICES

    context = {
        'products': products,
        'categories': categories,
        'grades': grades,
        'query': query,
        'selected_category': category_slug,
        'selected_grade': grade,
        'selected_sort': sort_by,
    }
    return render(request, 'products/catalog.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all().order_by('-created_at')
    
    # Simple simulated AI review summarizer
    positive_count = sum(1 for r in reviews if r.ai_sentiment == 'Positive')
    negative_count = sum(1 for r in reviews if r.ai_sentiment == 'Negative')
    neutral_count = len(reviews) - positive_count - negative_count
    
    summary = "No reviews available yet for AI analysis."
    if reviews:
        if positive_count > negative_count:
            summary = "AI Summary: Customers highly recommend this tea variety, highlighting its rich aroma, smooth finish, and excellent quality-to-price ratio."
        elif negative_count > positive_count:
            summary = "AI Summary: Reviews are mixed, with complaints focused on moisture levels or packaging. Consider checking with the vendor on batch details."
        else:
            summary = "AI Summary: Balanced reception. Buyers note typical standard flavor profiles for this grade and solid value for bulk orders."

    context = {
        'product': product,
        'reviews': reviews,
        'ai_summary': summary,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count': neutral_count,
    }
    return render(request, 'products/detail.html', context)

@login_required
def add_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if not rating or not comment:
            messages.error(request, "Rating and comment are required.")
            return redirect('products:detail', slug=product.slug)

        # Simple simulated sentiment analysis
        sentiment = 'Positive'
        lower_comment = comment.lower()
        negative_words = ['bad', 'poor', 'bitter', 'expensive', 'stale', 'worst', 'disappointed', 'low quality']
        positive_words = ['great', 'excellent', 'amazing', 'delicious', 'aroma', 'fresh', 'best', 'smooth']
        
        neg_count = sum(1 for w in negative_words if w in lower_comment)
        pos_count = sum(1 for w in positive_words if w in lower_comment)
        
        if neg_count > pos_count:
            sentiment = 'Negative'
        elif pos_count == neg_count:
            sentiment = 'Neutral'

        Review.objects.create(
            product=product,
            buyer=request.user,
            rating=int(rating),
            comment=comment,
            ai_sentiment=sentiment
        )
        messages.success(request, "Thank you for your feedback! AI analysis tagged this review as: " + sentiment)
        return redirect('products:detail', slug=product.slug)
    
    return redirect('products:list')
