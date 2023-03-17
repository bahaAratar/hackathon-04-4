from django.db import models
from project.models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='orders')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)


    def complete(self):
        if self.executor:
            self.is_available = False
            self.is_accepted = True
            self.save()

    def can_rate(self, user):
        if self.is_available or not self.is_accepted:
            return False
        return user in [self.owner, self.executor]

    def get_rating_for_user(self, user):
        if user == self.owner:
            return self.executor_rating
        elif user == self.executor:
            return self.owner_rating
        return None

    @property
    def executor_rating(self):
        ratings = self.rating_set.filter(user=self.executor)
        if not ratings:
            return None
        return sum([rating.rating for rating in ratings]) / len(ratings)

    @property
    def owner_rating(self):
        ratings = self.rating_set.filter(user=self.owner)
        if not ratings:
            return None
        return sum([rating.rating for rating in ratings]) / len(ratings)


class Rating(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='ratings')
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.project} rated by {self.user}'

    class Meta:
        unique_together = ('project', 'user')
