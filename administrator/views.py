from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from administrator.models import Category,Product,Lead,Lead_Update,Lead_Schedule,Attachments,Task,Salesman_Report,Review,Proposal,Sales_Target
from datetime import datetime,date
from datetime import date as dt
from django.contrib import messages
from u_auth.models import User
from datetime import timedelta
from django.db.models import Q
from administrator.set_fun import setTarget
from django.core.paginator import Paginator
import math
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
# Create your views here.

def setip(request):
    x_forw_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forw_for is not None:
        ip = x_forw_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return(ip)

def setcount():
    categories = Category.objects.all()
    for category in categories:
        count = Product.objects.filter(Category=category).filter(Status=1).count()
        category.Products = count
        category.save()


def setreport():
    users = User.objects.filter(is_salesman=True)

    ids = []

    for u in users:
        ids.append(u.id)
    
    for i in ids:
        user = User.objects.get(id=i)
        report = Salesman_Report.objects.get(Salesman=user)

        lead_total = Lead.objects.filter(Salesman=user).exclude(Status=0)
        lead_failed = lead_total.filter(Status=3,Lead_Status=0)
        # lead_success = lead_total.exclude(Status=3).exclude(Lead_Status=0)
        lead_success = lead_total.exclude(Status=3).filter(Q(Lead_Status=1)|Q(Lead_Status=2))

        opportunity_total = lead_success
        opportunity_failed = lead_total.filter(Status=2,Lead_Status=1)
        opportunity_success = lead_total.filter(Q(Lead_Status=2)|Q(Lead_Status=3))

        proposal_total = Proposal.objects.filter(Lead__Salesman = user)
        proposal_failed = proposal_total.filter(Proposal_Status = 0)
        proposal_success = proposal_total.filter(Proposal_Status = 1)

                            ##################################

        report.Pending_Tasks = Task.objects.filter(Task_Status=0).filter(Salesman=user).count()
        report.Completed_Tasks = Task.objects.filter(Task_Status=1).filter(Salesman=user).count()

        report.Lead_Total = lead_total.count()
        report.Lead_Faild = lead_failed.count()
        report.Lead_Succes = lead_success.count()

        report.Opportunity_Total = opportunity_total.count()
        report.Opportunity_Faild = opportunity_failed.count()
        report.Opportunity_Success = opportunity_success.count()

        report.Proposal_Total = proposal_total.count()
        report.Proposal_Success = proposal_success.count()
        report.Proposal_Faild = proposal_failed.count()

        report.SV_Pending = 124651684 #Lead.objects.filter(Salesman=user).filter(Lead_Status=1).count()
        report.SV_Success = 1398498498 #Lead.objects.filter(Salesman=user).filter(Lead_Status=2).count()
        report.SV_Failed = 145168465 #Lead.objects.filter(Salesman=user).filter(Lead_Status=4).count()

        schedules = Lead_Schedule.objects.filter(Lead__Salesman=user)
        previous = []
        upcoming = []

        for schedule in schedules:
            if schedule.AddedDate < dt.today() :
                previous.append(schedule)
            elif schedule.AddedDate >= dt.today() :
                upcoming.append(schedule)

        report.Upcoming_Meetings = len(upcoming)
        report.Previous_Meetings = len(previous)

        report.save()

def setmeeting():
    leads = Lead.objects.filter(Status=1)

    ids = []

    for l in leads:
        ids.append(l.id)
    
    for i in ids:
        lead = Lead.objects.get(id=i)
        schedules = Lead_Schedule.objects.filter(Lead=lead)
        previous = []
        upcoming = []

        for schedule in schedules:
            if schedule.AddedDate < dt.today() :
                previous.append(schedule)
            elif schedule.AddedDate >= dt.today() :
                upcoming.append(schedule)

        lead.Previous_Meetings = len(previous)
        lead.Upcoming_Meetings = len(upcoming)
        lead.save()


#################################################################################

@login_required
def add_category(request):

    r = Category.objects.last()

    if r:
        refer = f'VECR-00{r.id+1}'
    else:
        refer = 'VECR-001'
    
    context = {
        'refer':refer
    }

    if request.method == 'POST':
        date = dt.today()
        user = request.user.id
        ip = setip(request)
        name = request.POST.get('name')
        description = request.POST.get('description')

        value = Category(Date=date,AddedBy=user,Ip=ip,Name=name,Reference=refer,Description=description)
        value.save()
        # messages.success(request,'New category added successfully')
        return redirect('list-category')

    return render(request,'category-add.html',context)

#################################################################################

@login_required
def list_category(request):
    # categories = Category.objects.filter(Status=1).order_by('-id')
    # count = 10
    # count = request.GET.get('count')
    # print(count)
    p = Paginator(Category.objects.filter(Status=1).order_by('-id'),10)
    page = request.GET.get('page')
    categories = p.get_page(page)
    nums = 'a' * categories.paginator.num_pages

    if request.method == 'POST':
        id = request.POST.get('id')
        category = Category.objects.get(id=id)
        category.Status = 0
        category.save()
        return redirect('list-category')

    context = {
        'categories' : categories,
        'nums' : nums,
    }
    return render(request,'category-list.html',context)

#################################################################################

@login_required
def view_category(request,cid):
    category = Category.objects.get(id=cid)
    products = Product.objects.filter(Category=category).filter(Status=1).order_by('-id')
    if request.method == 'POST':
        id = request.POST.get('id')
        product = Product.objects.get(id=id)
        product.Category = None
        product.save()
        setcount()
        return redirect('.')
    context = {
        'category' : category,
        'products' : products,
    }
    return render(request,'category-view.html',context)

#################################################################################

@login_required
def edit_category(request,cid):
    category = Category.objects.get(id=cid)
    if request.method == 'POST':
        category.Name = request.POST.get('name')
        category.Description = request.POST.get('description')
        category.save()
        return redirect('list-category')
    context = {
        'category':category,
    }
    return render(request,'category-edit.html',context)

#################################################################################

@csrf_exempt
def check_part_number(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        try:
            Product.objects.get(Name=name)
            return JsonResponse({'status':False})
        except:
            return JsonResponse({'status':True})

#################################################################################

@login_required
def add_product(request):

    categories = Category.objects.filter(Status=1)
    r = Product.objects.last()
    date = dt.today()
    user = request.user.id
    ip = setip(request)

    if r:
        refer = f'VEPR-00{r.id+1}'
    else:
        refer = 'VEPR-001'

    if request.method == 'POST':
        category = request.POST.get('category')
        name = request.POST.get('name')
        price = request.POST.get('price')
        sprice = request.POST.get('sprice') or None
        description = request.POST.get('description')
        unit = request.POST.get('unit')

        try:
            c = Category.objects.get(id=category)
        except:
            messages.error(request,'no category selected')
            return redirect('.')
        
        try:
            Product.objects.get(Name=name,Category=c)
            messages.error(request,'product already exists with same part number')
            return redirect('.')
        except:
            value = Product(Date=date,AddedBy=user,Ip=ip,Category=c,Name=name,Buying_Price=price,Selling_Price=sprice,Reference=refer,Description=description,Unit=unit)
            value.save()
            c.Products = c.Products+1
            c.save()
            setcount()

        # messages.success(request,'new product added successfully')
        return redirect('list-product')
    
    context = {
        'refer':refer,
        'categories':categories,
    }

    return render(request,'product-add.html',context)

#################################################################################

@login_required
def list_products(request):
    # products = Product.objects.filter(Status=1).order_by('-id')
    p = Paginator(Product.objects.filter(Status=1).order_by('-id'),10)
    page = request.GET.get('page')
    products = p.get_page(page)
    nums = 'a' * products.paginator.num_pages
    if request.method == 'POST' :
        id = request.POST.get('id')
        product = Product.objects.get(id=id)
        product.Status = 0
        product.save()
        setcount()
        return redirect('list-product')
    context = {
        'products' : products,
        'nums' : nums,
    }
    return render(request,'product-list.html',context)

#################################################################################

@login_required
def edit_product(request,pid):
    product = Product.objects.get(id=pid)
    user = request.user.id
    ip = setip(request)
    categories = Category.objects.filter(Status=1)

    if request.method == 'POST':
        product.EditedBy = user
        product.Edited_Date = date.today()
        product.EditedIp = ip
        category = request.POST.get('category')
        c = Category.objects.get(id=category)

        product.Category = c
        product.Name = request.POST.get('name')
        product.Buying_Price = request.POST.get('price')
        product.Selling_Price = request.POST.get('sprice') or None
        product.Description = request.POST.get('description')
        product.Unit = request.POST.get('unit')
        product.save()
        setcount()

        # messages.success(request,'product details edited successfully')
        return redirect('list-product')

    context = {
        'categories' : categories,
        'product' : product,
    }

    return render(request,'edit-product.html',context)

#################################################################################

@login_required
def view_product(request,pid):
    product = Product.objects.get(id=pid)

    context = {
        'product' : product,
    }

    return render(request,'view-product.html',context)

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def add_salesman(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        qid = request.POST.get('id-number')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        country = request.POST.get('country')
        password = request.POST.get('password')

        user = User.objects.create(first_name=name,Qatar_ID=qid,email=email,
        Mobile=mobile,Address=address,Country=country,is_salesman=True,username=email)
        user.save()
        user.set_password(password)
        user.save()

        salesman = User.objects.last()
        report = Salesman_Report(Salesman=salesman)
        report.save()

        # messages.success(request,'new supervisor created successfully')
        return redirect('list-salesman')

    return render(request,'salesman-add.html')

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def list_salesman(request):
    setreport()
    salesmans = User.objects.exclude(is_superuser=True).filter(is_active=True).order_by('-id')
    rpts = Salesman_Report.objects.filter(Status=1)
    reports = []
    for report in rpts:
        archived = 0
        pending = 0
        faild = 0
        a_proposals = Proposal.objects.filter(Lead__Salesman = report.Salesman).filter(Proposal_Status=1)
        p_proposals = Proposal.objects.filter(Lead__Salesman = report.Salesman).filter(Proposal_Status=10)
        f_proposals = Proposal.objects.filter(Lead__Salesman = report.Salesman).filter(Proposal_Status=0)

        for a in a_proposals:
            if a.Grand_Total:
                archived += int(a.PO_Value)
        for p in p_proposals:
            if p.Grand_Total:
                pending += p.Grand_Total
        for f in f_proposals:
            if f.Grand_Total:
                faild += f.Grand_Total
        
        r = {'report':report,'archived':archived,'pending':pending,'faild':faild,'success_proposals':len(a_proposals),'pending_proposals':len(p_proposals),'failed_proposals':len(f_proposals)}
        reports.append(r)

    if request.method == 'POST' :
        id = request.POST.get('id')
        salesman = User.objects.get(id=id)
        salesman.is_active = False
        salesman.save()
        report = Salesman_Report.objects.get(Salesman=salesman)
        report.Status = 0
        report.save()
        return redirect('list-salesman')
    
    p = Paginator(reports,10)
    page = request.GET.get('page')
    reports = p.get_page(page)
    nums = 'a' * reports.paginator.num_pages

    context = {
        'salesmans':salesmans,
        'reports' : reports,
        'nums' : nums,
    }
    return render(request,'salesman-list.html',context)

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def edit_salesman(request,uid):
    salesman = User.objects.get(id=uid)
    if request.method == 'POST':
        salesman.first_name = request.POST.get('name')
        salesman.Qatar_ID = request.POST.get('id-number')
        salesman.email = request.POST.get('email')
        salesman.Mobile = request.POST.get('mobile')
        salesman.Address = request.POST.get('address')
        salesman.Country = request.POST.get('country')
        salesman.username = request.POST.get('email')
        salesman.save()
        # messages.success(request,'salesman detail edited')
        return redirect('/salesman-view/%s' %salesman.id)

    context = {
        'salesman':salesman
    }
    return render(request,'edit-salesman.html',context)

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def salesman_view(request,sid):
    setmeeting()
    setreport()
    d = dt.today()
    year = d.year
    salesman = User.objects.get(id=sid)
    schedules = Lead_Schedule.objects.filter(Lead__Salesman=salesman)
    leads = Lead.objects.filter(Salesman=salesman).filter(Lead_Status=0,Status=1)
    opportunities = Lead.objects.filter(Salesman=salesman).filter(Lead_Status=1,Status=1)
    clients = Lead.objects.filter(Salesman=salesman).filter(Lead_Status=2,Status=1)
    projects = Proposal.objects.filter(Lead__Salesman=salesman).filter(Proposal_Status=1)
    p_task = Task.objects.filter(Salesman=salesman).filter(Task_Status=0).exclude(Status=0).order_by('Due_Date')
    c_task = Task.objects.filter(Salesman=salesman).filter(Task_Status=1).exclude(Status=0).order_by('-Completed_Date')
    sales = Sales_Target.objects.filter(Salesman=salesman).filter(From__year = d.year)
    proposals = Proposal.objects.filter(Lead__Salesman = salesman)
    t_count = len(p_task)

    total_target = Sales_Target.objects.filter(From__year = year,Salesman=salesman).last()

    s_proposals = Proposal.objects.filter(Lead__Salesman=salesman,Proposal_Status=1)
    f_proposals = Proposal.objects.filter(Lead__Salesman=salesman,Proposal_Status=0)

    target_archived = 0
    target_failed = 0

    for proposal in s_proposals:
        target_archived += int(proposal.PO_Value)

    for proposal in f_proposals:
        target_failed += proposal.Grand_Total


    if request.method == 'POST':

        if request.POST.get('udate'):
            udate = request.POST.get('udate')
            udescription = request.POST.get('udescription')
            participents = request.POST.get('participents')
            id = request.POST.get('id')
            meeting = Lead_Schedule.objects.get(id=id)
            meeting.Update_Description = udescription
            meeting.Update_Date = udate
            meeting.Members = participents
            meeting.save()

            attachment = request.FILES.getlist('attachment')
            for a in attachment:
                if str(a).endswith(('.png', '.jpg', '.jpeg','.PNG','.JPG','.JPEG')):
                    format = 'image'
                else:
                    format = 'file'
                attach = Attachments(Attachment=a,Name=a,Format=format)
                attach.save()
                meeting.Attachment.add(attach)
                meeting.save()

            return redirect('/salesman-view/%s/' %salesman.id)
    
        if request.POST.get('taskid'):
            tid = request.POST.get('taskid')
            task = Task.objects.get(id=tid)
            date = request.POST.get('date')
            description = request.POST.get('update-description')
            task.Task_Status = 1
            task.Completed_Date = dt.today()
            task.save()

            data = Review(Task=task,Message=description,AddedDate=date)
            data.save()

            ld = Review.objects.last()
            attachment = request.FILES.getlist('attachment')
            for a in attachment:
                if str(a).endswith(('.png', '.jpg', '.jpeg','.PNG','.JPG','.JPEG')):
                    format = 'image'
                else:
                    format = 'file'
                attach = Attachments(Attachment=a,Name=a,Format=format)
                attach.save()
                ld.Attachments.add(attach)
                ld.save()
            return redirect('/salesman-view/%s/' %salesman.id)

    previous = []
    upcoming = []

    for schedule in schedules:
        if schedule.AddedDate < dt.today() :
            previous.append(schedule)
        elif schedule.AddedDate >= dt.today() :
            upcoming.append(schedule)

    monthly_report = []

    for month in range(1,13):
        proposals_report = Proposal.objects.filter(Lead__Salesman=salesman,PO_Date__year=year,PO_Date__month=month,Proposal_Status=1)
        # print(proposals_report.count())
        p_count = proposals_report.count()
        monthly_report.append(p_count)

    
    if total_target and target_archived != 0:
        p = (int(target_archived) / int(total_target.Targets)) * 100
        percentage = math.trunc(p)
        if percentage > 100:
            percentage = 100
    else :
        percentage = 0

    print(total_target,target_archived)

    p = Paginator(leads,10)
    page = request.GET.get('page')
    leads = p.get_page(page)
    nums = 'a' * leads.paginator.num_pages

    op = Paginator(opportunities,10)
    op_page = request.GET.get('page')
    opportunities = op.get_page(op_page)
    op_nums = 'a' * opportunities.paginator.num_pages

    pro = Paginator(proposals,10)
    pro_page = request.GET.get('page')
    proposals = pro.get_page(pro_page)
    pro_nums = 'a' * proposals.paginator.num_pages

    cli = Paginator(clients,10)
    cli_page = request.GET.get('page')
    clients = cli.get_page(cli_page)
    cli_nums = 'a' * clients.paginator.num_pages

    prj = Paginator(projects,10)
    prj_page = request.GET.get('page')
    projects = prj.get_page(prj_page)
    prj_nums = 'a' * projects.paginator.num_pages

    prv = Paginator(previous,10)
    prv_page = request.GET.get('page')
    previous = prv.get_page(prv_page)
    prv_nums = 'a' * previous.paginator.num_pages

    upc = Paginator(upcoming,10)
    upc_page = request.GET.get('page')
    upcoming = upc.get_page(upc_page)
    upc_nums = 'a' * upcoming.paginator.num_pages

    pt = Paginator(p_task,10)
    pt_page = request.GET.get('page')
    p_task = pt.get_page(pt_page)
    pt_nums = 'a' * p_task.paginator.num_pages

    ct = Paginator(c_task,10)
    ct_page = request.GET.get('page')
    c_task = ct.get_page(ct_page)
    ct_nums = 'a' * c_task.paginator.num_pages

    context = {
        'salesman':salesman,
        'previous' : previous,
        'upcoming' : upcoming,
        'leads' : leads,
        'opportunities' : opportunities,
        'clients' : clients,
        'projects' : projects,
        'ptasks' : p_task,
        'ctasks' : c_task,
        't_count' : t_count,
        'sales' : sales,
        'total_target' : total_target,
        'target_archived' : target_archived,
        'target_failed' : target_failed,
        'proposals' : proposals,
        'monthly_report' : monthly_report,
        'percentage' : percentage,
        'nums' : nums,
        'op_nums' : op_nums,
        'pro_nums' : pro_nums,
        'cli_nums' : cli_nums,
        'prj_nums' : prj_nums,
        'prv_nums' : prv_nums,
        'upc_nums' : upc_nums,
        'pt_nums' : pt_nums,
        'ct_nums' : ct_nums,
    }
    return render(request,'salesman-view.html',context)

#################################################################################

@login_required
def add_lead(request):
    user = request.user.id
    ip = setip(request)
    r = Lead.objects.last()
    salesmans = User.objects.filter(is_salesman=True)

    if r:
        refer = f'LEAD-00{r.id+1}'
    else:
        refer = 'LEAD-001'

    if request.method == 'POST':
        company = request.POST.get('company')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone = request.POST.get('number')
        ecdate = request.POST.get('date')
        esvalue = request.POST.get('value')
        state = request.POST.get('state')
        cname = request.POST.get('cname')
        cnumber = request.POST.get('cnumber')
        cmail = request.POST.get('cmail')
        salesman = request.POST.get('salesman')
        designation = request.POST.get('designation')

        if request.user.is_superuser:
            s = User.objects.get(id=salesman)
        else:
            s = request.user

        data = Lead(Date=date.today(),AddedBy=user,Ip=ip,Reference=refer,Company=company,Address=address,
        Email=email,Phone=phone,ECDate=ecdate,ESValue=esvalue,State=state,CName=cname,CNumber=cnumber,
        CMail=cmail,Salesman=s,Designation=designation)
        data.save()

        # report = Salesman_Report.objects.get(Salesman=s)
        # report.Lead_Total = report.Lead_Total+1
        # report.save()

        # messages.success(request,'created new lead')
        return redirect('list-lead')

    context = {
        'refer':refer,
        'salesmans' : salesmans,
    }

    return render(request,'leads-add.html',context)

#################################################################################

@login_required
def list_leads(request):
    setmeeting()
    if request.user.is_superuser:
        leads = Lead.objects.filter(Lead_Status=0).filter(Status=1).order_by('-id')
    else:
        leads = Lead.objects.filter(Salesman=request.user,Lead_Status=0).filter(Status=1).order_by('-id')
    if request.method == 'POST' :
        if request.POST.get('id') :
            id = request.POST.get('id')
            lead = Lead.objects.get(id=id)
            lead.Status = 0
            lead.save()

            salesman = lead.Salesman
            report = Salesman_Report.objects.get(Salesman=salesman)
            report.Lead_Total = report.Lead_Total - 1
            report.save()
            return redirect('list-lead')
        
        if request.POST.get('c'):
            c = request.POST.get('c')
            lead= Lead.objects.get(id=c)
            lead.Status = 3
            lead.Cancel_Date = date.today()
            lead.Cancel_Reason = request.POST.get('reason')
            lead.save()

            # salesman = lead.Salesman
            # report = Salesman_Report.objects.get(Salesman=salesman)
            # report.Lead_Faild = report.Lead_Faild + 1
            # report.save()
            return redirect('list-lead')
    
    p = Paginator(leads,10)
    page = request.GET.get('page')
    leads = p.get_page(page)
    nums = 'a' * leads.paginator.num_pages

    context = {
        'leads' : leads,
        'nums' : nums
    }
    return render(request,'leads-list.html',context)

#################################################################################

@login_required
def view_lead(request,lid):
    lead = Lead.objects.get(id=lid)
    user = request.user.id
    d = dt.today()
    ip = setip(request)
    lead_update = Lead_Update.objects.filter(Lead=lead)
    # attachments = Attachments.objects.all()

    if request.method == 'POST':
        if request.POST.get('date'):
            date = request.POST.get('date')
            description = request.POST.get('update-description')

            data = Lead_Update(Date=d,AddedBy=user,Ip=ip,Lead=lead,Description=description,AddedDate=date)
            data.save()

            ld = Lead_Update.objects.filter(Lead=lead).filter(AddedBy=user).last()
            attachment = request.FILES.getlist('attachment')
            
            for a in attachment:
                if str(a).endswith(('.png', '.jpg', '.jpeg','.PNG','.JPG','.JPEG')):
                    format = 'image'
                else:
                    format = 'file'
                attach = Attachments(Attachment=a,Name=a,Format=format)
                attach.save()
                ld.Attachments.add(attach)
                ld.save()

        if request.POST.get('sdate'):
            sdate = request.POST.get('sdate')
            mode = request.POST.get('mode')
            ftime = request.POST.get('from')
            to = request.POST.get('to')
            sdescription = request.POST.get('sdescription')

            data = Lead_Schedule(Date=d,AddedBy=user,Ip=ip,Lead=lead,Mode=mode,From=ftime,To=to,Description=sdescription,AddedDate=sdate)
            data.save()

        if request.POST.get('udate'):
            if request.POST.get('udate'):
                udate = request.POST.get('udate')
                udescription = request.POST.get('u-description')
                participends = request.POST.get('participents')
                id = request.POST.get('id')
                meeting = Lead_Schedule.objects.get(id=id)
                meeting.Update_Description = udescription
                meeting.Update_Date = udate
                meeting.Members = participends
                meeting.save()

                attachment = request.FILES.getlist('attach')
                for a in attachment:
                    if str(a).endswith(('.png', '.jpg', '.jpeg','.PNG','.JPG','.JPEG')):
                        format = 'image'
                    else:
                        format = 'file'
                    attach = Attachments(Attachment=a,Name=a,Format=format)
                    attach.save()
                    meeting.Attachment.add(attach)
                    meeting.save()

        return redirect('/view-lead/%s' %lead.id)

    schedules = Lead_Schedule.objects.filter(Lead=lead)

    previous = []
    upcoming = []

    for schedule in schedules:
        if schedule.AddedDate < dt.today() :
            previous.append(schedule)
        elif schedule.AddedDate >= dt.today() :
            upcoming.append(schedule)

    context = {
        'lead' : lead,
        'lead_update' : lead_update,
        # 'attachments' : attachments,
        'previous' : previous,
        'upcoming' : upcoming,
    }
    return render(request,'leads-view.html',context)

#################################################################################

@login_required
def edit_lead(request,lid):
    lead = Lead.objects.get(id=lid)
    user = request.user.id
    ip = setip(request)
    salesmans = User.objects.filter(is_salesman=True)

    if request.method == 'POST':
        lead.EditedBy = user
        lead.EditedIp = ip
        lead.Company = request.POST.get('company')
        lead.Address = request.POST.get('address')
        lead.Email = request.POST.get('email')
        lead.Phone = request.POST.get('number')
        date = request.POST.get('date')
        temp = lead.Date
        if date:
            lead.ECDate = date
        else:
            lead.ECDate = temp
        # lead.ECDate = datetime.strptime(date, "%Y-%m-%d")
        lead.ESValue = request.POST.get('value')
        lead.State = request.POST.get('state')
        lead.CName = request.POST.get('cname')
        lead.CNumber = request.POST.get('cnumber')
        lead.CMail = request.POST.get('cmail')
        lead.Designation = request.POST.get('designation')
        s = request.POST.get('salesman')
        salesman = User.objects.get(id=s)
        lead.Salesman = salesman
        lead.save()
        # messages.success(request,'lead data edited successfull')
        return redirect('list-lead')
    
    context = {
        'lead' : lead,
        'salesmans' : salesmans,
    }

    return render(request,'edit-lead.html',context)

#################################################################################

@login_required
def opertunity_convertion(request,lid):
    lead = Lead.objects.get(id=lid)
    lead.Lead_Status = 1
    lead.To_Opertunity = date.today()
    lead.save()
    # salesman = lead.Salesman
    # report = Salesman_Report.objects.get(Salesman=salesman)
    # report.Lead_Succes = report.Lead_Succes + 1
    # report.Opportunity_Total = report.Opportunity_Total + 1
    # report.save()
    return redirect('/opportunity-view/%s' %lead.id)

#################################################################################

@login_required
def canceld_leads(request):
    if request.user.is_superuser:
        leads = Lead.objects.filter(Lead_Status=0,Status=3)
    else:
        leads = Lead.objects.filter(Salesman=request.user,Lead_Status=0,Status=3)

    if request.user.is_superuser:
        opportunities = Lead.objects.filter(Status=2,Lead_Status=1)
    else:
        opportunities = Lead.objects.filter(Salesman=request.user,Status=2,Lead_Status=1)
        
    clients = Lead.objects.filter(Status=3,Lead_Status=2)
    projects = Lead.objects.filter(Status=3,Lead_Status=3)

    context = {
        'leads':leads,
        'opportunities':opportunities,
        'clients':clients,
        'projects':projects,
    }

    return render(request,'canceld.html',context)

#################################################################################

@login_required
def view_canceled(request,lid):
    lead = Lead.objects.get(id=lid)
    user = request.user.id
    d = dt.today()
    ip = setip(request)
    lead_update = Lead_Update.objects.filter(Lead=lead)
    # attachments = Attachments.objects.all()
    schedules = Lead_Schedule.objects.filter(Lead=lead)

    previous = []
    upcoming = []

    for schedule in schedules:
        if schedule.AddedDate < dt.today() :
            previous.append(schedule)
        elif schedule.AddedDate >= dt.today() :
            upcoming.append(schedule)

    context = {
        'lead' : lead,
        'lead_update' : lead_update,
        # 'attachments' : attachments,
        'previous' : previous,
        'upcoming' : upcoming,
    }
    return render(request,'canceled_lead_view.html',context)

#################################################################################

@login_required
def canceled_opertunity_view(request,lid):
    lead = Lead.objects.get(id=lid)
    user = request.user.id
    d = dt.today()
    ip = setip(request)
    lead_update = Lead_Update.objects.filter(Lead=lead)
    # attachments = Attachments.objects.all()
    schedules = Lead_Schedule.objects.filter(Lead=lead)

    previous = []
    upcoming = []

    for schedule in schedules:
        if schedule.AddedDate < dt.today() :
            previous.append(schedule)
        elif schedule.AddedDate >= dt.today() :
            upcoming.append(schedule)

    context = {
        'lead' : lead,
        'lead_update' : lead_update,
        # 'attachments' : attachments,
        'previous' : previous,
        'upcoming' : upcoming,
    }
    return render(request,'canceled_opportunity_view.html',context)

#################################################################################

@login_required
def canceled_client_view(request,lid):
    lead = Lead.objects.get(id=lid)
    user = request.user.id
    d = dt.today()
    ip = setip(request)
    lead_update = Lead_Update.objects.filter(Lead=lead)
    proposal = Proposal.objects.get(Lead=lead)
    # attachments = Attachments.objects.all()
    schedules = Lead_Schedule.objects.filter(Lead=lead)

    previous = []
    upcoming = []

    for schedule in schedules:
        if schedule.AddedDate < dt.today() :
            previous.append(schedule)
        elif schedule.AddedDate >= dt.today() :
            upcoming.append(schedule)

    context = {
        'lead' : lead,
        'lead_update' : lead_update,
        # 'attachments' : attachments,
        'previous' : previous,
        'upcoming' : upcoming,
        'proposal' : proposal,
    }
    return render(request,'canceled_client_view.html',context)

#################################################################################

@login_required
def canceled_project_view(request,lid):
    lead = Lead.objects.get(id=lid)
    user = request.user.id
    d = dt.today()
    ip = setip(request)
    lead_update = Lead_Update.objects.filter(Lead=lead)
    proposal = Proposal.objects.get(Lead=lead)
    # attachments = Attachments.objects.all()
    schedules = Lead_Schedule.objects.filter(Lead=lead)

    previous = []
    upcoming = []

    for schedule in schedules:
        if schedule.AddedDate < dt.today() :
            previous.append(schedule)
        elif schedule.AddedDate >= dt.today() :
            upcoming.append(schedule)

    context = {
        'lead' : lead,
        'lead_update' : lead_update,
        # 'attachments' : attachments,
        'previous' : previous,
        'upcoming' : upcoming,
        'proposal' : proposal,
    }
    return render(request,'canceled_project_view.html',context)

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def assign_target(request):
    setTarget()
    targets = Sales_Target.objects.all()
    t_s = User.objects.filter(is_salesman=True)

    yrs = []

    for target in targets:
        yrs.append(target.From.year)
    years = [*set(yrs)]
    years.sort(reverse=True)

    for year in years:
        salesmans = Sales_Target.objects.filter(From__year=year)
        for salesman in salesmans:
            proposals = Proposal.objects.filter(Date__year=year,Proposal_Status=1)
            archived = 0
            for proposal in proposals:
                archived += proposal.Grand_Total
            balance = int(salesman.Targets - archived)

            salesman.Archived = archived
            salesman.Balance = balance

    data = []

    for y in years :
        salesmans = Sales_Target.objects.filter(From__year = y).count()
        mans = Sales_Target.objects.filter(From__year = y )
        total = 0
        archived = 0
        balance = 0
        for man in mans:
            total = int(total + man.Targets)
            archived = int(archived + man.Archived)
            balance = int(balance + man.Balance)

        if balance == 0:
            balance = total
        if archived > total :
            balance = abs(balance)
            color = 'success'
        else:
            color = 'danger'


        d = {'year':y,'salesmans':salesmans,'total':total,'archived':archived,'balance':balance,'color':color}
        data.append(d)

    p = Paginator(data,10)
    page = request.GET.get('page')
    data = p.get_page(page)
    nums = 'a' * data.paginator.num_pages

    return render(request,'assign-target.html',{'data':data,'nums':nums})

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def target_setup(request):
    smans = User.objects.filter(is_salesman=True)
    salesmans = []
    d = dt.today()
    y = d.year
    years = []
    for x in range(y,y+500):
        years.append(x)
        years.sort()
        
    for s in smans:
        target = Sales_Target.objects.filter(Salesman=s,From__year=y).last()
        d = {'salesman':s,'target':target}
        salesmans.append(d)

    if request.method == 'POST':
        salesman = request.POST.getlist('salesmans')
        targets = request.POST.getlist('targets')
        year = request.POST.get('year')

        stryear = str(year)+'-'+'01'+'-'+'01'

        Begindate = datetime.strptime(stryear, "%Y-%m-%d")
        Enddate = Begindate + timedelta(days=365)

        for (s , t) in zip(salesman,targets):
            man = User.objects.get(id=s)
            if s and t:
                try:
                    data = Sales_Target.objects.get(Salesman=s,From__year=year)
                    data.Targets = t
                    data.save()
                except:
                    data = Sales_Target(Salesman=man,Targets=t,From=Begindate,To=Enddate)
                    data.save()
        return redirect('assign-target')
    

    p = Paginator(salesmans,10)
    page = request.GET.get('page')
    salesmans = p.get_page(page)
    nums = 'a' * salesmans.paginator.num_pages

    context = {
        'salesmans' : salesmans,
        'years' : years,
        'y' : y,
        'nums':nums,
    }

    return render(request,'target-setup.html',context)

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def target_view(request,year):
    setTarget()
    salesmans = Sales_Target.objects.filter(From__year = year)
    p = Paginator(salesmans,10)
    page = request.GET.get('page')
    salesmans = p.get_page(page)
    nums = 'a' * salesmans.paginator.num_pages
    return render(request,'target-view.html',{'salesmans':salesmans,'year':year,'nums':nums})

#################################################################################

@csrf_exempt
def get_target_data(request):
    if request.method == 'POST':
        smans = User.objects.filter(is_salesman=True)
        salesmans = []

        year = request.POST.get('year')

        for s in smans:
            target = Sales_Target.objects.filter(Salesman=s,From__year=year).last()
            if target:
                d = {'id':s.id,'salesman':s.first_name,'mobile':s.Mobile,'email':s.email,'target':target.Targets}
            else:
                d = {'id':s.id,'salesman':s.first_name,'mobile':s.Mobile,'email':s.email,'target':0.0}
            salesmans.append(d)
        
        data = list(salesmans)
        salesmans = list(smans)

        # salesmans = Sales_Target.objects.filter(From__year=year).values()
        # data = list(salesmans)
        if data:
            status = 'success'
        else:
            status = 'failed'
        return JsonResponse({'data':data,'status':status,})