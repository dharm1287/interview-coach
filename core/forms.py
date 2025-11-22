from django import forms

class StartSessionForm(forms.Form):
    role = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    level = forms.ChoiceField(choices=[('Junior','Junior'),('Mid','Mid'),('Senior','Senior')])

class AnswerForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea(attrs={'rows':6, 'cols':60}), required=False)
    audio = forms.FileField(required=False)
