from django.db import models

#登录用户
class Login_User(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)


