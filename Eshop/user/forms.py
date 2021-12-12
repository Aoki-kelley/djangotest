from django import forms
from captcha.fields import CaptchaField


class UserLog(forms.Form):
    username = forms.fields.CharField(max_length=32, required=True)
    password = forms.fields.CharField(widget=forms.PasswordInput(), required=True)
    captcha = CaptchaField()


class UserReg(forms.Form):
    username = forms.fields.CharField(max_length=32, required=True)
    password = forms.fields.CharField(widget=forms.PasswordInput(), required=True)
    p_again = forms.fields.CharField(widget=forms.PasswordInput(), required=True)
    email = forms.fields.EmailField(required=True)
    captcha = CaptchaField(required=True)


class CodeProve(forms.Form):
    code = forms.fields.CharField(max_length=32, required=True)


class ResetName(forms.Form):
    new_name = forms.fields.CharField(max_length=32, required=True)
    password = forms.fields.CharField(widget=forms.PasswordInput(), required=True)


class PasswordChange(forms.Form):
    new_password = forms.fields.CharField(widget=forms.PasswordInput(), required=True)
    p_again = forms.fields.CharField(widget=forms.PasswordInput(), required=True)
    code = forms.fields.CharField(max_length=32, required=True)


class ImageChange(forms.Form):
    image = forms.fields.ImageField(required=True)


class AddMoney(forms.Form):
    money = forms.fields.FloatField(required=True, max_value=10000, min_value=10)


class ForgetPwd(forms.Form):
    username = forms.fields.CharField(max_length=32, required=True)
    email = forms.fields.EmailField(required=True)
