# Generated by Django 4.1.1 on 2023-04-11 11:46

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Attachments",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Attachment", models.FileField(upload_to="update-files")),
                ("Name", models.TextField()),
                ("Format", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Date", models.DateTimeField(null=True)),
                ("Status", models.IntegerField(default=1)),
                ("AddedBy", models.IntegerField(default=0)),
                ("Ip", models.GenericIPAddressField(null=True)),
                ("Edited_Date", models.DateTimeField(auto_now_add=True)),
                ("EditedBy", models.IntegerField(default=0)),
                ("EditedIp", models.GenericIPAddressField(null=True)),
                ("Name", models.CharField(max_length=50)),
                ("Reference", models.CharField(max_length=20)),
                ("Products", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Lead",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Date", models.DateTimeField(null=True)),
                ("Status", models.IntegerField(default=1)),
                ("AddedBy", models.IntegerField(default=0)),
                ("Ip", models.GenericIPAddressField(null=True)),
                ("Edited_Date", models.DateTimeField(auto_now_add=True)),
                ("EditedBy", models.IntegerField(default=0)),
                ("EditedIp", models.GenericIPAddressField(null=True)),
                ("Reference", models.CharField(max_length=20)),
                ("Company", models.CharField(max_length=50)),
                ("Address", models.CharField(max_length=250)),
                ("Email", models.EmailField(max_length=254)),
                ("Phone", models.CharField(max_length=15)),
                ("ECDate", models.DateField(blank=True, null=True)),
                ("ESValue", models.FloatField()),
                ("State", models.IntegerField()),
                ("CName", models.CharField(max_length=50)),
                ("CNumber", models.CharField(max_length=15)),
                ("CMail", models.EmailField(max_length=254)),
                ("Designation", models.CharField(blank=True, max_length=50, null=True)),
                ("Lead_Status", models.IntegerField(default=0)),
                ("Upcoming_Meetings", models.IntegerField(default=0)),
                ("Previous_Meetings", models.IntegerField(default=0)),
                ("Rejected_Proposals", models.IntegerField(default=0)),
                ("Accepted_proposals", models.IntegerField(default=0)),
                ("Cancel_Date", models.DateField(null=True)),
                ("Cancel_Reason", models.TextField(blank=True, null=True)),
                ("To_Opertunity", models.DateField(null=True)),
                ("To_Proposal", models.DateField(null=True)),
                ("To_Client", models.DateField(null=True)),
                ("To_Project", models.DateField(null=True)),
                ("Reject_Date", models.DateField(null=True)),
                (
                    "Salesman",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Date", models.DateTimeField(null=True)),
                ("Status", models.IntegerField(default=1)),
                ("AddedBy", models.IntegerField(default=0)),
                ("Ip", models.GenericIPAddressField(null=True)),
                ("Edited_Date", models.DateTimeField(auto_now_add=True)),
                ("EditedBy", models.IntegerField(default=0)),
                ("EditedIp", models.GenericIPAddressField(null=True)),
                ("Name", models.CharField(max_length=50)),
                ("Buying_Price", models.FloatField()),
                ("Selling_Price", models.FloatField(blank=True, null=True)),
                ("Reference", models.CharField(max_length=20)),
                ("Description", models.TextField(null=True)),
                ("Unit", models.CharField(blank=True, max_length=5, null=True)),
                (
                    "Category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="administrator.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Proposal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Date", models.DateTimeField()),
                ("Status", models.IntegerField(default=1)),
                ("AddedBy", models.IntegerField(default=0)),
                ("Ip", models.GenericIPAddressField(blank=True, null=True)),
                ("Reviced", models.IntegerField(null=True)),
                ("Revised_Date", models.DateField(null=True)),
                ("revisible", models.BooleanField(default=True)),
                ("Revisions_Total", models.IntegerField(default=0)),
                ("Reference", models.CharField(max_length=20)),
                ("Proposal_Status", models.IntegerField(default=10)),
                (
                    "Proposal_Title",
                    models.CharField(blank=True, max_length=225, null=True),
                ),
                (
                    "Project_Name",
                    models.CharField(blank=True, max_length=225, null=True),
                ),
                ("Proposal_Date", models.DateField(blank=True, null=True)),
                ("Expire_Date", models.DateField(blank=True, null=True)),
                ("Subject", models.CharField(blank=True, max_length=225, null=True)),
                ("Scope", ckeditor.fields.RichTextField(blank=True, null=True)),
                ("Payment", ckeditor.fields.RichTextField(blank=True, null=True)),
                ("Exclusion", ckeditor.fields.RichTextField(blank=True, null=True)),
                (
                    "Terms_Condition",
                    ckeditor.fields.RichTextField(blank=True, null=True),
                ),
                ("Oppertunity", models.TextField(blank=True, null=True)),
                ("Action_Date", models.DateField(null=True)),
                ("PO_Number", models.CharField(max_length=50, null=True)),
                ("PO_Date", models.DateField(null=True)),
                ("PO_Value", models.FloatField(null=True)),
                ("PO_Description", models.TextField(null=True)),
                ("Grand_Total", models.FloatField(null=True)),
                ("Discount", models.FloatField(null=True)),
                ("Method", models.IntegerField(null=True)),
                ("Attachments", models.ManyToManyField(to="administrator.attachments")),
                (
                    "Lead",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="administrator.lead",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Date", models.DateTimeField()),
                ("Status", models.IntegerField(default=1)),
                ("AddedBy", models.IntegerField(default=0)),
                ("Ip", models.GenericIPAddressField(blank=True, null=True)),
                ("Title", models.CharField(max_length=50)),
                ("Priority", models.CharField(max_length=25, null=True)),
                ("Due_Date", models.DateField()),
                ("Description", models.TextField()),
                ("Task_Status", models.IntegerField(default=0)),
                ("Completed_Date", models.DateField(null=True)),
                ("notification", models.IntegerField(default=1)),
                ("Attachment", models.ManyToManyField(to="administrator.attachments")),
                (
                    "Lead",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="administrator.lead",
                    ),
                ),
                (
                    "Salesman",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Salesman_Report",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Status", models.IntegerField(default=1)),
                ("Pending_Tasks", models.IntegerField(default=0)),
                ("Completed_Tasks", models.IntegerField(default=0)),
                ("Lead_Total", models.IntegerField(default=0)),
                ("Lead_Succes", models.IntegerField(default=0)),
                ("Lead_Faild", models.IntegerField(default=0)),
                ("Opportunity_Total", models.IntegerField(default=0)),
                ("Opportunity_Success", models.IntegerField(default=0)),
                ("Opportunity_Faild", models.IntegerField(default=0)),
                ("Proposal_Total", models.IntegerField(default=0)),
                ("Proposal_Success", models.IntegerField(default=0)),
                ("Proposal_Faild", models.IntegerField(default=0)),
                ("SV_Pending", models.FloatField(default=0)),
                ("SV_Success", models.FloatField(default=0)),
                ("SV_Failed", models.FloatField(default=0)),
                ("Upcoming_Meetings", models.IntegerField(default=0)),
                ("Previous_Meetings", models.IntegerField(default=0)),
                (
                    "Salesman",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Sales_Target",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("From", models.DateField(blank=True, null=True)),
                ("To", models.DateField(blank=True, null=True)),
                ("Targets", models.FloatField(default=0)),
                ("Balance", models.FloatField(default=0)),
                ("Archived", models.FloatField(default=0)),
                ("Pending", models.FloatField(default=0)),
                ("Failed", models.FloatField(default=0)),
                (
                    "Salesman",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("AddedDate", models.DateField(null=True)),
                ("Message", models.TextField()),
                ("Attachments", models.ManyToManyField(to="administrator.attachments")),
                (
                    "Task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="administrator.task",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Replays",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Date", models.DateTimeField()),
                ("Status", models.IntegerField(default=1)),
                ("Ip", models.GenericIPAddressField(blank=True, null=True)),
                ("AddedDate", models.DateField(null=True)),
                ("Message", models.TextField()),
                (
                    "AddedBy",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("Attachments", models.ManyToManyField(to="administrator.attachments")),
                (
                    "Task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="administrator.task",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Receipt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Date", models.DateField()),
                ("Status", models.IntegerField(default=1)),
                ("AddedBy", models.IntegerField(default=0)),
                ("Ip", models.GenericIPAddressField(blank=True, null=True)),
                ("Reference", models.CharField(max_length=25)),
                ("Amount", models.FloatField()),
                (
                    "Proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="administrator.proposal",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Proposal_Items",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Sell_Price", models.FloatField()),
                ("Quantity", models.IntegerField()),
                ("Total", models.FloatField()),
                (
                    "Product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="administrator.product",
                    ),
                ),
                (
                    "Proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="administrator.proposal",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(auto_now_add=True)),
                ("Message", models.CharField(max_length=225)),
                ("Read_Status", models.BooleanField(default=False)),
                ("Read_Date", models.DateField(null=True)),
                (
                    "added_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="added_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "notification_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notification_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Lead_Update",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Date", models.DateTimeField()),
                ("Status", models.IntegerField(default=1)),
                ("AddedBy", models.IntegerField(default=0)),
                ("Ip", models.GenericIPAddressField(blank=True, null=True)),
                ("AddedDate", models.DateField(null=True)),
                ("Description", models.TextField()),
                ("Attachments", models.ManyToManyField(to="administrator.attachments")),
                (
                    "Lead",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="administrator.lead",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Lead_Schedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Date", models.DateTimeField()),
                ("Status", models.IntegerField(default=1)),
                ("AddedBy", models.IntegerField(default=0)),
                ("Ip", models.GenericIPAddressField(blank=True, null=True)),
                ("Reference", models.CharField(max_length=25, null=True)),
                ("AddedDate", models.DateField(null=True)),
                ("Mode", models.CharField(max_length=25)),
                ("From", models.TimeField()),
                ("To", models.TimeField()),
                ("Description", models.TextField()),
                ("Schedule_Status", models.IntegerField(default=1)),
                ("Members", models.CharField(max_length=255)),
                ("Update_Description", models.TextField()),
                ("Update_Date", models.DateField(null=True)),
                ("notification", models.IntegerField(default=1)),
                ("Attachment", models.ManyToManyField(to="administrator.attachments")),
                (
                    "Lead",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="administrator.lead",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Invoice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Date", models.DateField()),
                ("Status", models.IntegerField(default=1)),
                ("AddedBy", models.IntegerField(default=0)),
                ("Ip", models.GenericIPAddressField(blank=True, null=True)),
                ("Reference", models.CharField(max_length=25)),
                ("Amount", models.FloatField()),
                (
                    "Proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="administrator.proposal",
                    ),
                ),
            ],
        ),
    ]
