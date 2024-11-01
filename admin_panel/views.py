from email.headerregistry import Group
import logging
from pyexpat.errors import messages
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages


from admin_panel.models import Coordinator, CoordinatorAssignedEvent, SportEvent
from coordinator.forms import SportEventForm
from .forms import CoordinatorForm  # type: ignore # Import your form



def admin_dashboard(request):
    return render(request, 'admin_panel/dashboard.html')
    

def create_event(request):
    # Logic for creating an event goes here
    return render(request, 'admin_panel/create_event.html')
def manage_users(request):
    # Logic for managing users goes here
    return render(request,'admin_panel/manage_users.html')


logger = logging.getLogger(__name__)

def coordinators_list(request):
    """
    View function to display the list of coordinators.
    """
    try:
        # Retrieve the Coordinator group
        coordinator_group = Group.objects.get(name='Coordinator')
    except Group.DoesNotExist:
        # Log the error and handle the case where the group does not exist
        logger.error("Coordinator group not found.")
        return render(request, 'admin_panel/error.html', {'message': 'Coordinator group not found.'})

    # Get users in this group
    coordinators = User.objects.filter(groups=coordinator_group)
    
    # Check if there are any coordinators
    if not coordinators.exists():
        logger.info("No coordinators found in the Coordinator group.")
        return render(request, 'admin_panel/error.html', {'message': 'No coordinators found in this group.'})

    logger.info(f"Found {coordinators.count()} coordinators.")
    return render(request, 'admin_panel/coordinators_list.html', {'coordinators': coordinators})

# Add a new coordinator

def add_coordinator(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')  # Ensure your form includes an email field

        # Create the coordinator
        try:
            # Create the User instance
            user = User.objects.create_user(username=username, password=password, email=email)

            # Add the user to the Coordinator group
            coordinator_group = Group.objects.get(name='Coordinator')  # Fetch the Coordinator group
            user.groups.add(coordinator_group)  # Add the user to the group

            # Create the Coordinator instance
            coordinator = Coordinator(user=user, email=email)  # Assuming email is part of the Coordinator model
            coordinator.save()

            messages.success(request, 'Coordinator added successfully.')
            return redirect('coordinators_list')  # Redirect immediately after setting message
        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'admin_panel/add_coordinator.html')
    
def delete_coordinator(request, user_id):
    # Get the coordinator object based on user_id or return a 404 if not found
    coordinator = get_object_or_404(Coordinator, user__id=user_id)

    if request.method == 'POST':
        try:
            # Remove the user from the group and delete the user
            user = coordinator.user
            user.groups.remove(Group.objects.get(name='Coordinator'))  # Remove user from the group
            user.delete()  # Delete the user
            coordinator.delete()  # Delete the Coordinator instance
            messages.success(request, 'Coordinator deleted successfully.')
            return redirect('coordinators_list')  # Redirect to the coordinators list page
        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'admin_panel/delete_coordinator.html', {'coordinator': coordinator})


def my_view(request):
    response = my_view(request)
    if response.get('success'):
        return JsonResponse({'success': True, 'message': 'Action completed.'})  # Correctly returning a dict

# Edit a coordinator
def edit_coordinator(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Check if the user is in the "Coordinator" group
    if not user.groups.filter(name='Coordinator').exists():
        messages.warning(request, 'This user is not part of the Coordinator group.')
        return redirect('coordinators_list')  # Redirect if not a coordinator

    if request.method == 'POST':
        form = CoordinatorForm(request.POST, instance=user)  # Associate the form with the user
        if form.is_valid():
            # Update the user instance
            user = form.save(commit=False)  # Save but don't commit to the database yet

            # Handle password update if provided
            password = request.POST.get('password')
            if password:
                user.set_password(password)  # Set new password if provided

            # Save user instance to update the email and username
            user.save()  # Save user to the User table

            # Now update the Coordinator instance email
            coordinator_instance = Coordinator.objects.filter(user=user).first()  # Get the associated coordinator
            if coordinator_instance:
                coordinator_instance.email = user.email  # Set the coordinator's email to the updated user email
                coordinator_instance.save()  # Save the coordinator instance

            messages.success(request, 'Coordinator updated successfully.')
            return redirect('coordinators_list')  # Redirect after success
    else:
        form = CoordinatorForm(instance=user)  # Populate the form with existing user data

    return render(request, 'admin_panel/edit_coordinator.html', {'form': form, 'user': user})
# Delete a coordinato


def student_list(request):
    # Logic to retrieve student data goes here
    return render(request, 'admin_panel/student_list.html', {})

# admin_panel/views.py

def test_view(request):
    return render(request, 'admin_panel/test.html')

def sport_event_list(request):
    sport_events = SportEvent.objects.all()
    return render(request, 'admin_panel/sport_events.html', {'sport_events': sport_events})

def sport_event_add(request):
    if request.method == 'POST':
        try:
            coordinator_id = request.POST['coordinator']
            coordinator = Coordinator.objects.get(id=coordinator_id)  # Fetch the Coordinator instance

            # Create a new sport event
            event = SportEvent(
                title=request.POST['title'],
                description=request.POST['description'],
                date=request.POST['date'],
                time=request.POST['time'],
                location=request.POST['location'],
                sport_type=request.POST['sport_type'],
                coordinator=coordinator  # Assign Coordinator instance, not User instance
            )
            event.save()

            # Store the coordinator_id and sport_event_id in the CoordinatorAssignedEvent table
            CoordinatorAssignedEvent.objects.create(coordinator=coordinator, sport_event=event)

            messages.success(request, 'Sport event added successfully.')
            return redirect('sport_events')
        except Coordinator.DoesNotExist:
            messages.error(request, 'Coordinator does not exist.')
            return render(request, 'admin_panel/sport_event_add.html', {'error': 'Coordinator does not exist.'})

    # Fetch coordinators
    try:
        coordinator_group = Group.objects.get(name='Coordinator')
        coordinators = Coordinator.objects.filter(user__groups=coordinator_group)
    except Group.DoesNotExist:
        coordinators = []

    return render(request, 'admin_panel/sport_event_add.html', {'coordinators': coordinators})

def sport_event_edit(request, event_id):
    # Get the sport event or return a 404 if not found
    event = get_object_or_404(SportEvent, id=event_id)

    if request.method == 'POST':
        try:
            # Update the sport event details
            event.title = request.POST['title']
            event.description = request.POST['description']
            event.date = request.POST['date']
            event.time = request.POST['time']
            event.location = request.POST['location']
            event.sport_type = request.POST['sport_type']

            # If you want to change the coordinator as well
            if 'coordinator' in request.POST:
                coordinator_id = request.POST['coordinator']
                coordinator = Coordinator.objects.get(id=coordinator_id)
                event.coordinator = coordinator.user  # Use the User instance directly

            event.save()  # Save the updated event
            messages.success(request, 'Sport event updated successfully.')
            return redirect('sport_events')
        except Coordinator.DoesNotExist:
            messages.error(request, 'Coordinator does not exist.')

    # Fetch coordinators to populate the form
    try:
        coordinator_group = Group.objects.get(name='Coordinator')
        coordinators = Coordinator.objects.filter(user__groups=coordinator_group)
    except Group.DoesNotExist:
        coordinators = []

    # Render the edit template with the event and coordinators
    return render(request, 'admin_panel/sport_event_edit.html', {
        'event': event,
        'coordinators': coordinators
    })



def sport_event_delete(request, event_id):
    event = get_object_or_404(SportEvent, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('sport_events')  # Redirect to the list of events after deletion
    return render(request, 'admin_panel/sport_event_delete.html', {'event': event})