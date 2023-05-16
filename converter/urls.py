from django.urls import path
from converter import views

urlpatterns = [
    path('opportunities',views.list_opertunities,name='list-opportunities'),
    path('opportunity-view/<int:lid>',views.view_opertunity,name='view-opportunity'),

    path('set_proposal/<int:lid>/',views.proposal,name='set-proposal'),
    path('proposal/<int:lid>/',views.create_proposal,name='proposal'),
    path('list-proposals/<str:status>/',views.list_proposals,name='list-proposals'),
    path('view-proposal/<int:pid>/',views.view_proposal,name='view-proposal'),
    path('edit-proposal/<int:pid>/',views.edit_proposal,name='edit-proposal'),

    path('create-task/',views.create_task,name='create-task'),
    path('pending-task/',views.pending_task,name='pending-task'),
    path('completed-task/',views.completed_task,name='completed-task'),
    path('edit-task/<int:tid>/',views.edit_task,name='edit-task'),
    path('pending-task/<int:tid>/',views.view_pending_task,name='pending-task-view'),
    path('completed-task/<int:tid>/',views.view_completed_task,name='completed-task-view'),
    path('task-staff/',views.task_staff,name='task-staff'),
    path('task-staff/<int:uid>/',views.task_staff_view,name='task-staff-view'),

    path('clients/',views.client_list,name='clients'),
    path('client-view/<int:cid>/',views.client_view,name='client-view'),

    path('accept/<int:pid>/',views.accept,name='accept'),
    path('reject/<int:pid>/',views.reject,name='reject'),

    path('projects/',views.projects,name='projects'),
    path('projects/<int:pid>/',views.view_project,name='view-project'),

    path('upcomin-meetings/',views.upcoming_meetings,name='upcoming-meetings'),
    path('previous-meetings/',views.previous_meetings,name='previous-meetings'),
    path('meeting-staff-list/',views.meeting_staff_list,name='meeting-staff-list'),
    path('meeting-staff-view/<int:uid>/',views.meeting_staff_view,name='meeting-staff-view'),
    path('edit-meeting/<int:id>/',views.edit_upcoming_meeting,name='edit-meeting'),

    path('salesman-report/',views.salesman_report,name='salesman-report'),
    path('salestarget/',views.salestarget,name='sales-target'),
    path('target-report/',views.target_report,name='target-report'),
    path('top-customers/',views.top_customers,name='top-customers'),
    path('proposal_report/',views.proposal_report,name='proposal_report'),
    path('total-proposal/',views.total_propose,name='total-propose'),

    path('previous-meeting-details/<int:mid>/',views.previous_meeting_details,name='p-meeting-d'),

    path('r_p_p/<int:pid>/<int:id>/',views.remove_proposal_product,name='r_p_p'),
    path('g-p/',views.get_product,name='g-p'),
    path('g-p-d/',views.get_product_data,name='g-p-d'),
    path('save-product/',views.save_product,name='save-product'),

    path('print-proposal/<int:pid>/',views.print_proposal,name='print-proposal'),
    path('print-proposal-boq/<int:pid>/',views.print_proposal_boq,name='print-proposal-boq'),
    path('print-proposal-noboq/<int:pid>/',views.print_proposal_noboq,name='print-proposal-noboq'),
    path('print-proposal-noprice/<int:pid>/',views.print_proposal_noprice,name='print-proposal-noprice'),

    path('reviced/<int:lid>/',views.reviced_proposal,name='revice-proposal'),
    path('revice/<int:id>/',views.revise_proposal,name='revice'),

    path('add-proposal-product/',views.add_proposal_product,name='add-proposal-product'),
    path('add_percentage/',views.add_percentage,name='add-percentage')
]