from django.shortcuts import render, redirect
import tensorflow as tf
import numpy as np
from .forms import ImageUploadForm
from .models import upload
from django.core.files.storage import default_storage
from django.conf import settings

# Load the trained model
MODEL_PATH = r"C:\Users\bandi\plantdisease.keras"
model = tf.keras.models.load_model(MODEL_PATH)

# Define class labels
classes = [
    'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy',
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
    'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight',
    'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus',
    'Tomato_healthy'
]

def predict_image(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(256, 256)) 
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    predicted_class = classes[np.argmax(prediction)]
    confidence = np.max(prediction) * 100

    return predicted_class, confidence

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_instance = form.save()  
            file_path = uploaded_instance.image.path  

            predicted_class, confidence = predict_image(file_path)

            image_url = settings.MEDIA_URL + uploaded_instance.image.name

            return render(request, 'result.html', {
                'class_name': predicted_class, 
                'confidence': confidence, 
                'image_url': image_url
            })

    else:
        form = ImageUploadForm()

    return render(request, 'index.html', {'form': form})
