import cv2
import mediapipe as mp
import numpy as np
from gesture_tracker.tracker import GestureTracker
from gesture_tracker.grid import path_to_grid
from gesture_tracker.packet import grid_to_entities
from gesture_tracker.udp_sender import UDPSender

# Config
UDP_IP = "127.0.0.1"
UDP_PORT = 7777
GRID_SIZE = 128

# Init
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
tracker = GestureTracker()

with UDPSender(UDP_IP, UDP_PORT) as udp_sender:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            h, w = frame.shape[:2]
            hand = results.multi_hand_landmarks[0]
            index_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x = int(index_tip.x * w)
            y = int(index_tip.y * h)
            tracker.add_point(x, y)

            gesture = tracker.detect_gesture()
            if gesture:
                print(f"🧠 Geste détecté : {gesture.upper()}")
                path = tracker.get_path()
                grid = path_to_grid(path, size=GRID_SIZE, input_width=w, input_height=h)
                
                # Debug affichage entités activées
                packet = grid_to_entities(grid, r=255, g=255, b=0)
                active_entities = [e for e in packet if e[1] > 0 or e[2] > 0 or e[3] > 0]
                print(f"🔢 Total entités activées : {len(active_entities)}")
                for ent in active_entities[:15]:
                    print(" →", ent)

                # ✅ Affichage de la représentation
                vis_grid = np.zeros((GRID_SIZE, GRID_SIZE, 3), dtype=np.uint8)
                for y in range(GRID_SIZE):
                    for x in range(GRID_SIZE):
                        if grid[y][x]:
                            vis_grid[y, x] = [0, 255, 255]
                vis_grid = cv2.resize(vis_grid, (512, 512), interpolation=cv2.INTER_NEAREST)
                cv2.imshow("🟦 Simulation Panneau LED 128x128", vis_grid)

                # Envoi UDP
                success = udp_sender.send_packet(packet)
                print("✅ Packet envoyé" if success else "❌ Échec envoi")

                tracker.reset()

        cv2.imshow("Gesture Tracker (HD)", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
