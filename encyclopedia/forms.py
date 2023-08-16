from django import forms

class EditEntryForm(forms.Form):
    edit_contents = forms.CharField(widget=forms.Textarea)