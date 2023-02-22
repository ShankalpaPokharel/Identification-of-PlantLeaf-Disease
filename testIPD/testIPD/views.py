# provides tools for working with Python's in-memory binary data streams
from io import BytesIO
# provides encoding and decoding functions for base64 data
import base64
import os
# library for generating universally unique identifiers (UUIDs)
import uuid

from PIL import Image
import cv2
import numpy as np
import tensorflow as tf
import pickle

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect
from tensorflow.keras.preprocessing import image as keras_image

# Load the disease dictionary for predictions
disease_dict = pickle.load(open('testIPD/reference.pkl', 'rb'))

def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def SignUp(request):
    return render(request, 'SignUp.html')

# def handleSignup(request):
#     if request.method == 'POST': 
#         # Get the post parameters
#         username = request.POST['username']
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         pass1 = request.POST['pass1']
#         pass2 = request.POST['pass2']

#         # Check for erroneous input

#         # Create the user
#         myuser = User.objects.create_user(username, email, pass1)
#         myuser.first_name = fname
#         myuser.last_name = lname
#         myuser.save()
#         messages.success(request, "Your account has been successfully created")
#         return render(request, 'home.html')

#     else:
#         return HttpResponse('404 - Not Found')

def camera(request):
    return render(request, 'camera.html')

def preprocess_image(image):
    # Preprocess the image for prediction
    img = keras_image.load_img(image, target_size=(256, 256))
    x = keras_image.img_to_array(img)
    x = tf.keras.applications.mobilenet.preprocess_input(x)
    img_array = np.expand_dims(x, axis=0)
    return img_array

# Handel the upload Image
def upload_image(request):
    if request.method == 'POST':
        try:
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            image_path = fs.path(filename)

            # Load the trained model
            model = tf.keras.models.load_model("testIPD/best_model.h5")

            # Preprocess the image for prediction
            img_array = preprocess_image(image_path)

            # Make prediction using the model
            pred = np.argmax(model.predict(img_array))
            prediction = disease_dict[pred]

            return render(request, 'home.html', {'prediction': prediction})

        except KeyError:
            # Handle missing image error
            return HttpResponse("Please choose an image to upload.")

        except Exception as e:
            # Handle all other errors
            return HttpResponse("Error occurred during prediction: " + str(e))

    else:
        # Render upload form on GET request
        return render(request, 'home.html')


#Handel the camera capute image
def image_capture_view(request):
    if request.method == 'POST':
        # get the base64-encoded image data from the POST request
        image_data = request.POST.get('image_data')
        
        dataURL = image_data
        # remove the prefix and extract the encoded data
        encoded_data = dataURL.split(',')[1]
        # add padding to the encoded data if necessary
        padding_needed = len(encoded_data) % 4
        if padding_needed > 0:
            encoded_data += b'=' * (4 - padding_needed)
        # decode the base64-encoded data
        binary_data = base64.urlsafe_b64decode(encoded_data)
        # open the image from the binary data
        img = Image.open(BytesIO(binary_data))  
        # save the image to a temporary file
        temp_file = "temp.jpg"
        
        img.save(temp_file) 
        # preprocess the image for prediction
        img_array = preprocess_image(temp_file) 
        # load the trained model
        model = tf.keras.models.load_model("testIPD/best_model.h5") 
        # make a prediction using the model
        pred = np.argmax(model.predict(img_array))  
        # convert the predicted label to a string using the dictionary of labels
        prediction = disease_dict[pred] 
        # render the camera.html template with the prediction context
        context = {'prediction': prediction}
        return render(request, 'camera.html', context)









from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages





def loginn(request):
    print("hello")
    if request.method == 'POST':
        # Retrieve the user inputs from the request object
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = auth.authenticate(request, username=username, password=password)
        print("Entering in login fuction")
        if user is not None:
            print("user authencate")
            # Log in the user
            auth.login(request, user)
            return redirect('main')
        else:
            print("not authencate")
            # Invalid credentials
            error = {"errorr": "Username or password didn't match"}
            return render(request, 'login.html', error)
    else:
        return render(request, 'login.html')
        





from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def main(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Render the main page with a welcome message
        context = {'fname': request.user.first_name}
        return render(request, 'main.html', context)
    else:
        # Redirect to the login page if the user is not authenticated
        return redirect('login')





from django.contrib.auth import logout
# from django.views.decorators.cache import cache_control

# @never_cache
# def logout_view(request):
#     logout(request)
#     return redirect('login')

def logout_view(request):
    auth.logout(request)
    
    return redirect('login')




# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def logout_view(request):
#     logout(request)
#     response = redirect('login')
#     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#     response['Pragma'] = 'no-cache'
#     response['Expires'] = '0'
#     return response



def signupp(request):
    if request.method == 'POST':
        # Retrieve the user inputs from the request object
        username = request.POST.get('username')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        password1 = request.POST.get('pass1')
        password2 = request.POST.get('pass2')

        errors = {}
        if not username:
            errors['username'] = 'Username is required!'
        elif User.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists!'
        if not first_name.isalpha():
            errors['fname'] = 'First name should have only alphabetical letters!'
        if not last_name.isalpha():
            errors['lname'] = 'Last name should have only alphabetical letters!'
        if not email:
            errors['email'] = 'Email is required!'
        elif not '@' in email:
            errors['email'] = 'Email should be valid!'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'Email already exists!'
        if not password1:
            errors['pass1'] = 'Password is required!'
        elif len(password1) < 8:
            errors['pass1'] = 'Password must be at least 8 characters long!'
        if not password2:
            errors['pass2'] = 'Please confirm your password!'
        elif password1 != password2:
            errors['pass2'] = 'Passwords do not match!'



        # If there are errors, display them on the signup page
        if errors:
            return render(request, 'signup.html', {'errors': errors})

        # Create the user object
        user = User.objects.create_user(username=username, email=email, password=password1,
                                        first_name=first_name, last_name=last_name)
        # Log in the user after successful registration
        auth.login(request, user)
        messages.success(request, 'You are now registered and logged in!')
        return redirect('login')
    else:
        return render(request, 'signup.html')




def handler404(request, exception=None):
    return render(request, '404.html', status=404)