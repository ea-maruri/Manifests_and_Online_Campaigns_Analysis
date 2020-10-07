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
  


class ConfigureCaseStudyForm(forms.Form):
  campaig_name = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder': "Campaign's name"}),
    label=""
  )

  start_date = forms.DateField(
    widget=forms.TextInput(attrs={'placeholder': 'Start date'}),
    label=""
  )

  end_date = forms.DateField(
    widget=forms.TextInput(attrs={'placeholder': 'End date'}),
    label=""
  )

  description = forms.CharField(
    widget=forms.Textarea(attrs={'placeholder': 'Description'}),
    label=""
  )
  


class CreateCandidateForm(forms.Form):
  name = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder': 'Name'}),
    label=""
  )

  lastname = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
    label=""
  )

  type = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder': 'Type'}),
    label="",
    required=False
  )

  party = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder': 'Party'}),
    label="",
    required=False
  )

  candidates_list = forms.CharField(
    widget=forms.Textarea(attrs={'placeholder': 'List...', 'readonly': 'true'}),
    label=""
  )
