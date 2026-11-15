import random
from products.models import Product, Category

def get_chatbot_response(user_text):
    text = user_text.lower()
    
    responses = [
        "Welcome to sha_Tea Support. How can I help you negotiate bulk tea rates today?",
        "Our current trending teas are Darjeeling First Flush (Autumnal) and Stone-Ground Uji Matcha.",
        "To get optimal wholesale rates, try placing orders of 100kg or more; vendors often apply steep volume discounts.",
        "You can check our AI Dashboard in the vendor portal for seasonal tea demand forecasts and price trends.",
        "If you upload a purchase invoice, our OCR engine will extract products, quantities, and generate draft orders automatically.",
        "Matcha grade teas require shade growing for 3-4 weeks before harvest to boost chlorophyll and L-theanine levels.",
        "Assam CTC teas are standard choice for milk tea bases because of their rich malt profile and high extraction yield."
    ]

    if 'price' in text or 'cost' in text or 'cheap' in text:
        return "Market Analysis: Tea prices are currently stable. Green teas have seen a 3% decrease due to strong harvests in Shizuoka. I suggest looking at 'Uji Sencha Premium' or 'Gunpowder Pearl' for optimal margins."
    elif 'matcha' in text:
        return "Matcha Insight: Ceremonial Uji Matcha is currently trending in cafe chains. Average retail markups are 300%. Our platform vendor 'Himalayan Organic Tea Estates' has excellent ceremonial grades in stock."
    elif 'invoice' in text or 'ocr' in text or 'upload' in text:
        return "You can use the AI Invoice Scanner on our AI Tools page! Simply upload a purchase order image, and we will translate it into a cart order."
    elif 'recommend' in text or 'best' in text:
        return "Based on buyer preferences, 'Darjeeling First Flush Autumnal' (FTGFOP) is highly rated for luxury retail, while 'Assam CTC Golden Buds' is best for quick high-volume supply."
    elif 'hello' in text or 'hi' in text:
        return "Hello! I am your sha_Tea Assistant. Ask me about tea grades, market price forecasting, or invoice extraction."
    
    return random.choice(responses)

def get_tea_recommendations(user):
    # Retrieve random products but rank them beautifully
    products = list(Product.objects.all())
    if len(products) < 4:
        return products
    return random.sample(products, 4)

def get_market_trends():
    categories = Category.objects.all()
    trends = []
    for cat in categories:
        # Generate some mock numbers
        price_change = round(random.uniform(-5.0, 8.0), 2)
        demand_index = random.randint(60, 98)
        trends.append({
            'category': cat.name,
            'price_change': price_change,
            'demand_index': demand_index,
            'status': 'Rising' if price_change > 0 else 'Declining'
        })
    return trends
