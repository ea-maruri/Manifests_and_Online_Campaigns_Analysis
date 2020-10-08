from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render

#
from Manifests_and_Online_Campaigns_Analysis.forms import ContactForm, CreateCandidateForm, ConfigureCaseStudyForm

# Create your views here.
def configurator(request):
  """Renders the request page"""

  create_candidate_form = CreateCandidateForm()
  conf_cases_form = ConfigureCaseStudyForm()

  return render(request, "configurator.html", {"forms": [conf_cases_form, create_candidate_form]})



def case_study_conf(request):
  return HttpResponse("Case Study Conf")



def create_entity(request):
  return HttpResponse("Create entity")



def data_collection_conf(request):
  return HttpResponse("Data collectionConf")



def analysis_conf(request):
  return HttpResponse("Analysis Conf")



def document_conf(request):
  return HttpResponse("Document Conf")



def delete_account(request):
  return HttpResponse("Delete account")
