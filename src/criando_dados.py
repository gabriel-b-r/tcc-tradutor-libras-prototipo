import os
import pickle
import mediapipe as mp
import cv2


#Configurando o MediaPipe.
mp_hands = mp.solutions.hands
maos = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

#Selecionando o diretório de dados e criando listas para armazenamento.
dir_dados = './dados'
dados = []
rotulos = []

#Criando um loop para percorrer todas as imagens e listas para guardar as coordenadas.
for dir_ in os.listdir(dir_dados):
    for img_path in os.listdir(os.path.join(dir_dados, dir_)):
        dados_aux = []

        x_ = []
        y_ = []

#Leitura e processamento de imagens.
        img = cv2.imread(os.path.join(dir_dados, dir_, img_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        resultados = maos.process(img_rgb)

#Extração dos pontos de referências.
        if resultados.multi_hand_landmarks:
            for referencias_mao in resultados.multi_hand_landmarks:
                for i in range(len(referencias_mao.landmark)):
                    x = referencias_mao.landmark[i].x
                    y = referencias_mao.landmark[i].y

                    x_.append(x)
                    y_.append(y)

#Normatização das coordenadas.
                for i in range(len(referencias_mao.landmark)):
                    x = referencias_mao.landmark[i].x
                    y = referencias_mao.landmark[i].y
                    dados_aux.append(x - min(x_))
                    dados_aux.append(y - min(y_))

#Armazenamento de dados.
            dados.append(dados_aux)
            rotulos.append(dir_)

#Salvando em dados em um arquivo.
f = open('dados.pickle', 'wb')
pickle.dump({'dados': dados, 'rotulos': rotulos}, f)
f.close()