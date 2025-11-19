from flask import Flask, render_template, request, jsonify
import database as db

app = Flask(__name__)

# Initialize database immediately
db.init_db()

# --- PAGE ROUTES (Navigation) ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

# --- API ROUTES (Data) ---

@app.route('/api/register', methods=['POST'])
def register_api():
    data = request.json
    
    # Extract all fields
    username = data.get('username')
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    country = data.get('country')
    phone = data.get('phone')
    password = data.get('password')

    # Validation
    if not username or not email or not password:
        return jsonify({"success": False, "message": "Missing required fields"})
        
    # Save to DB
    success, msg = db.add_user(username, email, first_name, last_name, country, phone, password)
    return jsonify({"success": success, "message": msg})

@app.route('/api/login', methods=['POST'])
def login_api():
    data = request.json
    
    # Verify using EMAIL and PASSWORD
    user = db.verify_user(data.get('email'), data.get('password'))
    
    if user:
        del user['password_hash'] # Security
        return jsonify({"success": True, "user": user})
    
    return jsonify({"success": False, "message": "Invalid email or password"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
