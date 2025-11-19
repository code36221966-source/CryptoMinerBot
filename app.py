from flask import Flask, render_template, request, jsonify
import database as db  # This imports your database.py file

app = Flask(__name__)

# Initialize the database when the server starts
db.init_db()

@app.route('/')
def home():
    # This will show the website (we will build index.html next)
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"success": False, "message": "Missing fields"})

    # Call the function we wrote in database.py
    success, msg = db.add_user(username, email, password)
    return jsonify({"success": success, "message": msg})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = db.verify_user(data.get('username'), data.get('password'))
    
    if user:
        # Remove the password hash before sending back to user (Security)
        del user['password_hash']
        return jsonify({"success": True, "user": user})
    
    return jsonify({"success": False, "message": "Invalid username or password"})

if __name__ == '__main__':
    # Run the server on Port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
