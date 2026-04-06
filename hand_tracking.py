import cv2
import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

class HandTracker:
    def __init__(self):
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
            running_mode=VisionRunningMode.IMAGE,
            num_hands=1
        )
        self.detector = HandLandmarker.create_from_options(options)

    def get_x(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = self.detector.detect(mp_image)

        if result.hand_landmarks:
            hand = result.hand_landmarks[0]
            return int(hand[8].x * frame.shape[1])
        return None