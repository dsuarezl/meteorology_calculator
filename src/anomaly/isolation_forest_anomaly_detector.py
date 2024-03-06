from .anomaly_detector import AnomalyDetector
from sklearn.ensemble import IsolationForest


#https://en.wikipedia.org/wiki/Isolation_forest
class IsolationForestAnomalyDetector(AnomalyDetector):

    def _specific_calculate(self, data_frame, contamination='auto', n_estimators=100, variable=None, **kwargs):
        if contamination is None:
            raise ValueError("Contamination not provided")
        else: contamination = float(contamination)

        if variable is None:
            raise ValueError("Variable to analyze is None")
        
        contamination = float(contamination)
        if(contamination == 0):
            contamination = 'auto'

  
        isolation_forest = IsolationForest(n_estimators=n_estimators, contamination=contamination)

        def detect_anomalies(group):
            # Reshape the input data to ensure it's 2D
            X = group[variable].values.reshape(-1, 1)
            group['Anomaly'] = isolation_forest.fit_predict(X)
            return group

        return data_frame.groupby(['latitude', 'longitude']).apply(detect_anomalies).reset_index(drop=True)
