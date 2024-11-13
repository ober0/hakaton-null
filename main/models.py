from django.db import models


class Question(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        verbose_name = "Вопрос"


class Nutrition(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка", choices=[(i, i) for i in range(1, 6)])
    message = models.TextField(verbose_name="Сообщение")

    def __str__(self):
        return f"{self.name} - Оценка: {self.rating}"

    class Meta:
        verbose_name = "Отзыв о питании"
        verbose_name_plural = "Отзывы о питании"