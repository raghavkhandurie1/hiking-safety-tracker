import smtplib
import sqlite3
from email.mime.text import MIMEText
from datetime import datetime

def send_alert(contact_email, hiker_name, location, expected_return):
    sender = "fruthi280@gmail.com"
    password = "rpai zuru lrsa dguj"  # we'll set this up next
    
    msg = MIMEText(f"""
    HIKING SAFETY ALERT
    
    {hiker_name} was hiking at {location} and was expected to return by {expected_return}.
    They have not checked in. Please attempt to contact them or alert authorities if necessary.
    
    This is an automated alert from Hiking Tracker.
    """)
    
    msg["Subject"] = f"⚠️ SAFETY ALERT: {hiker_name} has not checked in"
    msg["From"] = sender
    msg["To"] = contact_email
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)
    
    print(f"Alert sent to {contact_email}")

def check_overdue_hikes():
    conn = sqlite3.connect("hikes.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM hikes 
        WHERE checked_in = 0 
        AND expected_return < datetime('now')
    """)
    overdue = cursor.fetchall()
    conn.close()
    return overdue

if __name__ == "__main__":
    send_alert(
        contact_email="fruthi280@gmail.com",  
        hiker_name="Raghav",
        location="Royal National Park",
        expected_return="10:00 AM"
    )