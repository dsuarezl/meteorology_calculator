from .heatwave_calculator import HeatWaveCalculator
import utils

class HeatwavesAbsoluteCalculator(HeatWaveCalculator):

    def _specific_calculate(self, data_frame, consecutive_days, heatwave_threshold=None, **kwargs):

        if heatwave_threshold is None:
            raise ValueError("heatwave_threshold is None")

        heatwave_threshold = float(heatwave_threshold)

        threshold_temp = utils.fahrenheit_to_celsius(heatwave_threshold)
        

        def detect_heatwaves(group):
            group = group.sort_values(by=['year', 'month', 'day'])
            above_threshold = group["t2m"] > threshold_temp
            heatwave_detected = above_threshold.rolling(window=consecutive_days).sum() >= consecutive_days
            group['Heatwave'] = 0 
            group.loc[heatwave_detected, 'Heatwave'] = 1
            return group
        
        return data_frame.groupby(['latitude', 'longitude']).apply(detect_heatwaves).reset_index(drop=True)
    

