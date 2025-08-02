from flask_mail import Mail, Message

mail = Mail()

def init_mail(app):
    mail.init_app(app)

def send_email(subject, recipients, body, reply_to=None):
    try:
        msg = Message(subject, recipients=recipients, body=body)
        if reply_to:
            msg.reply_to = reply_to  # ✅ sets "Reply-To" header
        mail.send(msg)
        print("✅ Email sent")
    except Exception as e:
        print("❌ Email send failed:", e)
