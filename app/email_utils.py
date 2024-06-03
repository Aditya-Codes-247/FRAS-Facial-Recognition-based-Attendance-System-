import smtplib
import logging
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import session

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = ''
EMAIL_PASSWORD = ''

def send_otp(email):
    otp = str(random.randint(100000, 999999))
    session['otp'] = otp 
    session['otp_email'] = email
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = 'Your OTP Code'
    body = f'Your OTP code is {otp}'
    msg.attach(MIMEText(body, 'plain'))
    try:
        logging.debug("Connecting to SMTP server...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        logging.debug("Logging in to SMTP server...")
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        logging.debug(f"Sending email to {email}...")
        server.sendmail(EMAIL_ADDRESS, email, text)
        server.quit()
        logging.info(f"OTP sent successfully to {email}.")
        return True, otp
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
        return False, None
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False, None