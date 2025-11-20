from flask import Flask, render_template, request, jsonify
import database as db
import smtplib
import random
from email.mime.text import MIMEText

app = Flask(__name__)

# --- EMAIL CONFIGURATION ---
# 🔴 REPLACE THESE WITH YOUR ACTUAL GMAIL DETAILS
SMTP_EMAIL = "globaltrustverify@gmail.com"
SMTP_PASSWORD = "mwdp bpzu llel vwmw" 

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

@app.route('/verify')
def verify_page():
    # We will create this file next
    return render_template('verify.html')

# --- HELPER FUNCTIONS ---

def generate_code():
    """Generates a 6-digit random code"""
    return str(random.randint(100000, 999999))

def send_email(to_email, code):
    """Sends the verification code via Gmail"""
    try:
        msg = MIMEText(f"Hello! Your verification code is: {code}")
        msg['Subject'] = "CryptoMiner Verification Code"
        msg['From'] = SMTP_EMAIL
        msg['To'] = to_email

        # Connect to Gmail (SSL)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Email Error: {e}")
        return False

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
    
    # Generate Verification Code
    code = generate_code()
        
    # Save to DB (Now includes code)
    success, msg = db.add_user(username, email, first_name, last_name, country, phone, password, code)
    
    if success:
        # Send Email
        email_status = send_email(email, code)
        if email_status:
            return jsonify({"success": True, "message": "Registration Successful! Check your email for the code."})
        else:
            return jsonify({"success": True, "message": "Registered, but failed to send email. Contact support."})
            
    return jsonify({"success": success, "message": msg})

@app.route('/api/verify_code', methods=['POST'])
def verify_code_api():
    data = request.json
    email = data.get('email')
    code = data.get('code')
    
    success, msg = db.activate_account(email, code)
    return jsonify({"success": success, "message": msg})

@app.route('/api/login', methods=['POST'])
def login_api():
    data = request.json
    
    # Verify using EMAIL and PASSWORD
    user = db.verify_user(data.get('email'), data.get('password'))
    
    if user:
        # Check if Verified
        if user['is_verified'] == 0:
             return jsonify({"success": False, "message": "Account not verified. Please check your email."})

        del user['password_hash'] # Security
        return jsonify({"success": True, "user": user})
    
    return jsonify({"success": False, "message": "Invalid email or password"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
