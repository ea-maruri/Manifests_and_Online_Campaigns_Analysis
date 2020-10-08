from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http.response import HttpResponse

# Import forms
from Manifests_and_Online_Campaigns_Analysis.forms import ContactForm, CreateCandidateForm, ConfigureCaseStudyForm

# Import model
from StudyCasesManage.models import Campaign


# Create your views here.
def home(request):
  """Renders the home page"""

  campaigns = []
  candidates = []
  candidates_docs = []
  context = {"campaigns": campaigns, "candidates": candidates, "docs": candidates_docs}

  return render(request, "home.html", context)



def cases_study_search(request):
  """Renders the form 'cases-study-search'"""

  return render(request, "forms/cases-study-search.html")



def search_case(request):
  """Renders and ensures the message is given to the server"""

  if request.GET["case_study"]:
    case_study = request.GET["case_study"]  # Case searched

    if len(case_study) > 20:
      message = "Too long text for searching"

    else:
      # icontrains works as LIKE of SQL
      # E.G: SELECT * FROM Campaign LIKE name='a given case'
      cases = Campaign.objects.filter(name__icontains=case_study)

      return render(request, "forms/cases-study-results.html", {"cases": cases, "query": case_study})

  else:
    message = "Sorry, a bad entry was received"

  return HttpResponse(message)



def contact(request):
  if request.method == "POST":
    #   subject = request.POST["contact_subject"]
    #   message = request.POST["contact_message"] + "\nMy email is " + request.POST["contact_email"]
    #   email_from = settings.EMAIL_HOST_USER
    #   recipient_list = ["ea.maruri@gmail.com"]

    my_form = ContactForm(request.POST)

    if my_form.is_valid():
      form_info = my_form.cleaned_data

      # send_mail(subject, message, email_from, recipient_list)
      send_mail(
          form_info['subject'],
          form_info['message'],
          form_info.get('email', settings.EMAIL_HOST_USER),
          ["ea.maruri@gmail.com"]
      )

      return render(request, "forms/thanks.html")

  else:
    my_form = ContactForm()

  return render(request, "forms/contact-form.html", {"form": my_form})  




def login(request):
  return render(request, "forms/login.html")



def register(request):
  return render(request, "forms/register.html")

