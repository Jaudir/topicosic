import pandas
import matplotlib.pyplot as plt
import scipy.stats as stats


#dados obtidos em: http://portal.inep.gov.br/web/guest/microdados
#dados referentes ao ENAD 2017
jaudir = 'C:\\Users\\jonas\\Desktop\\Enad\\Enad.txt'
enade2017=pandas.read_csv(jaudir, sep=';',dtype={"DS_VT_ESC_OFG": str,  "DS_VT_ESC_OFG": str, 
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

tabela = pandas.DataFrame(enade2017, columns=['NT_GER', 'CO_GRUPO', 'CO_IES', 'CO_UF_CURSO', 'TP_SEXO', 'ANO_IN_GRAD'])

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
alunos_exemplares = tabela.loc[tabela['NT_GER']>60]
print(alunos_exemplares)


#alunos com notas menores que 100
#alunos_exemplares = tabela.loc[tabela['NT_GER']<100]
#print(alunos_exemplares)


#seleciona apenas os alunos de computação
ccomp = alunos_exemplares[alunos_exemplares['CO_GRUPO']==4004]
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

#dos alunos do IFNMG do sexo M
ifMccomp = ifccomp[ifccomp['TP_SEXO']=='M']
ifMccomp.describe()
print(ifMccomp)


print(ifccomp)

#somente as notas de quem respondeu a questão sobre a renda
ufccomp=ufccomp.loc[(ufccomp['TP_SEXO'].notnull())]
ufccomp.NT_GER.describe()

ufccomp.TP_SEXO.head(10)
ufccomp['TP_SEXO'] = ufccomp['TP_SEXO'].map({'F': 1, 'M': 2})
ufccomp.TP_SEXO.head(10)


#visualmente
plt.scatter( ufccomp.NT_GER, ufccomp.TP_SEXO)
plt.ylabel('Sexo')
plt.xlabel('Nota do curso de C. da Comp.')
plt.show()


#Como verificar se a média dos alunos referente a cada sexo é realmente diferentes
sexo = pandas.DataFrame(ccomp, columns=['NT_GER', 'TP_SEXO'])
sexo.boxplot(by='TP_SEXO')

#referente apenas de Minas Gerais
sexo = pandas.DataFrame(ufccomp, columns=['NT_GER', 'TP_SEXO'])
sexo.boxplot(by='TP_SEXO')


#nota geral agrupada pelo sexo
print(tabela['NT_GER'].groupby(tabela['TP_SEXO']).describe())


print(stats.shapiro(sexo.NT_GER.loc[ufccomp.TP_SEXO ==1]))
print(stats.shapiro(sexo.NT_GER.loc[ufccomp.TP_SEXO ==2]))

sexo.NT_GER.loc[sexo.TP_SEXO ==2].hist()

# teste não paramétrico são métodos que não assumem uma distribuição específica para os dados.
stat, p = stats.mannwhitneyu(sexo.NT_GER.loc[sexo.TP_SEXO ==1], sexo.NT_GER.loc[sexo.TP_SEXO ==2])

print('Mann-Whitney: Estatisticas=%.3f, p=%.3f' % (stat, p))

alpha = 0.05
if p > alpha:
	print('Mesma distribuição')
else:
	print('Distribução diferente')
    
    
stat, p = stats.kruskal(sexo.NT_GER.loc[sexo.TP_SEXO ==1], sexo.NT_GER.loc[sexo.TP_SEXO ==2])
print('Kruskal-Wallis: Estatisticas=%.3f, p=%.3f' % (stat, p))

if p > alpha:
	print('Mesma distribuição')
else:
	print('Distribução diferente')
    
#anova
stat, p = stats.f_oneway(sexo.NT_GER.loc[sexo.TP_SEXO ==1], sexo.NT_GER.loc[sexo.TP_SEXO ==2])
print('Anova: Estatisticas=%.3f, p=%.3f' % (stat, p))
if p > alpha:
	print('Mesma distribuição')
else:
	print('Distribução diferente')