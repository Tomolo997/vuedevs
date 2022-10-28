from django.core.mail import send_mail
from django.template.loader import render_to_string
sending_email ='support@djangodevs.com'
class Mailer:
    
    
    def sendWelcomeMail(receiver):
        sender = sending_email
        send_mail(
            'Welcome aboard',
            "Welcome dear traveler to the best there is",
            sender,
            [receiver],
        )

    def sendVerificationMail(receiver,verification_code,user_id):
        sender = sending_email
        html_message = render_to_string(
            'emails/verification-mail.html',
            {
                'verification_link': f'https://djangodevs.com/verify/{verification_code}?user={user_id}',
            }
        )
        send_mail(
            'Verification Email',
            'Please Verify',
            sender,
            [receiver],
            html_message=html_message,
        )
