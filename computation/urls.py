from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard' ),
    path('upload/', views.upload, name='upload' ),
    path('calculation/', views.calculation, name='calculation' ),
    path('history/<str:level>/<str:prog>/<str:session>/', views.history, name='history' ),

    path('file/', views.upload_ajax, name='upload_ajax'),

    path('login/', views.loginpage, name='login' ),
    path('logout/', views.logoutpage, name='logout' ),
    path('register/', views.registerpage, name='register' ),
    path('profile/', views.profilePage, name='profilePage'),
    
    path('test/', views.test, name='test' ),
    path('staff/', views.staffPage, name='staff' ),
    path('fte/', views.ftepage, name='ftepage' ),
    
    path('data/', views.ajax, name='data'),
    path('zing/', views.zing, name='zing'),

    path('update_staff/<str:pk>/', views.updateStaff, name= 'updateStaff'),
    path('create_staff/', views.createStaff, name= 'createStaff'),
    path('delete_staff/<str:pk>/', views.deleteStaff, name= 'deleteStaff'),

    path('department/', views.deptPage, name='deptPage'),
    path('create_Dept/', views.createDept, name='createDept'),
    path('update_Dept/<str:pk>/', views.updateDept, name= 'updateDept'),
    path('delete_Dept/<str:pk>/', views.deleteDept, name= 'deleteDept'),

    path('faculty/', views.FacultyPage, name='faculty'),
    path('create_faculty/', views.createFaculty, name='createFaculty'),
    path('update_faculty/<str:pk>/', views.updateFaculty, name= 'updateFaculty'),
    path('delete_faculty/<str:pk>/', views.deleteFaculty, name= 'deleteFaculty'),

    path('Programme/', views.programme, name='programme'),
    path('create_programme/', views.createProgramme, name='createProgramme'),
    path('update_programme/<str:pk>/', views.updateProgramme, name='updateProgramme' ),
    path('delete_programme/<str:pk>/', views.deleteProgramme, name='deleteProgramme' ),
    path('student_raw_data/', views.rawDatePage, name='studRaw'),

    path('change_password/',
    auth_views.PasswordChangeView.as_view(template_name='computation/password_change.html'),
     name='password_change'),
    path('change_password/done/',
    auth_views. PasswordChangeDoneView.as_view(template_name='computation/password_change_done.html'),
     name='password_change_done'),



    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name='computation/password_rest.html'),
      name='reset_password'),
    path('reset_password_sent/',
     auth_views.PasswordResetDoneView.as_view(template_name='computation/password_rest_sent.html'),
      name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name='computation/password_rest_form.html'),
      name='password_reset_confirm'),
    path('reset_password_complete/',
     auth_views.PasswordResetCompleteView.as_view(template_name='computation/password_rest_done.html'),
      name='password_reset_complete')
]