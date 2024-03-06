from abc import ABC, abstractmethod
import plotly.express as px
from ..meteorology_calculator import MeteorologyCalculator

class ZScore(MeteorologyCalculator, ABC):

    @abstractmethod
    def _specific_calculate(self, data_frame,  **kwargs):
        pass

    def calculate(self, data_frame, date_range=None,  time_group="daily",  **kwargs):
        data_frame = super().calculate(data_frame, date_range=date_range, time_group=time_group)
        
        result_df = self._specific_calculate(data_frame, **kwargs)
        
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

        # Filter out only rows with z-scores
        zscore_df = df[df['z_score'].notnull()]

        if plot_type == 'density map':
            zscore_df = zscore_df.groupby(['latitude', 'longitude', time_group_conversion[time_group]])['z_score'].mean().reset_index()

            zscore_df = zscore_df.sort_values(by=[time_group_conversion[time_group]])



            fig = px.density_mapbox(
                zscore_df,
                lat='latitude',
                lon='longitude',
                z='z_score',
                hover_name='z_score',
                zoom=1,
                mapbox_style='open-street-map',
                animation_frame=time_group_conversion[time_group],

            )
            fig.update_layout(
                title='Z-Score Density Map',
                xaxis_title='Longitude',
                yaxis_title='Latitude'
            )

        elif plot_type == 'scatter map':
            zscore_df = zscore_df.groupby(['latitude', 'longitude', time_group_conversion[time_group]])['z_score'].mean().reset_index()

            zscore_df = zscore_df.sort_values(by=[time_group_conversion[time_group]])


            fig = px.scatter_mapbox(
                zscore_df,
                lat='latitude',
                lon='longitude',
                color='z_score',
                size=abs(zscore_df['z_score']),
                hover_name='z_score',
                zoom=1,
                mapbox_style='open-street-map',
                color_continuous_scale=px.colors.sequential.Plasma,
                animation_frame=time_group_conversion[time_group],

            )
            fig.update_layout(
                title='Z-Score Scatter Map',
                xaxis_title='Longitude',
                yaxis_title='Latitude'
            )

        elif plot_type == 'bar':
            zscore_df = zscore_df.groupby([time_group_conversion[time_group]])['z_score'].mean().reset_index()
            fig = px.bar(zscore_df, x=time_group_conversion[time_group], y='z_score', title=f'Z-Score {time_group.capitalize()} Distribution')

        elif plot_type == 'line':
            zscore_df = zscore_df.groupby([time_group_conversion[time_group]])['z_score'].mean().reset_index()
            fig = px.line(zscore_df, x=time_group_conversion[time_group], y='z_score', title=f'Z-Score {time_group.capitalize()} Trend')

        else:
            raise ValueError(f"Unknown plot type: {plot_type}")

        return fig

        

    
   