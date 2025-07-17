import numpy as np
from scipy.signal import savgol_filter

class GestureTracker:
    def __init__(self, max_points=50):
        self.points = []
        self.max_points = max_points

    def add_point(self, x, y):
        self.points.append((x, y))
        self.points = self.points[-self.max_points:]

    def reset(self):
        self.points = []

    def get_path(self):
        return self.points.copy()

    def detect_gesture(self):
        if len(self.points) < 15:
            return None

        points = self._get_smoothed_points()
        normed = self._normalize_points(points)

        if self._is_circle(normed):
            return 'circle'
        elif self._is_line(normed):
            return 'line'
        return None

    def _get_smoothed_points(self):
        points = np.array(self.points)
        if len(points) >= 7:
            x_smooth = savgol_filter(points[:, 0], 7, 2)
            y_smooth = savgol_filter(points[:, 1], 7, 2)
            return np.stack([x_smooth, y_smooth], axis=1)
        return points

    def _normalize_points(self, points):
        """Ramène les points entre [0, 1] pour être agnostique à la taille écran"""
        min_vals = np.min(points, axis=0)
        max_vals = np.max(points, axis=0)
        scale = np.max(max_vals - min_vals)
        if scale == 0:  # éviter division par zéro
            return points - min_vals
        return (points - min_vals) / scale

    def _is_circle(self, points):
        cx, cy = np.mean(points, axis=0)
        distances = np.sqrt((points[:, 0] - cx) ** 2 + (points[:, 1] - cy) ** 2)
        variance = np.var(distances)
        is_closed = np.linalg.norm(points[0] - points[-1]) < 0.2
        return variance < 0.01 and is_closed

    def _is_line(self, points):
        x = points[:, 0]
        y = points[:, 1]
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]
        y_fit = m * x + c
        error = np.mean((y - y_fit) ** 2)
        return error < 0.002
