from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.paginator import Paginator
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from .models import Image

# Create your views here.


def index(request):
    """
    A view to render the home page
    """
    images = Image.objects.all()
    paginator = Paginator(images, 10)

    template = 'home/index.html'
    context = {
        'images': images,
    }
    return render(request, template, context)


def about(request):
    """
    A view to render the home page
    """

    template = 'home/about.html'
    context = {}
    return render(request, template, context)


def contact(request):
    """
    A view to render the contact form
    """

    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        form_name = request.POST['name']
        form_email = request.POST['email']
        if form.is_valid():
            form.save()
            subject = form.cleaned_data['subject']
            form = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
            }
            name = form['name']
            message = form['message']
            form = ContactForm()
            try:
                send_mail(
                    subject,
                    f'Name: {name}\nMessage: {message}',
                    request.POST.get('email'),
                    [settings.DEFAULT_FROM_EMAIL],
                )
                # messages.success(request, 'Sucesfully sent email')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            context = {
                'form_name': form_name,
                'form_email': form_email,
                'form': form,
            }
            template = 'home/contact.html'
            return render(request, template, context)
    else:
        context = {
            'form': form,
        }
        template = 'home/contact.html'
        return render(request, template, context)