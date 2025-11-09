from django import forms

class PredictionForm(forms.Form):
    # Numeric features
    N = forms.FloatField(label="Nitrogen (N)")
    P = forms.FloatField(label="Phosphorus (P)")
    K = forms.FloatField(label="Potassium (K)")
    temperature = forms.FloatField(label="Temperature (°C)")
    humidity = forms.FloatField(label="Humidity (%)")
    ph = forms.FloatField(label="Soil pH")
    rainfall = forms.FloatField(label="Rainfall (mm)")

    # Crop selection (single)
    crop_choices = [
        ('banana', 'Banana'),
        ('blackgram', 'Blackgram'),
        ('chickpea', 'Chickpea'),
        ('coconut', 'Coconut'),
        ('coffee', 'Coffee'),
        ('cotton', 'Cotton'),
        ('grapes', 'Grapes'),
        ('jute', 'Jute'),
        ('kidneybeans', 'Kidney Beans'),
        ('lentil', 'Lentil'),
        ('maize', 'Maize'),
        ('mango', 'Mango'),
        ('mothbeans', 'Moth Beans'),
        ('mungbean', 'Mung Bean'),
        ('muskmelon', 'Muskmelon'),
        ('orange', 'Orange'),
        ('papaya', 'Papaya'),
        ('pigeonpeas', 'Pigeon Peas'),
        ('pomegranate', 'Pomegranate'),
        ('rice', 'Rice'),
        ('watermelon', 'Watermelon'),
    ]
    crop = forms.ChoiceField(choices=crop_choices, label="Crop")

    # Fertilizers (multiple)
    fertilizer_labels = [
        "Gypsum", "Lime", "MOP", "Potassium Nitrate", "Rhizobium",
        "Rock Phosphate", "SSP", "Urea"
    ]
    for fert in fertilizer_labels:
        locals()[f"fertilizer_{fert}"] = forms.BooleanField(required=False, label=fert)
