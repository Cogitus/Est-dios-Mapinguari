from django import forms
from .models import Dados

class arquivo(forms.Form):
	nome = forms.CharField(max_length = 100)
	arquivo = forms.FileField()

class dadosForm(forms.ModelForm):
	class Meta:
		model = Dados
		fields = ('data',)
		