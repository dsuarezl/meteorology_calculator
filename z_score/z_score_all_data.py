

from .z_score_calculator import ZScore

class ZScoreAllData(ZScore):

    def _specific_calculate(self, data_frame, time_group='daily', variable=None, **kwargs):

        if(variable is None):
            raise ValueError("Variable is none")
        
        grouped = data_frame.groupby(['latitude', 'longitude', 'day', 'month'])[variable]
        
        mean = grouped.transform('mean')
        std = grouped.transform('std')

        # Calculate z-score
        data_frame['z_score'] = (data_frame[variable] - mean) / std

        return data_frame

