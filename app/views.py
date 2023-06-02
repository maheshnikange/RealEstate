from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import SignUpForm,add_project_form,ImageForm,userUpdateForm,ProfileForm
from django.contrib.auth.models import User
from .models import Project,Image,My_income,My_Investment,Profile
import os
from django.db.models import Q

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
        form = SignUpForm(request.POST)
        # form=UserReg  istrationForm(request.POST)
        print('---------')
        if form.is_valid():
            print('----111111-----')
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
            # form=UserRegistrationForm()
            return render(request,'0signup.html',{'form': form})
    else:
        # form = SignUpForm()
        form=SignUpForm()
        return render(request,'signup.html',{'form': form})
# ----------------------------------------------------------------------
def admin_homepage(request):
    Project_list=Project.objects.all()
    user_list=User.objects.get(username=request.user)

    return render(request,'admin_homepage.html',{'data':Project_list})    
# --------------------admin about us------------------------------------
def admin_about_us(request):
    data=Project.objects.all()
    return render(request,'admin_about_us.html')



# --------------------User list------------------------------------------
def user_details(request):
    users=User.objects.all()
    print(users,'-----------')
    return render(request,'user_details.html',{'users':users})
# -----------------------------Projects--------------------------
def project(request):
    data=Project.objects.all()
    return render(request,'projects.html',{'data':data})

# ----------------------add project--------------------------
def add_project(request):
    if request.method=='POST':
        print('******************')
        form=add_project_form(request.POST)
        files=request.FILES.getlist('image')
        print(files,'---------')
        if form.is_valid():
            f=form.save(commit=False)
            f.save()
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
    project_data=Project.objects.all()
    return render(request,'user_homepage.html',{'data':project_data})

def user_about_us(request):
    return render(request,'user_about_us.html')
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
    return render(request,'payment_received.html',{'data':data,'flag':''})
# ---------------------------payment made---------------------------------
def payment_made(request):
    data=My_income.objects.all()
    return render(request,'payment_made.html',{'data':data})
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
        # dd/mm/YY
        d1 = today.strftime("%d/%m/%Y")
        p=My_income(project_name=project_name,username=user_name,amount_received=amount,date=d1)
        p.save()
        
        amt=My_Investment.objects.filter(Q(project_name=project_name) & Q(username=user_name)).values('amount_received')[0]
        print(amt['amount_received'],'---------pppppppp')
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
        return render(request,'user_my_investment.html',{'data1':data1})
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
def user_my_investment_detail(request,id):
    print(request.user,id,'-----------------------')
    data_for_project_name=My_income.objects.filter(username=request.user).values('project_name')[0]
    print(data_for_project_name)
    data1=My_Investment.objects.filter(username=request.user)
    data=My_income.objects.filter(username=request.user)
    return render(request,'user_my_investment_detail.html',{'data':data,'data1':data1,'project':data_for_project_name})
# ---------------------update project------------------------------------------------------
def update_project(request,id):
    if request.method=='POST':
        data=Project.objects.get(id=id)
        data=Project.objects.get(id=id)

        fm=add_project_form(request.POST,request.FILES, instance=data)
        if fm.is_valid():
            fm.save()
            data=Project.objects.all()
            return render(request,'admin_homepage.html',{'data':data})
    else:
        data=Project.objects.get(id=id)
        fm=add_project_form(instance=data)
        img1=ImageForm(instance=data)
    return render(request,'update_project.html',{'form':fm,'img1':img1})
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
