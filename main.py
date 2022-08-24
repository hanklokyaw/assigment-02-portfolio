from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import requests
import os
import smtplib
from email.message import EmailMessage
import ssl

app = Flask(__name__)

EMAIL_PASSWORD = os.environ.get("GMAIL_SECRET_KEY")
APP_ADMIN_EMAIL = "hank.lo.kyaw@gmail.com"
APP_ADMIN_EMAIL2 = "greeting@hanklo.com"
API_URL = "https://api.npoint.io/d340c201b32dea1e5708"

response = requests.get(API_URL)
form_data = response.json()

# def form_posts(function):
#     def wrapper(*args,**kwargs):
#         function(args[0])
#     return wrapper

title = ""
subtitle = ""
body = ""


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/form-entry', methods=["GET", "POST"])
def form_data_collection():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        # if name == "":
        #     return render_template("index.html", text="Please enter your name.")
        # if email == "":
        #     return render_template("index.html", text="Please enter your email")
        # if phone == "":
        #     return render_template("index.html", text="Please enter your phone")
        # if message == "":
        #     return render_template("index.html", text="Message cannot be empty.")
        subject = "Contact from your website viewer"
        body = f"Name: {name}\n" \
               f"Email: {email}\n" \
               f"Phone: {phone}\n" \
               f"Message: {message}."
        em = EmailMessage()
        em['From'] = APP_ADMIN_EMAIL
        em['To'] = APP_ADMIN_EMAIL2
        em['Subject'] = subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as connection:
            connection.login(APP_ADMIN_EMAIL, GMAIL_SECRET_KEY)
            connection.sendmail(APP_ADMIN_EMAIL, APP_ADMIN_EMAIL2, em.as_string())
        print(f"Email sent to Admin!")
        return render_template("index.html", text="Successfully sent your message")
    else:
        print("Error occur.")
        return render_template("index.html", text="Error occurred, please contact Hank by email.")


if __name__ == '__main__':
    app.run(debug=True)
