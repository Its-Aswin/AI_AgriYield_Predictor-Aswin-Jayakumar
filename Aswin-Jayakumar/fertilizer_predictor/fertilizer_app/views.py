import joblib
import numpy as np
from django.shortcuts import render
from .forms import PredictionForm
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'ml_model', 'random_forest_model.pkl')
model = joblib.load(MODEL_PATH)

def predict_view(request):
    prediction = None

    if request.method == "POST":
        form = PredictionForm(request.POST)
        if form.is_valid():
            # Get numeric inputs
            N = form.cleaned_data['N']
            P = form.cleaned_data['P']
            K = form.cleaned_data['K']
            temperature = form.cleaned_data['temperature']
            humidity = form.cleaned_data['humidity']
            ph = form.cleaned_data['ph']
            rainfall = form.cleaned_data['rainfall']

            # Calculate interaction features (from your EDA)
            N_temp = N * temperature
            P_humidity = P * humidity
            K_rainfall = K * rainfall

            # Start building the input list
            data = [N, P, K, temperature, humidity, ph, rainfall]

            # --- One-hot encode crop selection ---
            crops = [
                'banana', 'blackgram', 'chickpea', 'coconut', 'coffee', 'cotton',
                'grapes', 'jute', 'kidneybeans', 'lentil', 'maize', 'mango',
                'mothbeans', 'mungbean', 'muskmelon', 'orange', 'papaya',
                'pigeonpeas', 'pomegranate', 'rice', 'watermelon'
            ]
            selected_crop = form.cleaned_data['crop']
            for crop in crops:
                data.append(1.0 if crop == selected_crop else 0.0)

            # --- One-hot encode fertilizers ---
            fertilizers = [
                "Gypsum", "Lime", "MOP", "Potassium Nitrate", "Rhizobium",
                "Rock Phosphate", "SSP", "Urea"
            ]
            for fert in fertilizers:
                data.append(1.0 if form.cleaned_data.get(f"fertilizer_{fert}") else 0.0)

            # Append the interaction features (EDA features)
            data.extend([N_temp, P_humidity, K_rainfall])

            # Convert to numpy 2D array
            X_input = np.array(data).reshape(1, -1)
            prediction = model.predict(X_input)[0]

    else:
        form = PredictionForm()

    return render(request, "predict.html", {"form": form, "prediction": prediction})
