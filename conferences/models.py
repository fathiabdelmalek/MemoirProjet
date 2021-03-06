from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(verbose_name="email", max_length=254)

    def __str__(self):
        return self.last_name + " " + self.first_name


class Conference(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(verbose_name='description')
    place = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    submission_deadline = models.DateField()
    confirmation_deadline = models.DateField()
    payment_deadline = models.DateField()
    pre_price = models.CharField(max_length=20, null=True, blank=True)
    post_price = models.CharField(max_length=20, null=True, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.title

    def can_submit(self):
        return timezone.now().date() <= self.submission_deadline

    def can_accept(self):
        return self.submission_deadline < timezone.now().date() <= self.confirmation_deadline

    def can_confirm(self):
        return self.confirmation_deadline < timezone.now().date() <= self.payment_deadline


class Submission(models.Model):
    STATUS = (
        (0, 'waiting'),
        (1, 'accepted'),
        (2, 'refused'),
        (3, 'confirmed'),
    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(verbose_name="email", max_length=254)
    article_name = models.CharField(max_length=100)
    abstract = models.TextField(verbose_name='abstract')
    article = models.FileField(upload_to='files', null=True, blank=True)
    authors = models.ManyToManyField(Author, related_name='article_authors')
    status = models.IntegerField(choices=STATUS, default=0)
    demand_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + " submission in " + str(self.conference)

    def auto_refused(self):
        if timezone.now().date() > self.conference.submission_deadline:
            self.status = 2

    def is_waiting(self):
        return self.status == 0

    def is_accepted(self):
        return self.status == 1

    def is_refused(self):
        return self.status == 2

    def is_confirmed(self):
        return self.status == 3
