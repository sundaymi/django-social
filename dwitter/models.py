from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user1 = User.objects.create_user()
    #first_name = models.CharField(max_length=50)
    #last_name = models.CharField(max_length=50)
    #user_email = models.EmailField()
    #password = models.CharField()
    #confirm_password = models.CharField()
    
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)

    def __str__(self) :
        return self.user.username 
        

#this function should be outside of Profile class
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()
        
#Create a profile for each new user
# post_save.connect(create_profile, sender=User) 
#we do this by passing User as a keyword argument 

class Dweet(models.Model):
    user = models.ForeignKey(User, related_name="dweets", on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return (f"{self.user}" f"({self.created_at:%Y-%m-%d %H:%M}): " f"{self.body[:30]}...")

