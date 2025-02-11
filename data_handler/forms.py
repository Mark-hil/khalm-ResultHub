from django import forms
from .models import UserData, TestResult
from django.forms import inlineformset_factory


class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ["name", "age", "sex", "user_class", "lab_serial"]


class TestResultForm(forms.ModelForm):
    class Meta:
        model = TestResult
        fields = ["test_name", "result"]
