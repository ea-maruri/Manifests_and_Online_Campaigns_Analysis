from django import forms
from django.core.mail import message
from django.forms import widgets

class ContactForm(forms.Form):
  subject = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder': 'Subject'}), 
    label=""
  )

  email = forms.EmailField(
    widget=forms.TextInput(attrs={'placeholder': 'Your email'}), 
    label=""
  )

  message = forms.CharField(
    widget=forms.Textarea(attrs={'placeholder': 'Your message'}),
    label=""
  )
  
