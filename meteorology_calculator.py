from abc import ABC, abstractmethod
import pandas as pd
from datetime import datetime


class MeteorologyCalculator(ABC):

    @abstractmethod
    def calculate(self, df, date_range = None, time_group = 'daily', **kwargs):
        if time_group not in ["daily", "monthly", "yearly"]:
            raise ValueError("Invalid time_group value. Accepted values are 'daily', 'monthly', or 'yearly'")

        if(date_range is not None and date_range["start"] != "" and date_range["end"] != ""):
            print("filtering data")
            df = self.filter_by_date(df, date_range)

        return df
    
    @abstractmethod
    def plot(self, df, **kwargs):
        pass

    def filter_by_date(self, df, date_range):

        # # Convert date strings to datetime objects
        # start_date = datetime.strptime(date_range['start'], "%Y-%m-%d")
        # end_date = datetime.strptime(date_range['end'], "%Y-%m-%d")

        # if start_date > end_date:
        #     raise ValueError("Start date must be before or equal to end date")

        # # Create a 'date' column in the DataFrame
        # df['datetime'] = df.apply(lambda row: datetime(int(row['year']), int(row['month']), int(row['day'])), axis=1)


        # # Filter the data frame based on the date range
        # filtered_df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]

        # return filtered_df.drop(columns=['datetime'])

        start_date = pd.to_datetime(date_range['start'], format="%Y-%m-%d")
        end_date = pd.to_datetime(date_range['end'], format="%Y-%m-%d")

        # Creating a datetime column for filtering
        df['datetime'] = pd.to_datetime(df[['day', 'month', 'year']])
        
        # Filtering based on the date range
        filtered_df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)].drop(columns=['datetime'])
        
        return filtered_df