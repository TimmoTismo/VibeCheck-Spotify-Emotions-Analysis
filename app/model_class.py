import pickle, pandas as pd
#from flask import session

# Model and Spotify API functions

class Model: 

    # Retrieve model predictions
    def predict(self, token):
        # Load in saved model
        clf = pickle.load(open('models/model.sav', 'rb'))

        # Getting songs from user
        songs = self.get_user_songs()

        # Storing data in dataframe
        user_data = pd.DataFrame(songs)

        # Drop unnecessary columns
        user = user_data.drop(columns=['duration_ms','datetime'])
        X_test = user.iloc[:, 2:13]
        
        # Rearrange columns in right order
        cols = X_test.columns.tolist()
        cols.sort()
        X_test = X_test[cols]


        # Predict
        # svm_predictions = svm_model_linear.predict(X_test)
        svm_predictions = clf.predict(X_test)
        
        
        return svm_predictions, user_data
