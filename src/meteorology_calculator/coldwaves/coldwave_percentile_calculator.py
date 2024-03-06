from .coldwave_calculator import ColdWaveCalculator

class ColdwavesPercentileCalculator(ColdWaveCalculator):

    def _specific_calculate(self, data_frame, consecutive_days, selected_data_date_range = None,coldwave_percentile=None, **kwargs):
        if coldwave_percentile is None:
            raise ValueError("coldwave_percentile is None")
        
        if selected_data_date_range is None:
            raise ValueError("Data date range is None")

        coldwave_percentile = float(coldwave_percentile)

        def detect_coldwaves(group):
            group = group.sort_values(by=['year', 'month', 'day'])
            threshold_temp = self.filter_by_date(group, selected_data_date_range).t2m.quantile(1 - coldwave_percentile)
            below_threshold = group["t2m"] < threshold_temp
            coldwave_detected = below_threshold.rolling(window=consecutive_days).sum() >= consecutive_days
            group['Coldwave'] = 0
            group.loc[coldwave_detected, 'Coldwave'] = 1
            return group

        return data_frame.groupby(['latitude', 'longitude']).apply(detect_coldwaves).reset_index(drop=True).drop(columns=["datetime"])
