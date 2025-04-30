import pytest
import numpy as np
import os

SAMPLE_IMAGE_PATH = os.path.join(os.path.dirname(__file__), '..', 'samples', 'portrait.jpg')

@pytest.mark.skipif(
    not os.path.exists(SAMPLE_IMAGE_PATH),
    reason="Sample portrait image not found."
)
def test_crop_and_align_face_shape():
    try:
        from passive_liveness_api.app.utils.face_cropper import crop_and_align_face
    except ImportError:
        pytest.skip("face_cropper module not importable")
    try:
        from PIL import Image
        img = np.array(Image.open(SAMPLE_IMAGE_PATH).convert("RGB"))
    except ImportError:
        import cv2
        img = cv2.cvtColor(cv2.imread(SAMPLE_IMAGE_PATH), cv2.COLOR_BGR2RGB)
    except Exception:
        pytest.skip("Neither Pillow nor OpenCV available to load image.")
    try:
        crop = crop_and_align_face(img)
        assert crop.shape == (112, 112, 3)
    except ImportError:
        pytest.skip("Neither MediaPipe nor Haarcascade available.")
    except ValueError as e:
        pytest.skip(f"No face detected: {e}")
