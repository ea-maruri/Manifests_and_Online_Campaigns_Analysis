from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login as dj_login
# Class for searching, filtering and ordering
from django.views.generic import ListView
from django.db.models import Q
# from django.contrib.auth.decorators import login_required

# Own utilities
import StudyCasesManage.logic.ea_db_utilities as db_util

# Import forms
from Manifests_and_Online_Campaigns_Analysis.forms import ContactForm, CustomUserCreationForm

from .models import Candidate, Post

# @login_required
class TableListView(ListView):
  paginate_by = 10
  model = Post
  ordering = ['-post_date']  # First, the newest
  
  # def get_queryset(self):
  #   candidates = Candidate.objects.all()
  #   query = self.request.GET.get("q")
  #   if query:
  #     candidates = Candidate.objects.filter(
  #       Q(name__icontains=query) |
  #       Q(lastname__icontains=query) |
  #       Q(type__icontains=query) |
  #       Q(party__icontains=query)
  #     )
    
  #   return candidates
    # return super().get_queryset()  

  # def get_ordering(self):
  #     ordering = self.request.GET.get('ordering', '-timeline_id')
  #     # validate ordering here
  #     return ordering
  # def get_queryset(self):
  #   filter_val = self.request.GET.get('filter', 'give-default-value')
  #   order = self.request.GET.get('orderby', 'give-default-value')
  #   new_context = Candidate.objects.filter(state=filter_val,).order_by(order)
  #   return new_context

  # def get_context_data(self, **kwargs):
  #   context = super(TableListView, self).get_context_data(**kwargs)
  #   context['filter'] = self.request.GET.get('filter', 'give-default-value')
  #   context['orderby'] = self.request.GET.get('orderby', 'give-default-value')
  #   return context


#
# Views
#
def home(request):
  """Renders the home page"""

  campaigns_tuple = db_util.get_all_campaigns()
  candidates_tuple = db_util.get_all_candidates()
  candidates_docs = db_util.get_all_documents()
  candidates_smas = db_util.get_all_social_media_accounts()
  context = {
            "campaigns": campaigns_tuple, 
            "candidates": candidates_tuple,
            "docs": candidates_docs,
            "smas": candidates_smas,
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
  data = {
    'form': CustomUserCreationForm()
  }

  if request.method == 'POST':
    register_form = CustomUserCreationForm(request.POST)
    if register_form.is_valid():
      register_form.save()
      
      # authenticate the user and redirect him to the beginning
      username = register_form.cleaned_data['username']
      password = register_form.cleaned_data['password1']
      user = authenticate(username=username, password=password)
      dj_login(request, user)
      print('REDIRECT!')
      return redirect(to='StudyCasesManage')

  return render(request, "registration/register.html", data)

