import os
import json
import uuid
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, jsonify
)
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "reuse_eco_secret_key_2026")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'images')
DATA_FILE = os.path.join(BASE_DIR, 'reuse_data.json')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------------------------------------------
# Database Persistence & Initial Seed
# -------------------------------------------------------------
DEFAULT_SEED = {
    "stats": {
        "products_available": 142,
        "products_reused": 856,
        "total_donations": 524,
        "pending_requests": 19,
        "registered_users": 1280,
        "waste_diverted_kg": 14820.0,
        "co2_saved_tons": 22.4,
        "barter_swaps": 332
    },
    "products": [
        {
            "id": "p1",
            "name": "Solid Oak Study & Work Desk",
            "category": "Furniture",
            "condition": "Good",
            "type": "donation",
            "looking_for": "",
            "weight": 18.0,
            "location": "Green Park Eco Zone",
            "owner": "Sarah Green",
            "owner_email": "sarah.green@example.org",
            "description": "Sturdy wooden desk with 2 storage drawers. Perfect for remote study or work.",
            "image": "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?auto=format&fit=crop&w=600&q=80",
            "status": "Available",
            "date": "2026-11-10",
            "requests_count": 2
        },
        {
            "id": "p2",
            "name": "Sony Noise-Cancelling Headphones",
            "category": "Electronics",
            "condition": "Good",
            "type": "exchange",
            "looking_for": "Mechanical keyboard or guitar pedal",
            "weight": 0.35,
            "location": "Downtown Eco Hub",
            "owner": "Michael Chang",
            "owner_email": "m.chang@example.org",
            "description": "WH-1000XM3 series in solid black. Great battery life over 22h. Includes USB-C cable.",
            "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80",
            "status": "Available",
            "date": "2026-11-09",
            "requests_count": 4
        },
        {
            "id": "p3",
            "name": "Vintage Winter Corduroy Overcoat",
            "category": "Clothes",
            "condition": "Good",
            "type": "donation",
            "looking_for": "",
            "weight": 1.1,
            "location": "Westfield Suburb",
            "owner": "Elena Rostova",
            "owner_email": "elena.r@example.org",
            "description": "Warm olive-green winter coat, unisex medium size. Clean and freshly dry cleaned.",
            "image": "https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=600&q=80",
            "status": "Available",
            "date": "2026-11-08",
            "requests_count": 1
        },
        {
            "id": "p4",
            "name": "Fundamentals of Physics Textbooks (Set of 3)",
            "category": "Books",
            "condition": "New",
            "type": "donation",
            "looking_for": "",
            "weight": 2.8,
            "location": "University District",
            "owner": "Sarah Green",
            "owner_email": "sarah.green@example.org",
            "description": "Halliday & Resnick physics fundamentals with solutions. Clean with zero markings.",
            "image": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80",
            "status": "Available",
            "date": "2026-11-07",
            "requests_count": 3
        },
        {
            "id": "p5",
            "name": "Philips Compact Espresso Maker",
            "category": "Household",
            "condition": "Good",
            "type": "exchange",
            "looking_for": "Stainless steel blender or air fryer",
            "weight": 4.2,
            "location": "Southside Gardens",
            "owner": "Marcus Vance",
            "owner_email": "marcus.v@example.org",
            "description": "15-bar pump espresso maker with milk steam wand. Freshly descaled and working well.",
            "image": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?auto=format&fit=crop&w=600&q=80",
            "status": "Available",
            "date": "2026-11-06",
            "requests_count": 5
        },
        {
            "id": "p6",
            "name": "Dell 24-inch IPS Monitor",
            "category": "Electronics",
            "condition": "Good",
            "type": "donation",
            "looking_for": "",
            "weight": 5.4,
            "location": "Central Tech Quarter",
            "owner": "Sarah Green",
            "owner_email": "sarah.green@example.org",
            "description": "Full HD 1080p with HDMI and DisplayPort inputs. Adjustable stand. Great for home office.",
            "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=600&q=80",
            "status": "Available",
            "date": "2026-11-04",
            "requests_count": 6
        }
    ],
    "requests": [
        {
            "id": "req-1",
            "product_id": "p1",
            "product_name": "Solid Oak Study & Work Desk",
            "requester_name": "David Miller",
            "requester_email": "david.m@example.org",
            "owner_name": "Sarah Green",
            "message": "Hello! My son really needs a solid desk for high school studies. Can pick up Saturday.",
            "date": "2026-11-10",
            "status": "Pending"
        },
        {
            "id": "req-2",
            "product_id": "p2",
            "product_name": "Sony Noise-Cancelling Headphones",
            "requester_name": "Sarah Green",
            "requester_email": "sarah.green@example.org",
            "owner_name": "Michael Chang",
            "message": "Offering my mechanical keyboard in swap! Works cleanly.",
            "date": "2026-11-09",
            "status": "Approved"
        }
    ],
    "users": [
        {"name": "Sarah Green", "email": "sarah.green@example.org", "password": "password123", "role": "user", "tier": "Eco Champion"},
        {"name": "Admin Moderator", "email": "admin@reuse-ims.org", "password": "adminpassword", "role": "admin", "tier": "System Admin"}
    ],
    "activities": [
        {"title": "New Reuse Request", "desc": "David Miller requested Solid Oak Study Desk", "time": "2h ago", "icon": "fa-solid fa-paper-plane", "type": "request"},
        {"title": "Trade Approved", "desc": "Michael Chang accepted trade for Sony Headphones", "time": "5h ago", "icon": "fa-solid fa-repeat", "type": "exchange"},
        {"title": "Donation Completed", "desc": "Winter Coat handed over to local family", "time": "1d ago", "icon": "fa-solid fa-circle-check", "type": "donation"}
    ]
}

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_SEED)
        return DEFAULT_SEED
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {DATA_FILE}: {e}")
        return DEFAULT_SEED

def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving {DATA_FILE}: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Current user helper
def get_current_user():
    user_email = session.get('user_email')
    if not user_email:
        # Default mock login session for smooth experience
        return {
            "name": "Sarah Green",
            "email": "sarah.green@example.org",
            "role": "user",
            "tier": "Eco Champion"
        }
    data = load_data()
    for u in data.get('users', []):
        if u['email'] == user_email:
            return u
    return {"name": "Guest User", "email": user_email, "role": "user", "tier": "Eco Starter"}

# -------------------------------------------------------------
# Web Routes
# -------------------------------------------------------------

@app.route('/')
@app.route('/dashboard')
def index():
    data = load_data()
    user = get_current_user()
    
    # Calculate live stats
    products = data.get('products', [])
    available_count = len([p for p in products if p.get('status') == 'Available'])
    reused_count = data['stats']['products_reused'] + len([p for p in products if p.get('status') == 'Reused'])
    donations_count = data['stats']['total_donations'] + len([p for p in products if p.get('type') == 'donation'])
    pending_count = len([r for r in data.get('requests', []) if r.get('status') == 'Pending'])
    
    stats = {
        "products_available": available_count,
        "products_reused": reused_count,
        "total_donations": donations_count,
        "pending_requests": pending_count,
        "registered_users": data['stats']['registered_users'],
        "waste_diverted_kg": data['stats']['waste_diverted_kg'],
        "co2_saved_tons": data['stats']['co2_saved_tons'],
        "barter_swaps": data['stats']['barter_swaps']
    }
    
    recent_products = products[:4]
    activities = data.get('activities', [])[:5]
    
    return render_template(
        'index.html',
        stats=stats,
        recent_products=recent_products,
        activities=activities,
        user=user
    )

@app.route('/products')
def products():
    data = load_data()
    user = get_current_user()
    all_products = data.get('products', [])
    
    category = request.args.get('category', 'all')
    condition = request.args.get('condition', 'all')
    item_type = request.args.get('type', 'all')
    search_q = request.args.get('q', '').strip().lower()
    
    filtered = all_products
    if category != 'all':
        filtered = [p for p in filtered if p.get('category') == category]
    if condition != 'all':
        filtered = [p for p in filtered if p.get('condition') == condition]
    if item_type != 'all':
        filtered = [p for p in filtered if p.get('type') == item_type]
    if search_q:
        filtered = [
            p for p in filtered
            if search_q in p.get('name', '').lower()
            or search_q in p.get('description', '').lower()
            or search_q in p.get('location', '').lower()
        ]
        
    return render_template(
        'products.html',
        products=filtered,
        user=user,
        active_category=category,
        active_condition=condition,
        active_type=item_type,
        search_query=search_q,
        total_count=len(filtered)
    )

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    user = get_current_user()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        condition = request.form.get('condition', 'Good').strip()
        item_type = request.form.get('type', 'donation').strip()
        looking_for = request.form.get('looking_for', '').strip()
        location = request.form.get('location', '').strip()
        description = request.form.get('description', '').strip()
        weight = float(request.form.get('weight', 2.0) or 2.0)
        
        # Handle file upload or image url
        image_url = request.form.get('preset_image', '')
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and allowed_file(file.filename):
                fname = secure_filename(file.filename)
                unique_fname = f"{uuid.uuid4().hex[:8]}_{fname}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_fname))
                image_url = url_for('static', filename=f'images/{unique_fname}')
                
        if not image_url:
            image_url = "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?auto=format&fit=crop&w=600&q=80"
            
        data = load_data()
        new_prod = {
            "id": f"p{int(datetime.now().timestamp())}",
            "name": name,
            "category": category,
            "condition": condition,
            "type": item_type,
            "looking_for": looking_for,
            "weight": weight,
            "location": location,
            "owner": user['name'],
            "owner_email": user['email'],
            "description": description,
            "image": image_url,
            "status": "Available",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "requests_count": 0
        }
        
        data['products'].insert(0, new_prod)
        data['stats']['waste_diverted_kg'] += weight
        data['activities'].insert(0, {
            "title": f"New {item_type.capitalize()} Listed",
            "desc": f"{user['name']} listed '{name}' in {category}",
            "time": "Just now",
            "icon": "fa-solid fa-gift" if item_type == 'donation' else "fa-solid fa-repeat",
            "type": item_type
        })
        
        save_data(data)
        flash(f"Success! '{name}' has been added to the REUSE catalog.", "success")
        return redirect(url_for('products'))
        
    return render_template('add_product.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        data = load_data()
        for u in data.get('users', []):
            if u['email'] == email and u['password'] == password:
                session['user_email'] = u['email']
                session['user_name'] = u['name']
                session['user_role'] = u['role']
                flash(f"Welcome back, {u['name']}!", "success")
                return redirect(url_for('index'))
                
        # If user not found, auto-create or mock login for ease of review
        session['user_email'] = email
        session['user_name'] = email.split('@')[0].capitalize()
        session['user_role'] = "admin" if "admin" in email.lower() else "user"
        flash(f"Signed in as {session['user_name']}", "info")
        return redirect(url_for('index'))
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        data = load_data()
        data.setdefault('users', [])
        # Check existing
        for u in data['users']:
            if u['email'] == email:
                flash("An account with that email already exists. Please log in.", "warning")
                return redirect(url_for('login'))
                
        new_u = {
            "name": name,
            "email": email,
            "password": password,
            "role": "user",
            "tier": "Eco Starter"
        }
        data['users'].append(new_u)
        data['stats']['registered_users'] += 1
        save_data(data)
        
        session['user_email'] = email
        session['user_name'] = name
        session['user_role'] = "user"
        flash("Registration successful! Welcome to the REUSE community.", "success")
        return redirect(url_for('index'))
        
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for('login'))

@app.route('/request_item', methods=['POST'])
def request_item():
    user = get_current_user()
    prod_id = request.form.get('product_id')
    message = request.form.get('message', '').strip()
    contact = request.form.get('contact', '').strip()
    
    data = load_data()
    prod = next((p for p in data.get('products', []) if p['id'] == prod_id), None)
    if not prod:
        flash("Product not found.", "danger")
        return redirect(url_for('products'))
        
    new_req = {
        "id": f"req-{int(datetime.now().timestamp())}",
        "product_id": prod['id'],
        "product_name": prod['name'],
        "requester_name": user['name'],
        "requester_email": user['email'],
        "owner_name": prod['owner'],
        "message": f"{message} (Contact: {contact})",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": "Pending"
    }
    
    prod['status'] = "Requested"
    prod['requests_count'] = prod.get('requests_count', 0) + 1
    data.setdefault('requests', []).insert(0, new_req)
    data.setdefault('activities', []).insert(0, {
        "title": "New Reuse Request",
        "desc": f"{user['name']} requested '{prod['name']}'",
        "time": "Just now",
        "icon": "fa-solid fa-paper-plane",
        "type": "request"
    })
    
    save_data(data)
    flash(f"Your reuse request for '{prod['name']}' was sent successfully!", "success")
    return redirect(url_for('products'))

@app.route('/api/stats')
def api_stats():
    data = load_data()
    return jsonify(data.get('stats', {}))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🌱 REUSE Flask IMS running at: http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)

