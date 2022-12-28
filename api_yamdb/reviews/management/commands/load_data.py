import logging
import sys
from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(
    logging.Formatter(LOG_FORMAT)
)


logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)


files_to_download = {User: 'static/data/users.csv',
                     Category: 'static/data/category.csv',
                     Genre: 'static/data/genre.csv',
                     Title: 'static/data/titles.csv',
                     Review: 'static/data/review.csv',
                     Comment: 'static/data/comments.csv',
                     }


class Command(BaseCommand):
    """Класс реализует загрузку данных из csv в таблицы моделей проекта."""

    help = 'Загрузка данных из .csv в модели проекта.'

    def handle(self, *args, **options):
        for model, file in files_to_download.items():
            logger.info(f'Загрузка данных из файла {file} в модель {model}...')

            for row in DictReader(open(f'./{file}')):
                obj = model.objects.create(**row)
                obj.save()
        logger.info('Загрузка данных завершена!')
