from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

# Get the user model
User = get_user_model()


# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.quantity} of {self.item.name}'

    def get_total(self):
        total = self.item.price * self.item.tirazh
        floattotal = float("{0:.2f}".format(total))
        return floattotal

# Order Model
class Order(models.Model):
    orderitems  = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=200, blank=True , null=True)
    orderId = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.user.username


    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
        #for order_item in self.cart.item.calc.all():
            total += order_item.get_total()
        
        return total

from django.utils import timezone
tz = timezone.get_default_timezone()

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'client_files/user_{0}/{1}'.format(instance.user.id, filename)


class File(models.Model):
    # file = models.ImageField(upload_to='media/client_files')
    # file = models.ImageField(upload_to=user_directory_path)
    file = models.FileField(upload_to=user_directory_path)
    # file = models.ImageField(upload_to='client_files/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # created = models.DateTimeField()
    # created_time = models.DateTimeField('Created Time', auto_now_add=True, null=True)
    created = models.DateTimeField('Created Time', auto_now_add=True)
    def __str__(self):
        return 'Заявка от {}'.format(self.created.astimezone(tz).strftime('%d.%m.%Y %H:%M'))

    # start = models.DateTimeField('Начало приёма') 
    # end = models.DateTimeField('Конец приёма', null=True, blank=True)