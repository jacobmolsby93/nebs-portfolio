from django import forms
from .models import Contact, Image, Video


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 
                  'message',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholder and classes, remove auto-generated
        labels and set autofocus on first field
        """

        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Name',
            'email': 'Email',
            'subject': 'Subject',
            'message': 'Message',
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = '__all__'


class VideoForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = '__all__'