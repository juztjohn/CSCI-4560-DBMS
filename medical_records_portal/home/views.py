#from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def home(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def patient(request):
    template = loader.get_template('patient.html')
    return HttpResponse(template.render())

def appointments_view(request):
    template = loader.get_template('appointments.html')
    return HttpResponse(template.render())