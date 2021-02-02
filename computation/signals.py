from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
#for mailing address
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import *


@receiver(post_save, sender=User)
def create_staff(sender, instance, created,**kwargs):
    if created:
        user, create = Staff.objects.get_or_create(
            user= instance,
            name=instance.first_name,
            email= instance.email
        )

# @receiver(post_save, sender=User)
# def update_staff(sender, instance, created, **kwargs):
#     if created == False:
#         instance.save()
#         print('staff updated') 


@receiver(post_save, sender=User)
def userPasswordCreation(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(username=instance.username, email=instance.email)
        userEmail = user.email
        userN =len(user.username)
        a,b = userEmail.split('@')
        userPass = a+str(userN)
        print(userPass)

        if created:
            user.set_password(userPass)
            user.save()
            #sending the password to the user
            

            subject = 'Password to Login into the System'
            html_message = render_to_string('computation/password_email.html',{'name':instance.username,'password':userPass})
            plain_message = strip_tags(html_message)
            from_email = 'abdulahiopeyemiq@gmail.com'
            to = instance.email

            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)



     # subject, from_email, to = 'LOG-IN PASSWORD','abdulahiopeyemiq@gmail.com', instance.email
        # text_content = 'this email help to reset password.'
        # html_content = 'your password for {} is {}'.format(instance.username, userPass)
        # msg = EmailMultiAlternatives(subject,text_content,from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()
    # user = User.objects.filter(username=instance.username, email=instance.email)
    # user.update(password=userPass)
    # user.set_password(userPass)
    # user.save(update_fields=['password'])






