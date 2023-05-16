
from datetime import date
from administrator.models import Notification

today_date = date.today()

def data(request):
    try:
        notifications = Notification.objects.filter(notification_user=request.user)
    except:
        notifications = 'nothing'
    context = {
        'today':today_date,
        'notifications' : notifications,
    }
    return(context)