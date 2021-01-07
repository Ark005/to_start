from django.db import models
from django.urls import reverse
from datetime import datetime, timedelta


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=300)
    primaryCategory = models.BooleanField(default=False)
    mainimage = models.ImageField(upload_to='products/', blank=True)
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class SubCategory(models.Model):
    name = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    mainimage = models.ImageField(upload_to='products/', blank=True)
    
    def __str__(self):
        return self.name

from polymorphic.models import PolymorphicModel

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
                ('60х60х40-P', '60х60х40-P'),
                ('80х80х40', '80х80х40'),
                ('80х80х40-P', '80х80х40-P'),
                ('240х185х120', '240х185х120'),
                ('270х220х70', '270х220х70'),
                )

    mainimage = models.ImageField(upload_to='products/', blank=True, null=True)
    name = models.CharField(max_length=300, default = None, null=True)
    slug = models.SlugField(default = None, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, default = None, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default = None, null=True)
    preview_text = models.TextField(max_length=200, verbose_name='Preview Text', blank=True, null=True)
    detail_text = models.TextField(max_length=1000, verbose_name='Detail Text', blank=True, null=True)
    price = models.FloatField(default = None, null=True)
    tirazh = models.IntegerField(null=False)
    t = models.IntegerField(null=True)
    #t =  models.DateField(auto_now=False, auto_now_add= False)
    box_size = models.CharField(max_length=20, choices=BOX_SIZES,default='80х80х40')



    def timeplus(self):

        t = self.t
    
        futuredate = datetime.now() + timedelta(days=t)

        return futuredate 
    
    # Модель в методе save при сохранении объекта автоматически удаляет все остальные, 
    # что позволяет держать в базее данных всегда только один экземпляр данной модели.

    # Метод load берёт из базы данных то единственный объект настроек, если же объект 
    # не существует в базе данных, то возвращает новый инстанс этой модели, 
    # который нужно будет потом сохранить.


    
    def get_cost(self):
        a =(176.3969+17367.3469/self.tirazh)*self.tirazh
        
        return "{0:.2f}".format(round(a,0))


    def ret(request):
        all_result =Product.objects.all()
        result_one = all_result.filter(box_size ='50х50х35')
        result_two = all_result.filter(box_size ='60х60х40')
        result_three = all_result.filter(box_size ='80х80х40')
        result_four = all_result.filter(box_size ='60х60х40-P')
        result_five = all_result.filter(box_size ='80х80х40-P')
        result_six = all_result.filter(box_size ='240х185х120')
        result_seven = all_result.filter(box_size ='270х220х70')

        if result_one:
            return  3935428.2860 # 50х50х35 крышка-дно, сборка на автомат от 2500 шт
        elif  result_two:
            return 2560787.2222  # 60x60x40 крышка-дно, сборка на автомат от 2500 шт
        elif  result_three:
            return 2230289.1977  # 80х80х40 крышка-дно, сборка на автомат от 2500 шт  

        elif  result_four:
            return 2642166.1889  # 60x60x40 крышка-дно-поясок, сборка на автомат от 2500 шт
        elif  result_five:
            return 2248996.1600 # 224.8996x−0.1600 80х80х40 крышка-дно-поясок, сборка на автомат от 2500 шт
        
        elif  result_six:
            return 10780131.2554 # размер 240х185х120 мм ручная сборка    
        
        elif  result_seven:
            return 7799003.1669 # размер 270х220х70 мм ручная сборка y=779.9003x−0.1669

        else:
            return 0


class BoxType1(Product):
    """docstring for BoxType1"""

    BOX_SIZES = (
            ('240х185х120', '240х185х120'),
            ('270х220х70', '270х220х70'),
            )

    # box_size = models.CharField(max_length=20, choices=BOX_SIZES,default='80х80х40')

class BoxType2(Product):
    """docstring for BoxType1"""
    
    BOX_SIZES = (
            ('50х50х35', '50х50х35'),
            ('60х60х40', '60х60х40'),
            )

    # box_size = models.CharField(max_length=20, choices=BOX_SIZES,default='80х80х40')


        

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

class Friend(models.Model):

    dob = models.DateField(auto_now=False, auto_now_add=False)
    tirazh = models.IntegerField(null=False)

    def __str__(self):
        return self.nick_name


    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(Friend, self).save(*args, **kwargs)
 
    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()













