import numpy as np
import tensorflow as tf
from .anomaly_detector import AnomalyDetector


# Input Data
#     |
#     V
# [Encoder] -> [Encoded Representation] -> [Decoder] -> Reconstructed Data

# the reconstructed output should be very close to the original input for "normal" data. 
# However, for anomalous data that the model hasn't seen during training, 
# the reconstruction will likely have a higher error.

class AutoencoderAnomalyDetector(AnomalyDetector):

    def _specific_calculate(self, data_frame, variable=None, epochs=50, encoding_dim=3, **kwargs):
        if variable is None:
            raise ValueError("Variable to analyze is None")

        def detect_anomalies(group):
            # Prepare data
            X = group[variable].values.reshape(-1, 1)
            X = X.astype('float32')

            # Normalize data
            X = (X - np.min(X)) / (np.max(X) - np.min(X))

            # Build autoencoder model
            input_dim = X.shape[1]
            input_layer = tf.keras.layers.Input(shape=(input_dim,))
            encoder = tf.keras.layers.Dense(encoding_dim, activation="relu")(input_layer)
            decoder = tf.keras.layers.Dense(input_dim, activation='sigmoid')(encoder)
            autoencoder = tf.keras.Model(inputs=input_layer, outputs=decoder)

            autoencoder.compile(optimizer='adam', loss='mean_squared_error')

            # Train the model
            autoencoder.fit(X, X, epochs=epochs, shuffle=True, verbose=0)

            # Predict using the autoencoder
            predictions = autoencoder.predict(X)

            # Calculate the mean squared error for each data point
            mse = np.mean(np.power(X - predictions, 2), axis=1)

            # Label as 1 if anomaly, 0 if not
            threshold = np.quantile(mse, 0.99) 
            group['Anomaly'] = [-1 if e > threshold else 0 for e in mse]

            return group

        return data_frame.groupby(['latitude', 'longitude']).apply(detect_anomalies).reset_index(drop=True)
