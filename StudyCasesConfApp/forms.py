from django import forms
from django.forms.widgets import DateInput


from StudyCasesManage.models import Campaign


# iterable
CHOICES = (
    ("1", "One"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
    ("5", "Five"),
)


class DataCollectionForm(forms.Form):
  campaigns = list(Campaign.objects.all())
  # ids = Entry.objects.values_list('column_name', flat=True).filter(...)
  campaigns = Campaign.objects.values_list('id', 'name').filter()
  print(type(campaigns))
  print(campaigns)

  camps_as_list = list()
  for camp_id, camp_name in campaigns:
    print(camp_id, camp_name)
    camp_id = str(camp_id)
    camps_as_list.append((camp_id, camp_name))
  #   camps_as_tuple.__add__(tuple(camp))

  camps_as_tuple = tuple(camps_as_list)
  print(tuple(camps_as_tuple))


  case_study = forms.ChoiceField(
    #choices=Campaign.objects.all(),
    choices=camps_as_tuple,
    label="Case Study"
  )

  start_date = forms.DateField(
    widget=forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy'}),
    label=""
  )

  end_date = forms.DateField(
    widget=forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy'}),
    label=""
  )

  start_time = forms.TimeField(
    widget=forms.TimeInput(attrs={'placeholder': 'hh:mm'}),
    label=""
  )

  end_time = forms.TimeField(
    widget=forms.TimeInput(attrs={'placeholder': 'hh:mm'}),
    label=""
  )



class ConfigureCaseStudyForm(forms.Form):
  campaig_name = forms.CharField(
      widget=forms.TextInput(attrs={'placeholder': "Campaign's name"}),
      label=""
  )

  start_date = forms.DateField(
      widget=DateInput(attrs={'placeholder': 'dd/mm/yyyy'}),
      label=""
  )

  end_date = forms.DateField(
      widget=forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy'}),
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
      widget=forms.Textarea(
          attrs={'placeholder': 'List...', 'readonly': 'true'}),
      label=""
  )


class DocumentConfForm(forms.Form):
  case_study = forms.ChoiceField(
      #choices=Campaign.objects.all(),
      choices=CHOICES,
      label="Case Study"
  )

  candidate = forms.ChoiceField(
      #choices=Campaign.objects.all(),
      choices=CHOICES,
      label="Candidate"
  )



class AnalysisConf(forms.Form):
  case_study = forms.ChoiceField(
    #choices=Campaign.objects.all(),
    choices=CHOICES,
    label="Case Study"
  )

  metric = forms.ChoiceField(
      #choices=Campaign.objects.all(),
      choices=CHOICES,
      label="Metric"
  )
