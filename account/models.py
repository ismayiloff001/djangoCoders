from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from ckeditor.fields import RichTextField
from django.db import models
from services.generator import Generator



# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(
            self, email, password=None, is_activate=True, is_staff=False, is_superuser=False
    ):
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_activate = is_activate
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user=self.create_user(email=self.normalize_email(email), password=password)
        user.us_staff = True
        user.is_superuser=True
        user.save(using=self._db)
        return user

def upload_to(instance, filename):
    return "{}/{}/{}".format("accounts", instance.slug, filename)


class MyUser(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=120, blank=True, null=True)
    fullname = models.CharField(max_length=40, blank=True, null=True)
    photo = models.ImageField(upload_to=upload_to, blank=True, null=True)

    slug = models.SlugField(unique=True, blank=True, null=True)

    # activation_code = models.SlugField(blank=True, null=True)
    activation_code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    password_reset_code = models.CharField(max_length=120, blank=True, null=True)
    reset_code_expires_at = models.DateTimeField(null=True, blank=True)
    activation_code_expires_at = models.DateTimeField(blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "MyUser"
        verbose_name_plural = "MyUser"

    def _str_(self):
        return self.email
    
    def get_full_name(self):
        return self.fullname
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return True
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Generator.create_slug_shortcode(size=15, model_=MyUser)
        return super(MyUser,self).save(*args, **kwargs)