from django.urls import path
from authapp import views

urlpatterns = [
    path('',views.index, name="Index"),
    path('login/', views.Login, name='Login'),
    path('logout/', views.Logout, name='Logout'),
    path('register/', views.Register, name='Register'),
    path('fitness/', views.fitness, name='Fitness'),  # Fitness Tracking
    path('log-workout/', views.log_workout, name='LogWorkout'),
    path('save-workout/', views.SaveWorkout, name='SaveWorkout'),  # To handle form submission
    path('workout-history/', views.workout_history, name='WorkoutHistory'),
    path('nutrition/', views.nutrition, name='Nutrition'),  # Nutrition Tracking,
    path('log-nutrition/', views.log_nutrition, name='LogNutrition'),
    path('nutrition-history/', views.nutrition_history, name='NutritionHistory'),
    path('save-nutrition/', views.save_nutrition, name='SaveNutrition'),
    path('mental/', views.Mental, name='Mental'),  # Mental Wellness
    # path('mental/happy/', views.happy_details, name='HappyDetails'),
    # path('mental/sad/', views.sad_details, name='SadDetails'),
    # path('mental/stressed/', views.stressed_details, name='StressedDetails'),
    # path("mental/<str:mood>/", views.mood_details, name="MentalMoodDetails"),
    path('mental/<str:mood>/', views.mood_details, name='MoodDetails'),
    path('analytics/', views.analytics, name='Analytics'),  # Analytics
    # path('recommendation/', views.Recommendation, name='Recommendation'),
    path('home/', views.Home, name='Home'),  # Home page after login
]
