from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.utils import timezone
from django.utils.safestring import mark_safe
from tinymce.models import HTMLField


# Create your models here.

class News(models.Model):
    id = models.AutoField(primary_key=True)
    chat_id = models.IntegerField(verbose_name="ID чата с пользователем")
    user_name = models.CharField(unique=False, verbose_name="Telegram username")
    content = models.TextField(verbose_name="Содержание новости")
    send_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата поступления новости")

    def __str__(self):
        return f'Новость № {self.id}'

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'


class Image(models.Model):
    news = models.ForeignKey(News, on_delete = models.CASCADE)
    path = models.ImageField(unique=False, verbose_name="Название файла")

    def image_path(self):
        from django.utils.html import escape
        return mark_safe('<img src="/%s" width="350" height="350" />' % (self.path))
    image_path.short_description = 'Image'
    image_path.allow_tags = True

    def __str__(self):
        return f'Изображение: {self.path}'

    class Meta:
        verbose_name = 'Изображения'
        verbose_name_plural = 'Изображения'


class EntryPoint(models.Model):
    content = HTMLField( verbose_name="Текст", blank=False)
    path = models.ImageField(null=True, blank=False,  verbose_name="Изображение")

    def __str__(self):
        return 'Приветственное сообщение'

    class Meta:
        verbose_name = 'Приветственное сообщение'
        verbose_name_plural = 'Приветственное сообщение'


class SendNews(models.Model):
    content = HTMLField( verbose_name="Текст", blank=False)
    content_failed_news = HTMLField( verbose_name="Текст, когда прислали данные без текста", blank=False)
    content_failed_data = HTMLField( verbose_name="Текст, когда присланы неправильные данные", blank=False)
    content_accept_news = HTMLField( verbose_name="Текст, когда новость принята", blank=False)

    def __str__(self):
        return 'Предложить новость'

    class Meta:
        verbose_name = 'Предложить новость'
        verbose_name_plural = 'Предложить новость'


class AsqQuestion(models.Model):
    content = HTMLField( verbose_name="Текст")
    button_name = models.CharField(max_length=20, null=True, blank=False,  verbose_name="Текст кнопки")
    url = models.URLField( verbose_name="Ссылка для перенаправления", blank=False)

    def __str__(self):
        return 'Задать вопрос'

    class Meta:
        verbose_name = 'Задать вопрос'
        verbose_name_plural = 'Задать вопрос'


class AboutProjectContent(models.Model):
    content = HTMLField( verbose_name="Текст", blank=False)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Узнать о проектах: Заголовок'
        verbose_name_plural = 'Узнать о проектах: Заголовок'

class AboutProjectButton(models.Model):
    button_name = models.CharField(max_length=20, null=True, blank=False,  verbose_name="Текст кнопки")
    url = models.URLField( verbose_name="Ссылка для перенаправления", blank=False)

    def __str__(self):
        return f'Кнопка: {self.button_name}'

    class Meta:
        verbose_name = 'Узнать о проектах: кнопки'
        verbose_name_plural = 'Узнать о проектах: кнопки'


class Contact(models.Model):
    content = HTMLField(verbose_name="Текст", blank=False)

    def __str__(self):
        return 'Контакты'

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'


class JustSend(models.Model):
    content = HTMLField(verbose_name="Текст", blank=False)
    path = models.ImageField(null=True, blank=False, verbose_name="Изображение")

    def __str__(self):
        return 'Просто нажать'

    class Meta:
        verbose_name = 'Просто нажать'
        verbose_name_plural = 'Просто нажать'


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self,chat_id, password, **extra_fields):
        chat_id = self.model.normalize_username(chat_id)
        user = self.model(chat_id=chat_id,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, chat_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(chat_id, password, **extra_fields)

    def create_superuser(self, chat_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(chat_id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    chat_id = models.IntegerField(unique=True, verbose_name="ID диалога")
    user_id = models.IntegerField(null=True, verbose_name="ID пользователя")
    username = models.CharField(unique=False, null=True, verbose_name="Telegram username")
    first_name = models.CharField(unique=False, null=True, verbose_name="Telegram имя")
    last_name = models.CharField(unique=False, null=True, verbose_name="Telegram фамилия")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Дата и время,первого захода в бота")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'chat_id'
    REQUIRED_FIELDS = []
    objects = UserManager()
    def __str__(self):
        return 'Пользователь'

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"






