from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login

def index(request):
    return render(request, 'base.html')

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data.get('is_admin'):
                user.is_admin = True
            if form.cleaned_data.get('is_contractor'):
                user.is_contractor = True
            if form.cleaned_data.get('is_authority'):
                user.is_authority = True
            if form.cleaned_data.get('is_users'):
                user.is_users = True
            user.save()

            msg = 'User created successfully.'
            return redirect('login')  # After registration, redirect to login page
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
    
    return render(request, 'register.html', {'form': form, 'msg': msg})

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print(f'User {username} logged in with roles: is_admin={user.is_admin}, is_contractor={user.is_contractor}, is_authority={user.is_authority}, is_users={user.is_users}')

                # Redirect based on user roles
                role_redirects = {
                    'is_admin': 'adminpage',
                    'is_contractor': 'contractor',
                    'is_authority': 'authority',
                    'is_users': 'users',
                }

                for role, redirect_url in role_redirects.items():
                    if getattr(user, role):
                        return redirect(redirect_url)

                msg = 'User has no assigned role.'
            else:
                msg = 'Invalid credentials.'
        else:
            msg = 'Error occurred during form validation.'
    return render(request, 'login.html', {'form': form, 'msg': msg})

def admin(request):
    return render(request, 'admin.html')

def contractor(request):
    return render(request, 'contractor.html')

def authority(request):
    return render(request, 'authority.html')

def users(request):
    return render(request, 'users.html')
