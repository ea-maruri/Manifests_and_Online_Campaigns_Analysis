from os import name
from StudyCasesManage.models import Campaign, Candidate, SocialMediaAccount
from django.http import request
from django import http
from django.http.response import HttpResponse
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

# Fomrs
from .forms import CreateCandidateForm, ConfigureCaseStudyForm, DataCollectionForm, DocumentConfForm, AnalysisConf, CreateSocialMediaAccount


# Create your views here.
def configurator(request):
  """Renders the request page"""

  campaign_name = 'Test Campaign - 2020'
  screen_names_list = get_screen_names_list(campaign_name)
  print("Screen names in", campaign_name)
  print(screen_names_list)

  # Tuples used in forms
  campaigns_tuple = get_campaigns_tuple()
  candidates_tuple = get_candidates_tuple()

  
  # Forms
  data_collection_form = DataCollectionForm(campaigns_tuple)
  document_conf_form = DocumentConfForm(candidates_tuple)
  analysis_conf_form = AnalysisConf()
  create_candidate_form = CreateCandidateForm(campaigns_tuple)
  create_social_account = CreateSocialMediaAccount(candidates_tuple)


  # Handling forms
  if request.method == 'POST':
    # Handle create study case (campaign) form
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


    # Handle create account form
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


    document_conf_form = DocumentConfForm(candidates_tuple, request.POST, request.FILES)
    #print(document_conf_form)
    if document_conf_form.is_valid():
      print("DOCUMENT")
      form_info = document_conf_form.cleaned_data

      candidate = Candidate.objects.get(id=form_info['candidate'])
      document_to_create = SocialMediaAccount(
          candidate_id=candidate,
          document=form_info['document']
      )

      print("Suppose to create", document_to_create)
      try:
        document_to_create.save()
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
          request, 'Document "%s" for %s created successfully.' % (
              document_to_create, candidate)
      )

    else:
      print("Something happen in Doc")  

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



def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def handle_uploaded_file(f):
    with open('StudyCasesManage/uploads/manifests/%Y/%m/%d/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)




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


def get_screen_names_list(campaign_name: str):
  #TEST SELECT
  # accounts_list = SocialMediaAccount.objects.select_related(
  #     'candidate_id', 'campaign_id').values_list('screen_name').filter(name='Test Campaign - 2020')

  # accounts_list = Campaign.objects.get(name="Test Campaign - 2020")

  # print("\nList 1")
  # print()
  # print(accounts_list.__str__())

  the_query = """SELECT public."StudyCasesManage_socialmediaaccount"."id", screen_name 
                  FROM public."StudyCasesManage_socialmediaaccount"
                    INNER JOIN public."StudyCasesManage_candidate"
                      ON(public."StudyCasesManage_socialmediaaccount"."candidate_id_id"=public."StudyCasesManage_candidate"."id")
                    INNER JOIN public."StudyCasesManage_campaign"
                      ON(public."StudyCasesManage_candidate"."campaign_id_id"=public."StudyCasesManage_campaign"."id")
                  WHERE public."StudyCasesManage_campaign"."name"=""" + "'" + campaign_name + "'"


  screen_names_list = list()
  print('\nList 2')
  for account in SocialMediaAccount.objects.raw(the_query):
    screen_names_list.append(account.screen_name)

  return screen_names_list


# def handle_uploaded_file(f):   
#   with open("StudyCasesManage/uploads/manifests/%Y/%m/%d/" + f.name, 'wb +') as destination:
#     for chunk in f.chunks(): 
#       destination.write(chunk) 
