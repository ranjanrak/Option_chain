from django.conf.urls import url
from . import views
from daychangers.views import work
from django.conf import settings

app_name = 'daychangers'

urlpatterns = [	
    url(r'^nifty_latest/$',work.nifty_latest, name='nifty_latest'),
    url(r'^nifty_next/$',work.nifty_next, name='nifty_next'),
    url(r'^nifty_last/$',work.nifty_last, name='nifty_last'),
    url(r'^bank_latest/$',work.bank_latest, name='bank_latest'),
    url(r'^bank_next/$',work.bank_next, name='bank_next'),
    url(r'^bank_last/$',work.bank_last, name='bank_last'),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)