from django.urls import path
from administrator import views
from administrator import exports

urlpatterns = [
    path('add-category/',views.add_category,name='add-category'),
    path('list-category/',views.list_category,name='list-category'),
    path('view-category/<int:cid>/',views.view_category,name='view-category'),
    path('edit-category/<int:cid>/',views.edit_category,name='edit-category'),
    
    path('add-product/',views.add_product,name='add-product'),
    path('list-product/',views.list_products,name='list-product'),
    path('view-product/<int:pid>/',views.view_product,name='view-product'),
    path('edit-product/<int:pid>/',views.edit_product,name='edit-product'),

    path('add-salesman/',views.add_salesman,name='add-salesman'),
    path('list-salesman/',views.list_salesman,name='list-salesman'),
    path('edit-salesman/<int:uid>/',views.edit_salesman,name='edit-salesman'),
    path('salesman-view/<int:sid>/',views.salesman_view,name='salesman-view'),

    path('add-leads/',views.add_lead,name='add-lead'),
    path('list-lead/',views.list_leads,name='list-lead'),
    path('edit-lead/<int:lid>/',views.edit_lead,name='edit-lead'),
    path('view-lead/<int:lid>',views.view_lead,name='view-lead'),

    path('opertunity-convertion/<int:lid>/',views.opertunity_convertion,name='convert-op'),

    path('canceld-leads/',views.canceld_leads,name='canceld-leads'),
    path('canceled-view/<int:lid>/',views.view_canceled,name='view-canceled'),
    path('canceled-opportunity-view/<int:lid>/',views.canceled_opertunity_view,name='canceled-opportunity'),
    path('canceled-client-view/<int:lid>/',views.canceled_client_view,name='canceled-client'),
    path('canceled-project-view/<int:lid>/',views.canceled_project_view,name='canceled-project'),

    path('assign-target/',views.assign_target,name='assign-target'),
    path('target-setup/',views.target_setup,name='target-setup'),
    path('target-view/<int:year>',views.target_view,name='target-view'),

    path('g-t-d/',views.get_target_data,name='get-target-data'),

    path('export-catagories/',exports.export_catagories,name='export_catagories'),
    path('export-products/',exports.export_products,name='export_products'),

    path('c-p/',views.check_part_number,name='check_part_number'),
]