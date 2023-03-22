from django.http import HttpResponse
from django.shortcuts import render, redirect


from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'index.html')

def logo_redirect(request):
    return redirect('index')

def login_page(request):
    return render(request,'login.html')



def signup_page(request):
    return render(request,'signup.html')


# def signup(request):
#     print("Enering signup")
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
#         if not first_name.isalpha():
#             errors['fname'] = 'First name should have only alphabetical letters!'
#         if not last_name.isalpha():
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
#             print("error occured")
#             return render(request, 'signup.html', {'errors': errors})
#         print("no error")
#         # Create the user object
#         user = User.objects.create_user(username=username, email=email, password=password1,
#                                         first_name=first_name, last_name=last_name)
#         # Log in the user after successful registration
#         auth.login(request, user)
#         # messages.success(request, 'You are now registered and logged in!')

#         return render('login.html',{"successful":"'You are now registered and logged in!'" })

#         # return redirect('login_page')
#     else:
#         return render(request, 'signup.html')




# def signup(request):
#     print("Entering signup")
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
#             print("error occurred")
#             return render(request, 'signup.html', {'errors': errors})
#             # return render(request, 'signup.html',{'errors': errors, 'username': username, 'fname': first_name, 'lname': last_name, 'email': email})
#             # return render(request, 'signup.html', {'errors': errors, 'username': username, 'fname': first_name, 'lname': last_name, 'email': email})

#         # Create the user object
#         user = User.objects.create_user(username=username, email=email, password=password1,
#                                         first_name=first_name, last_name=last_name)
#         # Log in the user after successful registration
#         auth.login(request, user)
#         # messages.success(request, 'You are now registered and logged in!')

#         return render(request, 'login.html', {"successful": "You are now registered and logged in!"})

#         # return redirect('login_page')
#     else:
#         return render(request, 'signup.html')



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
#             # Clear previous error messages
#             username_value = request.POST.get('username', '')
#             first_name_value = request.POST.get('fname', '')
#             last_name_value = request.POST.get('lname', '')
#             email_value = request.POST.get('email', '')
#             return render(request, 'signup.html', {'errors': errors, 'username': username_value, 'fname': first_name_value, 'lname': last_name_value, 'email': email_value})
#         else:
#             # Create a new user object and save it to the database
#             user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
#             user.save()
#             # Redirect the user to the home page
#             return redirect('login')
#     else:
#         # Render the signup page
#         return render(request, 'signup.html')





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
            #  return render(request, 'login.html', {"successful": "You are now registered and logged in!"})

        # Create the user object
        user = User.objects.create_user(username=username, email=email, password=password1,
                                        first_name=first_name, last_name=last_name)
        # Log in the user after successful registration
        # auth.login(request, user)
        # messages.success(request, 'You are now registered and logged in!')
        # return redirect('login')
        return render(request, 'login.html', {"successful": "You have successfully created an account. You can now login and start exploring our platform."})
    else:
        return render(request, 'signup.html')




def login(request):
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
            return redirect('home')
        else:
            print("not authencate")
            # Invalid credentials
            error = {"errorr": "Username or password didn't match"}
            return render(request, 'login.html', error)
    else:
        return render(request, 'login.html')



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