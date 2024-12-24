from django.contrib import admin
from .models import NutritionLog
from .models import WorkoutLog, MoodLog
# Register your models here.


admin.site.register(NutritionLog)
admin.site.register(WorkoutLog)
admin.site.register(MoodLog)

