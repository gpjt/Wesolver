from django.db import models

from django.contrib.auth.models import User


class Spreadsheet(models.Model):

    owner = models.ForeignKey(User)

    name = models.CharField(max_length=255)

    contents = models.TextField()

    def __unicode__(self):
        return "[%s] %s" % (self.owner, self.name)
