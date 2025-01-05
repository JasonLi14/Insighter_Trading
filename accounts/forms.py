from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.widgets import NumberInput

# For creating user
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class rangeInputWidget(forms.MultiWidget):
    def __init__(self, attrs={"step": 0.25, "min": -5, "max": 5}):
        widgets = [
            forms.NumberInput(attrs={"id": "prediction_number", "step": 0.01}),
            forms.NumberInput(attrs={"id": "prediction_slider",
                                     "type": "range", 
                                     "step": attrs["step"], 
                                     "min": attrs["min"], 
                                     "max": attrs["max"],
                                     "class": "slider"})
        ]
        super().__init__(widgets, attrs={"required": True})

    def decompress(self, value):
        if isinstance(value, float):
            return [value, value]
        return [0, 0]

    def value_from_datadict(self, data, files, name):
        range_input, text_input = super().value_from_datadict(data, files, name)
        return text_input
    
    def subwidgets(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        return context['widget']['subwidgets']


class predictionForm(forms.Form):
    class Meta:
        fields = ("change")

    # Note: All the other data will be automatically collected
    def __init__(self, attrs={"step": 0.25, "min": -5, "max": 5}, *args, **kwargs):  # Allow other attributes
        super().__init__(*args, **kwargs)
        self.fields['change'] = forms.FloatField(widget=rangeInputWidget(attrs=attrs))
        

class searchForm(forms.Form):
    prompt = forms.CharField(label='', 
                             max_length=100, 
                             widget=forms.TextInput(
                                attrs={"class": "search_input", "name": "search", "placeholder": "TSLA"}),)
