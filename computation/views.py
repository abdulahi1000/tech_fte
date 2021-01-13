
import csv, io, json
from io import StringIO
from django.shortcuts import render,redirect,reverse, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import Group,User
from django.db.models import Count,Sum
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger




from .models import *
from .forms import *
from .filters import *
from .decorators import *


# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    
    staffMembers = Staff.objects.all()
    staffMembersCount = Staff.objects.all().count()
    if request.user.groups.all()[0].name == 'DEEN':
        programme = request.user.staff.programme
        department = Department.objects.filter(programme=programme)
        faculty = Faculty.objects.filter(department__id__in=department)
        staffMembers = Staff.objects.filter(faculty__in=faculty)
    print(request.user.groups.all()[0].name)
    fte = FTE.objects.all()
    fteCount = FTE.objects.all().count()
    if request.user.groups.all()[0].name == 'HOD' and request.user.staff.programme:
        d = Department.objects.filter(programme=request.user.staff.programme)
        fte = FTE.objects.filter(department__id__in=d)
    else:
        pass
    if request.user.groups.all()[0].name == 'DEEN':
        f = request.user.staff.faculty
        fte = FTE.objects.filter(faculty=f)
        
    programme = Programme.objects.all()
    programmeCount = programme.count()
    if request.user.groups.all()[0].name == 'HOD' and request.user.staff.programme:
        d = Department.objects.get(programme=request.user.staff.programme)
        # dd = Department.objects.get(name=d.name)
        # dd.programme.all()
        programme = Programme.objects.filter(department=d)
        programmeCount = programme.count()
    else:
        pass
    
    if request.user.groups.all()[0].name == 'DEEN' and request.user.staff.faculty:
        f = request.user.staff.faculty
        dept = f.department.all()
        for p in dept:
            print(p.programme.all())
        deptCount = dept.count()
    else:
        pass
    dept = Department.objects.all()
    deptCount = dept.count()
    
    if request.user.groups.all()[0].name == 'HOD' and request.user.staff.programme:
        dept = Department.objects.filter(programme=request.user.staff.programme)
        deptCount = dept.count()
        # print(d.programe.name)
        # dept = Department.objects.filter()
    else:
        pass
    if request.user.groups.all()[0].name == 'DEEN' and request.user.staff.faculty:
        dept = request.user.staff.faculty.department.all()
        deptCount = dept.count()
    else:
        pass

            
    
    
    
    
    context ={
        'staffMembersCount':staffMembersCount,
        'fteCount':fteCount,
        'programmeCount':programmeCount,
        'deptCount':deptCount,
    }
    
    return render(request, 'computation/dashboard.html', context)

def ajax(request):
    data =[]
    deptFteCount = FTE.objects.all()
    prog = Programme.objects.all()

    print(deptFteCount)
    levels = [1,2,3,4,5]
    for l in prog:
        d = FTE.objects.filter(programme=l).count()
        
        if d == 0:
            pass
        else:
            data.append({l.name:d})
            
    print(data)
    return JsonResponse(data, safe=False)
def zing(request):
    return render(request, 'computation/zingchart.html')
@login_required(login_url='login')
@unauthenticated_user
def registerpage(request):
    
    form = Createuserform()
    if request.method == 'POST':
        form = Createuserform(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
    
    context={'form':form}
    return render(request, 'computation/register.html', context)

@unauthenticated_user
def loginpage(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    context={}
    return render(request, 'computation/login.html', context)
@login_required(login_url='login')
def logoutpage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
#@restrict_access_to_groups(['HOD'])
def upload(request):

    staffDept = ''
    try:
        departments = Department.objects.all()
        programme = Programme.objects.all()
        user = request.user.staff.name
        staff = Staff.objects.get(name=user) 
        staffProg = staff.programme
        staffDept = Department.objects.get(programme=staffProg)
        print(staffDept)
    except:
        pass


    prompt ={
        'order': 'upload a file if theres one!! ',
        'departments':departments,
        'programme':programme,
        'staffProg':staffProg,
        'staffDept':staffDept,
    }
    if request.method == 'GET':
        return render(request, 'computation/upload.html', prompt )

    if request.method == 'POST' and 'progFile' in request.FILES:
        doc = request.FILES.get('progFile')
        
        p = request.POST['programme']
        s = request.POST['session']
        if doc:

            if not doc.name.endswith('.csv'):
                messages.error(request, 'the file you upload is not a CSV file. ')
                return redirect(upload)
            doc1 = io.TextIOWrapper(doc.file)
            studentData = csv.DictReader(doc1)
            list_of_dict = list(studentData)
            #print(list_of_dict)
            # for l in list_of_dict:
            #     print(l)
            objs =[
                Student(
                    reg_no=row['Reg_no'],
                    course_code=row['Course_code'],
                    course_unit=row['Course_unit'],
                    owner=row['Owner_programme'],
                    level= row['Level'],
                    programme_for_courses=row['Student_programme'],
                    programme=row['Programme'],
                    programme_student= row['Is_programme_student'],
                    session=s,
                    semester=('second' if int(row['Course_code'][4:])%2 ==0 else ('first'))
                )
                for row in list_of_dict
            ]
            msg = Student.objects.bulk_create(objs)

            messages.success(request, 'File uploaded Successfully')
            return redirect(upload)

    elif request.method == 'POST' and 'deptFile' in request.FILES:
        doc1 = request.FILES.get('deptFile')
        d= request.POST['department'] 
        s = request.POST['session']       
        if doc1:
            print(Department.objects.filter(name=d))
            dept = Department.objects.get(name=d)
            prog = dept.programme.all()
            print(prog)
            listofProg = []
            for p in prog: 
                listofProg.append(p.name)
            print(listofProg)

            if not doc1.name.endswith('.csv'):
                messages.error(request, 'the file you upload is not a CSV file. ')
                return redirect(upload)
            doc1 = io.TextIOWrapper(doc1.file)
            studData = csv.DictReader(doc1)
            list_of_dic = list(studData)
            for row in list_of_dic:
                if any(x ==row['Programme'] for x in listofProg):

                    objs =[
                        Student(
                            reg_no=row['Reg_no'],
                            course_code=row['Course_code'],
                            course_unit=row['Course_unit'],
                            owner=row['Owner_programme'],
                            level= row['Level'],
                            programme_for_courses=row['Student_programme'],
                            programme= row['Programme'],
                            programme_student= row['Is_programme_student'],
                            session=s,
                            semester=('second' if int(row['Course_code'][4:])%2 ==0 else ('first'))
                        )
                        for row in list_of_dic
                    ]
                    #msg = Student.objects.bulk_create(objs)

                    messages.success(request, 'File uploaded Successfully')
                    return redirect(upload)
                else:
                    messages.warning(request, 'File uploaded does not contain programme in the department you picked')
                    return redirect(upload)


            # data_set = doc1.read().decode('UTF-8')
            #     # setup a stream which is when we loop through each line we are able to handle a data in a stream
            # io_string = io.StringIO(data_set)
            # next(io_string)
            # for column in csv.reader(io_string, delimiter=',', quotechar="|"):

            #     if column:
            #         if any(x==column[5] for x in listofProg):
            #             print(column)
            #             print(column[5])
            #             _, created = Student.objects.update_or_create(
            #                 reg_no=column[0],
            #                 course_code= column[1],
            #                 course_unit= column[2],
            #                 programme=column[3],
            #                 level= column[4],
            #                 owner=column[5],
            #                 session=s
                            
            #             )
            #     else:
            #         messages.warning(request, 'File uploaded does not contain programme in the department you picked')
            #         return redirect(upload)         
            
            messages.success(request, 'File uploaded Successfully')
            return redirect(upload)
          
            
    context={  
        
    }
    return render(request, 'computation/upload.html',context)

@login_required(login_url='login')
#@restrict_access_to_groups(['HOD'])
def calculation(request):
    staffDept = ''
    try:
        programme = Programme.objects.all()
        user = request.user.staff.name
        staff = Staff.objects.get(name=user)
        staffDept = staff.programme.name
        print(staffDept)
    except:
        pass
    sesson =Student.objects.values('session').distinct()
    print(sesson)
    if request.method == 'POST':
        level = request.POST['levels']
        prog = request.POST['prog']
        session= request.POST['session']
        session= str(session).replace('/','-')
        return redirect(reverse('history', args=[level,prog,session]))
    context={
        'programme':programme,
        'staffDept':staffDept,
        'sesson':sesson,
    }
    return render(request, 'computation/calculation.html', context)

@login_required(login_url='login')
def history(request,level,prog,session):
    session = str(session).replace('-','/')
    print(session)
    level = int(level)
    fte =[]
    courseData=[]
    creditData =[]

    p = Programme.objects.get(name=prog)
    d = Department.objects.get(programme__id=p.id)
    f = Faculty.objects.get(department__id=d.id)

    product =[]
    #SELECT DISTINCT course_code, COUNT(reg_no) FROM `computation_student` GROUP BY course_code
    totalOfStudRegForCourse = Student.objects.values('course_code','course_unit','level').filter(level=level, owner=p.name, session=session).annotate(studentNo =Count('course_code'))
    # firstTotalOfcourseUnitStudReg = Student.objects.values('reg_no').filter(Q(level=level) & Q(session=session) & Q(semester='first') & (Q(programme=p.name)|Q(owner=p.name))).annotate(totalStudUnit = Sum('course_unit'))
    firstTotalOfcourseUnitStudReg = Student.objects.values('reg_no').filter((Q(level=level)|Q(level=level+1)|Q(level=level-1)|Q(level=level+2)|Q(level=level-2)) & Q(session=session) & Q(semester='first') & (Q(programme=p.name)|Q(owner=p.name))).annotate(totalStudUnit = Sum('course_unit'))
    # secondTotalOfcourseUnitStudReg = Student.objects.values('reg_no').filter(Q(level=level) & Q(session=session) & Q(semester='second') & (Q(programme=p.name)|Q(owner=p.name))).annotate(totalStudUnit = Sum('course_unit'))
    secondTotalOfcourseUnitStudReg = Student.objects.values('reg_no').filter((Q(level=level)|Q(level=level+1)|Q(level=level-1)|Q(level=level+2)|Q(level=level-2)) & Q(session=session) & Q(semester='second') & (Q(programme=p.name)|Q(owner=p.name))).annotate(totalStudUnit = Sum('course_unit'))
    StudCourse = Student.objects.values('reg_no').filter(Q(level=level) & Q(session=session) & Q(programme_student=1)& Q(owner=p.name)).distinct() 
    print(StudCourse.count())
    #print(totalOfStudRegForCourse)
    # totalOfStudRegForCourse.exists() and 
    if firstTotalOfcourseUnitStudReg.exists():
        for e in totalOfStudRegForCourse:
            product.append(e['course_unit']*e['studentNo'])
            data ={
                'course_code':e['course_code'],
                'course_unit': e['course_unit'],
                'NoOfStud':e['studentNo'],
                'level':e['level'],
                'product':e['course_unit']*e['studentNo']
            }
            courseData.append(data)
        #print(courseData)
        courseStudProduct = sum(product)
        #print(courseStudProduct)
        
        from collections import Counter

        no = []
        departmentalStud = []
        product1 = []
        noOfStud = []
        firstSemeter = []
        secondSemeter = []
        for course in StudCourse:
            departmentalStud.append(course['reg_no'])
            print(course)
        print(departmentalStud)
        for k in secondTotalOfcourseUnitStudReg:
            # print('second ', k)
            # no.append(k['totalStudUnit'])
            if any(x ==k['reg_no'] for x in departmentalStud ):
                print('second ', k)
                no.append(k['totalStudUnit'])
        for c in firstTotalOfcourseUnitStudReg:
            # print('first' ,c)
            # no.append(c['totalStudUnit'])
            if any(x ==c['reg_no'] for x in departmentalStud ):
                print('first ', c)
                no.append(c['totalStudUnit'])

        print('number', no)
        ade = Counter(no)
        for k,v in ade.items():
            product1.append(k*v)
            noOfStud.append(v)
            data1 ={
                'NoofUnits':k,
                'NoofStud':v,
                'product':k*v
            }
            creditData.append(data1)
        totalProduct = sum(product1)
        # totalNoStud = sum(noOfStud)
        totalNoStud = StudCourse.count()
        print(totalNoStud)
        print(totalProduct)
        if totalNoStud == 0:
            AvgNO = 0
        else:
            AvgNO = totalProduct/totalNoStud
            print(AvgNO)
            fte = courseStudProduct/AvgNO
            fte = round(fte, 2)
         #to update data if there exist 
            #Fte = FTE.objects.filter(fte=fte,CiNi=courseStudProduct, l=AvgNO, level=level, programme=p, department=d, faculty=f,session=session)
            Fte = FTE.objects.filter(department=d,CiNi=courseStudProduct,l=AvgNO, level=level, programme=p, faculty=f,session=session)
            if Fte.exists():
                Fte = Fte[0]
                Fte.fte = fte
                Fte.CiNi = courseStudProduct
                Fte.l = AvgNO
                Fte.save()
            else:
                Fte = FTE(fte=fte, CiNi=courseStudProduct, l=AvgNO, level=level, programme=p, department=d, faculty=f,session=session)
                Fte.save()
            
    else:
        messages.info(request,'No required Data Available')
        return redirect(calculation)


    context ={
        'creditData':creditData,
        'courseData':courseData,
        'fte':fte,
        'courseStudProduct':courseStudProduct,
        'totalProduct':totalProduct,
        'totalNoStud':totalNoStud,
        'prog':p,
        'dept':d,
        'faculty': f,
        'session': session,
        'level':level
        
     }
    return render(request, 'computation/cumputeHistory.html', context)
@login_required(login_url='login')
def staffPage(request): 
    staffMembers = Staff.objects.all()
    staffMembersCount = Staff.objects.all().count()
    if request.user.groups.all()[0].name == 'DEEN':
        programme = request.user.staff.programme
        department = Department.objects.filter(programme=programme)
        faculty = Faculty.objects.filter(department__id__in=department)
        staffMembers = Staff.objects.filter(faculty__in=faculty)

        
       
    context={
        
        'staffMembers':staffMembers,
        'staffMembersCount':staffMembersCount,
    }
    return render(request, 'computation/staff.html',context)
@login_required(login_url='login')
def createStaff(request):
    form = usersForm()
    if request.method == 'POST':
        role = request.POST['role']
        form = usersForm(request.POST)
        if form.is_valid():
            user = form.save()
            groups = Group.objects.all()
            for i in groups:
                if i.name == role:
                    user.groups.add(i.id)

        messages.success(request, 'Staff created Successfully!!')
        return redirect('staff')
           
    context={'form':form}
    return render(request, 'computation/users.html', context)

@login_required(login_url='login')
def updateStaff(request, pk):
    staff = Staff.objects.get(id=pk)
    form = staffForm(instance=staff)
    if request.method == 'POST':
        form = staffForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff updated Successfully!!')
            return redirect('staff')
            
        
    context ={
        'form':form,
    }
    return render(request, 'computation/staff_form.html',context)

@login_required(login_url='login')
def deleteStaff(request, pk):
    staff = Staff.objects.get(id=pk)
    if request.method == 'POST':
        staff.delete()
        messages.success(request, 'Staff deleted Successfully!!')
        return redirect('staff')
        
        
    context ={
        'staff':staff,
    }
    return render(request, 'computation/delete.html',context)

@login_required(login_url='login')
def programme(request):
    programme = Programme.objects.all()
    programmeCount = programme.count()
    
     
    if request.user.groups.all()[0].name == 'HOD':
        d = Department.objects.get(programme=request.user.staff.programme)
        # dd = Department.objects.get(name=d.name)
        # dd.programme.all()
        programme = Programme.objects.filter(department=d)
        programmeCount = programme.count()
    
    if request.user.groups.all()[0].name == 'DEEN':
        f = request.user.staff.faculty
        dept = f.department.all()
        print('department ',dept )
        deptCount = dept.count()
        
     
    context={
        'programmeCount':programmeCount,
        'programme':programme,

    }
    return render(request, 'computation/programmePage.html', context)

@login_required(login_url='login')
def createProgramme(request):
    form = progForm()
    if request.method == 'POST':
        form = progForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, 'Programme created Successfully!!')
            return redirect('programme')
    
    context={
        'form':form,

    }
    return render(request, 'computation/programme_form.html', context)

@login_required(login_url='login')
def updateProgramme(request, pk):
    programme = Programme.objects.get(id=pk)
    form = progForm(instance=programme)
    if request.method == 'POST':
        form = progForm(request.POST,instance=programme)
        if form.is_valid:
            form.save()
            messages.success(request, 'Programme updated Successfully!!')
            return redirect('programme')
    context={
        'form':form,

    }
    return render(request, 'computation/programme_form.html', context)

@login_required(login_url='login')
def deleteProgramme(request, pk):
    programme = Programme.objects.get(id=pk)
    if request.method == 'POST':
        programme.delete()
        messages.success(request, 'programme deleted Successfully!!')
        return redirect('programme')
        
        
    context ={
        'programme':programme,
    }
    return render(request, 'computation/delete.html',context)
@login_required(login_url='login')
def ftepage(request):
    fte = FTE.objects.all()
    fteCount = FTE.objects.all().count()
    if request.user.groups.all()[0].name == 'HOD':
        d = Department.objects.filter(programme=request.user.staff.programme)
        fte = FTE.objects.filter(department__id__in=d)
    if request.user.groups.all()[0].name == 'DEEN':
        f = request.user.staff.faculty
        fte = FTE.objects.filter(faculty=f)

    myfilters = fteFilters(request.GET, queryset=fte)
    fte = myfilters.qs
    context={
        'fte':fte,
        'myfilters':myfilters
    }
    return render(request, 'computation/ftepage.html', context)

@login_required(login_url='login')
def deptPage(request):
    dept = Department.objects.all()
    deptCount = dept.count()
    
    if request.user.groups.all()[0].name == 'HOD':
        d = Department.objects.filter(programme=request.user.staff.programme)
        print(d.programe.name)
        dept = Department.objects.filter()
    if request.user.groups.all()[0].name == 'DEEN':
        f = request.user.staff.faculty
        dept = f.department.all()
        deptCount = dept.count()

    context={
        'dept':dept,
        'deptCount':deptCount,
    }
    return render(request, 'computation/department.html', context)

@login_required(login_url='login')
def createDept(request):
    form = deptForm()
    if request.method == 'POST':
        form = deptForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created Successfully!!')
            return redirect('deptPage')
           
    context={'form':form}
    return render(request, 'computation/dept_form.html', context)

@login_required(login_url='login')
def updateDept(request, pk):
    dept = Department.objects.get(id=pk)
    form = deptForm(instance=dept)
    if request.method == 'POST':
        form = deptForm(request.POST, request.FILES, instance=dept)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated Successfully!!')
            return redirect('deptPage')
            
        
    context ={
        'form':form,
    }
    return render(request, 'computation/dept_form.html',context)

@login_required(login_url='login')
def deleteDept(request, pk):
    dept = Department.objects.get(id=pk)
    if request.method == 'POST':
        dept.delete()
        messages.success(request, 'Department deleted Successfully!!')
        return redirect('deptPage')
        
        
    context ={
        'dept':dept,
    }
    return render(request, 'computation/delete.html',context)

@login_required(login_url='login')
def FacultyPage(request):
    faculty = Faculty.objects.all()
    facultyCount = faculty.count()
    

    context={
        'faculty':faculty,
        'facultyCount':facultyCount,
    }
    return render(request, 'computation/faculty.html', context)

@login_required(login_url='login')
def createFaculty(request):
    form = FacultyForm()
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Faculty created Successfully!!')
            return redirect('faculty')
           
    context={'form':form}
    return render(request, 'computation/faculty_form.html', context)

@login_required(login_url='login')
def updateFaculty(request, pk):
    faculty = Faculty.objects.get(id=pk)
    form = FacultyForm(instance=faculty)
    if request.method == 'POST':
        form = FacultyForm(request.POST, request.FILES, instance=dept)
        if form.is_valid():
            form.save()
            messages.success(request, 'Faculty updated Successfully!!')
            return redirect('faculty')
            
        
    context ={
        'form':form,
    }
    return render(request, 'computation/faculty_form.html',context)

@login_required(login_url='login')
def deleteFaculty(request, pk):
    faculty = Faculty.objects.get(id=pk)
    if request.method == 'POST':
        faculty.delete()
        messages.success(request, 'Faculty deleted Successfully!!')
        return redirect('faculty')
        
        
    context ={
        'faculty':faculty,
    }
    return render(request, 'computation/delete.html',context)

@login_required(login_url='login')
def profilePage(request):
    instance = request.user.staff
    form = staffForm(instance=instance)
    if request.method == 'POST':
        form = staffForm(request.POST, request.FILES,instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff updated Successfully!!')
            return redirect('dashboard')
            
        
    context ={
        'form':form,
    }
    return render(request, 'computation/profile.html',context)
@restrict_access_to_groups(['ADMIN'])
@login_required(login_url='login')
def rawDatePage(request):
    students_list = Student.objects.all()
    page = request.GET.get('Page', 1)
    paginator =Paginator(students_list, 50)
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    context ={
        'students':students,

    }
    return render(request, 'computation/raw_data.html', context)


def upload_ajax(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        # import os
        # f = open(os.path.join(BASE_DIR, 'static', 'pic', file_obj.name), 'wb')
        print(file_obj,type(file_obj))
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        print('11111')
        return HttpResponse('OK')
    return render(request, 'computation/file.html')



from django.conf import settings
def test(request):
    user = User.objects.get(username='opeyemi', email='abdulahiopeyemiq@gmail.com')
    userEmail = user.email
    userN =len(user.username)
    a,b = userEmail.split('@')
    userPass = a+str(userN)
    print(userPass)
    base =request.build_absolute_uri()
    print(base)
    return render(request, 'computation/password_email.html',{'name':'qudus','password':'Some@gmail.com','url':base})



    
        
    
