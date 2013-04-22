from django.db import models

class ec2(models.Model):
    key = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)

    def __unicode__(self):
        return self.key

class euca(models.Model):
    key = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)

    def __unicode__(self):
        return self.key