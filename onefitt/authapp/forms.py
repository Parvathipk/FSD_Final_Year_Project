from django import forms
from .models import WorkoutLog
from .models import NutritionLog


class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        fields = ['workout_type', 'duration', 'calories_burned']

    def clean(self):
        cleaned_data = super().clean()
        workout_type = cleaned_data.get("workout_type")
        duration = cleaned_data.get("duration")
        calories_burned = cleaned_data.get("calories_burned")

        print("Cleaned Data:", cleaned_data)  # Debugging

        if not workout_type:
            self.add_error("workout_type", "Workout type is required.")
        if not duration or duration <= 0:
            self.add_error("duration", "Duration must be a positive number.")
        if not calories_burned or calories_burned <= 0:
            self.add_error("calories_burned", "Calories burned must be a positive number.")

        return cleaned_data



class NutritionLogForm(forms.ModelForm):
    class Meta:
        model = NutritionLog
        fields = ['meal_type', 'food_item', 'calories', 'protein', 'carbs', 'fats']
        widgets = {
            'meal_type': forms.Select(attrs={'class': 'form-control'}),
            'food_item': forms.TextInput(attrs={'class': 'form-control'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control'}),
            'carbs': forms.NumberInput(attrs={'class': 'form-control'}),
            'fats': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
       