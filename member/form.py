from django import forms
from .models import event_member

class MemberForm(forms.ModelForm):
    class Meta:
        model = event_member
        fields = ['mem_id', 'mem_name', 'mem_hp', 'mem_email', 'mem_Event']
        widgets = {
            'mem_id': forms.TextInput(attrs={'class': 'form-control'}),
            'mem_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mem_hp': forms.TextInput(attrs={'class': 'form-control'}),
            'mem_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }