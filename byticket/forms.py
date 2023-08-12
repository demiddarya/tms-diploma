from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(label="password", widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    email = forms.EmailField()
    password1 = forms.CharField(label="password1", widget=forms.PasswordInput)
    password2 = forms.CharField(label="password2", widget=forms.PasswordInput)
