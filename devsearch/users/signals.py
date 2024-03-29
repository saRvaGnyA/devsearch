from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User  # the default user model for auth
from .models import Profile
# from django.dispatch import receiver


# @receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    # sender is the model that sends this
    # instance is the instance of the model that actually triggered this
    # created is a boolean which will let us know if a new user was added and saved to the DB or an existing user was edited and saved
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    # since profile and user have a one-to-one relationship, we can do both
    # req.user.profile and profile.user
    if created == False:
        # update user profile
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    # the instance is a profile, and we access the one-to-one relationship
    user.delete()


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
