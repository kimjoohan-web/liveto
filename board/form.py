from django import forms
from .models import board

class boardForm(forms.ModelForm):
    class Meta:
        model = board
        fields = ['car_name', 'car_order', 'car_field', 'car_year', 'car_day', 'car_date', 'car_url', 'car_size_h', 'car_size_w', 'car_check', 'car_readnum', 'car_content', 'car_image', 'car_choo', 'car_soonwe']
        widgets = {
            'car_name': forms.TextInput(attrs={'class': 'form-control'}),
            'car_order': forms.TextInput(attrs={'class': 'form-control'}),
            'car_field': forms.TextInput(attrs={'class': 'form-control'}),
            'car_year': forms.TextInput(attrs={'class': 'form-control'}),
            'car_day': forms.TextInput(attrs={'class': 'form-control'}),
            'car_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'car_url': forms.TextInput(attrs={'class': 'form-control'}),
            'car_size_h': forms.NumberInput(attrs={'class': 'form-control'}),
            'car_size_w': forms.NumberInput(attrs={'class': 'form-control'}),   
            'car_check': forms.TextInput(attrs={'class': 'form-control'}),
            'car_readnum': forms.NumberInput(attrs={'class': 'form-control'}),  
            'car_content': forms.Textarea(attrs={'class': 'form-control'}),
            'car_image': forms.TextInput(attrs={'class': 'form-control'}),
            'car_choo': forms.NumberInput(attrs={'class': 'form-control'}),
            'car_soonwe': forms.NumberInput(attrs={'class': 'form-control'}),
        }

