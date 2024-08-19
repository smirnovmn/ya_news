import pytest

from django.test.client import Client
from django.conf import settings
from django.utils import timezone

from datetime import datetime, timedelta

from news.forms import BAD_WORDS
from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Тестовый комментарий',
    )
    return comment


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def news_id(news):
    return news.id,


@pytest.fixture
def news_settings():
    today = datetime.today()
    all_news = [
        News(
            title='Заголовок',
            text=f'Текст{index} новости',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def form_data_comment():
    return {
        'text': 'Текст комментария',
    }


@pytest.fixture
def comments_settings(news, author):
    now = timezone.now()
    comments = [
        Comment.objects.create(
            news=news,
            author=author,
            text=f'Комментарий {index}',
            created=now + timedelta(days=index)
        )
        for index in range(5)
    ]
    return comments


@pytest.fixture
def form_comment():
    return {
        'text': 'Текст комментария',
    }


@pytest.fixture
def comment_bad_words_form():
    return {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}