import utils
from .coldwave_calculator import ColdWaveCalculator
from numba import jit

class ColdwavesAbsoluteCalculator(ColdWaveCalculator):

    def _specific_calculate(self, data_frame, consecutive_days, coldwave_threshold=None, **kwargs):
        if coldwave_threshold is None:
            raise ValueError("coldwave_threshold is None")

        coldwave_threshold = float(coldwave_threshold)
        threshold_temp = utils.fahrenheit_to_celsius(coldwave_threshold)

        def detect_coldwaves(group):
            group = group.sort_values(by=['year', 'month', 'day'])
            below_threshold = group["t2m"] < threshold_temp
            coldwave_detected = below_threshold.rolling(window=consecutive_days).sum() >= consecutive_days
            group['Coldwave'] = 0
            group.loc[coldwave_detected, 'Coldwave'] = 1
            return group

        return data_frame.groupby(['latitude', 'longitude']).apply(detect_coldwaves).reset_index(drop=True)
