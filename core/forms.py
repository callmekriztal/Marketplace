from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, Message


# Styling helper dictionary for standard inputs
INPUT_CLASSES = 'w-full py-3 px-4 border border-gray-300 rounded-xl focus:outline-none focus:border-teal-500'


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': INPUT_CLASSES}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = INPUT_CLASSES


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'title', 'description', 'price', 'image')
        widgets = {
            'category': forms.Select(attrs={'class': INPUT_CLASSES}),
            'title': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g., Vintage Leather Jacket'}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 4, 'placeholder': 'Describe your item...'}),
            'price': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': '0.00'}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES}),
        }


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'title', 'description', 'price', 'image', 'is_sold')
        widgets = {
            'category': forms.Select(attrs={'class': INPUT_CLASSES}),
            'title': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES}),
            'is_sold': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-teal-600 rounded border-gray-300 focus:ring-teal-500'}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Your Email Address'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 5, 'placeholder': 'Write your message here...'}))


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
                'rows': 3,
                'placeholder': 'Write your message to the seller...'
            }),
        }
