from django.db import models
from django.urls import reverse


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )  # внешний ключ на эту же модель
    menu_name = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)  # явно заданное URL
    named_url = models.CharField(max_length=100, blank=True)  # имя URL
    order = models.PositiveIntegerField(default=0)  # позиция в пределах одного уровня
    

    class Meta:
        ordering = ["order"]  # сортировка

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("menu", args=(self.named_url,))

