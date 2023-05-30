from core.models import PublishedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class PublishedManager(models.Manager):
    def get_filter_for_post(self):
        return self.filter(
            pub_date__lte=timezone.now(),
            is_published=True)


class Post(PublishedModel):
    title = models.CharField(verbose_name='Заголовок', max_length=256)
    text = models.TextField(verbose_name='Текст', blank=True, null=False)
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        blank=True, null=False,
        help_text='Если установить дату и время в будущем — '
        'можно делать отложенные публикации.')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               blank=True,
                               null=False,
                               verbose_name='Автор публикации')
    location = models.ForeignKey('Location', on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True,
                                 verbose_name='Местоположение')
    category = models.ForeignKey('Category',
                                 on_delete=models.SET_NULL,
                                 blank=False, null=True,
                                 verbose_name='Категория')
    image = models.ImageField('Фото', upload_to='posts_images',
                              blank=True)

    objects = PublishedManager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'id': self.pk})


class Category(PublishedModel):
    title = models.CharField(verbose_name='Заголовок', max_length=256)
    description = models.TextField(verbose_name='Описание',
                                   blank=True,
                                   null=False)
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL; '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.')

    objects = PublishedManager()

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField('Название места', max_length=256)

    objects = PublishedManager()

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField('комментарий', max_length=256)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comment',
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментария'
        ordering = ('created_at',)
