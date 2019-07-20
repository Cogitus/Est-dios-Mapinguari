from django.conf import settings
from django.db import models
import pandas as pd
from django import forms

class Session(models.Model):
    user = models.CharField(max_length=20, default='')
    password = models.CharField(max_length=20, default='')

class Dados(models.Model):
	data = models.FileField(default='')

class Retorno(models.Model):
	nome = models.CharField(max_length=500, default='')
	mapaRisco = models.FileField(default='')
	mapaFreq = models.FileField(default='')