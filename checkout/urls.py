from django.urls import path 
from . views import checkout, payment, charge, oderView, send_email

app_name = "checkout"

urlpatterns = [
	path('checkout/', checkout, name="index"),
	path('payment/', payment, name="payment"),
	path('charge/', charge, name="charge"),
	path('my-orders/', oderView, name="oderView"),
	path('send_email/', send_email, name='send_email'),
]