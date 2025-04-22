from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return self.username

class ChatMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Технологии'),
        ('science', 'Наука'),
        ('health', 'Здоровье'),
        ('education', 'Образование'),
    ]

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    url = models.URLField(verbose_name="Ссылка на статью", default="https://example.com")
    image_url = models.URLField(verbose_name="URL изображения", default="https://via.placeholder.com/350x200")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='tech', verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
    
    def __str__(self):
        return self.title