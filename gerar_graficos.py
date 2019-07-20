#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# script que gera os gráficos
def gerar_graficos(lista_repeticoes_abs, lista_repeticoes_perc): 
    """
    input: listas de contagem de repeticões, absolutas e percentuais
    output: fotos, em .png, dos gráficos de contagem absoluta e percentual (TO_DO)  
    """
    
    # As fotos não são retornadas, apenas salvas na pasta atual.
    
    # aqui organizam-se as séries contidas nas listas em ordem decrescente (maiores repitições aparecem no topo). 
    for i in range(0,len(lista_repeticoes_abs)): #como ambas listas possuem o mesmo tamanho, tanto faz qual usar pra ter o tamanho
        lista_repeticoes_abs[i]=lista_repeticoes_abs[i].sort_values(ascending=False)   # organizando
        lista_repeticoes_perc[i]=lista_repeticoes_perc[i].sort_values(ascending=False) # organizando
        
    # fazer uma copia das listas das series pra podermos gerar os graficos
    copia_lista_rep_abs = lista_repeticoes_abs.copy()
    copia_lista_rep_perc = lista_repeticoes_perc.copy()       
    
    # aqui iremos normalizar os dados 
    for i in range (0,len(lista_repeticoes_abs)):
        soma = copia_lista_rep_abs[i].astype(float).values.sum() # para cada série precisamos da soma total
        for j in range(0,len(lista_repeticoes_abs[i])):
            copia_lista_rep_abs[i][j]=100*(copia_lista_rep_abs[i][j]/soma) # cada valor da série é dividido pelo valor total
            copia_lista_rep_perc[i][j]=100*(copia_lista_rep_perc[i][j]/soma) # cada valor da série é dividido pelo valor total
    # aqui iremos plotar os gráficos
    import matplotlib.pyplot as plt

    #plotagem do gráfico de diferenças absolutas
    for i in range (0,len(lista_repeticoes_abs)):
        plt.figure(i)

        plt.xticks(rotation = 90) # fazer os elementos do eixo das abcissas rotacionarem 90º, evitando poluição visual.
        plt.ylim([0,100])

        plt.title('grafico de risco')
        plt.ylabel('%')
        plt.xlabel('elemento repetido')
        plt.bar(copia_lista_rep_abs[i].index,lista_repeticoes_abs[i].values)#plotagem do gráfico de diferenças percentuais
        plt.savefig(str(i)+'abs.png')    

