# Modulos Básicos
import itertools
import numpy as np
import matplotlib.pyplot as plt
# Divisão do datasets
from sklearn.model_selection import train_test_split
# Base de dados
from sklearn.datasets import load_iris
# Arvores de decisao
from sklearn import tree
import graphviz
# Matriz de Confusao
from sklearn.metrics import confusion_matrix

def plot_tree(clf,iris):
    """
    Essa função imprime a Árvore de decisão.
    """
    dot_data = tree.export_graphviz(clf, out_file=None) 
    graph = graphviz.Source(dot_data) 
    graph.render("iris") 

    dot_data = tree.export_graphviz(clf, out_file=None, feature_names=iris.feature_names,class_names=iris.target_names, filled=True, rounded=True, special_characters=True)  
    graph = graphviz.Source(dot_data)  
    return graph 

def plot_confusion_matrix(cm, classes, normalize=False, title='Matriz de Confusão',cmap=plt.cm.Blues):
    """
    Essa função imprime a matriz de confusão
    A matriz pode ser nomarlizada atraves de `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
                 
    plt.tight_layout()
    plt.ylabel('Classe Verdadeira')
    plt.xlabel('Classe Obtida')

def MatrizConfusao(y_test, y_pred,class_names):
        # Matriz de confusao
        cnf_matrix = confusion_matrix(y_test, y_pred)
        np.set_printoptions(precision=2)
        # Plot non-normalized confusion matrix
        plt.figure()
        plot_confusion_matrix(cnf_matrix, classes=class_names,title='Matriz de confusão não normalizada')
        # Plot normalized confusion matrix
        plt.figure()
        plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True, title='Matriz de confusão normalizada')
        plt.show()

def DecisionTree(iris):
    """
    Essa função gera a Árvore de Decisão e realiza os testes
    """
    # Realizando a construção da arvore de decisão e classificando
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.20, train_size = 0.80, random_state=80)
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    return clf, y_test,y_pred,clf.score(X_test,y_test)

def main():
    iris = load_iris()
    class_names = iris.target_names
    clf,y_test,y_pred,score = DecisionTree(iris)
    print('Score: %f' %score)
    MatrizConfusao(y_test, y_pred,class_names)
    g = plot_tree(clf,iris)
    g.view()

main()