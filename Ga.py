# -*- coding: utf-8 -*-
"""
	Tópicos em IC
	Equipe:
		Jaudir Aguiar
		Jonas Diego
		Matheus Aguiar
"""

import numpy as np
import random as rand
import pylab as gr

qtObj = 4
qtInd = 40
qtGer = 500
pMax = 35
txMut = 0.2

def geraPopulacao():
	"""
	A populacao (Pop) de tamanho 'qtInd' é gerada no intervalo uniforme de (-3,4)
	sendo 'qtObj' o número de dimensões
	"""
	
	Pop = np.zeros((qtInd,qtObj))
	for l in range(qtInd):
		for c in range(qtObj):
			Pop[l,c] = np.random.uniform(-3,4)
	return Pop
	
def avaliar(X):
	"""
		A função avaliar é responsavel por retornar o valor do ponto na 
		função rastrigin. Sendo que realiza para toda população.
	"""
	
	qtLinhas = len(X)
	fit = np.zeros((qtLinhas,1))
	for l in range(qtLinhas):
		result = 0
		for j in range(0,4):
			result = result + X[l,j]*X[l,j]+10.0*np.cos(X[l,j]*2.0*np.pi)
		fit[l] = result+10*qtObj
	return fit
	
def selecao(X,fit):
	"""
	Seleciona através de um torneio (com competidores aleatórios)
	'qtPais' para ser os pais da proxima geração
	"""
	
	qtPais = qtInd
	pais = np.zeros((qtPais,qtObj))
	qt= 0
	while qt<qtPais:
		p1 = rand.randrange(0,(qtInd-1))
		p2 = rand.randrange(0,(qtInd-1))
		if fit[p1] < fit[p2]:
			pais[qt,:] = X[p1,:]
		else:
			pais[qt,:] = X[p2,:]
		qt = qt+1
	return pais

def cruzamento(pais):
	"""
		Realiza o cruzamento por cortes onde o ponto de corte é definido 
		por 'pCort', sendo este definido aleatoriamente.
	"""
	qtPais = len(pais)
	filhos = np.zeros((qtPais,qtObj))
	par = 0
	while par < qtPais:
		pCort = rand.randrange(2,(qtObj-1))
		filhos[par,0:pCort] = pais[par,0:pCort]
		filhos[par,pCort:qtObj] = pais[par+1,pCort:qtObj]
		filhos[par+1,0:pCort] = pais[par+1,0:pCort]
		filhos[par+1,pCort:qtObj] = pais[par,pCort:qtObj]
		par = par+2
	return filhos
	
def mutacao(X):
	"""
		A População recebida é mutada, ou seja, um gene é modificado aleatoriamente
		para o um valor uniforme. A quantidade de mutações são definidas por txMut.
	"""
	qtLinhas = len(X)
	for l in range(qtLinhas):
		if np.random.random() < txMut:
			x = np.random.randint(0,4)
			y = np.random.uniform(-3,4)
			X[l,x] = y
	return X
	
def main():
	"""
	É gerada uma população através da função 'geraPopulacao()'.
	Através da função 'avaliar()' é obtido os pontos da função rastrigin
	com estes pontos é feito a seleção dos melhores pais, estes que serão
	colocados para cruzar gerando filhosestes são mutados a fim de melhorare a proxima geração.
	Os filhos mutados são avaliados e minimizados a fim de achar o valormínimo da função.
	Sempre salavando o melgor de cada geração.
	"""
	Pop = geraPopulacao()
	g = 0
	melhores = np.zeros((qtGer,1))
	while g < qtGer:
		fit = avaliar(Pop)
		pais = selecao(Pop,fit)
		filhos = cruzamento(pais)
		filhos = mutacao(filhos)
		fitFilhos = avaliar(filhos)
		
		if min(fitFilhos) < min(fit):
			melhor = filhos[np.argmin(fitFilhos),:]
		else:
			melhor = Pop[np.argmin(fit),:]
		
		Pop[0,:] = melhor
		Pop[1:qtInd,:] = filhos[1:qtInd,:]
		melhores[g] = np.min(fit)
		g=g+1
	gr.plot(melhores)
	gr.show()
	return melhor,min(fit)
	
print(main())