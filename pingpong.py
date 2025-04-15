import cv2
import mediapipe as mp
import pygame
import time

# Configurações do jogo
WIDTH, HEIGHT = 640, 480
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
BALL_SIZE = 10
BALL_SPEED = 5

# Inicializando o Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Controlado por Mãos")

# Configurações do MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Inicializa a Bola
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = BALL_SPEED, BALL_SPEED

# Inicializa paddles para duas mãos
paddle_y_left = HEIGHT // 2 - PADDLE_HEIGHT // 2
paddle_y_right = HEIGHT // 2 - PADDLE_HEIGHT // 2

# Pontuação
score_left = 0
score_right = 0

def detectar_maos(frame):
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    return results.multi_hand_landmarks  # Retorna todas as mãos detectadas

def controlar_paddle(hand_landmarks, side):
    # Pegando a posição do dedo indicador (pode ser alterado para outro dedo)
    x = hand_landmarks.landmark[8].x
    y = hand_landmarks.landmark[8].y
    paddle_y = int(y * HEIGHT)  # Mapeia a posição para a altura da tela
    
    # Atualiza a posição do paddle dependendo do lado (esquerdo ou direito)
    if side == "left":
        return max(0, min(paddle_y, HEIGHT - PADDLE_HEIGHT))
    elif side == "right":
        return max(0, min(paddle_y, HEIGHT - PADDLE_HEIGHT))
    return paddle_y

# Função para desenhar o placar
def desenhar_placar():
    font = pygame.font.Font(None, 36)
    text_left = font.render(f"{score_left}", True, (255, 255, 255))
    text_right = font.render(f"{score_right}", True, (255, 255, 255))
    screen.blit(text_left, (WIDTH // 4 - text_left.get_width() // 2, 20))
    screen.blit(text_right, (WIDTH * 3 // 4 - text_right.get_width() // 2, 20))

# Loop principal do jogo
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detecta as mãos
    hand_landmarks_list = detectar_maos(frame)

    if hand_landmarks_list:
        if len(hand_landmarks_list) > 0:
            paddle_y_right = controlar_paddle(hand_landmarks_list[0], "right")  # Controla o paddle direito (mão esquerda)
        if len(hand_landmarks_list) > 1:
            paddle_y_left = controlar_paddle(hand_landmarks_list[1], "left")  # Controla o paddle esquerdo (mão direita)

    # Movimento da bola
    ball_x += ball_dx
    ball_y += ball_dy

    # Colisão com a parede superior/inferior
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
        ball_dy = -ball_dy

    # Colisão com o paddle esquerdo (mão direita)
    if ball_x <= PADDLE_WIDTH and paddle_y_left <= ball_y <= paddle_y_left + PADDLE_HEIGHT:
        ball_dx = -ball_dx

    # Colisão com o paddle direito (mão esquerda)
    if ball_x >= WIDTH - PADDLE_WIDTH and paddle_y_right <= ball_y <= paddle_y_right + PADDLE_HEIGHT:
        ball_dx = -ball_dx

    # Colisão com a parede direita (perdeu o ponto)
    if ball_x >= WIDTH:
        score_left += 1  # Mão esquerda (paddle direito) ganha ponto
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2  # Resetando a bola

    # Colisão com a parede esquerda (perdeu o ponto)
    if ball_x <= 0:
        score_right += 1  # Mão direita (paddle esquerdo) ganha ponto
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2  # Resetando a bola

    # Desenha a bola e os paddles
    screen.fill((0, 0, 0))  # Preenche a tela de preto
    pygame.draw.rect(screen, (255, 255, 255), (0, paddle_y_left, PADDLE_WIDTH, PADDLE_HEIGHT))  # Desenha o paddle esquerdo (mão direita)
    pygame.draw.rect(screen, (255, 255, 255), (WIDTH - PADDLE_WIDTH, paddle_y_right, PADDLE_WIDTH, PADDLE_HEIGHT))  # Desenha o paddle direito (mão esquerda)
    pygame.draw.circle(screen, (255, 255, 255), (ball_x, ball_y), BALL_SIZE)  # Desenha a bola

    # Desenha o placar
    desenhar_placar()

    # Exibe os landmarks das mãos (sempre)
    if hand_landmarks_list:
        for hand_landmarks in hand_landmarks_list:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    pygame.display.flip()

    # Captura as teclas para fechar o jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            exit()

    # Exibe a imagem com o MediaPipe
    cv2.imshow('MediaPipe - Pong', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Pressione ESC para sair
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
