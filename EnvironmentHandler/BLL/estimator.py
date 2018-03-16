import numpy as np


class Estimator:

    def estimate_total_light(self, light: list) -> int:
        current_logged_hour = len(light)-1
        x = np.arange(current_logged_hour)
        y = np.array(light)
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y)[0]
        return ((m*current_logged_hour+c)+(m*23+c))/2*(23-current_logged_hour)
