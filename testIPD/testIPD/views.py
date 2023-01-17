
from django.shortcuts import render
from django.http import HttpResponse
import tensorflow as tf
import numpy as np

from django.core.files.storage import FileSystemStorage
import pickle
disease_dict = pickle.load(open('testIPD/reference.pkl', 'rb'))

from io import BytesIO

def upload_image(request):
    if request.method == 'POST' :
        image = request.FILES['image']
        fs = FileSystemStorage()
        fs.save(image.name, image)
        # image = str(image)

        # print("img type" + type(image))

        imagee = "/Users/shankalpapokharel/Django_Course/testfileupload/testIPD/"+str(image)


        model = tf.keras.models.load_model("testIPD/best_model.h5")
        img = tf.keras.preprocessing.image.load_img(imagee, target_size=(256, 256))
        x = tf.keras.preprocessing.image.img_to_array(img)
        x = tf.keras.applications.mobilenet.preprocess_input(x)
        img = np.expand_dims(x, axis =0)
        pred = np.argmax(model.predict(img))
        predictio = disease_dict[pred]

        predictionn = {"prediction" : predictio}

        # print(f"The image belongs to {disease_dict[pred]}")
        

        return render(request, 'home.html',predictionn)
    else:
        return render(request, 'home.html')

def home(request):
    return render(request, 'home.html' )

def login(request):
    return render(request, 'login.html')

def SignUp(request):
    return render(request, 'SignUp.html')




# /Users/shankalpapokharel/Django_Course/testfileupload/testIPD/AppleCedarRust1.JPG