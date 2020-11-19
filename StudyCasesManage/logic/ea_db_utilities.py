from typing import Counter
from StudyCasesManage.models import Campaign, Candidate, Manifest, Post, SocialMediaAccount, Timeline


def get_all_campaigns():
  """Returns a list of Campaigns in the model"""
  campaigns_list = list()
  for camp in Campaign.objects.all():
    campaigns_list.append(camp)
  
  return campaigns_list



def get_all_documents():
  """Returns a list of Documents in the model"""
  docs_list = list()
  for doc in Manifest.objects.all():
    docs_list.append(doc)
  
  return docs_list



def get_campaigns_tuple():
  """Returns a list of Campaigns (id, name) in the model"""
  campaigns_list = list()
  for camp in Campaign.objects.values_list('id', 'name'):
    campaigns_list.append(camp)

  return tuple(campaigns_list)



def get_candidates_tuple():
  """Returns a list of Candidates (id, name lastname) in the model"""
  candidates_list = list()
  for cand in Candidate.objects.values_list('id', 'name', 'lastname'):
    new_candidate = (cand[0], str(cand[1]) + ' ' + str(cand[2]))
    candidates_list.append(new_candidate)

  return tuple(candidates_list)



def get_screen_names_list(campaign_name: str):
  """REeturns a list of screen names given a Campaign name"""

  the_query = """SELECT public."StudyCasesManage_socialmediaaccount"."id", screen_name 
                  FROM public."StudyCasesManage_socialmediaaccount"
                    INNER JOIN public."StudyCasesManage_candidate"
                      ON(public."StudyCasesManage_socialmediaaccount"."candidate_id_id"=public."StudyCasesManage_candidate"."id")
                    INNER JOIN public."StudyCasesManage_campaign"
                      ON(public."StudyCasesManage_candidate"."campaign_id_id"=public."StudyCasesManage_campaign"."id")
                  WHERE public."StudyCasesManage_campaign"."name"=""" + "'" + campaign_name + "'"

  screen_names_list = list()
  for account in SocialMediaAccount.objects.raw(the_query):
    screen_names_list.append(account.screen_name)

  return screen_names_list



def get_manifest(candidate_complete_name: str):
  """Returns a manifest given a candidate name"""
  # candidates = Candidate.objects.all()
  # print(candidates)

  try:
    # print("TRY:", candidate_complete_name.split()[0], candidate_complete_name.split()[1])
    candidate = Candidate.objects.get(name=candidate_complete_name.split()[0], lastname=candidate_complete_name.split()[1])
    manifest = Manifest.objects.filter(candidate_id=candidate)[0]
    # print('Received candidate:', candidate)
    # print('Manifest to return', manifest)
    return manifest.manifest.name
  
  except Exception as e:
    return 'Error at "get_manifest:" ' + str(e)



def get_posts_by_candidate(cand_name):
  try:
    print('Data in "get_posts_by_candidate"')
    candidate = Candidate.objects.get(name=cand_name.split()[0], lastname=cand_name.split()[1])
    print('\t', candidate)
    account = SocialMediaAccount.objects.get(candidate_id=candidate)
    print('\t', account)
    # timeline = Timeline.objects.get(social_media_id=account)
    timeline = Timeline.objects.filter(social_media_id=account).order_by('-id')[:1][0]  # Choose the last one
    print('\t', timeline)
    # posts = Post.objects.values_list('post_text').filter(timeline_id=timeline)
    # print('\t', posts)
    # print('Posts', len(posts))
    
    posts_content = ''
    counter = 0
    for post in Post.objects.values_list('post_text').filter(timeline_id=timeline):
      # post_text is a tuple, for this, choos zero position
      # print('Post:', post)
      posts_content += post[0]
      counter += 1

    print('Posts num:', counter)
    
    return posts_content
  
  except Exception as e:
    return "Error while collecting post by candidate: " + str(e)
