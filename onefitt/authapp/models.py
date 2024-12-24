from django.db import models
from django.contrib.auth.models import User

class WorkoutLog(models.Model):
    WORKOUT_CHOICES = [
        ('Cardio', 'Cardio'),
        ('Strength', 'Strength'),
        ('Yoga', 'Yoga'),
        ('Swimming', 'Swimming'),
        ('Cycling', 'Cycling'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_type = models.CharField(max_length=100, choices=WORKOUT_CHOICES)
    duration = models.PositiveIntegerField()  # Duration in minutes
    calories_burned = models.PositiveIntegerField(default=0)  # Calories burned
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.workout_type} ({self.date.strftime('%Y-%m-%d %H:%M:%S')})"


class NutritionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    meal_type = models.CharField(max_length=50)
    food_item = models.CharField(max_length=255)
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fats = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.food_item} ({self.date})"

    

class MoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to user
    mood = models.CharField(max_length=50)  # e.g., Happy, Sad, etc.
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically logs the time of entry

    def __str__(self):
        return f"{self.user.username} - {self.mood} - {self.timestamp}"

