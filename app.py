from flask import Flask, render_template, request, redirect, url_for, session, make_response
import os
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Simulated user data and session logic
users = {
    'user1': '1234',
    'user2': '5678'
}

SESSION_TOKEN_VALIDITY = 120

def generate_session_token():
    return os.urandom(24).hex()

def get_content(user_id, session_id):
    # Dummy logic for deciding content based on user and session ID
    return (0 if (user_id == 'user1' and session_id % 2 == 0) else 1)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'logged_in' in session:
        user_id = session['user_id']
        session_id = session.get('session_id', 0)
        
        content_choice = get_content(user_id, session_id)
        
        images = [
            'images/cat_picture.jpg',
            'images/dog_picture.jpg'
        ]
        texts = [
            "This is trial page.",
            "Not ready for deployment."
        ]
        
        # Select content based on content_choice
        selected_image = images[content_choice]
        selected_text = texts[content_choice % len(texts)]
        
        return render_template('index.html', username=user_id, image=selected_image, text=selected_text)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if users.get(username) == password:
            session['logged_in'] = True
            session['user_id'] = username
            session['session_id'] = 0  # Set session ID or use a method to increment
            token = generate_session_token()
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('session_token', token, max_age=SESSION_TOKEN_VALIDITY, httponly=True)
            session['token_time'] = time.time()
            return resp
        else:
            return 'Invalid credentials', 403
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('session_id', None)
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('session_token', '', expires=0)
    return resp

@app.route('/process_number', methods=['POST'])
def process_number():
    number = request.form.get('number', '')
    result = "Invalid"
    
    try:
        number = int(number)
        if number % 2 == 0:
            result = "Even"
        else:
            result = "Odd"
    except ValueError:
        result = "Invalid"
    
    # Render the same page with the result
    return render_template('index.html', result=result, username=session.get('user_id'))

if __name__ == '__main__':
    app.run(debug=True)




#==================================================================================================================================================================================
#Initial code

# from flask import Flask, render_template
# import json
# import os

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# # @app.route('/')
# # def hello_world():
# #     return 'Hello, World!'

# if __name__ == '__main__':
#     app.run(debug=True)
