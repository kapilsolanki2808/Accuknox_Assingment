
from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=100)
    dob = forms.DateField()
    gender = forms.CharField(max_length=10)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.dob = self.cleaned_data['dob']
        user.gender = self.cleaned_data['gender']
        user.save()
        return user
