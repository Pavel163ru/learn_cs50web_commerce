from django import forms

class ListingForm(forms.Form):
    title = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description'}))
    startbid = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'starting bid'}))
    image = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'image URL'}))
    category = forms.CharField(max_length=64, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'category'}))
