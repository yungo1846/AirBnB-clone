from django.db import models
from . import managers

# Create your models here.


class TimeStampedModel(models.Model):
    """ Time Stampled Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()
    # auto_now_add = 모델이 생성될 때 날짜,시간 자동저장, auto_now는 모델이 업데이트 될 때마다 날짜,시간 자동저장

    class Meta:  # TimeStampedModel이 DB에 들어가는 것을 방지. 기타사항을 적기 위함
        abstract = (
            True  # abstract model은 모델이긴 하지만 데이터베이스에 들어가지 않는 모델이다. 대부분 확장을 하기 위해 사용된다.
        )
