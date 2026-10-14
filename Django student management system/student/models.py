from django.db import models

# Create your models here.
class Student(models.Model):
    roll = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    age = models.CharField()
    course = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.roll} - {self.name}"



class Marks(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    telugu = models.IntegerField()
    english = models.IntegerField()
    maths = models.IntegerField()
    science = models.IntegerField()
    def __str__(self):
        return self.student.name