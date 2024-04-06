from django.db import models

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    is_done = models.BooleanField()
    priority = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.title}'

