#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 09:57:56 2018

@author: magoj
"""

import numpy as np
import skfuzzy as fuzz
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

def p_gauss(x,info):
    """ Processo para fuzzificação dos valores
     Distribuição normal: Tende a zero para valores muito
     maiores ou muito menores do que a média. """
    centro = info[0]
    sigma = info[1]
    return fuzz.membership.gaussmf(x,centro,sigma)

def p_singleton(classe, classe_teste):
    hash_t = {0: 'setosa',1:'versicolor',2:'virginica'}
    if classe == hash_t[classe_teste]:
        return 1
    else:
        return 0

def fuzzificador(elemento):
    """ Função de fuzzificação
    considerando os valores dados pela Sckilearn 
    Temos que:
    elemento = valor a ser fuzzificado"""

    info = {"sepal length (cm)": (5.84,0.8),"sepal width (cm)" : (3.05,0.43),"petal length (cm)": (3.76,1.76),"petal width (cm)" : (1.20,0.76)}
    resposta = np.zeros(4)
    for dim in range(0,4):
        dim_info = list(info.keys())[dim] 
        resposta[dim] = p_gauss(elemento[dim],info[dim_info])/elemento[dim]
    return resposta

def desfuzzificador_max(elemento,classes,pos):
    valor_maximo =  np.mean(elemento[list(classes)[0]][pos])
    for classe in classes:
        x = np.mean(elemento[classe][pos])
        if (x >= valor_maximo):
            valor_maximo = x
            resp = classe
    return resp



def fuzzy(X,ini,fim):
    resposta = {}
    for classe in X.target_names:
        resposta[classe] = np.zeros((fim-ini,4))
        for e in range(ini,fim): # e = elemento
            resposta[classe][e] = fuzzificador(X.data[e])
    
    resposta_final = []
    for e in range(ini,fim): # e = elemento
        resposta_final.append(desfuzzificador_max(resposta,X.target_names,e))
    return resposta,resposta_final

data = load_iris()
x,cc = fuzzy(data,0,10)

