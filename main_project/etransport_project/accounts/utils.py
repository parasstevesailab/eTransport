from rest_framework.response import Response
from rest_framework import status
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def sendMail(emailid, otp, html=""):
    """
    Send an OTP verification email to the user.
    
    Args:
        emailid (str): Recipient's email address
        otp (str): One-time password to send
        html (str, optional): Custom HTML content for the email
    
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate email address
    try:
        validate_email(emailid)
    except ValidationError:
        return False, "Invalid email address format"

    # Sender email configuration
    sender_email = "naveenpatidar4513@gmail.com"
    sender_password = "qpfw mlkg whcj qzuu"  # App-specific password
    
    # Create email message
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = emailid
    msg['Subject'] = 'Email Verification - Etransport'

    # Default HTML content if none provided
    if not html:
        html = f"""<html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        background-color: #ffffff;
                        border-radius: 8px;
                        padding: 20px;
                        max-width: 600px;
                        margin: auto;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    h1 {{
                        color: #333;
                    }}
                    p {{
                        color: #555;
                    }}
                    .otp {{
                        font-size: 24px;
                        color: #0066cc;
                        font-weight: bold;
                    }}
                    .footer {{
                        font-size: 12px;
                        color: #888;
                        text-align: center;
                        margin-top: 20px;
                        border-top: 1px solid #ddd;
                        padding-top: 10px;
                    }}
                    a {{
                        color: #1a0dab;
                        text-decoration: none;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Welcome to Etransport!</h1>
                    <p>Thank you for registering with us. Please use the following OTP to verify your email:</p>
                    <p class="otp">{otp}</p>
                    <p>Username: {emailid}</p>
                    <p>This OTP is valid for 10 minutes. Do not share it with anyone.</p>
                    <p>If you didn't request this, please ignore this email or contact support@etransport.app</p>
                </div>
                <div class="footer">
                    <p>© 2025 Etransport, Inc. All rights reserved.<br>
                       IT Park, Indore, M.P. India<br>
                       <a href="https://etransport.app/unsubscribe">Unsubscribe</a></p>
                </div>
            </body>
        </html>"""
    
    # Attach HTML content
    part = MIMEText(html, 'html')
    msg.attach(part)

    try:
        # Connect to SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()
            s.login(sender_email, sender_password)
            s.sendmail(sender_email, emailid, msg.as_string())
        return True, "Verification email sent successfully"
    
    except smtplib.SMTPAuthenticationError:
        return False, "Email authentication failed. Please check credentials"
    except smtplib.SMTPRecipientsRefused:
        return False, "Email address rejected by server"
    except smtplib.SMTPException as e:
        return False, f"SMTP error occurred: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error occurred: {str(e)}"