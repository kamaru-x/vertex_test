from django.contrib import admin
from administrator.models import Category,Product,Lead,Lead_Update,Lead_Schedule,Attachments,Proposal,Task,Replays,Salesman_Report,Review,Proposal_Items,Sales_Target,Invoice,Receipt,Notification

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Lead)
admin.site.register(Lead_Update)
admin.site.register(Lead_Schedule)
admin.site.register(Attachments)
admin.site.register(Proposal)
admin.site.register(Task)
admin.site.register(Replays)
admin.site.register(Salesman_Report)
admin.site.register(Review)
admin.site.register(Proposal_Items)
admin.site.register(Sales_Target)
admin.site.register(Invoice)
admin.site.register(Receipt)
admin.site.register(Notification)