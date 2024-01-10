from typing import Any
from django.shortcuts import render, redirect
from . import forms
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

# Create your views here.
class UserLoginView(LoginView):
    template_name= 'register.html'
    # success_url = reverse_lazy('homepage' )
    def get_success_url(self):
        return reverse_lazy('homepage' )
    

    def form_valid(self, form):
        messages.success(self.request, 'login successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'login invalid')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["type"] = 'login'
        return context

    


# form base
def add_author(request):
    if request.method == 'POST':
        author_form = forms.AuthorForm(request.POST)
        if author_form.is_valid():
            author_form.save()
            return redirect('add_author')
    
    else:
        author_form = forms.AuthorForm()
    return render(request, 'add_author.html', {'form' : author_form})