from .z_score_calculator import ZScore

class ZScorePrevData(ZScore):

    def _specific_calculate(self, data_frame, time_group='daily', variable = None,  **kwargs):

        if(variable is None):
            raise ValueError("Variable is none")
        
        # Sort the dataframe by year for cumulative calculations
        data_frame = data_frame.sort_values(by=['year'])

        # Function to calculate the cumulative mean up to but not including the current year
        def cumulative_mean(s):
            return s.expanding().mean().shift(1)

        # Function to calculate the cumulative std up to but not including the current year
        def cumulative_std(s):
            return s.expanding().std().shift(1)

        # Group by the relevant columns
        grouped = data_frame.groupby(['latitude', 'longitude', 'day', 'month'])

        # Calculate the cumulative mean and std for each group as Series
        cumulative_mean_series = grouped[variable].transform(cumulative_mean)
        cumulative_std_series = grouped[variable].transform(cumulative_std)

        # Calculate the z-score 
        data_frame['z_score'] = (data_frame[variable] - cumulative_mean_series) / cumulative_std_series

        return data_frame
