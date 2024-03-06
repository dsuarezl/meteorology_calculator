
from .coldwave_calculator import ColdWaveCalculator

class ColdwavesDailyPercentileCalculator(ColdWaveCalculator):

    def _specific_calculate(self, data_frame, consecutive_days = 3, coldwave_daily_percentile=None, **kwargs):
        if coldwave_daily_percentile is None:
            raise ValueError("coldwave_daily_percentile is None")

        coldwave_daily_percentile = float(coldwave_daily_percentile)
        daily_thresholds = data_frame.groupby(['latitude', 'longitude', 'day', 'month']).t2m.quantile(1 - coldwave_daily_percentile).reset_index()
        daily_thresholds.rename(columns={'t2m': 't2m_threshold'}, inplace=True)
        data_frame = data_frame.merge(daily_thresholds, on=['latitude', 'longitude', 'day', 'month'], how='left')
        data_frame['below_threshold'] = data_frame['t2m'] < data_frame['t2m_threshold']

        def detect_coldwaves(group):
            group = group.sort_values(by=['year', 'month', 'day'])
            coldwave_detected = group['below_threshold'].rolling(window=consecutive_days).sum() >= consecutive_days
            group['Coldwave'] = 0
            group.loc[coldwave_detected, 'Coldwave'] = 1
            return group

        return data_frame.groupby(['latitude', 'longitude']).apply(detect_coldwaves).reset_index(drop=True)
