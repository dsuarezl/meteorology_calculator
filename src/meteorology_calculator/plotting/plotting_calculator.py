from abc import ABC, abstractmethod
import plotly.express as px
from ..meteorology_calculator import MeteorologyCalculator

class PlottingCalculator(MeteorologyCalculator):


    def calculate(self, data_frame, date_range=None,  time_group="daily", variable = "Heatwave", **kwargs):
        data_frame = super().calculate(data_frame, date_range=date_range, time_group=time_group)
    
        return data_frame
    

    def plot(self, df, plot_type=None, time_group = None, **kwargs):
        if(plot_type is None):
            raise ValueError("No plot type set")
        
        
        if plot_type == 'density map':
            # Directly use df without summing data or sorting by time group
            fig = px.density_mapbox(
                df,
                lat='latitude',
                lon='longitude',
                z='rwi',
                hover_name='rwi',
                zoom=1,
                mapbox_style='open-street-map',
            )
            fig.update_layout(
                title='RWI Map',
                xaxis_title='Longitude',
                yaxis_title='Latitude'
            )

        elif plot_type == 'scatter map':
            offset = abs(min(df['rwi'])) + 1  # Ensure all values are positive by adding 1 more than the absolute minimum
            df['rwi_adjusted'] = df['rwi'] + offset
            fig = px.scatter_mapbox(
                df,
                lat='latitude',
                lon='longitude',
                color='rwi',
                size='rwi_adjusted',
                hover_name='rwi',
                zoom=1,
                mapbox_style='open-street-map',
            )
            fig.update_layout(
                title='RWI Scatter Map',
                xaxis_title='Longitude',
                yaxis_title='Latitude'
            )

        elif plot_type == 'fixed size scatter map':
            offset = abs(min(df['rwi'])) + 1  # Ensure all values are positive by adding 1 more than the absolute minimum
            df['rwi_adjusted'] = df['rwi'] + offset
            fig = px.scatter_mapbox(
                df,
                lat='latitude',
                lon='longitude',
                color='rwi',
                size='rwi_adjusted',

                hover_name='rwi',
                zoom=1,
                mapbox_style='open-street-map',
            )
            fig.update_traces(marker=dict(size=10))
            fig.update_layout(
                title='RWI Rectangle Map',
                xaxis_title='Longitude',
                yaxis_title='Latitude'
            )

        elif plot_type == 'bar':
            # Example of a bar plot; adjust grouping/aggregation as needed
            fig = px.bar(df, x='YourXAxisColumn', y='rwi', title='RWI Bar Plot')

        elif plot_type == 'line':
            # Example of a line plot; adjust grouping/aggregation as needed
            fig = px.line(df, x='YourXAxisColumn', y='rwi', title='RWI Trend Line')

        else:
            raise ValueError(f"Unknown plot type: {plot_type}")
        
        return fig
