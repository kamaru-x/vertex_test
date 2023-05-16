from django.db import models
from u_auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class Category(models.Model):
    # default
    Date = models.DateTimeField(null=True)
    Status = models.IntegerField(default=1)
    AddedBy = models.IntegerField(default=0)
    Ip = models.GenericIPAddressField(null=True)

    Edited_Date = models.DateTimeField(auto_now_add=True)
    EditedBy = models.IntegerField(default=0)
    EditedIp = models.GenericIPAddressField(null=True)

    Name = models.CharField(max_length=50)
    Reference = models.CharField(max_length=20)
    Description = models.TextField()
    Products = models.IntegerField(default=0)

    def __str__(self):
        return self.Name

#################################################################################

class Product(models.Model):
    # default
    Date = models.DateTimeField(null=True)
    Status = models.IntegerField(default=1)
    AddedBy = models.IntegerField(default=0)
    Ip = models.GenericIPAddressField(null=True)

    Edited_Date = models.DateTimeField(auto_now_add=True)
    EditedBy = models.IntegerField(default=0)
    EditedIp = models.GenericIPAddressField(null=True)

    Category = models.ForeignKey(Category,on_delete=models.DO_NOTHING,null=True)
    Name = models.CharField(max_length=50)
    Buying_Price = models.FloatField()
    Selling_Price = models.FloatField(null=True,blank=True)
    Reference = models.CharField(max_length=20)
    Description = models.TextField(null=True)
    Unit = models.CharField(max_length=5,null=True,blank=True)

    def __str__(self):
        return self.Name

#################################################################################

class Lead(models.Model):
    Date = models.DateTimeField(null=True)
    Status = models.IntegerField(default=1)
    AddedBy = models.IntegerField(default=0)
    Ip = models.GenericIPAddressField(null=True)

    Edited_Date = models.DateTimeField(auto_now_add=True)
    EditedBy = models.IntegerField(default=0)
    EditedIp = models.GenericIPAddressField(null=True)

    Reference = models.CharField(max_length=20)
    Company = models.CharField(max_length=50)
    Address = models.CharField(max_length=250)
    Email = models.EmailField()
    Phone = models.CharField(max_length=15)
    ECDate = models.DateField(null=True,blank=True)
    ESValue = models.FloatField()
    State = models.IntegerField()
    CName = models.CharField(max_length=50)
    CNumber = models.CharField(max_length=15)
    CMail = models.EmailField()
    Designation = models.CharField(max_length=50,null=True,blank=True)
    Salesman = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    Lead_Status = models.IntegerField(default=0)

    Upcoming_Meetings = models.IntegerField(default=0)
    Previous_Meetings = models.IntegerField(default=0)

    Rejected_Proposals = models.IntegerField(default=0)
    Accepted_proposals = models.IntegerField(default=0)

    Cancel_Date = models.DateField(null=True)
    Cancel_Reason = models.TextField(null=True,blank=True)
    
    To_Opertunity = models.DateField(null=True)
    To_Proposal = models.DateField(null=True)
    To_Client = models.DateField(null=True)
    To_Project = models.DateField(null=True)
    Reject_Date = models.DateField(null=True)

    def __str__(self):
        return self.Company

#################################################################################

class Attachments(models.Model):
    # Lead_Update = models.ForeignKey(Lead_Update,on_delete=models.SET_NULL,null=True)
    Attachment = models.FileField(upload_to='update-files')
    Name = models.TextField()
    Format = models.TextField()

    def __str__(self):
        return self.Name

#################################################################################

class Lead_Update(models.Model):
    Date = models.DateTimeField()
    Status = models.IntegerField(default=1)
    AddedBy = models.IntegerField(default=0)
    Ip = models.GenericIPAddressField(null=True,blank=True)

    AddedDate = models.DateField(null=True)
    Lead = models.ForeignKey(Lead,on_delete=models.SET_NULL,null=True)
    Description = models.TextField()
    Attachments = models.ManyToManyField(Attachments)

    # def __str__(self):
    #     return self.Lead.Company

#################################################################################

class Lead_Schedule(models.Model):
    Date = models.DateTimeField()
    Status = models.IntegerField(default=1)
    AddedBy = models.IntegerField(default=0)
    Ip = models.GenericIPAddressField(null=True,blank=True)

    Reference = models.CharField(max_length=25,null=True)
    AddedDate = models.DateField(null=True)
    Lead = models.ForeignKey(Lead,on_delete=models.SET_NULL,null=True)
    Mode = models.CharField(max_length=25)
    From = models.TimeField()
    To = models.TimeField()
    Description = models.TextField()
    Schedule_Status = models.IntegerField(default=1)

    Members = models.CharField(max_length=255)
    Update_Description = models.TextField()
    Update_Date = models.DateField(null=True)
    Attachment = models.ManyToManyField(Attachments)

    notification = models.IntegerField(default=1)


    # def __str__(self):
    #     return self.Lead.Company

#################################################################################

class Proposal(models.Model):
    Date = models.DateTimeField()
    Status = models.IntegerField(default=1)
    AddedBy = models.IntegerField(default=0)
    Ip = models.GenericIPAddressField(null=True,blank=True)

    Reviced = models.IntegerField(null=True)
    Revised_Date = models.DateField(null=True)
    revisible = models.BooleanField(default=True)
    Revisions_Total = models.IntegerField(default=0)

    Lead = models.ForeignKey(Lead,on_delete=models.DO_NOTHING)
    Reference = models.CharField(max_length=20)
    # Products = models.ManyToManyField(Product)
    Proposal_Status = models.IntegerField(default=10)

    Proposal_Title = models.CharField(max_length=225,null=True,blank=True)
    Project_Name = models.CharField(max_length=225,null=True,blank=True)
    Proposal_Date = models.DateField(null=True,blank=True)
    Expire_Date = models.DateField(null=True,blank=True)
    Subject = models.CharField(max_length=225,null=True,blank=True)

    Scope = RichTextField(null=True,blank=True)
    Payment = RichTextField(null=True,blank=True)
    Exclusion = RichTextField(null=True,blank=True)
    Terms_Condition = RichTextField(null=True,blank=True)
    Oppertunity = models.TextField(null=True,blank=True)
    Action_Date = models.DateField(null=True)

    PO_Number = models.CharField(max_length=50,null=True)
    PO_Date = models.DateField(null=True)
    PO_Value = models.FloatField(null=True)
    PO_Description = models.TextField(null=True)
    Attachments = models.ManyToManyField(Attachments)

    Grand_Total = models.FloatField(null=True)
    Discount = models.FloatField(null=True)
    Method = models.IntegerField(null=True)
    def __str__(self):
        return self.Reference

#################################################################################

class Section(models.Model):
    Proposal = models.ForeignKey(Proposal,on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    Description = models.TextField()

    def __str__(self):
        return self.Name
    
#################################################################################

class Proposal_Items(models.Model):
    Proposal = models.ForeignKey(Proposal,on_delete=models.CASCADE)
    Section = models.ForeignKey(Section,on_delete=models.CASCADE)
    Product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    Sell_Price = models.FloatField()
    Quantity = models.IntegerField()
    Total = models.FloatField()

    def __str__(self):
        return self.Proposal.Reference

#################################################################################

class Task(models.Model):
    Date = models.DateTimeField()
    Status = models.IntegerField(default=1)
    AddedBy = models.IntegerField(default=0)
    Ip = models.GenericIPAddressField(null=True,blank=True)

    Lead = models.ForeignKey(Lead,on_delete=models.SET_NULL,null=True)
    Salesman = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    Title = models.CharField(max_length=50)
    Priority = models.CharField(max_length=25,null=True)
    Due_Date = models.DateField()
    Description = models.TextField()
    Attachment = models.ManyToManyField(Attachments)
    Task_Status = models.IntegerField(default=0)
    Completed_Date = models.DateField(null=True)

    notification = models.IntegerField(default=1)

    def __str__(self):
        return self.Title

#################################################################################

class Replays(models.Model):
    Date = models.DateTimeField()
    Status = models.IntegerField(default=1)
    AddedBy = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    Ip = models.GenericIPAddressField(null=True,blank=True)

    AddedDate = models.DateField(null=True)
    Task = models.ForeignKey(Task,on_delete=models.DO_NOTHING)
    Message = models.TextField()
    Attachments = models.ManyToManyField(Attachments)

    def __str__(self):
        return self.Message

#################################################################################

class Review(models.Model):
    AddedDate = models.DateField(null=True)
    Task = models.ForeignKey(Task,on_delete=models.DO_NOTHING)
    Message = models.TextField()
    Attachments = models.ManyToManyField(Attachments)

    def __str__(self):
        return self.Message

#################################################################################

class Salesman_Report(models.Model):
    Status = models.IntegerField(default=1)
    Salesman = models.ForeignKey(User,on_delete=models.DO_NOTHING)

    Pending_Tasks = models.IntegerField(default=0)
    Completed_Tasks = models.IntegerField(default=0)

    Lead_Total = models.IntegerField(default=0)
    Lead_Succes = models.IntegerField(default=0)
    Lead_Faild = models.IntegerField(default=0)

    Opportunity_Total = models.IntegerField(default=0)
    Opportunity_Success = models.IntegerField(default=0)
    Opportunity_Faild = models.IntegerField(default=0)

    Proposal_Total = models.IntegerField(default=0)
    Proposal_Success = models.IntegerField(default=0)
    Proposal_Faild = models.IntegerField(default=0)

    SV_Pending = models.FloatField(default=0)
    SV_Success = models.FloatField(default=0)
    SV_Failed = models.FloatField(default=0)

    Upcoming_Meetings = models.IntegerField(default=0)
    Previous_Meetings = models.IntegerField(default=0)

    def __str__(self):
        return self.Salesman.first_name
    
#################################################################################

class Sales_Target(models.Model):
    Salesman = models.ForeignKey(User,on_delete=models.CASCADE)
    From = models.DateField(null=True,blank=True)
    To = models.DateField(null=True,blank=True)
    Targets = models.FloatField(default=0)
    Balance = models.FloatField(default=0)
    Archived = models.FloatField(default=0)
    Pending = models.FloatField(default=0)
    Failed = models.FloatField(default=0)

    def __str__(self):
        return self.Salesman.first_name + '  ///  ' + str(self.From) + '  ///  ' + str(self.To)
    
#################################################################################

class Invoice(models.Model):
    Date = models.DateField()
    Status = models.IntegerField(default=1)
    AddedBy = models.IntegerField(default=0)
    Ip = models.GenericIPAddressField(null=True,blank=True)

    Proposal = models.ForeignKey(Proposal,on_delete=models.DO_NOTHING)
    Reference = models.CharField(max_length=25)
    Amount = models.FloatField()

    def __str__(self):
        return self.Reference
    
#################################################################################

class Receipt(models.Model):
    Date = models.DateField()
    Status = models.IntegerField(default=1)
    AddedBy = models.IntegerField(default=0)
    Ip = models.GenericIPAddressField(null=True,blank=True)

    Proposal = models.ForeignKey(Proposal,on_delete=models.DO_NOTHING)
    Reference = models.CharField(max_length=25)
    Amount = models.FloatField()

    def __str__(self):
        return self.Reference
    
#################################################################################

class Notification(models.Model):
    added_by = models.ForeignKey(User,related_name='added_by',on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    notification_user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='notification_user')
    Message = models.CharField(max_length=225)
    Read_Status = models.BooleanField(default=False)
    Read_Date = models.DateField(null=True)

#################################################################################