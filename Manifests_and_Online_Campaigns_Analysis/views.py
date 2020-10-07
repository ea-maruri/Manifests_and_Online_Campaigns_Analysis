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
