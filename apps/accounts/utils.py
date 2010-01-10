import datetime
import hashlib

from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string


from stark.apps.accounts.models import EmailConfirmation

def request_confirmation(request, email):
    # sha1 hash based on time, user ID and email address
    key = hashlib.sha1("%s%s%s" % (
        datetime.datetime.now(),
        request.user.id, email)
    ).hexdigest()

    EmailConfirmation.objects.create(user=request.user,
                                     email=email,
                                     key=key,
                                     created=datetime.datetime.now())

    link = "%s%s" % (request.get_host(),
                     reverse('confirm_email', args=[key]))
    
    subject = 'Stark e-mail confirmation'
    msg = render_to_string('emails/confirmation.txt', {
                                'link': link,
                                'email': email,
                            })
    from_email = 'stark@teebes.com'
    to_email = [email]
    
    send_mail(subject, msg, from_email, to_email, fail_silently=False)

