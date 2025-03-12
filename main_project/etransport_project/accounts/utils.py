def sendMail(emailid, otp, html=""):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Sender and receiver email
    me = "naveenpatidar951@gmail.com"
    you = emailid

    # Create the email message
    msg = MIMEMultipart('alternative')
    msg['From'] = me
    msg['To'] = you
    msg['Subject'] = 'Email_Verification'

    # Default HTML content
    if html == "":
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
                            .footer {{
                                font-size: 12px;
                                color: #888;
                                text-align: center;
                                margin-top: 20px;
                                border-top: 1px solid #ddd;
                                padding-top: 10px;
                                width: 100%;
                                box-sizing: border-box;
                            }}
                            a {{
                                color: #1a0dab;
                                text-decoration: none;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>Welcome to etransport!</h1>
                            <p>Thank you for registering on our site, <strong>etransport.app/strong>. Please do not share your credentials with others:</p>
                            <h2>Username: {emailid}</h2>
                            <h2>otp: {otp}</h2>
                            <br>
                            <p>If you have any questions, feel free to contact us at support@etransport.app</p>
                        </div>
                        <div class="footer">
                                <p>&copy; 2025 tailorhub, Inc. All rights reserved.<br>
                                   IT park, Indore, M.P. India<br>
                                   If you no longer wish to receive emails from  E-transport, please <a href="https://test">click here</a>.</p>
                        </div>
                    </body>
                </html>"""
    part2 = MIMEText(html, 'html')
    msg.attach(part2)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("naveenpatidar4513@gmail.com", "qpfw mlkg whcj qzuu")
    s.sendmail(me, you, msg.as_string())
    s.quit()
    
    print("Mail sent successfully....")
      