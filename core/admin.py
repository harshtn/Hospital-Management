from django.contrib import admin
from .models import Department, Room

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head_of_department', 'phone', 'created_at')
    search_fields = ('name', 'code', 'head_of_department')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'department', 'capacity', 'current_occupancy', 'status', 'cost_per_day')
    list_filter = ('room_type', 'status', 'department')
    search_fields = ('room_number',)

