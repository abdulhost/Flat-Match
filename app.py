from flask import Flask, jsonify, render_template, request, redirect, url_for, session,flash
import sqlite3
from math import radians, sin, cos, sqrt, atan2
import json
import uuid
from werkzeug.utils import secure_filename

import os
app = Flask(__name__)
app.secret_key = "1154"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dummy.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

def create_tables():
    conn = sqlite3.connect('dummy.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS Room (
                 id INTEGER PRIMARY KEY,
                 address TEXT,
                 description TEXT,
                 latitude REAL,
                 longitude REAL,
                images TEXT
                 )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Roommate (
                id INTEGER PRIMARY KEY,
                address TEXT,   
                gender TEXT,
                description TEXT,
                contact TEXT,
                latitude REAL,
                longitude REAL
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
              email TEXT,
              password REAl
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS contact (
                id INTEGER PRIMARY KEY,
                name TEXT,
              email TEXT,
              message TEXT
                 )''')

    conn.commit()
    conn.close()

def insert_dummy_data():
    conn = sqlite3.connect('dummy.db')
    c = conn.cursor()

    # Check if the Room table is empty before inserting
    c.execute("SELECT COUNT(*) FROM Room")
    count = c.fetchone()[0]
    if count == 0:
        c.execute("INSERT INTO Room (address, description, latitude, longitude) VALUES (?, ?, ?, ?)", 
                  ('Gali Number 23, Tugalkabad, New Delhi', 'This is near Gali Number 24', 28.5206, 77.2581))

        c.execute("INSERT INTO Room (address, description, latitude, longitude) VALUES (?, ?, ?, ?)", 
                  ('Gali Number 25, Tugalkabad, New Delhi', 'This is also near Gali Number 24', 28.5205, 77.2579))
        c.execute("INSERT INTO Roommate (address, gender,description) VALUES (?, ?,?)", 
                  ('tugalkabaad extn','Male','needed roommate '))
        c.execute("INSERT INTO Roommate (address, gender,description,contact) VALUES (?, ?,?,?)", 
                  ('tugalkabaad extn','FeMale','needed roommate ','87545wff'))

        conn.commit()
    else:
        print("Data already inserted.")

    conn.close()

create_tables()
insert_dummy_data()

# @app.before_request
# def clear_session():
#     print("session cleared")
#     session.clear()

@app.route('/')
def index():
    conn = sqlite3.connect('dummy.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Room")
    rooms = c.fetchall()
    print("rooms data= ",rooms)
    room_data = []
    for room in rooms:
        images = room[5].split(', ') if room[5] else []
        room_data.append({'room': room, 'images': images})
    
    c.execute("SELECT id,address,gender,description FROM Roommate")
    roommates = c.fetchall()
    print("roommates data= ",roommates)
    conn.close()
    if 'username' in session:
            username = session['username']
            print("username=",username)
            return render_template('index.html', room_data=room_data, roommates=roommates, username=username)
    else:
    
        return render_template('index.html', room_data=room_data, roommates=roommates)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('dummy.db')
        c = conn.cursor()

        # Check if the username or email already exists in the database
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user = c.fetchone()
        if existing_user:
            flash('Email already exists. Please choose a different one.', 'error')
            return redirect(url_for('signup'))

        # Insert the new user into the database
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        
        session['username'] = username!=None
        
        flash('You have successfully signed up!', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html')
# Dummy user credentials
admin_username = "admin"
admin_password = "123"
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('dummy.db')
        c = conn.cursor()
        print(username,password)
        
        if username == admin_username and password == admin_password:
            # Set 'logged_in' session variable to True
            print("inside admin")
            session['username'] ="admin"     
                   # Redirect to admin dashboard if login successful
            return redirect(url_for('admin'))
          
        # Check if the username and password are valid
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        
        if user:
            # If valid, store the username in the session
            session['username'] = username
            print(username)
            flash(f'Welcome back, {username}!', 'success')

            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            

    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    print("register working")
    
    if 'username' in session:
        username = session['username']
        print("username=",username)
        if request.method == 'POST':
            print("register working post")
            # Access form data
            latitude = float(request.form.get('latitude'))
            longitude = float(request.form.get('longitude'))
            address = request.form.get('address')
            description = request.form.get('description')
            
            # Get uploaded files
            images = request.files.getlist('images[]')
            
            print(latitude, longitude, address, description)

            # Insert data into room table
            conn = sqlite3.connect('dummy.db')
            c = conn.cursor()
            image_filenames = []
            for file in images:
                # Generate unique filename with address prefix
                filename = secure_filename(address + "_" + file.filename)
                image_filenames.append(filename)
                
                # Save the file with the prefixed filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
            
            # Convert the list of filenames to a comma-separated string
            image_filenames_str = ', '.join(image_filenames)
            
            c.execute("INSERT INTO Room (latitude, longitude, address, description, images) VALUES (?, ?, ?, ?, ?)", 
                    (latitude, longitude, address, description, image_filenames_str))
            
            # Commit changes and close connection
            conn.commit()
            conn.close()
            
            return jsonify({"message": "Data saved successfully"})
        
        return render_template('register.html', username=username)
    flash('You Need to login First,and Please try again.', 'error')
    return redirect(url_for('login'))

@app.route('/register_roommate', methods=['GET', 'POST'])
def register_roommate():
    print("register_roommate working")
    
    if 'username' in session:
        username = session['username']
        print("username=",username)
        if request.method == 'POST':

            print("register_roommate working roommate post")
            data = request.json
            latitude = float(data.get('latitude'))
            longitude = float(data.get('longitude'))
            address = data.get('address')
            description = data.get('description')
            gender = data.get('gender')
            contact = data.get('contact')
        
            print(latitude , longitude,address,description,gender,contact)
            conn = sqlite3.connect('dummy.db')
            c = conn.cursor()
            # Insert data into room table
            c.execute("INSERT INTO roommate (latitude, longitude, address, description,gender,contact) VALUES (?, ?,?,?, ?, ?)", 
                    (latitude, longitude, address, description,gender,contact))

            # Commit changes and close connection
            conn.commit()
            conn.close()
            return(json.dumps({"message": "Data saved successfully Thank You!"})) 
        
        return render_template('register roommate.html', username=username)
    flash('You Need to login First,and Please try again.', 'error')
    return redirect(url_for('login'))


@app.route('/dummy')
def dummy():
    # Fetch available properties from database and display search results
    return render_template('dummy.html')

@app.route('/room', methods=['GET', 'POST'])
def get_rooms():
    conn = sqlite3.connect('dummy.db')
    c = conn.cursor()
    room_id = request.args.get('id')
    print(room_id)
    
    if 'username' in session:
        username = session['username']
        print("username=",username)
        if room_id == 'all':
            c.execute("SELECT * FROM Room")
            rooms = c.fetchall()
            print(rooms)
            room_data = []
            for room in rooms:
                images = room[5].split(', ') if room[5] else []
                room_data.append({'room': room, 'images': images})
            return render_template('room.html', room_data=room_data, username=username)
        elif room_id and room_id.isdigit():
            c.execute("SELECT * FROM Room WHERE id=?", (room_id,))
            room = c.fetchone()
            print(room)
            room_data = []
            if room:
                images = room[5].split(', ') if room[5] else []
                room_data.append({'room': room, 'images': images})
                return render_template('room.html',room_data=room_data, username=username)
            else:
                return 'Room not found', 404
            
    else:
        flash('You Need to login First,and Please try again.', 'error')

        return redirect(url_for('login'))


@app.route('/roommate', methods=['GET', 'POST'])
def get_roommates():
    conn = sqlite3.connect('dummy.db')
    c = conn.cursor()

    roommate_id = request.args.get('id')
    print("id== ", roommate_id)
    
    if 'username' in session:
        username = session['username']
        print("username=",username)
        if roommate_id == 'all':
            c.execute("SELECT id,address,gender,description FROM Roommate")
            roommates = c.fetchall()
            conn.close()
            return render_template('roommate.html', roommates=roommates, username=username)
        elif roommate_id and roommate_id.isdigit():
            # also send phone numbers or other contact details 
            c.execute("SELECT * FROM Roommate WHERE id=?", (roommate_id,))
            roommate = c.fetchone()
            if roommate:
                conn.close()
                return render_template('roommate.html', roommates=[roommate], username=username)
            else:
                conn.close()
                return jsonify({'message': 'Roommate not found'}), 404
    else:
        conn.close()
        flash('You Need to login First,and Please try again.', 'error')
        return redirect(url_for('login'))

    
@app.route('/getavailability', methods=['POST'])
def getavailability():
    # Get data from request body
    data = request.json
    latitude = float(data.get('latitude'))
    longitude = float(data.get('longitude'))
    range_value = float(data.get('range'))

    # Calculate distance using Haversine formula
    def calculate_distance(lat1, lon1, lat2, lon2):
        # Radius of the Earth in km
        R = 6371.0

        # Convert latitude and longitude from degrees to radians
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        # Calculate the change in coordinates
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        # Apply Haversine formula
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return distance

    # Filter database rows within the specified range
    conn = sqlite3.connect('dummy.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Room")
    rooms = c.fetchall()

    rooms_in_range = []
    for room in rooms:
        room_distance = calculate_distance(latitude, longitude, room[3], room[4])
        if room_distance <= range_value:
            rooms_in_range.append({
                'id': room[0],
                'address': room[1],
                'description': room[2],
                'latitude': room[3],
                'longitude': room[4]
            })

    return jsonify({"rooms_in_range": rooms_in_range})


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        conn = sqlite3.connect('dummy.db')
        c = conn.cursor()
        c.execute("INSERT INTO contact (name, email,message) VALUES (?, ?, ?)", 
                    (name,email,message))
            
            # Commit changes and close connection
        conn.commit()
        conn.close()

        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    print("route admin")
    if 'username' in session and session['username'] == "admin":

        username = session['username']
        print("username=",username)
        conn = sqlite3.connect('dummy.db')
        c = conn.cursor()

        # Fetch data from the Room table
        c.execute("SELECT * FROM Room")
        room_data = c.fetchall()

        # Fetch data from the Roommate table
        c.execute("SELECT * FROM Roommate")
        roommate_data = c.fetchall()

        # Fetch data from the users table
        c.execute("SELECT * FROM users")
        users_data = c.fetchall()

        # Fetch data from the contact table
        c.execute("SELECT * FROM contact")
        contact_data = c.fetchall()

        conn.close()

        return render_template('admin.html', room_data=room_data, roommate_data=roommate_data, users_data=users_data, contact_data=contact_data)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Clear the session
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
