from django.contrib import admin
from .models import User, Lead, Agent, UserProfile, Category, FollowUp

# Register your models here.


class LeadAdmin(admin.ModelAdmin):
    # fields = (
    #     'first_name',
    #     'last_name',
    # )
    list_display = ['first_name', 'last_name', 'age', 'email']
    list_display_links = ['first_name']
    list_editable = ['last_name']
    list_filter = ['category', 'first_name']
    search_fields = ['first_name', 'last_name']


admin.site.register(Agent)
admin.site.register(Category)
admin.site.register(FollowUp)
admin.site.register(Lead, LeadAdmin)
admin.site.register(User)
admin.site.register(UserProfile)
