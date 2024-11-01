
from email.headerregistry import Group
from venv import logger
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from admin_panel.models import Coordinator
from core.models import CoreStudent

from core.forms import StudentSignupForm

def index(request):
    return render(request, 'core/index.html')

def student_dashboard(request):
    return render(request, 'student/dashboard.html')

def coordinator_dashboard(request):
    return render(request, 'coordinator/dashboard.html')

# views.py
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Check if the user is a superuser (Admin)
                if user.is_superuser:
                    login(request, user)
                    return redirect('admin_dashboard')

                # Check if the user is a coordinator
                elif user.groups.filter(name='Coordinator').exists():
                    try:
                        coordinator = Coordinator.objects.get(user=user)

                        if not coordinator.full_name:
                            return redirect('coordinator_details')  # Redirect to provide additional details
                        else:
                            login(request, user)
                            return redirect('coordinator_dashboard')  # Redirect to the dashboard

                    except Coordinator.DoesNotExist:
                        messages.error(request, "Coordinator details not found. Please contact the administrator.")
                        return redirect('login')

                # Check if the user is a student
                elif user.groups.filter(name='student').exists():
                    try:
                        # Attempt to retrieve the associated CoreStudent instance
                        core_student = CoreStudent.objects.get(user=user)

                        # Check if the student account is approved
                        if core_student.is_approved:
                            login(request, user)
                            return redirect('student_dashboard')  # Redirect to the student dashboard
                        else:
                            messages.error(request, "Your account is not yet approved by an administrator.")
                            return redirect('login')

                    except CoreStudent.DoesNotExist:
                        messages.error(request, "Your account has not been set up as a student. Please contact the administrator.")
                        return redirect('login')

                # Default fallback if user type is unknown or no role matches
                return redirect('home')

            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose a different username.")
                return render(request, 'core/signup.html', {'form': form})

            # Try saving the user and student profile
            try:
                user = User(
                    username=username,
                    password=make_password(password)  # Hash the password
                )
                user.save()  # Save the user to the database
                
                # Create the CoreStudent profile linked to the User
                core_student = CoreStudent(
                    user=user,
                    full_name=form.cleaned_data['full_name'],
                    register_number=form.cleaned_data['register_number'],
                    email=form.cleaned_data['email'],
                    course=form.cleaned_data['course'],
                    branch=form.cleaned_data['branch'],
                    phone_number=form.cleaned_data['phone_number'],
                    year_of_study=form.cleaned_data['year_of_study'],
                    is_approved=False  # Set to False for pending approval
                )
                core_student.save()

                # Assign the user to the 'student' group
                student_group, created = Group.objects.get_or_create(name='student')
                user.groups.add(student_group)
                
                messages.success(request, "Registration successful! Your account is pending approval.")
                return redirect('login')  # Adjust to your login URL

            except Exception as e:
                # Log the error and show a friendly message
                print(f"Error during signup: {e}")
                messages.error(request, "There was an error processing your signup. Please try again.")
                return render(request, 'core/signup.html', {'form': form})

        else:
            # If form is not valid, display errors
            messages.error(request, "Please correct the errors below.")

    else:
        form = StudentSignupForm()

    return render(request, 'core/signup.html', {'form': form})


def home(request):
    return render(request, 'core/index.html')

def logout_view(request):
    logout(request)
    return redirect('home')  # Adjust according to your routing



from .models import CoreStudent  # Import your Student model

def student_list(request):
    # Retrieve all student data from the database
    students = CoreStudent.objects.all()
    # Pass the student data to the template
    return render(request, 'admin_panel/student_list.html', {'students': students})



def edit_student(request, student_id):
    student = get_object_or_404(CoreStudent, id=student_id)

    if request.method == 'POST':
        # Update student attributes from form data
        student.full_name = request.POST.get('full_name')
        student.email = request.POST.get('email')
        student.username = request.POST.get('username')
        
        # Check if the password field is empty; if so, keep the old password
        new_password = request.POST.get('password')
        if new_password:  # Only update if a new password was provided
            student.password = new_password  # Consider hashing this for security

        student.course = request.POST.get('course')
        student.branch = request.POST.get('branch')
        student.year_of_study = request.POST.get('year_of_study')
        student.phone_number = request.POST.get('phone_number')
        
        # Save the updated student object
        student.save()

        # Add success message
        messages.success(request, 'Student updated successfully!')
        return redirect('student_list')  # Change this to your actual student list URL name

    return render(request, 'admin_panel/edit_student.html', {'student': student})



