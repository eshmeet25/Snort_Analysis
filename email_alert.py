# email_alert.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body):
    sender_email = "nandiniiiii03@gmail.com"
    receiver_email = "nandiniiiii03@gmail.com"
    app_password = "sbus bajf jjrn zwrc"  # Use Gmail App Password
 
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("✅ Email alert sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)
