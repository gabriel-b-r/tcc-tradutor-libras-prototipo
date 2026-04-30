import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

#carregando os dados.
dicio_dados = pickle.load(open('./dados.pickle', 'rb'))
dados = np.asarray(dicio_dados['dados'])
rotulos = np.asarray(dicio_dados['rotulos'])

#Separação dos dados entre treino e teste.
x_treino, x_teste, y_treino, y_teste = train_test_split(dados, rotulos,
                                                        test_size=0.2, shuffle=True, stratify=rotulos)

#Criação do modelo.
modelo = RandomForestClassifier()

#Treinamento do modelo.
modelo.fit(x_treino, y_treino)

#Predição e avaliação do modelo.
y_predicao = modelo.predict(x_teste)
pontuacao = accuracy_score(y_predicao, y_teste)

#Resultados.
print(f'{pontuacao * 100}% das amostras foram classificadas corretamente!')

#Salvando o modelo.
f = open('modelo.p', 'wb')
pickle.dump({'modelo': modelo}, f)
f.close()