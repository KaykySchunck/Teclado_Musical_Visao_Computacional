import cv2
import mediapipe as mp
import serial
import time

arduino = serial.Serial('COM5', 9600)  # Troque por sua porta correta
time.sleep(2)  # Espera inicial para estabilizar a conexão

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)

def dedos_abaixados(landmarks):
    dedos = []
    dedos_tips = [4, 8, 12, 16, 20]

    for i in range(5):
        tip = landmarks.landmark[dedos_tips[i]]
        base = landmarks.landmark[dedos_tips[i] - 2]

        if i == 0:
            dedos.append(tip.x < base.x)  # Polegar na horizontal
        else:
            dedos.append(tip.y > base.y)  # Outros dedos na vertical
    return dedos

while True:
    ret, frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            estado = dedos_abaixados(hand)
            for i, abaixado in enumerate(estado):
                if abaixado:
                    arduino.write(str(i).encode())
                    time.sleep(0.3)  # Delay para evitar repetições

    cv2.imshow('Controle Musical', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
