import cv2
import mediapipe as mp
from Funciones.condicionales import condicionalesLetras
from Funciones.normalizacionCords import obtenerAngulos

lectura_actual = 0
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles
cap = cv2.VideoCapture(0)  
wCam, hCam = 1280, 720  
cap.set(3, wCam)
cap.set(4, hCam)

with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame = cv2.GaussianBlur(frame, (3, 3), 0)  
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            angulosid = obtenerAngulos(results, width, height)[0]
            dedos = []
            if angulosid[5] > 125:
                dedos.append(1)
            else:
                dedos.append(0)
            if angulosid[4] > 150:
                dedos.append(1)
            else:
                dedos.append(0)
            for id in range(0, 4):
                if angulosid[id] > 90:
                    dedos.append(1)
                else:
                    dedos.append(0)
            condicionalesLetras(dedos, frame)
            pinky = obtenerAngulos(results, width, height)[1]
            pinkY = pinky[1] + pinky[0]
            resta = pinkY - lectura_actual
            lectura_actual = pinkY
            print(abs(resta), pinkY, lectura_actual)
            if dedos == [0, 0, 1, 0, 0, 0]:
                if abs(resta) > 30:
                    print("jota en movimiento")
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.rectangle(frame, (0, 0), (100, 100), (0, 0, 0), -1)  
                    cv2.putText(frame, 'J', (20, 80), font, 3, (255, 0, 0), 2, cv2.LINE_AA) 
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS, 
                        mp_drawing_styles.get_default_hand_landmarks_style(), 
                        mp_drawing_styles.get_default_hand_connections_style())  
                    for idx, landmark in enumerate(hand_landmarks.landmark):
                        x, y = int(landmark.x * width), int(landmark.y * height)
                        cv2.circle(frame, (x, y), 7, (0, 255, 0), -1) 
                    for connection in mp_hands.HAND_CONNECTIONS:
                        start_idx, end_idx = connection
                        start = hand_landmarks.landmark[start_idx]
                        end = hand_landmarks.landmark[end_idx]
                        start_coords = int(start.x * width), int(start.y * height)
                        end_coords = int(end.x * width), int(end.y * height)
                        cv2.line(frame, start_coords, end_coords, (0, 0, 0), 4)  
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
