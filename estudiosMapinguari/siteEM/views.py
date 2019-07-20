import io
import pandas as pd
from django_pandas.io import read_frame
from .models import Session, Dados, Retorno
from django.conf import settings
from reportlab.pdfgen import canvas
from django.http import FileResponse
from django.shortcuts import render_to_response
from django.shortcuts import render, get_object_or_404
from django.core.files.storage import FileSystemStorage
posicao = [-1]
nome = ''
def analisar(request):
	pos = posicao
	tabDifAbs, tabDifPer, lisRepAbs, lisRepPerc = gera_tabelas(pos[0].data)
	return render(request, 'siteEM/analise.html', {'pos' : pos[0].data.name, 'tda' : tabDifAbs, 'tdp' : tabDifPer, 'lra' : lisRepAbs, 'lrp' : lisRepPerc})

def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        nome = myfile.name
        dt = Dados.objects.create(data = myfile);
        posicao[0] = Dados.objects.all()[len(Dados.objects.all()) - 1]
        return render(request, 'siteEM/inicial.html', {
            'uploaded_file_url': uploaded_file_url
        })

    return render(request, 'siteEM/inicial.html')

def gera_tabelas(uri):
    dados = pd.read_csv(uri) #lê a tabela (a primeira linha do arquivo csv JÁ VAI SER o cabeçalho)
    
    dados.dropna(inplace=True) #apaga as linhas com NaN
    dados.reset_index(drop=True, inplace=True) #ajeitando os índices
    
    qtdEmp = dados.shape[1] - 4 #número de colunas excluindo as 4 primeiras
    dados.iloc[:,4] = dados.iloc[:,4].astype(float) #convertemos pra float, pois essa coluna não estava sendo identificada (type = object) (é o preço de referência)
    
    lista_series_empresas = list(dados.columns.values[4:]) #A partir da quinta coluna ou quarto índice (começa em 0) temos as empresas e o preço de referência (primeiro termo)
    
    copia_lista_series_empresas = lista_series_empresas.copy() #copia para poder utilizar futuramente o método list.remove()

    #criando as tabelas de diferenças
    tabela_diff_abs_empresas = pd.DataFrame()
    tabela_diff_perc_empresas = pd.DataFrame()
    
    for nome_empresa in lista_series_empresas: #interando em cima dos nomes das empresas
        #remove o primeiro elemento da LISTA
        copia_lista_series_empresas.remove(nome_empresa)
        
        for nome_empresa2 in copia_lista_series_empresas:
            #gerando as colunas de diferenças absolutas
            coluna_abs = dados[nome_empresa] - dados[nome_empresa2]
            titulo_coluna_abs = f'{nome_empresa}_{nome_empresa2}'
            
            #gerando as colunas de diferenças relativas
            coluna_perc = 100*abs((dados[nome_empresa] - dados[nome_empresa2])/dados[nome_empresa])
            titulo_coluna_perc = f'{nome_empresa}_{nome_empresa2}'
            
            tabela_diff_abs_empresas[titulo_coluna_abs] = coluna_abs
            tabela_diff_perc_empresas[titulo_coluna_perc] = coluna_perc
            
    #gerando duas listas que recebem as séries oriundas das contagens de repetições (lista de série)
    lista_repeticoes_abs = list()
    lista_repeticoes_perc = list()
    
    #precisamos dos nomes das colunas do NOVO dataframe pra poder iterar sobre os dataframes tabela_diff_abs_empresas
    #e tabela_diff_perc_empresas
    colunas_dataframe_abs = list(tabela_diff_abs_empresas.columns.values) #nomes das colunas da tabela_diff_abs_empresas
    colunas_dataframe_perc = list(tabela_diff_perc_empresas.columns.values) #nomes das colunas da tabela_diff_perc_empresas
    
    #construindo as listas de contagens de repetições
    #ambos dataframes têm o mesmmo nome para as colunas, logo, iterando sobre qualquer dataframe dá no mesmo
    for titulo in colunas_dataframe_abs:
        # aqui geraremos as contagens das repetições que existem na coluna nomeada com 'titulo'
        # pro dataframe tabela_diff_perc_empresas e tabela_diff_abs_empresas.
        contagem_abs = tabela_diff_abs_empresas.groupby(tabela_diff_abs_empresas[titulo].map(lambda x: "%.2f" % x)).size()
        contagem_perc = tabela_diff_perc_empresas.groupby(tabela_diff_perc_empresas[titulo].map(lambda x: "%.2f" % x)).size()
        
        #adicionando as contagens nas suas respectivas listas de contagem
        lista_repeticoes_abs.append(contagem_abs)
        lista_repeticoes_perc.append(contagem_perc)
        

    return tabela_diff_abs_empresas, tabela_diff_perc_empresas, lista_repeticoes_abs, lista_repeticoes_perc 