
from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.conf import settings

# Create your models here.


land_p=[('Not Started','Not Started'),('In Progress','In Progress'),('Completed','Completed')]
dev=[('Not Started','Not Started'),('In Progress','In Progress'),('Completed','Completed')]
sales=[('Not Started','Not Started'),('In Progress','In Progress'),('Completed','Completed')]
class Project(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    project_name=models.CharField(max_length=100)
    proposer=models.CharField(max_length=100)
    project_manager=models.CharField(max_length=100)
    brief_desc=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    locality=models.CharField(max_length=100)
    Projected_ROI=models.CharField(max_length=100)
    start_date=models.CharField(max_length=100)
    location_link=models.CharField(max_length=100)
    expected_duration=models.CharField(max_length=100)
    min_investment=models.CharField(max_length=100)
    Investment_till_date=models.CharField(max_length=100)
    total_investment=models.CharField(max_length=100)
    land_purchased=models.CharField(max_length=20,choices=land_p)
    development=models.CharField(max_length=20,choices=dev)
    sales=models.CharField(max_length=20,choices=sales)
    detail_desc=models.TextField(max_length=1000)
    
    def __str__(self):
        return '{}'.format(self.project_name)   
    
class Image(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    image=models.FileField(upload_to='Project_img',null=True,default=None)


class My_Investment(models.Model):
    amount_invested=models.CharField(max_length=20,default='00')
    amount_received=models.CharField(max_length=20,default='00')
    roi=models.CharField(max_length=10)
    date_of_invested = models.DateField(auto_now_add=True)
    date_of_received = models.CharField(max_length=30)
    project_name=models.CharField(max_length=100)
    username=models.CharField(max_length=20)
    def __str__(self):
        return '{} {} {}'.format(self.id,self.username,self.project_name)     
class My_income(models.Model):
    amount_received=models.CharField(max_length=20,default='00')
    date=models.CharField(max_length=20)
    username=models.CharField(max_length=20)
    project_name=models.CharField(max_length=100)

    def __str__(self):
        return '{} {}'.format(self.username,self.amount_received)     


class Profile(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    phone_no=models.CharField(max_length=10)
    address_line1=models.CharField(max_length=30)
    address_line2=models.CharField(max_length=30)
    pincode=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    country=models.CharField(max_length=30)
    image=models.ImageField(upload_to='profile',null=True,default='default.jpg')
    activate_flag=models.CharField(max_length=10,default='0')
    # def __str__(self):
    #     return self.user.username 
        # return f'{self.user.username} Profile '
