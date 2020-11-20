import base64
from math import cos
from django.http import request
from django.http.response import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render

import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np
import io
import urllib
import base64


# Models
from StudyCasesManage.models import Campaign, Candidate, Manifest, SocialMediaAccount

# Forms
from .forms import CreateCandidateForm, ConfigureCaseStudyForm, DataCollectionForm, DocumentConfForm, AnalysisConf, CreateSocialMediaAccount, DocumentForm, ComputeCollectionForm

# Own utilities
import StudyCasesManage.logic.ea_db_utilities as db_util

# Constants
ERROR_MESSAGE = 'Something went wrong: '
CONF_PAGE = 'configurator-base.html'
IS_COLLECTING = False


# Create your views here.

@login_required 
# @permission_required('????')
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

        print('Campaign to create', campaign_to_create)
        try:
          campaign_to_create.save()
          print('Correct!')

        except Exception as e:
          print('Fail!')
          messages.error(request, ERROR_MESSAGE + str(e))
          return render(request, "middle/case-study-conf.html", {"form": conf_cases_form})

        campaign_id = campaign_to_create.id

        messages.success(
            request, 
            'Campaign "%s" created successfully. It\'s id is %s' % (form_info['name'], campaign_id)
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

      print('Candidate to create:', candidate_to_create)
      try:
        candidate_to_create.save()
        print('Correct!')
      except Exception as e:
        print('Fail!')
        messages.error(request, ERROR_MESSAGE + str(e))
        return render(request, "middle/case-study-conf.html", {"form": conf_cases_form})

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

      print('Account to create:', account_to_create)
      try:
        account_to_create.save()
        print('Correct')
      except Exception as e:
        print('Fail!')
        messages.error(request, ERROR_MESSAGE + str(e))
        return render(request, "middle/case-study-conf.html", {"form": conf_cases_form})

      messages.success(
          request, 
          'Account "%s" for %s created successfully.' % (account_to_create, candidate)
      )
  

    # Handle document form
    document_form = DocumentForm(request.POST or None, request.FILES or None)
    if document_form.is_valid():
      print('Valid Form')
      if request.FILES['manifest']:
        form_info = document_form.cleaned_data
        print("Form info:", form_info)

        try:
          document_form.save()  # DO not save, instead update (CHECK IT)
          print('File Added')
        except Exception as e:
          messages.error(request, ERROR_MESSAGE + str(e))
          return render(request, "middle/document-conf.html", {"form": document_form})

        messages.success(
            request,
            'Manifest "%s" for %s added successfully.' % (
                form_info['name'], form_info['candidate_id'])
        )

    else:
      print("NO UPLOAD (form no valid)")
      print(document_form.errors)

  else:
    conf_cases_form = ConfigureCaseStudyForm()
    create_candidate_form = CreateCandidateForm(campaigns_tuple)
    create_social_account = CreateSocialMediaAccount(candidates_tuple)
    document_form = DocumentForm()


  forms = [conf_cases_form, create_candidate_form, create_social_account]
  forms_names = ['Case Study', 'Candidate', 'Account']

  # return render(request, "middle/document-conf.html", {"form": document_form})
  return render(
    request, 
    "middle/case-study-conf.html", 
    {"forms": forms, 
      "forms_names": forms_names, 
      "conf_cases_form": conf_cases_form, 
      "create_candidate_form": create_candidate_form,
      "create_social_account": create_social_account,
      "document_form": document_form,
    }, 
  )



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


    # Handle compute data collection form
    compute_collection_form = ComputeCollectionForm(campaigns_tuple, request.POST)
    if compute_collection_form.is_valid():
      form_info = compute_collection_form.cleaned_data
    
      # Received as <QuerySet [('Test Study Case - 2020',)]>, for this, choose [0][0] which is a str
      campaign_name = Campaign.objects.values_list('name').filter(id=form_info['case_study'])[0][0]
      print("Campaign to collect:", campaign_name, "\nForm info:", form_info)

      #compute_collection(campaign_name: str, count: int, since: str, until: str)
      compute_collection(
              campaign_name,
              form_info['posts_limit'], 
              form_info['from_date'], 
              form_info['until_date']
            )
      
      messages.success(
          request,
          "Computing data collection for " + campaign_name + '.' + 
          " From: " + form_info['from_date'] + " To: " + form_info['until_date'] + "... Check 'your_url/admin/'."
      )


  return render(
    request, 
    "middle/collection-conf.html", 
    {"conf_data_form": data_collection_form, "compute_data_collect": compute_collection_form,}
  )



def analysis_conf(request):
  campaigns_tuple = db_util.get_campaigns_tuple()
  analysis_conf_form = AnalysisConf(campaigns_tuple, request.POST)

  if request.method == 'POST':
    if analysis_conf_form.is_valid():
      print('\nStarting analysis...')
      form_info = analysis_conf_form.cleaned_data
      campaign = Campaign.objects.get(id=form_info['case_study'])
      candidates = Candidate.objects.values_list('id', 'name', 'lastname').filter(campaign_id=campaign)
      print('Candidates:', candidates)

      cosine_results = list()
      cosine_results_dict = dict()

      metric = int(form_info['metric'])
      print('Metric:', metric)
      
      for candidate in candidates:
        # print('The Candidate:', candidate, '\tType:', str(type(candidate)))  # Is a tuple
        manif = db_util.get_manifest(id=candidate[0])  # str
        print('Manifest:', manif)

        from StudyCasesManage.logic.ea_data_process import document_content, process_data, posts_content

        manif_content = document_content(manif)
        if "Error" in manif_content:
          print(manif_content)
          print('Do not include', candidate)
          message = ERROR_MESSAGE + 'Do not include ' + str(candidate[0]) + ' ' +candidate[1] + ' ' + candidate[2] + '(Due to manifest problem)'
          messages.error(request, message=message)
          continue  # Do not include this candidate
          # return HttpResponse('Get a manifest.', manif_content)

        # posts_text = posts_content(cand_name=candidate[1] + ' ' + candidate[2])
        posts_text = posts_content(candidate_id=candidate[0])
        if "Error" in posts_text:
          print(posts_text)
          message = ERROR_MESSAGE + 'Do not include ' + str(candidate[0]) + ' ' +candidate[1] + ' ' + candidate[2] + '(Due to posts error)'
          messages.error(request, message=message)
          continue
          # return HttpResponse('Get Posts.', posts_text)

        # print('Posts text\n', posts_text)
        result = process_data(manifest_content=manif_content, posts_grouped=posts_text, metric=metric)

        if result[0] == 1:
          # values_in_manifestos = list()
          # values_in_manifestos_npMatrix = np.array(values_in_manifestos)
          # heat_map = sns.heatmap(np.transpose(values_in_manifestos_npMatrix), cmap='Blues',
          #                        annot=labels_values_in_manifestos, linewidths=.5, fmt='',
          #                        annot_kws={"size": 17}, cbar=False)
          # heat_map.set_yticklabels(labels_y, rotation=0, fontsize=17)
          # heat_map.set_xticklabels(candidates_in_manifestos, rotation=25, fontsize=17)
          # #cbar = heat_map.collections[0].colorbar
          #cbar.ax.tick_params(labelsize=12)
          # plt.xlabel("Candidates", fontsize=18)
          # #plt.ylabel("Evaluated Metrics", fontsize=16)
          # plt.title("Candidate Timelines versus Manifestos", fontsize=24)
          # plt.savefig("Candidate Timelines versus Manifestos - Comparison.pdf", bbox_inches='tight')
          # plt.show()

          cosine_results.append(result[1])
          cosine_results_dict[candidate[1] + ' ' + candidate[2]] = result[1]
          similarities = result[1]  # a dict
          cosine_results_dict[candidate[1] + ' ' + candidate[2]] = similarities

      if metric == 1:
        print(cosine_results_dict)
        # plt.figure(figsize=(1,1))
        plt.bar(range(len(cosine_results_dict)), list(cosine_results_dict.values()), align='center')
        plt.xticks(range(len(cosine_results_dict)), list(cosine_results_dict.keys()), rotation=45)
        # plt.title(str(cosine_results_dict))
        # plt.text(0, 0, str(cosine_results_dict))
        # plt.legend(cosine_results_dict)

        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        return render(request, 'analysis-result.html', {'data': uri})

      else:
        print('No Metric received!!!')
    else:
      print('Something')

  return render(request, "middle/analysis-conf.html", {"form": analysis_conf_form})



def document_conf(request):

  document_form = DocumentForm(request.POST or None, request.FILES or None)

  if request.method == 'POST' and request.FILES['manifest']: 
    if document_form.is_valid():
      form_info = document_form.cleaned_data
      print("Form info:", form_info)

      try:
        document_form.save()  # DO not save, instead update (CHECK IT)
      except Exception as e:
        messages.error(request, ERROR_MESSAGE + str(e))
        return render(request, "middle/document-conf.html", {"form": document_form})

      messages.success(
        request, 
        'Manifest "%s" for %s added successfully.' % (form_info['name'], form_info['candidate_id'])
      )

    else:
      print("NO UPLOAD")

  return render(request, "middle/document-conf.html", {"form": document_form})



def delete_account(request):
  return render(request, "middle/account.html")



def get_manifest(request):
  candidate_name = 'Jorge Yunda'  # 'Guillermo Lasso'
  manif = db_util.get_manifest(candidate_name)  # str
  print(manif)
  from StudyCasesManage.logic.ea_data_process import document_content, process_data, posts_content
  
  manif_content = document_content(manif)
  if "Error" in manif_content:
    print(manif_content)
    return HttpResponse('Get a manifest ' + manif_content)
  
  posts_text = posts_content(cand_name=candidate_name)
  if "Error" in posts_text:
    print(posts_text)
    return HttpResponse('Get a manifest ' + posts_text)

  print('Posts text\n', posts_text)
  posts_text = "Hello, this is a test"
  process_data(manifest_content=manif_content, posts_grouped=posts_text)
  return HttpResponse('Get a manifest ' + manif)


# Not a view
def compute_collection(campaign_name: str, count: int, since: str, until: str):
  from StudyCasesManage.logic.ea_get_time_lines import main

  screen_names_list = db_util.get_screen_names_list(campaign_name)
  print("Screen names in %s: %s" %(campaign_name, screen_names_list))
  
  main(screen_names=screen_names_list, count=count, until=until, since=since)
