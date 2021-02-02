from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class Createuserform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(Createuserform, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class staffForm(ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(staffForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class deptForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        widgets = {
            'programme': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(deptForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class progForm(ModelForm):
    class Meta:
        model = Programme
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(progForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class FacultyForm(ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'
        widgets = {
            'department': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(FacultyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class LecturerForm(ModelForm):
    class Meta:
        model = Lecturer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LecturerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class usersForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = super(UserCreationForm, self).clean_password2()
    #     if bool(password1) ^ bool(password2):
    #         raise forms.ValidationError("Fill out both fields")
    #     return password2
