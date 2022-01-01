from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import ContactForm
from django.core.paginator import Paginator
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Image, Video
from .forms import ImageForm

# Create your views here.


def index(request):
    """
    A view to render the home page
    """
    videos = Video.objects.all()
    images = Image.objects.all()

    template = 'home/index.html'
    context = {
        'videos': videos,
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


@login_required
def add_photo(request):
    """ Add a photo to the gallery"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            messages.success(request, 'Successfully added Image!')
            return redirect(reverse('home'))
        else:
            messages.error(request, 'Failed to add Image. Please ensure the form is valid')
    else:
        form = ImageForm()
    
    template = 'home/add_photo.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def delete_image(request, image_id):
    """
    Delete an Image
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
        
    image = get_object_or_404(Image, pk=image_id)
    image.delete()
    messages.success(request, 'Image deleted!')
    return redirect(reverse('home'))


@login_required
def edit_image(request, image_id):
    """
    Edit a product in the store
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    image = get_object_or_404(Image, pk=image_id)

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated image!')
            return redirect(reverse('home'))
        else:
            messages.error(request, 'Failed to update image. Please ensure the form is valid.')
    else:
        form = ImageForm(instance=image)
        messages.info(request, f'Your are editing {image.name}')
    
    template = 'home/edit_gallery.html'
    context = {
        'form': form,
        'image': image,
    }

    return render(request, template, context)
