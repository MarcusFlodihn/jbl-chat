from django.db import models


class User(models.Model):
    username = models.fields.CharField(max_length=255)

    def to_json(self):
        return {"username": self.username}


class Message(models.Model):
    content = models.fields.CharField(max_length=255)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    created_at = models.DateTimeField(auto_now=True)

    def to_json(self):
        return {
            "content": self.content,
            "created_at": self.created_at
        }
