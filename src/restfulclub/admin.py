from django.contrib import admin
from .models import Match, Suite, Reservation, User

admin.site.register(Match)
admin.site.register(Suite)
admin.site.register(Reservation)
admin.site.register(User)

# Register your models here.
