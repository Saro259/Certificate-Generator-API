from django import forms

class CertificateForm(forms.Form):
    name = forms.CharField(max_length=255)
    course_name = forms.CharField(max_length=255)
    certificate_award_date = forms.DateField()