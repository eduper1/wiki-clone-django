from django import forms


class New(forms.Form):
    title = forms.CharField(label="Title of your entry",
                            min_length=2, max_length=30, widget=forms.TextInput())
    content = forms.CharField(
        label="Entry content", min_length=10, max_length=1200, widget=forms.Textarea())
    edit = forms.BooleanField(
        initial=False, widget=forms.HiddenInput, required=False)
