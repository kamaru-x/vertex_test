from django.shortcuts import render,redirect
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from administrator.models import Category,Product,Lead,Lead_Update,Lead_Schedule,Attachments,Proposal,Sales_Target,User,Task,Notification
from datetime import date
from django.db.models import Q
import math
from django.http import HttpResponse
import json

# Create your views here.

#################################################################################

def signin(request):
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if request.user.is_superuser:
                return redirect('dashboard')
            elif request.user.is_salesman:
                return redirect('dashboard')
        else:
            messages.error(request,'incorrect username or password')
            return redirect('.')
    return render(request,'login.html')

#################################################################################

# @user_passes_test(lambda u: u.is_superuser)
@login_required
def dashboard(request):

    d = date.today()
    year = d.year

    if request.user.is_superuser:
        total_leads = Lead.objects.exclude(Status=0)
        Lead_Faild = total_leads.filter(Status=3,Lead_Status=0)
        Lead_Succes = total_leads.exclude(Status=3).exclude(Lead_Status=0)

        total_opportunities = Lead_Succes.count()
        Opportunity_Faild = total_leads.filter(Status=2,Lead_Status=1)
        Opportunity_Success = total_leads.filter(Q(Lead_Status=2)|Q(Lead_Status=3))

        total_proposals = Proposal.objects.all()
        Proposal_Success = Proposal.objects.filter(Proposal_Status = 1)
        Proposal_Faild = Proposal.objects.filter(Proposal_Status = 0)
        Proposal_Pending = Proposal.objects.filter(Proposal_Status = 10)

        total_clients = Lead.objects.filter(Lead_Status=2,Status=1).count()
        meetings_today = Lead_Schedule.objects.filter(AddedDate=date.today()).count()

        salesmans = Sales_Target.objects.filter(From__year = year)

        targets = Sales_Target.objects.all()


        proposal_success_volume = 0 
        proposal_failed_volume = 0
        proposal_pending_volume = 0

        above_80 = 0
        above_50 = 0
        below_50 = 0

        for p in total_proposals:
            if p.Proposal_Status == 1:
                if p.PO_Value:
                    proposal_success_volume += p.PO_Value

            elif p.Proposal_Status == 0:
                if p.Grand_Total:
                    proposal_failed_volume += p.Grand_Total

            elif p.Proposal_Status == 10:
                if p.Grand_Total:
                    proposal_pending_volume += p.Grand_Total
        
        for s in salesmans:
            t = (s.Archived / s.Targets) * 100
            if t >= 80 :
                above_80 += 1
            elif t > 50 and t < 80 :
                above_50 += 1
            elif t < 50:
                below_50 += 1

        yrs = []

        reports = []

        for target in targets:
            yrs.append(target.From.year)
        years = [*set(yrs)]
        years.sort()
        
        for year in years:
            archived = 0
            total_target = 0
            ts = Sales_Target.objects.filter(From__year = year)
            for t in ts:
                archived += t.Archived
                total_target += t.Targets
            report = {'year':int(year),'archived':int(archived),'total_target':int(total_target)}
            reports.append(report)

        
        overall_given_target = 0
        overall_achived_target = 0

        for r in reports:
            overall_given_target += r['total_target']
            overall_achived_target += r['archived']

        proposal_expair_today = Proposal.objects.filter(Expire_Date = date.today(),Proposal_Status=10).count()

########################################################################################################################

    else:
        total_leads = Lead.objects.exclude(Status=0).filter(Salesman=request.user)
        Lead_Faild = total_leads.filter(Status=3,Lead_Status=0)
        Lead_Succes = total_leads.exclude(Status=3).exclude(Lead_Status=0)

        total_opportunities = Lead_Succes.count()
        Opportunity_Faild = total_leads.filter(Status=2,Lead_Status=1)
        Opportunity_Success = total_leads.filter(Q(Lead_Status=2)|Q(Lead_Status=3))

        total_proposals = Proposal.objects.filter(Lead__Salesman=request.user)
        Proposal_Success = Proposal.objects.filter(Proposal_Status = 1,Lead__Salesman=request.user)
        Proposal_Faild = Proposal.objects.filter(Proposal_Status = 0,Lead__Salesman=request.user)
        Proposal_Pending = Proposal.objects.filter(Proposal_Status = 10,Lead__Salesman=request.user)

        total_clients = Lead.objects.filter(Lead_Status=2,Status=1,Salesman=request.user).count()
        meetings_today = Lead_Schedule.objects.filter(AddedDate=date.today(),Lead__Salesman=request.user).count()

        salesmans = Sales_Target.objects.filter(Salesman=request.user,From__year = year)

        targets = Sales_Target.objects.filter(Salesman=request.user)

        proposal_success_volume = 0 
        proposal_failed_volume = 0
        proposal_pending_volume = 0

        above_80 = 0
        above_50 = 0
        below_50 = 0

        for p in total_proposals:
            if p.Proposal_Status == 1:
                if p.PO_Value:
                    proposal_success_volume += p.PO_Value

            elif p.Proposal_Status == 0:
                if p.Grand_Total:
                    proposal_failed_volume += p.Grand_Total

            elif p.Proposal_Status == 10:
                if p.Grand_Total:
                    proposal_pending_volume += p.Grand_Total
        
        a = Sales_Target.objects.filter(From__year=year).last()
        if a:
            above_80 = a.Targets
            below_50 = proposal_success_volume
        else:
            above_80 = 0
            below_50 = 0

        yrs = []
        reports = []

        for target in targets:
            yrs.append(target.From.year)
        years = [*set(yrs)]
        years.sort()
        
        for year in years:
            archived = 0
            total_target = 0
            ts = Sales_Target.objects.filter(From__year = year).last()
            # for t in ts:
            archived += ts.Archived
            total_target += ts.Targets
            report = {'year':int(year),'archived':int(archived),'total_target':int(total_target)}
            reports.append(report)

        
        overall_given_target = 0
        overall_achived_target = 0

        for r in reports:
            overall_given_target += r['total_target']
            overall_achived_target += r['archived']

        proposal_expair_today = Proposal.objects.filter(Expire_Date = date.today(),Proposal_Status=10,Lead__Salesman=request.user).count()

#####################################################################################################################################

    try:
        lead_success_percentage = (Lead_Succes.count() / total_leads.count()) * 100
    except:
        lead_success_percentage = 0
    
    try:
        lead_failed_percentage = (Lead_Faild.count() / total_leads.count()) * 100
    except:
        lead_failed_percentage = 0

    try:
        opportunity_success_percentage = (Opportunity_Success.count() / total_opportunities) * 100
    except:
        opportunity_success_percentage = 0

    try:
        opportunity_faild_percentage = (Opportunity_Faild.count() / total_opportunities) * 100
    except:
        opportunity_faild_percentage = 0

    try:
        proposal_pending_percentage = (Proposal_Pending.count() / total_proposals.count()) * 100
    except:
        proposal_pending_percentage = 0
    
    try:
        proposal_success_percentage = (Proposal_Success.count() / total_proposals.count()) * 100
    except:
        proposal_success_percentage = 0
    
    try:
        proposal_failed_percentage = (Proposal_Faild.count() / total_proposals.count()) * 100
    except:
        proposal_failed_percentage = 0


    ls_percentage = math.floor(lead_success_percentage)
    lf_percentage = math.ceil(lead_failed_percentage)

    os_percentage = math.floor(opportunity_success_percentage)
    of_percentage = math.ceil(opportunity_faild_percentage)

    pp_percentage = math.ceil(proposal_pending_percentage)
    ps_percentage = math.floor(proposal_success_percentage)
    pf_percentage = math.ceil(proposal_failed_percentage)

    context = {
        'total_leads' : total_leads.count(),
        'total_opportunities' : total_opportunities,
        'total_proposals' : total_proposals.count(),
        'total_clients' : total_clients,
        'meetings_today' : meetings_today,
        'lead_success' : Lead_Succes.count(),
        'lead_faild' : Lead_Faild.count(),
        'opportunity_success' : Opportunity_Success.count(),
        'opportunity_failed' : Opportunity_Faild.count(),
        'proposal_success' : Proposal_Success.count(),
        'proposal_failed' : Proposal_Faild.count(),
        'proposal_pending' : Proposal_Pending.count(),
        'psv' : proposal_success_volume,
        'ppv' : proposal_pending_volume,
        'pfv' : proposal_failed_volume,
        'ab80' : above_80,
        'ab50' : above_50,
        'bl50' : below_50,
        'reports':reports,
        'success_percentage' : ls_percentage,
        'faild_percentage' : lf_percentage,
        'os_percentage' : os_percentage,
        'of_percentage' : of_percentage,
        'pp_percentage' : pp_percentage,
        'ps_percentage' : ps_percentage,
        'pf_percentage' : pf_percentage,
        'yrs' : yrs,
        'overall_given_target' : overall_given_target,
        'overall_achived_target' : overall_achived_target,
        'proposal_expair_today' : proposal_expair_today,
    }

    return render(request,'index.html',context)

#################################################################################

@login_required
def salesboard(request):
    return render(request,'salesboard.html')

#################################################################################

@login_required
def changepassword(request):
    user = request.user
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.warning(request,'password does not matching')
            return redirect('/change-password/')
        else:
            user.set_password(password1)
            user.save()
            return redirect('dashboard')
    return render(request,'change-password.html')

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def change_salesman_password(request,id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.warning(request,'password does not matching')
            return redirect('/change-salesman-password/%s' %user.id)
        else:
            user.set_password(password1)
            user.save()
            return redirect('list-salesman')
    return render(request,'salesman-password.html',{'user':user})

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def signout(request):
    logout(request)
    return redirect('sign-in')

#################################################################################

def header(request):
    notifications = Notification.objects.filter(notification_user=request.user)
    return render(request,'header.html',{'notifications':notifications})