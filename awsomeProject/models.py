from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
#from django.contrib.auth.models import AbstractUser

class UserProfile(models.Model):
    #TODO add profilePicture attribute
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    isDeveloper = models.BooleanField()

class Game(models.Model):
    name = models.CharField(max_length=255, unique=True)
    url = models.URLField()
    price = models.FloatField()
    description = models.TextField(default='')

class DeveloperGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #on_delete=models.CASCADE deletes the entries if the entry in the UserProfile table gets deleed
    game = models.ForeignKey('Game', on_delete=models.CASCADE)

class Scores(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    score = models.FloatField()

class Gameplay(models.Model):
    #TODO: user and game should be unique as combination if possible
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    game = models.ForeignKey('Game', on_delete=models.CASCADE)

class PlayerItem(models.Model):
    gameplay = models.ForeignKey('Gameplay', on_delete=models.CASCADE)
    itemName = models.CharField(max_length=255)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    game = models.ForeignKey('Game', on_delete = models.CASCADE)
    commentText = models.TextField()
    created = models.DateTimeField(default=now, editable=False)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    game = models.ForeignKey('Game', on_delete = models.CASCADE)
    rating = models.IntegerField()

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    game = models.ForeignKey('Game', on_delete = models.CASCADE)
