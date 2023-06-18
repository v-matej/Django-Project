from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Predmeti(models.Model):
    IZBORNI = (
        ('DA', 'da'),
        ('NE', 'ne'),
    )

    name = models.CharField(max_length=50)
    kod = models.CharField(max_length=50)
    program = models.CharField(max_length=50)
    ects = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    izborni = models.CharField(max_length=50, choices=IZBORNI)

    def __str__(self):
        return self.name


class Korisnik(AbstractUser):
    ROLES = (
        ('prof', 'profesor'),
        ('stu', 'student'),
        ('admin', 'administrator'),
    )
    STATUS = (
        ('none', 'None'),
        ('izv', 'izvanredni student'),
        ('red', 'redovni student'),
    )

    role = models.CharField(max_length=50, choices=ROLES)
    status = models.CharField(max_length=50, choices=STATUS)
    UpisniList = models.ManyToManyField(Predmeti, through='UpisniList', related_name='korisnici')


class UpisniList(models.Model):
    STATUS_CHOICES = (
        ('pass', 'Passed'),
        ('fail', 'Failed'),
        ('enr', 'Enrolled'),
    )

    predmet = models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    korisnik = models.ForeignKey(Korisnik, on_delete=models.CASCADE, related_name='upisni_list')
    status = models.CharField(max_length=4, choices=STATUS_CHOICES)
    semester = models.IntegerField()

    def __str__(self):
        return f'{self.predmet} - {self.korisnik}'

    class Meta:
        unique_together = ('predmet', 'korisnik', 'semester')


class PredmetiAssignment(models.Model):
    professor = models.ForeignKey(Korisnik, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmeti, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('professor', 'predmet')



