from django import forms
from django.contrib.auth.models import Group
from custom_auth.models import User
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["titulo", "descripcion", "approver", "path"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        approvers_group = Group.objects.get(name='Approvers')
        self.fields['approver'].queryset = User.objects.filter(groups=approvers_group)


class ApproveDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["status"]
