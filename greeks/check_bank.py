from kiteconnect import KiteConnect
import collections
from urllib.parse import urlencode
import requests
import time
import mibian
import datetime

class Checking1():

		def calculation(self,bank,bank_next,check,cont):	
			nov_token=[]
			day_expiry=0
			#Get today's date for calculating time left to expire for using in BS calculator
			d0=datetime.date.today()
			# Making list helps in extracting the required values through API call
			for value in bank:
				if(cont==1):	
					nov_token.append(value.banknifty_latest_call)
					d1=datetime.date(2017,11,30)
						# for calculating the time difference w.r.t expiry date for november contract
					day_expiry=d1-d0
					day_expiry=day_expiry.days
				if(cont==2):	
					nov_token.append(value.banknifty_next_call)
					d1=datetime.date(2017,12,28)
						# for calculating the time difference w.r.t expiry date for november contract
					day_expiry=d1-d0
					day_expiry=day_expiry.days 
				if(cont==3):	
					nov_token.append(value.banknifty_last_call)
					d1=datetime.date(2018,1,25)
						# for calculating the time difference w.r.t expiry date for november contract
					day_expiry=d1-d0
					day_expiry=day_expiry.days 		           
			nov_token3=[]		
			for value in bank_next:
				if(cont==1):
					nov_token3.append(value.banknifty_latest_put)
				if(cont==2):
					nov_token3.append(value.banknifty_next_put)
				if(cont==3):
					nov_token3.append(value.banknifty_last_put)	
			nov_token1,nov_token2,nov_change1,nov_change2,nov_open1,nov_open2,options=([] for i in range(7))		
			nov_token_final=nov_token1,nov_token2
			nov_token_final1=[nov_change1,nov_change2]
			nov_token_final2=[nov_open1,nov_open2]
			nov_token_list=[nov_token,nov_token3]
	        #Getting Nifty Bank spot, close value for input in BS calculator			
			url_code1='https://api.kite.trade/instruments/NSE/'
			encoded_args= urlencode([('api_key', 'blwekjvno83ep8vo'), ('access_token',check["access_token"])])
			result = url_code1+'NIFTY BANK'+'?'+encoded_args
			response1 = requests.get(result).json()
			count=0
			for checklist in nov_token_list:
				url_code='https://api.kite.trade/instruments/NFO/'
				for item in checklist:
					result = url_code+item+'?'+encoded_args
					response = requests.get(result).json()
					nov_token_final[count].append(response['data']['last_price'])
					nov_token_final1[count].append(response['data']['change_percent'])
					nov_token_final2[count].append(response['data']['open_interest'])
	                #Input the required paramter to BS calculator
					options.append(mibian.BS([response1['data']['close'],item[14:-2],6,day_expiry],volatility=20))
					time.sleep(0.75)
				count=count+1 
				# found namedtuple , best as per requirement.There are other ways also 	
			Point = collections.namedtuple('Point', ['a','b','c','d','e','f','g','h','i'])
			p = Point(nov_change1,nov_change2,bank_next,nov_token1,nov_token2,bank,nov_open1,nov_open2,options)
			return p		           