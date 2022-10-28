from site import USER_BASE
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.files import File
from pathlib import Path
from io import BytesIO
import os
from PIL import Image, ImageOps
# Create your models here.s
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from pkg_resources import require

User._meta.get_field('email')._unique = True

TIMEZONES = (
    ('-12:00','(GMT -12:00)'),
    ('-11:00','(GMT -11:00)'),
    ('-10:00','(GMT -10:00)'),
    ( '-09:00','(GMT -09:00)'),
    ( '-08:00','(GMT -08:00)'),
    ( '-07:00','(GMT -07:00)'),
    ( '-06:00','(GMT -06:00)'),
    ( '-05:00','(GMT -05:00)'),
    ( '-04:00','(GMT -04:00)'),
    ( '-03:00','(GMT -03:00)'),
    ( '-02:00','(GMT -02:00)'),
    ( '-01:00','(GMT -01:00)'),
    ( '+00:00','(GMT)'),
    ( '+01:00','(GMT +01:00)'),
    ( '+02:00','(GMT +02:00)'),
    ( '+03:00','(GMT +03:00)'),
    ( '+04:00','(GMT +04:00)'),
    ( '+05:00','(GMT +05:00)'),
    ( '+06:00','(GMT +06:00)'),
    ( '+07:00','(GMT +07:00)'),
    ( '+08:00','(GMT +08:00)'),
    ( '+09:00','(GMT +09:00)'),
    ( '+10:00','(GMT +10:00)'),
    ( '+11:00','(GMT +11:00)'),
    ( '+12:00','(GMT +12:00)'),
)

def _path_and_rename(instance,filename):
    upload_to = 'profiles/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format("mamamia", ext)
        print("FILENAME",filename)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

def file_size(value): # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')    

class Developer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=False, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    timezone = models.CharField(max_length=6, choices=TIMEZONES, default='+00:00')
    hero = models.CharField(max_length=50, blank=False, null=True)
    bio = models.TextField(null=True, blank=False)
    pay_rate=models.BigIntegerField(null=True, blank=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles/', default="profiles/user-default.png",validators=[file_size])
    social_github = models.URLField(max_length=200, blank=True, null=True)
    social_twitter = models.URLField(max_length=200, blank=True, null=True)
    social_linkedin = models.URLField(max_length=200, blank=True, null=True)
    social_website = models.URLField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['created']

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        print(url)
        return url
    def save(self, *args, **kwargs):
        _image_resize(self.user.id, self.profile_image, 400, 400)
        super().save(*args, **kwargs)

class RoleType(models.Model):
    developer_id = models.ForeignKey(
        Developer, on_delete=models.CASCADE, null=True, blank=True)
    part_time_contract = models.BooleanField(default=False, null=True)
    full_time_contract = models.BooleanField(default=False, null=True)
    full_time_job = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.developer_id)

class RoleLevel(models.Model):
    developer_id = models.ForeignKey(
        Developer, on_delete=models.CASCADE, null=True, blank=True)
    junior = models.BooleanField(default=False, null=True)
    mid = models.BooleanField(default=False, null=True)
    senior = models.BooleanField(default=False, null=True)
    principal = models.BooleanField(default=False, null=True)
    c_level = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.developer_id)

class Availability(models.Model):
    developer_id = models.ForeignKey(
        Developer, on_delete=models.CASCADE, null=True, blank=True)
    available = models.BooleanField(default=False, null=True)
    open = models.BooleanField(default=False, null=True)
    not_available = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.developer_id)

class Skill(models.Model):
    owner = models.ForeignKey(
        Developer, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)

class Verifications(models.Model):
    verification_code = models.CharField(verbose_name="vericiation Code",max_length=128,null=True, blank=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)


class Business(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    is_payed=models.BooleanField(default=False,null=True)
    is_active=models.BooleanField(default=True,null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='business/', default="business-profiles/user-default.png",validators=[file_size])
    def __str__(self):
        return str(self.name)

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url
    def save(self, *args, **kwargs):
        _image_resize(self.user.id, self.profile_image, 300, 300,True)
        super().save(*args, **kwargs)

class Conversation(models.Model):
    developer_id = models.ForeignKey(Developer, on_delete=models.CASCADE, null=True, blank=True)
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.developer_id.name +' | '+ self.business_id.name

class Message(models.Model):
    sender_id =  models.UUIDField()
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,null=True, blank=True)
    sender_type = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.body

    class Meta:
        ordering = ['is_read', '-created']


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.user.email




image_types = {
    "jpg": "JPEG",
    "JPG": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
}


def _image_resize(userId,image, width, height, business=False):
    # Open the image using Pillow
    img = Image.open(image)
    # check if either the width or height is greater than the max
    if img.width > width or img.height > height:
        output_size = (width, height)
        # Create a new resized “thumbnail” version of the image with Pillow
        img.thumbnail(output_size)
        # Find the file name of the image
        # Spilt the filename on “.” to get the file extension only
        img_suffix = Path(image.file.name).name.split(".")[-1]
        # Use the file extension to determine the file type from the image_types dictionary

        img_format = image_types[img_suffix]
        # Save the resized image into the buffer, noting the correct file type
        buffer = BytesIO()
        img.save(buffer, format=img_format)
        # Wrap the buffer in File object
        file_object = File(buffer)
        # Save the new resized file as usual, which will save to S3 using django-storages
        yeaimage = f'user_{userId}_developer.{img_format}'       
        if business:
            yeaimage = yeaimage = f'user_{userId}_business.{img_format}' 
        image.save(yeaimage, file_object)
