from abc import ABC, abstractmethod
import plotly.express as px
from ..meteorology_calculator import MeteorologyCalculator

class ColdWaveCalculator(MeteorologyCalculator, ABC):

    @abstractmethod
    def _specific_calculate(self, data_frame, consecutive_days, **kwargs):
        pass

    def calculate(self, data_frame, date_range=None, consecutive_days=None, time_group="daily", **kwargs):
        data_frame = super().calculate(data_frame, date_range=date_range, time_group=time_group)
        consecutive_days = int(consecutive_days)
        result_df = self._specific_calculate(data_frame, consecutive_days, **kwargs)
        return result_df

    def plot(self, df, plot_type="scatter map", time_group="daily", **kwargs):
        if plot_type is None:
            raise ValueError("No plot type set")
        if time_group is None:
            raise ValueError("No time group type set")

        time_group_conversion = {"daily": "day", "monthly": "month", "yearly": "year"}
        coldwave_df = df[df['Coldwave'] >= 1]

        if plot_type == 'density map':
            coldwave_df = coldwave_df.groupby(['latitude', 'longitude', time_group_conversion[time_group]])['Coldwave'].sum().reset_index()
            coldwave_df = coldwave_df.sort_values(by=[time_group_conversion[time_group]])
            fig = px.density_mapbox(
                coldwave_df,
                lat='latitude',
                lon='longitude',
                z='Coldwave',
                hover_name='Coldwave',
                zoom=1,
                mapbox_style='open-street-map',
                animation_frame=time_group_conversion[time_group],
            )
            fig.update_layout(
                title='Coldwave Map',
                xaxis_title='Longitude',
                yaxis_title='Latitude'
            )

        elif plot_type == 'scatter map':
            coldwave_df = coldwave_df.groupby(['latitude', 'longitude', time_group_conversion[time_group]])['Coldwave'].sum().reset_index()
            coldwave_df = coldwave_df.sort_values(by=[time_group_conversion[time_group]])
            fig = px.scatter_mapbox(
                coldwave_df,
                lat='latitude',
                lon='longitude',
                color='Coldwave',
                size='Coldwave',
                hover_name='Coldwave',
                zoom=1,
                mapbox_style='open-street-map',
                animation_frame=time_group_conversion[time_group],
            )
            fig.update_layout(
                title='Coldwave Map',
                xaxis_title='Longitude',
                yaxis_title='Latitude'
            )

        elif plot_type == 'bar':
            coldwave_df = coldwave_df.groupby([time_group_conversion[time_group]])['Coldwave'].sum().reset_index()
            fig = px.bar(coldwave_df, x=time_group_conversion[time_group], y='Coldwave', title=f'{time_group} Coldwaves')

        elif plot_type == 'line':
            coldwave_df = coldwave_df.groupby([time_group_conversion[time_group]])['Coldwave'].sum().reset_index()
            fig = px.line(coldwave_df, x=time_group_conversion[time_group], y='Coldwave', title=f'{time_group} Coldwaves Trend')

        else:
            raise ValueError(f"Unknown plot type: {plot_type}")

        return fig
