from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.contrib import messages
from django.http import HttpResponse
from .models import Predmeti, Korisnik, PredmetiAssignment,UpisniList
from .forms import PredmetForm,StudentForm,StudentEditForm,ProfessorForm,ProfessorEditForm,AssignPredmetForm,UpisniListForm,SemesterChoiceForm,UpisniListFormSet,UpisniListFormSetStudent
from django.contrib.auth.decorators import user_passes_test

import pdb;

def admin_required(view_func):
    decorated_view_func = user_passes_test(lambda user: user.role == 'admin', login_url='login')
    return decorated_view_func(view_func)

def profesor_required(view_func):
    decorated_view_func = user_passes_test(lambda user: user.role == 'prof', login_url='login')
    return decorated_view_func(view_func)

def student_required(view_func):
    decorated_view_func = user_passes_test(lambda user: user.role == 'stu', login_url='login')
    return decorated_view_func(view_func)

##########################################

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'prof':
                return redirect('professor_dashboard')
            elif user.role == 'stu':
                return redirect('student_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
        else:
            return render(request, 'login.html', {'error_message': 'Pogrešno korisničko ime ili lozinka.'})
    else:
        return render(request, 'login.html')

#####################################################################
@admin_required
def predmeti_list(request):
    predmeti = Predmeti.objects.all()
    return render(request, 'predmeti_list.html', {'predmeti':predmeti})

@admin_required
def predmet_details(request,predmet_id):
    predmet=get_object_or_404(Predmeti,id=predmet_id)
    return render(request, 'predmet_details.html', {'predmet':predmet})

@admin_required
def predmet_edit(request, predmet_id):
    predmet = get_object_or_404(Predmeti, id=predmet_id)

    if request.method == 'POST':
        predmet.name = request.POST['name']
        predmet.kod = request.POST['kod']
        predmet.program = request.POST['program']
        predmet.ects = int(request.POST['ects'])
        predmet.sem_red = int(request.POST['sem_red'])
        predmet.sem_izv = int(request.POST['sem_izv'])
        predmet.izborni = request.POST['izborni']

        predmet.save()
        return redirect('predmet_details', predmet_id=predmet.id)

    return render(request, 'predmet_edit.html', {'predmet': predmet})

@admin_required
def predmet_add(request):
    if request.method == 'POST':
        form = PredmetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('predmeti_list')
    else:
        form=PredmetForm()
    return render(request,'predmet_add.html',{'form':form})


@admin_required
def predmeti_lista_detaljno(request):
    predmeti=Predmeti.objects.all()
    for predmet in predmeti:
        upisni_list=UpisniList.objects.filter(predmet=predmet,status='pass')
        predmet.ukupno_polozilo=upisni_list.count()
        predmet.redovnih_polozilo=upisni_list.filter(korisnik__status='red').count()
        predmet.izvarednih_polozilo=upisni_list.filter(korisnik__status='izv').count()

    context={
        'predmeti':predmeti
    }
    
    return render(request,'predmeti_lista_detaljno.html',context)

@admin_required
def detalji(request, predmet_id):
    predmet = get_object_or_404(Predmeti, id=predmet_id)
    redovni = UpisniList.objects.filter(predmet=predmet, status='pass', korisnik_id__status='red')
    izvanredni = UpisniList.objects.filter(predmet=predmet, status='pass', korisnik_id__status='izv')
    redovni_students = redovni.values('korisnik_id__first_name', 'korisnik_id__last_name')
    izvanredni_students = izvanredni.values('korisnik_id__first_name', 'korisnik_id__last_name')
    redovni_names = [f"{student['korisnik_id__first_name']} {student['korisnik_id__last_name']}" for student in redovni_students]
    izvanredni_names = [f"{student['korisnik_id__first_name']} {student['korisnik_id__last_name']}" for student in izvanredni_students]
    return render(request, 'detalji.html', {'predmet': predmet, 'redovni': redovni_names, 'izvanredni': izvanredni_names})


########################################################

@admin_required
def studenti_list(request):
    studenti = Korisnik.objects.filter(role="stu")
    return render(request, 'studenti_list.html',{'studenti':studenti})

@admin_required
def student_details(request,student_id):
    student=get_object_or_404(Korisnik,id=student_id)
    return render(request, 'student_details.html',{'student':student})

@admin_required
def student_edit(request,student_id):
    student = get_object_or_404(Korisnik, id=student_id, role='stu')

    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_details', student_id=student_id)
    else:
        form = StudentEditForm(instance=student)

    return render(request, 'student_edit.html', {'form': form, 'student': student})

@admin_required    
def student_add(request):
    if request.method == 'POST':
        form=StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('studenti_list')
    else:
        form=StudentForm()
    return render(request,'student_add.html',{'form':form})

################################################################

@admin_required
def professor_list(request):
    professors = Korisnik.objects.filter(role='prof')
    return render(request, 'profesori_list.html', {'professors': professors})

@admin_required
def professor_details(request, professor_id):
    professor = get_object_or_404(Korisnik, id=professor_id, role='prof')
    return render(request, 'profesor_details.html', {'professor': professor})

@admin_required
def professor_add(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            professor = form.save(commit=False)
            professor.role = 'prof'
            professor.save()
            return redirect('professor_list')
    else:
        form = ProfessorForm()

    return render(request, 'profesor_add.html', {'form': form})

@admin_required
def professor_edit(request, professor_id):
    professor = get_object_or_404(Korisnik, id=professor_id, role='prof')

    if request.method == 'POST':
        form = ProfessorEditForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            return redirect('professor_details', professor_id)
    else:
        form = ProfessorEditForm(instance=professor)

    return render(request, 'profesor_edit.html', {'form': form, 'professor': professor})

@admin_required
def assign_predmet(request, professor_id):
    professor = get_object_or_404(Korisnik, id=professor_id)

    if professor.role != 'professor':
        messages.error(request, 'Invalid professor ID.')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        predmeti_form = AssignPredmetForm(request.POST)
        if predmeti_form.is_valid():
            predmeti = predmeti_form.cleaned_data['predmeti']
            PredmetiAssignment.objects.filter(professor=professor).delete()
            for predmet in predmeti:
                PredmetiAssignment.objects.create(professor=professor, predmet=predmet)
            return redirect('professor_details', professor_id=professor_id)
    else:
        predmeti_form = AssignPredmetForm()

    return render(request, 'assign_predmeti.html', {'predmeti_form': predmeti_form, 'professor': professor})
##############################################################

@admin_required
def student_upisni_list(request, student_id):
    student = get_object_or_404(Korisnik, id=student_id)

    if student.status == 'red':
        max_semesters = 6
    elif student.status == 'izv':
        max_semesters = 8
    else:
        max_semesters = 0

    semesters = student.upisni_list.values('semester').annotate(semester_count=Count('semester')).order_by('semester')[:max_semesters]

    return render(request, 'student_upisni_list.html', {'student': student, 'semesters': semesters})


@admin_required
def create_upisni_list(request, student_id):
    student = get_object_or_404(Korisnik, id=student_id)

    if request.method == 'POST':
        semestar_choice = request.POST.get('semestar_choice')
        return redirect('create_upisni_list_display', student_id=student_id, semestar_choice=semestar_choice)

    context = {
        'student': student,
    }
    return render(request, 'semester_choice.html', context)

@admin_required
def create_upisni_list_display(request, student_id, semestar_choice):
    student = get_object_or_404(Korisnik, id=student_id)

    if student.status == 'red' and int(semestar_choice) > 6:
        messages.error(request, 'Invalid semester choice for redovan student.')
        return redirect('student_upisni_list', student_id=student_id)
    
    if student.status == 'izv' and int(semestar_choice) > 8:
        messages.error(request, 'Invalid semester choice for izvaredan student.')
        return redirect('student_upisni_list', student_id=student_id)

    if student.status == 'red':
        predmeti = Predmeti.objects.filter(sem_red=int(semestar_choice))
    else:
        predmeti = Predmeti.objects.filter(sem_izv=int(semestar_choice))

    if request.method == 'POST':
        upisni_list_entries = []
        existing_entries = UpisniList.objects.filter(korisnik=student, semester=semestar_choice)
        existing_predmeti_ids = [entry.predmet.id for entry in existing_entries]

        for predmet in predmeti:
            status = request.POST.get(f'status_{predmet.id}')
            if status in ['pass', 'enr', 'fail'] and predmet.id not in existing_predmeti_ids:
                upisni_list_entries.append(
                    UpisniList(predmet=predmet, korisnik=student, status=status, semester=semestar_choice)
                )

        UpisniList.objects.bulk_create(upisni_list_entries)

        return redirect('student_upisni_list', student_id=student_id)

    context = {
        'student': student,
        'predmeti': predmeti,
        'semestar_choice': semestar_choice,
    }
    return render(request, 'create_upisni_list.html', context)

@admin_required
def edit_upisni_list(request, student_id, semestar_id):
    student = get_object_or_404(Korisnik, id=student_id)
    upisni_list = UpisniList.objects.filter(korisnik=student, semester=semestar_id)

    if request.method == 'POST':
        formset = UpisniListFormSetStudent(request.POST, queryset=upisni_list, prefix='upisni')
        if formset.is_valid():
            for form in formset:
                upisni = form.save(commit=False)
                upisni.korisnik = student
                upisni.semester = semestar_id
                upisni.save()
            return redirect('student_upisni_list', student_id=student_id)
    else:
        formset = UpisniListFormSet(queryset=upisni_list, prefix='upisni')

    return render(request, 'edit_upisni_list.html', {'formset': formset, 'student': student, 'semestar_id': semestar_id})




########################################################

@admin_required
def upisani_studenti(request,predmet_id):
    students=Korisnik.objects.filter(upisni_list__predmet_id=predmet_id)

    return render(request,'upisani_studenti.html',{'students':students})

#########################################################

@profesor_required
def professor_dashboard(request):
    current_user_id=request.user.id
    professor=get_object_or_404(Korisnik,id=current_user_id)
    return render(request,'professor_control_panel.html',{'professor':professor})

@profesor_required
def upisani_studenti_prof(request,predmet_id):
    students=Korisnik.objects.filter(upisni_list__predmet_id=predmet_id)
    predmet=Predmeti.objects.get(id=predmet_id)

    return render(request,'upisani_studenti_prof.html',{'predmet':predmet,'students':students})

@profesor_required
def prosli_studenti_prof(request,predmet_id):
    students=Korisnik.objects.filter(upisni_list__predmet_id=predmet_id)
    predmet=Predmeti.objects.get(id=predmet_id)

    return render(request,'prosli_studenti_prof.html',{'predmet':predmet,'students':students})

@profesor_required
def pali_studenti_prof(request,predmet_id):
    students=Korisnik.objects.filter(upisni_list__predmet_id=predmet_id)
    predmet=Predmeti.objects.get(id=predmet_id)

    return render(request,'pali_studenti_prof.html',{'predmet':predmet,'students':students})

@profesor_required
def update_status(request, student_id, predmet_id):
    upisni = get_object_or_404(UpisniList, korisnik=student_id, predmet=predmet_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        if status == 'passed':
            upisni.status = 'pass'
        elif status == 'failed':
            upisni.status = 'fail'
        upisni.save()

    return redirect('upisani_studenti_prof', predmet_id=predmet_id)

########################################################################

@student_required
def student_dashboard(request):
    current_user_id=request.user.id
    student=Korisnik.objects.get(id=current_user_id)
    if student.status == 'red':
        max_semesters = 6
    elif student.status == 'izv':
        max_semesters = 8
    else:
        max_semesters = 0
    semesters = student.upisni_list.values('semester').annotate(semester_count=Count('semester')).order_by('semester')[:max_semesters]
    
    return render(request,'student_control_panel.html',{'student':student,'semesters':semesters})

@student_required
def create_upisni_list_student(request):
    student = get_object_or_404(Korisnik, id=request.user.id)

    if request.method == 'POST':
        semestar_choice = request.POST.get('semestar_choice')
        return redirect('create_upisni_list_display_student', semestar_choice=semestar_choice)

    context = {
        'student': student,
    }
    return render(request, 'semester_choice.html', context)

@student_required
def create_upisni_list_display_student(request, semestar_choice):
    student_id = request.user.id
    student = get_object_or_404(Korisnik, id=student_id)

    if student.status == 'red' and int(semestar_choice) > 6:
        messages.error(request, 'Invalid semester choice for redovan student.')
        return redirect('student_dashboard')
    
    if student.status == 'izv' and int(semestar_choice) > 8:
        messages.error(request, 'Invalid semester choice for izvaredan student.')
        return redirect('student_dashboard')

    if student.status == 'red':
        predmeti = Predmeti.objects.filter(sem_red=int(semestar_choice))
    else:
        predmeti = Predmeti.objects.filter(sem_izv=int(semestar_choice))

    if request.method == 'POST':
        #####################
        if student.status == 'red' and int(semestar_choice) >= 5:
            year_1_passed = UpisniList.objects.filter(korisnik=student, semester=1, status='pass').count()
            year_1_passed+=UpisniList.objects.filter(korisnik=student, semester=2, status='pass').count()
            year_1_count=Predmeti.objects.filter(sem_red=1).count()
            year_1_count+=Predmeti.objects.filter(sem_red=2).count()

            if year_1_passed < year_1_count:
                messages.error(request, 'Nisi prosao sve predmete s prve godine.')
                return redirect('student_dashboard')
        
        if student.status == 'izv' and int(semestar_choice) >= 7:
            year_1_passed = UpisniList.objects.filter(korisnik=student, semester=1, status='pass').count()
            year_1_passed+=UpisniList.objects.filter(korisnik=student, semester=2, status='pass').count()
            year_2_passed = UpisniList.objects.filter(korisnik=student, semester=3, status='pass').count()
            year_2_passed+=UpisniList.objects.filter(korisnik=student, semester=4, status='pass').count()
            year_1_count=Predmeti.objects.filter(sem_izv=1).count()
            year_1_count+=Predmeti.objects.filter(sem_izv=2).count()
            year_2_count=Predmeti.objects.filter(sem_izv=3).count()
            year_2_count+=Predmeti.objects.filter(sem_izv=4).count()

            if year_1_passed+year_2_passed < year_1_count+year_2_count:
                messages.error(request, 'Nisi prosao sve predmete s prve ili druge godine.')
                return redirect('student_dashboard')
        ####################
        upisni_list_entries = []
        existing_entries = UpisniList.objects.filter(korisnik=student, semester=semestar_choice)
        existing_predmeti_ids = [entry.predmet.id for entry in existing_entries]

        for predmet in predmeti:
            status = request.POST.get(f'status_{predmet.id}')
            if status == 'enr' and predmet.id not in existing_predmeti_ids:
                upisni_list_entries.append(
                    UpisniList(predmet=predmet, korisnik=student, status=status, semester=semestar_choice)
                )

        UpisniList.objects.bulk_create(upisni_list_entries)

        return redirect('student_dashboard')

    context = {
        'student': student,
        'predmeti': predmeti,
        'semestar_choice': semestar_choice,
    }
    return render(request, 'upisni_list.html', context)

@student_required
def delete_upisni_list_entry(request, upisni_id):
    upisni_entry = get_object_or_404(UpisniList, id=upisni_id)
    upisni_entry.delete()
    return redirect('student_dashboard')

@student_required
def create_upisni_list_student(request):
    student_id=request.user.id
    student = get_object_or_404(Korisnik, id=student_id)

    if request.method == 'POST':
        semestar_choice = request.POST.get('semestar_choice')
        return redirect('create_upisni_list_display_student',semestar_choice=semestar_choice)

    context = {
        'student': student,
    }
    return render(request, 'semester_choice_student.html', context)


def check_last_year(request):
    students = Korisnik.objects.all()
    students_last_year = []

    for student in students:
        if student.status == 'red':
            check=UpisniList.objects.filter(korisnik=student,semester=5,status='enr').count()
            check+=UpisniList.objects.filter(korisnik=student,semester=6,status='enr').count()
            if check >0:
                students_last_year.append(student)
            
        elif student.status == 'izv':
            check=UpisniList.objects.filter(korisnik=student,semester=7,status='enr').count()
            check+=UpisniList.objects.filter(korisnik=student,semester=8,status='enr').count()
            if check > 0:
                students_last_year.append(student)
        

    return render(request, 'check_last_year.html', {'students_last_year': students_last_year})
