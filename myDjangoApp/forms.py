from django import forms


class SignInForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'username', 'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', 'placeholder': 'Password'}))
    # username = forms.IntegerField()
    # password = forms.IntegerField()


class SignUpForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'username', 'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'password','id':'new-password', 'class': 'form-control', 'placeholder': 'Password'}))
    password_comfirm = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'password','id':'confirm-password','class': 'form-control', 'placeholder': 'Confirm Password'}))
