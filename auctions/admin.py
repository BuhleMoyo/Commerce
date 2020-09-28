from django.contrib import admin

# Register your models here.
from auctions.models import Listing, Comment, Bid, User

admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(User)