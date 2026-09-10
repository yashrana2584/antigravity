import cv2
import numpy as np

def draw_hud_box(frame, x, y, w, h, color=(0, 230, 80), label="", confidence=None, corner_len=20, thickness=2):
    """
    Draws a sleek, modern biometric HUD bounding box with corner brackets
    and a clean name/confidence badge.
    """
    # Semi-transparent inner tint
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
    cv2.addWeighted(overlay, 0.08, frame, 0.92, 0, frame)

    # Outer thin bounding box
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1)

    # Corner brackets
    # Top-Left
    cv2.line(frame, (x, y), (x + corner_len, y), color, thickness + 1)
    cv2.line(frame, (x, y), (x, y + corner_len), color, thickness + 1)
    # Top-Right
    cv2.line(frame, (x + w, y), (x + w - corner_len, y), color, thickness + 1)
    cv2.line(frame, (x + w, y), (x + w, y + corner_len), color, thickness + 1)
    # Bottom-Left
    cv2.line(frame, (x, y + h), (x + corner_len, y + h), color, thickness + 1)
    cv2.line(frame, (x, y + h), (x, y + h - corner_len), color, thickness + 1)
    # Bottom-Right
    cv2.line(frame, (x + w, y + h), (x + w - corner_len, y + h), color, thickness + 1)
    cv2.line(frame, (x + w, y + h), (x + w, y + h - corner_len), color, thickness + 1)

    # Label badge
    text = label
    if confidence is not None:
        text = f"{label} ({confidence}%)"

    if text:
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 0.55
        font_thick = 1
        (txt_w, txt_h), baseline = cv2.getTextSize(text, font, font_scale, font_thick)

        # Badge background
        badge_y1 = max(0, y - txt_h - 10)
        badge_y2 = y
        badge_x1 = x
        badge_x2 = x + txt_w + 16

        cv2.rectangle(frame, (badge_x1, badge_y1), (badge_x2, badge_y2), (20, 20, 25), -1)
        cv2.rectangle(frame, (badge_x1, badge_y1), (badge_x2, badge_y2), color, 1)
        cv2.putText(frame, text, (badge_x1 + 8, badge_y2 - 6), font, font_scale, (255, 255, 255), font_thick, cv2.LINE_AA)

def draw_scan_line(frame, scan_pos_pct, color=(0, 200, 255)):
    """Draws an animated horizontal scanning beam across the frame."""
    h, w = frame.shape[:2]
    y = int(h * scan_pos_pct)
    if 0 <= y < h:
        # Beam glow
        overlay = frame.copy()
        cv2.line(overlay, (0, y), (w, y), color, 3)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        cv2.line(frame, (0, y), (w, y), (255, 255, 255), 1)
