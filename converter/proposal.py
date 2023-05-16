from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from administrator.models import Lead,Lead_Schedule,Lead_Update,Attachments,Product,Task,Proposal,Replays,Salesman_Report,Review,Proposal_Items,Sales_Target,Invoice,Receipt,Notification
from u_auth.models import User
from datetime import date as dt
from administrator.views import setip
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from administrator.set_fun import setTarget
import math
from django.db.models import Sum
from administrator.views import setreport
from django.core.paginator import Paginator
from datetime import datetime
from datetime import timedelta

# @login_required
# def list_accepted_proposals(request):
#     return render(request,'')