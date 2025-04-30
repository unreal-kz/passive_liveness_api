import numpy as np

def crop_and_align_face(image: np.ndarray) -> np.ndarray:
    """
    Detect, crop, and align the largest face in the image.
    Uses MediaPipe Face Detection if available, else OpenCV Haarcascade.
    Args:
        image (np.ndarray): Input RGB image (H,W,3)
    Returns:
        np.ndarray: Cropped, aligned face (112,112,3) RGB
    Raises:
        ValueError: If no face is detected.
    """
    h, w = image.shape[:2]
    face_bbox = None
    # Try MediaPipe Face Detection
    try:
        import mediapipe as mp
        mp_face = mp.solutions.face_detection
        with mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5) as detector:
            results = detector.process(image)
            if results.detections:
                # Pick largest face
                max_area = 0
                for det in results.detections:
                    bbox = det.location_data.relative_bounding_box
                    x, y, bw, bh = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                    abs_bbox = [int(x*w), int(y*h), int(bw*w), int(bh*h)]
                    area = bw * bh
                    if area > max_area:
                        max_area = area
                        face_bbox = abs_bbox
    except ImportError:
        pass
    except Exception:
        pass
    # Fallback: OpenCV Haarcascade
    if face_bbox is None:
        try:
            import cv2
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            haar = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = haar.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            if len(faces) > 0:
                # Pick largest
                x, y, bw, bh = max(faces, key=lambda b: b[2]*b[3])
                face_bbox = [x, y, bw, bh]
        except ImportError:
            pass
        except Exception:
            pass
    if face_bbox is None:
        raise ValueError("No face detected")
    # Expand bbox by 10%
    x, y, bw, bh = face_bbox
    cx, cy = x + bw/2, y + bh/2
    scale = 1.1
    size = int(max(bw, bh) * scale)
    nx = int(cx - size/2)
    ny = int(cy - size/2)
    nx = max(0, nx)
    ny = max(0, ny)
    size = min(size, w-nx, h-ny)
    crop = image[ny:ny+size, nx:nx+size]
    # Resize to 112x112
    try:
        import cv2
        crop = cv2.resize(crop, (112, 112), interpolation=cv2.INTER_LINEAR)
    except ImportError:
        try:
            from PIL import Image
            crop = Image.fromarray(crop)
            crop = crop.resize((112,112), resample=Image.BILINEAR)
            crop = np.array(crop)
        except ImportError:
            raise ImportError("Neither OpenCV nor Pillow is installed for resizing.")
    return crop
