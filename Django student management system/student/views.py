from django.shortcuts import render
from .models import Student,Marks
# Create your views here.


def add_student(request):
    if request.method == "POST":
        roll = request.POST['roll']
        name = request.POST['name']
        age = request.POST['age']
        course = request.POST['course']
        Student.objects.create(
            roll = roll,
            name = name,
            age = age,
            course = course,
        )
    return render(request,'add_student.html')


def add_marks(request):
    if request.method == "POST":
        roll = request.POST['roll']
        student = Student.objects.get(roll = roll)
        telugu = request.POST['telugu']
        english = request.POST['english']
        maths = request.POST['maths']
        science = request.POST['science']

        Marks.objects.create(
            student = student,
            telugu = telugu,
            english = english,
            maths = maths,
            science = science,
        )
    return render (request,'add_marks.html')


def view_student(request):
    student = None
    marks = None
    if request.method == "POST":
        roll = request.POST['roll']
        try:
            student = Student.objects.get(roll = roll)
            marks = Marks.objects.get(student = student)
        except:
            student = None
            marks = None
    return render(request,'view_student.html',{'student':student,'marks':marks})

def edit_details(request):