from typing import Any
import numpy as np
import base64


def decode_base64_to_rgb_array(image_base64: str) -> np.ndarray:
    """
    Decode a base64-encoded RGB image string into a NumPy RGB array.
    Args:
        image_base64 (str): Base64-encoded image string.
    Returns:
        np.ndarray: Decoded RGB image array.
    Raises:
        ValueError: If decoding or image loading fails.
    """
    try:
        image_bytes = base64.b64decode(image_base64)
    except Exception as e:
        raise ValueError("Invalid base64 input") from e

    # Try Pillow first, fallback to OpenCV
    try:
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        arr = np.array(img)
        return arr
    except ImportError:
        pass
    except Exception as e:
        raise ValueError("Invalid image input (Pillow)") from e

    try:
        import cv2
        arr = np.frombuffer(image_bytes, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("OpenCV failed to decode image")
        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img
    except ImportError:
        raise ImportError("Neither Pillow nor OpenCV is installed.")
    except Exception as e:
        raise ValueError("Invalid image input (OpenCV)") from e


def preprocess_for_model(image: np.ndarray) -> np.ndarray:
    """
    Crop, resize, and normalize image for SilentFace model: 1x3x112x112 float32, 0-1 range.
    Args:
        image (np.ndarray): Input RGB image array (H,W,3).
    Returns:
        np.ndarray: Preprocessed image array (1,3,112,112).
    """
    img = image
    # Try to import face_cropper and crop face
    try:
        from passive_liveness_api.app.utils import face_cropper
        img = face_cropper.crop_and_align_face(img)
    except ImportError:
        try:
            from ..utils import face_cropper
            img = face_cropper.crop_and_align_face(img)
        except Exception:
            # Could not import face_cropper, fallback to original image
            pass
    except Exception:
        # Could not crop face (e.g., no face detected), fallback to original image
        pass
    # Resize (should already be 112x112, but ensure)
    target_size = (112, 112)
    try:
        import cv2
        img = cv2.resize(img, target_size, interpolation=cv2.INTER_LINEAR)
    except ImportError:
        try:
            from PIL import Image
            img = Image.fromarray(img)
            img = img.resize(target_size, resample=Image.BILINEAR)
            img = np.array(img)
        except ImportError:
            raise ImportError("Neither OpenCV nor Pillow is installed for resizing.")
    # Normalize to 0-1 float32
    img = img.astype(np.float32) / 255.0
    # Reorder to (1,3,112,112)
    img = np.transpose(img, (2, 0, 1))  # (3,112,112)
    img = np.expand_dims(img, 0)        # (1,3,112,112)
    return img
