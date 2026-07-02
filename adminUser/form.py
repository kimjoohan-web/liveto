from django import forms
from .models import AdminMember


class AdminMemberForm(forms.ModelForm):
    class Meta:
        model = AdminMember
        fields = ['admin_id', 'password', 'admin_name', 'admin_email', 'admin_phone', 'admin_is_superuser']
        widgets = {
            'admin_id': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'admin_name': forms.TextInput(attrs={'class': 'form-control'}),
            'admin_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'admin_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'admin_is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }