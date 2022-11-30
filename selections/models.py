from django.db import models
from ads.models import Advertisement

class Collection(models.Model):

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"

    slug = models.SlugField(max_length=50)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    items = models.ManyToManyField(Advertisement)


    # def get_dict(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'author': self.author.get_dict(),
    #         'price': self.price,
    #         'description': self.description,
    #         'is_published': self.is_published,
    #         'image': self.image.name,
    #         'category': self.category.get_dict(),
    #     }

    def __str__(self):
        return self.name
