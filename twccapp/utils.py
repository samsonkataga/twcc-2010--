# utils.py
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import os
from django.shortcuts import render, redirect, get_object_or_404


def send_newsletter_email(subscriber, newsletter):
    subject = f"TWCC Newsletter: {newsletter.title}"
    body = render_to_string('twccapp/newsletter_email.html', {
        'subscriber': subscriber,
        'newsletter': newsletter
    })
    
    email = EmailMessage(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [subscriber.email],
    )
    
    # Attach the PDF
    if newsletter.pdf_file:
        file_path = newsletter.pdf_file.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                email.attach(
                    f'TWCC_Newsletter_{newsletter.title}.pdf',
                    f.read(),
                    'application/pdf'
                )
    
    email.send()