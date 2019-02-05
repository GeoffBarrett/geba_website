from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
import pytz
from .managers import VotableManager

from math import log, sqrt
from datetime import datetime

UP = 0
DOWN = 1
# eastern = tz('US/Eastern')
utc = pytz.utc


def epoch_seconds(date):
    """This method acquires the epoch in seconds to use in scoring"""
    epoch = datetime(1970, 1, 1)

    td = date - utc.localize(epoch)
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)


class VoteManager(models.Manager):

    def filter(self, *args, **kwargs):
        if 'content_object' in kwargs:
            content_object = kwargs.pop('content_object')
            content_type = ContentType.objects.get_for_model(content_object)
            kwargs.update({
                'content_type': content_type,
                'object_id': content_object.pk
            })

        return super(VoteManager, self).filter(*args, **kwargs)


class Vote(models.Model):

    # dictionary of the voting choices
    ACTION_FIELD = {
        UP: 'num_vote_up',
        DOWN: 'num_vote_down'
    }

    user_id = models.BigIntegerField()  # keep track of who voted
    # get the content type of the model that the vote belongs to
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()  # get the id of the object voted on
    content_object = GenericForeignKey()  # the object that was voted on
    action = models.PositiveSmallIntegerField(default=UP)  # field for the vote choices
    create_at = models.DateTimeField(auto_now_add=True)  # time the vote was created

    objects = VoteManager()  # defines the manager

    class Meta:
        unique_together = ('user_id', 'content_type', 'object_id', 'action')
        index_together = ('content_type', 'object_id')

    @classmethod
    def votes_for(cls, model, instance=None, action=UP):
        ct = ContentType.objects.get_for_model(model)
        kwargs = {
            "content_type": ct,
            "action": action
        }
        if instance is not None:
            kwargs["object_id"] = instance.pk

        return cls.objects.filter(**kwargs)


class VoteModel(models.Model):

    score_method = 'hot_score'  # defaults as 'hot_score'

    vote_score = models.FloatField(default=0, db_index=True)  # score value
    num_vote_up = models.PositiveIntegerField(default=0, db_index=True)  # number of up votes
    num_vote_down = models.PositiveIntegerField(default=0, db_index=True)  # number of down votes
    votes = VotableManager()

    class Meta:
        # makes this model an abstract base class, and thus will not create a separate database
        abstract = True

    def save(self, *args, **kwargs):
        # saves the vote
        self.vote_score = self.calculate_vote_score
        super(VoteModel, self).save(*args, **kwargs)

    @property
    def net_vote(self):
        try:
            return self._net_vote
        except AttributeError:
            return False

    @net_vote.setter
    def net_vote(self):
        self._net_vote = self.num_vote_up - self.num_vote_down

    @property
    def calculate_vote_score(self):
        """Calculate the score of the vote based on different scoring types"""
        if self.score_method == 'hot_score':
            '''This voting method is used by reddit, it takes in account the time
                        since the post, heavily weighted towards newer posts.'''
            return self.calculate_hot_score
        elif self.score_method == 'confidence':
            """This voting method is time independent, and is generally used for commenting,
            just because you commented first/last does not mean it should be ranked higher or lower.
            It uses Wilson Score Intervals to predict the score given the vote population."""
            return self.calculate_confidence

    @property
    def is_voted_up(self):
        """Determines if the object is voted up, it is added to the instance of the object temporarily"""
        try:
            return self._is_voted_up
        except AttributeError:
            return False

    @is_voted_up.setter
    def is_voted_up(self, value):
        self._is_voted_up = value

    @property
    def is_voted_down(self):
        """Determines if the object is voted down, it is added to the instance of the object temporarily"""
        try:
            return self._is_voted_down
        except AttributeError:
            return False

    @is_voted_down.setter
    def is_voted_down(self, value):
        self._is_voted_down = value

    @property
    def unvoted_net_likes(self):
        n = int(self.num_vote_up - self.num_vote_down)
        print('nnnnnnnnnnnnnnn', n)
        if self.is_voted_up:
            return n - 1
        elif self.is_voted_down:
            return n + 1
        else:
            return n

    @property
    def calculate_confidence(self):
        n = self.num_vote_up + self.num_vote_down
        if n == 0:
            confidence = 0
        else:
            z = 1.281551565545
            p = float(self.num_vote_up) / n
            left = p + 1 / (2 * n) * z * z
            right = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
            under = 1 + 1 / n * z * z

            confidence = (left - right) / under

        return confidence

    @property
    def calculate_hot_score(self):
        """
        This score is similar to how Reddit scores their posts, we will not have downvotes since these
        posts aren't geba_auth submitted
        """

        s = self.num_vote_up
        date = datetime.now(timezone.utc)
        # date = datetime.utcnow()
        # date = datetime(tz=pytz.utc)

        order = log(max(abs(s), 1), 10)
        sign = 1 if s > 0 else -1 if s < 0 else 0
        seconds = epoch_seconds(date) - 1134028003

        return round(sign * order + seconds / 45000, 7)
