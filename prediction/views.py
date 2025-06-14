import os
import pickle
import numpy as np
from django.shortcuts import render
from django.conf import settings

def load_model_and_scaler():
    MODEL_PATH = os.path.join(settings.BASE_DIR, 'prediction', 'model.pkl')
    SCALER_PATH = os.path.join(settings.BASE_DIR, 'prediction', 'scaler.pkl')
    if not (os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH)):
        return None, None
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

def home(request):
    return render(request, 'prediction/index.html')

def submit(request):
    prediction = None
    model, scaler = load_model_and_scaler()
    if model is None or scaler is None:
        return render(request, 'prediction/prediction.html', {'result': "Model or Scaler not found! Please train and copy model.pkl and scaler.pkl."})

    if request.method == 'POST':
        gender = int(request.POST['gender'])
        ssc_p = float(request.POST['ssc_p'])
        ssc_b_Central = int(request.POST['ssc_b'])
        hsc_p = float(request.POST['hsc_p'])
        hsc_b_Central = int(request.POST['hsc_b'])
        hsc_s = request.POST['hsc_s']
        if hsc_s == "Commerce":
            commerce = 1
            science = 0
        elif hsc_s == "Science":
            commerce = 0
            science = 1
        else:
            commerce = 0
            science = 0
        degree_p = float(request.POST['degree_p'])
        degree_t = request.POST['degree_t']
        if degree_t == "Sci&Tech":
            other = 0
            scitech = 1
        elif degree_t == "Comm&Mgmt":
            other = 0
            scitech = 0
        else:
            other = 1
            scitech = 0
        workex = int(request.POST['workex'])
        etest_p = float(request.POST['etest_p'])
        specialisation = int(request.POST['specialisation'])
        mba_p = float(request.POST['mba_p'])
        status = int(request.POST['status'])

        features = np.array([
            commerce, science, other, scitech, gender, ssc_p, hsc_p, degree_p,
            workex, etest_p, mba_p, status, ssc_b_Central, hsc_b_Central, specialisation
        ]).reshape(1, -1)
        scaled = scaler.transform(features)
        prediction = round(model.predict(scaled)[0], 2)
        if prediction < 0:
            prediction = 0

    return render(request, 'prediction/prediction.html', {'result': prediction})