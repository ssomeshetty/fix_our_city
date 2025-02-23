from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm  # Import the profile form
from .models import User
from authorities.models import Authority
from contractor.models import Contractor
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')

            # Check if the user is an authority, and create an Authority profile
            if user.role == 'authority':
                Authority.objects.create(
                    user=user,
                    name=user.username,  # You can customize this based on how you want to get the name
                    description="Description for authority",
                    jurisdiction="Jurisdiction for authority",
                    contact_info=user.contact_info,
                    address="Address for authority",
                    is_active=True
                )
                messages.success(request, 'Authority profile created successfully!')

            # Check if the user is a contractor, and create a Contractor profile
            elif user.role == 'contractor':
                authority = Authority.objects.first()  # You can adjust this to choose the appropriate authority
                Contractor.objects.create(
                    user=user,
                    name=user.username,  # Use username or custom field for name
                    expertise="General",  # Default value or adjust as necessary
                    contact_info=user.contact_info,
                    credit_score=1.00,  # Default value
                    authority=authority,  # Assign an authority
                    total_completed_issues=0,
                    is_active=True
                )
                messages.success(request, 'Contractor profile created successfully!')

            # Redirect based on role
            if user.role == 'public':
                return redirect('base')
            elif user.role == 'authority':
                return redirect('authority_dashboard')
            elif user.role == 'contractor':
                return redirect('contractor_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            # Redirect based on role
            if user.role == 'public':
                return redirect('view_issues')
            elif user.role == 'authority':
                return redirect('authority_dashboard')
            elif user.role == 'contractor':
                return redirect('contractor_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('base')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm
@login_required
def profile_display_view(request):
    """View to display the profile details."""
    return render(request, 'profile.html', {'user': request.user})

@login_required
def profile_update_view(request):
    """View to handle profile update."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')  # Redirect to the profile display page after update
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'profile_update.html', {'form': form})