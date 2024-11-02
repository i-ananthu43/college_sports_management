# student/views.py
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from admin_panel.models import SportEvent
from django.contrib.auth.decorators import login_required
from coordinator.models import Certificate, Result
from core.models import CoreStudent
from student.forms import EventRegistrationForm
from student.models import EventRegistration

def student_dashboard(request):
    events = SportEvent.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'student/dashboard.html', {'events': events})
   

def dashboard(request):
    core_student = None
    if request.user.is_authenticated:
        core_student = CoreStudent.objects.get(user=request.user)  # Assuming user is linked to CoreStudent
    return render(request, 'student/dashboard.html', {'core_student': core_student})


def upcoming_events(request):
    events = SportEvent.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'student/upcoming_events.html', {'events': events})

    
def your_view(request):
    if request.user.is_authenticated:
        try:
            core_student = CoreStudent.objects.get(user=request.user)
            print(core_student.user.full_name)  # Debugging line
        except CoreStudent.DoesNotExist:
            core_student = None
    else:
        return redirect('login')

    return render(request, 'student/dashboard.html', {'core_student': core_student})

@login_required   
def event_registration(request, event_id):
    # Fetch the CoreStudent instance associated with the logged-in user
    student = get_object_or_404(CoreStudent, user=request.user)
    event = get_object_or_404(SportEvent, id=event_id)  # Fetch the specific event by ID

    # Check if the student is already registered for this event
    if EventRegistration.objects.filter(student=student, event=event).exists():
        messages.error(request, 'You are already registered for this event.')
        return redirect('upcoming_events')  # Redirect to the upcoming events page

    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            # Check if the student has already registered for 4 events
            registered_events_count = EventRegistration.objects.filter(student=student).count()

            if registered_events_count >= 4:
                messages.error(request, 'You can only register for a maximum of 4 events.')
                return render(request, 'student/event_registration.html', {'form': form, 'event': event})

            # Update the student's house field in CoreStudent model
            selected_house = form.cleaned_data['house']
            student.house = selected_house
            student.save()

            # Create registration for the event
            registration = EventRegistration(
                full_name=student.full_name,
                course=student.course,
                branch=student.branch,
                event=event,
                student=student,
                house=selected_house,  # Save the house in the registration as well
            )
            registration.save()

            messages.success(request, 'Successfully registered for the event!')
            return redirect('upcoming_events')
    else:
        # Pre-fill the form with student's data, including the house if it exists
        form = EventRegistrationForm(initial={
            'full_name': student.full_name,
            'course': student.course,
            'branch': student.branch,
            'house': student.house,  # Pre-fill with existing house if available
        })

    context = {
        'form': form,
        'event': event,
    }
    return render(request, 'student/event_registration.html', context)

@login_required
def view_registered_events(request):
    # Fetch the CoreStudent instance associated with the logged-in user
    student = get_object_or_404(CoreStudent, user=request.user)

    # Fetch the events registered by the student
    registrations = EventRegistration.objects.filter(student=student)

    context = {
        'registrations': registrations,
    }
    return render(request, 'student/view_registered_events.html', context)

def view_all_events(request):
    # Fetch all events from the database
    events = SportEvent.objects.all()

    context = {
        'events': events,
    }
    return render(request, 'student/view_all_events.html', context)

@login_required
def view_results(request):
    # Get the current logged-in student
    student = get_object_or_404(CoreStudent, user=request.user)

    # Get all event registrations for this student
    registered_events = EventRegistration.objects.filter(student=student)

    # Initialize a list to hold the results
    results = []

    # Loop through each registered event and fetch its result
    for registration in registered_events:
        result = Result.objects.filter(sport_event=registration.event).first()
        if result:
            results.append({
                'event': registration.event,
                'result': result
            })

    return render(request, 'student/view_results.html', {'results': results})

@login_required  # Ensure that the user is logged in
def view_certificates(request):
    try:
        # Retrieve the CoreStudent instance related to the logged-in user
        student = CoreStudent.objects.get(user=request.user)

        # Query for Event Registrations related to the student
        registrations = EventRegistration.objects.filter(student=student)

        # Query for certificates related to those registrations that are approved
        certificates = Certificate.objects.filter(
            student__in=registrations,  # Filter by EventRegistration instances related to the student
            status='approved'  # Only include approved certificates
        )

        # Render the template with the certificates context
        return render(request, 'student/view_certificates.html', {'certificates': certificates})

    except CoreStudent.DoesNotExist:
        # Handle the case where the student profile does not exist
        return render(request, 'student/view_certificates.html', {
            'certificates': [],
            'error': "Student profile not found."
        })