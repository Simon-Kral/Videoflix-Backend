from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from email.mime.image import MIMEImage


def send_activation_email(saved_account):

    if not saved_account.is_active:
        objective = 'activate_account'
        mail_data = get_mail_data(saved_account, objective)
        mail_texts = get_mail_texts(objective, mail_data)
        send_mail(mail_texts, saved_account)


def send_reset_password_email(user):

    objective = 'reset_password'
    mail_data = get_mail_data(user, objective)
    mail_texts = get_mail_texts(objective, mail_data)
    send_mail(mail_texts, user)


def get_mail_data(user, objective):

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    domain = get_domain()
    activation_endpoint = reverse(f'{objective}', kwargs={'uidb64': uid, 'token': token})

    username = user.email.split('@')[0]
    url = f'{domain}{activation_endpoint}'

    mail_data = {'username': username, 'url': url}

    return mail_data


def get_mail_texts(objective, mail_data):

    subjects = {'activate_account': 'Confirm your email', 'reset_password': 'Reset your Password'}
    subject = subjects[objective]
    content = get_content(objective, mail_data)

    return {'subject': subject, 'text_content': content['txt'], 'html_content': content['html']}


def get_content(objective, mail_data):
    content = {}
    for extension in ['txt', 'html']:
        file_path = f"emails/{objective}.{extension}"
        context = {"user": mail_data['username'], "url": mail_data['url']}
        content_entry = render_to_string(file_path, context=context)
        content.update({extension: content_entry})
    return content


def send_mail(content, user):

    img_path = 'auth_app/templates/emails/logo_w_text.png'

    msg = EmailMultiAlternatives(
        subject=content['subject'],
        body=content['text_content'],
        from_email=None,
        to=[user.email]
    )

    msg.attach_alternative(content['html_content'], "text/html")
    with open(img_path, 'rb') as img_file:
        image_data = img_file.read()
        msg.attach(get_logo(image_data))

    msg.send()


def get_logo(image_data):

    msg_logo = MIMEImage(image_data)
    msg_logo.add_header('Content-ID', '<logo>')
    msg_logo.add_header('Content-Disposition', 'inline', filename='logo_w_text.png')

    return msg_logo


def get_domain():

    if settings.DEBUG:
        return 'http://localhost:8000'

    current_site = get_current_site().domain
    return current_site.domain
