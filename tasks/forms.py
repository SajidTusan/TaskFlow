from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ["title", "description", "category", "priority", "due_date"]

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "What needs to be done?"}),
            "description": forms.Textarea(attrs={"placeholder": "Add details..."}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }


class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")

        if password:
            # Run the validators from AUTH_PASSWORD_VALIDATORS (length, common, numeric...).
            # Passing an unsaved user lets the "too similar to username/email" check work.
            candidate = User(
                username=cleaned_data.get("username", ""),
                email=cleaned_data.get("email", ""),
            )
            try:
                validate_password(password, candidate)
            except forms.ValidationError as error:
                self.add_error("password", error)

        return cleaned_data
