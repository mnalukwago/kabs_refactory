from django.urls import path
from . import views
from .views import Login  
from .views import director_dashboard
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views  # if you have custom views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('home/', views.home, name='home'),  
    path('', views.index_view, name='index'),  # root URL
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),


    path('login/', Login, name='login'),
    # path('dashboard/director/', director_dashboard, name='director_dashboard'),
    path("director/dashboard/", views.director_dashboard, name="director_dashboard"),


    # procurement
    path('procurement/new/', views.create_procurement, name='create_procurement'),
    path('procurements/', views.procurement_list, name='procurement_list'),

    # sales
    path('sales/', views.sales_list, name='sales_list'),
    path('sales/new/', views.create_sale, name='create_sale'),

    # creditsales
    path('credit-sale/new/', views.create_credit_sale, name='create_credit_sale'),
    path('credit-sales/', views.credit_sales_list, name='credit_sales_list'),

    # supplier
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
    path('suppliers/edit/<int:pk>/', views.edit_supplier, name='edit_supplier'),
    path('suppliers/delete/<int:pk>/', views.delete_supplier, name='delete_supplier'),

    # produce
    path('produce/', views.produce_list, name='produce_list'),
    path('produce/add/', views.add_produce, name='add_produce'),
    path('produce/edit/<int:pk>/', views.edit_produce, name='edit_produce'),
    path('produce/delete/<int:pk>/', views.delete_produce, name='delete_produce'),

    # branch
    path('branches/add/', views.add_branch, name='add_branch'),
    path('branches/', views.branch_list, name='branch_list'),
    path('branches/edit/<int:pk>/', views.edit_branch, name='edit_branch'),
    path('branches/delete/<int:pk>/', views.delete_branch, name='delete_branch'),

    #receipt
    path('receipts/', views.receipt_list, name='receipt_list'),
    path('receipts/new/', views.create_receipt, name='create_receipt'),
    path('receipts/<int:pk>/', views.receipt_detail, name='receipt_detail'),

    # dashboards
    path('manager/dashboard/matugga/', views.manager_dashboard_matugga, name='manager_dashboard_matugga'),
    path('manager/dashboard/maganjo/', views.manager_dashboard_maganjo, name='manager_dashboard_maganjo'),
    path('sales_agent/dashboard/matugga/', views.sales_agent_dashboard_matugga, name='sales_agent_dashboard_matugga'),
    path('sales_agent/dashboard/maganjo/', views.sales_agent_dashboard_maganjo, name='sales_agent_dashboard_maganjo'),

]





