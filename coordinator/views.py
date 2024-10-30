
from itertools import combinations
import random
from django.shortcuts import redirect, render , get_object_or_404


from admin_panel.models import Coordinator, CoordinatorAssignedEvent, SportEvent
from coordinator.forms import  SportEventForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import CoreStudent
from student.models import Certificate, EventRegistration
 # Ensure that the user is logged in

    
@login_required  # Ensures the user must be logged in to access this view
def coordinator_dashboard(request):
    # Check if the user has a related Coordinator instance
    if hasattr(request.user, 'coordinator'):
        coordinator = request.user.coordinator
        
        # Fetch assigned events from CoordinatorAssignedEvent model
        assigned_events = CoordinatorAssignedEvent.objects.filter(coordinator=coordinator)

        if not assigned_events.exists():  # Check if there are any assigned events
            messages.info(request, 'You have no assigned events.')  # Notify the user
        
        return render(request, 'coordinator/dashboard.html', {'assigned_events': assigned_events})
    else:
        messages.error(request, 'Coordinator profile not found.')  # Notify if coordinator profile does not exist
        return redirect('login')  # Redirect to login if not authenticated or coordinator not found


def manage_events(request):
    events = []  # Initialize an empty list to hold the events
    try:
        # Get the Coordinator instance associated with the logged-in user
        coordinator = Coordinator.objects.get(user=request.user)
        
        # Access events assigned to this coordinator from the CoordinatorAssignedEvent model
        events = CoordinatorAssignedEvent.objects.filter(coordinator=coordinator)  # Adjust the model name if necessary
    except Coordinator.DoesNotExist:
        events = []  # No events if the coordinator does not exist

    return render(request, 'coordinator/manage_events.html', {'events': events})

def edit_event(request, event_id):
    # Fetch the assigned event using the event_id from CoordinatorAssignedEvent
    assigned_event = get_object_or_404(CoordinatorAssignedEvent, id=event_id)

    # Check if the logged-in user is associated with the assigned event's coordinator
    if request.user != assigned_event.coordinator.user:
        messages.error(request, 'You are not authorized to edit this event.')
        return redirect('manage_events')  # Redirect if unauthorized

    # Handle form submission
    if request.method == 'POST':
        # Bind form with POST data and specify the instance to update
        form = SportEventForm(request.POST, instance=assigned_event.sport_event, coordinator_assigned=True)
        
        if form.is_valid():
            # Save the form data to update the SportEvent instance
            form.save()
            messages.success(request, 'Event updated successfully.')
            return redirect('manage_events')  # Redirect after successful save
        else:
            # Output form errors for debugging
            print("Form errors:", form.errors)  # Check for validation errors
            messages.error(request, 'There were errors in your submission.')

    else:
        # Pre-fill the form with existing data for the GET request
        form = SportEventForm(instance=assigned_event.sport_event, coordinator_assigned=True)

    # Render the form with the event data
    return render(request, 'coordinator/edit_event.html', {'form': form, 'event': assigned_event})

@login_required
def view_assigned_events(request):
    # Fetch the coordinator instance associated with the logged-in user
    coordinator = get_object_or_404(Coordinator, user=request.user)

    # Fetch the events assigned to this coordinator
    assigned_events = CoordinatorAssignedEvent.objects.filter(coordinator=coordinator)

    # Create a list to hold events and their registered students
    events_with_students = []

    for assigned_event in assigned_events:
        event = assigned_event.sport_event
        registrations = EventRegistration.objects.filter(event=event)
        events_with_students.append((event, registrations))

    context = {
        'events_with_students': events_with_students,
    }
    return render(request, 'coordinator/view_assigned_events.html', context)

@login_required
def approve_registration(request, registration_id):
    registration = get_object_or_404(EventRegistration, id=registration_id)
    
    # Change the registration status to approved
    registration.approved = True
    registration.save()

    messages.success(request, 'Registration approved successfully!')
    return redirect('view_assigned_events')  # Redirect back to the assigned events view




def coordinator_details(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        department = request.POST.get('department')

        try:
            # Assuming you have access to the logged-in user's coordinator instance
            coordinator = Coordinator.objects.get(user=request.user)
            coordinator.full_name = full_name
            coordinator.phone_number = phone_number
            coordinator.department = department
            coordinator.save()

            messages.success(request, 'Your details have been updated successfully!')
            return redirect('coordinator_dashboard')  # Redirect to coordinator dashboard
        except Coordinator.DoesNotExist:
            messages.error(request, 'Coordinator details not found.')

    return render(request, 'coordinator/coordinator_details.html')  # Render the form again if not a POST request

def view_events(request):
    events = SportEvent.objects.all()  # Fetch all events

    return render(request, 'coordinator/view_events.html', {'events': events})
