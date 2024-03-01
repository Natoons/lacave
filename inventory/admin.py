from django.contrib import admin
from inventory.models import Product, UserProfile

admin.site.site_header = "Inventory Admin"
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display =  ('name', 'category', 'quantity')
    list_filter = ['category']
    search_fields = ['name']

class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ('user', 'physical_address', 'mobile', 'picture')
    list_filter = ['user']
    search_fields = ['user']

admin.site.register(Product, ProductAdmin)
admin.site.register(UserProfile, UserProfileAdmin)