"""
URL configuration for seminar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.shortcuts import render
from app_1 import views

def professor_dashboard(request):
    return render(request, 'professor_control_panel.html')
def student_dashboard(request):
    return render(request, 'student_control_panel.html')
def admin_dashboard(request):
    return render(request, 'admin_control_panel.html')

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('professor/control_panel', views.professor_dashboard, name='professor_dashboard'),
    path('student/control_panel', views.student_dashboard, name='student_dashboard'),
    path('admin/control_panel', admin_dashboard, name='admin_dashboard'),
    path('admin/control_panel/predmeti_list', views.predmeti_list, name='predmeti_list'),
    path('admin/control_panel/predmet_details/<int:predmet_id>', views.predmet_details, name='predmet_details'),
    path('admin/control_panel/predmet_details/<int:predmet_id>/upisani_studenti', views.upisani_studenti, name='upisani_studenti'),
    path('admin/control_panel/predmet_edit/<int:predmet_id>', views.predmet_edit, name='predmet_edit'),
    path('admin/control_panel/predmet_add', views.predmet_add, name='predmet_add'),
    path('admin/control_panel/studenti_list/', views.studenti_list, name='studenti_list'),
    path('admin/control_panel/student_details/<int:student_id>/', views.student_details, name='student_details'),
    path('admin/control_panel/student_edit/<int:student_id>/', views.student_edit, name='student_edit'),
    path('admin/control_panel/student_add/', views.student_add, name='student_add'),
    path('admin/control_panel/profesori_list/', views.professor_list, name='professor_list'),
    path('admin/control_panel/profesors_details/<int:professor_id>/', views.professor_details, name='professor_details'),
    path('admin/control_panel/profesors_add/', views.professor_add, name='professor_add'),
    path('admin/control_panel/profesors_edit/<int:professor_id>/', views.professor_edit, name='professor_edit'),
    path('admin/control_panel/assign_predmet/<int:professor_id>/', views.assign_predmet, name='assign_predmet'),
    path('admin/control_panel/student/<int:student_id>/upisni_list/', views.student_upisni_list, name='student_upisni_list'),
    path('admin/control_panel/student/<int:student_id>/upisni_list/create/', views.create_upisni_list, name='create_upisni_list'),
    path('admin/control_panel/upisni_list/<int:student_id>/edit/<int:semestar_id>/', views.edit_upisni_list, name='edit_upisni_list'),
    path('admin/control_panel/student/<int:student_id>/upisni_list/create/<int:semestar_choice>/', views.create_upisni_list_display, name='create_upisni_list_display'),
    path('admin/control_panel/predmeti_lista_detaljno/', views.predmeti_lista_detaljno, name='predmeti_lista_detaljno'),
    path('admin/control_panel/predmeti_lista_detaljno/detalji/<int:predmet_id>',views.detalji,name='detalji'),
    path('admin/control_panel/last_year_students/', views.check_last_year,name="last_year_student"),

    path('professor/control_panel/<int:predmet_id>/upisani_studenti/', views.upisani_studenti_prof, name='upisani_studenti_prof'),
    path('professor/control_panel/<int:predmet_id>/prosli_studenti/', views.prosli_studenti_prof, name='prosli_studenti_prof'),
    path('professor/control_panel/<int:predmet_id>/pali_studenti/', views.pali_studenti_prof, name='pali_studenti_prof'),
    path('professor/control_panel/update_status/<int:student_id>/<int:predmet_id>/', views.update_status, name='update_status'),

    path('student/control_panel/upisni_list/create',views.create_upisni_list_student,name='create_upisni_list_student'),
    path('student/control_panel/upisni_list/create/<int:semestar_choice>/',views.create_upisni_list_display_student,name='create_upisni_list_display_student'),
    path('student/control_panel/upisni_list/delete/<int:upisni_id>/',views.delete_upisni_list_entry,name='delete_upisni_list_entry'),
    path('student/control_panel/upisni_list/create/', views.create_upisni_list_student, name='create_upisni_list_student'),


]

