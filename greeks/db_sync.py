from kiteconnect import KiteConnect
from urllib.parse import urlencode
from .models import Instruments
import requests

class Syncing():
    """ This function should be called only on expiry day, it will sync data base with next month contract """
    def option_chain(token):
        kite = KiteConnect(api_key="XXXXXXXXXXX")
        kite.set_access_token(token["access_token"])
        response=kite.instruments()
        number=1
        for values in response:
            """ Storing the contract of banknifty """ 
            if (values['tradingsymbol'][0:9] == "BANKNIFTY"):
                         
                #November month bank nifty contract 
                #Checking the required common nomenclature for option contract and saving to DB 
                if(values['tradingsymbol'][9:14] == "17NOV"):
                    #storing CE and PE option contract in different database
                    if(values['tradingsymbol'][-2:] == "CE"):
                        feeding =Instruments(banknifty_latest_call=values['tradingsymbol'],banknifty_latestce_token=values['instrument_token'])
                        feeding.save()
                        number=number+1
                    if(values['tradingsymbol'][-2:] == "PE"):
                        feeding =Instruments(banknifty_latest_put=values['tradingsymbol'],banknifty_latestpe_token=values['instrument_token'])
                        feeding.save()
                        number=number+1


                #December month bank nifty contract     
                if(values['tradingsymbol'][9:14] == "17DEC"):
                    #storing CE and PE option contract in different database
                    if(values['tradingsymbol'][-2:] == "CE"):
                        feeding=Instruments(banknifty_next_call=values['tradingsymbol'],banknifty_nextce_token=values['instrument_token'])
                        feeding.save()
                        number=number+1
                    if(values['tradingsymbol'][-2:] == "PE"):
                        feeding =Instruments(banknifty_next_put=values['tradingsymbol'],banknifty_nextpe_token=values['instrument_token'])
                        feeding.save()
                        number=number+1

                #18January bank nifty contract
                if(values['tradingsymbol'][9:14] == "18JAN"):
                    if(values['tradingsymbol'][-2:] == "CE"):
                        feeding =Instruments(banknifty_last_call=values['tradingsymbol'],banknifty_lastce_token=values['instrument_token'])
                        feeding.save()
                        
                    if(values['tradingsymbol'][-2:] == "PE"):
                        feeding =Instruments(banknifty_last_put=values['tradingsymbol'],banknifty_lastpe_token=values['instrument_token'])
                        feeding.save()      

            """ Storing the Nifty contract """          
            if (values['tradingsymbol'][0:5] == "NIFTY"):

                # November month nifty contract 
                if(values['tradingsymbol'][5:10] == "17NOV"):
                    if(values['tradingsymbol'][-2:] == "CE"):
                        feeding =Instruments(nifty_latest_call=values['tradingsymbol'],nifty_latestce_token=values['instrument_token'])
                        feeding.save()
                        number=number+1
                    if(values['tradingsymbol'][-2:] == "PE"):
                        feeding =Instruments(nifty_latest_put=values['tradingsymbol'],nifty_latestpe_token=values['instrument_token'])
                        feeding.save()
                        number=number+1
                    

                # December month nifty contract 
                if(values['tradingsymbol'][5:10] == "17DEC"):
                    if(values['tradingsymbol'][-2:] == "CE"):
                        feeding =Instruments(nifty_next_call=values['tradingsymbol'],nifty_nextce_token=values['instrument_token'])
                        feeding.save()
                        number=number+1
                    if(values['tradingsymbol'][-2:] == "PE"):
                        feeding =Instruments(nifty_next_put=values['tradingsymbol'],nifty_nextpe_token=values['instrument_token'])
                        feeding.save()
                        number=number+1

                # 18January month nifty contract 
                if(values['tradingsymbol'][5:10] == "18JAN"):
                    if(values['tradingsymbol'][-2:] == "CE"):
                        feeding =Instruments(nifty_last_call=values['tradingsymbol'],nifty_lastce_token=values['instrument_token'])
                        feeding.save()
                        number=number+1
                    if(values['tradingsymbol'][-2:] == "PE"):
                        feeding =Instruments(nifty_last_put=values['tradingsymbol'],nifty_lastpe_token=values['instrument_token'])
                        feeding.save()
                        number=number+1        


        return HttpResponse('<h2>Data is synced</h2>')
