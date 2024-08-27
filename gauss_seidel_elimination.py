# -*- coding: utf-8 -*-
"""

@author: Sudipto3331
"""

##Import libraries as necessary
import numpy as np
import xlrd
from xlwt import Workbook
def brcond_Seidel(E,err,n):
    
    a=0
    for i in range(n):  
        if E[i]<err:
            a=a+1
    return a/n

#taking necessary input values from keyboard
err=float(input('Enter desired percentage relative error: '))
ite=int(input('Enter number of iterations: '))
relaxation=float(input('Enter relaxation factor: '))

#Reading data from excel file
loc = ('data.xls')

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(3)

n=sheet.nrows   #number of unknown variables
#Initialize variables
a=np.zeros([n,n+1])
E=np.zeros([n])
rel_err=np.zeros([ite,n])
X=np.zeros([n])
x=np.zeros([ite,n])
x_new=np.zeros([ite,n])
itern=np.zeros([ite])
p=np.zeros([n])

for i in range(sheet.ncols):
    for j in range(sheet.nrows):
        a[j,i]=sheet.cell_value(j, i)

#Iteration for Gauss Seidel begins here.
for j in range(ite):
    #storing the values of iteration
    itern[j]=j+1
             
    for i in range(n):
        summation=0
        
        for k in range(n):
            
            if k>i or k<i:
                summation=summation+a[i,k]*x[j,k]
        
        x_new[j,i]=(a[i,n]-summation)/a[i,i]   #Determining the values of unknown variables
        if j>0:
            x[j,i]=x_new[j,i]*relaxation+(1-relaxation)*x[j-1,i]   #Determining the values of unknown variables
        if j==0:
            x[j,i]=x_new[j,i]
            
        #Error calculation
        if j>0:
            rel_err[j,i]=((x[j,i]-x[j-1,i])/x[j,i])*100
            E[i]=rel_err[j,i]
    
    if j>0:
        Q=brcond_Seidel(E,err,n)
        
        if Q==1:
            break
    
    if j==ite-1:
        break
     
    x[j+1,:]=x[j,:]

num_of_iter=j
X=x[j,:]

print('The values of the unknown variables are respectively:')
print(X)

wb = Workbook()
  
# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('Sheet 1')

#writing on excel
sheet1.write(0,n,'Gauss')
sheet1.write(0,n+1,'Seidel')
sheet1.write(1,0,'Number of iteration')

for i in range(1,n+1):
    sheet1.write(1,i,'x_'+str(i))
    
for i in range(n+1,2*n+1):
    sheet1.write(1,i,'Relative error of x_'+str(i-n))

for i in range(num_of_iter+1):
    
    sheet1.write(i+2,0,itern[i])
    for j in range(n):
        sheet1.write(i+2,1+j,x[i,j])
        sheet1.write(i+2,n+1+j,rel_err[i,j])
   
sheet1.write(i+4,0,'The')
sheet1.write(i+4,1,'unknown')
sheet1.write(i+4,2,'values')
sheet1.write(i+4,3,'are:')
for k in range(n):
    sheet1.write(i+4,k+4,X[k])

#save the excel file
wb.save('xlwt example.xls')

#Result Verification    
for i in range(n):
    summation=0
    for j in range(n):
        summation=summation+a[i,j]*X[j]
    
    p[i]=summation-a[i,j+1]
    
#The implementation is corrct if verification results are all zero
print('The verification results are:')
print(p)
print('The implementation is corrct if verification results are all zero')
