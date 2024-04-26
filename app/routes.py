from flask import render_template, request, redirect, url_for, session
from app import app, redQueue
@app.route('/')
def home():
    session.clear()
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)