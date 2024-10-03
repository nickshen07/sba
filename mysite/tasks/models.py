from django.db import models

class Task(models.Model):
    taskid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255, default=None, null = True)
    label=models.CharField(max_length=255, default=None, null = True)
    status=models.BooleanField(default=False, null = True)
    deadline=models.DateTimeField(default=None, null = True)
    image = models.ImageField(upload_to='img')
    def __str__(self):
        return str(self.taskid) + '. ' + self.title


