from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from users.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'country', 'password1', 'password2')


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label='email', max_length=254, required=False)

    def clean_email(self):
        cleaned_data = self.cleaned_data['email']
        try:
            user = User.objects.get(email=cleaned_data)
        except User.DoesNotExist:
            raise forms.ValidationError("Пользователь с указанным email не существует")
        return cleaned_data


class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('phone', 'country', 'profile_img')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()