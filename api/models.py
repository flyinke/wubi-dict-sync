from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=255, blank=True)
    invitation_code = models.CharField(max_length=255, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class WubiDict(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    content_size = models.IntegerField()
    word_count = models.IntegerField()
    date_init = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'title')

class WubiCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    sort_id = models.IntegerField()
    date_init = models.DateTimeField(auto_now_add=True)

class WubiWord(models.Model):
    word = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    priority = models.IntegerField(default=0)
    up = models.IntegerField(default=0)
    down = models.IntegerField(default=0)
    date_create = models.DateTimeField(auto_now_add=True)
    date_modify = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True)
    user_init = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wubi_words_created')
    user_modify = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wubi_words_modified')
    category = models.ForeignKey(WubiCategory, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)