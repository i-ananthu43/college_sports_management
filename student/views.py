# student/views.py
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from admin_panel.models import SportEvent
from django.contrib.auth.decorators import login_required
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


def view_certificates(request):
    # Logic for viewing a student's certificate
    return render(request, 'student/view_certificates.html')

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

            # Create registration for the event
            registration = EventRegistration(
                full_name=student.full_name,
                course=student.course,
                branch=student.branch,
                event=event,
                student=student,
                house=form.cleaned_data['house'],  # Get the house from the form
            )
            registration.save()

            messages.success(request, 'Successfully registered for the event!')
            return redirect('upcoming_events')
    else:
        # Pre-fill the form with student's data
        form = EventRegistrationForm(initial={
            'full_name': student.full_name,
            'course': student.course,
            'branch': student.branch,
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