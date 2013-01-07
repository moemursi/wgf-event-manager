from django import forms

class RegistrationForm(forms.Form):
   username = forms.CharField(max_length=30)
   first_name = forms.CharField(max_length=30)
   last_name = forms.CharField(max_length=30)
   email = forms.EmailField()
   password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=100)
   is_player = forms.BooleanField(label="Check this box if you will be participating in a tournament", required=False)
   age = forms.IntegerField(min_value=1, max_value=150)
   is_ucsd = forms.BooleanField(label="Check this box if you are a UCSD student", required=False)
   
class LoginForm(forms.Form):
   username = forms.CharField(max_length=30)
   password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=100)