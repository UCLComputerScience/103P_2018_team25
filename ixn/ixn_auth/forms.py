from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class ClientSignUp(UserCreationForm):
    first_name = forms.CharField(
            required=False,
            max_length=30,
            help_text='First Name')
    last_name = forms.CharField(
            max_length=30,
            required=False,
            help_text='Surname')
    email = forms.EmailField(
            max_length=254,
            help_text='Email required for contact')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        username = cleaned_data['username']
        if(check_number(username)): # To prevent student / client conflicts
            raise forms.ValidationError('Username cannot be a number!')
        return cleaned_data

def check_number(username):
    try:
        float(username)
        return True
    except ValueError:
        return False
