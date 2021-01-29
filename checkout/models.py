from django.db import models
from django.forms import ModelForm
from django.contrib.auth import get_user_model
# Create your models here.

# Get the user model
User = get_user_model()

class BillingAddress(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	address = models.CharField(max_length=100)
	zipcode = models.CharField(max_length=50)
	cellular = models.CharField(max_length=50)
	landmark = models.CharField(max_length=300)

	def __str__(self):
		return f'{self.user.username} billing address'

	class Meta:
		verbose_name_plural = "Billing Addresses"


# Address Form
class BillingForm(ModelForm):

	class Meta:
		model = BillingAddress
		fields = ['address', 'zipcode', 'cellular', 'landmark']
		labels = {
           'address': ('адрес'),'zipcode': ('почтовый индекс'),'cellular': ('номер телефона'),'landmark': ('ориентир'),
       }
		 