from datetime import datetime
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from Manifests_and_Online_Campaigns_Analysis.forms import ContactForm, CreateCandidateForm, ConfigureCaseStudyForm
#from .classes import Campaign

# Import Models
from StudyCasesManage.models import Campaign



# class Campaign(object):
#   """Class wich represents a Campaign
#   Args:
#     object
#   """  
#   def __init__(self, id: str, start_date: datetime, end_date: datetime, desc: str):
#     self.id = id
#     self.start_date = start_date
#     self.end_date = end_date
#     self.description = desc

#     self.candidates_list = list()

#   def add_candidate(self, name: str):
#     self.candidates_list.append(name)


# class Candidate(object):
#   def __init__(self, name:str):
#     self.name = name
#     self.documents = list()

#   def add_document(self, name:str):
#     self.documents.append(name)


# class Docment(object):
#   def __init__(self, name:str):
#     self.doc_name = name


# a = datetime(2020, 10, 1)
# b = datetime(2020, 12, 31)
# camp0 = Campaign("1", a, b, "Case Study 1")
# camp1 = Campaign("2", a, b, "Case Study 2")
# camp2 = Campaign("3", a, b, "Case Study 3")
# camp3 = Campaign("4", a, b, "Case Study 4")


def home(request):
  """Renders the home page"""
  # db_helper = DBHelper()
  # campaigns = db_helper.campaigns

  # campaigns = [camp0, camp1, camp2, camp3]

  # cand = Candidate("Alejandro")
  # cand.add_document(Docment("Manifest"))
  # cand.add_document(Docment("Manif. 2"))
  # camp0.add_candidate(cand)
  # camp0.add_candidate(Candidate("Daniel"))
  # camp0.add_candidate(Candidate("Jorge"))

  # candidates = list()
  # candidates_docs = list()
  # for camp in campaigns:
  #   for candidate in camp.candidates_list:
  #     candidates.append(candidate.name)
  #     for doc in candidate.documents:
  #       print(type(doc))
  #       print(doc)
  #       candidates_docs.append(candidate.name + "_" + doc.doc_name)

  # print(candidates_docs)

  campaigns = []
  candidates = []
  candidates_docs = []
  context = {"campaigns": campaigns, "candidates": candidates, "docs": candidates_docs}

  return render(request, "home.html", context)



def configurator(request):
  """Renders the request page"""

  create_candidate_form = CreateCandidateForm()
  conf_cases_form = ConfigureCaseStudyForm()

  return render(request, "configurator.html", {"forms": [conf_cases_form, create_candidate_form]})



def cases_study_search(request):
  """Renders the form 'cases-study-search'"""

  return render(request, "forms/cases-study-search.html")



def search_case(request):
  """Renders and ensures the message is given to the server"""

  if request.GET["case_study"]:
    # message = "Case Study searched: %r" % request.GET["case_study"]
    case_study = request.GET["case_study"]

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
    my_form = ContactForm(request.POST)

    if my_form.is_valid():
      form_info = my_form.cleaned_data

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


  # if request.method == "POST":
  #   subject = request.POST["contact_subject"]
  #   message = request.POST["contact_message"] + "\nMy email is " + request.POST["contact_email"]
  #   email_from = settings.EMAIL_HOST_USER
  #   recipient_list = ["ea.maruri@gmail.com"]

  #   send_mail(subject, message, email_from, recipient_list)

  #   return render(request, "forms/thanks.html")

  # return render(request, "forms/contact.html")
