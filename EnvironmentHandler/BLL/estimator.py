import numpy as np
from datetime import time


class Estimator:

    def estimate_total_light(self, light: list, dark_hours_start: time) -> int:
        current_logged_hour = len(light)-1
        x = np.arange(current_logged_hour)
        y = np.array(light)
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y)[0]
        if dark_hours_start.hour == 0:
            return ((m*current_logged_hour+c)+(m*23+c))/2*(23-current_logged_hour)
        return ((m*current_logged_hour+c)+(m*23+c))/2*(dark_hours_start.hour-current_logged_hour)
