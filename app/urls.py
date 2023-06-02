from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index,name='index'),
    path('user_login/', views.user_login,name='user_login'),
    path('user_logout/', views.user_logout,name='user_logout'),
    path('signup/', views.signup,name='signup'),
    path('about_us/', views.about_us, name='about_us'),

# -----------------------------admin tabs-------------------------------
    path('admin_homepage', views.admin_homepage,name='admin_homepage'),
    path('project/', views.project,name='project'),
    path('remove_project/<int:id>', views.remove_project, name='remove_project'),
    path('add_project/', views.add_project,name='add_project'),
    path('<int:id>/', views.update_project, name='update_project'),
    path('user_details/', views.user_details, name='user_details'),
    path('know_more/<int:id>', views.know_more, name='know_more'),
    path('admin_about_us/', views.admin_about_us, name='admin_about_us'),
    path('payment_received/', views.payment_received, name='payment_received'),
    path('payment_received_update/<int:id>', views.payment_received_update, name='payment_received_update'),
    path('payment_made/', views.payment_made, name='payment_made'),
    path('add_payment/', views.add_payment, name='add_payment'),
    path('my_investment/', views.my_investment, name='my_investment'),
    path('user_my_investment/', views.user_my_investment, name='user_my_investment'),
    path('user_my_investment_detail/<int:id>', views.user_my_investment_detail, name='user_my_investment_detail'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('admin_signup/', views.admin_signup,name='admin_signup'),






# ------------------------------user tabs------------------------------
    path('user_homepage', views.user_homepage,name='user_homepage'),
    path('user_about_us', views.user_about_us,name='user_about_us'),
    path('user_know_more/<int:id>', views.user_know_more,name='user_know_more'),
    path('user_invest/<int:id>', views.user_invest,name='user_invest'),
    path('user_invest_response', views.user_invest_response,name='user_invest_response'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('edit_user_profile/', views.edit_user_profile, name='edit_user_profile'),


    



   
]