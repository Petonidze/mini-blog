# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login as auth_login

from django.template import RequestContext

from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView, LogoutView

from django.core.paginator import Paginator #pagination
from django.urls import reverse_lazy

from django.http import HttpRequest

from django.conf import settings

from .models import CustomUser, notes
from .forms import RegisterUserForm, PickyAuthenticationForm, NoteCreateForm, NoteDeleteForm, NoteUpdateForm
# Create your views here.

class BaseView():
    user = None
    blog_user = None

    def dispatch(self, request, *args, **kwargs):
        self.object = super(BaseView, self).get_object()
        if not request.user.is_anonymous and self.object.author == request.user:
           self.blog_user = request.user
           return super(BaseView, self).dispatch(request, *args, **kwargs)
        elif request.user.is_anonymous:
            return render(request, 'application/login_error.html')
        elif self.object.author != request.user:
            print(request)
            return render(request, 'application/not_author_error.html')
       

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context['context_user'] = self.user
        context['blog_user'] = self.blog_user
        context['request'] = self.request
        return context

def index(request):
    user_display = CustomUser.objects.all()
    notes_display = notes.objects.all().order_by("-date")

    notes_paginator = Paginator(notes_display, 20) # Show 20 articles per page.

    page_number = request.GET.get('page', 1)
    page_obj = notes_paginator.get_page(page_number)

    is_paginated = page_obj.has_other_pages()

    if page_obj.has_previous():
        prev_url = '?page={}'.format(page_obj.previous_page_number())
    else:
        prev_url = ''
    
    if page_obj.has_next():
        next_url = '?page={}'.format(page_obj.next_page_number())
    else:
        next_url = ''
    
    context = {
        'Users': user_display,
        'notes': page_obj,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    return render(request, 'application/homePage.html', context = context)

class RegisterUser(CreateView):
    model = CustomUser
    form_class = RegisterUserForm
    template_name = "application/user_register.html"
    def form_valid(self, form):
        
        form.save()
        return redirect("/")
        
    def get_success_url(self):
        if self.success_url:
            return self.success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")


class AuthUser(LoginView):
    form_class = PickyAuthenticationForm
    template_name = 'application/login.html'
    
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)
    

class NoteCreate(CreateView, FormView):
    model = notes
    form_class = NoteCreateForm
    template_name = "application/note_form.html"

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
            form.save()
            return redirect("/")
        else: 
            return render(request, 'application/login_error.html')

    def success_url(self):
        return redirect("/")

class NoteUpdate(BaseView, UpdateView):
    model = notes
    form_class = NoteUpdateForm
    template_name = "application/note_update_form.html"

    def form_valid(self, form):
        form.save()
        return redirect("/")

    def get_success_url(self):
        return redirect("/")


class NoteDelete(BaseView,DeleteView):
    model = notes
    success_url = reverse_lazy('index')
    form_class = NoteDeleteForm
    template_name = 'application/note_delete_form.html'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object.delete()
        return HttpResponseRedirect(self.success_url)
    
    def get_success_url(self):
        if self.success_url:
            return self.success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")

#logout
class LogOutUser(LogoutView):
    template_name = 'application/logout.html'

