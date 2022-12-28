from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()

TEXT_LEN: int = 15


class Category(models.Model):
    """Модель для работы с категория."""

    name = models.CharField(
        max_length=256,
        verbose_name='название категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='слаг поле'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для работы с жанрами."""

    name = models.CharField(
        max_length=256,
        verbose_name='название жанра'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='слаг жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для работы с произведениями."""

    name = models.CharField(max_length=256, verbose_name='название тайтла')
    year = models.IntegerField(db_index=True, verbose_name='год')
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='описание'
    )
    genre = models.ManyToManyField(
        Genre,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='title',
        null=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель для работы с отзывами."""

    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews'
                              )
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='оценка'
    )
    pub_date = models.DateTimeField('Дата публикации отзыва',
                                    auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author',
            )
        ]

    def __str__(self):
        return self.text[:TEXT_LEN]


class Comment(models.Model):
    """Модель для работы с комментариями к отзывам."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата добавления комментария', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-id']

    def __str__(self):
        return self.text[:TEXT_LEN]
