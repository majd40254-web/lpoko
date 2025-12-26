"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     🏆 سوق النخبة - ELITE SOUK                                                ║
║     E-Commerce Platform Backend API                                           ║
║     Built with Python Flask                                                   ║
║                                                                               ║
║     Features:                                                                 ║
║     ✓ RESTful API Architecture                                               ║
║     ✓ JWT Authentication                                                      ║
║     ✓ Product Management                                                      ║
║     ✓ Order Processing                                                        ║
║     ✓ Cart Management                                                         ║
║     ✓ User Management                                                         ║
║     ✓ Analytics & Reporting                                                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

from flask import Flask, request, jsonify
from functools import wraps
from datetime import datetime, timedelta
from uuid import uuid4
import hashlib
import hmac
import base64
import json
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'elite-souk-super-secret-key-2024-production'

# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE SIMULATION (In-Memory)
# ═══════════════════════════════════════════════════════════════════════════════

class Database:
    def __init__(self):
        self.users = {}
        self.products = {}
        self.categories = {}
        self.orders = {}
        self.carts = {}
        self.reviews = {}
        self.wishlists = {}
        self.sessions = {}
        self._initialize_data()
    
    def _initialize_data(self):
        """Initialize database with sample data"""
        
        # Categories
        categories_data = [
            {
                'id': str(uuid4()),
                'name': 'الإلكترونيات',
                'name_en': 'Electronics',
                'slug': 'electronics',
                'description': 'أحدث الأجهزة الإلكترونية والتقنية',
                'image': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400',
                'icon': '📱',
                'color': '#3B82F6',
                'is_active': True,
                'sort_order': 1
            },
            {
                'id': str(uuid4()),
                'name': 'الأزياء',
                'name_en': 'Fashion',
                'slug': 'fashion',
                'description': 'أحدث صيحات الموضة العالمية',
                'image': 'https://images.unsplash.com/photo-1445205170230-053b83016050?w=400',
                'icon': '👗',
                'color': '#EC4899',
                'is_active': True,
                'sort_order': 2
            },
            {
                'id': str(uuid4()),
                'name': 'المنزل',
                'name_en': 'Home',
                'slug': 'home',
                'description': 'أثاث ومستلزمات منزلية فاخرة',
                'image': 'https://images.unsplash.com/photo-1484101403633-562f891dc89a?w=400',
                'icon': '🏠',
                'color': '#10B981',
                'is_active': True,
                'sort_order': 3
            },
            {
                'id': str(uuid4()),
                'name': 'الرياضة',
                'name_en': 'Sports',
                'slug': 'sports',
                'description': 'معدات رياضية احترافية',
                'image': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400',
                'icon': '⚽',
                'color': '#F59E0B',
                'is_active': True,
                'sort_order': 4
            },
            {
                'id': str(uuid4()),
                'name': 'الجمال',
                'name_en': 'Beauty',
                'slug': 'beauty',
                'description': 'مستحضرات تجميل وعناية',
                'image': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400',
                'icon': '💄',
                'color': '#8B5CF6',
                'is_active': True,
                'sort_order': 5
            },
            {
                'id': str(uuid4()),
                'name': 'الكتب',
                'name_en': 'Books',
                'slug': 'books',
                'description': 'كتب ومراجع متنوعة',
                'image': 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400',
                'icon': '📚',
                'color': '#EF4444',
                'is_active': True,
                'sort_order': 6
            }
        ]
        
        for cat in categories_data:
            self.categories[cat['id']] = cat
        
        # Get category IDs
        cat_ids = list(self.categories.keys())
        
        # Products
        products_data = [
            # Electronics
            {
                'id': str(uuid4()),
                'name': 'آيفون 15 برو ماكس',
                'name_en': 'iPhone 15 Pro Max',
                'slug': 'iphone-15-pro-max',
                'description': 'أحدث هاتف من آبل مع شريحة A17 Pro الثورية، كاميرا 48 ميجابكسل مع تصوير سينمائي، وإطار من التيتانيوم. تجربة استخدام لا مثيل لها مع أفضل أداء في عالم الهواتف الذكية.',
                'short_description': 'الهاتف الأقوى من آبل',
                'price': 4999,
                'original_price': 5499,
                'currency': 'SAR',
                'category_id': cat_ids[0],
                'images': [
                    'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600',
                    'https://images.unsplash.com/photo-1696446701796-da61225697cc?w=600',
                    'https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=600'
                ],
                'thumbnail': 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=300',
                'stock': 50,
                'sku': 'APL-IP15PM-256',
                'brand': 'Apple',
                'tags': ['هاتف', 'آيفون', 'آبل', 'ذكي', 'تيتانيوم'],
                'specifications': {
                    'الشاشة': '6.7 بوصة Super Retina XDR',
                    'المعالج': 'A17 Pro',
                    'الذاكرة': '256GB',
                    'الكاميرا': '48MP + 12MP + 12MP',
                    'البطارية': '4422 mAh',
                    'نظام التشغيل': 'iOS 17'
                },
                'rating': 4.9,
                'review_count': 2847,
                'sold_count': 12500,
                'is_featured': True,
                'is_active': True,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': str(uuid4()),
                'name': 'ماك بوك برو 16 M3 Max',
                'name_en': 'MacBook Pro 16 M3 Max',
                'slug': 'macbook-pro-16-m3-max',
                'description': 'أقوى لابتوب احترافي في العالم مع شريحة M3 Max. شاشة Liquid Retina XDR مذهلة، أداء خارق للمونتاج والتصميم ثلاثي الأبعاد، وبطارية تدوم حتى 22 ساعة.',
                'short_description': 'قوة خارقة للمحترفين',
                'price': 18999,
                'original_price': 21999,
                'currency': 'SAR',
                'category_id': cat_ids[0],
                'images': [
                    'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600',
                    'https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=600'
                ],
                'thumbnail': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300',
                'stock': 25,
                'sku': 'APL-MBP16-M3MAX',
                'brand': 'Apple',
                'tags': ['لابتوب', 'ماك', 'آبل', 'احترافي', 'M3'],
                'specifications': {
                    'الشاشة': '16.2 بوصة Liquid Retina XDR',
                    'المعالج': 'Apple M3 Max',
                    'الذاكرة': '48GB RAM + 1TB SSD',
                    'الجرافيكس': '40-core GPU',
                    'البطارية': '22 ساعة'
                },
                'rating': 4.95,
                'review_count': 1256,
                'sold_count': 3200,
                'is_featured': True,
                'is_active': True,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': str(uuid4()),
                'name': 'سماعات Sony WH-1000XM5',
                'name_en': 'Sony WH-1000XM5',
                'slug': 'sony-wh-1000xm5',
                'description': 'أفضل سماعات لاسلكية في العالم مع إلغاء ضوضاء لا مثيل له. صوت Hi-Res Audio، راحة فائقة، وبطارية تدوم 30 ساعة.',
                'short_description': 'صوت استثنائي بلا حدود',
                'price': 1499,
                'original_price': 1799,
                'currency': 'SAR',
                'category_id': cat_ids[0],
                'images': [
                    'https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=600',
                    'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600'
                ],
                'thumbnail': 'https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=300',
                'stock': 80,
                'sku': 'SNY-WH1000XM5',
                'brand': 'Sony',
                'tags': ['سماعات', 'لاسلكية', 'سوني', 'إلغاء ضوضاء'],
                'specifications': {
                    'نوع': 'Over-ear لاسلكية',
                    'إلغاء الضوضاء': 'نعم - أفضل في فئتها',
                    'البطارية': '30 ساعة',
                    'الصوت': 'Hi-Res Audio, LDAC',
                    'الوزن': '250 جرام'
                },
                'rating': 4.8,
                'review_count': 3421,
                'sold_count': 8900,
                'is_featured': True,
                'is_active': True,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': str(uuid4()),
                'name': 'ساعة Apple Watch Ultra 2',
                'name_en': 'Apple Watch Ultra 2',
                'slug': 'apple-watch-ultra-2',
                'description': 'الساعة الأكثر تطوراً من آبل للمغامرين والرياضيين. هيكل من التيتانيوم، شاشة أكثر سطوعاً، ودقة GPS لا مثيل لها.',
                'short_description': 'لا حدود لمغامراتك',
                'price': 3699,
                'original_price': 3999,
                'currency': 'SAR',
                'category_id': cat_ids[0],
                'images': [
                    'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=600',
                    'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=600'
                ],
                'thumbnail': 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=300',
                'stock': 35,
                'sku': 'APL-AWU2-49',
                'brand': 'Apple',
                'tags': ['ساعة', 'آبل', 'ذكية', 'رياضة', 'تيتانيوم'],
                'specifications': {
                    'الشاشة': '49mm Always-On Retina',
                    'المادة': 'تيتانيوم Grade 5',
                    'مقاومة الماء': '100 متر',
                    'البطارية': '36 ساعة',
                    'GPS': 'دقة L1 + L5'
                },
                'rating': 4.85,
                'review_count': 1892,
                'sold_count': 4500,
                'is_featured': True,
                'is_active': True,
                'created_at': datetime.now().isoformat()
            },
            # Fashion
            {
                'id': str(uuid4()),
                'name': 'حقيبة Louis Vuitton Neverfull',
                'name_en': 'Louis Vuitton Neverfull MM',
                'slug': 'lv-neverfull-mm',
                'description': 'حقيبة يد أيقونية من لويس فيتون بتصميم Monogram الكلاسيكي. سعة واسعة مع أناقة لا تُضاهى. الرفيق المثالي لكل مناسبة.',
                'short_description': 'أيقونة الأناقة الفرنسية',
                'price': 8999,
                'original_price': 9999,
                'currency': 'SAR',
                'category_id': cat_ids[1],
                'images': [
                    'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600',
                    'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=600'
                ],
                'thumbnail': 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300',
                'stock': 15,
                'sku': 'LV-NVF-MM-MON',
                'brand': 'Louis Vuitton',
                'tags': ['حقيبة', 'فاخرة', 'لويس فيتون', 'جلد'],
                'specifications': {
                    'المادة': 'كانفاس Monogram + جلد طبيعي',
                    'الأبعاد': '31 × 28 × 14 سم',
                    'الإغلاق': 'سحاب داخلي',
                    'الجيوب': 'جيب داخلي + حقيبة صغيرة قابلة للفصل',
                    'بلد الصنع': 'فرنسا'
                },
                'rating': 4.9,
                'review_count': 892,
                'sold_count': 1200,
                'is_featured': True,
                'is_active': True,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': str(uuid4()),
                'name': 'ساعة Rolex Submariner',
                'name_en': 'Rolex Submariner Date',
                'slug': 'rolex-submariner-date',
                'description': 'ساعة الغواصين الأسطورية من رولكس. هيكل من الفولاذ Oystersteel، إطار دوار Cerachrom، ومقاومة للماء حتى 300 متر.',
                'short_description': 'أسطورة تحت الماء',
                'price': 52000,
                'original_price': 55000,
                'currency': 'SAR',
                'category_id': cat_ids[1],
                'images': [
                    'https://images.unsplash.com/photo-1587836374828-4dbafa94cf0e?w=600',
                    'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600'
                ],
                'thumbnail': 'https://images.unsplash.com/photo-1587836374828-4dbafa94cf0e?w=300',
                'stock': 5,
                'sku': 'RLX-SUB-126610LN',
                'brand': 'Rolex',
                'tags': ['ساعة', 'رولكس', 'فاخرة', 'غوص'],
                'specifications': {
                    'القطر': '41 مم',
                    'المادة': 'Oystersteel',
                    'الحركة': '3235 أوتوماتيكية',
                    'مقاومة الماء': '300 متر',
                    'احتياطي الطاقة': '70 ساعة'
                },
                'rating': 5.0,
                'review_count': 234,
                'sold_count': 89,
                'is_featured': True,
                'is_active': True,
                'created_at': datetime.now().isoformat()
            },
            # Home
            {
                'id': str(uuid4()),
                'name': 'كنبة زاوية مودرن',
                'name_en': 'Modern Corner Sofa',
                'slug': 'modern-corner-sofa',
                'description': 'كنبة زاوية فاخرة بتصميم إيطالي معاصر. قماش مخمل فاخر مقاوم للبقع، هيكل خشبي متين، ووسائد مريحة للغاية.',
                'short_description': 'راحة وأناقة في منزلك',
                'price': 12999,
                'original_price': 15999,
                'currency': 'SAR',
                'category_id': cat_ids[2],
                'images': [
                    'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600',
                    'https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=600'
                ],
                'thumbnail': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=300',
                'stock': 12,
                'sku': 'HOM-SOFA-CRN01',
                'brand': 'Elite Home',
                'tags': ['كنبة', 'أثاث', 'غرفة معيشة', 'مودرن'],
                'specifications': {
                    'الأبعاد': '300 × 200 × 85 سم',
                    'المادة': 'مخمل فاخر + خشب زان',
                    'عدد المقاعد': '6 أشخاص',
                    'الألوان': 'رمادي، بيج، أزرق',
                    'الضمان': '5 سنوات'
                },
                'rating': 4.7,
                'review_count': 456,
                'sold_count': 890,
                'is_featured': True,
                'is_active': True,
                'created_at': datetime.now().isoformat()
            },
            # Sports
            {
                'id': str(uuid4()),
                'name': 'جهاز جري Technogym',
                'name_en': 'Technogym Skillrun',
                'slug': 'technogym-skillrun',
                'description': 'جهاز الجري الأكثر تطوراً في العالم من Technogym. شاشة تفاعلية 19 بوصة، برامج تدريب احترافية، وتقنية Biofeedback.',
                'short_description': 'تدريب احترافي في منزلك',
                'price': 45000,
                'original_price': 52000,
                'currency': 'SAR',
                'category_id': cat_ids[3],
                'images': [
                    'https://images.unsplash.com/photo-1576678927484-cc907957088c?w=600',
                    'https://images.unsplash.com/photo-1538805060514-97d9cc17730c?w=600'
                ],
                'thumbnail': 'https://images.unsplash.com/photo-1576678927484-cc907957088c?w=300',
                'stock': 8,
                'sku': 'SPR-TG-SKILLRUN',
                'brand': 'Technogym',
                'tags': ['جري', 'رياضة', 'منزلي', 'احترافي'],
                'specifications': {
                    'السرعة': '0.8 - 30 كم/ساعة',
                    'الميل': '-3% إلى +25%',
                    'الشاشة': '19 بوصة تفاعلية',
                    'البرامج': 'غير محدودة عبر التطبيق',
                    'الحمولة': '180 كجم'
                },
                'rating': 4.9,
                'review_count': 167,
                'sold_count': 234,
                'is_featured': True,
                'is_active': True,
                'created_at': datetime.now().isoformat()
            },
            # Beauty
            {
                'id': str(uuid4()),
                'name': 'مجموعة La Mer الفاخرة',
                'name_en': 'La Mer Luxury Collection',
                'slug': 'la-mer-luxury-collection',
                'description': 'مجموعة العناية الفاخرة من La Mer تشمل الكريم المرطب الأسطوري، سيروم التجديد، وتونر الترطيب. سر جمال نجمات هوليوود.',
                'short_description': 'سر الجمال الخالد',
                'price': 4500,
                'original_price': 5200,
                'currency': 'SAR',
                'category_id': cat_ids[4],
                'images': [
                    'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=600',
                    'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=600'
                ],
                'thumbnail': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=300',
                'stock': 40,
                'sku': 'BTY-LAMER-LUX',
                'brand': 'La Mer',
                'tags': ['عناية', 'بشرة', 'فاخر', 'ترطيب'],
                'specifications': {
                    'المحتويات': 'كريم 60مل + سيروم 30مل + تونر 100مل',
                    'نوع البشرة': 'جميع أنواع البشرة',
                    'المكون الرئيسي': 'Miracle Broth™',
                    'بلد المنشأ': 'الولايات المتحدة'
                },
                'rating': 4.95,
                'review_count': 1234,
                'sold_count': 3400,
                'is_featured': True,
                'is_active': True,
                'created_at': datetime.now().isoformat()
            },
            # Books
            {
                'id': str(uuid4()),
                'name': 'مجموعة كتب ريادة الأعمال',
                'name_en': 'Entrepreneurship Book Collection',
                'slug': 'entrepreneurship-book-collection',
                'description': 'مجموعة من أهم كتب ريادة الأعمال تشمل: The Lean Startup، Zero to One، Think and Grow Rich، وغيرها من الكتب الملهمة.',
                'short_description': 'طريقك نحو النجاح',
                'price': 450,
                'original_price': 650,
                'currency': 'SAR',
                'category_id': cat_ids[5],
                'images': [
                    'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=600',
                    'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=600'
                ],
                'thumbnail': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300',
                'stock': 100,
                'sku': 'BOK-ENT-COL',
                'brand': 'مكتبة النخبة',
                'tags': ['كتب', 'ريادة', 'أعمال', 'نجاح', 'تطوير ذات'],
                'specifications': {
                    'عدد الكتب': '10 كتب',
                    'اللغة': 'إنجليزي',
                    'الغلاف': 'ورقي',
                    'إجمالي الصفحات': '3500+ صفحة'
                },
                'rating': 4.8,
                'review_count': 567,
                'sold_count': 2100,
                'is_featured': True,
                'is_active': True,
                'created_at': datetime.now().isoformat()
            }
        ]
        
        for prod in products_data:
            self.products[prod['id']] = prod
        
        # Create admin user
        admin_id = str(uuid4())
        self.users[admin_id] = {
            'id': admin_id,
            'email': 'admin@elitesouk.com',
            'password': self._hash_password('admin123'),
            'first_name': 'مدير',
            'last_name': 'النظام',
            'phone': '+966500000000',
            'role': 'admin',
            'avatar': None,
            'is_verified': True,
            'is_active': True,
            'addresses': [],
            'created_at': datetime.now().isoformat()
        }
        
        print("✅ Database initialized successfully!")
        print(f"   📦 {len(self.categories)} categories")
        print(f"   🛍️ {len(self.products)} products")
        print(f"   👤 {len(self.users)} users")
    
    def _hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password, hashed):
        """Verify password"""
        return self._hash_password(password) == hashed

# Initialize database
db = Database()

# ═══════════════════════════════════════════════════════════════════════════════
# JWT AUTHENTICATION
# ═══════════════════════════════════════════════════════════════════════════════

def generate_token(user_id):
    """Generate JWT-like token"""
    payload = {
        'user_id': user_id,
        'exp': (datetime.now() + timedelta(days=7)).isoformat()
    }
    payload_json = json.dumps(payload)
    encoded = base64.b64encode(payload_json.encode()).decode()
    signature = hmac.new(
        app.config['SECRET_KEY'].encode(),
        encoded.encode(),
        hashlib.sha256
    ).hexdigest()
    return f"{encoded}.{signature}"

def verify_token(token):
    """Verify JWT-like token"""
    try:
        parts = token.split('.')
        if len(parts) != 2:
            return None
        
        encoded, signature = parts
        expected_sig = hmac.new(
            app.config['SECRET_KEY'].encode(),
            encoded.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature, expected_sig):
            return None
        
        payload_json = base64.b64decode(encoded).decode()
        payload = json.loads(payload_json)
        
        if datetime.fromisoformat(payload['exp']) < datetime.now():
            return None
        
        return payload
    except:
        return None

def auth_required(f):
    """Authentication decorator"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'message': 'غير مصرح. يرجى تسجيل الدخول.',
                'code': 'NO_TOKEN'
            }), 401
        
        token = auth_header.split(' ')[1]
        payload = verify_token(token)
        
        if not payload:
            return jsonify({
                'success': False,
                'message': 'جلسة منتهية. يرجى إعادة تسجيل الدخول.',
                'code': 'INVALID_TOKEN'
            }), 401
        
        user = db.users.get(payload['user_id'])
        if not user or not user['is_active']:
            return jsonify({
                'success': False,
                'message': 'المستخدم غير موجود أو معطل',
                'code': 'USER_NOT_FOUND'
            }), 401
        
        request.user = user
        request.user_id = user['id']
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """Admin authorization decorator"""
    @wraps(f)
    @auth_required
    def decorated(*args, **kwargs):
        if request.user['role'] != 'admin':
            return jsonify({
                'success': False,
                'message': 'صلاحيات المدير مطلوبة',
                'code': 'ADMIN_REQUIRED'
            }), 403
        return f(*args, **kwargs)
    return decorated

# ═══════════════════════════════════════════════════════════════════════════════
# CORS MIDDLEWARE
# ═══════════════════════════════════════════════════════════════════════════════

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        return '', 200

# ═══════════════════════════════════════════════════════════════════════════════
# API ROUTES - HEALTH & INFO
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def home():
    return jsonify({
        'success': True,
        'message': '🏆 مرحباً بك في سوق النخبة API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'products': '/api/products',
            'categories': '/api/categories',
            'cart': '/api/cart',
            'orders': '/api/orders'
        }
    })

@app.route('/health')
def health():
    return jsonify({
        'success': True,
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'stats': {
            'products': len(db.products),
            'categories': len(db.categories),
            'users': len(db.users)
        }
    })

# ═══════════════════════════════════════════════════════════════════════════════
# API ROUTES - AUTHENTICATION
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json or {}
    
    # Validation
    required = ['email', 'password', 'first_name', 'last_name']
    for field in required:
        if not data.get(field):
            return jsonify({
                'success': False,
                'message': f'الحقل {field} مطلوب'
            }), 400
    
    # Check email format
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data['email']):
        return jsonify({
            'success': False,
            'message': 'بريد إلكتروني غير صالح'
        }), 400
    
    # Check if email exists
    for user in db.users.values():
        if user['email'] == data['email']:
            return jsonify({
                'success': False,
                'message': 'البريد الإلكتروني مسجل مسبقاً'
            }), 400
    
    # Create user
    user_id = str(uuid4())
    user = {
        'id': user_id,
        'email': data['email'],
        'password': db._hash_password(data['password']),
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'phone': data.get('phone'),
        'role': 'customer',
        'avatar': None,
        'is_verified': False,
        'is_active': True,
        'addresses': [],
        'created_at': datetime.now().isoformat()
    }
    db.users[user_id] = user
    
    # Create cart
    cart_id = str(uuid4())
    db.carts[cart_id] = {
        'id': cart_id,
        'user_id': user_id,
        'items': [],
        'created_at': datetime.now().isoformat()
    }
    
    # Generate token
    token = generate_token(user_id)
    
    # Return user without password
    user_response = {k: v for k, v in user.items() if k != 'password'}
    
    return jsonify({
        'success': True,
        'message': 'تم إنشاء الحساب بنجاح',
        'data': {
            'user': user_response,
            'token': token
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    
    if not data.get('email') or not data.get('password'):
        return jsonify({
            'success': False,
            'message': 'البريد الإلكتروني وكلمة المرور مطلوبان'
        }), 400
    
    # Find user
    user = None
    for u in db.users.values():
        if u['email'] == data['email']:
            user = u
            break
    
    if not user or not db.verify_password(data['password'], user['password']):
        return jsonify({
            'success': False,
            'message': 'بيانات الدخول غير صحيحة'
        }), 401
    
    if not user['is_active']:
        return jsonify({
            'success': False,
            'message': 'الحساب معطل'
        }), 401
    
    # Generate token
    token = generate_token(user['id'])
    
    # Return user without password
    user_response = {k: v for k, v in user.items() if k != 'password'}
    
    return jsonify({
        'success': True,
        'message': 'تم تسجيل الدخول بنجاح',
        'data': {
            'user': user_response,
            'token': token
        }
    })

@app.route('/api/auth/me')
@auth_required
def get_me():
    user_response = {k: v for k, v in request.user.items() if k != 'password'}
    return jsonify({
        'success': True,
        'data': {'user': user_response}
    })

# ═══════════════════════════════════════════════════════════════════════════════
# API ROUTES - CATEGORIES
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/api/categories')
def get_categories():
    categories = [c for c in db.categories.values() if c['is_active']]
    categories.sort(key=lambda x: x['sort_order'])
    
    # Add product count
    for cat in categories:
        cat['product_count'] = len([
            p for p in db.products.values() 
            if p['category_id'] == cat['id'] and p['is_active']
        ])
    
    return jsonify({
        'success': True,
        'data': {'categories': categories}
    })

@app.route('/api/categories/<slug>')
def get_category(slug):
    category = None
    for c in db.categories.values():
        if c['slug'] == slug or c['id'] == slug:
            category = c
            break
    
    if not category:
        return jsonify({
            'success': False,
            'message': 'التصنيف غير موجود'
        }), 404
    
    return jsonify({
        'success': True,
        'data': {'category': category}
    })

# ═══════════════════════════════════════════════════════════════════════════════
# API ROUTES - PRODUCTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/api/products')
def get_products():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 12))
    sort = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')
    category = request.args.get('category')
    search = request.args.get('search', '').lower()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    featured = request.args.get('featured')
    
    # Filter products
    products = [p for p in db.products.values() if p['is_active']]
    
    # Filter by category
    if category:
        cat = None
        for c in db.categories.values():
            if c['slug'] == category or c['id'] == category:
                cat = c
                break
        if cat:
            products = [p for p in products if p['category_id'] == cat['id']]
    
    # Filter by search
    if search:
        products = [
            p for p in products 
            if search in p['name'].lower() or 
               search in p['name_en'].lower() or
               search in p.get('description', '').lower() or
               any(search in tag.lower() for tag in p.get('tags', []))
        ]
    
    # Filter by price
    if min_price is not None:
        products = [p for p in products if p['price'] >= min_price]
    if max_price is not None:
        products = [p for p in products if p['price'] <= max_price]
    
    # Filter featured
    if featured == 'true':
        products = [p for p in products if p['is_featured']]
    
    # Sort
    reverse = order == 'desc'
    if sort == 'price':
        products.sort(key=lambda x: x['price'], reverse=reverse)
    elif sort == 'rating':
        products.sort(key=lambda x: x['rating'], reverse=reverse)
    elif sort == 'sold_count':
        products.sort(key=lambda x: x['sold_count'], reverse=reverse)
    elif sort == 'name':
        products.sort(key=lambda x: x['name'], reverse=reverse)
    else:
        products.sort(key=lambda x: x['created_at'], reverse=True)
    
    # Pagination
    total = len(products)
    start = (page - 1) * limit
    end = start + limit
    paginated = products[start:end]
    
    # Add category info
    for p in paginated:
        cat = db.categories.get(p['category_id'])
        p['category'] = {
            'id': cat['id'],
            'name': cat['name'],
            'slug': cat['slug']
        } if cat else None
    
    return jsonify({
        'success': True,
        'data': {
            'products': paginated,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit,
                'has_next': end < total,
                'has_prev': page > 1
            }
        }
    })

@app.route('/api/products/featured')
def get_featured_products():
    limit = int(request.args.get('limit', 8))
    products = [
        p for p in db.products.values() 
        if p['is_active'] and p['is_featured']
    ]
    products.sort(key=lambda x: x['sold_count'], reverse=True)
    return jsonify({
        'success': True,
        'data': {'products': products[:limit]}
    })

@app.route('/api/products/deals')
def get_deal_products():
    limit = int(request.args.get('limit', 8))
    products = [
        p for p in db.products.values() 
        if p['is_active'] and p.get('original_price') and p['original_price'] > p['price']
    ]
    # Sort by discount percentage
    for p in products:
        p['discount_percent'] = round((p['original_price'] - p['price']) / p['original_price'] * 100)
    products.sort(key=lambda x: x['discount_percent'], reverse=True)
    return jsonify({
        'success': True,
        'data': {'products': products[:limit]}
    })

@app.route('/api/products/<slug>')
def get_product(slug):
    product = None
    for p in db.products.values():
        if (p['slug'] == slug or p['id'] == slug) and p['is_active']:
            product = p.copy()
            break
    
    if not product:
        return jsonify({
            'success': False,
            'message': 'المنتج غير موجود'
        }), 404
    
    # Add category
    cat = db.categories.get(product['category_id'])
    product['category'] = {
        'id': cat['id'],
        'name': cat['name'],
        'slug': cat['slug']
    } if cat else None
    
    # Get related products
    related = [
        p for p in db.products.values()
        if p['category_id'] == product['category_id'] and 
           p['id'] != product['id'] and 
           p['is_active']
    ][:4]
    
    return jsonify({
        'success': True,
        'data': {
            'product': product,
            'related_products': related
        }
    })

# ═══════════════════════════════════════════════════════════════════════════════
# API ROUTES - CART
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/api/cart')
@auth_required
def get_cart():
    cart = None
    for c in db.carts.values():
        if c['user_id'] == request.user_id:
            cart = c
            break
    
    if not cart:
        cart_id = str(uuid4())
        cart = {
            'id': cart_id,
            'user_id': request.user_id,
            'items': [],
            'created_at': datetime.now().isoformat()
        }
        db.carts[cart_id] = cart
    
    # Populate product details
    items_with_products = []
    subtotal = 0
    
    for item in cart['items']:
        product = db.products.get(item['product_id'])
        if product and product['is_active']:
            item_total = product['price'] * item['quantity']
            subtotal += item_total
            items_with_products.append({
                **item,
                'product': {
                    'id': product['id'],
                    'name': product['name'],
                    'price': product['price'],
                    'original_price': product.get('original_price'),
                    'thumbnail': product['thumbnail'],
                    'slug': product['slug'],
                    'stock': product['stock']
                },
                'total': item_total
            })
    
    return jsonify({
        'success': True,
        'data': {
            'cart': {
                **cart,
                'items': items_with_products,
                'subtotal': subtotal,
                'item_count': sum(item['quantity'] for item in items_with_products)
            }
        }
    })

@app.route('/api/cart/add', methods=['POST'])
@auth_required
def add_to_cart():
    data = request.json or {}
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    
    if not product_id:
        return jsonify({
            'success': False,
            'message': 'معرف المنتج مطلوب'
        }), 400
    
    product = db.products.get(product_id)
    if not product or not product['is_active']:
        return jsonify({
            'success': False,
            'message': 'المنتج غير متاح'
        }), 404
    
    if product['stock'] < quantity:
        return jsonify({
            'success': False,
            'message': f'الكمية المتاحة: {product["stock"]}'
        }), 400
    
    # Find or create cart
    cart = None
    for c in db.carts.values():
        if c['user_id'] == request.user_id:
            cart = c
            break
    
    if not cart:
        cart_id = str(uuid4())
        cart = {
            'id': cart_id,
            'user_id': request.user_id,
            'items': [],
            'created_at': datetime.now().isoformat()
        }
        db.carts[cart_id] = cart
    
    # Check if product already in cart
    found = False
    for item in cart['items']:
        if item['product_id'] == product_id:
            new_qty = item['quantity'] + quantity
            if new_qty > product['stock']:
                return jsonify({
                    'success': False,
                    'message': f'الكمية المتاحة: {product["stock"]}'
                }), 400
            item['quantity'] = new_qty
            found = True
            break
    
    if not found:
        cart['items'].append({
            'product_id': product_id,
            'quantity': quantity,
            'added_at': datetime.now().isoformat()
        })
    
    return jsonify({
        'success': True,
        'message': 'تمت الإضافة إلى السلة'
    })

@app.route('/api/cart/update', methods=['PUT'])
@auth_required
def update_cart_item():
    data = request.json or {}
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 0))
    
    cart = None
    for c in db.carts.values():
        if c['user_id'] == request.user_id:
            cart = c
            break
    
    if not cart:
        return jsonify({
            'success': False,
            'message': 'السلة فارغة'
        }), 404
    
    if quantity <= 0:
        # Remove item
        cart['items'] = [i for i in cart['items'] if i['product_id'] != product_id]
    else:
        # Update quantity
        for item in cart['items']:
            if item['product_id'] == product_id:
                product = db.products.get(product_id)
                if product and quantity > product['stock']:
                    return jsonify({
                        'success': False,
                        'message': f'الكمية المتاحة: {product["stock"]}'
                    }), 400
                item['quantity'] = quantity
                break
    
    return jsonify({
        'success': True,
        'message': 'تم تحديث السلة'
    })

@app.route('/api/cart/clear', methods=['DELETE'])
@auth_required
def clear_cart():
    for cart in db.carts.values():
        if cart['user_id'] == request.user_id:
            cart['items'] = []
            break
    
    return jsonify({
        'success': True,
        'message': 'تم تفريغ السلة'
    })

# ═══════════════════════════════════════════════════════════════════════════════
# API ROUTES - ORDERS
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/api/orders')
@auth_required
def get_orders():
    if request.user['role'] == 'admin':
        orders = list(db.orders.values())
    else:
        orders = [o for o in db.orders.values() if o['user_id'] == request.user_id]
    
    orders.sort(key=lambda x: x['created_at'], reverse=True)
    
    return jsonify({
        'success': True,
        'data': {'orders': orders}
    })

@app.route('/api/orders/<order_id>')
@auth_required
def get_order(order_id):
    order = db.orders.get(order_id)
    
    if not order:
        return jsonify({
            'success': False,
            'message': 'الطلب غير موجود'
        }), 404
    
    if request.user['role'] != 'admin' and order['user_id'] != request.user_id:
        return jsonify({
            'success': False,
            'message': 'غير مصرح'
        }), 403
    
    return jsonify({
        'success': True,
        'data': {'order': order}
    })

@app.route('/api/orders', methods=['POST'])
@auth_required
def create_order():
    data = request.json or {}
    
    # Validate shipping address
    shipping = data.get('shipping_address', {})
    required_fields = ['full_name', 'phone', 'city', 'address']
    for field in required_fields:
        if not shipping.get(field):
            return jsonify({
                'success': False,
                'message': f'الحقل {field} مطلوب في عنوان الشحن'
            }), 400
    
    # Get cart
    cart = None
    for c in db.carts.values():
        if c['user_id'] == request.user_id:
            cart = c
            break
    
    if not cart or not cart['items']:
        return jsonify({
            'success': False,
            'message': 'السلة فارغة'
        }), 400
    
    # Process items
    items = []
    subtotal = 0
    
    for cart_item in cart['items']:
        product = db.products.get(cart_item['product_id'])
        if not product or not product['is_active']:
            return jsonify({
                'success': False,
                'message': f'المنتج غير متاح'
            }), 400
        
        if product['stock'] < cart_item['quantity']:
            return jsonify({
                'success': False,
                'message': f'المنتج "{product["name"]}" غير متوفر بالكمية المطلوبة'
            }), 400
        
        item_total = product['price'] * cart_item['quantity']
        subtotal += item_total
        
        items.append({
            'product_id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'quantity': cart_item['quantity'],
            'total': item_total,
            'thumbnail': product['thumbnail']
        })
        
        # Update stock
        product['stock'] -= cart_item['quantity']
        product['sold_count'] += cart_item['quantity']
    
    # Calculate totals
    shipping_cost = 0 if subtotal >= 500 else 30
    tax = round(subtotal * 0.15, 2)
    total = subtotal + tax + shipping_cost
    
    # Create order
    order_id = str(uuid4())
    order_number = f"ES-{datetime.now().strftime('%Y%m%d')}-{order_id[:8].upper()}"
    
    order = {
        'id': order_id,
        'order_number': order_number,
        'user_id': request.user_id,
        'items': items,
        'shipping_address': shipping,
        'payment_method': data.get('payment_method', 'cash'),
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'tax': tax,
        'total': round(total, 2),
        'status': 'pending',
        'status_label': 'قيد الانتظار',
        'notes': data.get('notes'),
        'created_at': datetime.now().isoformat()
    }
    
    db.orders[order_id] = order
    
    # Clear cart
    cart['items'] = []
    
    return jsonify({
        'success': True,
        'message': 'تم إنشاء الطلب بنجاح',
        'data': {'order': order}
    }), 201

@app.route('/api/orders/<order_id>/status', methods=['PUT'])
@admin_required
def update_order_status(order_id):
    order = db.orders.get(order_id)
    if not order:
        return jsonify({
            'success': False,
            'message': 'الطلب غير موجود'
        }), 404
    
    data = request.json or {}
    status = data.get('status')
    
    status_labels = {
        'pending': 'قيد الانتظار',
        'confirmed': 'تم التأكيد',
        'processing': 'قيد التحضير',
        'shipped': 'تم الشحن',
        'delivered': 'تم التسليم',
        'cancelled': 'ملغي'
    }
    
    if status not in status_labels:
        return jsonify({
            'success': False,
            'message': 'حالة غير صالحة'
        }), 400
    
    order['status'] = status
    order['status_label'] = status_labels[status]
    order['updated_at'] = datetime.now().isoformat()
    
    return jsonify({
        'success': True,
        'message': 'تم تحديث حالة الطلب',
        'data': {'order': order}
    })

# ═══════════════════════════════════════════════════════════════════════════════
# API ROUTES - ANALYTICS (Admin)
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/api/analytics/dashboard')
@admin_required
def get_dashboard_analytics():
    # Calculate stats
    total_revenue = sum(o['total'] for o in db.orders.values() if o['status'] != 'cancelled')
    total_orders = len(db.orders)
    total_products = len([p for p in db.products.values() if p['is_active']])
    total_users = len([u for u in db.users.values() if u['role'] == 'customer'])
    
    # Recent orders
    recent_orders = sorted(
        db.orders.values(),
        key=lambda x: x['created_at'],
        reverse=True
    )[:5]
    
    # Top products
    top_products = sorted(
        [p for p in db.products.values() if p['is_active']],
        key=lambda x: x['sold_count'],
        reverse=True
    )[:5]
    
    return jsonify({
        'success': True,
        'data': {
            'stats': {
                'total_revenue': total_revenue,
                'total_orders': total_orders,
                'total_products': total_products,
                'total_users': total_users
            },
            'recent_orders': recent_orders,
            'top_products': top_products
        }
    })

# ═══════════════════════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'message': 'المسار غير موجود',
        'code': 'NOT_FOUND'
    }), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({
        'success': False,
        'message': 'خطأ في الخادم',
        'code': 'SERVER_ERROR'
    }), 500

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     🏆 سوق النخبة - ELITE SOUK API                                            ║
║     Server running on http://localhost:5000                                   ║
║                                                                               ║
║     Endpoints:                                                                ║
║     • GET  /health              - Health check                                ║
║     • POST /api/auth/register   - Register user                               ║
║     • POST /api/auth/login      - Login user                                  ║
║     • GET  /api/categories      - Get categories                              ║
║     • GET  /api/products        - Get products                                ║
║     • GET  /api/cart            - Get cart                                    ║
║     • POST /api/orders          - Create order                                ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=True)
