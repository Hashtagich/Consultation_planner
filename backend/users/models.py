from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission)


class Role(models.Model):
    title = models.CharField(
        'Название',
        max_length=64,
    )

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.title


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **kwargs):
        is_staff = kwargs.pop('is_staff', False)
        is_superuser = kwargs.pop('is_superuser', False)
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=True,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password, **kwargs):
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, role, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        role = Role(id=role)
        kwargs.setdefault('role', role)

        return self._create_user(email=email, password=password, **kwargs)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=128,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=128,
        blank=True,
        null=True,
    )
    middle_name = models.CharField(
        verbose_name='Отчество',
        max_length=128,
        blank=True,
        null=True,
    )
    role = models.ForeignKey(
        verbose_name='Роль',
        to=Role,
        on_delete=models.PROTECT,
        related_name='role',
        null=True,
        blank=True,
    )
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=15,
        blank=True,
        null=True,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Email',
        null=False,
        unique=True,
    )
    is_staff = models.BooleanField(
        verbose_name='Суперпользователь',
        default=False
    )
    is_active = models.BooleanField(
        verbose_name='Активен',
        default=True
    )

    is_blocked = models.BooleanField(
        verbose_name='Заблокирован',
        default=False
    )

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'first_name',
        'last_name',
        'middle_name',
        'role',
        'password',
    )

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        # ordering = ('-id',)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'
