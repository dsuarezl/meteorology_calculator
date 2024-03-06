from .anomaly_detector import AnomalyDetector
from sklearn.svm import OneClassSVM

class OneClassSVMAnomalyDetector(AnomalyDetector):

    def _specific_calculate(self, data_frame, nu=0.1, kernel='rbf', variable=None, **kwargs):
        """
        nu : float, default=0.1
            An upper bound on the fraction of margin errors and a lower bound of the fraction of support vectors.
            Should be in the interval (0, 1].
        
        kernel : string, default='rbf'
            Specifies the kernel type to be used in the algorithm.
            It must be one of ‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’ or a callable.
        """
        
        if variable is None:
            raise ValueError("Variable to analyze is None")

        # Initialize One-Class SVM
        oc_svm = OneClassSVM(nu=nu, kernel=kernel)

        def detect_anomalies(group):
            # Reshape the input data to ensure it's 2D
            X = group[variable].values.reshape(-1, 1)
            group['Anomaly'] = oc_svm.fit_predict(X)
            return group

        return data_frame.groupby(['latitude', 'longitude']).apply(detect_anomalies).reset_index(drop=True)
