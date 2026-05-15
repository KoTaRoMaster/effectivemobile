from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .decorators import authenticate_required, staff_required, superuser_required
from .forms import *
from .models import Staff, Office, Schedule

# Create your views here.
User = get_user_model()


def home(request):
    return render(request, 'main/home.html')


def about(request):
    return render(request, 'main/about.html')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:home')

    error = {'error': ''}
    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            if not user.is_active:
                return redirect('main:login')
            login(request, user)
            return redirect('/')
        else:
            error['error'] = 'Неверный логин или пароль'
    return render(request, 'main/login.html', error)


# USER PERMISSIONS
@authenticate_required
def profile_view(request):
    user = request.user
    data = {}

    if user.is_superuser:
        data['role'] = 'Администратор'
    elif user.is_staff:
        data['role'] = 'Персонал'
        staff = Staff.objects.filter(user=user).first()
        data['offices'] = staff.offices.all()
    else:
        data['role'] = 'Пользователь'

    return render(request, 'main/profile.html', {'data': data})


@authenticate_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('main:profile')
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'main/profile_edit.html', {'form': form})


@authenticate_required
def records_view(request):
    offices = Office.objects.all()

    return render(request, 'main/records.html', {'offices': offices})


@authenticate_required
def records_write_view(request, office_id, data):
    if request.method == 'POST':
        selected = request.POST.get('selected_slots')
        if selected:
            ids = selected.split(',')
            schedules = Schedule.objects.filter(
                id__in=ids,
                user__isnull=True
            )

            for schedule in schedules:
                schedule.user = request.user
                schedule.save()

        return redirect('main:records')

    office = Office.objects.get(id=office_id)
    day = office.day_set.filter(date=data).first()

    context = {
        'office': office,
        'day': day,
    }

    return render(request, 'main/records_write.html', context)


@authenticate_required
def user_records_view(request):
    schedules = Schedule.objects.filter(user=request.user).all()

    offices = []
    days = []

    for schedule in schedules:
        if schedule.day not in days:
            days.append(schedule.day)

        if schedule.day.office not in offices:
            offices.append(schedule.day.office)

    offices = sorted(offices, key=lambda office: office.name)
    days = sorted(days, key=lambda day: day.date)
    schedules = sorted(schedules, key=lambda schedule: schedule.from_time)

    context = {
        'offices': offices,
        'days': days,
        'schedules': schedules,
    }

    return render(request, 'main/user_records.html', context)


@authenticate_required
def logout_view(request):
    logout(request)
    return redirect('main:login')


# STAFF PERMISSIONS
@staff_required
def staff_view(request):
    if request.user.is_superuser:
        offices = Office.objects.all()
    else:
        staff = Staff.objects.filter(user=request.user).first()
        offices = staff.offices.all()

    return render(request, 'main/staff.html', {'offices': offices})


@staff_required
def staff_edit_view(request, office_id, data):
    if request.method == 'POST':
        return redirect('main:staff')

    office = Office.objects.get(id=office_id)
    day = office.day_set.filter(date=data).first()

    context = {
        'office': office,
        'day': day,
    }

    return render(request, 'main/staff_edit.html', context)


# ADMIN PERMISSIONS
@superuser_required
def admin_view(request):
    users = User.objects.all()

    return render(request, 'main/admin.html', {'users': users})


@superuser_required
def admin_users_partial(request):
    users = User.objects.all()

    return render(request, 'main/admin/users_table.html', {'users': users})


@superuser_required
def admin_offices_partial(request):
    offices = Office.objects.all()

    return render(request, 'main/admin/offices_table.html', {'offices': offices})


@superuser_required
def admin_staff_partial(request):
    staff_members = Staff.objects.select_related('user').prefetch_related('offices')

    return render(request, 'main/admin/staff_table.html', {'staff_members': staff_members})


@superuser_required
def admin_user_create_view(request):

    if request.method == 'POST':
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:admin')
    else:
        form = AdminUserCreateForm()

    return render(request, 'main/admin_create_user.html', {'form': form})


@superuser_required
def admin_staff_create_view(request):
    if request.method == 'POST':
        form = AdminStaffCreateForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            user.is_staff = True
            user.save()
            staff = Staff.objects.get(user=user)
            offices = form.cleaned_data['offices']
            staff.offices.add(*offices)
            staff.save()
            return redirect('main:admin')
    else:
        form = AdminStaffCreateForm()

    return render(request, 'main/admin_create_staff.html', {'form': form})


@superuser_required
def admin_office_create_view(request):
    if request.method == 'POST':
        form = AdminOfficeCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:admin')
    else:
        form = AdminOfficeCreateForm()

    return render(request, 'main/admin_create_office.html', {'form': form})


@superuser_required
def admin_edit_user(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('main:admin')
    else:
        form = AdminUserEditForm(instance=user)

    context = {
        'form': form,
        'user_obj': user
    }
    return render(request, 'main/admin_edit_user.html', context)


@superuser_required
def admin_edit_staff(request, staff_id):
    staff = Staff.objects.get(id=staff_id)

    if request.method == 'POST':
        form = AdminStaffEditForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('main:admin')
    else:
        form = AdminStaffEditForm(instance=staff)

    context = {
        'form': form,
        'staff_obj': staff
    }

    return render(request, 'main/admin_edit_staff.html', context)


@superuser_required
def admin_edit_office(request, office_id):
    office = Office.objects.get(id=office_id)

    if request.method == 'POST':
        form = AdminOfficeEditForm(request.POST, instance=office)
        if form.is_valid():
            form.save()
            return redirect('main:admin')
    else:
        form = AdminOfficeEditForm(instance=office)

    context = {
        'form': form,
        'office_obj': office
    }
    return render(request, 'main/admin_edit_office.html', context)


@superuser_required
@require_POST
def admin_delete_users(request):
    ids = request.POST.get('ids[]')
    ids = [int(id) for id in ids.split(',')]
    users = User.objects.filter(id__in=ids).all()

    for user in users:
        user.is_active = False
        user.save()

    return JsonResponse({'success': True})


@superuser_required
@require_POST
def admin_delete_staffs(request):
    ids = request.POST.get('ids[]')
    ids = [int(id) for id in ids.split(',')]

    staffs = Staff.objects.filter(id__in=ids)

    for staff in staffs.all():
        staff.user.is_staff = False
        staff.user.save()
    staffs.delete()

    return JsonResponse({'success': True})


@superuser_required
@require_POST
def admin_delete_offices(request):
    ids = request.POST.get('ids[]')
    ids = [int(id) for id in ids.split(',')]
    Office.objects.filter(id__in=ids).delete()

    return JsonResponse({'success': True})
