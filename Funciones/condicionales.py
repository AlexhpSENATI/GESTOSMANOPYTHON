import cv2
import numpy as np

def condicionalesLetras(dedos, frame):
    font = cv2.FONT_HERSHEY_SIMPLEX

    letras = {
        'like': {'dedos': [1, 1, 0, 0, 0, 0]},
        'paz': {'dedos': [0, 1, 0, 0, 1, 1]},
        'Hola': {'dedos': [1, 1, 1, 1, 1, 1]},  # Mano abierta, todos los dedos levantados
        'Adiós': {'dedos': [1, 0, 1, 0, 1, 0]},  # Mano levantada con solo el pulgar, índice y meñique levantados
        'Pausa': {'dedos': [0, 1, 1, 1, 1, 0]},  # Mano paralela con dedos juntos

        # Gestos populares (de la lengua de señas)
        'Pulgar Abajo': {'dedos': [0, 0, 0, 0, 0]},  # Pulgar hacia abajo (mano cerrada)
        'Ok': {'dedos': [1, 1, 1, 1, 1, 0]},  # Forma de OK, pulgar, índice y meñique levantados
        'Mano Cerrada': {'dedos': [0, 0, 0, 0, 0]},  # Mano completamente cerrada
        'Pulgar Hacia Un Lado': {'dedos': [1, 0, 0, 0, 0]},  # Pulgar hacia el lado (sin levantar)
        'Puño': {'dedos': [0, 0, 0, 0, 0]},  # Puño cerrado
    
        # Gestos de insultos o comentarios (puedes personalizarlos según necesidades)
        'Dedo Medio': {'dedos': [0, 0, 1, 0, 0]},  # Dedo medio levantado (gesto común de insulto)
        'Señal de Cuernos': {'dedos': [1, 0, 0, 0, 1]},  # Mano haciendo el gesto de cuernos (dedo índice y meñique levantados)
        }

    for gesto, info in letras.items():
        if dedos == info['dedos']:
            mostrar_letra(frame, gesto)
            return dedos

    return dedos

def mostrar_letra(frame, gesto):
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    cv2.rectangle(frame, (10, 10), (290, 90), (255, 0, 0), 10) 
    cv2.rectangle(frame, (10, 10), (290, 90), (0, 255, 0), -1)  
    
    cv2.putText(frame, gesto, (30, 70), font, 2, (255, 0, 0), 4, cv2.LINE_AA)
    print(gesto)

