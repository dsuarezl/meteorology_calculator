from abc import ABC, abstractmethod
import plotly.express as px
from ..meteorology_calculator import MeteorologyCalculator

class HeatWaveCalculator(MeteorologyCalculator, ABC):

    @abstractmethod
    def _specific_calculate(self, data_frame, consecutive_days, **kwargs):
        pass

    def calculate(self, data_frame, date_range=None, consecutive_days=None,  time_group="daily", **kwargs):
        data_frame = super().calculate(data_frame, date_range=date_range, time_group=time_group)
    
        consecutive_days = int(consecutive_days)
        
        result_df = self._specific_calculate(data_frame, consecutive_days, **kwargs)

        return result_df
    

    def plot(self, df, plot_type="scatter map", time_group = "daily", **kwargs):
        if(plot_type is None):
            raise ValueError("No plot type set")
        
        
        if(time_group is None):
            raise ValueError("No time group type set")
        
        time_group_conversion = {   
            "daily" : "day",
            "monthly" : "month",
            "yearly" : "year"
         }

        
        heatwave_df = df[df['Heatwave'] >= 1]

        if plot_type == 'density map':
            heatwave_df = heatwave_df.groupby(['latitude', 'longitude', time_group_conversion[time_group]])['Heatwave'].sum().reset_index()
            heatwave_df = heatwave_df.sort_values(by=[time_group_conversion[time_group]])
            fig = px.density_mapbox(
                heatwave_df,
                lat='latitude',
                lon='longitude',
                z = 'Heatwave',
                hover_name='Heatwave',
                zoom=1,
                mapbox_style='open-street-map',
                animation_frame=time_group_conversion[time_group],
            )
            fig.update_layout(
                title='Heatwave Map',
                xaxis_title='Longitude',
                yaxis_title='Latitude'
            )
        elif plot_type == 'scatter map':
            # heatwave_df = heatwave_df.groupby(['latitude', 'longitude'])['Heatwave'].sum().reset_index()

            heatwave_df = heatwave_df.groupby(['latitude', 'longitude', time_group_conversion[time_group]])['Heatwave'].sum().reset_index()
            heatwave_df = heatwave_df.sort_values(by=[time_group_conversion[time_group]])

            fig = px.scatter_mapbox(
                heatwave_df,
                lat='latitude',
                lon='longitude',
                color='Heatwave',
                size='Heatwave',
                hover_name='Heatwave',
                zoom=1,
                mapbox_style='open-street-map',
                animation_frame=time_group_conversion[time_group],
                # animation_group=time_group_conversion[time_group],
 

            )

            # fig.update_traces(marker=dict(symbol='square', size=120))


            fig.update_layout(
                title='Heatwave Map',
                xaxis_title='Longitude',
                yaxis_title='Latitude'
            )

        elif plot_type == 'rectangle map':
            # heatwave_df = heatwave_df.groupby(['latitude', 'longitude'])['Heatwave'].sum().reset_index()

            heatwave_df = heatwave_df.groupby(['latitude', 'longitude', time_group_conversion[time_group]])['Heatwave'].sum().reset_index()
            heatwave_df = heatwave_df.sort_values(by=[time_group_conversion[time_group]])

            fig = px.scatter_mapbox(
                heatwave_df,
                lat='latitude',
                lon='longitude',
                color='Heatwave',
                size='Heatwave',
                hover_name='Heatwave',
                zoom=1,
                mapbox_style='open-street-map',
                animation_frame=time_group_conversion[time_group],
                # animation_group=time_group_conversion[time_group],

            )

            fig.update_layout(
                title='Heatwave Map',
                xaxis_title='Longitude',
                yaxis_title='Latitude'
            )
        elif plot_type == 'bar':
            heatwave_df = heatwave_df.groupby([ time_group_conversion[time_group]])['Heatwave'].sum().reset_index()
            fig = px.bar(heatwave_df, x=time_group_conversion[time_group], y='Heatwave', title=f'{time_group} Heatwaves')

        elif plot_type == 'line':
            heatwave_df = heatwave_df.groupby([ time_group_conversion[time_group]])['Heatwave'].sum().reset_index()
            fig = px.line(heatwave_df, x=time_group_conversion[time_group], y='Heatwave', title=f'{time_group} Heatwaves Trend')

        else:
            raise ValueError(f"Unknown plot type: {plot_type}")
        
        return fig
