from flask import Flask, jsonify, render_template, request, redirect, url_for, session
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    print("register working")

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
    
    return render_template('register.html')

@app.route('/register_roommate', methods=['GET', 'POST'])
def register_roommate():
    print("register_roommate working")
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
    
    return render_template('register roommate.html')


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
    if room_id == 'all':
        c.execute("SELECT * FROM Room")
        rooms = c.fetchall()
        print(rooms)
        room_data = []
        for room in rooms:
            images = room[5].split(', ') if room[5] else []
            room_data.append({'room': room, 'images': images})
        return render_template('room.html', room_data=room_data)
    elif room_id and room_id.isdigit():
        c.execute("SELECT * FROM Room WHERE id=?", (room_id,))
        room = c.fetchone()
        if room:
            images = room[5].split(', ') if room[5] else []
            return render_template('room.html', room=room, images=images)
        else:
            return 'Room not found', 404
    else:
        return 'Invalid parameter', 400


@app.route('/roommate', methods=['GET', 'POST'])
def get_roommates():
    conn = sqlite3.connect('dummy.db')
    c = conn.cursor()

    roommate_id = request.args.get('id')
    print("id== ", roommate_id)
    if roommate_id == 'all':
        c.execute("SELECT id,address,gender,description FROM Roommate")
        roommates = c.fetchall()
        
        return render_template('roommate.html', roommates=roommates)
    elif roommate_id and roommate_id.isdigit():
        # also send phone numbers or other contact details 
        c.execute("SELECT * FROM Roommate WHERE id=?", (roommate_id,))
        roommate = c.fetchone()
        if roommate:
            return render_template('roommate.html', roommates=[roommate])
        else:
            return jsonify({'message': 'Roommate not found'}), 404
    else:
        return jsonify({'message': 'Invalid parameter'}), 400

    conn.close()


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

if __name__ == '__main__':
    app.run(debug=True)
