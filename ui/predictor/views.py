from django.shortcuts import render
import joblib
import pandas as pd
import os

# Build the paths to the model files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'model')
MODEL_PATH = os.path.join(MODEL_DIR, 'crop_model_pipeline.joblib') # Use the RF pipeline
APP_DATA_PATH = os.path.join(MODEL_DIR, 'app_data_v2.joblib') # Use the v2 app data

# Load the model and app data
try:
    model_pipeline = joblib.load(MODEL_PATH)
    app_data = joblib.load(APP_DATA_PATH)
    
    all_regions = app_data['regions']
    all_soil_types = app_data['soil_types']
    all_crops = app_data['crops']
    all_weather = app_data['weather_conditions']
    
except FileNotFoundError as e:
    raise FileNotFoundError(f"Error loading files. Make sure 'crop_yield_random_forest_pipeline.joblib' and 'app_data_v2.joblib' are in {MODEL_DIR}") from e
except KeyError as e:
    raise KeyError(f"Error: {e} not found in app_data_v2.joblib. Please re-generate this file from your Colab notebook.")


def predict_view(request):
    prediction_result = None
    context = {
        'regions': all_regions,
        'soil_types': all_soil_types,
        'crops': all_crops,
        'weather_conditions': all_weather,
        'prediction': None,
        'submitted_data': {}
    }

    if request.method == 'POST':
        data = request.POST
        context['submitted_data'] = data.dict()

        try:
            # --- 1. Get all base data from the form ---
            
            # Categorical
            region = data.get('region')
            soil_type = data.get('soil_type')
            crop = data.get('crop')
            weather = data.get('weather')
            
            # Boolean -> convert to int (1 or 0)
            fertilizer = 1 if 'fertilizer' in data else 0
            irrigation = 1 if 'irrigation' in data else 0
            
            # Numerical
            rainfall = float(data.get('rainfall'))
            temp = float(data.get('temp'))
            days_harvest = int(data.get('days_harvest'))

            # --- 2. Create a DataFrame for the model ---
            # This must match the *base* features
            input_data = pd.DataFrame({
                'Region': [region],
                'Soil_Type': [soil_type],
                'Crop': [crop],
                'Rainfall_mm': [rainfall],
                'Temperature_Celsius': [temp],
                'Fertilizer_Used': [fertilizer],
                'Irrigation_Used': [irrigation],
                'Weather_Condition': [weather],
                'Days_to_Harvest': [days_harvest]
            })

            # --- 3. (THE FIX) Create the engineered features ---
            # These lines MUST be here to match the features your model was trained on
            # This is what solves the "columns are missing" error
            if 'Temp_sq' in model_pipeline.named_steps['preprocessor'].feature_names_in_:
                input_data['Temp_sq'] = input_data['Temperature_Celsius']**2
            if 'Rainfall_sq' in model_pipeline.named_steps['preprocessor'].feature_names_in_:
                input_data['Rainfall_sq'] = input_data['Rainfall_mm']**2
            if 'Rainfall_x_Temp' in model_pipeline.named_steps['preprocessor'].feature_names_in_:
                input_data['Rainfall_x_Temp'] = input_data['Rainfall_mm'] * input_data['Temperature_Celsius']
            if 'Fert_x_Irrig' in model_pipeline.named_steps['preprocessor'].feature_names_in_:
                input_data['Fert_x_Irrig'] = input_data['Fertilizer_Used'] * input_data['Irrigation_Used']

            # --- 4. Make prediction ---
            # The pipeline will handle preprocessing and prediction
            prediction = model_pipeline.predict(input_data)
            
            prediction_result = f"{prediction[0]:,.2f} tons/hectare"
            context['prediction'] = prediction_result
        
        except Exception as e:
            # This will catch any other errors, like a mismatch in column names
            context['error'] = f"An error occurred during prediction: {e}"

    return render(request, 'predictor/predict.html', context)