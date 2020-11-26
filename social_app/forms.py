from django import forms
from captcha.fields import CaptchaField


class captcha_class(forms.Form):
    captcha = CaptchaField(label='Verification Code')
