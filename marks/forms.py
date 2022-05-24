from django import forms
class StudentForm(forms.Form):
     file = forms.FileField()