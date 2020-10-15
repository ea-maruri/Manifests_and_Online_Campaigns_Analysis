from os import name
from StudyCasesManage.models import Campaign, Candidate, SocialMediaAccount
from django.http import request
from django import http
from django.http.response import HttpResponse
from django.contrib import messages
from django.shortcuts import render

# Fomrs
from .forms import CreateCandidateForm, ConfigureCaseStudyForm, DataCollectionForm, DocumentConfForm, AnalysisConf, CreateSocialMediaAccount


# Create your views here.
def configurator(request):
  """Renders the request page"""

  # Tuples used in forms
  campaigns_tuple = get_campaigns_tuple()
  candidates_tuple = get_candidates_tuple()

  
  # Forms
  data_collection_form = DataCollectionForm(campaigns_tuple)
  document_conf_form = DocumentConfForm()
  analysis_conf_form = AnalysisConf()
  create_candidate_form = CreateCandidateForm(campaigns_tuple)
  create_social_account = CreateSocialMediaAccount(candidates_tuple)


  # Handling forms
  if request.method == 'POST':
    conf_cases_form = ConfigureCaseStudyForm(request.POST)
    if conf_cases_form.is_valid():
      form_info = conf_cases_form.cleaned_data

      # Create the campaign
      campaign_to_create = Campaign(
                            name = form_info['name'], 
                            start_date = form_info['start_date'], 
                            end_date = form_info['end_date'], 
                            description = form_info['description']
                          )
      
      try:
        campaign_to_create.save()
        
      except Exception as e:
        messages.error(request, 'Something went wrong: ' + str(e))
        return render(request, "configurator.html",
                      {
                          "forms": [conf_cases_form, create_candidate_form],
                          "collection_conf": data_collection_form,
                          "document_conf": document_conf_form,
                          "analysis_conf": analysis_conf_form
                      }
                      )

      campaign_id = campaign_to_create.id

      messages.success(
        request, 'Campaign "%s" created successfully. It\'s id is %s' % (form_info['name'], campaign_id)
      )


    # Handle create candidate form
    create_candidate_form = CreateCandidateForm(campaigns_tuple, request.POST)
    if create_candidate_form.is_valid():
      form_info = create_candidate_form.cleaned_data

      campaign = Campaign.objects.get(id=form_info['case_study'])
      candidate_to_create = Candidate(
          campaign_id=campaign,
          name=form_info['name'],
          lastname=form_info['lastname'],
          type=form_info['type'],
          party=form_info['party']
      )

      try:
        candidate_to_create.save()
      except Exception as e:
        messages.error(request, 'Something went wrong: ' + str(e))
        return render(request, "configurator.html",
                      {
                          "forms": [conf_cases_form, create_candidate_form],
                          "collection_conf": data_collection_form,
                          "document_conf": document_conf_form,
                          "analysis_conf": analysis_conf_form
                      }
                      )

      candidate_id = candidate_to_create.id

      messages.success(
          request, 'Candidate "%s %s" on %s campaign created successfully. It\'s id is %s' % (
              form_info['name'], form_info['lastname'], campaign, candidate_id)
      )



    create_social_account = CreateSocialMediaAccount(candidates_tuple, request.POST)
    if create_social_account.is_valid():
      form_info = create_social_account.cleaned_data

      candidate = Candidate.objects.get(id=form_info['candidate'])
      account_to_create = SocialMediaAccount(
        candidate_id=candidate,
        screen_name = form_info['screen_name'],
        account = form_info['account']
      )

      try:
        account_to_create.save()
      except Exception as e:
        messages.error(request, 'Something went wrong: ' + str(e))
        return render(request, "configurator.html",
                      {
                          "forms": [conf_cases_form, create_candidate_form],
                          "collection_conf": data_collection_form,
                          "document_conf": document_conf_form,
                          "analysis_conf": analysis_conf_form
                      }
                      )


      messages.success(
          request, 'Account "%s" for %s created successfully.' % (
              account_to_create, candidate)
      )


  else:
    conf_cases_form = ConfigureCaseStudyForm()


  return render(request, "configurator.html", 
                  {
                    "forms": [conf_cases_form, create_candidate_form, create_social_account], 
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


## Used methods
def get_campaigns_tuple():
  campaigns_list = list()
  for camp in Campaign.objects.values_list('id', 'name'):
    campaigns_list.append(camp)
  
  return tuple(campaigns_list)


def get_candidates_tuple():
  candidates_list = list()
  for cand in Candidate.objects.values_list('id', 'name', 'lastname'):
    new_candidate = (cand[0], str(cand[1]) + ' ' + str(cand[2]))
    candidates_list.append(new_candidate)

  return tuple(candidates_list)

