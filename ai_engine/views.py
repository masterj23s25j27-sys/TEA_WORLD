from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import AIChatSession, AIChatMessage
from .services import get_chatbot_response, get_market_trends, get_tea_recommendations
from products.models import Product, Category
from orders.models import CartItem
import json

@login_required
def chatbot_view(request):
    # Find or create a session for the user
    session = AIChatSession.objects.filter(user=request.user).order_by('-created_at').first()
    if not session:
        session = AIChatSession.objects.create(user=request.user)
        # Add greeting
        AIChatMessage.objects.create(
            session=session,
            sender='BOT',
            text="Hello! I am your sha_Tea copilot. I can help you select wholesale varieties, estimate global logistics times, or forecast seasonal demand. What are you looking to source today?"
        )

    if request.method == 'POST':
        user_text = request.POST.get('message', '').strip()
        if user_text:
            AIChatMessage.objects.create(session=session, sender='USER', text=user_text)
            bot_text = get_chatbot_response(user_text)
            AIChatMessage.objects.create(session=session, sender='BOT', text=bot_text)
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'user_message': user_text, 'bot_response': bot_text})

        return redirect('ai_engine:chatbot')

    messages = session.messages.all().order_by('timestamp')
    return render(request, 'ai_engine/chatbot.html', {'chat_messages': messages})

@login_required
def ai_tools_dashboard(request):
    trends = get_market_trends()
    recommendations = get_tea_recommendations(request.user)

    # Simulated invoice scanning
    invoice_results = None
    if request.method == 'POST' and request.FILES.get('invoice_file'):
        file = request.FILES['invoice_file']
        # Mock OCR output
        invoice_results = {
            'file_name': file.name,
            'vendor_detected': 'Himalayan Organic Tea Estates',
            'confidence': '98.4%',
            'items': [
                {'name': 'Darjeeling First Flush Autumnal', 'quantity': 50, 'est_cost': 2250.00},
                {'name': 'Uji Sencha Premium', 'quantity': 30, 'est_cost': 1650.00},
                {'name': 'Silver Needle (Baihao Yinzhen)', 'quantity': 15, 'est_cost': 1275.00}
            ],
            'total_extracted': 5175.00
        }
        
        # Save mock items to session so user can add them to cart
        request.session['ocr_invoice_items'] = invoice_results['items']

    context = {
        'trends': trends,
        'recommendations': recommendations,
        'invoice_results': invoice_results,
    }
    return render(request, 'ai_engine/tools_dashboard.html', context)

@login_required
def add_ocr_items_to_cart(request):
    items = request.session.get('ocr_invoice_items')
    if items:
        added = 0
        for item in items:
            product = Product.objects.filter(name=item['name']).first()
            if product:
                cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
                if created:
                    cart_item.quantity = item['quantity']
                else:
                    cart_item.quantity += item['quantity']
                cart_item.save()
                added += 1
        
        if added > 0:
            import django.contrib.messages as dj_messages
            dj_messages.success(request, f"Successfully imported {added} items from scanned invoice into your cart!")
            del request.session['ocr_invoice_items']
    return redirect('orders:cart_detail')
