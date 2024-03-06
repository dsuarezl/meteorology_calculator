from .z_score_calculator import ZScore

class ZScoreSelectedData(ZScore):

    def _specific_calculate(self, data_frame, variable=None, selected_data_date_range=None, **kwargs):
        if variable is None:
            raise ValueError("Variable is None")

        if selected_data_date_range is None or 'start' not in selected_data_date_range or 'end' not in selected_data_date_range:
            raise ValueError("date_range must be a dictionary with 'start' and 'end' keys")

        filtered_data = self.filter_by_date(data_frame, selected_data_date_range)
        
        # Group the data and calculate mean and std, including latitude and longitude in the result
        grouped = filtered_data.groupby(['latitude', 'longitude'])
        stats = grouped[variable].agg(['mean', 'std']).reset_index()

        # Merge mean and std back to the original data frame
        data_frame = data_frame.merge(stats, on=['latitude', 'longitude'])

        # Calculate z-score for the original data frame
        data_frame['z_score'] = (data_frame[variable] - data_frame['mean']) / data_frame['std']
        data_frame['z_score'] = data_frame['z_score'].fillna(0)  # Handle division by zero if std is 0

        # Drop the mean and std columns if you don't need them anymore
        data_frame = data_frame.drop(columns=['mean', 'std'])

        return data_frame
