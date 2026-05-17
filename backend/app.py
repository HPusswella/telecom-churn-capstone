from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

# 1. Initialize Flask App
app = Flask(__name__)
CORS(app) # Frontend eken ena requests allow karanna meka oni

print("Loading ML models and preprocessors...")
# 2. Load Models (Ara save karapu files 3 load karagannawa)
model = joblib.load('churn_prediction_model.pkl')
scaler = joblib.load('scaler.pkl')
model_columns = joblib.load('model_columns.pkl')
print("✅ Models loaded successfully!")

# 3. Base Route (Meken balanne server eka wada da kiyala)
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Telecom Churn Prediction API is Running!"})

# 4. Predict Route (Frontend eken data enne mekata)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # User form eke fill karana data tika JSON widiyata gannawa
        data = request.json
        
        # E data tika Pandas DataFrame (table) ekakata harawanawa
        input_df = pd.DataFrame([data])
        
        # Data Encoding & Alignment (Training data wala order ekatama hadagannawa)
        input_encoded = pd.get_dummies(input_df)
        input_aligned = input_encoded.reindex(columns=model_columns, fill_value=0)
        
        # Scaling (Data normalize karanawa)
        input_scaled = scaler.transform(input_aligned)
        
        # Prediction eka gannawa
        prediction = model.predict(input_scaled)
        
        # Result eka text ekak widiyata hadanawa
        if prediction[0] == 1:
            result = "Yes, this customer is likely to Churn."
        else:
            result = "No, this customer is likely to stay."
            
        return jsonify({'prediction': result})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Server eka port 5000 eken run wenawa
    app.run(debug=True, port=5000)