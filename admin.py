from django.contrib import admin
from .models import Profile, Event

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "roll_no",
        "department",
        "passout_year",
        "company",
        "location",
    )
    list_filter = ("role", "department", "passout_year")
    search_fields = ("user__username", "roll_no", "company")
    
admin.site.register(Event)
