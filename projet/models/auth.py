from django.db import models


class User(models.Model):
    is_admin = models.BooleanField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'


class Role(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'roles'


class UserRole(models.Model):
    role_id = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name='user_roles')
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_roles')

    class Meta:
        db_table = 'user_roles'


class LoginHistory(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='login_histories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'login_histories'
