from django.db import models
from django.urls import reverse
from datetime import datetime, timedelta


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=300)
    primaryCategory = models.BooleanField(default=False)
    mainimage = models.ImageField(upload_to='products/', blank=True)
    preview_text = models.TextField(max_length= 60 , verbose_name='Preview Text', blank=True, null=True)
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class SubCategory(models.Model):
    name = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    mainimage = models.ImageField(upload_to='products/', blank=True)
    preview_text = models.TextField(max_length= 60 , verbose_name='Preview Text', blank=True, null=True)
    
    def __str__(self):
        return self.name

from polymorphic.models import PolymorphicModel

from django.utils.translation import gettext_lazy as _




#Product Model
# class  Product(models.Model):
class  Product(PolymorphicModel):


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse("mainapp:product", kwargs={
            'slug': self.slug
        })

    # def save(self, *args, **kwargs):
    #     self.__class__.objects.exclude(id=self.id).delete()
    #     super(Product, self).save(*args, **kwargs)
 
    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

    BOX_SIZES = (
                ('50х50х35', '50х50х35'),
                ('60х60х40', '60х60х40'),
                ('80х80х40', '80х80х40'),
                ('240х185х120', '240х185х120'),
                ('270х220х70', '270х220х70'),
                ('корешок 25-40 круглый механизм 7200', 'корешок 25-40 круглый механизм 7200'),
                ('корешок 45-65 д-образный механизм', 'корешок 45-65 д-образный механизм'),
                )
    
   


    mainimage = models.ImageField(upload_to='products/', blank=True, null=True)
    name = models.CharField(max_length=300, default = None, null=True)
    slug = models.SlugField(default = None, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, default = None, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default = None, null=True)
    preview_text = models.TextField(max_length=50, verbose_name='Preview Text', blank=True, null=True)
    detail_text = models.TextField(max_length=1000, verbose_name='Detail Text', blank=True, null=True)
    price = models.FloatField(default = None, null=True)
    tirazh = models.IntegerField(null=False)
    t = models.IntegerField(null=True)
    k = models.FloatField(default = None, null=True)
    box_size = models.CharField(max_length=50)
    

    def timeplus(self):

        t = self.t
    
        futuredate = datetime.now() + timedelta(days=t)

        return futuredate 
    
    # Модель в методе save при сохранении объекта автоматически удаляет все остальные, 
    # что позволяет держать в базее данных всегда только один экземпляр данной модели.

    # Метод load берёт из базы данных то единственный объект настроек, если же объект 
    # не существует в базе данных, то возвращает новый инстанс этой модели, 
    # который нужно будет потом сохранить.


    def calc(self):

        boxsize = self.boxsizes_set.get(value = self.box_size)

        a = float(boxsize.k*self.tirazh**boxsize.b)*self.k

        return "{0:.2f}".format(round(a,0))

"""
        def get_total(self):
        total = int(self.item.calc())
        #floattotal = float("{0:.2f}".format(total))
        return total #floattotal

        return "{0:.2f}".format(round(a,0))
"""
class BoxSizes(models.Model):
    value = models.CharField(max_length=80)
    name = models.CharField(max_length=80)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null = True, blank = True)
    # к - первый коэффициент
    k = models.FloatField(null = True, blank = True)
    # b - второй коэффициент
    b = models.FloatField(null = True, blank = True)

    def __str__(self):
        # return self.name
        return '  {} {}_{}'.format(self.value, self.product.name, self.product.id)
       



class BoxType1(Product):
    """docstring for BoxType1"""

    def __init__(self, *args, **kwargs):
  
        super(BoxType1, self).__init__(*args, **kwargs)
    


class BoxType2(Product):
    """docstring for BoxType1"""

    def __init__(self, *args, **kwargs):
       
        super(BoxType2, self).__init__(*args, **kwargs)
    


class FolderType1(Product):
    """docstring for BoxType1"""

    def __init__(self, *args, **kwargs):

        super(FolderType1, self).__init__(*args, **kwargs)



class FolderType2(Product):
    """docstring for BoxType1"""

    def __init__(self, *args, **kwargs):
 
        super(FolderType2, self).__init__(*args, **kwargs)

class Note1 (Product):

    def __init__(self, *args, **kwargs):
     
        super(Note1, self).__init__(*args, **kwargs)

class Note2 (Product):

    def __init__(self, *args, **kwargs):
     
        super(Note2, self).__init__(*args, **kwargs)

from django.core.validators import int_list_validator

class Test(PolymorphicModel):
    BOX_SIZES = (
         
                ('240х185х120', '240х185х120'),
                ('270х220х70', '270х220х70'),
                )

    name = models.CharField(max_length=40)
    # dob = models.DateField(verbose_name='Date of birth')
    box_size = models.CharField(max_length=50, choices=BOX_SIZES,default='80х80х40')
    # int_list = models.CharField(validators=int_list_validator)
    int_list = models.CharField(validators=[int_list_validator], max_length=100)




'''
class Payment(models.Model):
    event_date = models.DateField()
    payment_due_date = models.DateField()

    class Meta:
        ordering = ["payment_due_date"]

    def save(self, *args, **kwargs):
        if self.payment_due_date is None:
            self.payment_due_date = self.event_date.date() + datetime.timedelta(days=2)
        super(Payment, self).save(*args, **kwargs)


'''
class Post(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='client_files/')
 
    def __str__(self):
        return self.title

class BoxSizes(models.Model):
    mainimage = models.ImageField(upload_to='products/', blank=True, null=True)
    value = models.CharField(max_length=80)
    name = models.CharField(max_length=80)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null = True, blank = True)
    # к - первый коэффициент
    k = models.FloatField(null = True, blank = True)
    # b - второй коэффициент
    b = models.FloatField(null = True, blank = True)

    def __str__(self):
        # return self.name
        return '  {} {}_{}'.format(self.value, self.product.name, self.product.id)

        #return "{0:.0f}".format(round(a,0))















