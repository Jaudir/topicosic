import pandas
import matplotlib.pyplot as plt

#dados obtidos em: http://portal.inep.gov.br/web/guest/microdados
#dados referentes ao ENAD 2017

enade2017=pandas.read_csv("Enade.txt" sep=';',dtype={"DS_VT_ESC_OFG": str, 
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
#CO_UF_CURSO -> Código da UF de funcionamento do curso 31 = MG
#TP_SEXO -> tipo do sexo: M - Masculino, F - Feminino

tabela = pandas.DataFrame(enade2017, columns=['NT_GER', 'CO_GRUPO', 'QE_I08', 'CO_IES', 'CO_UF_CURSO', 'TP_SEXO'])
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

#alunos com notas maiores que 60
alunos_exemplares = tabela.loc[tabela['NT_GER'] > 60]
print(alunos_exemplares)

ccomp = alunos_exemplares[alunos_exemplares['CO_GRUPO']==4004]
#mostra todos os alunos de ciência da computação com nota maior que 60
print(ccomp)

# seleciona alunos Minas Gerais
ufccomp = ccomp[ccomp['CO_UF_CURSO']==31]
ufccomp.describe()

print(ufccomp)

#dos alunos do IFNMG
ifccomp = ccomp[ccomp['CO_IES']==3188]
ifccomp.describe()
print(ifccomp)

#dos alunos do IFNMG do sexo F
ifFccomp = ifccomp[ifccomp['TP_SEXO']=='F']
ifFccomp.describe()
print(ifFccomp)

#somente as notas de quem respondeu a questão sobre a renda
ifFccomp=ifFccomp.loc[(ifFccomp['QE_I08'].notnull())]
ifFccomp.NT_GER.describe()

ifFccomp.QE_I08.head(10)
ifFccomp['QE_I08'] = ifFccomp['QE_I08'].map({'A': 1, 'B': 2, 'C': 3, 'D': 4,'E': 5, 'F':6,'G':7})
ifFccomp.QE_I08.head(10)


#visualmente
plt.scatter( ifFccomp.NT_GER, ifFccomp.QE_I08)
plt.ylabel('Faixa de renda')
plt.xlabel('Nota do curso de C. da Comp.')
plt.show()

#dos alunos do IFNMG do sexo M
ifMccomp = ifccomp[ifccomp['TP_SEXO']=='M']
ifMccomp.describe()
print(ifMccomp)

#somente as notas de quem respondeu a questão sobre a renda
ifMccomp=ifMccomp.loc[(ifMccomp['QE_I08'].notnull())]
ifMccomp.NT_GER.describe()

ifMccomp.QE_I08.head(10)
ifMccomp['QE_I08'] = ifMccomp['QE_I08'].map({'A': 1, 'B': 2, 'C': 3, 'D': 4,'E': 5, 'F':6,'G':7})
ifMccomp.QE_I08.head(10)


#visualmente
plt.scatter( ifMccomp.NT_GER, ifMccomp.QE_I08)
plt.ylabel('Faixa de renda')
plt.xlabel('Nota do curso de C. da Comp.')
plt.show()