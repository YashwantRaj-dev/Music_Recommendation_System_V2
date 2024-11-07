# tasks.py
from flask_mail import Message
from config import celery, mail

@celery.task
def send_email(email_address, message_body):
    try:
        # Create the message
        sender_email = "yashwantraj159@gmail.com"
        message = Message("Welcome to Music Recommendation System Website!",sender=sender_email,recipients=[email_address], body=message_body)
        # Send the email
        mail.send(message)
        return f"Email sent successfully to {email_address}"
    except Exception as e:
        return f"Failed to send email to {email_address}: {str(e)}"
