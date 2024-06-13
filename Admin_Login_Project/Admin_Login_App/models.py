import datetime
import os
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from ckeditor.fields import RichTextField

# Create your models here.

def getFileName(request,filename):
    now_time = datetime.datetime.now().strftime('%Y%m%d%X')
    new_filename = "{}{}".format(now_time,filename)
    return os.path.join('Images/',new_filename)
 
def getlogo(request, filename):
    now_time = datetime.datetime.now().strftime('%Y%m%d%X')
    new_filename = "{}{}".format(now_time,filename)
    return os.path.join('logo/',new_filename)

def picture(request, filename):
    now_time = datetime.datetime.now().strftime('%Y%m%d%X')
    new_filename = "{}{}".format(now_time,filename)
    return os.path.join('picture/',new_filename)

def video(request, filename):
    now_time = datetime.datetime.now().strftime('%Y%m%d%X')
    new_filename = "{}{}".format(now_time,filename)
    return os.path.join('video/',new_filename)

def blog_images(request, filename):
    now_time = datetime.datetime.now().strftime('%Y%m%d%X')
    new_filename = "{}{}".format(now_time,filename)
    return os.path.join('media/',new_filename)

class AdminLoginManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        # User creation logic
        if not email:
            raise ValueError('User must have an email.')
        if not username:
            raise ValueError('User must have a username.')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        # Superuser creation logic
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class AdminLogin(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True, blank=False)
    email = models.CharField(max_length=150, unique=True, blank=False)
    password = models.CharField()
    ph_no = PhoneNumberField(region='US', unique=True, blank=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = AdminLoginManager()


class courses(models.Model):
    Title = models.CharField(max_length=100)
    Description = RichTextField()
    Technologies = models.CharField(max_length=150)
    Images = models.ImageField(upload_to= getFileName, blank=False)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True,blank=True)
    modified_by = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

class technologies(models.Model):
    Technologies = models.CharField(max_length=150)


# placement partners

class partners_logo(models.Model):
    name = models.CharField(max_length=100, default=None)
    logo = models.ImageField(upload_to=getlogo)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    created_by=models.IntegerField(null=True,blank=True)
    modified_by=models.IntegerField(null=True)
    is_active=models.BooleanField(default=True)
    is_deleted=models.BooleanField(default=False)

# testimonial 

class Testimonial(models.Model):
    student_name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=picture, blank=False)
    course = models.CharField(max_length=100)
    date = models.DateField()
    testimonial = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True,blank=True)
    modified_by = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

# Placement Stories

class PlacementStories(models.Model):
    student_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    testimonial_video = models.FileField(upload_to=video, blank=False)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True,blank=True)
    modified_by = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)


# FAQ

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True,blank=True)
    modified_by = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

# Blog

class Blog(models.Model):
    images = models.ImageField(upload_to=blog_images, blank=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    course = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True,blank=True)
    modified_by = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

# Careers

class Careers(models.Model):
    Logo = models.ImageField(upload_to=getlogo, blank=False)
    Job_Heading = models.CharField(max_length=100)
    Location = models.CharField(max_length=100)
    Experience = models.CharField(max_length=100)
    No_Of_Openings = models.CharField(max_length=100)
    Salary = models.FloatField()
    Status = models.BooleanField(default=True)

    Job_Type = models.CharField(max_length=100)
    Qualification = models.CharField(max_length=255)
    Job_Description = models.TextField()
    Skills_Required = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True,blank=True)
    modified_by = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)