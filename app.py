from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import  generate_password_hash, check_password_hash
from email.message import EmailMessage
import smtplib
from scholarly import scholarly, ProxyGenerator

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "glen": generate_password_hash("hello"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def check_google_scholar():
    pg = ProxyGenerator()
    success = pg.ScraperAPI("c80dc3c0a8fccc86a06da4cdaea21406")
    scholarly.use_proxy(pg)

    # Function to check if journals or articles from "stratfordjournals.com" exist
    def check_stratford_journals():
        search_query = scholarly.search_pubs('site:stratfordjournals.org')
        publications = [pub for pub in search_query]
        return len(publications) > 0

    # Function to send an email
    def send_email(subject, body):
        EmailAdd = "notifications@tobitresearchconsulting.com"
        Pass = "Tobitit2025"

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EmailAdd
        msg['To'] = 'gmark1586@gmail.com', 'glennmakhandia@gmail.com'
        msg.set_content(body)

        with smtplib.SMTP_SSL('tobitresearchconsulting.com', 465) as smtp:
            smtp.login(EmailAdd, Pass)
            smtp.send_message(msg)

    # Check if journals or articles from "stratfordjournals.com" exist
    if check_stratford_journals():
        send_email("Stratford Google Scholar Found", "Journals or Articles from stratfordjournals.com have been found on Google Scholar.")
        return "Email sent: Stratford Google Scholar Found"
    else:
        send_email("Stratford Google Scholar Not Found", "Publications for Stratford Journals Not Found on Google Scholar")
        return "Email sent: Stratford Google Scholar Not Found"

if __name__ == '__main__':
    app.run()
