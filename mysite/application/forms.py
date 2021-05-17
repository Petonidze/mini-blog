from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser, notes

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

#register
class RegisterUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'biography', 'birth_date']

#auth
class PickyAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, CustomUser):
        if not CustomUser.is_active:
            raise ValidationError(
                _("This account is inactive."),
                code='inactive',
            )

class NoteCreateForm(forms.ModelForm):

    class Meta:
        model = notes
        fields = ['date', 'title', 'text']
    
    #def init(self, *args, **kwargs):
    #    super(NoteCreateForm, self).init(*args, **kwargs)
    #    self.instance.author = self.request.user
     #         #  CustomUser.object.filter(email = self.request.user)[0]



class NoteUpdateForm(forms.ModelForm):
   # title = forms.CharField(max_length = 255)
    #text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = notes
        fields = ['title', 'text']

class NoteDeleteForm(forms.ModelForm):
    class Meta:
        model = notes
        fields = ['date', 'title', 'text','author']
