
import logging
import math
import random
from django.shortcuts import redirect, render , get_object_or_404


from admin_panel.models import Coordinator, CoordinatorAssignedEvent, SportEvent
from coordinator.forms import  SportEventForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from coordinator.models import House, MatchFixture, Result
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

logger = logging.getLogger(__name__)

def generate_fixture_view(request, event_id):
    event = get_object_or_404(SportEvent, id=event_id)
    sport_type = event.sport_type.lower()

    if sport_type == "athletics":
        return render(request, 'coordinator/match_fixture.html', {
            'event': event,
            'message': 'This is an athletics event. Fixture generation is not required.',
        })

    elif sport_type == "sports":
        registered_students = list(CoreStudent.objects.filter(eventregistration__event=event))
        num_participants = len(registered_students)

        if num_participants < 4:
            return render(request, 'coordinator/match_fixture.html', {
                'event': event,
                'message': 'At least 4 participants are required to generate fixtures.',
            })

        rounds = int(math.log2(num_participants))
        matches = []

        for round_number in range(1, rounds + 1):
            if MatchFixture.objects.filter(event=event, round_number=round_number).exists():
                continue

            random.shuffle(registered_students)
            round_matches = []
            
            for i in range(0, len(registered_students) - 1, 2):
                match = MatchFixture.objects.create(
                    event=event,
                    student_1=registered_students[i],
                    student_2=registered_students[i + 1],
                    round_number=round_number
                )
                round_matches.append(match)
                matches.append(match)

            if len(registered_students) % 2 != 0:
                match = MatchFixture.objects.create(
                    event=event,
                    student_1=registered_students[-1],
                    student_2=None,
                    round_number=round_number
                )
                round_matches.append(match)
                matches.append(match)

            registered_students = [match.winner for match in round_matches if match.winner]

        logger.info("Matches created: %s", matches)
        return render(request, 'coordinator/match_fixture.html', {
            'event': event,
            'matches': matches,
        })

    return render(request, 'coordinator/match_fixture.html', {
        'event': event,
        'message': 'Invalid sport type. Fixture generation is only available for sports events.',
    })






def enter_score_view(request, match_id):

    match = get_object_or_404(MatchFixture, id=match_id)
    
    if request.method == 'POST':
        try:
            # Assuming you're getting scores from POST data
            student_1_score = request.POST.get('student_1_score')
            student_2_score = request.POST.get('student_2_score')

            # Check if scores are provided and convert to int
            if student_1_score is None or student_2_score is None:
                return render(request, 'coordinator/enter_score.html', {
                    'match': match,
                    'error': 'Both scores must be provided.',
                })

            # Convert scores to integers
            student_1_score = int(student_1_score)
            student_2_score = int(student_2_score)

            # Save scores to the match
            match.student_1_score = student_1_score
            match.student_2_score = student_2_score
            
            # Determine and set the winner based on scores
            if student_1_score > student_2_score:
                match.winner = match.student_1
            elif student_2_score > student_1_score:
                match.winner = match.student_2
            else:
                match.winner = None  # Tie case, handle as needed

            match.save()

            return redirect('match_fixture', event_id=match.event.id)

        except ValueError:
            return render(request, 'coordinator/enter_score.html', {
                'match': match,
                'error': 'Invalid score input. Please enter valid integers.',
            })

    return render(request, 'coordinator/enter_score.html', {'match': match})


@login_required
def select_winners(request, event_id):
    # Retrieve the CoordinatorAssignedEvent instance using event_id
    assigned_event = get_object_or_404(CoordinatorAssignedEvent, id=event_id)

    # Get the Coordinator instance for the logged-in user
    try:
        coordinator = request.user.coordinator
    except Coordinator.DoesNotExist:
        messages.error(request, "You do not have permission to select winners for this event.")
        return redirect('manage_events')

    # Check if the coordinator is assigned to the event
    if assigned_event.coordinator != coordinator:
        messages.error(request, "You do not have permission to select winners for this event.")
        return redirect('manage_events')

    # Access the associated sport_event from the assigned_event
    event = assigned_event.sport_event

    # Ensure the event type is "Athletics"
    if event.sport_type != "Athletics":
        messages.error(request, "This option is only available for athletics events.")
        return redirect('manage_events')

    # Fetch registered students related to the given event_id
    registered_students = EventRegistration.objects.filter(event_id=event.id)

    # Check if winners have already been selected for this event
    result = Result.objects.filter(sport_event=event).first()

    if request.method == "POST":
        winner_id = request.POST.get("winner")
        runner_up_id = request.POST.get("runner_up")
        third_place_id = request.POST.get("third_place")

        if winner_id and runner_up_id and third_place_id:
            if result:  # If results already exist, update them
                result.first_prize = winner_id
                result.second_prize = runner_up_id
                result.third_prize = third_place_id
                result.save()
                messages.success(request, "Results have been updated successfully!")
            else:  # If results do not exist, create a new entry
                Result.objects.create(
                    sport_event=event,
                    title=event.title,
                    first_prize=winner_id,
                    second_prize=runner_up_id,
                    third_prize=third_place_id,
                    date=event.date
                )
                messages.success(request, "Winners have been selected and saved successfully!")

            return redirect('view_assigned_event_results')
        else:
            messages.error(request, "Please select all three placements.")

    return render(request, 'coordinator/select_winners.html', {
        'event': event,
        'registered_students': registered_students,
        'event_id': assigned_event.sport_event.id,
        'result': result  # Pass existing result to the template
    })

def view_assigned_event_results(request):
    
    coordinator = request.user.coordinator  # Assuming you have a related Coordinator model
    assigned_events = CoordinatorAssignedEvent.objects.filter(coordinator=coordinator)
    
    # Fetch results and related student information for assigned events
    results = Result.objects.filter(
        sport_event__in=assigned_events.values_list('sport_event', flat=True)
    ).prefetch_related('sport_event')
    
    # Build a list with detailed student information for each result
    event_results = []
    for result in results:
        event_result = {
            'event': result.sport_event,
            'first_prize': CoreStudent.objects.filter(id=result.first_prize).first(),
            'second_prize': CoreStudent.objects.filter(id=result.second_prize).first(),
            'third_prize': CoreStudent.objects.filter(id=result.third_prize).first(),
        }
        event_results.append(event_result)

    context = {
        'event_results': event_results,
    }
    return render(request, 'coordinator/view_assigned_event_results.html', context)