from django.shortcuts import render
from django.conf import settings
from urllib.request import build_opener, HTTPCookieProcessor, Request
from django.shortcuts import get_object_or_404,redirect
from .models import Instruments
from urllib.parse import urlencode
from django.views.generic import View
from .check_list import Checking
from .check_bank import Checking1
from kiteconnect import KiteConnect
from kiteconnect import WebSocket
import requests
import json
import collections

class work(View):

	def login_test(request):
	 	""" Login though kite button """
	 	#this is the initial landing page
        x = request.GET.get('status', '')
        if x == "success":
            token = request.GET.get('request_token','None')
            kite = KiteConnect(api_key="blwekjvno83ep8vo")
            
            try:
                user = kite.request_access_token(request_token=token,secret="0hivw5gapvrv5y5stye56mm2w2pvktvr")
                kite.set_access_token(user["access_token"])
                #Using django session to store login user info
                #session date will be moved to other views as per requirement 
                request.session['token no']=user
            except:
                return render(request, 'daychangers/logtest.html',{'reason':'Authentication failed'})
            
            return render(request, 'daychangers/logtest1.html',{'specific':user} )
        else:
            return render(request, 'daychangers/login.html')

    #Creating individual view for every month contract for time being
    def nifty_latest(request):
        """ Page re-directed to after successful login through kite """
        #Retriving the access_token
        check=request.session['token no']
        #If there is post request from option form, below condition will be checked and redirected to required views
        if request.method == "POST":        
            contract= request.POST['contract']
            month=request.POST['month']

            if(contract=="nifty" and month=="november"):
                return redirect('http://127.0.0.1:8000/nifty_latest/')

            if(contract=="nifty" and month=="december"):
                return redirect('http://127.0.0.1:8000/nifty_next/')

            if(contract=="nifty" and month=="jan"):
                return redirect('http://127.0.0.1:8000/nifty_last/')           

            if(contract=="banknifty" and month=="november"):
                return redirect('http://127.0.0.1:8000/bank_latest/')

            if(contract=="banknifty" and month=="december"):
                return redirect('http://127.0.0.1:8000/bank_next/')      
                    
            if(contract=="banknifty" and month=="jan"):
                return redirect('http://127.0.0.1:8000/bank_last/')

        #Getting top 22 contract(11 in-the-money and 11 out-of-the-money) nearest to index spot , list can be increased as per requirement
        #slicing the database to get only the required 22 contract
        #Had to divide the database in 2 parts, because of 4(9900) and 5 digit(10000) discrepancy
        nifty1 =Instruments.objects.order_by('nifty_latest_call')[65:75]
        nifty1_next=Instruments.objects.order_by('nifty_latest_call')[:11]
        nifty2 = Instruments.objects.order_by('nifty_latest_put')[65:75]
        nifty2_next=Instruments.objects.order_by('nifty_latest_put')[:11]
        #importing the fucntion, which has the required value for option contract , needed for formation of option chain
        easy=Checking()
        value=easy.calculation(nifty1,nifty1_next,nifty2,nifty2_next,check,cont=1)
        return render(request,'daychangers/test.html',{'nov_change1':value[0],'nov_change2':value[1], 'nov_token':value[2], 'nifty1':value[3],
        'nifty1_next':value[4],'nov_token2':value[5], 'nifty2_next':value[9],'nifty2':value[8],'nov_open1':value[6],'nov_open2':value[7],'month':"November",'options':value[10]}) 

    def nifty_next(request):
        """ Getting top 22 contract(11 in-the-money and 11 out-of-the-money) nearest to index spot , list can be increased as per requirement """
        #slicing the database to get only the required 22 contract
        #Had to divide the database in 2 parts, because of 4(9900) and 5 digit(10000) discrepancy
        check=request.session['token no']         
        nifty1 =Instruments.objects.order_by('nifty_next_call')[120:130]
        nifty1_next=Instruments.objects.order_by('nifty_next_call')[:11]
        nifty2 = Instruments.objects.order_by('nifty_next_put')[120:130]
        nifty2_next=Instruments.objects.order_by('nifty_next_put')[:11]      
        easy=Checking()
        value=easy.calculation(nifty1,nifty1_next,nifty2,nifty2_next,check,cont=2)
        return render(request,'daychangers/test.html',{'nov_change1':value[0],'nov_change2':value[1], 'nov_token':value[2], 'nifty1':value[3],
        'nifty1_next':value[4],'nov_token2':value[5], 'nifty2_next':value[9],'nifty2':value[8],'nov_open1':value[6],'nov_open2':value[7],'month':"December",'options':value[10]})         

    def nifty_last(request):
        """ Getting top 22 contract(11 in-the-money and 11 out-of-the-money) nearest to index spot , list can be increased as per requirement """
        #Same as above no different just different month contract
        check=request.session['token no'] 
        nifty1 =Instruments.objects.order_by('nifty_last_call')[54:64]
        nifty1_next=Instruments.objects.order_by('nifty_last_call')[:11]
        nifty2 = Instruments.objects.order_by('nifty_last_put')[54:64]
        nifty2_next=Instruments.objects.order_by('nifty_last_put')[:11]      
        easy=Checking()
        value=easy.calculation(nifty1,nifty1_next,nifty2,nifty2_next,check,cont=3)
        return render(request,'daychangers/test.html',{'nov_change1':value[0],'nov_change2':value[1], 'nov_token':value[2], 'nifty1':value[3],
        'nifty1_next':value[4],'nov_token2':value[5], 'nifty2_next':value[9],'nifty2':value[8],'nov_open1':value[6],'nov_open2':value[7],'month':"Jan",'options':value[10]}) 

    def nifty_chain(request):
        return render(request,'daychangers/test1.html')

    def bank_latest(request):
        """ Getting top 20 contract(10 in-the-money and 10 out-of-the-money) nearest to index spot , list can be increased as per requirement """
        #Unlike nifty, no need to divide DB in 2 parts as all contracts are 5 digit(25000)
        check=request.session['token no']
        #Slice database to get only top 20 contracts
        bank1=Instruments.objects.order_by('banknifty_latest_call')[23:44]
        bank2=Instruments.objects.order_by('banknifty_latest_put')[23:44]
        easy=Checking1()
        #Passing value to required function to get values for formation of option chain
        value=easy.calculation(bank1,bank2,check,cont=1)
        return render(request,'daychangers/test_bank.html',{'nov_change1':value[0],'nov_change2':value[1], 'nov_token':value[2], 'nifty1':value[3],
            'nov_token2':value[4], 'nifty2':value[5],'nov_open1':value[6],'nov_open2':value[7],'options':value[8],'month':"November"})

    def bank_next(request):
        """ Getting top 20 contract(10 in-the-money and 10 out-of-the-money) nearest to index spot , list can be increased as per requirement """
        #same as above just,next month expiry contract
        check=request.session['token no']
        bank1=Instruments.objects.order_by('banknifty_next_call')[23:44]
        bank2=Instruments.objects.order_by('banknifty_next_put')[23:44]
        easy=Checking1()
        value=easy.calculation(bank1,bank2,check,cont=2)
        return render(request,'daychangers/test_bank.html',{'nov_change1':value[0],'nov_change2':value[1], 'nov_token':value[2], 'nifty1':value[3],
            'nov_token2':value[4], 'nifty2':value[5],'nov_open1':value[6],'nov_open2':value[7],'options':value[8],'month':"December"})

    def bank_last(request):
        """ Getting top 20 contract(10 in-the-money and 10 out-of-the-money) nearest to index spot , list can be increased as per requirement """
        #same as above ,far month contract
        check=request.session['token no']
        bank1=Instruments.objects.order_by('banknifty_last_call')[13:34]
        bank2=Instruments.objects.order_by('banknifty_last_put')[13:34]
        easy=Checking1()
        value=easy.calculation(bank1,bank2,check,cont=3)
        return render(request,'daychangers/test_bank.html',{'nov_change1':value[0],'nov_change2':value[1], 'nov_token':value[2], 'nifty1':value[3],
            'nov_token2':value[4], 'nifty2':value[5],'nov_open1':value[6],'nov_open2':value[7],'options':value[8],'month':"Jan"})         