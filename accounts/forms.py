from django import forms
from .models import Account, UserProfile

class RegistrationForm(forms.ModelForm): # the ModelForm creates a form based on a given model

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Enter Password",
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": 'Confirm Password'
    }))



    class Meta: #provide configurations for the form
        model = Account #create model based on this model's field
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Passwords do not match'
            )
        

class UserForm(forms.ModelForm):
    class Meta:
        model= Account
        fields = ['first_name', 'last_name', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



class UserProfileForm(forms.ModelForm):

    profile_picture = forms.ImageField(required=False, error_messages= {'invalid': ("Image files only")}, widget=forms.FileInput)
    class Meta:
        model= UserProfile
        fields = ['address', 'city', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

