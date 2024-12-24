from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import WorkoutLogForm, NutritionLogForm
from .models import WorkoutLog, NutritionLog, MoodLog
import logging
from django.db.models import Count, Sum

logger = logging.getLogger(__name__)


# Home view
def index(request):
    return render(request, "index.html")


# Login view
def Login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("Home")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


# Register view
def Register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]
        if password == confirm_password:
            User.objects.create_user(username=username, email=email, password=password)
            return redirect("Home")
        else:
            return render(request, "register.html", {"error": "Passwords do not match"})
    return render(request, "register.html")


@login_required
def Home(request):
    return render(request, "index1.html")


# Logout view
def Logout(request):
    logout(request)
    return redirect("Index")


@login_required
def fitness(request):
    workout_logs = WorkoutLog.objects.filter(user=request.user).order_by("-date")
    return render(request, "fitness.html", {"workout_logs": workout_logs})


@login_required
def log_workout(request):
    if request.method == "POST":
        form = WorkoutLogForm(request.POST)
        if form.is_valid():
            workout_log = form.save(commit=False)
            workout_log.user = request.user
            workout_log.save()
            messages.success(request, "Workout logged successfully!")
            return redirect("Fitness")
        else:
            messages.error(request, "Error logging workout. Please check your input.")
    else:
        form = WorkoutLogForm()
    return render(request, "log_workout.html", {"form": form})


@login_required
def workout_history(request):
    workout_logs = WorkoutLog.objects.filter(user=request.user).order_by("-date")
    return render(request, "workout_history.html", {"workout_logs": workout_logs})


@login_required
def SaveWorkout(request):
    if request.method == "POST":
        form = WorkoutLogForm(request.POST)
        if form.is_valid():
            workout_log = form.save(commit=False)
            workout_log.user = request.user
            workout_log.save()
            messages.success(request, "Workout saved successfully!")
            return redirect("Fitness")
        else:
            messages.error(request, "Error saving workout. Please check your input.")
    else:
        form = WorkoutLogForm()
    return render(request, "log_workout.html", {"form": form})


@login_required
def nutrition(request):
    return render(request, "nutrition.html")


@login_required
def log_nutrition(request):
    if request.method == "POST":
        form = NutritionLogForm(request.POST)
        if form.is_valid():
            nutrition_log = form.save(commit=False)
            nutrition_log.user = request.user
            nutrition_log.save()
            return redirect("Nutrition")
    else:
        form = NutritionLogForm()
    return render(request, "log_nutrition.html", {"form": form})


@login_required
def nutrition_history(request):
    logs = NutritionLog.objects.filter(user=request.user).order_by("-date")
    return render(request, "nutrition_history.html", {"logs": logs})


@login_required
def save_nutrition(request):
    if request.method == "POST":
        form = NutritionLogForm(request.POST)
        if form.is_valid():
            nutrition_log = form.save(commit=False)
            nutrition_log.user = request.user
            nutrition_log.save()
            messages.success(request, "Nutrition log saved successfully!")
            return redirect("Nutrition")
    return redirect("LogNutrition")


@login_required
def Mental(request):
    if request.method == "POST":
        mood = request.POST.get("mood")
        if mood:
            MoodLog.objects.create(user=request.user, mood=mood)
            messages.success(request, f"Your mood '{mood}' has been logged successfully!")
            return redirect("Mental")
    return render(request, "mental.html")


@login_required
def mood_details(request, mood):
    mood_mapping = {
        "happy": {
            "title": "Happy Tips",
            "description": "Here are tips to amplify your happiness and enjoy the moment.",
            "tips": [
                "Smile often and practice gratitude.",
                "Spend time with loved ones.",
                "Engage in activities that bring you joy.",
            ],
        },
        "sad": {
            "title": "Dealing with Sadness",
            "description": "Here are some ways to cope with sadness and uplift your spirits.",
            "tips": [
                "Talk to a trusted friend or family member.",
                "Practice mindfulness and deep breathing.",
                "Engage in light physical activities like a walk.",
            ],
        },
        "stressed": {
            "title": "Stress Relief Tips",
            "description": "Try these strategies to alleviate stress and find calm.",
            "tips": [
                "Take deep breaths and meditate for 10 minutes.",
                "Create a to-do list and tackle one task at a time.",
                "Exercise or listen to relaxing music.",
            ],
        },
    }

    context = mood_mapping.get(
        mood.lower(),
        {"title": "Mood Details", "description": "No tips available.", "tips": []},
    )
    return render(request, "mental_mood_details.html", context)


@login_required
def analytics(request):
    mood_counts = (
        MoodLog.objects.filter(user=request.user)
        .values("mood")
        .annotate(count=Count("mood"))
    )

    mood_labels = [entry["mood"] for entry in mood_counts]
    mood_data = [entry["count"] for entry in mood_counts]

    workout_logs = WorkoutLog.objects.filter(user=request.user).order_by("-date")[:5]
    workout_labels = [log.date.strftime("%b %d") for log in workout_logs]
    workout_data = [log.calories_burned for log in workout_logs]

    nutrition_summary = NutritionLog.objects.filter(user=request.user).aggregate(
        total_protein=Sum("protein"),
        total_carbs=Sum("carbs"),
        total_fats=Sum("fats"),
    )
    nutrition_labels = ["Protein", "Carbs", "Fats"]
    nutrition_data = [
        nutrition_summary.get("total_protein", 0),
        nutrition_summary.get("total_carbs", 0),
        nutrition_summary.get("total_fats", 0),
    ]

    context = {
        "mood_labels": mood_labels,
        "mood_data": mood_data,
        "workout_labels": workout_labels,
        "workout_data": workout_data,
        "nutrition_labels": nutrition_labels,
        "nutrition_data": nutrition_data,
    }
    return render(request, "analytics.html", context)
