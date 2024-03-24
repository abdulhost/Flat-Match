from flask import Flask, render_template, request, redirect, url_for, session
# from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL Configuration
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'your_username'
# app.config['MYSQL_PASSWORD'] = 'your_password'
# app.config['MYSQL_DB'] = 'your_database_name'

# mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration logic
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if 'username' in session:
        # Fetch user data and display dashboard
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/search')
def search():
    # Fetch available properties from database and display search results
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
