from django import forms

class ParametersForm(forms.Form):
    petal_length = forms.DecimalField()
    petal_width = forms.DecimalField()
    sepal_length = forms.DecimalField()
    sepal_width = forms.DecimalField()