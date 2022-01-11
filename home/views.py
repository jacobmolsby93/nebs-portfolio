from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import ContactForm
from itertools import chain
from django.core.paginator import Paginator
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Image, Video
from .forms import ImageForm, VideoForm


# Create your views here.


def index(request):
    """
    A view to render the home page
    """
    images = Image.objects.all().order_by("-created_on")
    videos = Video.objects.all().order_by("-created_on")
    items = list(chain(images, videos))

    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    template = 'home/index.html'
    context = {
        'videos': videos,
        'images': images,
        'items': page_obj
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

            message = f'Email from {form_name} from the email of {form_email}\n{form["message"]}'
            form = ContactForm()
            try:
                send_mail(
                    subject,
                    message,
                    from_email = settings.DEFAULT_FROM_EMAIL,
                    recipient_list = [settings.EMAIL_HOST_USER],
                    fail_silently=False,
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
def add_video(request):
    """ Add a video to the gallery"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            messages.success(request, 'Successfully added Video!')
            return redirect(reverse('home'))
        else:
            messages.error(request, 'Failed to add Video. Please ensure the form is valid')
    else:
        form = VideoForm()
    
    template = 'home/add_video.html'
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
def delete_video(request, video_id):
    """
    Delete a Video
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
        
    video = get_object_or_404(Video, pk=video_id)
    video.delete()
    messages.success(request, 'Video deleted!')
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
    
    template = 'home/edit_image.html'
    context = {
        'form': form,
        'image': image,
    }

    return render(request, template, context)


@login_required
def edit_video(request, video_id):
    """
    Edit a product in the store
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    video = get_object_or_404(Video, pk=video_id)

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated video!')
            return redirect(reverse('home'))
        else:
            messages.error(request, 'Failed to update video. Please ensure the form is valid.')
    else:
        form = VideoForm(instance=video)
        messages.info(request, f'Your are editing {video.caption}')
    
    template = 'home/edit_video.html'
    context = {
        'form': form,
        'video': video,
    }

    return render(request, template, context)


def site_management(request):
    return render(request, 'home/site_management.html')