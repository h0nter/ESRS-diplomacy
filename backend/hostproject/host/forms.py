from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(required=True, max_length=30)

    # override the clean_password2 method to skip the password verification step, in the production we need to commit it
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")  # confirmation password, provided at here to identify this one is unavailable

        return password1
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')



class inviteForm(forms.Form):
    room_ID = forms.IntegerField()