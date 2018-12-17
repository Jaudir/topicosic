import pandas
import matplotlib.pyplot as plt

enade2017=pandas.read_csv("MICRODADOS_ENADE_2017.txt", sep=';',dtype={"DS_VT_ESC_OFG": str, 
                                                                               'DS_VT_ESC_OCE':str,
                                                                              'DS_VT_ACE_OCE':str,
                                                                              'NT_GER':str,
                                                                              'NT_FG':str,
                                                                              'NT_OBJ_FG':str,
                                                                              'NT_DIS_FG':str,
                                                                              'NT_CE':str,
                                                                              'NT_OBJ_CE':str,
                                                                              'NT_DIS_CE':str})
enade2017.columns[0:10]

tabela = pandas.DataFrame(enade2017, columns=['NT_GER', 'CO_GRUPO', 'QE_I08', 'CO_IES', 'QE_I05'])
print(tabela.head(10))

##limpeza dos dados

#substitui vírgula por ponto
tabela['NT_GER'] = tabela['NT_GER'].str.replace(',', '.')
print (tabela['NT_GER'])

#observe os NaN (not a number)


'''No arquivo 'Dicionário de variáveis dos Microdados do Enade_Edição 2017' descreve que:
o codigo 222 no campo TP_PR_GER significa ausente 
556 e 888 são participações desconsideradas.
Portanto, algumas notas podem ser desconsideradas dependendo do seu objetivo, 
e aqui, será de calcular a média daqueles que fizeram a prova.
'''
tabela=tabela.loc[(tabela['NT_GER'].notnull())]
#print(tabela['NT_GER'])
#converte de str para float
tabela['NT_GER'] = pandas.to_numeric(tabela['NT_GER'])
print(tabela['NT_GER'])
print(tabela['NT_GER'].mean())



print(tabela['NT_GER'].describe())


print(tabela.loc[tabela['NT_GER'] > 96])



#outros comandos
print('indice da primeira maior nota: ', tabela['NT_GER'].idxmax())
print('Maior nota: ', tabela['NT_GER'][72257])
#print(tabela['NT_GER'].idxmax())

#Calcula a média de um curso especifico
#Código da área de enquadramento do curso no Enade == ciencia da computacao

ccomp = tabela[tabela['CO_GRUPO']==4004]

print(ccomp)

#do curso do IFNMG
ifccomp = ccomp[ccomp['CO_IES']==3188]
ifccomp.describe()

#somente as notas de quem respondeu a questão sobre a renda
ccomp=ccomp.loc[(ccomp['QE_I08'].notnull())]
ccomp.NT_GER.describe()

ccomp=ccomp.loc[(ccomp['QE_I05'].notnull())]
ccomp.NT_GER.describe()

ccomp.QE_I08.head(10)

ccomp['QE_I08'] = ccomp['QE_I08'].map({'A': 1, 'B': 2, 'C': 3, 'D': 4,'E': 5, 'F':6,'G':7})

ccomp.QE_I08.head(10)


import matplotlib.pyplot as plt
#visualmente
plt.scatter( ccomp.NT_GER, ccomp.QE_I08)
plt.ylabel('Faixa de renda')
plt.xlabel('Nota do curso de C. da Comp.')
plt.show()


ccomp.QE_I05 = ccomp['QE_I05'].map({'A': 1, 'B': 2, 'C': 3, 'D': 4,'E': 5, 'F':6})

ccomp.QE_I05.head(10)



#visualmente
plt.scatter( ccomp.NT_GER, ccomp.QE_I05)
plt.ylabel('Escolaridade da mãe')
plt.xlabel('Nota do curso de C. da Comp.')
plt.show()


escolaridade = ccomp.loc[ccomp.QE_I05 ==1]
escolaridade.NT_GER.describe()
