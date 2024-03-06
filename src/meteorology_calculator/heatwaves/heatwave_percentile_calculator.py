from .heatwave_calculator import HeatWaveCalculator

class HeatwavesPercentileCalculator(HeatWaveCalculator):

    def _specific_calculate(self, data_frame,  consecutive_days, selected_data_date_range = None, heatwave_percentile=None, **kwargs):

        if  heatwave_percentile is None:
            raise ValueError("heatwave_percentile is None")

        if selected_data_date_range is None:
            raise ValueError("Data date range is None")
        
        heatwave_percentile = float(heatwave_percentile)

        def detect_heatwaves(group):
            
            group = group.sort_values(by=['year', 'month', 'day'])

            threshold_temp = self.filter_by_date(group, selected_data_date_range).t2m.quantile(heatwave_percentile)
            above_threshold = group["t2m"] > threshold_temp
            heatwave_detected = above_threshold.rolling(window=consecutive_days).sum() >= consecutive_days
            group['Heatwave'] = 0 
            group.loc[heatwave_detected, 'Heatwave'] = 1 
            return group

        return data_frame.groupby(['latitude', 'longitude']).apply(detect_heatwaves).drop(columns=["datetime"]).reset_index(drop=True)
