from django.db.models import fields
from StudyCasesManage.models import Manifest
from django import forms
from django.forms.widgets import DateInput



# iterable
METRICS = (
  ("1", "Cosine"),
  ("2", "L1"),
  ("3", "L2"),
)

CHOICES = (
  ("1", "One"),
  ("2", "Two"),
  ("3", "Three"),
  ("4", "Four"),
  ("5", "Five"),
)

SOCIAL_ACCOUNTS = (
  ("Twitter", "Twitter"),
  ("Facebook", "Facebook"),
  ("Instagram", "Instagram"),
)


CAMPAIGN_LABEL = "Case Study"

class DataCollectionForm(forms.Form):

  def __init__(self, campaigns: tuple, *args, **kwargs):
    super(DataCollectionForm, self).__init__(*args, **kwargs)
    self.fields["case_study"] = forms.ChoiceField(choices=campaigns, label=CAMPAIGN_LABEL)


  case_study = forms.ChoiceField()

  start_date = forms.DateField(
    widget=forms.DateInput(attrs={'placeholder': 'yyyy-mm-dd'}),
    label="",
  )

  end_date = forms.DateField(
    widget=forms.DateInput(attrs={'placeholder': 'yyyy-mm-dd'}),
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
  name = forms.CharField(
      widget=forms.TextInput(attrs={'placeholder': "Campaign's name"}),
      label=""
  )

  start_date = forms.DateField(
      widget=DateInput(attrs={'placeholder': 'yyyy-mm-dd'}),
      label=""
  )

  end_date = forms.DateField(
      widget=forms.DateInput(attrs={'placeholder': 'yyyy-mm-dd'}),
      label=""
  )

  description = forms.CharField(
      widget=forms.Textarea(attrs={'placeholder': 'Description'}),
      label=""
  )



class CreateCandidateForm(forms.Form):
  def __init__(self, campaigns: tuple, *args, **kwargs):
    super(CreateCandidateForm, self).__init__(*args, **kwargs)
    self.fields["case_study"] = forms.ChoiceField(
        choices=campaigns, label=CAMPAIGN_LABEL)

  case_study = forms.ChoiceField()
  
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



class CreateSocialMediaAccount(forms.Form):
  def __init__(self, candidates: tuple, *args, **kwargs):
    super(CreateSocialMediaAccount, self).__init__(*args, **kwargs)
    self.fields["candidate"] = forms.ChoiceField(
        choices=candidates, label="Candidate")

  candidate = forms.ChoiceField()

  screen_name = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder': 'Screen name'}),
    label=""
  )

  account = forms.ChoiceField(
    choices=SOCIAL_ACCOUNTS,
    label="Account"
  )



class DocumentConfForm(forms.Form):
  def __init__(self, candidates: tuple, *args, **kwargs):
    super(DocumentConfForm, self).__init__(*args, **kwargs)
    self.fields["candidate"] = forms.ChoiceField(
        choices=candidates, label="Candidate")

  candidate = forms.ChoiceField()

  document = forms.FileField(max_length=1000)


class AnalysisConf(forms.Form):
  def __init__(self, campaigns: tuple, *args, **kwargs):
    super(AnalysisConf, self).__init__(*args, **kwargs)
    self.fields["case_study"] = forms.ChoiceField(choices=campaigns, label=CAMPAIGN_LABEL)

  case_study = forms.ChoiceField()

  metric = forms.ChoiceField(
    choices=METRICS,
    label="Metric"
  )


class ComputeCollectionForm(forms.Form):
  def __init__(self, campaigns: tuple, *args, **kwargs):
    super(ComputeCollectionForm, self).__init__(*args, **kwargs)
    self.fields["case_study"] = forms.ChoiceField(
        choices=campaigns, label=CAMPAIGN_LABEL)

  case_study = forms.ChoiceField()
  from_date = forms.CharField(
    widget=forms.TextInput(attrs={"placeholder": "yyyy-mm-dd"}),
    label='From'
  )
  until_date = forms.CharField(
    widget=forms.TextInput(attrs={"placeholder": "yyyy-mm-dd"}),
    label='Until'
  )
  posts_limit = forms.IntegerField()


# TEST FORM
# create a ModelForm
class DocumentForm(forms.ModelForm):
  # def __init__(self, *args, **kwargs):
  #   super(DocumentForm, self).__init__(*args, **kwargs)
  #   self.fields["document"] = forms.FileField(
  #     widget=forms.FileInput(attrs={'name': 'myfile',})
  #   )

  class Meta:
    model = Manifest  # specify the name of model to use
    fields = "__all__"


class UploadFileForm(forms.Form):
  title = forms.CharField(max_length=50)
  file = forms.FileField()
