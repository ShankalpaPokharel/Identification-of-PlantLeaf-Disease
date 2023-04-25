from django.http import HttpResponse
from django.shortcuts import render, redirect


from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .models import DiseasePrediction

def index(request):
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
        email_body = f"Hi {user.username},\n\nPlease click on the link below to activate your account:\n\nhttp://{current_site.domain}{activation_url}\n\nIf you did not request this registration, please disregard this email.\n\nBest regards,\nThe Website Team"
        
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

# @login_required
# def image_upload(request):
#     if request.method == 'POST':

#         print(request.FILES)

#         image = request.FILES.get('image')  # Use request.FILES to get the uploaded file data

#         print("image name si ", image)

#         predicted_disease = "disease1" # Replace with your prediction logic
#         treatment = "Fungicides such as azoxystrobin, propiconazole, or chlorothalonil can be used to control cercospora leaf spot. " # Replace with your prediction logic
#         how_to_use = "Mix the fungicide with water according to the manufacturer's instructions and apply it evenly to the tree's foliage and fruit using a sprayer or other suitable equipment. It's best to apply the fungicide before the onset of infection, and repeat every 7-14 days as necessary." # Replace with your prediction logic


       

#         if image:  # Check if an image was uploaded
#             fname, ext = os.path.splitext(image.name)
#             filename = str(timezone.now().timestamp()) + '_' + str(uuid.uuid4().hex) + ext

#             # Save the file to the media folder with a unique filename
#             with open(os.path.join('media', filename), 'wb+') as destination:
#                 for chunk in image.chunks():
#                     destination.write(chunk)

#             # Get the currently logged in user
#             user = request.user

#             # Create a new instance of the DiseasePrediction model and save the data
#             disease_prediction = DiseasePrediction(user=user, image=filename, predicted_disease=predicted_disease, treatment=treatment, how_to_use=how_to_use)
#             disease_prediction.save()

#             disease_predictions = DiseasePrediction.objects.filter(user=request.user).order_by('-created_at')[:1]
#             fname = request.user.first_name
#             context = {'disease_predictions': disease_predictions, 'fname':fname}
#             return render(request, 'home.html', context)
#         else: 
#             return HttpResponse("Image not found")

    


@login_required
def image_upload(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        print(request.FILES)
        print("image name is ",image)
        predicted_disease = "disease1" 
        # Replace with your prediction logic
        treatment = "Fungicides such as azoxystrobin, propiconazole, or chlorothalonil can be used to control cercospora leaf spot. " # Replace with your prediction logic
        how_to_use = "Mix the fungicide with water according to the manufacturer's instructions and apply it evenly to the tree's foliage and fruit using a sprayer or other suitable equipment. It's best to apply the fungicide before the onset of infection, and repeat every 7-14 days as necessary." # Replace with your prediction logic


        if image and image.content_type.startswith('image/'):
            try:
                fname, ext = os.path.splitext(image.name)
                filename = str(timezone.now().timestamp()) + '_' + str(uuid.uuid4().hex) + ext

                # Save the file to the media folder with a unique filename
                with open(os.path.join('media', filename), 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

                # Get the currently logged in user
                user = request.user

                # Create a new instance of the DiseasePrediction model and save the data
                disease_prediction = DiseasePrediction(user=user, image=filename, predicted_disease=predicted_disease, treatment=treatment, how_to_use=how_to_use)
                disease_prediction.save()

                disease_predictions = DiseasePrediction.objects.filter(user=request.user).order_by('-created_at')[:1]
                fname = request.user.first_name
                context = {'disease_predictions': disease_predictions, 'fname':fname}
                return render(request, 'home.html', context)

            except Exception as e:
                return HttpResponse(f"Error uploading file: {str(e)}")
        else: 
            return HttpResponse("Please upload an image file")
    
    return HttpResponse("Invalid request method")





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
        return render(request, 'take_photo.html', context)
