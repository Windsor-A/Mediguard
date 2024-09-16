
import boto3
import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm, ReportForm, ResolveForm, ReportFileForm, PracticeForm
from .models import Profile, Report, ReportFile, Practice
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render



@login_required(login_url='MediGuard:login')
def user_dashboard(request):
    user_groups = request.user.groups.all()
    is_siteAdmin = user_groups.filter(name='Site Admin').exists()
    reports = Report.objects.filter(whistleblower=request.user)

    sort_order = {'New': 1, 'In Progress': 2, 'Resolved': 3}

    reports = sorted(reports, key=lambda x: (sort_order[x.status], x.date_time))


    return render(request, 'user_dashboard.html', {
        'is_siteAdmin': is_siteAdmin,
        'reports': reports,
    })


def home_page(request):
    user_groups = request.user.groups.all()
    is_siteAdmin = user_groups.filter(name='Site Admin').exists()

    return render(request, 'home_page.html', {'is_siteAdmin': is_siteAdmin})


def login(request):
    if request.user.is_authenticated:
        return redirect('')
    else:
        return render(request, 'login.html')




def view_profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})


@login_required(login_url='MediGuard:login')
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})


# NEW REPORT TO PASS AnonymousReportSubmissionTest
def report(request):
    is_siteAdmin = request.user.groups.filter(name='Site Admin').exists() if request.user.is_authenticated else False

    if request.method == 'POST':
        report_form = ReportForm(request.POST, request.FILES)
        practice_form = PracticeForm(request.POST)

        if report_form.is_valid() and practice_form.is_valid():
            new_report = report_form.save(commit=False)
            new_practice = practice_form.save()
            new_practice.save()

            if request.user.is_authenticated:
                new_report.whistleblower = request.user
            new_report.practice = new_practice
            new_report.save()

            files = request.FILES.getlist('file')
            for f in files:
                f = ReportFile(report=new_report, file=f)
                f.save()

            return redirect('MediGuard:report_submitted', report_id = new_report.id)

    else:
        report_form = ReportForm()
        practice_form = PracticeForm()

    return render(request, 'report.html', {
        'report_form': report_form,
        'is_siteAdmin': is_siteAdmin,
        'practice_form': practice_form
    })

def report_submitted(request, report_id):
    user_groups = request.user.groups.all()
    report = Report.objects.get(id=report_id)
    is_siteAdmin = user_groups.filter(name='Site Admin').exists()

    return render(request, 'report_submitted.html', {'is_siteAdmin': is_siteAdmin, 'report': report})


@login_required(login_url='MediGuard:login')
def report_list(request):
    user_groups = request.user.groups.all()
    is_siteAdmin = user_groups.filter(name='Site Admin').exists()
    if is_siteAdmin:
        template_name = 'report_list.html'
        reports = Report.objects.all()
        sort_order = {'New': 1, 'In Progress': 2, 'Resolved': 3}
        reports = sorted(reports, key=lambda x: (sort_order[x.status], x.date_time))
        return render(request, template_name, {'is_siteAdmin': is_siteAdmin, 'reports': reports})
    else:
        return redirect('MediGuard:home_page')






@login_required(login_url='MediGuard:login')
def report_detail(request, report_id):
    user_groups = request.user.groups.all()
    is_siteAdmin = user_groups.filter(name='Site Admin').exists()
    report = Report.objects.get(id=report_id)
    if is_siteAdmin or request.user== report.whistleblower:
        files = ReportFile.objects.filter(report=report)
        if report.status == ('New' or 'new') and is_siteAdmin:
            report.status = 'In Progress'
            report.save()
            return redirect('MediGuard:report_detail', report_id=report_id)
        if request.method == 'POST':
            form = ResolveForm(request.POST)

            if form.is_valid():
                report.notes = form.cleaned_data['notes']
                report.status = 'Resolved'
                report.save()
                return redirect('MediGuard:report_detail', report_id=report_id)
            else:
                return render(request, 'report_detail.html', {'form': form, 'is_siteAdmin': is_siteAdmin, 'report': report})
        else:
            form = ResolveForm()
        return render(request, 'report_detail.html', {'form': form, 'is_siteAdmin': is_siteAdmin, 'report': report, 'files': files})
    else:
        return redirect('MediGuard:home_page')

@login_required(login_url='MediGuard:login')
def delete_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report_files = ReportFile.objects.filter(report_id=report.id)
    '''for file in report_files:
        file.delete()'''
    if request.user == report.whistleblower:
        if not ('ON_HEROKU' in os.environ):
            try:
                os.environ.get('AWS_ACCESS_KEY_ID')
                os.environ.get('AWS_SECRET_ACCESS_KEY')
            except:
                import AWS_KEYS
                AWS_ACCESS_KEY_ID = AWS_KEYS.AccessKey
                AWS_SECRET_ACCESS_KEY = AWS_KEYS.SecretAccessKey
        else:
            AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
            AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
        AWS_QUERYSTRING_AUTH: False
        client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        for file in report_files:
            client.delete_object(Bucket='medi-giard', Key=str(file.file))
        report.delete()
        return redirect('MediGuard:user_dashboard')
    else:
        return HttpResponse("You don't have permission to delete this report.", status=403)


@login_required(login_url='MediGuard:login')
def practice_detail(request, practice_id):
    user_groups = request.user.groups.all()
    is_siteAdmin = user_groups.filter(name='Site Admin').exists()
    practice = Practice.objects.get(id=practice_id)
    reports = Report.objects.filter(practice=practice)
    count = reports.count()
    sort_order = {'New': 1, 'In Progress': 2, 'Resolved': 3}
    reports = sorted(reports, key=lambda x: (sort_order[x.status], x.date_time))

    return render(request, 'practice_detail.html', {'is_siteAdmin': is_siteAdmin, 'practice': practice, 'reports': reports, 'count': count})

