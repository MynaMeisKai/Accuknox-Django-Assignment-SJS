from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display  = ('id','email','name' )
    list_per_page  = 15 
    
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(FriendRequests)
admin.site.register(Friendships)



