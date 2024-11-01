from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from .models import CoreStudent  # Adjust the import based on your project structure

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            # Check if the user is active and verify the password
            if user.is_active and user.check_password(password):
                try:
                    # Fetch the associated CoreStudent instance
                    core_student = CoreStudent.objects.get(user=user)
                    # Check if the CoreStudent account is approved
                    if core_student.is_approved:
                        return user  # Return the user if approved
                    else:
                        return None  # Not approved
                except CoreStudent.DoesNotExist:
                    return None  # No CoreStudent found
        except User.DoesNotExist:
            return None  # User does not exist

        return None  # Default return if no conditions are met
