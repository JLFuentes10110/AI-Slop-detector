import cv2
import numpy as np
import io
from typing import Tuple, List
from PIL import Image
from transformers import pipeline

# Loaded once at startup — not on every request
detector = pipeline(
    "image-classification",
    model="umm-maybe/AI-image-detector"
)


def detect_blur(image: np.ndarray) -> Tuple[float, bool]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    return round(float(variance), 2), variance < 100.0


def detect_noise(image: np.ndarray) -> Tuple[float, bool]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    noise_level = float(np.mean(cv2.absdiff(gray, blurred)))
    return round(noise_level, 2), noise_level > 8.0


def detect_color_uniformity(image: np.ndarray) -> Tuple[float, bool]:
    avg_std = sum(float(np.std(image[:, :, c])) for c in range(3)) / 3
    return round(avg_std, 2), avg_std < 30.0


def detect_edge_unnaturalness(image: np.ndarray) -> Tuple[float, bool]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_density = float(np.sum(edges > 0)) / edges.size
    return round(edge_density, 4), edge_density < 0.01


def detect_ai_generated(image_bytes: bytes) -> Tuple[float, bool]:
    """
    Uses a HuggingFace model trained specifically to detect
    AI-generated images. Returns (confidence %, is_ai_generated).
    """
    pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    results = detector(pil_image)

    ai_score = next(
        (r["score"] for r in results if "artificial" in r["label"].lower()
         or "ai" in r["label"].lower()),
        0.0
    )
    return round(ai_score * 100, 1), ai_score > 0.5


def analyze_image(image_bytes: bytes) -> Tuple[float, List[str], List[str]]:
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image is None:
        return 80.0, ["Could not decode image."], ["Upload a valid JPEG or PNG file."]

    issues, suggestions, penalty = [], [], 0.0

    # --- Existing quality checks ---
    _, is_blurry = detect_blur(image)
    if is_blurry:
        penalty += 25
        issues.append("Image appears blurry.")
        suggestions.append("Use a higher-resolution or sharper source image.")

    noise_level, has_noise = detect_noise(image)
    if has_noise:
        penalty += 20
        issues.append(f"Elevated noise level detected ({noise_level}).")
        suggestions.append("Apply light denoising or use a cleaner source.")

    color_std, is_uniform = detect_color_uniformity(image)
    if is_uniform:
        penalty += 25
        issues.append(f"Suspiciously uniform color palette (std={color_std}). Possible AI generation.")
        suggestions.append("Prefer natural, varied imagery over AI-generated visuals.")

    edge_density, unnatural_edges = detect_edge_unnaturalness(image)
    if unnatural_edges:
        penalty += 20
        issues.append(f"Very low edge density ({edge_density}). May indicate synthetic content.")
        suggestions.append("Use photographic or hand-crafted images when possible.")

    # --- AI generation detection (main new check) ---
    ai_confidence, is_ai = detect_ai_generated(image_bytes)
    if is_ai:
        penalty += 40
        issues.append(f"Image likely AI-generated (confidence: {ai_confidence}%).")
        suggestions.append("Use real photographs instead of AI-generated imagery.")
    elif ai_confidence > 25:
        # Borderline — flag it but with lower penalty
        penalty += 15
        issues.append(f"Image shows some AI-generation characteristics ({ai_confidence}% confidence).")

    return round(min(100.0, max(0.0, penalty)), 1), issues, suggestions