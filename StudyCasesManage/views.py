from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http.response import HttpResponse

# Own utilities
import StudyCasesManage.logic.ea_db_utilities as db_util

# Import forms
from Manifests_and_Online_Campaigns_Analysis.forms import ContactForm

#
# Views
#
def home(request):
  """Renders the home page"""

  campaigns_tuple = db_util.get_all_campaigns()
  candidates_tuple = db_util.get_candidates_tuple()
  candidates_docs = db_util.get_all_documents()
  context = {
            "campaigns": campaigns_tuple, 
            "candidates": candidates_tuple,
            "docs": candidates_docs
            }

  return render(request, "home.html", context)



def contact(request):
  if request.method == "POST":
    #   subject = request.POST["contact_subject"]
    #   message = request.POST["contact_message"] + "\nMy email is " + request.POST["contact_email"]
    #   email_from = settings.EMAIL_HOST_USER
    #   recipient_list = ["ea.maruri@gmail.com"]

    my_form = ContactForm(request.POST)

    if my_form.is_valid():
      form_info = my_form.cleaned_data

      # send_mail(subject, message, email_from, recipient_list)
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



def login(request):
  return render(request, "forms/login.html")



def register(request):
  return render(request, "forms/register.html")

