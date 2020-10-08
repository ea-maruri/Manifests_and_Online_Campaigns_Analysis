from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render

# Fomrs
from .forms import CreateCandidateForm, ConfigureCaseStudyForm, DataCollectionForm, DocumentConfForm, AnalysisConf


# Create your views here.
def configurator(request):
  """Renders the request page"""

  create_candidate_form = CreateCandidateForm()
  conf_cases_form = ConfigureCaseStudyForm()

  data_collection_form = DataCollectionForm()

  document_conf_form = DocumentConfForm()

  analysis_conf_form = AnalysisConf()

  return render(request, "configurator.html", 
                  {
                    "forms": [conf_cases_form, create_candidate_form], 
                    "collection_conf": data_collection_form,
                    "document_conf": document_conf_form,
                    "analysis_conf": analysis_conf_form
                  }
  )



def case_study_conf(request):
  return HttpResponse("Case Study Conf")



def create_entity(request):
  return HttpResponse("Create entity")



def data_collection_conf(request):
  data_collection_form = DataCollectionForm()

  return render(request, "requ", )



def analysis_conf(request):
  return HttpResponse("Analysis Conf")



def document_conf(request):
  return HttpResponse("Document Conf")



def delete_account(request):
  return HttpResponse("Delete account")
