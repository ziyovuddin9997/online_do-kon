from django.contrib import admin

from django.contrib.auth.models import Group

from app_main.models import Category, Product, User, Cart, Transaction


admin.site.site_header = "Boshqaruv paneli"  # Login page & top banner
admin.site.site_title = "Admin panel"           # HTML <title> tag
admin.site.index_title = "Online do'konga xush kelibsiz" # Top of admin index page

admin.site.unregister(Group)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Cart)
admin.site.register(Transaction)
