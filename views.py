from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Profile,Event,Job,Announcement
from .forms import EventForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.profile.role == "admin":
                return redirect("admin_portal")
            else:
                return redirect("alumni_portal")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            password=password
        )

    #     profile = Profile.objects.create(
    #         user=user,
    #         role=role
    #     )

    #     if role == "alumni":
    #         profile.profile_image = request.FILES.get("profile_image")
    #         profile.roll_no = request.POST.get("roll_no")
    #         profile.department = request.POST.get("department")
    #         profile.passout_year = request.POST.get("passout_year")
    #         profile.current_status = request.POST.get("current_status")
    #         profile.company = request.POST.get("company")
    #         profile.location = request.POST.get("location")
    #         profile.phone = request.POST.get("phone")
    #         profile.save()

    #     messages.success(request, "Account created successfully")
    #     return redirect("login")

    # return render(request, "register.html")

        Profile.objects.create(
            user=user,
            role=role,
            roll_no=request.POST.get("roll_no"),
            department=request.POST.get("department"),
            passout_year=request.POST.get("passout_year"),
            current_status=request.POST.get("current_status"),
            company=request.POST.get("company"),
            location=request.POST.get("location"),
            phone=request.POST.get("phone"),
        )

        if role == "admin":
            return redirect("admin_portal")
        return redirect("alumni_portal")

    return render(request, "register.html")

@login_required
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

@login_required
def alumni_dashboard(request):
    return render(request, "alumni_dashboard.html")

@login_required
def admin_view_alumni(request):
    if request.user.profile.role != "admin":
        return redirect("login")

    alumni_list = Profile.objects.filter(role="alumni")

    return render(request, "admin_view_alumni.html", {
        "alumni_list": alumni_list
    })

@login_required
def alumni_portal(request):
    event_count = Event.objects.filter(is_approved=True).count()
    return render(request, "alumni_portal.html", {
        "event_count": event_count
    })

@login_required
def admin_portal(request):
    return render(request, "admin_portal.html")


@login_required
def create_event(request):
    if request.method == "POST":
        Event.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            date=request.POST["date"],
            created_by=request.user
        )
        messages.success(request, "Event submitted for admin approval")
        return redirect("alumni_portal")

    return render(request, "create_event.html")

@login_required
def view_events(request):
    events = Event.objects.filter(is_approved=True)
    return render(request, "view_events.html", {"events": events})

@login_required
def admin_events(request):
    events = Event.objects.all()
    return render(request, "admin_events.html", {"events": events})

# @login_required
# def approve_event(request, id):
#     event = get_object_or_404(Event, id=id)
#     event.is_approved = True
#     event.is_rejected = False
#     event.save()
#     return redirect("admin_events")

# @login_required
# def reject_event(request, id):
#     event = get_object_or_404(Event, id=id)
#     event.is_rejected = True
#     event.is_approved = False
#     event.save()
#     return redirect("admin_events")

# 🔹 MANAGE EVENTS
def manage_events(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'manage_events.html', {'events': events})


# 🔹 EDIT EVENT
def edit_event(request, id):
    event = get_object_or_404(Event, id=id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('manage_events')
    else:
        form = EventForm(instance=event)

    return render(request, 'edit_event.html', {'form': form})


# 🔹 DELETE EVENT
def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    event.delete()
    return redirect('manage_events')

def create_job(request):
    if request.method == "POST":
        Job.objects.create(
            title=request.POST["title"],
            description=request.POST["description"]
        )
        return redirect("alumni_portal")

    return render(request, "create_job.html")

def view_jobs(request):
    jobs = Job.objects.all()
    return render(request, "view_jobs.html", {"jobs": jobs})


def post_job(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        Job.objects.create(
            title=title,
            description=description
        )
        return redirect("view_jobs")

    return render(request, "post_job.html")

# ===== ANNOUNCEMENTS =====
def announcements(request):
    announcements = Announcement.objects.all()
    return render(request, "announcements.html", {"announcements": announcements})

@login_required
def add_announcement(request):
    if request.method == "POST":
        Announcement.objects.create(
            title=request.POST["title"],
            message=request.POST["message"],
            image_url=request.POST.get('image_url', '')
        )
    return redirect("admin_announcements")



@login_required
def edit_announcement(request, id):
    announcement = Announcement.objects.get(id=id)

    if request.method == "POST":
        announcement.title = request.POST['title']
        announcement.message = request.POST['message']
        announcement.image_url = request.POST.get('image_url', '')
        announcement.save()

    return redirect('admin_announcements')

@login_required
def delete_announcement(request, id):
    ann = get_object_or_404(Announcement, id=id)
    ann.delete()
    return redirect("admin_announcements")


@login_required
def add_job(request):
    if request.method == "POST":
        Job.objects.create(
            title=request.POST.get("title"),
            company=request.POST.get("company"),
            description=request.POST.get("description"),
            posted_by=request.user
        )
        return redirect("alumni_portal")
    
    return render(request, "jobs/add_job.html")


@login_required
def view_alumni(request):
    alumni = Profile.objects.filter(role="alumni")
    return render(request, "admin_view_alumni.html", {"alumni": alumni})

@login_required
def admin_announcements(request):
    announcements = Announcement.objects.all()
    return render(request, "admin_announcements.html", {"announcements": announcements})

def is_admin(user):
    return user.is_staff
    
def alumni_announcements(request):
    announcements = Announcement.objects.all().order_by('-posted_on')
    return render(request, 'alumni_announcements.html', {
        'announcements': announcements
    })
@login_required
@user_passes_test(is_admin)
def manage_admin_events(request):
    events = Event.objects.all().order_by('-id')

    if request.method == "POST":
        event_id = request.POST.get("event_id")
        action = request.POST.get("action")
        event = get_object_or_404(Event, id=event_id)

        # APPROVE
        if action == "approve":
            event.is_approved = True
            event.is_rejected = False
            event.save()

        elif action == "reject":
            event.is_rejected = True
            event.is_approved = False
            event.save()

        elif action == "edit":
            event.title = request.POST.get("title")
            event.description = request.POST.get("description")
            event.date = request.POST.get("date")
            event.save()

        return redirect("admin_events")

    return render(request, "admin/admin_portal.html", {"events": events})