"""
This module provides email functionality for sending workout advice using Gmail's SMTP server.
It handles email composition and sending through a secure connection.

Example:
   email_handler = EmailHandler()
   await email_handler.send_email("Workout Advice", "Here's your personalized advice...")

Note:
   Requires environment variables:
   - EMAIL_SENDER: Gmail address sending the emails
   - EMAIL_PASSWORD: Google App Password for authentication
   - EMAIL_RECEIVER: Recipient email address
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class EmailHandler:
   """
   Handles email operations for sending workout advice.
   """
   
   def __init__(self) -> None:
       """
       Initialize EmailHandler with credentials from environment variables.
       
       The constructor loads email configuration from environment variables
       set in the .env file.
       """
       self.sender_email: Optional[str] = os.getenv('EMAIL_SENDER')
       self.sender_password: Optional[str] = os.getenv('EMAIL_PASSWORD')
       self.receiver_email: Optional[str] = os.getenv('EMAIL_RECEIVER')

   async def send_email(self, subject: str, message: str) -> bool:
       """
       Send an email with the provided subject and message.
       
       Args:
           subject (str): The subject line of the email
           message (str): The body content of the email
           
       Returns:
           bool: True if email was sent successfully, False otherwise
           
       Raises:
           smtplib.SMTPException: If there are SMTP-related errors
           Exception: For other unexpected errors
       """
       try:
           msg = MIMEMultipart()
           msg['From'] = self.sender_email
           msg['To'] = self.receiver_email
           msg['Subject'] = subject

           msg.attach(MIMEText(message, 'plain'))

           with smtplib.SMTP('smtp.gmail.com', 587) as server:
               server.starttls()
               server.login(self.sender_email, self.sender_password)
               server.send_message(msg)

           return True
       except Exception as e:
           print(f"Error sending email: {str(e)}")
           return False