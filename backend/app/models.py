from django.db import models
from django.conf import settings

import uuid

class User(models.Model):
    id = models.UUIDField(default=uuid.uuid4,unique=True)
    userName = models.CharField(max_length=100)


class conversation(models.Model):
    _id = models.ForeignKey(id,on_delete=models.CASCADE)
    history = models.TextField()
    documents = models.FieldFile(upload_to='')
    message = models.TextField()
