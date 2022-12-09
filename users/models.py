from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    MEMBER = 'member'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (MEMBER, 'пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'администратор')
    ]
    slug = models.SlugField(max_length=50, null=True)
    role = models.CharField(max_length=20, choices=ROLES, default='member')
    age = models.PositiveSmallIntegerField()
    birth_date = models.DateField()
    email = models.EmailField(unique=True)
    location = models.ForeignKey('ads.Location', null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['username']
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.id}: {self.first_name} {self.last_name}"

    def get_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'role': self.role,
            'age': self.age,
            'total_published_ads': self.advertisement_set.filter(is_published=True).count(),
            'location': self.location.get_dict(),
        }
