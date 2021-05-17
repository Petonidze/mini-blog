from django.urls import re_path, include
from . import views
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import PasswordResetView


from .models import CustomUser, notes
from .views import RegisterUser, AuthUser, LogOutUser, NoteUpdate, NoteCreate, NoteDelete

urlpatterns= [

    re_path(r'^$', views.index, name = 'index'),

    re_path(r'^add-note/$', NoteCreate.as_view(), name = 'add_note'),
    re_path(r'^update-note/(?P<pk>\d+)/$', NoteUpdate.as_view(), name = 'update_note'),
    re_path(r'^delete-note/(?P<pk>\d+)/$', NoteDelete.as_view(), name = 'delete_note'),
    

    #listing a special page for the unique note
    re_path(r'^(?P<pk>\d+)/$', DetailView.as_view(model=notes, template_name ="application/note.html")),

    #register
    re_path(r'^register/$', RegisterUser.as_view(), name = 'register'),

    #auth
    re_path(r'^auth/$', AuthUser.as_view(template_name='application/login.html'), name = 'login'),

    #password reset
    re_path(r'^password-reset/$', PasswordResetView.as_view(template_name=''), name='password_reset' ),

    re_path(r'^logout/$', LogOutUser.as_view(), name = 'logout'),
    re_path(r'^contact/$', ListView.as_view(model=notes, template_name = "application/contact_us.html"), name="contact"),
]