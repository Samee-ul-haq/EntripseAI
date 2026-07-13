from django.db import models
from django.conf import settings

import uuid

class User(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True)
    userName = models.CharField(max_length=100)

    def __str__(self):
        return self.userName


class conversation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='conversations')
    history = models.TextField()
    documents = models.FieldFile(upload_to='',blank=True,null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation for {self.user.userName}"
