from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    icon_class = models.CharField(max_length=50, default='ri-leaf-line') # remixicon classes

    class Meta:
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    GRADE_CHOICES = (
        ('FTGFOP', 'Fine Tippy Golden Flowery Orange Pekoe (Premium)'),
        ('TGFOP', 'Tippy Golden Flowery Orange Pekoe'),
        ('OP', 'Orange Pekoe'),
        ('BOP', 'Broken Orange Pekoe'),
        ('FANNINGS', 'Fannings (Quick Brew)'),
        ('DUST', 'Fine Tea Dust'),
        ('MATCHA', 'Ceremonial Matcha Grade'),
    )

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    origin = models.CharField(max_length=100, default='Assam, India')
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, default='OP')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # price per kg for wholesale
    stock = models.IntegerField(default=100) # stock in kg
    image_url = models.URLField(max_length=500, blank=True, null=True)
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_products')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)

    def __str__(self):
        return f"{self.name} ({self.grade})"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    ai_sentiment = models.CharField(max_length=20, default='Neutral') # Positive, Negative, Neutral
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.buyer.username}"
