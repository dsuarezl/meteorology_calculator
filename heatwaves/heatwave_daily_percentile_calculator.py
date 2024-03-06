from .heatwave_calculator import HeatWaveCalculator

class HeatwavesDailyPercentileCalculator(HeatWaveCalculator):


    def _specific_calculate(self, data_frame, consecutive_days, heatwave_daily_percentile=None, **kwargs):
        if heatwave_daily_percentile is None:
            raise ValueError("heatwave_daily_percentile is None")
        
        heatwave_daily_percentile = float(heatwave_daily_percentile)

        # Calculate daily thresholds based on the provided percentile across all years for each day-month combination for each cluster
        daily_thresholds = data_frame.groupby(['latitude', 'longitude', 'day', 'month']).t2m.quantile(heatwave_daily_percentile).reset_index()
        daily_thresholds.rename(columns={'t2m': 't2m_threshold'}, inplace=True)

        # Merge the daily_thresholds with the main data frame
        data_frame = data_frame.merge(daily_thresholds, on=['latitude', 'longitude', 'day', 'month'], how='left')

        # Create a boolean column to check if t2m is above the daily threshold
        data_frame['above_threshold'] = data_frame['t2m'] > data_frame['t2m_threshold']

        def detect_heatwaves(group):
            group = group.sort_values(by=['year', 'month', 'day'])
            heatwave_detected = group['above_threshold'].rolling(window=consecutive_days).sum() >= consecutive_days
            group['Heatwave'] = 0 
            group.loc[heatwave_detected, 'Heatwave'] = 1 
            return group

        return data_frame.groupby(['latitude', 'longitude']).apply(detect_heatwaves).reset_index(drop=True)
