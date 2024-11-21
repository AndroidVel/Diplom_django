from django.db import models


# User model
class User(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


# Product model
class Product(models.Model):
    name = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    weight = models.DecimalField(decimal_places=2, max_digits=6)
    image_url = models.URLField()
    buyer = models.ManyToManyField(User, related_name='product')
