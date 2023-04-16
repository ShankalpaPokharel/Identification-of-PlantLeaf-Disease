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



# def signup(request):
#     if request.method == 'POST':
#         # Retrieve the user inputs from the request object
#         username = request.POST.get('username')
#         first_name = request.POST.get('fname')
#         last_name = request.POST.get('lname')
#         email = request.POST.get('email')
#         password1 = request.POST.get('pass1')
#         password2 = request.POST.get('pass2')

#         errors = {}
#         if not username:
#             errors['username'] = 'Username is required!'
#         elif User.objects.filter(username=username).exists():
#             errors['username'] = 'Username already exists!'
#         if first_name and not first_name.isalpha():
#             errors['fname'] = 'First name should have only alphabetical letters!'
#         if last_name and not last_name.isalpha():
#             errors['lname'] = 'Last name should have only alphabetical letters!'
#         if not email:
#             errors['email'] = 'Email is required!'
#         elif not '@' in email:
#             errors['email'] = 'Email should be valid!'
#         elif User.objects.filter(email=email).exists():
#             errors['email'] = 'Email already exists!'
#         if not password1:
#             errors['pass1'] = 'Password is required!'
#         elif len(password1) < 8:
#             errors['pass1'] = 'Password must be at least 8 characters long!'
#         if not password2:
#             errors['pass2'] = 'Please confirm your password!'
#         elif password1 != password2:
#             errors['pass2'] = 'Passwords do not match!'



#         # If there are errors, display them on the signup page
#         if errors:
#             return render(request, 'signup.html', {'errors': errors})
#             #  return render(request, 'login.html', {"successful": "You are now registered and logged in!"})

#         # Create the user object
#         user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
#         return render(request, 'login.html', {"successful": "You have successfully created an account. You can now login and start exploring our platform."})
#     else:
#         return render(request, 'signup.html')




# def login(request):
#     print("hello")
#     if request.method == 'POST':
#         # Retrieve the user inputs from the request object
#         username = request.POST['username']
#         password = request.POST['password']

#         # Authenticate the user
#         user = auth.authenticate(request, username=username, password=password)
#         print("Entering in login fuction")
#         if user is not None:
#             print("user authencate")
#             # Log in the user
#             auth.login(request, user)
#             return redirect('home')
#         else:
#             print("not authencate")
#             # Invalid credentials
#             error = {"errorr": "Username or password didn't match"}
#             return render(request, 'login.html', error)
#     else:
#         return render(request, 'login.html')



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

# @login_required
# def image_upload(request):
#     if request.method == 'POST':
#         image = request.FILES.get('image')



#         predicted_disease = "disease1" # Replace with your prediction logic
#         treatment = "Fungicides such as azoxystrobin, propiconazole, or chlorothalonil can be used to control cercospora leaf spot. " # Replace with your prediction logic
#         how_to_use = "Mix the fungicide with water according to the manufacturer's instructions and apply it evenly to the tree's foliage and fruit using a sprayer or other suitable equipment. It's best to apply the fungicide before the onset of infection, and repeat every 7-14 days as necessary." # Replace with your prediction logic
        





#         fname = request.user.first_name
#         # Get the currently logged in user
#         user = request.user

#         # Create a new instance of the DiseasePrediction model and save the data
#         disease_prediction = DiseasePrediction(user=user, image=image, predicted_disease=predicted_disease, treatment=treatment, how_to_use=how_to_use)
#         disease_prediction.save()

#         disease_predictions = DiseasePrediction.objects.filter(user=request.user).order_by('-created_at')[:1]
#         context = {'disease_predictions': disease_predictions, 'fname':fname}
#         return render(request, 'home.html', context)
       

# @login_required
# def history(request):
#     disease_predictions = DiseasePrediction.objects.all().order_by('-created_at')
#     context = {'disease_predictions': disease_predictions}
#     return render(request, 'history.html', context)

@login_required
def history(request):
    user = request.user
    disease_predictions = DiseasePrediction.objects.filter(user=user).order_by('-created_at')
    context = {'disease_predictions': disease_predictions}
    return render(request, 'history.html', context)



def page_not_found_view(request, exception):
    return render(request, 'page_not_found.html', status=404)







# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.sites.shortcuts import get_current_site
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes

# def signup(request):
#     if request.method == 'POST':
#         # Retrieve the user inputs from the request object
#         username = request.POST.get('username')
#         first_name = request.POST.get('fname')
#         last_name = request.POST.get('lname')
#         email = request.POST.get('email')
#         password1 = request.POST.get('pass1')
#         password2 = request.POST.get('pass2')

#         errors = {}
#         if not username:
#             errors['username'] = 'Username is required!'
#         elif User.objects.filter(username=username).exists():
#             errors['username'] = 'Username already exists!'
#         if first_name and not first_name.isalpha():
#             errors['fname'] = 'First name should have only alphabetical letters!'
#         if last_name and not last_name.isalpha():
#             errors['lname'] = 'Last name should have only alphabetical letters!'
#         if not email:
#             errors['email'] = 'Email is required!'
#         elif not '@' in email:
#             errors['email'] = 'Email should be valid!'
#         elif User.objects.filter(email=email).exists():
#             errors['email'] = 'Email already exists!'
#         if not password1:
#             errors['pass1'] = 'Password is required!'
#         elif len(password1) < 8:
#             errors['pass1'] = 'Password must be at least 8 characters long!'
#         if not password2:
#             errors['pass2'] = 'Please confirm your password!'
#         elif password1 != password2:
#             errors['pass2'] = 'Passwords do not match!'

#         # If there are errors, display them on the signup page
#         if errors:
#             return render(request, 'signup.html', {'errors': errors})

#         # Create the user object
#         user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)

#         # Generate verification token and save it to user object
#         verification_token = default_token_generator.make_token(user)
#         user.verification_token = verification_token
#         user.save()

#         # Send verification email
#         current_site = get_current_site(request)
#         mail_subject = 'Activate your account.'
#         message = render_to_string('email_verification.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': verification_token,
#         })
#         to_email = email
#         email = EmailMessage(
#             mail_subject, message, to=[to_email]
#         )
#         email.send()

#         return render(request, 'login.html', {"successful": "You have successfully created an account. Please check your email for a verification link."})
#     else:
#         return render(request, 'signup.html')




# def verifyEmail(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         messages.success(request, "Your email has been successfully verified. You are now logged in.")
#         return redirect('login_page')
#     else:
#         messages.error(request, "The verification link is invalid or has expired.")
#         return redirect('home')



# from django.contrib import messages
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect
# from django.utils.encoding import force_bytes, force_str
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.template.loader import render_to_string
# from django.core.mail import EmailMessage
# from django.conf import settings
# from .tokens import account_activation_token
# from .models import DiseasePrediction

# # from .utils.tokens import account_activation_token


# def signup(request):
#     if request.method == 'POST':
#         # Retrieve the user inputs from the request object
#         username = request.POST.get('username')
#         first_name = request.POST.get('fname')
#         last_name = request.POST.get('lname')
#         email = request.POST.get('email')
#         password1 = request.POST.get('pass1')
#         password2 = request.POST.get('pass2')

#         errors = {}
#         if not username:
#             errors['username'] = 'Username is required!'
#         elif User.objects.filter(username=username).exists():
#             errors['username'] = 'Username already exists!'
#         if first_name and not first_name.isalpha():
#             errors['fname'] = 'First name should have only alphabetical letters!'
#         if last_name and not last_name.isalpha():
#             errors['lname'] = 'Last name should have only alphabetical letters!'
#         if not email:
#             errors['email'] = 'Email is required!'
#         elif not '@' in email:
#             errors['email'] = 'Email should be valid!'
#         elif User.objects.filter(email=email).exists():
#             errors['email'] = 'Email already exists!'
#         if not password1:
#             errors['pass1'] = 'Password is required!'
#         elif len(password1) < 8:
#             errors['pass1'] = 'Password must be at least 8 characters long!'
#         if not password2:
#             errors['pass2'] = 'Please confirm your password!'
#         elif password1 != password2:
#             errors['pass2'] = 'Passwords do not match!'

#         # If there are errors, display them on the signup page
#         if errors:
#             return render(request, 'signup.html', {'errors': errors})

#         # Create the user object
#         user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
#         user.is_active = False
#         user.save()

#         # Send the email verification link
#         message = render_to_string('email_verification.html', {
#             'user': user,
#             'domain': settings.DOMAIN,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': account_activation_token.make_token(user),
#         })
#         mail_subject = 'Activate your account.'
#         to_email = user.email
#         email = EmailMessage(mail_subject, message, to=[to_email])
#         email.send()

#         # Render the login page with a success message
#         return render(request, 'login.html', {"successful": "You have successfully created an account. Please check your email and activate your account to start exploring our platform."})
#     else:
#         return render(request, 'signup.html')

# def activate(request, uidb64, token):
#     try:
#         # Decode the uidb64 to get the user's primary key
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     # Verify the token and activate the user
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         messages.success(request, 'Thank you for your email confirmation. Now you can login to your account.')
#         return redirect('login_page')
#     else:
#         messages.error(request, 'Activation link is invalid or has expired.')
#         return redirect('signup_page')


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

@login_required
def image_upload(request):
    if request.method == 'POST':
        image = request.FILES.get('image')

        predicted_disease = "disease1" # Replace with your prediction logic
        treatment = "Fungicides such as azoxystrobin, propiconazole, or chlorothalonil can be used to control cercospora leaf spot. " # Replace with your prediction logic
        how_to_use = "Mix the fungicide with water according to the manufacturer's instructions and apply it evenly to the tree's foliage and fruit using a sprayer or other suitable equipment. It's best to apply the fungicide before the onset of infection, and repeat every 7-14 days as necessary." # Replace with your prediction logic

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
