from django.http import HttpResponse
from django.shortcuts import render, redirect


from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required


from django.conf import settings

from .models import DiseasePrediction

def index(request):
    if request.user.is_authenticated:
        context = {'fname': request.user.first_name}
        return render(request, 'home.html', context)

    else:
        return render(request,'index.html')

def logo_redirect(request):
    return redirect('index')

def login_page(request):
    return render(request,'login.html')


def signup_page(request):
    return render(request,'signup.html')



from django.views.decorators.cache import never_cache, cache_control
# @login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def home(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Render the main page with a welcome message
        context = {'fname': request.user.first_name}
        return render(request, 'home.html', context)
    else:
        # Redirect to the login page if the user is not authenticated
        return redirect('login_page')



@login_required
def logout_view(request):
    auth.logout(request)
    return render(request, 'index.html')



def handler404(request, exception=None):
    return render(request, '404.html', status=404)




from django.shortcuts import render



@login_required
def history(request):
    user = request.user
    disease_predictions = DiseasePrediction.objects.filter(user=user).order_by('-created_at')
    context = {'disease_predictions': disease_predictions}
    return render(request, 'history.html', context)



def page_not_found_view(request, exception):
    return render(request, 'page_not_found.html', status=404)




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse
# from .tokens import account_activation_token
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

def signup(request):
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
        if first_name and not first_name.isalpha():
            errors['fname'] = 'First name should have only alphabetical letters!'
        if last_name and not last_name.isalpha():
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

        # Create the user object but don't save it yet
        user = User(username=username, email=email, first_name=first_name, last_name=last_name, is_active=False)

        # Set the password and save the user object
        user.set_password(password1)
        user.save()

        # Generate a unique URL for the user to confirm their email address
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_url = f"{settings.BASE_URL}/activate/{uid}/{token}/"

        # Send the email
        email_subject = 'Activate your account'
        # email_body = render_to_string('email_verification.html', {
        #     'user': user,
        #     'activation_url': activation_url,
        # })
        current_site = get_current_site(request)
        email_body = f"Hi {user.username},\n\nPlease click on the link below to activate your account:\n\nhttp://{current_site.domain}{activation_url}\n\nIf you did not request this registration, please disregard this email.\n\nBest regards,\nIdentification of Plant Disease Team"
        
        email = EmailMessage(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
        email.send()

        return render(request, 'login.html', {"successful": "You have successfully created an account. A verification email has been sent to your email address."})
    else:
        return render(request, 'signup.html')

from django.contrib.auth.tokens import default_token_generator

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'The activation link is invalid or has expired.')
        return redirect('signup')
    

    # from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from django.contrib.auth import authenticate, login as auth_login

def login(request):
    print("hello")
    if request.method == 'POST':
        # Retrieve the user inputs from the request object
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        print("Entering in login function")
        if user is not None:
            print("user authenticated")
            # Log in the user
            auth_login(request, user)
            return redirect('home')
        else:
            print("not authenticated")
            # Invalid credentials
            error = {"errorr": "Username or password didn't match"}
            return render(request, 'login.html', error)
    else:
        return render(request, 'login.html')






import os
import uuid
from django.utils import timezone



@login_required
def image_upload(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        print(request.FILES)
        print("image name is ",image)

        # Check if an image was uploaded
        if not image:
            error_message = "No Image was uploaded"
            context = {'error_message': error_message}
            return render(request, 'home.html', context)

        # Check if the file type is valid
        if not image.content_type.startswith('image/') or \
           not any(image.name.lower().endswith('.' + ext) for ext in ['png', 'jpg', 'jpeg']):
            return HttpResponse("Invalid image file type. Please upload a png, jpg or jpeg file.")

        try:
            # Try to open the image with Pillow
            img = Image.open(image)

            # Generate a unique filename and save the file to the media folder
            fname, ext = os.path.splitext(image.name)
            filename = str(timezone.now().timestamp()) + '_' + str(uuid.uuid4().hex) + ext
            with open(os.path.join('media', filename), 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            path = os.path.join(settings.MEDIA_ROOT, filename)

            predicted_disease = ""
            treatment, how_to_use = "", ""
            caution = classify_image(path)
            print(caution)
            if caution == "Plant":
                caution = ""
                img_array = preprocess_image(path)
                predicted_disease = model_return(img_array)
                print(predicted_disease)
                treatment, how_to_use = get_treatment_and_how_to_use(predicted_disease)
            else:
                caution = "Your uploaded photo doesn't seem to be a plant. Please Provide Plant Image(Only Leaf Image Recommended). "
                treatment = ""
                how_to_use = ""

            # Get the currently logged in user
            user = request.user

            # Create a new instance of the DiseasePrediction model and save the data
            disease_prediction = DiseasePrediction(user=user, image=filename, predicted_disease=predicted_disease,
                                                   treatment=treatment, how_to_use=how_to_use, caution=caution)
            disease_prediction.save()

            disease_predictions = DiseasePrediction.objects.filter(user=request.user).order_by('-created_at')[:1]
            fname = request.user.first_name
            context = {'disease_predictions': disease_predictions, 'fname':fname}
            return render(request, 'home.html', context)

        except UnidentifiedImageError:
            error_message = "The image file is corrupted or not supported. Please upload a valid image file."
            context = {'error_message': error_message}
            return render(request, 'home.html', context)

            

    return HttpResponse("Invalid request method")




@login_required
def take_photo(request):
    return render(request, 'take_photo.html')



# provides tools for working with Python's in-memory binary data streams
from io import BytesIO
# provides encoding and decoding functions for base64 data
import base64
import os
# library for generating universally unique identifiers (UUIDs)
import uuid

from PIL import Image

from tensorflow.keras.preprocessing import image as keras_image

import tensorflow as tf 

import numpy as np 






import pickle


ref_path = os.path.join(settings.MODEL_ROOT, 'ref.pickle')
treat_dict_path = os.path.join(settings.MODEL_ROOT, 'disease_dictionary.pickle')

with open(ref_path, 'rb') as f:
    disease_dict = pickle.load(f)

with open(treat_dict_path, 'rb') as f:
    use_treat_dict = pickle.load(f)





        

    
from django.core.files.base import ContentFile



from PIL import Image, UnidentifiedImageError

@login_required
def image_capture(request):
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

        try:
            # open the image from the binary data
            img = Image.open(BytesIO(binary_data))
        except UnidentifiedImageError:
            # handle the error by returning an error message to the user
            error_message = "The uploaded file is not a valid image file. Please upload a valid image file. OR your camera can be disable, please enable it."
            context = {'error_message': error_message}
            return render(request, 'take_photo.html', context)

        # Save the file to the media folder with a unique filename
        filename = str(timezone.now().timestamp()) + '_' + str(uuid.uuid4().hex) + '.jpg'
        with open(os.path.join(settings.MEDIA_ROOT, filename), 'wb+') as destination:
            img.save(destination, 'JPEG')

        # preprocess the image for prediction
        img_array = preprocess_image(os.path.join(settings.MEDIA_ROOT, filename))
        predicted_disease = model_return(img_array)
        print(predicted_disease)

        treatment, how_to_use = get_treatment_and_how_to_use(predicted_disease)
        
        caution= classify_image(os.path.join(settings.MEDIA_ROOT, filename))
        print(caution)
        if caution=="Plant":
            caution=""
        else:
            caution="Your uploaded photo doesn't seem to be a plant. Please Provide Plant Image(Only Leaf Image Recommended)."

        # Get the currently logged in user
        user = request.user

        # Create a new instance of the DiseasePrediction model and save the data
        disease_prediction = DiseasePrediction(user=user, image=filename, predicted_disease=predicted_disease, treatment=treatment, how_to_use=how_to_use,caution=caution)
        disease_prediction.save()

        disease_predictions = DiseasePrediction.objects.filter(user=request.user).order_by('-created_at')[:1]
        fname = request.user.first_name
        context = {'disease_predictions': disease_predictions}
        return render(request, 'take_photo.html', context)








from tensorflow.keras.preprocessing.image import load_img, img_to_array
def preprocess_image(image):
    # Preprocess the image for prediction
    img = load_img(image, target_size=(256, 256))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    img_array= x/255.0

    return img_array 


d_model= os.path.join(settings.MODEL_ROOT, 'best_model.h5')
p_model = os.path.join(settings.MODEL_ROOT, 'plant_classifier_model.h5')

model_d = tf.keras.models.load_model(d_model)
model_p = tf.keras.models.load_model(p_model) 
 
def model_return(image_array):
        
    # make a prediction using the model
    # Make a prediction using the trained model
    predictions = model_d.predict(image_array)
    # Get the index of the predicted class
    pred = np.argmax(predictions)
        
    print("Prediction index is", pred)
    # convert the predicted label to a string using the dictionary of labels
    prediction = disease_dict[pred] 
        
    confidence = round(100 * np.max(predictions), 2)
    print(confidence)
    return prediction




# Define the classify_image function
def classify_image(image_path):
    # Load the image
    img = load_img(image_path, target_size=(224, 224))
    # Convert the image to a numpy array
    img_array = img_to_array(img)
    # Reshape the array to match the input shape of the model
    img_array = img_array.reshape((1, 224, 224, 3))
    # Preprocess the image
    img_array = img_array / 255.0
    # Predict the class label
    prediction = model_p.predict(img_array)
    # Map the class label to a human-readable string
    print("plant or not plant",prediction)
    if prediction < 0.5:
        return 'Not a plant'
    else:
        return 'Plant'
    

def get_treatment_and_how_to_use(disease_name):
  treatment = use_treat_dict[disease_name]["Treatment"]
  how_to_use = use_treat_dict[disease_name].get("How to Use", "No information available.")
  return treatment, how_to_use



