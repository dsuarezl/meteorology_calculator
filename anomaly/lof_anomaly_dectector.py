from .anomaly_detector import AnomalyDetector
from sklearn.neighbors import LocalOutlierFactor  

class LOFAnomalyDetector(AnomalyDetector):

    def _specific_calculate(self, data_frame, contamination='auto', n_neighbors=20, variable=None, **kwargs):
 
        if contamination is None:
            raise ValueError("Contamination not provided")
        else: contamination = float(contamination)

        if variable is None:
            raise ValueError("Variable to analyze is None")
        
        
        contamination = float(contamination)
        if(contamination == 0):
            contamination = 'auto'
  

        lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)

        def detect_anomalies(group):
            #Reshape the input data to ensure its 2D
            X = group[variable].values.reshape(-1, 1)
            group['Anomaly'] = lof.fit_predict(X)
            return group

        return  data_frame.groupby(['latitude', 'longitude']).apply(detect_anomalies).reset_index(drop=True)
    


