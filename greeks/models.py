from django.db import models

class Instruments(models.Model):
	#Specific month contract will be stored in column with nomenclature like nifty_latest_call,banknifty_latest_put
	#Storing instrument token number for retriving market depth details using Web socket,saved by having nomenclature like nifty_latestce_token
	nifty_latest_call=models.CharField(max_length=100,null=True)
	nifty_latestce_token=models.IntegerField(null=True)
	nifty_latest_put=models.CharField(max_length=100,null=True)
	nifty_latestpe_token=models.IntegerField(null=True)
	nifty_next_call=models.CharField(max_length=100,null=True)
	nifty_nextce_token=models.IntegerField(null=True)
	nifty_next_put=models.CharField(max_length=100,null=True)
	nifty_nextpe_token=models.IntegerField(null=True)
	nifty_last_call=models.CharField(max_length=100,null=True)
	nifty_lastce_token=models.IntegerField(null=True)
	nifty_last_put=models.CharField(max_length=100,null=True)
	nifty_lastpe_token=models.IntegerField(null=True)
	banknifty_latest_call=models.CharField(max_length=100,null=True)
	banknifty_latestce_token=models.IntegerField(null=True)
	banknifty_latest_put=models.CharField(max_length=100,null=True)
	banknifty_latestpe_token=models.IntegerField(null=True)
	banknifty_next_call=models.CharField(max_length=100,null=True)
	banknifty_nextce_token=models.IntegerField(null=True)
	banknifty_next_put=models.CharField(max_length=100,null=True)
	banknifty_nextpe_token=models.IntegerField(null=True)
	banknifty_last_call=models.CharField(max_length=100,null=True)
	banknifty_lastce_token=models.IntegerField(null=True)
	banknifty_last_put=	models.CharField(max_length=100,null=True)
	banknifty_lastpe_token=models.IntegerField(null=True)
