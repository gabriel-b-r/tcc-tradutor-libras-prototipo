import pickle
import cv2
import mediapipe as mp
import numpy as np

#Carregando o modelo.
dicio_modelo = pickle.load(open('./modelo.p', 'rb'))
modelo = dicio_modelo['modelo']

#Captura de câmera.
captura = cv2.VideoCapture(0)

#Configurações do MediaPipe.
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

maos = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

#Dicionário de classes.
dicio_rotulos = {0: '4', 1: '5', 2: '6', 3: '7', 4: 'A', 5: 'B', 6: 'C', 7: 'D',
                 8: 'E', 9: 'F', 10: 'G', 11: 'I', 12: 'L', 13: 'O', 14: 'P', 15: 'R',
                 16: 'S', 17: 'T', 18: 'U', 19: 'V', 20: 'Y'}

#Loop principal para processar os frames da câmera
while True:

    dados_aux = []
    x_ = []
    y_ = []

    ret, frame = captura.read()

    altura, largura, _ = frame.shape

#Processamento da imagem.
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultados = maos.process(frame_rgb)

#Extração e desenho dos parâmetros
    if resultados.multi_hand_landmarks:
        pontos_referencia = resultados.multi_hand_landmarks[0]
        for pontos_referencia in resultados.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  #imagem para ilustração
                pontos_referencia,  #modelo de saída
                mp_hands.HAND_CONNECTIONS,  #Conexão dos pontos de referência
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

#Normatização das coordenadas.
        for pontos_referencia in resultados.multi_hand_landmarks:
            for i in range(len(pontos_referencia.landmark)):
                x = pontos_referencia.landmark[i].x
                y = pontos_referencia.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(pontos_referencia.landmark)):
                x = pontos_referencia.landmark[i].x
                y = pontos_referencia.landmark[i].y
                dados_aux.append(x - min(x_))
                dados_aux.append(y - min(y_))

#Definição da região da mão.
        x1 = int(min(x_) * largura) - 10
        y1 = int(min(y_) * altura) - 10

        x2 = int(max(x_) * largura) - 10
        y2 = int(max(y_) * altura) - 10

#Predisão do modelo.
        predicao = modelo.predict([np.asarray(dados_aux)])

        caractere_predito = dicio_rotulos[int(predicao[0])]

        cv2.putText(frame, caractere_predito, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3,
                    (255, 255, 255), 3, cv2.LINE_AA)

#Exibição dos resultados.
    cv2.imshow('frame', frame)
    cv2.waitKey(1)

#Finalização da execução
captura.release()
cv2.destroyAllWindows()