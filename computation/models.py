from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Programme(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    programme = models.ManyToManyField(Programme, blank=True)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=200, blank=True)
    department = models.ManyToManyField(Department, blank=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    staff_No = models.CharField(max_length=200, null=True)
    programme = models.ForeignKey(
        Programme, on_delete=models.CASCADE, null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(
        default='defult.jpg', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


# class LevelCourses(models.Model):
#     course_code = models.CharField(max_length=200, null=True)
#     credit_Units = models.IntegerField(default=0, null=True, blank=True)
#     no_of_students = models.IntegerField(default=0, null=True, blank=True)
#     course_level = models.IntegerField(default=0, null=True, blank=True)
#     programme = models.ForeignKey(Programme, null=True, blank=True, on_delete= models.CASCADE)
#     date_added = models.DateTimeField(auto_now_add=True, null=True)

#     def __str__(self):
#         return self.course_code

#     @property
#     def get_courseProduct_sum(self):
#         product = self.credit_Units* self.no_of_students
#         return product

# class CreditUnitsRegistered(models.Model):
#     no_of_units_reg = models.IntegerField(default=0, null=True, blank=True)
#     no_of_students = models.IntegerField(default=0, null=True, blank=True)
#     credit_level = models.IntegerField(default=0, null=True, blank=True)
#     programme = models.ForeignKey(Programme, null=True, blank=True, on_delete= models.CASCADE)
#     date_added = models.DateTimeField(auto_now_add=True, null=True)

#     def __str__(self):
#         return str(self.id)
#     @property
#     def get_creditProduct_sum(self):
#         product = self.no_of_units_reg* self.no_of_students
#         return product

class FTE(models.Model):
    fte = models.DecimalField(default=0, max_digits=20,
                              decimal_places=2, null=True, blank=True)
    CiNi = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, null=True, blank=True)
    l = models.IntegerField(default=0, null=True, blank=True)
    programme = models.ForeignKey(
        Programme, null=True, blank=True, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, null=True, blank=True, on_delete=models.CASCADE)
    faculty = models.ForeignKey(
        Faculty, null=True, blank=True, on_delete=models.CASCADE)
    level = models.IntegerField(default=0, null=True, blank=True)
    session = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.programme)


class Student(models.Model):
    reg_no = models.CharField(max_length=200, null=True)
    course_code = models.CharField(max_length=200, null=True)
    course_unit = models.IntegerField(default=0, null=True, blank=True)
    programme = models.CharField(max_length=200, null=True)
    programme_for_courses = models.CharField(max_length=200, null=True)
    programme_student = models.CharField(max_length=200, null=True)
    owner = models.CharField(max_length=200, null=True)
    semester = models.CharField(max_length=200, null=True)
    session = models.CharField(max_length=200, null=True)
    level = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.programme


class Lecturer(models.Model):
    full_name = models.CharField(max_length=200, null=True)
    lecturer_id = models.IntegerField(default=0, null=True)
    programme = models.ForeignKey(
        Programme, null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, null=True, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class TeachingLoad(models.Model):
    lecturer = models.ForeignKey(Lecturer, null=True, on_delete=models.CASCADE)
    session = models.CharField(max_length=100, null=True)
    student_teacher_ratio = models.IntegerField(
        default=0, null=True, blank=True)
    CiNiHi = models.IntegerField(default=0, null=True, blank=True)
    fte_session = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, null=True, blank=True)
    fte_semester = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, null=True, blank=True)
    workload = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, null=True, blank=True)


class Course(models.Model):
    course_name = models.CharField(max_length=10, null=True)
    lecture = models.IntegerField(null=True)
    tutorial = models.IntegerField(null=True)
    practical = models.IntegerField(null=True)
    unit = models.IntegerField(null=True)
    faculty = models.CharField(max_length=100, null=True)
    department = models.CharField(max_length=100, null=True)
    programme = models.CharField(max_length=100, null=True)

    def __str__(self):
        return (self.course_name + ' '+self.programme)


# class Level(models.Model):
#     levelCourses = models.ForeignKey(LevelCourses, blank=True, on_delete= models.CASCADE)
#     creditUnitsRegistered = models.ForeignKey(CreditUnitsRegistered, blank=True, on_delete= models.CASCADE)
