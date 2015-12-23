from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ManyToManyField
from django.utils.translation import ugettext as _
import re
from main.models import ApiKey

from datetime import datetime, timedelta
from django.utils import timezone
# Create your models here.


class MultiQuestion(models.Model):

    group_name = models.CharField(max_length=100)

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'id:{},{}'.format(self.id, self.group_name)


class Question(models.Model):
    TYPE_SURVEY = 'SURV'
    TYPE_VOTE = 'VOTE'
    TYPE_CHOICE = (
        (TYPE_SURVEY, 'Survey'),
        (TYPE_VOTE, 'Vote'),
    )

    api_key = models.ForeignKey(ApiKey, related_name='questions')

    type = models.CharField(max_length=60, choices=TYPE_CHOICE, default=TYPE_VOTE)

    ''' is checked group question '''
    multi_question = models.ForeignKey(MultiQuestion, related_name='question_elements', null=True)

    ''' question '''
    question_title = models.CharField(max_length=50)
    question_text = models.CharField(max_length=100)

    ''' question available '''
    is_closed = models.BooleanField(default=False)
    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField()
    is_editable = models.BooleanField(default=True)  # if answer can be changed
    is_private = models.BooleanField(default=False)

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'id:{},{}'.format(self.id, self.question_text)

    @classmethod
    def check_same_title(cls, api_key, new_title):
        if cls.objects.filter(api_key=api_key, question_title=new_title):
            return True
        return False

    def clean(self):
        # clean question_title
        if self.check_same_title(self.api_key, self.question_title):
            raise ValidationError({'question_title': _('This question_title is already exist in same api_key')})

        # clean start_dt
        if self.start_dt:
            if datetime.strptime(self.start_dt, '%Y-%m-%dT%H:%M') < datetime.now():
                raise ValidationError({'start_dt': _('Start date should be later than now')})
        else:
            self.start_dt = timezone.now()
        # clean end_dt
        if self.end_dt:
            if datetime.strptime(self.end_dt, '%Y-%m-%dT%H:%M') <= datetime.strptime(self.start_dt, '%Y-%m-%dT%H:%M'):
                raise ValidationError({'end_dt': _('End date should be later than start date')})
        else:
            self.end_dt = timezone.now() + timezone.timedelta(days=30)

        if re.match(r'^[a-zA-Z0-9]*$', self.question_title):
            raise ValidationError({'question_title': _('question_title has to be consisted of characters ans numbers.')})

    def save(self, **kwargs):
        self.clean()
        return super(Question, self).save(**kwargs)

    # @classmethod
    # def set_group_number(cls, api):
    #     max_group_number = cls.objects.filter(api_key=api).order_by('-group_number').last()
    #     return int(max_group_number) + 1


class Url(models.Model):
    question = models.ForeignKey(Question, related_name='authenticated_urls')
    url_name = models.CharField(max_length=100, null=True, blank=True)
    full_url = models.CharField(max_length=200)

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-({})'.format(self.url_name, self.full_url)


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers')
    answer_text = models.CharField(max_length=50)
    answer_num = models.IntegerField(null=True)

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-({})'.format(self.answer_text, self.answer_num)

    @property
    def get_answer_count(self):
        return self.user_answers.count()


# user vote info 따로 관리
class UserAnswer(models.Model):
    answer = models.ForeignKey(Answer, related_name='user_answers')
    unique_user = models.CharField(max_length=100, unique=True)  # api_key+unique Id
    # survey_text = models.TextField()

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}'.format(self.answer, self.unique_user)


# make a dictionary which includes editable fields
def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
        else:
            data[f.name] = f.value_from_object(instance)
    return data
# todo question type == survey 일 경우 answer table field 변경