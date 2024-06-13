from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from ckeditor.widgets import CKEditorWidget
from django.utils.safestring import mark_safe

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = AdminLogin
        fields = ('username', 'email', 'ph_no', 'password')

    def save(self, commit=True):
        # Save the provided password in hashed format

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user

class CoursesForm(forms.Form):
    Title = forms.CharField(label= "Course Name", max_length=100)
    Description = forms.CharField(widget=CKEditorWidget())
    Technologies = forms.CharField(label="Topics", max_length=150)
    Images = forms.ImageField(label="Banner Images")
    status = forms.BooleanField()

class PartnersLogoForm(forms.ModelForm):
    class Meta:
        model = partners_logo
        fields = ['name', 'logo']

class ImagePreviewWidget(forms.ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value and hasattr(value, 'url'):
            image_html = f'<img id="{name}" src="{value.url}" alt="Course Banner" style="max-width: 50px; max-height: 50px;">'
            script = f'<script>document.getElementById("{name}").addEventListener("change", function() {{ document.getElementById("{name}_image_preview").src = window.URL.createObjectURL(this.files[0]); }});</script>'
            return mark_safe(f'{image_html}<br>{html}{script}')
        return html

class UpdataCourseForm(forms.Form):
    Title = forms.CharField(label="Course Name", max_length=100)
    Description = forms.CharField(widget=CKEditorWidget())
    Technologies = forms.CharField(label="Topics", max_length=150)
    Images = forms.ImageField(label="Banner Images", widget=ImagePreviewWidget)
    status = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super(UpdataCourseForm, self).__init__(*args, **kwargs)
        if instance:
            self.fields['Title'].initial = instance.Title
            self.fields['Description'].initial = instance.Description
            self.fields['Technologies'].initial = instance.Technologies
            self.fields['Images'].initial = instance.Images
            self.fields['status'].initial = instance.status

class FaqForm(forms.Form):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']