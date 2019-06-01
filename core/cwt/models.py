import uuid

from django.db import models
from django.urls import reverse


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{}.{}".format(uuid.uuid4(), ext.lower())

    return 'media/{sub}/{filename}'.format(
        sub=filename[:2],
        filename=filename
        )


class Test(models.Model):
    title = models.CharField(max_length=35, unique=True)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('cwt:test-variants', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Variant(models.Model):
    tests = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='variants')
    title = models.CharField(max_length=15)
    description = models.CharField(max_length=255, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('cwt:test-questions', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Question(models.Model):
    variants = models.ForeignKey('Variant', on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255, unique=True)
    points = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    @property
    def correct_answer(self):
        return self.answers.get(is_correct=True)


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='user_answers')
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='+')


class UserResult(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='user_results')
    test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='user_test', null=True)
    scores = models.IntegerField()
    variant_scores = models.IntegerField(default=0)
    add_time = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('cwt:test-results', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['add_time']