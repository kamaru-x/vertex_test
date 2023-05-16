from administrator.models import User,Sales_Target,Proposal
from datetime import date
from django.db.models import Q

def setTarget():
    salesmans = User.objects.filter(is_salesman=True)
    d = date.today()
    year = d.year
    for salesman in salesmans:
        archived = 0
        faild = 0
        pending = 0

        r_proposals = Proposal.objects.filter(Lead__Salesman=salesman,Proposal_Status=0,Date__year=year)
        a_proposals = Proposal.objects.filter(Lead__Salesman=salesman,Proposal_Status=1,Date__year=year)
        p_proposals = Proposal.objects.filter(Lead__Salesman=salesman,Proposal_Status=10,Date__year=year)

        for a in a_proposals:
            if a.Grand_Total:
                archived += int(a.PO_Value)

        for r in r_proposals:
            if r.Grand_Total:
                faild += r.Grand_Total

        for p in p_proposals:
            if p.Grand_Total:
                pending += p.Grand_Total

        target = Sales_Target.objects.filter(Salesman=salesman,From__year=year).last()
        if target:
            target.Archived = archived
            target.Failed = faild
            target.Pending = pending
            target.Balance = target.Targets - archived
            target.save()


def set_revisions_count():
    proposals = Proposal.objects.all()

    count = Proposal.objects.all().count()

    for proposal in proposals:

        list_upward = []
        list_backward = []

        i = proposal.Reviced
        u = proposal.id
        
        for y in range(count):
            try:
                upwards = Proposal.objects.filter(Reviced=u)
                for upward in upwards:
                    if upward.Proposal_Status == 15:
                        pass
                    elif upward.Scope or upward.Proposal_Title:
                        list_upward.append(upward)
                    u = upward.id
            except:
                u = 0

        for x in range(count):
            if i != None:
                reviceds = Proposal.objects.filter(id=i)
                for reviced in reviceds:
                    if upward.Proposal_Status == 15:
                        pass
                    elif reviced.Reviced or reviced.Revised_Date:
                        list_backward.append(reviced)
                        i = reviced.Reviced
                    else:
                        break

        proposal.Revisions_Total = len(list_upward) + len(list_backward)
        proposal.save()

        # print('#####################################################################################')

        # print(list_upward)
        # print('total upward : ' ,len(list_upward))

        # print('#####################################################################################')