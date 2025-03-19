import cv2
import numpy as np

cap = cv2.VideoCapture("q1/q1B.mp4")

ultrapassagem_confirmada = False
colisao_ocorreu = False
ultimo_contato = False

# Função para detectar contornos
def detectar_formas(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img_gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Seu código aqui.......

    contours = detectar_formas(frame)
    formas = [(contour, cv2.contourArea(contour)) for contour in contours]

    if len(formas) >= 2:
        maior_contorno = max(formas, key=lambda x: x[1])[0]
        menor_contorno = min(formas, key=lambda x: x[1])[0]

        # Aumenta o contorno do quadrado azul
        x, y, w, h = cv2.boundingRect(maior_contorno)
        margem = 5  
        x = max(0, x - margem)
        y = max(0, y - margem)
        w = w + 2 * margem
        h = h + 2 * margem

        # Desenha os contornos
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Azul
        cv2.drawContours(frame, [menor_contorno], -1, (0, 255, 255), 2)  # Bege

        # Verifica colisão
        colisao = ( cv2.boundingRect(menor_contorno)[0] + cv2.boundingRect(menor_contorno)[2] > x 
                    and 
                    cv2.boundingRect(menor_contorno)[0] < x + w 
                    and 
                    cv2.boundingRect(menor_contorno)[1] + cv2.boundingRect(menor_contorno)[3] > y 
                    and
                    cv2.boundingRect(menor_contorno)[1] < y + h)

        if colisao:
            # Marca a colisão
            colisao_ocorreu = True
            ultimo_contato = True
            cv2.putText(frame, "COLISAO DETECTADA", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif colisao_ocorreu and not colisao:
            # Confirma ultrapassagem
            maior_contorno_x = x
            menor_contorno_x = cv2.boundingRect(menor_contorno)[0]

            if maior_contorno_x < menor_contorno_x:
                ultrapassagem_confirmada = True
                colisao_ocorreu = False
                ultimo_contato = False

        if ultrapassagem_confirmada and not ultimo_contato:
            cv2.putText(frame, "PASSOU A BARREIRA", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

     # Exibe resultado
    cv2.imshow("VIDEO FINAL", frame)
    
    # Wait for key 'ESC' to quit
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()