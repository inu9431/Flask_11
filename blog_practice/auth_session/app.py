from flask import Flask, render_template, request, redirect, flash, session
from datetime import timedelta

app = Flask(__name__)

app.secret_key = 'flask-secert-key' # 실제 배포시에는 .env or yaml 파일로 저장 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
users = {
    'john': 'pw123',
    'leo': 'pw123'
}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        session['username'] = username
        session.permanent = True
        
        return redirect('/secret')
    else:
        flash('Invalid username or password')
        return redirect('/')
    
@app.route('/secret')
def secret():
    if 'username' in session:
        return render_template('secret.html')
    else:
        return redirect('/')
    #logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
