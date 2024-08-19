import pytest

from http import HTTPStatus

from django.urls import reverse
from django.conf import settings


@pytest.mark.django_db
def test_news_count(client, news_settings):
    url = reverse('news:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, news_settings):
    url = reverse('news:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    object_list = response.context['object_list']
    comments_dates = [comment.date for comment in object_list]
    assert comments_dates == sorted(comments_dates, reverse=True)


@pytest.mark.django_db
def test_comments_order(client, news, comments_settings):
    url = reverse('news:detail', args=[news.id])
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    comments_list = response.context.get('comments', [])
    comments_dates = [comment.created for comment in comments_list]
    assert comments_dates == sorted(comments_dates)


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert 'form' not in response.context