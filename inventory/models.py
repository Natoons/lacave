from email.policy import default
from django.db import models
from django.contrib.auth.models import User

CATEGORY = (
    ('DryFly GIN', 'DryFly GIN'),
    ('Rocky Mountain GIN', 'Rocky Mountain GIN'),
    ('Few American GIN', 'Few American GIN'),
    ('DryFly Vodka', 'DryFly Vodka'),
    ('Hooch Vodka Citron', 'Hooch Vodka Citron'),
    ('Journeyman Whisky', 'Journeyman Whisky'),
    ('FireWater Whisky', 'FireWater Whisky'),
    ('Tequila', 'Tequila'),
    ('Violetta', 'Violetta'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    physical_address = models.CharField(max_length=40, null=True)
    mobile = models.CharField(max_length=12, null=True)
    picture = models.ImageField(default='avatar.jpeg' ,upload_to='Pictures')

    def __str__(self) -> str:
        return self.user.username


class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY, null=True)
    quantity = models.PositiveIntegerField(null=True)
    description = models.CharField(max_length=200, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=100, choices=[(user.username, user.username) for user in User.objects.all()])

    def __str__(self) -> str:
        return self.name
