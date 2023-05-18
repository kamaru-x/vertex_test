from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from administrator.models import Lead,Lead_Schedule,Lead_Update,Attachments,Product,Task,Proposal,Replays,Salesman_Report,Review,Proposal_Items,Sales_Target,Invoice,Receipt,Notification,Category,Section
from u_auth.models import User
from datetime import date as dt
from administrator.views import setip
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse,HttpResponse
from administrator.set_fun import setTarget
import math
from django.db.models import Sum
from administrator.views import setreport
from django.core.paginator import Paginator
from datetime import datetime
from datetime import timedelta
from django.contrib import messages
from django.db.models import Q
from administrator.set_fun import set_revisions_count

# Create your views here.

def set_proposals():
    leads = Lead.objects.filter(Status=1)
    for lead in leads:
        r_proposals = Proposal.objects.filter(Lead=lead).filter(Proposal_Status=0).count()
        a_proposals = Proposal.objects.filter(Lead=lead).filter(Proposal_Status=1).count()
        lead.Rejected_Proposals = r_proposals
        lead.Accepted_proposals = a_proposals
        lead.save()


@login_required
def list_opertunities(request):
    if request.user.is_superuser:
        opertunities = Lead.objects.filter(Lead_Status=1).filter(Status=1).order_by('-id')
    else:
        opertunities = Lead.objects.filter(Salesman=request.user,Lead_Status=1).filter(Status=1).order_by('-id')

    for opportunity in opertunities:
        rejected = Proposal.objects.filter(Lead=opportunity,Proposal_Status=0)
        opportunity.Rejected_Proposals = rejected.count()
        opportunity.save()

    if request.method == 'POST':
        c = request.POST.get('c')
        lead= Lead.objects.get(id=c)
        lead.Status = 2
        lead.Cancel_Date = dt.today()
        lead.Cancel_Reason = request.POST.get('reason')
        lead.save()

        # salesman = lead.Salesman
        # report = Salesman_Report.objects.get(Salesman=salesman)
        # report.Opportunity_Faild = report.Opportunity_Faild + 1
        # report.save()
        return redirect('list-opportunities')
    
    p = Paginator(opertunities,10)
    page = request.GET.get('page')
    opertunities = p.get_page(page)
    nums = 'a' * opertunities.paginator.num_pages
    return render(request,'opportunity-list.html',{'opertunitunities':opertunities,'nums':nums})

#################################################################################

@login_required
def view_opertunity(request,lid):
    set_proposals()
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

        return redirect('/opportunity-view/%s' %lead.id)

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
    return render(request,'opportunity-view.html',context)

#################################################################################

@login_required
def proposal(request,lid):
    products = Product.objects.all()
    lead = Lead.objects.get(id=lid)
    user = request.user.id
    d = dt.today()
    ip = setip(request)
    r = Proposal.objects.last()

    if r:
        refer = f'PROPOSAL-00{r.id+1}'
    else:
        refer = 'PROPOSAL-001'

    proposal = Proposal(Date=d,AddedBy=user,Ip=ip,Lead=lead,Reference=refer)
    proposal.save()

    return redirect('/proposal/%s/' %proposal.id)

#################################################################################

@csrf_exempt
def create_proposal(request,lid):
    products = Product.objects.filter(Status=1)
    categories = Category.objects.all()
    proposal = Proposal.objects.get(id=lid)
    lead = proposal.Lead
    pros = Proposal_Items.objects.filter(Proposal=proposal)
    sections = Section.objects.filter(Proposal=proposal)

    t = 0

    for p in pros:
        t += p.Total

    if request.method == 'POST':
        if request.POST.get('proposal_title'):
            proposal.Proposal_Title = request.POST.get('proposal_title')
            proposal.Project_Name = request.POST.get('project_name')
            proposal.Proposal_Date = request.POST.get('proposal_date')
            proposal.Expire_Date = request.POST.get('expire_date')
            proposal.Subject = request.POST.get('subject')
            proposal.Scope = request.POST.get('scope')
            proposal.Payment = request.POST.get('payment')
            proposal.Exclusion = request.POST.get('exclusion')
            proposal.Terms_Condition = request.POST.get('terms')
            # proposal.Grand_Total = request.POST.get('current_value')
            proposal.save()
            if proposal.Proposal_Title and proposal.Project_Name:
                messages.success(request,'proposal created successfully and added to pending proposals')
                return redirect('/list-proposals/pending/')
            else:
                messages.success(request,'proposal created successfully and added to draft proposals')
                return redirect('/list-proposals/draft/')
        
        if request.POST.get('id'):
            id = request.POST.get('id')
            item = Proposal_Items.objects.get(id=id)
            item.delete()
            return redirect('/proposal/%s' %proposal.id)
        
        if request.POST.get('section_name'):
            section_name = request.POST.get('section_name')
            section_description = request.POST.get('section_description')

            Section.objects.create(Proposal=proposal,Name=section_name,Description=section_description)

            return redirect('.')
        
        if request.POST.get('section_id'):
            section_id = request.POST.get('section_id')
            product_list = request.POST.getlist('checks')
            qty_list = request.POST.getlist('qty')
            price_list = request.POST.getlist('price')
            # print(f'products list = {product_list} | price list = {price_list} | quantity list = {qty_list}')
            section = Section.objects.get(id=section_id)
            for product in product_list:
                pro = Product.objects.get(id=product)
                Proposal_Items.objects.create(Proposal=proposal,Section=section,Product=pro,Sell_Price=pro.Selling_Price,Quantity=1,Total=pro.Selling_Price)
            return redirect('.')

    context = {
        'products' : products,
        'pros' : pros,
        'proposal' : proposal,
        't' : t,
        'categories':categories,
        'sections' : sections,
    }
    return render(request,'proposal.html',context)

#################################################################################

@csrf_exempt
def add_proposal_product(request):
    if request.method == 'POST':
        p = request.POST.get('product')
        pro = Product.objects.get(id=p)
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        total = request.POST.get('total')
        psl = request.POST.get('proposal')
        proposal = Proposal.objects.get(id=psl)
        # proposal.Grand_Total = request.POST.get('grand_total')
        # proposal.save()
        try:
            pr = Proposal_Items.objects.get(Proposal=proposal,Product=pro)
            if pr:
                return redirect('/proposal/%s' %proposal.id)
        except:
            product = Proposal_Items(Proposal=proposal,Product=pro,Quantity=quantity,Sell_Price=price,Total=total)
            product.save()
            products_list = Proposal_Items.objects.filter(Proposal=proposal)

            data_list = []

            for one in products_list:
                data = {'id':one.id,'reference':one.Product.Reference,'name':one.Product.Name,'category':one.Product.Category.Name,'price':one.Sell_Price,'quantity':one.Quantity,'total':one.Total}
                data_list.append(data)

            products = list(data_list)
            return JsonResponse({'status' : 'saved','products':products})

#################################################################################

@csrf_exempt
def add_percentage(request):
    if request.method == 'POST':
        p = request.POST.get('proposal')
        mode = request.POST.get('method')
        discount = request.POST.get('discount')
        grand = request.POST.get('grand')

        proposal = Proposal.objects.get(id=p)
        proposal.Grand_Total = grand
        proposal.Discount = discount
        proposal.Method = mode
        proposal.save()
        return JsonResponse({'status':'percentage changed'})

#################################################################################

@login_required
def list_proposals(request,status):
    leads = Lead.objects.filter(Status=1)
    set_proposals()
    # set_revisions_count()
    if request.user.is_superuser:
        if status == 'accepted':
            proposals = Proposal.objects.filter(Status=1,Proposal_Status=1).order_by('-id')
        elif status == 'pending':
            proposals = []
            proposal = Proposal.objects.filter(Status=1,Proposal_Status=10,Reviced=None).order_by('-id')
            for p in proposal:
                if p.Scope != None:
                    proposals.append(p)
        elif status == 'rejected':
            proposals = Proposal.objects.filter(Status=1,Proposal_Status=0).order_by('-id')
        elif status == 'invalid':
            proposals = Proposal.objects.filter(Status=1,Proposal_Status=404).order_by('-id')
        elif status == 'draft':
            proposals = []
            pros = Proposal.objects.filter(Status=1).order_by('-id')
            proposal = pros.filter(Q(Proposal_Status=10) | Q(Proposal_Status=5))
            for p in proposal:
                if p.Scope == None or p.Proposal_Title == None:
                    proposals.append(p)
                elif p.Proposal_Status == 5:
                    proposals.append(p)
    else:
        if status == 'accepted':
            proposals = Proposal.objects.filter(Status=1,Proposal_Status=1,Lead__Salesman=request.user).order_by('-id')
        elif status == 'pending':
            proposals = []
            proposal = Proposal.objects.filter(Status=1,Proposal_Status=10,Lead__Salesman=request.user,Reviced=None).order_by('-id')
            for p in proposal:
                if p.Scope != None:
                    proposals.append(p)
        elif status == 'rejected':
            proposals = Proposal.objects.filter(Status=1,Proposal_Status=0,Lead__Salesman=request.user).order_by('-id')
        elif status == 'invalid':
            proposals = Proposal.objects.filter(Status=1,Proposal_Status=404,Lead__Salesman=request.user).order_by('-id')
        elif status == 'draft':
            proposals = []
            proposal = Proposal.objects.filter(Status=1,Proposal_Status=10,Lead__Salesman=request.user).order_by('-id')
            for p in proposal:
                if p.Scope == None or p.Proposal_Title == None:
                    proposals.append(p)
                elif p.Proposal_Status == 5:
                    proposals.append(p)

    if request.method == 'POST':
        lid = request.POST.get('lead')
        lead = Lead.objects.get(id=lid)
        user = request.user.id
        d = dt.today()
        ip = setip(request)
        r = Proposal.objects.last()

        if r:
            refer = f'PROPOSAL-00{r.id+1}'
        else:
            refer = 'PROPOSAL-001'

        proposal = Proposal(Date=d,AddedBy=user,Ip=ip,Lead=lead,Reference=refer)
        proposal.save()

        return redirect('/proposal/%s/' %proposal.id)

    p = Paginator(proposals,10)
    page = request.GET.get('page')
    proposals = p.get_page(page)
    nums = 'a' * proposals.paginator.num_pages
    return render(request,'list_proposal.html',{'proposals':proposals,'nums':nums,'status':status,'leads':leads})

#################################################################################

@login_required
def view_proposal(request,pid):
    proposal = Proposal.objects.get(id=pid)

    count = Proposal.objects.all().count()

    total = 0
    dis = 0

    list_backward = []
    list_upward = []

    i = proposal.Reviced
    u = proposal.id

    # while i != None:
    #     per = 0
    #     reviced = Proposal.objects.get(id=i)
    #     if reviced.Scope or reviced.Proposal_Title:
    #         data = {'proposal':reviced}
    #         list_backward.append(data)
    #     if reviced.Reviced:
    #         i = reviced.Reviced
    #     else:
    #         break

    for x in range(count):
        if i != None:
            reviceds = Proposal.objects.filter(id=i)
            for reviced in reviceds:
                # if reviced.Scope or reviced.Proposal_Title:
                    # list_backward.append(reviced)
                if reviced.Reviced or reviced.Revised_Date or reviced.Scope or reviced.Proposal_Title:
                    list_backward.append(reviced)
                    i = reviced.Reviced
                else:
                    break
    
    # while u != 0:
    #     per = 0
        # try:
        #     upward = Proposal.objects.get(Reviced=u)
        #     if upward.Scope or upward.Proposal_Title:
        #         data = {'proposal':upward}
        #         list_upward.append(data)
        #     u = upward.id
        # except:
        #     u = 0

    for y in range(count):
        try:
            upwards = Proposal.objects.filter(Reviced=u)
            for upward in upwards:
                if upward.Scope or upward.Proposal_Title:
                    list_upward.append(upward)
                u = upward.id
        except:
            u = 0
    
    pros = Proposal_Items.objects.filter(Proposal=proposal)

    for p in pros:
        total += p.Total

    if proposal.Method == 1:
        grand_total = (int(total) - int(proposal.Discount))
    elif proposal.Method == 2:
        p = (total*proposal.Discount) / 100
        dis = p
        grand_total = total - p
    else:
        grand_total = total

    if request.method == 'POST':
        attachment = request.FILES.getlist('attachment')

        proposal.PO_Date = request.POST.get('today')
        proposal.PO_Number = request.POST.get('po-number')
        proposal.PO_Value = request.POST.get('po-value')
        proposal.Proposal_Status = 1
        
        i = proposal.Reviced
        u = proposal.id

        while i != None:
            reviced = Proposal.objects.get(id=i)
            reviced.Proposal_Status = 404
            reviced.save()
            if reviced.Reviced:
                i = reviced.Reviced
            else:
                break
        
        while u != 0:
            try:
                upward = Proposal.objects.get(Reviced=u)
                upward.Proposal_Status = 404
                upward.save()
                u = upward.id
            except:
                u = 0

        proposal.save()

        lead = proposal.Lead
        lead.To_Client = dt.today()
        lead.Lead_Status = 2
        lead.save()

        for a in attachment:
            if str(a).endswith(('.png', '.jpg', '.jpeg','.PNG','.JPG','.JPEG')):
                format = 'image'
            else:
                format = 'file'
            attach = Attachments(Attachment=a,Name=a,Format=format)
            attach.save()
            proposal.Attachments.add(attach)
            proposal.save()
        
        # salesman = proposal.Lead.Salesman
        # report = Salesman_Report.objects.get(Salesman=salesman)
        # report.Proposal_Success = report.Proposal_Success + 1
        # report.save()

        return redirect('/view-proposal/%s/' %proposal.id)
    
    context = {
        'proposal' : proposal,
        'pros' : pros,
        'list_backward' : list_backward,
        'list_upward' : list_upward,
        'total' : total,
        'grand_total' : grand_total,
        'dis' : dis
    }
    return render(request,'proposal_view.html',context)

#################################################################################

@login_required
def edit_proposal(request,pid):
    products = Product.objects.all()
    categories = Category.objects.all()
    proposal = Proposal.objects.get(id=pid)
    lead = proposal.Lead
    pros = Proposal_Items.objects.filter(Proposal=proposal)
    sections = Section.objects.filter(Proposal=proposal)

    t = 0
    for p in pros:
        t += p.Total
    
    if request.method == 'POST':            
        if request.POST.get('id'):
            id = request.POST.get('id')
            item = Proposal_Items.objects.get(id=id)
            item.delete()
            return redirect('/edit-proposal/%s' %proposal.id)
        if request.POST.get('scope'):
            proposal.Scope = request.POST.get('scope')
            proposal.Payment = request.POST.get('payment')
            proposal.Exclusion = request.POST.get('exclusion')
            proposal.Terms_Condition = request.POST.get('terms')
            proposal.Grand_Total = request.POST.get('current_value')
            proposal.Proposal_Status = 10
            proposal.Proposal_Title = request.POST.get('proposal_title')
            proposal.Project_Name = request.POST.get('project_name')
            proposal.Proposal_Date = request.POST.get('proposal_date')
            proposal.Expire_Date = request.POST.get('expire_date')
            proposal.Subject = request.POST.get('subject')
            proposal.save()
            messages.success(request,'proposal edited successfully')
            return redirect('/list-proposals/pending/')
        
        if request.POST.get('section_name'):
            section_name = request.POST.get('section_name')
            section_description = request.POST.get('section_description')

            Section.objects.create(Proposal=proposal,Name=section_name,Description=section_description)

            return redirect('.')
        
        if request.POST.get('section_id'):
            section_id = request.POST.get('section_id')
            product_list = request.POST.getlist('checks')
            qty_list = request.POST.getlist('qty')
            price_list = request.POST.getlist('price')
            # print(f'products list = {product_list} | price list = {price_list} | quantity list = {qty_list}')
            section = Section.objects.get(id=section_id)
            for product in product_list:
                pro = Product.objects.get(id=product)
                if pro.Selling_Price:
                    Proposal_Items.objects.create(Proposal=proposal,Section=section,Product=pro,Sell_Price=pro.Selling_Price,Quantity=1,Total=pro.Selling_Price)
                else:
                    Proposal_Items.objects.create(Proposal=proposal,Section=section,Product=pro,Sell_Price=pro.Buying_Price,Quantity=1,Total=pro.Buying_Price)
            return redirect('.')
    context = {
        'products' : products,
        'pros' : pros,
        'proposal' : proposal,
        't' : t,
        'categories':categories,
        'sections' : sections,
    }

    return render(request,'proposal_edit.html',context)

#################################################################################

@login_required
def remove_proposal_product(request,pid,id):
    product = Product.objects.get(id=id)
    proposal = Proposal.objects.get(id=pid)
    lid = proposal.Lead.id
    return redirect('.')

#################################################################################

@login_required
def accept(request,pid):
    proposal = Proposal.objects.get(id=pid)
    proposal.Proposal_Status = 1
    proposal.save()
    lead = proposal.Lead
    lead.To_Client = dt.today()
    setTarget()

    # salesman = proposal.Lead.Salesman
    # report = Salesman_Report.objects.get(Salesman=salesman)
    # report.Proposal_Success = report.Proposal_Success + 1
    # report.save()
    return redirect('/client-view/%s' %lead.id)

#################################################################################

@login_required
def reject(request,pid):
    proposal = Proposal.objects.get(id=pid)
    proposal.Proposal_Status = 0
    proposal.save()

    setTarget()

    i = proposal.Reviced
    u = proposal.id

    while i != None:
        reviced = Proposal.objects.get(id=i)
        reviced.Proposal_Status = 404
        reviced.save()
        if reviced.Reviced:
            i = reviced.Reviced
        else:
            break
    
    while u != 0:
        try:
            upward = Proposal.objects.get(Reviced=u)
            upward.Proposal_Status = 404
            upward.save()
            u = upward.id
        except:
            u = 0

    # salesman = proposal.Lead.Salesman
    # report = Salesman_Report.objects.get(Salesman=salesman)
    # report.Proposal_Faild = report.Proposal_Faild + 1
    # report.save()
    return redirect('/view-proposal/%s' %proposal.id)

#################################################################################

@login_required
def create_task(request):
    user = request.user.id
    d = dt.today()
    ip = setip(request)
    leads = Lead.objects.filter(Status=1)
    salesmans = User.objects.filter(is_salesman=True)
    users = User.objects.all()
    if request.method == 'POST':
        lead = request.POST.get('lead')
        salesman = request.POST.get('salesman')
        title = request.POST.get('title')
        priority = request.POST.get('priority')
        date = request.POST.get('date')
        description = request.POST.get('description')

        try:
            ld = Lead.objects.get(id=lead)
        except:
            return redirect('.')
        
        try:
            sm = User.objects.get(id=salesman)
        except:
            return redirect('.')

        data = Task(Date=d,AddedBy=user,Ip=ip,Lead=ld,Title=title,Priority=priority,Due_Date=date,Description=description,Salesman=sm)
        data.save()

        ls = Task.objects.filter(Lead=ld).filter(AddedBy=user).last()
        attachment = request.FILES.getlist('attach')
        for a in attachment:
            if str(a).endswith(('.png', '.jpg', '.jpeg','.PNG','.JPG','.JPEG')):
                format = 'image'
            else:
                format = 'file'
            attach = Attachments(Attachment=a,Name=a,Format=format)
            attach.save()
            ls.Attachment.add(attach)
            ls.save()

        for salesman in users:
            notification = Notification(added_by=request.user,notification_user=salesman,Message=f'new task added for {sm.first_name}')
            notification.save()

        return redirect('pending-task')

    context = {
        'leads' : leads,
        'salesmans' : salesmans,
    }
    return render(request,'create-task.html',context)

#################################################################################

@login_required
def pending_task(request):
    if request.user.is_superuser:
        tasks = Task.objects.filter(Task_Status=0).filter(Status=1).order_by('Due_Date')
    else:
        tasks = Task.objects.filter(Salesman=request.user,Task_Status=0).filter(Status=1).order_by('Due_Date')

    user = request.user.id
    ip = setip(request)
    d = dt.today()
    if request.method == 'POST' :
        if request.POST.get('taskid'):
            tid = request.POST.get('taskid')
            task = Task.objects.get(id=tid)
            date = request.POST.get('date')
            description = request.POST.get('update-description')
            task.Task_Status = 1
            task.Completed_Date = d
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
            return redirect('pending-task')

        if request.POST.get('id'):
            id = request.POST.get('id')
            task = Task.objects.get(id=id)
            task.Status = 0
            task.save()
            return redirect('pending-task')

    p = Paginator(tasks,10)
    page = request.GET.get('page')
    tasks = p.get_page(page)
    nums = 'a' * tasks.paginator.num_pages        

    context = {
        'tasks' : tasks,
        'nums':nums,
    }
    return render(request,'task-pending.html',context)

#################################################################################

@login_required
def completed_task(request):
    if request.user.is_superuser:
        tasks = Task.objects.filter(Task_Status=1).order_by('-Completed_Date')
    else:
        tasks = Task.objects.filter(Salesman=request.user,Task_Status=1).order_by('-Completed_Date')

    p = Paginator(tasks,1)
    page = request.GET.get('page')
    tasks = p.get_page(page)
    nums = 'a' * tasks.paginator.num_pages
    return render(request,'task-completed.html',{'tasks':tasks,'nums':nums})

#################################################################################

@login_required
def edit_task(request,tid):
    task = Task.objects.get(id=tid)
    leads = Lead.objects.all()
    salesmans = User.objects.filter(is_salesman=True)
    user = request.user.id
    if request.method == 'POST':
        lead = request.POST.get('lead')
        salesman = request.POST.get('salesman')
        ld = Lead.objects.get(id=lead)
        sm = User.objects.get(id=salesman)

        task.Lead = ld
        task.Salesman = sm
        task.Title = request.POST.get('title')
        task.Priority = request.POST.get('priority')
        task.Due_Date = request.POST.get('date')
        task.Description = request.POST.get('description')
        task.save()

        ls = Task.objects.filter(Lead=ld).filter(AddedBy=user).last()
        attachment = request.FILES.getlist('attach')
        for a in attachment:
            if str(a).endswith(('.png', '.jpg', '.jpeg','.PNG','.JPG','.JPEG')):
                format = 'image'
            else:
                format = 'file'
            attach = Attachments(Attachment=a,Name=a,Format=format)
            attach.save()
            ls.Attachment.add(attach)
            ls.save()
        return redirect('pending-task')
    context = {
        'leads' : leads,
        'task' : task,
        'salesmans' : salesmans,
    }
    return render(request,'task-edit.html',context)

#################################################################################

@login_required
def view_pending_task(request,tid):
    user = request.user
    d = dt.today()
    ip = setip(request)
    task = Task.objects.get(id=tid)
    replayes = Replays.objects.filter(Task=task)
    top = Replays.objects.filter(Task=task).first()

    if request.POST.get('date'):
        date = request.POST.get('date')
        description = request.POST.get('update-description')

        data = Replays(Date=d,AddedBy=user,Ip=ip,Task=task,Message=description,AddedDate=date)
        data.save()

        ld = Replays.objects.filter(Task=task).filter(AddedBy=user).last()
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
        return redirect('.')

    context = {
        'task' : task,
        'replayes' : replayes,
        'top' : top,
    }

    return render(request,'view-task-pending.html',context)

#################################################################################

@login_required
def view_completed_task(request,tid):
    task = Task.objects.get(id=tid)
    replayes = Replays.objects.filter(Task=task)
    top = Replays.objects.filter(Task=task).first()
    review = Review.objects.get(Task=task)
    context = {
        'task' : task,
        'replayes' : replayes,
        'review' : review,
        'top' : top,
    }
    return render(request,'view-task-completed.html',context)

#################################################################################

@login_required
def client_list(request):
    set_proposals()
    if request.user.is_superuser:
        clients = Lead.objects.filter(Lead_Status=2).filter(Status=1).order_by('-id')
    else:
        clients = Lead.objects.filter(Salesman=request.user,Lead_Status=2).filter(Status=1).order_by('-id')

    if request.method == 'POST':
        c = request.POST.get('c')
        lead= Lead.objects.get(id=c)
        lead.Status = 3
        lead.Cancel_Date = dt.today()
        lead.Cancel_Reason = request.POST.get('reason')
        lead.save()
        return redirect('clients')
    p = Paginator(clients,10)
    page = request.GET.get('page')
    clients = p.get_page(page)
    nums = 'a' * clients.paginator.num_pages
    return render(request,'clients.html',{'clients':clients,'nums':nums})

#################################################################################

@login_required
def client_view(request,cid):
    lead = Lead.objects.get(id=cid)
    user = request.user.id
    d = dt.today()
    ip = setip(request)
    lead_update = Lead_Update.objects.filter(Lead=lead)
    proposals = Proposal.objects.filter(Lead=lead)
    # attachments = Attachments.objects.all()
    count = Proposal.objects.filter(Lead=lead).count()

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

        return redirect('/client-view/%s' %lead.id)

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
        'proposals' : proposals,
        'count' : count,
    }
    return render(request,'clients-view.html',context)

#################################################################################

@login_required
def projects(request):
    # projects = Lead.objects.filter(Lead_Status=3).filter(Status=1).order_by('-id')
    if request.user.is_superuser:
        projects = Proposal.objects.filter(Proposal_Status=1).order_by('-id')
    else:
        projects = Proposal.objects.filter(Lead__Salesman=request.user,Proposal_Status=1).order_by('-id')
    # if request.method == 'POST':
    #     c = request.POST.get('c')
    #     lead= Lead.objects.get(id=c)
    #     lead.Status = 3
    #     lead.Cancel_Date = dt.today()
    #     lead.Cancel_Reason = request.POST.get('reason')
    #     lead.save()
    #     return redirect('projects')
    p = Paginator(projects,10)
    page = request.GET.get('page')
    projects = p.get_page(page)
    nums = 'a' * projects.paginator.num_pages
    return render(request,'projects-list.html',{'projects':projects,'nums':nums})

#################################################################################

@login_required
def view_project(request,pid):
    lead = Proposal.objects.filter(id=pid).last()
    user = request.user.id
    d = dt.today()
    ip = setip(request)
    lead_update = Lead_Update.objects.filter(Lead=lead.Lead)
    proposal = Proposal.objects.get(id=pid)

    invoices = Invoice.objects.filter(Proposal=proposal)
    receipts = Receipt.objects.filter(Proposal=proposal)

    invoice_totals = invoices.aggregate(sum=Sum('Amount'))
    receipt_totals = receipts.aggregate(sum=Sum('Amount'))

    products = Proposal_Items.objects.filter(Proposal=proposal)
    catagories = []
    for product in products:
        catagories.append(product.Product.Category.Name)
        catagories = [*set(catagories)]

    ir = Invoice.objects.last()

    if ir:
        irefer = f'INVOICE-00{ir.id+1}'
    else:
        irefer = 'INVOICE-001'

    rr = Receipt.objects.last()

    if rr:
        rrefer = f'RECEIPT-00{rr.id+1}'
    else:
        rrefer = 'RECEIPT-001'

    if request.method == 'POST':
        if request.POST.get('invoice'):
            date = request.POST.get('i-date')
            refer = request.POST.get('irefer')
            amount = request.POST.get('i-amount')

            data = Invoice(Date=date,AddedBy=user,Ip=ip,Proposal=proposal,Reference=refer,Amount=amount)
            data.save()
            return redirect ('.')
        
        if request.POST.get('receipt'):
            date = request.POST.get('r-date')
            refer = request.POST.get('rrefer')
            amount = request.POST.get('r-amount')

            data = Receipt(Date=date,AddedBy=user,Ip=ip,Proposal=proposal,Reference=refer,Amount=amount)
            data.save()
            return redirect ('.')
        
    context = {
        'lead' : lead,
        'lead_update' : lead_update,
        # 'attachments' : attachments,
        # 'previous' : previous,
        # 'upcoming' : upcoming,
        'proposal' : proposal,
        'catagories' : catagories,
        'products' : products,
        'irefer' : irefer,
        'rrefer' : rrefer,
        'invoices' : invoices,
        'receipts' : receipts,
        'invoice_totals' : invoice_totals,
        'receipt_totals' : receipt_totals,
    }
    return render(request,'project-view.html',context)

#################################################################################

@login_required
def upcoming_meetings(request):
    if request.user.is_superuser:
        schedules = Lead_Schedule.objects.filter(Status=1).order_by('AddedDate')
    else:
        schedules = Lead_Schedule.objects.filter(Lead__Salesman=request.user,Status=1).order_by('AddedDate')

    user = request.user.id
    d = dt.today()
    ip = setip(request)
    leads = Lead.objects.filter(Status=1)
    users = User.objects.all()

    if request.method == 'POST':
        if request.POST.get('date'):
            date = request.POST.get('date')
            mode = request.POST.get('mode')
            ftime = request.POST.get('from')
            to = request.POST.get('to')
            description = request.POST.get('description')
            l = request.POST.get('lead')
            lead = Lead.objects.get(id=l)

            data = Lead_Schedule(Date=d,AddedBy=user,Ip=ip,Lead=lead,Mode=mode,From=ftime,To=to,Description=description,AddedDate=date)
            data.save()

            for salesman in users:
                notification = Notification(added_by=request.user,notification_user=salesman,Message=f'new meeting scheduled on {date} from {ftime} to {to}')
                notification.save()
            return redirect('.')

        if request.POST.get('id'):
            id = request.POST.get('id')
            meeting = Lead_Schedule.objects.get(id=id)
            meeting.Status = 0
            meeting.save()
            return redirect('upcoming-meetings')

    previous = []
    upcoming = []

    for schedule in schedules:
        if schedule.AddedDate < dt.today() :
            previous.append(schedule)
        elif schedule.AddedDate >= dt.today() :
            upcoming.append(schedule)

    p = Paginator(upcoming,1)
    page = request.GET.get('page')
    upcoming = p.get_page(page)
    nums = 'a' * upcoming.paginator.num_pages
    return render(request,'meeting-upcoming.html',{'upcoming':upcoming,'leads':leads,'nums':nums})

#################################################################################

@login_required
def edit_upcoming_meeting(request,id):
    meeting = Lead_Schedule.objects.get(id=id)
    leads = Lead.objects.filter(Status=1)

    if request.method == 'POST':
        meeting.AddedDate = request.POST.get('date')
        meeting.Mode = request.POST.get('mode')
        meeting.From = request.POST.get('from')
        meeting.To = request.POST.get('to')
        meeting.Description = request.POST.get('description')
        l = request.POST.get('lead')
        meeting.Lead = Lead.objects.get(id=l)
        meeting.save()
        return redirect('upcoming-meetings')

    context = {
        'meeting':meeting,
        'leads':leads,
    }
    return render(request,'meeting-upcoming-edit.html',context)

#################################################################################

@login_required
def previous_meetings(request):
    if request.user.is_superuser:
        schedules = Lead_Schedule.objects.all().order_by('-AddedDate')
    else:
        schedules = Lead_Schedule.objects.filter(Lead__Salesman=request.user).order_by('-AddedDate')

    user = request.user.id
    d = dt.today()
    ip = setip(request)
    leads = Lead.objects.filter(Status=1)
    users = User.objects.all()

    if request.method == 'POST':
        if request.POST.get('date'):
            date = request.POST.get('date')
            mode = request.POST.get('mode')
            ftime = request.POST.get('from')
            to = request.POST.get('to')
            description = request.POST.get('description')
            l = request.POST.get('lead')
            lead = Lead.objects.get(id=l)

            data = Lead_Schedule(Date=d,AddedBy=user,Ip=ip,Lead=lead,Mode=mode,From=ftime,To=to,Description=description,AddedDate=date)
            data.save()

            for salesman in users:
                notification = Notification(added_by=request.user,notification_user=salesman,Message=f'new meeting scheduled on {date} from {ftime} to {to}')
                notification.save()
            return redirect('.')
            
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

            return redirect('/previous-meeting-details/%s' %meeting.id)
        

    previous = []
    upcoming = []

    for schedule in schedules:
        if schedule.AddedDate < dt.today() :
            previous.append(schedule)
        elif schedule.AddedDate > dt.today() :
            upcoming.append(schedule)

    p = Paginator(previous,10)
    page = request.GET.get('page')
    previous = p.get_page(page)
    nums = 'a' * previous.paginator.num_pages 

    return render(request,'meeting-previous.html',{'previous':previous,'leads':leads,'nums':nums})

#################################################################################

@login_required
def meeting_staff_list(request):
    setreport()
    salesmans = User.objects.filter(is_salesman=True)
    reports = Salesman_Report.objects.filter(Status=1)
    p = Paginator(reports,10)
    page = request.GET.get('page')
    reports = p.get_page(page)
    nums = 'a' * reports.paginator.num_pages
    return render(request,'meeting-staff.html',{'salesmans':salesmans,'reports':reports,'nums':nums})

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def meeting_staff_view(request,uid):
    salesman = User.objects.get(id=uid)
    schedules = Lead_Schedule.objects.filter(Lead__Salesman=salesman)
    previous = []
    upcoming = []

    for schedule in schedules:
        if schedule.AddedDate < dt.today() :
            previous.append(schedule)
        elif schedule.AddedDate >= dt.today() :
            upcoming.append(schedule)
    context = {
        'salesman':salesman,
        'previous' : previous,
        'upcoming' : upcoming,
    }
    return render(request,'meeting-staff-view.html',context)

#################################################################################


@login_required
def previous_meeting_details(request,mid):
    meeting = Lead_Schedule.objects.get(id=mid)
    return render(request,'meeting-previous-details.html',{'meeting':meeting})

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def task_staff(request):
    setreport()
    salesmans = User.objects.filter(is_salesman=True)
    reports = Salesman_Report.objects.filter(Status=1)
    p = Paginator(reports,10)
    page = request.GET.get('page')
    reports = p.get_page(page)
    nums = 'a' * reports.paginator.num_pages
    return render(request,'task-staff.html',{'salesmans':salesmans,'reports':reports,'nums':nums})

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def task_staff_view(request,uid):
    salesman = User.objects.get(id=uid)
    pending = Task.objects.filter(Salesman = salesman).filter(Task_Status=0)
    completed = Task.objects.filter(Salesman = salesman).filter(Task_Status=1)

    if request.method == "POST" :
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
        return redirect('/task-staff/%s' %salesman.id)
    
    context = {
        'salesman' : salesman,
        'pending' : pending,
        'completed' : completed,
    }

    return render(request,'task-staff-view.html',context)

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def salesman_report(request):
    reports = []
    salesmans = User.objects.filter(is_salesman=True)
    for salesman in salesmans:
        leads = Lead.objects.filter(Salesman=salesman).count()
        total_proposals = Proposal.objects.filter(Lead__Salesman=salesman)
        accepteted_proposals = Proposal.objects.filter(Lead__Salesman=salesman,Proposal_Status=1)
        rejected_proposals = Proposal.objects.filter(Lead__Salesman=salesman,Proposal_Status=0)

        sum_total_proposals = 0
        sum_accepteted_proposals = 0
        sum_rejected_proposals = 0

        for p in total_proposals:
            if p.Grand_Total:
                sum_total_proposals += p.Grand_Total

        for a in accepteted_proposals:
            if a.PO_Value:
                sum_accepteted_proposals += a.PO_Value
        
        for r in rejected_proposals:
            if r.Grand_Total:
                sum_rejected_proposals += r.Grand_Total

        report = {
            'salesman':salesman,
            'leads':leads,
            'total':total_proposals.count(),
            'accepteted_proposals':accepteted_proposals.count(),
            'rejected_proposals':rejected_proposals.count(),
            'sum_total_proposals':sum_total_proposals,
            'sum_accepteted_proposals':sum_accepteted_proposals,
            'sum_rejected_proposals':sum_rejected_proposals,
            }
        reports.append(report)
    p = Paginator(reports,10)
    page = request.GET.get('page')
    reports = p.get_page(page)
    nums = 'a' * reports.paginator.num_pages
    return render(request,'salesman-report.html',{'reports':reports,'nums':nums})

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def salestarget(request):
    setTarget()
    target = 0
    archived = 0
    balance = 0
    d = dt.today()
    year = d.year
    targets = Sales_Target.objects.filter(From__year=year)
    for t in targets:
        target += t.Targets
        archived += t.Archived
        balance = target - archived
    context = {
        'target' : target,
        'archived' : archived,
        'balance' : balance,
    }
    return render(request,'salestarget-report.html',context)

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def target_report(request):
    salesmans = User.objects.filter(is_salesman = True)
    d = dt.today()
    y = d.year

    trgts = Sales_Target.objects.filter(From__year=y)
    targets = []
    setTarget()

    for t in trgts:

        if t.Targets and t.Archived != 0:
            p = (t.Archived / t.Targets) * 100
            percentage = math.trunc(p)
            if percentage > 100:
                percentage = 100
        else :
            percentage = 0

        target = {'Salesman':t.Salesman,'Targets':t.Targets,'Archived':t.Archived,'Pending':t.Balance,'Percentage':percentage}
        targets.append(target)
    
    p = Paginator(targets,10)
    page = request.GET.get('page')
    targets = p.get_page(page)
    nums = 'a' * targets.paginator.num_pages

    context = {
        'targets' : targets,
        'nums':nums,
    }

    return render(request,'target-report.html',context)

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def top_customers(request):
    lds = Lead.objects.filter(Status=1,Lead_Status=2).order_by('-id')
    leads = []
    for lead in lds:
        volume = 0
        total_volume = 0
        proposals =  Proposal.objects.filter(Proposal_Status=1)
        a_proposals = Proposal.objects.filter(Lead=lead,Proposal_Status=1)
        pro = Proposal.objects.filter(Lead=lead).count()

        for p in proposals:
            total_volume += p.PO_Value

        for a in a_proposals:
            volume += a.PO_Value

        if volume and total_volume != 0:
            p = volume / total_volume * 100
            percentage = math.trunc(p)
        else:
            percentage = 0

        company = {
            'Company':lead.Company,'Email':lead.Email,
            'Mobile':lead.Phone,'Reference':lead.Reference,
            'Salesman':lead.Salesman.first_name,'semail':lead.Salesman.email,
            'smobile':lead.Salesman.Mobile,#'proposals':lead.Accepted_proposals+lead.Rejected_Proposals,
            'proposals':pro,
            'volume':volume,'Percentage':percentage
            }
        leads.append(company)

    p = Paginator(leads,10)
    page = request.GET.get('page')
    leads = p.get_page(page)
    nums = 'a' * leads.paginator.num_pages
    return render(request,'top-customers.html',{'leads':leads,'nums':nums})

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def proposal_report(request):
    total = Proposal.objects.filter(Proposal_Status = 10).count()
    faild = Proposal.objects.filter(Proposal_Status = 0).count()
    success = Proposal.objects.filter(Proposal_Status = 1).count()

    proposals = Proposal.objects.all()

    total_value = 0
    failed_value = 0
    success_value = 0

    for proposal in proposals:
        if proposal.Proposal_Status == 10:
            if proposal.Grand_Total:
                total_value += proposal.Grand_Total

        if proposal.Proposal_Status == 1:
            if proposal.PO_Value:
                success_value += proposal.PO_Value

        if proposal.Proposal_Status == 0:
            if proposal.Grand_Total:
                failed_value += proposal.Grand_Total

    context = {
        'total' : total,
        'faild' : faild,
        'success' : success,
        'total_value' : total_value,
        'failed_value' : failed_value,
        'success_value' : success_value,
    }

    return render(request,'report-proposal.html',context)

#################################################################################

@user_passes_test(lambda u: u.is_superuser)
def total_propose(request):
    proposals = Proposal.objects.filter(Status=1).order_by('-id')
    p = Paginator(proposals,10)
    page = request.GET.get('page')
    proposals = p.get_page(page)
    nums = 'a' * proposals.paginator.num_pages
    return render(request,'report-proposal-total.html',{'proposals':proposals,'nums':nums})

#################################################################################

@csrf_exempt
def get_product(request):
    data = '<option value="">Select Product</option>'
    if request.method == 'POST':
        id = request.POST.get('cat')
        print(id)
        c = Category.objects.get(id=id)
        products = Product.objects.filter(Category=c)
        for product in products:
            data += '<option value="%s">%s(%s)</option>' % (product.id,product.Name,product.Description)
        # data = {id:'1','product':'product1'}
        return HttpResponse (data)

@csrf_exempt
def get_product_data(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        pro = Product.objects.get(id=id)

        product = {'id':pro.id,'price':pro.Buying_Price,'sprice':pro.Selling_Price}
        return JsonResponse(product)

#################################################################################

@login_required
def print_proposal(request,pid):
    proposal = Proposal.objects.get(id=pid)
    products = Proposal_Items.objects.filter(Proposal=proposal)
    date = dt.today()

    Begindate = datetime.strptime(str(date), "%Y-%m-%d")
    Enddate = Begindate + timedelta(days=30)

    summery = []
    catagories = []

    total = 0

    for product in products:
        catagories.append(product.Product.Category.Name)
        catagories = [*set(catagories)]

    for c in catagories:
        grand_total = 0
        for p in products:
            if p.Product.Category.Name == c :
                grand_total += p.Total
                category = Category.objects.get(Name=c)
        cat = {'category':category,'grand':grand_total}
        total += cat['grand']
        summery.append(cat)

    if total and proposal.Discount:
        if proposal.Method == 1:
            grand = (int(total) - int(proposal.Discount))
        elif proposal.Method == 2:
            p = (total*proposal.Discount) / 100
            grand = total - p
    else:
        grand = total

    table = ''
    category_index = 1

    for c in catagories:
        table += f'''<tr>
                        <td></td>
                        <td></td>
                        <td class="desc" colspan="2" style="color:red; text-align: center;"><b>{c}</b></td>
                        <td class="small"></td>
                        <td class="small"></td>
                        <td class="small"></td>
                        <td class="small"></td>
                    </tr>'''
        product_index = 1

        for product in products:
            if product.Product.Category.Name == c :
                table += f'''<tr>
                                <td>{category_index}.{ product_index }</td>
                                <td class="small">{ product.Product.Name }</td>
                                <td class="desc" colspan="2">{ product.Product.Description }</td>
                                <td class="small">{ product.Product.Unit }</td>
                                <td class="small">{ product.Quantity }</td>
                                <td class="small">{ product.Sell_Price }</td>
                                <td class="small">{ product.Total }</td>
                            </tr>'''
                product_index += 1
        category_index += 1

    context = {
        'proposal':proposal,
        'catagories':catagories,
        'products':products,
        'date':date,
        'Enddate':Enddate,
        'summery':summery,
        'total' : total,
        'grand' : grand,
        'p' : p,
        'table':table 
    }
    return render(request,'print-proposal.html',context)

@login_required
def print_proposal_boq(request,pid):
    proposal = Proposal.objects.get(id=pid)
    products = Proposal_Items.objects.filter(Proposal=proposal)
    date = dt.today()

    Begindate = datetime.strptime(str(date), "%Y-%m-%d")
    Enddate = Begindate + timedelta(days=30)

    summery = []
    catagories = []

    total = 0

    for product in products:
        catagories.append(product.Product.Category.Name)
        catagories = [*set(catagories)]

    for c in catagories:
        grand_total = 0
        for p in products:
            if p.Product.Category.Name == c :
                grand_total += p.Total
        cat = {'category':c,'grand':grand_total}
        total += cat['grand']
        summery.append(cat)

    if total and proposal.Discount:
        if proposal.Method == 1:
            grand = (int(total) - int(proposal.Discount))
        elif proposal.Method == 2:
            p = (total*proposal.Discount) / 100
            grand = total - p
    else:
        grand = total

    table = ''
    category_index = 1

    for c in catagories:
        table += f'''<tr>
                        <td></td>
                        <td></td>
                        <td class="desc" colspan="2" style="color:red; text-align: center;"><b>{c}</b></td>
                        <td class="small"></td>
                        <td class="small"></td>
                        <td class="small"></td>
                        <td class="small"></td>
                    </tr>'''
        product_index = 1

        for product in products:
            if product.Product.Category.Name == c :
                table += f'''<tr>
                                <td>{category_index}.{ product_index }</td>
                                <td class="small">{ product.Product.Name }</td>
                                <td class="desc" colspan="2">{ product.Product.Description }</td>
                                <td class="small">{ product.Product.Unit }</td>
                                <td class="small">{ product.Quantity }</td>
                                <td class="small">{ product.Sell_Price }</td>
                                <td class="small">{ product.Total }</td>
                            </tr>'''
                product_index += 1
        category_index += 1

    context = {
        'proposal':proposal,
        'catagories':catagories,
        'products':products,
        'date':date,
        'Enddate':Enddate,
        'summery':summery,
        'total' : total,
        'grand' : grand,
        'p' : p, 
        'table' : table
    }
    return render(request,'print-proposal-boq.html',context)

@login_required
def print_proposal_noboq(request,pid):
    proposal = Proposal.objects.get(id=pid)
    products = Proposal_Items.objects.filter(Proposal=proposal)
    date = dt.today()

    Begindate = datetime.strptime(str(date), "%Y-%m-%d")
    Enddate = Begindate + timedelta(days=30)

    summery = []
    catagories = []

    total = 0

    for product in products:
        catagories.append(product.Product.Category.Name)
        catagories = [*set(catagories)]

    for c in catagories:
        grand_total = 0
        for p in products:
            if p.Product.Category.Name == c :
                grand_total += p.Total
                category = Category.objects.get(Name=c)
        cat = {'category':category,'grand':grand_total}
        total += cat['grand']
        summery.append(cat)

    if total and proposal.Discount:
        if proposal.Method == 1:
            grand = (int(total) - int(proposal.Discount))
        elif proposal.Method == 2:
            p = (total*proposal.Discount) / 100
            grand = total - p
    else:
        grand = total

    context = {
        'proposal':proposal,
        'catagories':catagories,
        'products':products,
        'date':date,
        'Enddate':Enddate,
        'summery':summery,
        'total' : total,
        'grand' : grand,
        'p' : p, 
    }
    return render(request,'print-proposal-noboq.html',context)

@login_required
def print_proposal_noprice(request,pid):
    proposal = Proposal.objects.get(id=pid)
    products = Proposal_Items.objects.filter(Proposal=proposal)
    date = dt.today()

    Begindate = datetime.strptime(str(date), "%Y-%m-%d")
    Enddate = Begindate + timedelta(days=30)

    summery = []
    catagories = []

    total = 0

    for product in products:
        catagories.append(product.Product.Category.Name)
        catagories = [*set(catagories)]

    for c in catagories:
        grand_total = 0
        for p in products:
            if p.Product.Category.Name == c :
                grand_total += p.Total
                category = Category.objects.get(Name=c)
        cat = {'category':category,'grand':grand_total}
        total += cat['grand']
        summery.append(cat)

    if total and proposal.Discount:
        if proposal.Method == 1:
            grand = (int(total) - int(proposal.Discount))
        elif proposal.Method == 2:
            p = (total*proposal.Discount) / 100
            grand = total - p
    else:
        grand = total

    table = ''
    category_index = 1

    for c in catagories:
        table += f'''<tr>
                        <td></td>
                        <td></td>
                        <td class="desc" colspan="2" style="color:red; text-align: center;"><b>{c}</b></td>
                        <td class="small"></td>
                        <td class="small"></td>
                    </tr>'''
        product_index = 1

        for product in products:
            if product.Product.Category.Name == c :
                table += f'''<tr>
                                <td>{category_index}.{ product_index }</td>
                                <td class="small">{ product.Product.Name }</td>
                                <td class="desc" colspan="2">{ product.Product.Description }</td>
                                <td class="small">{ product.Product.Unit }</td>
                                <td class="small">{ product.Quantity }</td>
                            </tr>'''
                product_index += 1
        category_index += 1

    context = {
        'proposal':proposal,
        'catagories':catagories,
        'products':products,
        'date':date,
        'Enddate':Enddate,
        'summery':summery,
        'total' : total,
        'grand' : grand,
        'p' : p, 
        'table':table
    }
    return render(request,'print-proposal-noprice.html',context)

####################################################################################################

def revise_proposal(request,id):
    proposal = Proposal.objects.get(id=id)
    proposal.Revised_Date = dt.today()
    # proposal.revisible = False
    proposal.save()
    lead = Lead.objects.get(id=proposal.Lead.id)
    user = request.user.id
    d = dt.today()
    ip = setip(request)
    r = Proposal.objects.last()

    if r:
        refer = f'PROPOSAL-00{r.id+1}'
    else:
        refer = 'PROPOSAL-001'

    p = Proposal(Date=d,AddedBy=user,Ip=ip,Lead=lead,Reference=refer,Proposal_Title=proposal.Proposal_Title,
                Project_Name=proposal.Project_Name,Proposal_Date=proposal.Proposal_Date,Expire_Date=proposal.Expire_Date,
                Subject=proposal.Subject,Scope=proposal.Scope,Payment=proposal.Payment,Exclusion=proposal.Exclusion,
                Terms_Condition=proposal.Terms_Condition,Oppertunity=proposal.Oppertunity,PO_Number=proposal.PO_Number,
                PO_Date=proposal.PO_Date,PO_Value=proposal.PO_Value,PO_Description=proposal.PO_Description,
                Grand_Total=proposal.Grand_Total,Discount=proposal.Discount,Method=proposal.Method,Reviced=id,Proposal_Status=15)
    p.save()
    pro = Proposal.objects.get(id=p.Reviced)

    Items = Proposal_Items.objects.filter(Proposal=pro)
    for item in Items:
        data = Proposal_Items(Proposal=p,Product=item.Product,Sell_Price=item.Sell_Price,Quantity=item.Quantity,Total=item.Total)
        data.save()

    return redirect('/reviced/%s/' %p.id)

#########################################################################################################

@login_required
def reviced_proposal(request,lid):
    products = Product.objects.all()
    proposal = Proposal.objects.get(id=lid)
    list_reviced = []

    i = proposal.Reviced
    base_proposal = Proposal.objects.get(id=i)

    print('base proposal number : ' , i)
    print('base proposal reference : ', base_proposal.Reference)


    while i != None:
        reviced = Proposal.objects.get(id=i)
        # sum = reviced.Grand_Total - reviced.Discount
        data = {'proposal':reviced}
        list_reviced.append(data)
        if reviced.Reviced:
            i = reviced.Reviced
        else:
            break


    lead = proposal.Lead
    pros = Proposal_Items.objects.filter(Proposal=proposal)

    t = 0

    for p in pros:
        t += p.Total

    
    if request.method == 'POST':            
        if request.POST.get('id'):
            id = request.POST.get('id')
            item = Proposal_Items.objects.get(id=id)
            item.delete()
            return redirect('/reviced/%s' %proposal.id)
        if request.POST.get('scope'):
            proposal.Scope = request.POST.get('scope')
            proposal.Payment = request.POST.get('payment')
            proposal.Exclusion = request.POST.get('exclusion')
            proposal.Terms_Condition = request.POST.get('terms')
            proposal.Grand_Total = request.POST.get('current_value')
            proposal.Proposal_Status = 10
            base_proposal.revisible = 0
            base_proposal.save()
            proposal.save()
            messages.success(request,'new proposal revised')
            return redirect('/list-proposals/pending/')
        if request.POST.get('proposal_title'):
            proposal.Proposal_Title = request.POST.get('proposal_title')
            proposal.Project_Name = request.POST.get('project_name')
            proposal.Proposal_Date = request.POST.get('proposal_date')
            proposal.Expire_Date = request.POST.get('expire_date')
            proposal.Subject = request.POST.get('subject')
            proposal.Proposal_Status = 5
            base_proposal.revisible = 0
            base_proposal.save()
            proposal.save()
            messages.success(request,'details added to proposal')
            return redirect('/reviced/%s' %proposal.id)

    context = {
        'products' : products,
        'pros' : pros,
        'proposal' : proposal,
        'recived' : reviced,
        'list_reviced' : list_reviced,
        't' : t
    }

    return render(request,'revice.html',context)

########################################################################################################

@csrf_exempt
def save_product(request):
    if request.method == 'POST':
        p = request.POST.get('proposal')
        proposal = Proposal.objects.get(id=p)
        proposal_item = request.POST.get('proposal_item')
        pi = Proposal_Items.objects.get(id=proposal_item)
        pi.Sell_Price = request.POST.get('sell_price')
        pi.Quantity = request.POST.get('quantity')
        pi.Total = request.POST.get('total')
        pi.save()

        pros = Proposal_Items.objects.filter(Proposal=proposal)

        t = 0

        for p in pros:
            t += p.Total
        
        return JsonResponse({'status':'data updated','total':t})