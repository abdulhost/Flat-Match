from flask import Flask, jsonify, render_template, request, redirect, url_for, session,flash
import sqlite3
from math import radians, sin, cos, sqrt, atan2
import json
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import bcrypt
import random  # Import random module for generating random numbers
import string

app = Flask(__name__)
app.secret_key = "1154"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dummy.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

def create_tables():
    conn = sqlite3.connect('dummy.db')
    c = conn.cursor()

    # c.execute('''CREATE TABLE IF NOT EXISTS Room (
    #              id INTEGER PRIMARY KEY,
    #              address TEXT,
    #              description TEXT,
    #              latitude REAL,
    #              longitude REAL,
    #             images TEXT,
    #           contact TEXT
    #              )''')

    # c.execute('''CREATE TABLE IF NOT EXISTS Roommate (
    #             id INTEGER PRIMARY KEY,
    #             address TEXT,   
    #             gender TEXT,
    #             description TEXT,
    #             contact TEXT,
    #             latitude REAL,
    #             longitude REAL
    #              )''')
    # c.execute('''CREATE TABLE IF NOT EXISTS users (
    #             id INTEGER PRIMARY KEY,
    #             username TEXT,
    #           email TEXT,
    #           password REAl
    #              )''')
    # c.execute('''CREATE TABLE IF NOT EXISTS contact (
    #             id INTEGER PRIMARY KEY,
    #             name TEXT,
    #           email TEXT,
    #           message TEXT
    #              )''')

    c.execute('''CREATE TABLE IF NOT EXISTS contact (
                id INTEGER PRIMARY KEY,
                name TEXT,
              email TEXT,
              message TEXT
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    email TEXT,
                    password TEXT,
                    phone_number TEXT,
                    about_me TEXT,
                    profile_picture TEXT,
                    created_at DATETIME,
                    updated_at DATETIME,
                    last_login_at DATETIME
                    )''')

    # c.execute('''CREATE TABLE IF NOT EXISTS UserProfile (
    #                 profile_id INTEGER PRIMARY KEY,
    #                 user_id INTEGER REFERENCES Users(user_id),
    #                 first_name TEXT,
    #                 last_name TEXT,
    #                 date_of_birth DATE,
    #                 gender TEXT,
    #                 phone_number TEXT,
    #                 about_me TEXT,
    #                 profile_picture TEXT,
    #                 created_at DATETIME,
    #                 updated_at DATETIME
    #                 )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Room (
                    room_id INTEGER PRIMARY KEY,
                    user_id INTEGER REFERENCES Users(user_id),
                    title TEXT,
                    description TEXT,
                    price REAL,
                    address TEXT,
                    images TEXT,
                    contact TEXT,
                    latitude REAL,
                    longitude REAL,
                    created_at DATETIME,
                    updated_at DATETIME
                    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Roommate (
                    roommate_id INTEGER PRIMARY KEY,
                    user_id INTEGER REFERENCES Users(user_id),
                    price REAL,
                    address TEXT,
                    description TEXT,
                    gender TEXT,
                    contact TEXT,
                    latitude REAL,
                    longitude REAL,
                    is_smoker TEXT,
                    is_pet_friendly TEXT,
                    created_at DATETIME,
                    updated_at DATETIME
                    )''')

    conn.commit()
    conn.close()

# def insert_dummy_data():
#     conn = sqlite3.connect('dummy.db')
#     c = conn.cursor()

#     # Check if the Room table is empty before inserting
#     c.execute("SELECT COUNT(*) FROM Room")
#     count = c.fetchone()[0]
#     if count == 0:
#         c.execute("INSERT INTO Room (address, description, latitude, longitude) VALUES (?, ?, ?, ?)", 
#                   ('Gali Number 23, Tugalkabad, New Delhi', 'This is near Gali Number 24', 28.5206, 77.2581))

#         c.execute("INSERT INTO Room (address, description, latitude, longitude) VALUES (?, ?, ?, ?)", 
#                   ('Gali Number 25, Tugalkabad, New Delhi', 'This is also near Gali Number 24', 28.5205, 77.2579))
#         c.execute("INSERT INTO Roommate (address, gender,description,contact,latitude,longitude) VALUES (?, ?,?,?, ?,?)", 
#                   ('tugalkabaad extn','Male','needed roommate',"adsddsv",28.5142,77.2600))
#         c.execute("INSERT INTO Roommate (address, gender,description,contact,latitude,longitude) VALUES (?, ?,?,?,?, ?)", 
#                   ('tugalkabaad extn','FeMale','needed roommate ','87545wff',28.5142,77.2600))

# Latitude: 28.5142, Longitude: 77.2600
# Latitude: 28.5119, Longitude: 77.2629
    #     conn.commit()
    # else:
    #     print("Data already inserted.")

    # conn.close()

create_tables()
# insert_dummy_data()

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
    # print("rooms data= ",rooms)
    room_data = []
    for room in rooms:
        images = room[6].split(', ') if room[6] else []
        room_data.append({'room': room, 'images': images})
    
    c.execute("SELECT roommate_id,address,gender,description FROM Roommate")
    roommates = c.fetchall()
    # print("roommates data= ",roommates)
    conn.close()
    if 'username' in session:
            username = session['username']
            useremail = session['useremail']
            print("username=",username,useremail)

            return render_template('index.html', room_data=room_data, roommates=roommates, username=username)
    else:
        # flash('Welcome to FlatMatch! Finding Rooms and Roommates made easy. We are here to help you find the perfect room and roommate near your college. Say goodbye to the hassle of searching for accommodation - our platform makes it easy and convenient. Plus, with FlatMatch, you can save on brokerage fees when the flat is posted by its owner. Get started now and make your college life easier!', 'success')
       
        return render_template('index.html', room_data=room_data, roommates=roommates)

#    c.execute('''CREATE TABLE IF NOT EXISTS Users (
#                     user_id INTEGER PRIMARY KEY,
#                     username TEXT,
#                     email TEXT,
#                     password TEXT,
#                     phone_number TEXT,
#                     about TEXT,
#                     profile_picture TEXT,
#                     created_at DATETIME,
#                     updated_at DATETIME,
#                     last_login_at DATETIME
#                     )''')
UPLOAD_FOLDER2 = 'static/profile_pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone_number = request.form['phone_number']
        about_me = request.form['about']

        # Get current timestamp for created_at and updated_at fields
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Initialize profile_picture with None
        profile_picture = None

        conn = sqlite3.connect('dummy.db')
        c = conn.cursor()

        # Check if the username or email already exists in the database
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user = c.fetchone()
        if existing_user:
            flash('Email already exists. Please choose a different one.', 'error')
            return redirect(url_for('signup'))

        file = request.files['profile_picture']
        # If the user does not select a file, the browser submits an empty part without filename
        if file.filename == '':
            flash('No selected file', 'error')
            print("no file error")
            return redirect(url_for('signup'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = filename.rsplit('.', 1)[1].lower()
            filename = f"{email}.{file_ext}"
            file_path = os.path.join('static/profile_pictures', filename)
            file.save(file_path)
            profile_picture = file_path
            print("image saved ",file_path,profile_picture)
        else:
            flash('Invalid file format', 'error')
            print("invalid error")
            return redirect(url_for('signup'))


         # Generate a random salt for password hashing
        # salt = bcrypt.gensalt()

        # Generate a random sequence of characters for additional randomness
        # random_data = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        # Hash the password using the generated salt and additional random data
        # hashed_password = bcrypt.hashpw(password.encode('utf-8') + random_data.encode('utf-8'), salt)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert the new user into the database
        c.execute("INSERT INTO Users (username, email, password, phone_number, about_me, profile_picture, created_at, updated_at, last_login_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (username, email, hashed_password, phone_number, about_me, profile_picture, current_timestamp, current_timestamp, current_timestamp))
        conn.commit()


        # Insert the new user into the database
        # c.execute("INSERT INTO Users (username, email, password, phone_number, about_me, profile_picture, created_at, updated_at, last_login_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        #         (username, email, password, phone_number, about_me, profile_picture, current_timestamp, current_timestamp, current_timestamp))
        # conn.commit()
        
         # Save profile picture with user id as filename
        # if 'profile_picture' in request.files:
        #     file = request.files['profile_picture']
        #     if file.filename != '' and allowed_file(file.filename):
        #         filename = secure_filename(file.filename)
        #         file_ext = filename.rsplit('.', 1)[1].lower()
        #         # filename = f"user_{user_id}.{file_ext}"
        #         filename = f"{user_id}.{file_ext}"
        #         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #         file.save(file_path)
        #         profile_picture = file_path
        #         flash('File successfully uploaded', 'success')
        #     else:
        #         flash('Invalid file format', 'error')
        #         return redirect(request.url)

        # # Update the user record with the profile picture path
        # c.execute("UPDATE Users SET profile_picture=? WHERE user_id=?", (profile_picture, user_id))

        # if username is not None:
        #     session['username'] = username

        
        flash('You have successfully signed up!', 'success')
        
        # c.execute("SELECT * FROM Users WHERE email=?", (email,))

        # user = c.fetchone()
        
        conn.close()
        print("working till end of signup")
        session['useremail'] = email
        print("inside signup ",email)
        session['username'] = username
        print("inside signup ",username)
        return redirect(url_for('profile'))
        # return render_template('profile.html')




    return render_template('signup.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'useremail' in session and 'username' in session :
        useremail = session['useremail']
        print("profile useremail=",useremail)
        username = session['username']
        print("profile username=",username)
        
   
        conn = sqlite3.connect('dummy.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Users WHERE email=?", (useremail,))
        user = c.fetchone()
        print(user)

        user_id=user[0]
        print("userid=",user_id)
        c.execute('''SELECT * FROM Room WHERE user_id = ?''', (user_id,))
        room_data = c.fetchall()
        
        c.execute('''SELECT * FROM Roommate WHERE user_id = ?''', (user_id,))
        roommate_data = c.fetchall()
        
        # if room_data:
        #     print("data in room:", room_data)
        # else:
        #     print("no room data found")
        # if roommate_data:
        #     print("data in roommate:", roommate_data)
        # else:
        #     print("no roommate data found")

        if request.method == 'POST':
            
            updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            variable = request.form.get('variable')
            print("variable name= ",variable)
            if variable=='room':
                description = request.form.get('description')
                address = request.form.get('address')
                contactdetails = request.form.get('contactDetails')
                room_id = request.form.get('room_id')
                variable = request.form.get('variable')
                images = request.files.getlist('images[]')
                # Handle FormData as needed
                print('Description:', description)
                print('address:', address)
                print('Contact Details:', contactdetails)
                print('Room ID:', room_id)
                print('Variable:', variable)
                print('img:', images)
                
                if images: 
                    print("images present")
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
                    c.execute("UPDATE Room SET contact=?, description=?, images=?, updated_at=? WHERE room_id=?", (contactdetails, description, image_filenames_str, updated_at, room_id))
                else:
                    print("images empty")
                    c.execute("UPDATE Room SET contact=?,description=?, updated_at=? WHERE room_id=?", (contactdetails,  description, updated_at, room_id))
                conn.commit() 
                return jsonify({'message': 'Profile updated successfully'})       
            
            elif variable=='profile':
                print("inside profile")
                username = request.form.get('username')
                password = request.form.get('password') 
                phone_number = request.form.get('phone_number') 
                about_me =request.form.get('about_me')
                email = request.form.get('email')
                print(username,"password= ",password,phone_number,about_me,email)
                variable = request.form.get('variable')
                images = request.files.getlist('images[]')
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                if images: 
                    print("images present")
                    file_path=None
                    for file in images:
                        # Generate unique filename with address prefix
                        filename = secure_filename(file.filename)
                        file_ext = filename.rsplit('.', 1)[1].lower()
                        filename = f"{email}.{file_ext}"
                        file_path = os.path.join('static/profile_pictures', filename)
                        # If a file with the same name exists, delete it
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        file.save(file_path)
                    c.execute("UPDATE Users SET username=?, password=?, phone_number=?,profile_picture=?, about_me=?, updated_at=? WHERE email=?", (username, hashed_password, phone_number,file_path,about_me,updated_at, email))
                    conn.commit() 
                else:
                    c.execute("UPDATE Users SET username=?, password=?, phone_number=?, about_me=?, updated_at=? WHERE email=?", (username, hashed_password, phone_number,about_me,updated_at, email))
                    conn.commit() 

            elif variable=='roommate':
                print("inside roommate")
                description = request.form.get('description')
                address = request.form.get('address') 
                contactdetails = request.form.get('contactDetails') 
                roommate_id =request.form.get('roommate_id')
                
                print(description,address,contactdetails,roommate_id)
                
                
                c.execute("UPDATE Roommate SET description=?, contact=?, updated_at=? WHERE roommate_id=?", (description, contactdetails,updated_at, roommate_id))
                conn.commit() 

            conn.close() 
            flash('Profile updated successfully!', 'success')
            return jsonify({'message': 'Profile updated successfully'})         
     
        return render_template('profile.html',user=user,room_data=room_data,roommate_data=roommate_data)


    
    # else:
    #     flash('Invalid request method', 'error')
        # return redirect(url_for('profile'))
    flash('You Need to login First,and Please try again.', 'error')
    return redirect(url_for('login'))
    



# Dummy user credentials
admin_username = "admin"
admin_password = "123"
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('dummy.db')
        c = conn.cursor()
        print(email,password)
        
        if email == admin_username and password == admin_password:
            # Set 'logged_in' session variable to True
            print("inside admin")
            session['username'] ="admin"     
                   # Redirect to admin dashboard if login successful
            return redirect(url_for('admin'))
          
        # Check if the username and password are valid
        # c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        # user = c.fetchone()

        # Check if the user exists in the database
        c.execute("SELECT * FROM Users WHERE email=?", (email,))
        user = c.fetchone()
        print(user)
        if user:
            # Retrieve the stored hashed password from the database
            stored_hashed_password = user[3]
            print(stored_hashed_password)
            # Verify the password by hashing the entered password with the stored salt
            actual_salt = stored_hashed_password[:29]  # Bcrypt uses 29 bytes for salt
            # Verify the password by hashing the entered password with the extracted salt
            hashed_password_bytes = bcrypt.hashpw(password.encode('utf-8'), actual_salt)

        # Now you can use bcrypt.checkpw() with the hashed password in bytes format
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password_bytes):
                username=user[1]
                session['username'] = username
                print(username)
                
                
                flash(f'Welcome back, {username}!', 'success')
                
                session['useremail'] = email
                print(email)
                # return redirect(url_for('index'))
                return redirect(url_for('profile'))
        
        # if user:
        #     # If valid, store the username in the session
        #     username=user[1]
        #     session['username'] = username
        #     print(username)
            
            
        #     flash(f'Welcome back, {username}!', 'success')
            
        #     session['useremail'] = email
        #     print(email)
        #     # return redirect(url_for('index'))
        #     return redirect(url_for('profile'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            

    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    print("register working")
    
    if 'username' in session:
        username = session['username']
        print("username=",username)
        useremail = session['useremail']
        print("useremail register=",useremail)
        if request.method == 'POST':
            print("register working post")
            conn = sqlite3.connect('dummy.db')
            c = conn.cursor()
            c.execute("SELECT user_id FROM Users WHERE email=?", (useremail,))
            user_id = c.fetchone()
            user_id=user_id[0]
            print("userid register= ",user_id)
            
            # Access form data
            latitude = float(request.form.get('latitude'))
            longitude = float(request.form.get('longitude'))
            address = request.form.get('address')
            description = request.form.get('description')
            contact = request.form.get('contact')
            
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
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            
            c.execute("INSERT INTO Room (user_id,latitude, longitude, address, description, images, contact,created_at,updated_at) VALUES (?,?, ?, ?, ?, ?,?, ?,?)", 
                    (user_id,latitude, longitude, address, description, image_filenames_str, contact,current_timestamp,current_timestamp))
            
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
        useremail = session['useremail']
        print("useremail register=",useremail)

        if request.method == 'POST':
            print("register_roommate working roommate post")
            conn = sqlite3.connect('dummy.db')
            c = conn.cursor()
            c.execute("SELECT user_id FROM Users WHERE email=?", (useremail,))
            user_id = c.fetchone()
            user_id=user_id[0]
            print("userid register= ",user_id)
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
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Insert data into room table
            c.execute("INSERT INTO Roommate (user_id,latitude, longitude, address, description,gender,contact,created_at,updated_at) VALUES (?,?, ?,?,?, ?, ?, ?, ?)", 
                    (user_id,latitude, longitude, address, description,gender,contact,current_timestamp,current_timestamp))

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
                images = room[6].split(', ') if room[6] else []
                room_data.append({'room': room, 'images': images})
            return render_template('room.html', room_data=room_data, username=username)
        elif room_id and room_id.isdigit():
            c.execute("SELECT * FROM Room WHERE room_id=?", (room_id,))
            room = c.fetchone()
            print(room)
            room_data = []
            if room:
                images = room[6].split(', ') if room[6] else []
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
            c.execute("SELECT roommate_id,address,gender,description FROM Roommate")
            roommates = c.fetchall()
            
            # return render_template('roommate.html', roommates=roommates, username=username)
            if roommates:
                if len(roommates)!=1:
                        conn.close()
                        return render_template('roommate.html', roommates=roommates, username=username)
                else:
                    c.execute("SELECT * FROM Roommate")
                    roommate = c.fetchone()
                    conn.close()
                    print(roommate)
                    return render_template('roommate.html', roommates=[roommate], username=username)

            else:
                
                return jsonify({'message': 'Roommate not found'}), 404
        elif roommate_id and roommate_id.isdigit():
            # also send phone numbers or other contact details 
            c.execute("SELECT * FROM Roommate WHERE roommate_id=?", (roommate_id,))
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

    
# @app.route('/getavailability', methods=['POST'])
# def getavailability():
#     # Get data from request body
#     data = request.json
#     latitude = float(data.get('latitude'))
#     longitude = float(data.get('longitude'))
#     range_value = float(data.get('range'))

#     # Calculate distance using Haversine formula
#     def calculate_distance(lat1, lon1, lat2, lon2):
#         # Radius of the Earth in km
#         R = 6371.0

#         # Convert latitude and longitude from degrees to radians
#         lat1 = radians(lat1)
#         lon1 = radians(lon1)
#         lat2 = radians(lat2)
#         lon2 = radians(lon2)

#         # Calculate the change in coordinates
#         dlon = lon2 - lon1
#         dlat = lat2 - lat1

#         # Apply Haversine formula
#         a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
#         c = 2 * atan2(sqrt(a), sqrt(1 - a))
#         distance = R * c
#         return distance

#     # Filter database rows within the specified range
#     conn = sqlite3.connect('dummy.db')
#     c = conn.cursor()
#     c.execute("SELECT * FROM Room")
    
#     rooms = c.fetchall()
#     c.execute("SELECT * FROM Roommate")
#     roommate = c.fetchall()
    
#     rooms_in_range = []
#     for room in rooms:
#         room_distance = calculate_distance(latitude, longitude, room[3], room[4])
#         if room_distance <= range_value:
#             rooms_in_range.append({
#                 'id': room[0],
#                 'address': room[1],
#                 'description': room[2],
#                 'latitude': room[3],
#                 'longitude': room[4]
#             })

#     return jsonify({"rooms_in_range": rooms_in_range})

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

    # Establish database connection
    conn = sqlite3.connect('dummy.db')
    c = conn.cursor()

    # Fetch rooms within the specified range
    c.execute("SELECT * FROM Room")
    rooms = c.fetchall()

    # Fetch roommates
    c.execute("SELECT * FROM Roommate")
    roommates = c.fetchall()

    # Prepare room data
    rooms_in_range = []
    for room in rooms:
        room_distance = calculate_distance(latitude, longitude, room[8], room[9])
        if room_distance <= range_value:
            rooms_in_range.append({
                'id': room[0],
                'address': room[5],
                'description': room[3],
                'latitude': room[8],
                'longitude': room[9]
            })

    # Prepare roommate data
    roommates_data = []
    for roommate in roommates:
        roommate_distance = calculate_distance(latitude, longitude, roommate[7], roommate[8])
        if roommate_distance <= range_value:
            roommates_data.append({
                'id': roommate[0],
                'address': roommate[3],
                'gender': roommate[5],
                'description': roommate[4],
                'contact': roommate[6],
                'latitude': roommate[7],
                'longitude': roommate[8]
                
            })

    # Close database connection
    conn.close()
    # print(rooms_in_range,"\n",roommates_data)

    return jsonify({"rooms_in_range": rooms_in_range, "roommates_data": roommates_data})


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
        print(room_data)
        return render_template('admin.html', room_data=room_data, roommate_data=roommate_data, users_data=users_data, contact_data=contact_data)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Clear the session
    session.pop('username', None)
    session.pop('useremail', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
