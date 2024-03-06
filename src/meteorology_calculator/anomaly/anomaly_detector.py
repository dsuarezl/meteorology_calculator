from abc import ABC, abstractmethod
import plotly.express as px

from ..meteorology_calculator import MeteorologyCalculator

class AnomalyDetector(MeteorologyCalculator, ABC):

    @abstractmethod
    def _specific_calculate(self, data_frame, anomaly_threshold=None, **kwargs):
        pass

    def calculate(self, data_frame, date_range=None, contamination=None, time_group="daily", variable = None, **kwargs):
        data_frame = super().calculate(data_frame, date_range=date_range, time_group=time_group)
        
        result_df = self._specific_calculate(data_frame, contamination=contamination, variable=variable, **kwargs)

        return result_df

    def plot(self, df, plot_type="scatter map", time_group = "daily", **kwargs):
        if plot_type is None:
            plot_type="scatter map"
        
        if(time_group is None):
            time_group = "daily"

        time_group_conversion = {   
            "daily": "day",
            "monthly": "month",
            "yearly": "year"
        }

        # Filter and sum anomalies (values equal to -1)
        anomaly_df = df[df['Anomaly'] == -1]

        if time_group in time_group_conversion:
            anomaly_df = anomaly_df.groupby(['latitude', 'longitude', time_group_conversion[time_group]])['Anomaly'].sum().reset_index()
        else:
            raise ValueError(f"Unknown time group: {time_group}")

        # Convert negative anomalies to positive
        anomaly_df['Anomaly'] = anomaly_df['Anomaly'].abs()

        if plot_type == 'density map':
            fig = px.density_mapbox(
                anomaly_df,
                lat='latitude',
                lon='longitude',
                z='Anomaly',
                hover_name='Anomaly',
                zoom=1,
                mapbox_style='open-street-map',
                animation_frame=time_group_conversion[time_group],
            )
        elif plot_type == 'scatter map':
            fig = px.scatter_mapbox(
                anomaly_df,
                lat='latitude',
                lon='longitude',
                color='Anomaly',
                size='Anomaly',
                hover_name='Anomaly',
                zoom=1,
                mapbox_style='open-street-map',
                animation_frame=time_group_conversion[time_group],
            )
        elif plot_type == 'bar':
            fig = px.bar(anomaly_df, x=time_group_conversion[time_group], y='Anomaly', title=f'{time_group} Anomalies')
        elif plot_type == 'line':
            fig = px.line(anomaly_df, x=time_group_conversion[time_group], y='Anomaly', title=f'{time_group} Anomalies Trend')
        else:
            raise ValueError(f"Unknown plot type: {plot_type}")
        
        return fig