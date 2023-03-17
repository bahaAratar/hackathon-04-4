from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    title = models.SlugField(primary_key=True,unique=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.title}'


class Project(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    experience = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='executer', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    is_accepted = models.BooleanField(default=False)#для добавления возможности приема другим лицом заказа
    is_complete = models.BooleanField(default=False)#для возможности ставить рейтинг
    candidates = models.ManyToManyField(User, related_name='projects_candidate', blank=True)

    def __str__(self):
        return self.description[:50]
