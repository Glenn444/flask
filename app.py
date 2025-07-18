from flask import Flask
from dotenv import load_dotenv
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from email.message import EmailMessage
import smtplib
from scholarly import scholarly
import os
import time

load_dotenv()

app = Flask(__name__)
auth = HTTPBasicAuth()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

if not username or not password:
    raise ValueError("USERNAME and PASSWORD environment variables must be set in .env file")

users = {
    username: generate_password_hash(password, method='pbkdf2:sha256'),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def check_google_scholar():
    # Remove proxy setup for now
    # pg = ProxyGenerator()
    # success = pg.ScraperAPI(os.getenv("SCRAPER_API"))
    # scholarly.use_proxy(pg)

    def check_stratford_journals():
        try:
            search_query = scholarly.search_pubs('site:stratfordjournalpublishers.org')
            publications = []
            count = 0
            for pub in search_query:
                publications.append(pub)
                count += 1
                if count >= 5:  # Limit to 5 results to avoid rate limiting
                    break
                time.sleep(1)  # Add delay to be respectful
            return len(publications) > 0
        except Exception as e:
            print(f"Error searching: {e}")
            return False

    def send_email(subject, body):
        try:
            EmailAdd = os.getenv("SENDER_EMAIL")
            Pass = os.getenv("SENDER_PASS")

            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = EmailAdd
            msg['To'] = [os.getenv("EMAIL1"), os.getenv("EMAIL2")]
            msg.set_content(body)

            with smtplib.SMTP_SSL('tobitresearchconsulting.com', 465) as smtp:
                smtp.login(EmailAdd, Pass)
                smtp.send_message(msg)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    if check_stratford_journals():
        if send_email("Stratford Google Scholar Found", "Journals or Articles from stratfordjournalpublishers.org have been found on Google Scholar."):
            return "Email sent: Stratford Google Scholar Found"
        else:
            return "Stratford content found but email failed to send"
    else:
        if send_email("Stratford Google Scholar Not Found", "Publications for Stratford Journals Not Found on Google Scholar"):
            return "Email sent: Stratford Google Scholar Not Found"
        else:
            return "No Stratford content found and email failed to send"

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)