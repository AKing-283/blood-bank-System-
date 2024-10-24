from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError



def index(request):
    all_group = BloodGroup.objects.annotate(total=Count('donor'))
    return render(request, "index.html", {'all_group': all_group})


def donors_list(request, myid):
    blood_groups = BloodGroup.objects.filter(id=myid).first()
    if blood_groups is None:
        messages.error(request, "No matching BloodGroup found.")
        return redirect('index')  # Or any other page you'd like to redirect to

    donor = Donor.objects.filter(blood_group=blood_groups)
    return render(request, "donors_list.html", {'donor': donor})



def donors_details(request, myid):
    details = Donor.objects.filter(id=myid)[0]
    return render(request, "donors_details.html", {'details': details})


def request_blood(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        state = request.POST['state']
        city = request.POST['city']
        address = request.POST['address']
        blood_group = request.POST['blood_group']
        date = request.POST['date']

        # Check if blood group exists
        try:
            blood_group_instance = BloodGroup.objects.get(name=blood_group)
        except BloodGroup.DoesNotExist:
            messages.error(request, "Selected blood group does not exist.")
            return redirect('request_blood')

        # Create the blood request
        blood_requests = RequestBlood.objects.create(
            name=name,
            email=email,
            phone=phone,
            state=state,
            city=city,
            address=address,
            blood_group=blood_group_instance,
            date=date
        )
        blood_requests.save()

        messages.success(request, "Blood request submitted successfully!")
        return redirect('index')  # Redirect to index after submitting the request
    return render(request, "request_blood.html")


def see_all_request(request):
    requests = RequestBlood.objects.all()
    return render(request, "see_all_request.html", {'requests': requests})

from django.db import IntegrityError


def become_donor(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        state = request.POST['state']
        city = request.POST['city']
        address = request.POST['address']
        gender = request.POST['gender']
        blood_group = request.POST['blood_group']
        date = request.POST['date']
        image = request.FILES['image']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose a different one.')
            return redirect('become_donor')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        # Associate donor with blood group
        try:
            blood_group_instance = BloodGroup.objects.get(name=blood_group)
        except BloodGroup.DoesNotExist:
            messages.error(request, "Invalid blood group selected.")
            return redirect('become_donor')

        # Create donor profile
        donors = Donor.objects.create(
            donor=user,
            phone=phone,
            state=state,
            city=city,
            address=address,
            gender=gender,
            blood_group=blood_group_instance,  # Associate with blood group
            date_of_birth=date,
            image=image
        )

        # Save the created donor and user
        user.save()
        donors.save()

        messages.success(request, "Donor registration successful!")
        return redirect('index')  # Redirect to index page or wherever you prefer
    return render(request, "become_donor.html")


def Login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/profile")
            else:
                messages.error(request, "Invalid login credentials.")
                return render(request, "index.html")
    return render(request, "login.html")


def Logout(request):
    logout(request)
    return redirect('/')


from django.shortcuts import render, redirect

@login_required(login_url='/login')
def profile(request):
    try:
        donor_profile = Donor.objects.get(donor=request.user)
        return render(request, "profile.html", {'donor_profile': donor_profile})
    except Donor.DoesNotExist:
        # Redirect to a custom error page or provide a user-friendly message
        return redirect('/')

@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'profile.html', {'profile': profile})


@login_required(login_url='/login')
def edit_profile(request):
    donor_profile = get_object_or_404(Donor, donor=request.user)
    if request.method == "POST":
        donor_profile.donor.email = request.POST['email']
        donor_profile.phone = request.POST['phone']
        donor_profile.state = request.POST['state']
        donor_profile.city = request.POST['city']
        donor_profile.address = request.POST['address']

        try:
            donor_profile.donor.save()
            donor_profile.save()

            image = request.FILES.get('image')
            if image:
                donor_profile.image = image
                donor_profile.save()

            messages.success(request, "Profile updated successfully!")
        except Exception as e:
            messages.error(request, f"Error: {e}")

        return render(request, "edit_profile.html", {'donor_profile': donor_profile})
    return render(request, "edit_profile.html", {'donor_profile': donor_profile})

@login_required(login_url='/login')
def change_status(request):
    donor_profile = Donor.objects.get(donor=request.user)
    if donor_profile.ready_to_donate:
        donor_profile.ready_to_donate = False
        donor_profile.save()
    else:
        donor_profile.ready_to_donate = True
        donor_profile.save()
    return redirect('/profile')



def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signup')  # Redirect to the signup page

        # Check password length
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
            return redirect('signup')  # Redirect to the signup page

        # Create the user
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Create the profile and associate it with the user
        profile = Profile.objects.create(
            user=user,
            phone=request.POST.get('phone'),
            location=request.POST.get('location'),
            email=request.POST.get('email'),
            user_type=user_type,  # Save user type (hospital or donor)
            blood_group=request.POST.get('blood_group') if user_type == 'donor' else None
        )
        profile.save()

        messages.success(request, 'Account created successfully! You can now log in.')
        login(request, user)  # Log in the user after signup

        return redirect('login')  # Redirect to the login page

    return render(request, 'signup.html')