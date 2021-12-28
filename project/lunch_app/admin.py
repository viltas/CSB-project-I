from django.contrib import admin
from .models import Choice, Lunch


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class LunchAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['lunch']}),
        ('Date', {'fields': ['date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Lunch, LunchAdmin)