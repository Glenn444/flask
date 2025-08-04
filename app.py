from flask import Flask
from dotenv import load_dotenv
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from email.message import EmailMessage
import smtplib
from scholarly import scholarly
import os
import time
import random

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


def check_journal_site(site_url, site_name):
    """Check if a journal site has publications on Google Scholar"""
    try:
        print(f"Starting Google Scholar search for {site_name} ({site_url})")
        search_query = scholarly.search_pubs(f'site:{site_url}')
        
        # Just check if we can get the first result
        try:
            first_pub = next(search_query)
            print(f"Found publication: {first_pub.get('title', 'Unknown title')}")
            return True, [first_pub]
        except StopIteration:
            # No publications found
            return False, []
            
    except Exception as e:
        print(f"Error searching {site_name}: {e}")
        return False, []
    

def send_email(subject, body):
    """Send email notification"""
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
        print(f"Email sent successfully: {subject}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/')
def home():
    return """
    <h1>Google Scholar Journal Checker</h1>
    <p>Available endpoints:</p>
    <ul>
        <li><a href="/check/stratford">/check/stratford</a> - Check Stratford Journals</li>
        <li><a href="/check/ajoei">/check/ajoei</a> - Check AJOEI Journal</li>
        <li><a href="/check/jbmi">/check/jbmi</a> - Check JBMI Publisher</li>
    </ul>
    <p>Note: All endpoints require authentication</p>
    """

@app.route('/check/stratford')
@auth.login_required
def check_stratford():
    """Check Stratford Journals on Google Scholar"""
    site_url = "stratfordjournalpublishers.org"
    site_name = "Stratford Journals"
    
    print(f"Checking {site_name}...")
    found, publications = check_journal_site(site_url, site_name)
    
    if found:
        subject = f"{site_name} Google Scholar Found"
        body = f"""Journals or Articles from {site_url} have been found on Google Scholar.

Found {len(publications)} publication(s).

Check performed at: {time.strftime('%Y-%m-%d %H:%M:%S')}
Site checked: {site_url}

This is an automated notification from the Google Scholar monitoring system."""
        
        email_sent = send_email(subject, body)
        status = f"✓ {site_name}: Content found on Google Scholar ({len(publications)} publications)"
        
        if email_sent:
            status += " - Email notification sent successfully"
        else:
            status += " - Email notification failed to send"
            
    else:
        subject = f"{site_name} Google Scholar Not Found"
        body = f"""No publications for {site_name} ({site_url}) were found on Google Scholar.

Check performed at: {time.strftime('%Y-%m-%d %H:%M:%S')}
Site checked: {site_url}

This is an automated notification from the Google Scholar monitoring system."""
        
        email_sent = send_email(subject, body)
        status = f"✗ {site_name}: No content found on Google Scholar"
        
        if email_sent:
            status += " - Email notification sent successfully"
        else:
            status += " - Email notification failed to send"
    
    return status

@app.route('/check/ajoei')
@auth.login_required
def check_ajoei():
    """Check AJOEI Journal on Google Scholar"""
    site_url = "ajoeijournal.org"
    site_name = "AJOEI Journal"
    
    print(f"Checking {site_name}...")
    found, publications = check_journal_site(site_url, site_name)
    
    if found:
        subject = f"{site_name} Google Scholar Found"
        body = f"""Journals or Articles from {site_url} have been found on Google Scholar.

Found {len(publications)} publication(s).

Check performed at: {time.strftime('%Y-%m-%d %H:%M:%S')}
Site checked: {site_url}

This is an automated notification from the Google Scholar monitoring system."""
        
        email_sent = send_email(subject, body)
        status = f"✓ {site_name}: Content found on Google Scholar ({len(publications)} publications)"
        
        if email_sent:
            status += " - Email notification sent successfully"
        else:
            status += " - Email notification failed to send"
            
    else:
        subject = f"{site_name} Google Scholar Not Found"
        body = f"""No publications for {site_name} ({site_url}) were found on Google Scholar.

Check performed at: {time.strftime('%Y-%m-%d %H:%M:%S')}
Site checked: {site_url}

This is an automated notification from the Google Scholar monitoring system."""
        
        email_sent = send_email(subject, body)
        status = f"✗ {site_name}: No content found on Google Scholar"
        
        if email_sent:
            status += " - Email notification sent successfully"
        else:
            status += " - Email notification failed to send"
    
    return status

@app.route('/check/jbmi')
@auth.login_required
def check_jbmi():
    """Check JBMI Publisher on Google Scholar"""
    site_url = "jbmipublisher.org"
    site_name = "JBMI Publisher"
    
    print(f"Checking {site_name}...")
    found, publications = check_journal_site(site_url, site_name)
    
    if found:
        subject = f"{site_name} Google Scholar Found"
        body = f"""Journals or Articles from {site_url} have been found on Google Scholar.

Found {len(publications)} publication(s).

Check performed at: {time.strftime('%Y-%m-%d %H:%M:%S')}
Site checked: {site_url}

This is an automated notification from the Google Scholar monitoring system."""
        
        email_sent = send_email(subject, body)
        status = f"✓ {site_name}: Content found on Google Scholar ({len(publications)} publications)"
        
        if email_sent:
            status += " - Email notification sent successfully"
        else:
            status += " - Email notification failed to send"
            
    else:
        subject = f"{site_name} Google Scholar Not Found"
        body = f"""No publications for {site_name} ({site_url}) were found on Google Scholar.

Check performed at: {time.strftime('%Y-%m-%d %H:%M:%S')}
Site checked: {site_url}

This is an automated notification from the Google Scholar monitoring system."""
        
        email_sent = send_email(subject, body)
        status = f"✗ {site_name}: No content found on Google Scholar"
        
        if email_sent:
            status += " - Email notification sent successfully"
        else:
            status += " - Email notification failed to send"
    
    return status

# Health check endpoint
@app.route('/health')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)