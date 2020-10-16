from StudyCasesManage.models import Campaign, Candidate, SocialMediaAccount

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
