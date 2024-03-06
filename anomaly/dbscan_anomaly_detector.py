from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from .anomaly_detector import AnomalyDetector

class DBSCANAnomalyDetector(AnomalyDetector):

    def _specific_calculate(self, data_frame, variable=None, eps=0.5, min_samples=5, **kwargs):
        if variable is None:
            raise ValueError("Variable to analyze is None")

        def detect_anomalies(group):
            X = group[variable].values.reshape(-1, 1)
            X = StandardScaler().fit_transform(X)

            # Apply DBSCAN
            db = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
            labels = db.labels_

            # Label anomalies as 1, and non-anomalies as 0
            group['Anomaly'] = [-1 if label == -1 else 0 for label in labels]
            return group

        return data_frame.groupby(['latitude', 'longitude']).apply(detect_anomalies).reset_index(drop=True)
