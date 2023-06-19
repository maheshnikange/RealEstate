from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import SignUpForm,add_project_form,ImageForm,userUpdateForm,ProfileForm
from django.contrib.auth.models import User
from .models import Project,Image,My_income,My_Investment,Profile
import os
from django.db.models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    project_data=Project.objects.all()
    return render(request,'index.html',{'data':project_data})

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        print(username)
        user=authenticate(request,username=username,password=password)
        if user is not None:
            print(username,'----',user)
            login(request,user)
            if username=='admin':
                return redirect('admin_homepage')
            else:
                id=User.objects.filter(username=username).values('id')
                print('user_id for profile',id)
                id_value=id[0]['id']
                print(id_value)
                id_value=str(id_value)
                flag=Profile.objects.filter(user=id_value)
                print(flag)

                flag=Profile.objects.filter(user=id_value).values('activate_flag')
                print('flag',flag)
                flag_value=flag[0]['activate_flag']
                if flag_value=='0':
                    messages.error(request,'Please Kindly contact to admin for login !')
                    return redirect('user_login')

                else:
                    return redirect('user_homepage')
        else:
            messages.error(request,'you have entered wrong username or password !')
            return redirect('user_login')
    return render(request,'login.html')
# ---------------------user logout----------------------------------------
def user_logout(request):
    logout(request)
    return redirect('index')

# -----------------------sign up--------------------------------------------
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['first_name']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password=request.POST['password1']
        password2=request.POST['password2']   
        if len(username)<4:
            messages.error(request,'Username must be greater than 3 characters')
            return redirect('signup')
        if password !=password2:
            messages.error(request,'Passwords do not match')
            return redirect('signup')
        if '@' not in email:
            messages.error(request,'not a valid email')
            return redirect('signup')

        user = User.objects.create_user(username,email=email,password=password)
        user.first_name = firstname  # use the correct attribute here.
        user.last_name = lastname  # use the correct attribute here.
        user.save()
        profile=Profile.objects.create(user=user)
        profile.save()
        return redirect('user_login')
    else:
        form=SignUpForm()
        return render(request,'signup.html',{'form': form})
# ----------------------------------------------------------------------
def admin_homepage(request):
    Project_list=Project.objects.all()
    user_list=User.objects.get(username=request.user)
    profile_info=Profile.objects.filter(user=request.user)
    if len(profile_info)==1:
        profile_info=Profile.objects.get(user=request.user)
        return render(request,'admin_homepage.html',{'data':Project_list,'profile':profile_info,'data1':user_list})    
    else:
        return render(request,'admin_homepage.html',{'data':Project_list,'data1':user_list})    

# --------------------admin about us------------------------------------
def admin_about_us(request):
    user_list=User.objects.get(username=request.user)
    profile_info=Profile.objects.filter(user=request.user)
    if len(profile_info)==1:
        profile_info=Profile.objects.get(user=request.user)
    return render(request,'admin_about_us.html',{'profile':profile_info,'data1':user_list})



# --------------------User list------------------------------------------
def user_details(request):
    users=User.objects.all()
    user_list=User.objects.get(username=request.user)
    page=Paginator(users,10)
    page_list=request.GET.get('page')
    page=page.get_page(page_list)
    nums="a"*page.paginator.num_pages

    profile_info=Profile.objects.filter(user=request.user)
    if len(profile_info)==1:
        profile_info=Profile.objects.get(user=request.user)
    all_profile_info=Profile.objects.all()
    
    return render(request,'user_details.html',{'users':users,'profile':profile_info,'data1':user_list,'page':page,'nums':nums,'all_profile_info':all_profile_info})
# -----------------------------Projects--------------------------
def project(request):
    data=Project.objects.all()
    user_list=User.objects.get(username=request.user)
    profile_info=Profile.objects.filter(user=request.user)
    if len(profile_info)==1:
        profile_info=Profile.objects.get(user=request.user)
    return render(request,'projects.html',{'data':data,'profile':profile_info,'data1':user_list})

# ----------------------add project--------------------------
def add_project(request):
    if request.method=='POST':
        form=add_project_form(request.POST)
        files=request.FILES.getlist('image')
        if form.is_valid():
            f=form.save(commit=False)
            f.save()
            print(f,type(f),'project_intsnce-----------------')
            for i in files:
                Image.objects.create(project=f,image=i)    
            return redirect('admin_homepage')
    else:
        form1=add_project_form()
        form2=ImageForm()
        return render(request,'add_project.html',{'form1':form1,'form2':form2})
# -------------------------------know more tab----------------------------

def know_more(request,id):
    data1=Project.objects.get(id=id)
    print(data1.project_name)
    project=data1.project_name.split()
    project='_'.join(project)
    list2=[]
    list1=Image.objects.values_list('image')
    list1=list(list1)
    for i in list1:
        i=str(i)
        list2.append(i[14:-3])
    list3=[]
    for i in list2:
        if i.startswith(project):
            list3.append(i)
    print('---------------------')
    print(project,list3,list2)

    # ------------capture current status from project----------
    context={
    'land_purchase':data1.land_purchased,
    'sales':data1.sales,
    'development':data1.development
    }
    return render(request,'know_more.html',{'data':data1,'Image_list':list3,'status':context})

# ------------------------------remove project---------------------------------
def remove_project(request,id):
    data=Project.objects.get(id=id)
    data.delete()
    data=Project.objects.all()
    return render(request,'projects.html',{'data':data})
# -------------------------about us---------------------------------------------
def about_us(request):
    return render(request,'about_us.html')

# -----------------------------user homepage--------------------------------------
def user_homepage(request):
    user_list=User.objects.get(username=request.user)
    profile_info=Profile.objects.filter(user=request.user)
    if len(profile_info)==1:
        profile_info=Profile.objects.get(user=request.user)
    project_data=Project.objects.all()
    return render(request,'user_homepage.html',{'data':project_data,'profile':profile_info,'data1':user_list})

def user_about_us(request):
    user_list=User.objects.get(username=request.user)
    profile_info=Profile.objects.filter(user=request.user)
    if len(profile_info)==1:
        profile_info=Profile.objects.get(user=request.user)
    return render(request,'user_about_us.html',{'profile':profile_info,'data1':user_list})

def user_know_more(request,id):
    data1=Project.objects.get(id=id)
    print(data1.project_name)
    project=data1.project_name.split()
    project='_'.join(project)
    list2=[]
    list1=Image.objects.values_list('image')
    list1=list(list1)
    for i in list1:
        i=str(i)
        list2.append(i[14:-3])
    list3=[]
    for i in list2:
        if i.startswith(project):
            list3.append(i)
    print('---------------------')
    print(project,list3,list2)

    # ------------capture current status from project----------
    context={
    'land_purchase':data1.land_purchased,
    'sales':data1.sales,
    'development':data1.development
    }
    return render(request,'user_know_more.html',{'data':data1,'Image_list':list3,'status':context})

# ---------------------------------user invest----------------------------------

def user_invest(request,id):
    if request.method=='POST':
        project_name=request.POST['project']    
        amount=request.POST['amount']
        username=request.user
        data=My_Investment(project_name=project_name,amount_invested=amount,username=username)
        data.save()
        return render(request,'user_invest_response.html')
    else:
        project_name=Project.objects.get(id=id)
        print(project_name,'--------')
        return render(request,'user_invest.html',{'project':project_name})

def user_invest_response(request):
    if request.method=='POST':
        project_name=request.POST['project']    
        amount=request.POST['amount']
        username=request.user
        print(username,'username ----')
        data=My_Investment(project_name=project_name,amount_invested=amount,username=username)
        data.save()
    return render(request,'user_invest_response.html')

# ----------------------payment received------------------------------------
flag=''
def payment_received(request):
    data=My_Investment.objects.all()
    user_list=User.objects.get(username=request.user)
    profile_info=Profile.objects.filter(user=request.user)
    if len(profile_info)==1:
        profile_info=Profile.objects.get(user=request.user)
    return render(request,'payment_received.html',{'data':data,'flag':'','profile':profile_info,'data1':user_list})
# ---------------------------payment made---------------------------------
def payment_made(request):
    data=My_income.objects.all()
    user_list=User.objects.get(username=request.user)
    profile_info=Profile.objects.filter(user=request.user)
    if len(profile_info)==1:
        profile_info=Profile.objects.get(user=request.user)
    return render(request,'payment_made.html',{'data':data,'profile':profile_info,'data1':user_list})
# -------------------------------add payment-------------------------------
def add_payment(request):
    if request.method=='POST':
        username=request.POST['user_name']
        project=request.POST['project']
        amount=request.POST['amount']
        print(username,project,amount)
        # ---------get Projectname ,username---------------
        project_name=Project.objects.get(id=project)
        user_name=User.objects.get(id=username)
        print(project_name,user_name)
        # ----------add values to My_income1 model----
        from datetime import date
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        p=My_income(project_name=project_name,username=user_name,amount_received=amount,date=d1)
        p.save()
        
        amt=My_Investment.objects.filter(Q(project_name=project_name) & Q(username=user_name)).values('amount_received')[0]
        print(amt['amount_received'],'------------------p')
        Total_amt=int(amt['amount_received'])+int(amount)
        # ------------update--------------------
        My_Investment.objects.filter(project_name=project_name).update(amount_received=Total_amt)
        return redirect('admin_homepage')
    else:
        data1=Project.objects.all()
        data2=User.objects.all()
        print(data1)
        print(data2)
    return render(request,'add_payment.html',{'projects':data1,'users':data2})

# -----------------------------my investment--------------------------------
def my_investment(request):
    user1=request.user
    data1=My_Investment.objects.filter(username=user1)
    print('my investment',data1)
    return render(request,'my_investment.html',{'data1':data1})
# -----------------------------user my investment--------------------------------
def user_my_investment(request):
    user1=request.user
    data1=My_Investment.objects.filter(username=user1)
    print('my investment',data1,user1)
    if request.user=='admin':
        return render(request,'my_investment.html',{'data1':data1})
    else:
        profile_info=Profile.objects.filter(user=request.user)
        if len(profile_info)==1:
            profile_info=Profile.objects.get(user=request.user)
        return render(request,'user_my_investment.html',{'profile':profile_info,'data1':data1})
# --------------------------payment received update----------------------------------
def payment_received_update(request,id=None):
    if request.method=='POST':
        flag=1
        amt=request.POST['amt']
        date=request.POST['date']
        d=My_Investment.objects.filter(id=id).values().update(amount_received=amt,date_of_received=date)
        data=My_Investment.objects.all()
        return render(request,'payment_received.html',{'data':data})
    else:
        data=My_Investment.objects.all()
        return render(request,'payment_received_update.html',{'data':data,'flag':''})
# -------------------my investment detail-------------------------------------------------
def user_my_investment_detail(request):
    if request.method=='POST':
        print(request.user,'--------------------llll---')
        p=request.POST['project_name1']
        data_for_project_name=My_income.objects.filter(username=request.user).values('project_name')[0]
        print(data_for_project_name)
        data1=My_Investment.objects.filter(username=request.user)
        data=My_income.objects.filter(username=request.user , project_name=p)

        profile_info=Profile.objects.filter(user=request.user)
        if len(profile_info)==1:
            profile_info=Profile.objects.get(user=request.user)
        # return render(request,'user_my_investment.html',{'profile':profile_info,'data1':data1})
        return render(request,'user_my_investment_detail.html',{'data':data,'data1':data1,'project':data_for_project_name,'profile':profile_info})

# ---------------------update project------------------------------------------------------
def update_project(request,id):
    if request.method=='POST':
        data1=Project.objects.get(id=id)
        data2=str(data1)
        data2=data2.replace(' ','_')
        print(data2,type(data2),len(data2),'ppppppppppppppppppppp')
        fm=add_project_form(request.POST,request.FILES, instance=data1)
        if fm.is_valid():
            fm.save()
            data=Project.objects.all()
            return redirect('edit_project_images',data2)
            # return render(request,'admin_homepage.html',{'data':data})
        
    else:
        data=Project.objects.get(id=id)
        fm=add_project_form(instance=data)
        img1=ImageForm(instance=data)
    user_list=User.objects.get(username=request.user)
    profile_info=Profile.objects.filter(user=request.user)
    if len(profile_info)==1:
        profile_info=Profile.objects.get(user=request.user)
    return render(request,'update_project.html',{'form':fm,'img1':img1,'profile':profile_info,'data1':user_list})

# ----------------------------------user profile--------------------------------------------------
def user_profile(request):
    if request.method=='POST':
        user_info=User.objects.get(username=request.user)
        profile_info=Profile.objects.get(user=request.user)
        return render(request,'5my_profile.html',{'form':user_info,'profile':profile_info})
    else:
        u_form=userUpdateForm(instance=request.user)
        user1=request.user
        user_check=Profile.objects.filter(user=user1)
        print(user_check,len(user_check),'-------')
        if len(user_check)==0:
            p=Profile.objects.create(user=user1)
        user_info=User.objects.get(username=request.user)
        profile_info=Profile.objects.get(user=request.user)
        return render(request,'user_profile.html',{'form':user_info,'profile':profile_info})
# -----------------------------------------------edit profile-------------------------------------
def edit_user_profile(request):
    if request.method=='POST':
        u_form=userUpdateForm(request.POST, instance=request.user)
        p_form=ProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect(user_profile)
    else:
        u_form=userUpdateForm(instance=request.user)
        p_form=ProfileForm(instance=request.user.profile)
        context={'u_form':u_form,'p_form':p_form}
        return render(request,'edit_user_profile.html',context)
# -----------------------------------------------edit profile-------------------------------------
def edit_user_profile_by_admin(request,id=None):
    
    if request.method=='POST':
        userid=Profile.objects.filter(id=id).values('user')[0]['user']
        username=User.objects.get(id=userid)
        u_form=userUpdateForm(request.POST, instance=username)
        p_form=ProfileForm(request.POST,request.FILES, instance=username.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect(user_details)
        else:
            print('invalid')
    else:
        print(id,'--------------------')
        userid=Profile.objects.filter(id=id).values('user')[0]['user']
        username=User.objects.get(id=userid)
        u_form=userUpdateForm(instance=username)
        p_form=ProfileForm(instance=username.profile)
        context={'u_form':u_form,'p_form':p_form}
        return render(request,'edit_user_profile.html',context)



# ------------------------------remove user---------------------------------
def delete_user(request,id):
    data=User.objects.get(id=id)
    data.delete()
    data=User.objects.all()
    return render(request,'user_details.html',{'data':data})
# --------------------------------admin_signup----------------------------------
def admin_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print('---------')
        if form.is_valid():
            username = form.cleaned_data['username']
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            password=form.cleaned_data['password1']
            user = User.objects.create_user(username,email=email,password=password)
            user.first_name = firstname  # use the correct attribute here.
            user.last_name = lastname  # use the correct attribute here.
            user.save()
            # form.save()
            msg = 'user created'
            return redirect('user_login')
        else:
            print('Invalid Creds')
            form = SignUpForm()
            return render(request,'admin_signup.html',{'form': form})
    else:
        form=SignUpForm()
        return render(request,'admin_signup.html',{'form': form})
# ---------------------------------------admin_profile--------------------------------------
def admin_profile(request):
    u_form=userUpdateForm(instance=request.user)
    user1=request.user
    user_check=Profile.objects.filter(user=user1)
    print(user_check,len(user_check),'-------')
    if len(user_check)==0:
        p=Profile.objects.create(user=user1)
    user_info=User.objects.get(username=request.user)
    profile_info=Profile.objects.get(user=request.user)
    return render(request,'admin_profile.html',{'form':user_info,'profile':profile_info})
# -----------------------------------------------edit admin profile-------------------------------------
def edit_admin_profile(request):
    if request.method=='POST':
        u_form=userUpdateForm(request.POST, instance=request.user)
        p_form=ProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect(admin_profile)
    else:
        u_form=userUpdateForm(instance=request.user)
        p_form=ProfileForm(instance=request.user.profile)
        context={'u_form':u_form,'p_form':p_form}
        return render(request,'edit_admin_profile.html',context)

# ---------------------------Enable User---------------------------------------------------------------------
def enable_user(request,id=None):
    print(id,type(id))
    user1=User.objects.filter(id=id).values('first_name')[0]['first_name']
    print(user1,type(user1))
    user2=Profile.objects.filter(user=id).values()
    print(user2,'ssssssssssss')
    activate_user=Profile.objects.filter(user_id=id).update(activate_flag=1)
    return redirect('user_details')

def disable_user(request,id=None):
    print(id,type(id))
    user1=User.objects.filter(id=id).values('first_name')[0]['first_name']
    print(user1,type(user1))
    user2=Profile.objects.filter(user=id).values()
    print(user2,'ssssssssssss')
    activate_user=Profile.objects.filter(user_id=id).update(activate_flag=0)
    return redirect('user_details')

# ----------------------------change password---------------------------------------------------------------

def change_password1(request):
    if request.method == 'POST':
        username=request.POST['username']
        # return render(request, 'change_password2.html',{'username':username})  
        return redirect('change_password2',username)
    else:
        return render(request, 'change_password1.html')  

def change_password2(request,username):
    if request.method == 'POST':
        user=User.objects.get(username=username)
        p1=request.POST['p1']
        p2=request.POST['p2']
        if p1==p2 and len(p1)>=8:
            print('same')
            check=user.check_password(p1)
            user.set_password(p1)
            user.save()
            return redirect('user_login')
        elif p1!=p2:
            messages.error(request, 'password and re-enter password are different')
            return redirect('change_password2',username)  
        elif len(p1)<8:
            messages.error(request, 'Password must be more than length 8 ')
            return redirect('change_password2',username)  
    else:
        # print(user,'-------------kkkkkkkkk')
        return render(request, 'change_password2.html', {'username':username})  
# --------------------------------------edit_project_images-----------------------------------

def edit_project_images(request,data):
    images=Image.objects.all()
    image_list=[]
    for i in images:
        k=str(i.image)[12:]
        image_prefix=data[0:6]
        print(k,image_prefix)
        if k.startswith(image_prefix):
            image_list.append(k)
    return render(request,'edit_project_images.html',{'data':image_list})
# ------------------------------delete_image from projects-----------------------------------
def delete_image(request,id=None):
    print(id,'-------------------------------')
    image_id=Image.objects.filter(image__contains=id).values('id')
    data=Image.objects.get(id=image_id[0]['id'])
    data.delete()
    data1=Project.objects.all()
    return render(request,'projects.html',{'data':data1})
# ------------------add Images for project----------------------------------------------------
def add_images(request):
    if request.method=='POST':
        files=request.FILES.getlist('image')
        print(files,'sssssssssssssssss')
        for i in files:
            k=i
        k=str(k)
        k=k.split('_')[0]
        print(k)
        project_instance=Project.objects.get(project_name=k)
        print(project_instance,type(project_instance))


        for i in files:
            Image.objects.create(project=project_instance ,image=i)    
        return redirect('admin_homepage')
    else:
        form2=ImageForm()
        return render(request,'add_images.html')
# -------------------------------admin change password-----------------------------------------------------
def admin_update_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('user_login')

    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'admin_update_password.html', {'form': form,})

# -------------------------------admin change password-----------------------------------------------------
def user_update_password(request):
    user_list=User.objects.get(username=request.user)
    profile_info=Profile.objects.filter(user=request.user)
    if len(profile_info)==1:
        profile_info=Profile.objects.get(user=request.user)
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('user_login')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'user_update_password.html', {'form': form,'profile':profile_info,'data1':user_list})


def dashboard(request):
    profile_info=Profile.objects.filter(user=request.user)
    if len(profile_info)==1:
        profile_info=Profile.objects.get(user=request.user)
    return render(request,'dashboard_investment.html',{'profile':profile_info})



# -------------------------------------------dashboard incomesection-----------------------------------------------
def dashboard_investment(request):
# -----------------------------group by clause for My investment---------------------------
    results = My_Investment.objects.values('project_name').order_by('project_name').annotate(Total_investment=Sum('amount_invested'))
# ---------------------capture project name list-----------------------
    project_names=results.values('project_name')
    project_names_list=[]
    total_investment_projectwise=[]
    for i in results:
        project_names_list.append(i['project_name'])
        total_investment_projectwise.append(i['Total_investment'])
    print(project_names_list,total_investment_projectwise)
# -----------------------------group by clause for My Income---------------------------
    income = My_income.objects.values('username').order_by('username').annotate(Total_amt_received=Sum('amount_received'))
# ---------------------capture project name list-----------------------
    user_names=income.values('username')
    user_list=[]
    total_income_userwise=[]
    for i in income:
        user_list.append(i['username'])
        total_income_userwise.append(i['Total_amt_received'])
    print(user_list,total_income_userwise)

# ----------------profile pic-------------------------------------
    profile_info=Profile.objects.filter(user=request.user)
    if len(profile_info)==1:
        profile_info=Profile.objects.get(user=request.user)
    return render(request,'dashboard_investment.html',{'a':project_names_list,'b':total_investment_projectwise,'c':user_list,'d':total_income_userwise,'profile':profile_info})



def dashboard_income(request):
    
# -----------------------------group by clause for My investment---------------------------
    results = My_Investment.objects.values('project_name').order_by('project_name').annotate(Total_investment=Sum('amount_invested'))
# ---------------------capture project name list-----------------------
    project_names=results.values('project_name')
    project_names_list=[]
    total_investment_projectwise=[]
    for i in results:
        project_names_list.append(i['project_name'])
        total_investment_projectwise.append(i['Total_investment'])
    print(project_names_list,total_investment_projectwise)
# -----------------------------group by clause for My Income---------------------------
    income = My_income.objects.values('username').order_by('username').annotate(Total_amt_received=Sum('amount_received'))
# ---------------------capture project name list-----------------------
    user_names=income.values('username')
    user_list=[]
    total_income_userwise=[]
    for i in income:
        user_list.append(i['username'])
        total_income_userwise.append(i['Total_amt_received'])
    print(user_list,total_income_userwise)
    # -------------------------profile pic-------------------------------------
    profile_info=Profile.objects.filter(user=request.user)
    if len(profile_info)==1:
        profile_info=Profile.objects.get(user=request.user)    
    return render(request,'dashboard_income.html',{'a':project_names_list,'b':total_investment_projectwise,'c':user_list,'d':total_income_userwise,'profile':profile_info})




def demo(request):
    return render(request,'demo.html')