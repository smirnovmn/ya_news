from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError
from django.urls import reverse

from news.models import Comment
from news.forms import WARNING


def test_user_can_create_comment(
    author_client, author, form_comment, news
):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=form_comment)
    assert response.status_code == HTTPStatus.FOUND
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_comment['text']
    assert new_comment.author == author


@pytest.mark.django_db
def test_anonim_cant_create_comment(client, form_comment, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.post(url, data=form_comment)
    expected_redirect_url = f'/auth/login/?next={url}'
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == expected_redirect_url
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_cant_use_bad_words(
    news, author_client, comment_bad_words_form
):
    excepted_comment_count = Comment.objects.count()
    url = reverse('news:detail', args=[news.id])
    response = author_client.post(
        url,
        data=comment_bad_words_form
    )
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == excepted_comment_count


@pytest.mark.django_db
def test_author_can_delete_comment(author_client, comment):
    delete_url = reverse('news:delete', args=(comment.id,))
    response = author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.FOUND
    assert not Comment.objects.filter(id=comment.id).exists()


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(not_author_client, comment):
    delete_url = reverse('news:delete', args=(comment.id,))
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.filter(id=comment.id).exists()