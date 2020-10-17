# from django.core.files.storage import FileSystemStorage
from django.http.response import HttpResponse
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Models
from StudyCasesManage.models import Campaign, Candidate, Manifest, SocialMediaAccount

# Forms
from .forms import CreateCandidateForm, ConfigureCaseStudyForm, DataCollectionForm, DocumentConfForm, AnalysisConf, CreateSocialMediaAccount, DocumentForm, ComputeCollectionForm

# Own utilities
import StudyCasesManage.logic.ea_db_utilities as db_util

# Constant
ERROR_MESSAGE = 'Something went wrong: '
CONF_PAGE = 'configurator.html'


# Create your views here.
def configurator(request):
  """Renders the request page"""

  return render(request, CONF_PAGE)



def case_study_conf(request):
  campaigns_tuple = db_util.get_campaigns_tuple()
  candidates_tuple = db_util.get_candidates_tuple()
  
  if request.method == 'POST':

    # Handle create study case (campaign) form
    conf_cases_form = ConfigureCaseStudyForm(request.POST)
    if conf_cases_form.is_valid():
        form_info = conf_cases_form.cleaned_data

        # Create the campaign
        campaign_to_create = Campaign(
            name=form_info['name'],
            start_date=form_info['start_date'],
            end_date=form_info['end_date'],
            description=form_info['description']
        )

        try:
          campaign_to_create.save()

        except Exception as e:
          messages.error(request, ERROR_MESSAGE + str(e))
          return render(request, "middle/case_study_conf.html", {"form": conf_cases_form})

        campaign_id = campaign_to_create.id

        messages.success(
            request, 
            'Campaign "%s" created successfully. It\'s id is %s' % (form_info['name'], campaign_id)
        )


    # Hnadle creat candidate form
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
        messages.error(request, ERROR_MESSAGE + str(e))
        return render(request, "middle/case_study_conf.html", {"form": conf_cases_form})

      candidate_id = candidate_to_create.id

      messages.success(
          request, 
          'Candidate "%s %s" on %s campaign created successfully. It\'s id is %s' % 
          (form_info['name'], form_info['lastname'], campaign, candidate_id)
      )


    # Handle create account form
    create_social_account = CreateSocialMediaAccount(candidates_tuple, request.POST)
    if create_social_account.is_valid():
      form_info = create_social_account.cleaned_data

      candidate = Candidate.objects.get(id=form_info['candidate'])
      account_to_create = SocialMediaAccount(
          candidate_id=candidate,
          screen_name=form_info['screen_name'],
          account=form_info['account']
      )

      try:
        account_to_create.save()
      except Exception as e:
        messages.error(request, ERROR_MESSAGE + str(e))
        return render(request, "middle/case_study_conf.html", {"form": conf_cases_form})

      messages.success(
          request, 
          'Account "%s" for %s created successfully.' % (account_to_create, candidate)
      )
  
  else:
    conf_cases_form = ConfigureCaseStudyForm()
    create_candidate_form = CreateCandidateForm(campaigns_tuple)
    create_social_account = CreateSocialMediaAccount(candidates_tuple)
  

  forms = [conf_cases_form, create_candidate_form, create_social_account]

  return render(request, "middle/case_study_conf.html", {"forms": forms})



def create_entity(request):
  # Meanwhile equals to conf
  return case_study_conf(request)



def data_collection_conf(request):
  campaigns_tuple = db_util.get_campaigns_tuple()
  data_collection_form = DataCollectionForm(campaigns_tuple)

  compute_collection_form = ComputeCollectionForm(campaigns_tuple)

  if request.method == 'POST':

    data_collection_conf = DataCollectionForm(campaigns_tuple, request.POST)
    if data_collection_conf.is_valid():
      print("DO SOMETHING")


    compute_collection_form = ComputeCollectionForm(campaigns_tuple, request.POST)
    if compute_collection_form.is_valid():
      print("COMPUTE!!")
      form_info = compute_collection_form.cleaned_data
      print(form_info)

      # Received as <QuerySet [('Test Study Case - 2020',)]>, for this choose [0][0]
      campaign_name = Campaign.objects.values_list('name').filter(id=form_info['case_study'])[0][0]
      print("Campaign")
      print(campaign_name, str(type(campaign_name)))

      compute(request, campaign_name, form_info['posts_limit'], form_info['from_date'].replace('/', '-'))

      messages.success(
          request,
          "Computing data collection from " + campaign_name + "...\n\nCheck 'admin'."
      )


  return render(
    request, 
    "middle/collection_conf.html", 
    {"conf_data_form": data_collection_form, "compute_data_collect": compute_collection_form,}
  )



def analysis_conf(request):
  analysis_conf_form = AnalysisConf()
  return render(request, "middle/analysis_conf.html", {"form": analysis_conf_form})



def document_conf(request):

  form = DocumentForm(request.POST or None, request.FILES or None)

  if request.method == 'POST' and request.FILES['manifest']: 
    # manifest = request.FILES['document']
    # fs = FileSystemStorage()
    # filename = fs.save(manifest.name, manifest)
    # uploaded_file_url = fs.url(filename)
    # print("Upoladed to", uploaded_file_url)

    if form.is_valid():
      form_info = form.cleaned_data
      print("Form info:")
      print(form_info)
      print("UPLOAD...")

      try:
        form.save()  # DO not save, instead update (CHECK IT)
      except Exception as e:
        messages.error(request, ERROR_MESSAGE + str(e))
        return render(request, "middle/document_conf.html", {"form": form})

      messages.success(
        request, 
        'Manifest "%s" for %s added successfully.' % (form_info['name'], form_info['candidate_id'])
      )

    else:
      print("NO UPLOAD")

  return render(request, "middle/document_conf.html", {"form": form})



def delete_account(request):
  return render(request, "middle/del_account.html")
  

def compute(request, campaign_name: str, count: int, since: str):
  from StudyCasesManage.logic.ea_get_time_lines import main

  screen_names_list = db_util.get_screen_names_list(campaign_name)
  print("Screen names in", campaign_name)
  print(screen_names_list)
  
  main(screen_names_list, count, since)

  out_response = "Computing data collection from " + campaign_name + "...\n\nCheck 'admin'."
  return HttpResponse(out_response)

