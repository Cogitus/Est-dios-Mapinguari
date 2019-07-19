from django import forms
from .models import Dados

class dadosForm(forms.ModelForm):
	class Meta:
		model = Dados
		filds=('DataFrame')
class arquivo(forms.Form):
	nome = forms.CharField(max_length = 100)
	arquivo = forms.FileField()


		