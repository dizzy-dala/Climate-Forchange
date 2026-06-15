from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, PDFResource, NewsArticle, WeatherAlert


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False, max_length=150)
    last_name = forms.CharField(required=False, max_length=150)
    phone = forms.CharField(required=False, max_length=20)
    city = forms.CharField(required=False, max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone', ''),
                city=self.cleaned_data.get('city', ''),
            )
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'city', 'receive_alerts']


class PDFResourceForm(forms.ModelForm):
    class Meta:
        model = PDFResource
        fields = ['title', 'file', 'description', 'active']


class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['title', 'content', 'active']


class WeatherAlertForm(forms.ModelForm):
    class Meta:
        model = WeatherAlert
        fields = ['alert_type', 'title', 'message', 'severity', 'expires_at', 'active']
