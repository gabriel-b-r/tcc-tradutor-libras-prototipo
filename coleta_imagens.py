import os
import cv2

#Criando o diretório para os dados.
dir_dados = './dados'
if not os.path.exists(dir_dados):
    os.makedirs(dir_dados)

#Definindo a quantidade de classes e de imagens por classe.
num_classes = 21
tam_dados = 100

#Iniciando a captura de câmera e criando um loop para cada classe
captura = cv2.VideoCapture(0)
for j in range(num_classes):
    if not os.path.exists(os.path.join(dir_dados, str(j))):
        os.makedirs(os.path.join(dir_dados, str(j)))

    print(f'Coletando dados para a classe {j}')

#Criando um sistema de espera pelo usuário.
    pronto = False
    while True:
        ret, frame = captura.read()
        cv2.putText(frame, 'Pressione "Q" para iniciar a captura!', (100, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1.3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ord('q'):
            break

#Iniciando a coleta de imagens.
    counter = 0
    while counter < tam_dados:
        ret, frame = captura.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(dir_dados, str(j), '{}.jpg'.format(counter)), frame)

        counter += 1

#Finalizando o programa.
captura.release()
cv2.destroyAllWindows()