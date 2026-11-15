import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Product, Review

User = get_user_model()

# Royalty-free Unsplash tea images
TEA_IMAGES = {
    'Black Tea': [
        'https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=600&auto=format&fit=crop&q=60',
        'https://images.unsplash.com/photo-1597481499750-3e6b22637e12?w=600&auto=format&fit=crop&q=60',
    ],
    'Green Tea': [
        'https://images.unsplash.com/photo-1563822249548-9a72b6353cd1?w=600&auto=format&fit=crop&q=60',
        'https://images.unsplash.com/photo-1627435601361-ec25f5b1d0e5?w=600&auto=format&fit=crop&q=60',
    ],
    'Oolong Tea': [
        'https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=600&auto=format&fit=crop&q=60',
        'https://images.unsplash.com/photo-1597481499750-3e6b22637e12?w=600&auto=format&fit=crop&q=60',
    ],
    'White Tea': [
        'https://images.unsplash.com/photo-1563822249548-9a72b6353cd1?w=600&auto=format&fit=crop&q=60',
    ],
    'Matcha': [
        'https://images.unsplash.com/photo-1536256263959-770b48d82b0a?w=600&auto=format&fit=crop&q=60',
        'https://images.unsplash.com/photo-1582793988951-9aed5509eb97?w=600&auto=format&fit=crop&q=60',
    ],
    'Herbal Infusion': [
        'https://images.unsplash.com/photo-1555597673-b21d5c935865?w=600&auto=format&fit=crop&q=60',
        'https://images.unsplash.com/photo-1594631252845-29fc4cc8cfa9?w=600&auto=format&fit=crop&q=60',
    ]
}

DEFAULT_IMAGE = 'https://images.unsplash.com/photo-1597481499750-3e6b22637e12?w=600&auto=format&fit=crop&q=60'

TEA_SEED_DATA = [
    # Black Teas
    {
        'name': 'Darjeeling First Flush Autumnal',
        'category': 'Black Tea',
        'origin': 'Darjeeling, India',
        'grade': 'FTGFOP',
        'description': 'Light-bodied, floral, and highly aromatic tea harvested during the fresh spring rains of Darjeeling.',
        'price': 45.00,
        'stock': 500,
    },
    {
        'name': 'Assam CTC Golden Buds',
        'category': 'Black Tea',
        'origin': 'Assam, India',
        'grade': 'BOP',
        'description': 'Rich, malty, and full-bodied black tea. Perfect for strong breakfast brews and traditional milk blends.',
        'price': 18.50,
        'stock': 1200,
    },
    {
        'name': 'Ceylon Premium Orange Pekoe',
        'category': 'Black Tea',
        'origin': 'Ruhuna, Sri Lanka',
        'grade': 'OP',
        'description': 'Bright golden color with a crisp, slightly citrusy flavor characteristic of high-grown Sri Lankan estates.',
        'price': 22.00,
        'stock': 800,
    },
    {
        'name': 'Yunnan Dian Hong Golden Needle',
        'category': 'Black Tea',
        'origin': 'Yunnan, China',
        'grade': 'TGFOP',
        'description': 'Made entirely from tender golden spring buds, releasing notes of sweet honey, cocoa, and soft wood.',
        'price': 65.00,
        'stock': 300,
    },
    {
        'name': 'Lapsang Souchong Smoked Black',
        'category': 'Black Tea',
        'origin': 'Fujian, China',
        'grade': 'OP',
        'description': 'Traditional smoke-dried black tea over pine fires, imparting a bold, campfire-like fragrance and deep flavor.',
        'price': 28.00,
        'stock': 400,
    },

    # Green Teas
    {
        'name': 'Uji Sencha Premium',
        'category': 'Green Tea',
        'origin': 'Kyoto, Japan',
        'grade': 'OP',
        'description': 'Freshly steamed green tea leaves from Kyoto with a sweet, grassy aroma and deep umami finish.',
        'price': 55.00,
        'stock': 350,
    },
    {
        'name': 'Dragon Well (Longjing) Pre-Rain',
        'category': 'Green Tea',
        'origin': 'Hangzhou, China',
        'grade': 'FTGFOP',
        'description': 'Flat-fried leaves offering a delicate chestnut aroma, velvety texture, and lingering sweet taste.',
        'price': 72.00,
        'stock': 200,
    },
    {
        'name': 'Gunpowder Pearl Green',
        'category': 'Green Tea',
        'origin': 'Zhejiang, China',
        'grade': 'OP',
        'description': 'Leaves rolled into tight pellets that unfurl during brewing, delivering a smoky and herbaceous cup.',
        'price': 14.50,
        'stock': 1500,
    },

    # Oolong Teas
    {
        'name': 'Iron Goddess of Mercy (Tieguanyin)',
        'category': 'Oolong Tea',
        'origin': 'Anxi, China',
        'grade': 'OP',
        'description': 'Lightly oxidized oolong with a captivating floral aroma reminiscent of fresh orchids and sweet peaches.',
        'price': 38.00,
        'stock': 600,
    },
    {
        'name': 'Da Hong Pao (Big Red Robe)',
        'category': 'Oolong Tea',
        'origin': 'Wuyi Mountains, China',
        'grade': 'FTGFOP',
        'description': 'Legendary heavily roasted cliff oolong. Rich, mineral-heavy, and complex with cocoa and stonefruit undertones.',
        'price': 95.00,
        'stock': 150,
    },

    # White Teas
    {
        'name': 'Silver Needle (Baihao Yinzhen)',
        'category': 'White Tea',
        'origin': 'Fujian, China',
        'grade': 'FTGFOP',
        'description': 'The most prized white tea, consisting of pure downy buds. Light, sweet, and cucumber-fresh.',
        'price': 85.00,
        'stock': 250,
    },
    {
        'name': 'White Peony (Bai Mu Dan)',
        'category': 'White Tea',
        'origin': 'Fujian, China',
        'grade': 'OP',
        'description': 'A blend of silver buds and young tea leaves, offering a slightly bolder, sweet, and floral cup.',
        'price': 40.00,
        'stock': 400,
    },

    # Matcha
    {
        'name': 'Ceremonial Stone-Ground Matcha',
        'category': 'Matcha',
        'origin': 'Uji, Japan',
        'grade': 'MATCHA',
        'description': 'First harvest, shade-grown, stone-ground green tea buds. Incredibly rich umami, vibrant green color.',
        'price': 110.00,
        'stock': 180,
    },
    {
        'name': 'Culinary Grade Matcha Blend',
        'category': 'Matcha',
        'origin': 'Shizuoka, Japan',
        'grade': 'MATCHA',
        'description': 'A bolder matcha flavor designed specifically for lattes, baking, and culinary applications.',
        'price': 45.00,
        'stock': 600,
    },

    # Herbal Infusions
    {
        'name': 'Egyptian Chamomile Blossoms',
        'category': 'Herbal Infusion',
        'origin': 'Fayoum, Egypt',
        'grade': 'FANNINGS',
        'description': 'Whole chamomile heads providing a golden, caffeine-free liquor with soothing apple-like sweet notes.',
        'price': 19.00,
        'stock': 700,
    },
    {
        'name': 'Organic Rooibos Superior',
        'category': 'Herbal Infusion',
        'origin': 'Cederberg, South Africa',
        'grade': 'OP',
        'description': 'Rich, woody, and naturally sweet needle-leaves packed with antioxidants and zero caffeine.',
        'price': 16.50,
        'stock': 900,
    }
]

class Command(BaseCommand):
    help = 'Seeds categories, vendors, and products for sha_Tea marketplace'

    def handle(self, *args, **options):
        self.stdout.write('Checking database and seeding data...')

        # 1. Ensure admin exists
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@shatea.com',
                'role': 'ADMIN',
                'is_staff': True,
                'is_superuser': True,
                'company_name': 'sha_Tea HQ',
            }
        )
        if created:
            admin.set_password('admin')
            admin.save()
            self.stdout.write('Created superuser account: admin/admin')
        else:
            self.stdout.write('Superuser admin already exists')

        # Create a mock vendor account if not exists
        vendor, created = User.objects.get_or_create(
            username='vendor',
            defaults={
                'email': 'vendor@teafarm.com',
                'role': 'VENDOR',
                'company_name': 'Himalayan Organic Tea Estates',
                'phone': '+91-9876543210',
                'address': 'Darjeeling Tea Valley, West Bengal, India'
            }
        )
        if created:
            vendor.set_password('admin')
            vendor.save()
            self.stdout.write('Created vendor account: vendor/admin')

        # Create a mock buyer account if not exists
        buyer, created = User.objects.get_or_create(
            username='buyer',
            defaults={
                'email': 'buyer@cafechain.com',
                'role': 'BUYER',
                'company_name': 'Green Brew Coffee & Tea Chains Inc.',
                'phone': '+1-555-0199',
                'address': '120 Ocean Drive, Miami, FL, USA'
            }
        )
        if created:
            buyer.set_password('admin')
            buyer.save()
            self.stdout.write('Created buyer account: buyer/admin')

        # 2. Seed Categories
        categories_dict = {}
        categories_metadata = [
            ('Black Tea', 'Bold, fully oxidized teas including Darjeeling, Assam, and Earl Grey.', 'ri-cup-line'),
            ('Green Tea', 'Unoxidized teas preserved with steam or pan heat, rich in antioxidants.', 'ri-leaf-line'),
            ('Oolong Tea', 'Semi-oxidized gourmet tea offering complex notes ranging from floral to toasted.', 'ri-water-flash-line'),
            ('White Tea', 'Minimalist, minimally processed buds with delicate and fresh sweetness.', 'ri-windy-line'),
            ('Matcha', 'Shade-grown stone-ground Japanese green tea powder, packing intense umami.', 'ri-magic-line'),
            ('Herbal Infusion', 'Naturally caffeine-free herbal flowers, roots, and dried fruits.', 'ri-seedling-line'),
        ]

        for name, desc, icon in categories_metadata:
            cat, c = Category.objects.get_or_create(
                name=name,
                defaults={'description': desc, 'icon_class': icon}
            )
            categories_dict[name] = cat

        # 3. Seed Products
        product_count = 0
        for item in TEA_SEED_DATA:
            cat_obj = categories_dict[item['category']]
            # Pick a royalty-free image from the list or fallback
            img_list = TEA_IMAGES.get(item['category'], [DEFAULT_IMAGE])
            img_url = random.choice(img_list)

            prod, c = Product.objects.get_or_create(
                name=item['name'],
                category=cat_obj,
                grade=item['grade'],
                defaults={
                    'origin': item['origin'],
                    'description': item['description'],
                    'price': item['price'],
                    'stock': item['stock'],
                    'image_url': img_url,
                    'vendor': vendor
                }
            )
            if c:
                product_count += 1
                # Add a few default reviews
                comments = [
                    ("Excellent quality, leaves look fresh and smell amazing.", 5, "Positive"),
                    ("Strong malty taste. Ideal for our cafe's custom morning blend.", 4, "Positive"),
                    ("Solid tea, but shipping took a day longer than expected.", 3, "Neutral")
                ]
                for comment, rating, sentiment in comments:
                    Review.objects.create(
                        product=prod,
                        buyer=buyer,
                        rating=rating,
                        comment=comment,
                        ai_sentiment=sentiment
                    )

        self.stdout.write(f'Successfully seeded {product_count} new products and categories!')
