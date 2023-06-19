from django.contrib import admin
from django.urls import path
from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index,name='index'),
    path('user_login/', views.user_login,name='user_login'),
    path('user_logout/', views.user_logout,name='user_logout'),
    path('signup/', views.signup,name='signup'),
    path('about_us/', views.about_us, name='about_us'),
    path('change_password1/', views.change_password1, name='change_password1'),
    path('change_password2/<str:username>', views.change_password2, name='change_password2'),
    path('admin_update_password/', views.admin_update_password, name='admin_update_password'),
    path('user_update_password/', views.user_update_password, name='user_update_password'),

# --------------------forget password------------------------------------------------------------
    path('reset_password/', auth_views.PasswordResetView.as_view(), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name ='password_reset_complete'),
    


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
    # path('user_my_investment_detail/<int:id>', views.user_my_investment_detail, name='user_my_investment_detail'),
    path('user_my_investment_detail/', views.user_my_investment_detail, name='user_my_investment_detail'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('admin_signup/', views.admin_signup,name='admin_signup'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    path('edit_admin_profile/', views.edit_admin_profile, name='edit_admin_profile'),
    path('enable_user/<int:id>', views.enable_user, name='enable_user'),
    path('disable_user/<int:id>', views.disable_user, name='disable_user'),
    path('edit_project_images/<str:data>', views.edit_project_images, name='edit_project_images'),
    path('delete_image/<str:id>', views.delete_image, name='delete_image'),
    path('add_images/', views.add_images, name='add_images'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('dashboard_investment/', views.dashboard_investment, name='dashboard_investment'),
    path('dashboard_income/', views.dashboard_income, name='dashboard_income'),
    path('edit_user_profile_by_admin/<str:id>', views.edit_user_profile_by_admin, name='edit_user_profile_by_admin'),







# ------------------------------user tabs------------------------------
    path('user_homepage', views.user_homepage,name='user_homepage'),
    path('user_about_us', views.user_about_us,name='user_about_us'),
    path('user_know_more/<int:id>', views.user_know_more,name='user_know_more'),
    path('user_invest/<int:id>', views.user_invest,name='user_invest'),
    path('user_invest_response', views.user_invest_response,name='user_invest_response'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('edit_user_profile/', views.edit_user_profile, name='edit_user_profile'),

    path('demo/', views.demo, name='demo'),

    



   
]