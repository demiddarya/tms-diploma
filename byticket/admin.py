from django.contrib import admin
from .models import CustomUser, Cinema, Category, Movie, Screening, PurchasedTicket


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'created_at', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'created_at']
    list_filter = ['is_active', 'is_staff']


admin.site.register(CustomUser, CustomUserAdmin)


class CinemaAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
    search_fields = ['name', 'address']


admin.site.register(Cinema, CinemaAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


admin.site.register(Category, CategoryAdmin)


class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'category']
    search_fields = ['title', 'description']


admin.site.register(Movie, MovieAdmin)


class ScreeningAdmin(admin.ModelAdmin):
    list_display = ['movie', 'cinema', 'start_time', 'seats_count', 'price']
    list_filter = ['cinema', 'movie', 'start_time']


admin.site.register(Screening, ScreeningAdmin)


class PurchasedTicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'screening', 'seat_number', 'purchase_time']
    search_fields = ['user__username', 'screening__movie__title', 'screening__cinema__name']
    list_filter = ['screening__cinema', 'screening__movie']


admin.site.register(PurchasedTicket, PurchasedTicketAdmin)
