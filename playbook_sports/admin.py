from django.contrib import admin
from .models import Sport, User, Team
admin.site.register(User)
admin.site.register(Team)
admin.site.register(Sport)
# Register your models here.
