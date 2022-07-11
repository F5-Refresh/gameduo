import uuid

from core.models import TimeStampModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, user_id, nickname, password=None):
        if not user_id:
            raise ValueError('Users must have an user id')

        user = self.model(
            user_id=user_id,
            nickname=nickname,
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, nickname, password=None):
        user = self.create_user(
            user_id=user_id,
            password=password,
            nickname=nickname,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, TimeStampModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    is_admin = models.BooleanField(default=False)
    delete_flag = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = [
        'nickname',
    ]

    def __str__(self):
<<<<<<< HEAD
        return f'{self.nickname}({self.user_id})'
=======
        return f'{self.nickname}({self.email})'
>>>>>>> 859e607 (feat: DB 모델링 적용 (#2))

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'user'
