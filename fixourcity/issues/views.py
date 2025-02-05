# issues/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')  # Ensure you have an index.html template
