from django.shortcuts import render


def home(request):
  """Renders the home page"""

  return render(request, "home.html")


def configurator(request):
  """Renders the request page"""

  return render(request, "configurator.html")
