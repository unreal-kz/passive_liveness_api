import numpy as np
from typing import List

class BlinkDetector:
    """
    Lightweight blink detector using MediaPipe Face Mesh or OpenCV eye aspect ratio.
    """
    def __init__(self):
        self.use_mediapipe = False
        try:
            import mediapipe as mp
            self.mp_face_mesh = mp.solutions.face_mesh
            self.use_mediapipe = True
        except ImportError:
            self.mp_face_mesh = None
        try:
            import cv2
            self.cv2 = cv2
        except ImportError:
            self.cv2 = None

    def detect(self, video_bytes: bytes) -> bool:
        """
        Returns True if a blink is detected in the video.
        Args:
            video_bytes (bytes): Video file bytes (mp4/webm).
        Returns:
            bool: True if blink detected, else False.
        """
        frames = self._extract_frames(video_bytes)
        if not frames:
            return False
        if self.use_mediapipe:
            return self._detect_blink_mediapipe(frames)
        elif self.cv2 is not None:
            return self._detect_blink_cv(frames)
        return False

    def _extract_frames(self, video_bytes: bytes) -> List[np.ndarray]:
        # Try OpenCV
        if self.cv2 is None:
            return []
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=True) as f:
            f.write(video_bytes)
            f.flush()
            cap = self.cv2.VideoCapture(f.name)
            frames = []
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_rgb = self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2RGB)
                frames.append(frame_rgb)
            cap.release()
        return frames

    def _detect_blink_mediapipe(self, frames: List[np.ndarray]) -> bool:
        mp = self.mp_face_mesh
        with mp.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True) as face_mesh:
            eye_aspect_ratios = []
            for frame in frames:
                results = face_mesh.process(frame)
                if not results.multi_face_landmarks:
                    continue
                landmarks = results.multi_face_landmarks[0].landmark
                # Eye landmark indices (left: 33, 133, 159, 145), (right: 362, 263, 386, 374)
                def ear(indices):
                    p = [landmarks[i] for i in indices]
                    v = lambda a, b: np.linalg.norm([a.x-b.x, a.y-b.y])
                    return (v(p[1], p[3]) + v(p[0], p[2])) / (2.0 * v(p[0], p[1]))
                left_ear = ear([33, 133, 159, 145])
                right_ear = ear([362, 263, 386, 374])
                ear_avg = (left_ear + right_ear) / 2.0
                eye_aspect_ratios.append(ear_avg)
            # Blink = EAR drops below threshold and rises again
            if len(eye_aspect_ratios) < 3:
                return False
            min_ear = min(eye_aspect_ratios)
            max_ear = max(eye_aspect_ratios)
            return (max_ear - min_ear) > 0.15

    def _detect_blink_cv(self, frames: List[np.ndarray]) -> bool:
        # Naive: use Haarcascade for eyes, check for closed/open alternation
        if self.cv2 is None:
            return False
        cv2 = self.cv2
        haar = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
        eye_counts = []
        for frame in frames:
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            eyes = haar.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
            eye_counts.append(len(eyes))
        # Blink: at least one frame with no eyes detected between frames with eyes
        if len(eye_counts) < 3:
            return False
        return (min(eye_counts) == 0 and max(eye_counts) >= 2)
