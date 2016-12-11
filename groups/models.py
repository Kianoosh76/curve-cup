from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=50)
    group = models.ForeignKey(to='Group', related_name='players')

    def __str__(self):
        return self.name


class Score(models.Model):
    score = models.IntegerField()
    player = models.ForeignKey(to='Player', related_name='scores')

    def __str__(self):
        return str(self.player) + " " + str(self.score)