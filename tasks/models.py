from django.conf import settings
from django.db import models

class Task(models.Model):
    LOW = 'low'
    NORMAL = 'normal'
    HIGH = 'high'
    PRIORITIES = [(LOW, 'Низкий'), (NORMAL, 'Обычный'), (HIGH, 'Высокий')]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    date_added = models.DateTimeField('Создана', auto_now_add=True)
    due_date = models.DateTimeField('Срок выполнения', null=True, blank=True)
    priority = models.CharField('Приоритет', max_length=10, choices=PRIORITIES, default=NORMAL)
    completed = models.BooleanField('Выполнена', default=False)

    def __str__(self):
        return self.title
