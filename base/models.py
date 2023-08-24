from django.db import models


# Create your models here.

from component.base_model import BaseModel


# 用户-数据来自于统一权限
class UserInfo(BaseModel):
    phone = models.CharField(max_length=128, null=True, blank=True)
    username = models.CharField(max_length=128)
    email = models.CharField(max_length=255)
    ch_name = models.CharField(max_length=255)
    role = models.IntegerField()
    is_activate = models.BooleanField(default=True)
    icon_url = models.CharField(max_length=255)

    class Meta:
        db_table = "user_info"

    def to_base_dict(self):
        dt = {
            "id": self.id,
            "username": self.username,
            "ch_name": self.ch_name,
        }
        return dt

    def to_nest_dict(self):
        dt = {
            "username": self.username,
            "ch_name": self.ch_name,
        }
        return dt

    def to_dict(self):
        dt = {
            "phone": self.phone,
            "username": self.username,
            "email": self.email,
            "ch_name": self.ch_name,
            "role": self.role,
            "icon_url": self.icon_url
        }
        return dt

    def to_member_dict(self):
        dt = {
            "phone": self.phone,
            "username": self.username,
            "email": self.email,
            "ch_name": self.ch_name,
        }
        return dt

    def to_code_dict(self):
        dt = {
            "id": self.id,
            "phone": self.phone,
            "username": self.username,
            "ch_name": self.ch_name,
        }
        return dt

    def to_role_dict(self):
        dt = {
            "id": self.id,
            "phone": self.phone,
            "username": self.username,
            "ch_name": self.ch_name,
        }
        return dt

    def to_user_info_dict(self):
        dt = {
            "phone": self.phone,
            "username": self.username,
            "email": self.email,
            "ch_name": self.ch_name,
            "role": self.role,
            # "icon_url": self.icon_url
        }
        return dt

