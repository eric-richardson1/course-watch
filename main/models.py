from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Course(models.Model):
    crn = models.IntegerField(unique=True)
    subject = models.CharField(max_length=200, null=True)
    course_number = models.FloatField(null=True)
    section = models.IntegerField(null=True)
    title = models.CharField(max_length=200, null=True)
    period = models.CharField(max_length=50, null=True)
    instructor = models.CharField(max_length=200, null=True)
    world_culture = models.CharField(max_length=50, null=True)
    distributive = models.CharField(max_length=50, null=True)
    enrollment_limit = models.IntegerField(default=None, null=True)
    num_enrolled = models.IntegerField(default=0)
    requires_ip = models.BooleanField(default=False)
    is_nr_eligible = models.BooleanField(default=False)

    def can_be_watched(self):
        if self.enrollment_limit is not None and self.num_enrolled is not None:
            return self.enrollment_limit >= self.num_enrolled and not self.requires_ip

        return False

    def truncate_course_number(self):
        if self.course_number == round(self.course_number):
            return round(self.course_number)
        else:
            return self.course_number

    def __str__(self):
        return "{} {}: {}, Enrolled: {}, Limit: {}".format(self.subject, self.truncate_course_number(),
                                                           self.title, self.num_enrolled, self.enrollment_limit)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class UserWatchedCourse(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"User: {self.user}, Course: {self.course}"

