from django.db import models

# Create your models here.
class Button(models.Model):
    button = models.CharField(max_length=200)

    def __str__(self):
        return self.button


class Text(models.Model):
    button = models.ForeignKey(Button, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)

    def __str__(self):
        return self.text

