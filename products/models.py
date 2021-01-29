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
                ('60х60х40-P', '60х60х40-P'),
                ('80х80х40', '80х80х40'),
                ('80х80х40-P', '80х80х40-P'),
                ('240х185х120', '240х185х120'),
                ('270х220х70', '270х220х70'),
                ('корешок 25-40 круглый механизм 7200', 'корешок 25-40 круглый механизм 7200'),
                ('корешок 45-65 д-образный механизм', 'корешок 45-65 д-образный механизм'),
                )
    
   

    # class BOX_SIZES(models.TextChoices):
    #     size1 = '270х220х70', _('270х220х70')

    #     class Meta:
    #         abstract = True

    # BOX_SIZES = None
    # BOX_SIZES = (
    #     ('50х50х35', '50х50х35'),
    #     )

    # @property
    # def box_sizes(self):
    #    return self.BOX_SIZES



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
    k = models.IntegerField(null=True)
    #t =  models.DateField(auto_now=False, auto_now_add= False)
    # box_size = models.CharField(max_length=50, choices=BOX_SIZES,default='80х80х40')
    box_size = models.CharField(max_length=50, default='80х80х40')
    

    # box_size = models.CharField(max_length=48, choices=BOX_SIZES.choices, default='80х80х40')

    def koef(self):

         k = self.k
         kprice = k * price()

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
   

       

    def calc(self):
        tirazh = self.tirazh
        all_result =Product.objects.all()
        result_one = all_result.filter(box_size ='50х50х35')
        result_two = all_result.filter(box_size ='60х60х40')
        result_three = all_result.filter(box_size ='80х80х40')
        result_four = all_result.filter(box_size ='60х60х40-P')
        result_five = all_result.filter(box_size ='80х80х40-P')
        result_six = all_result.filter(box_size ='240х185х120')
        result_seven = all_result.filter(box_size ='270х220х70')
        result_eight = all_result.filter(box_size ='корешок 25-40 круглый механизм 7200')
        result_nine = all_result.filter(box_size ='корешок 45-65 д-образный механизм')

        if result_one:
            a = 39.35428* self.tirazh ** 0.2860
            #return  3935428.2860 + self.tirazh # 50х50х35 крышка-дно, сборка на автомат от 2500 шт
            return "{0:.0f}".format(round(a,0)) # 50х50х35 крышка-дно, сборка на автомат от 2500 шт
        elif  result_two:
            a = 2560787.2222
            return  "{0:.0f}".format(round(a,0)) # 60x60x40 крышка-дно, сборка на автомат от 2500 шт
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

        elif  result_eight:
            a = (59.35428* self.tirazh) ** 0.2860
       
            return "{0:.0f}".format(round(a,0))
        elif  result_nine:

            a = (39.35428* self.tirazh) ** 0.2860

            return "{0:.0f}".format(round(a,0))
        else:
            return 0

    # class Meta:
    #     abstract = True


class BoxType1(Product):
    """docstring for BoxType1"""

    def __init__(self, *args, **kwargs):
        # BOX_SIZES = (
        #     ('240х185х120', '240х185х120'),
        #     ('270х220х70', '270х220х70'),
        #     )

        # self._meta.get_field('box_size').default  = '240х185х120'
        # self._meta.get_field('box_size').choices = BOX_SIZES
        super(BoxType1, self).__init__(*args, **kwargs)
    
    # class Meta:
    #     proxy = True


    # class BOX_SIZES(models.TextChoices):
    #     size1 = '240х185х120', _('240х185х120')

    # box_size = models.CharField(max_length=20, choices=BOX_SIZES,default='240х185х120')


class BoxType2(Product):
    """docstring for BoxType1"""

    def __init__(self, *args, **kwargs):
        # BOX_SIZES = (
        #     ('50х50х35', '50х50х35'),
        #     ('60х60х40', '60х60х40'),
        #     )

        # self._meta.get_field('box_size').default  = '270х220х70'
        # self._meta.get_field('box_size').choices = BOX_SIZES
        super(BoxType2, self).__init__(*args, **kwargs)
    
    # BOX_SIZES = (
    #         ('50х50х35', '50х50х35'),
    #         ('60х60х40', '60х60х40'),
    #         )

    # class BOX_SIZES(models.TextChoices):
    #     size1 = '50х50х35', _('50х50х35')
    # box_size = models.CharField(max_length=20, choices=BOX_SIZES,default='50х50х35')

class FolderType1(Product):
    """docstring for BoxType1"""

    def __init__(self, *args, **kwargs):
        # BOX_SIZES = (
        #     ('корешок 25-40 круглый механизм 7200', 'корешок 25-40 круглый механизм 7200'),
        #     ('корешок 45-65 д-образный механизм', 'корешок 45-65 д-образный механизм'),
        #     )

        # self._meta.get_field('box_size').default  = 'корешок 25-40 круглый механизм 7200'
        # self._meta.get_field('box_size').choices = BOX_SIZES
        super(FolderType1, self).__init__(*args, **kwargs)



class FolderType2(Product):
    """docstring for BoxType1"""

    def __init__(self, *args, **kwargs):
        # BOX_SIZES = (
        #     ('корешок 25-40 круглый механизм 7200', 'корешок 25-40 круглый механизм 7200'),
        #     ('корешок 45-65 д-образный механизм', 'корешок 45-65 д-образный механизм'),
        #     )

        # self._meta.get_field('box_size').default  = 'корешок 25-40 круглый механизм 7200'
        # self._meta.get_field('box_size').choices = BOX_SIZES
        super(FolderType2, self).__init__(*args, **kwargs)



class BoxSizes(models.Model):
    value = models.CharField(max_length=80)
    name = models.CharField(max_length=80)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null = True, blank = True)

    def __str__(self):
        # return self.name
        return '  {} {}_{}'.format(self.value, self.product.name, self.product.id)



# return 'Заявка от {}'.format(self.created.astimezone(tz).strftime('%d.%m.%Y %H:%M'))

# BOX_SIZES = (
#                 ('50х50х35', '50х50х35'),
#                 ('60х60х40', '60х60х40'),
#                 ('60х60х40-P', '60х60х40-P'),
#                 ('80х80х40', '80х80х40'),
#                 ('80х80х40-P', '80х80х40-P'),
#                 ('240х185х120', '240х185х120'),
#                 ('270х220х70', '270х220х70'),
#                 ('корешок 25-40 круглый механизм 7200', 'корешок 25-40 круглый механизм 7200'),
#                 ('корешок 45-65 д-образный механизм', 'корешок 45-65 д-образный механизм'),
#                 )



# def get_box_sizes(indexes):
#     for element in indexes:


#     return BOX_SIZES    

from django.core.validators import int_list_validator

class Test(PolymorphicModel):
    BOX_SIZES = (
                ('50х50х35', '50х50х35'),
                ('60х60х40', '60х60х40'),
                ('60х60х40-P', '60х60х40-P'),
                ('80х80х40', '80х80х40'),
                ('80х80х40-P', '80х80х40-P'),
                ('240х185х120', '240х185х120'),
                ('270х220х70', '270х220х70'),
                )


    name = models.CharField(max_length=40)
    # dob = models.DateField(verbose_name='Date of birth')
    box_size = models.CharField(max_length=50, choices=BOX_SIZES,default='80х80х40')
    # int_list = models.CharField(validators=int_list_validator)
    int_list = models.CharField(validators=[int_list_validator], max_length=100)

    # @property
    # def age(self):
    #     return timezone.now().year - self.dob.year
    #     # return timezone.now().year - self.dob.year


# class  

# class  Product(PolymorphicModel):


#     def __str__(self):
#         return self.name


#     def get_absolute_url(self):
#         return reverse("mainapp:product", kwargs={
#             'slug': self.slug
#         })


#     name = models.CharField(max_length=300, default = None, null=True)
#     slug = models.SlugField(default = None, null=True)
#     subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, default = None, null=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, default = None, null=True)
#     preview_text = models.TextField(max_length=200, verbose_name='Preview Text', blank=True, null=True)
#     detail_text = models.TextField(max_length=1000, verbose_name='Detail Text', blank=True, null=True)
#     price = models.FloatField(default = None, null=True)
#     tirazh = models.IntegerField(null=False)
#     t = models.IntegerField(null=True)
#     k = models.IntegerField(null=True)
#     #t =  models.DateField(auto_now=False, auto_now_add= False)
#     box_size = models.CharField(max_length=50, choices=BOX_SIZES,default='80х80х40')

# BOX_SIZES = (
#                 ('50х50х35', '50х50х35'),
#                 ('60х60х40', '60х60х40'),
#                 ('60х60х40-P', '60х60х40-P'),
#                 ('80х80х40', '80х80х40'),
#                 ('80х80х40-P', '80х80х40-P'),
#                 ('240х185х120', '240х185х120'),
#                 ('270х220х70', '270х220х70'),
#                 ('корешок 25-40 круглый механизм 7200', 'корешок 25-40 круглый механизм 7200'),
#                 ('корешок 45-65 д-образный механизм', 'корешок 45-65 д-образный механизм'),
#                 )
    

# def get_years(initial=1970):
#     return [(year, year) for year in range(datetime.datetime.now().year, initial, -1)]

# class Profile(UserenaBaseProfile):
#     starting_year = models.CharField(blank=False, max_length=4, choices=get_years, default=datetime.datetime.now().year)


# --------------------

# def get_my_choices():
#     # you place some logic here
#     return choices_list

# class MyForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super(MyForm, self).__init__(*args, **kwargs)
#         self.fields['my_choice_field'] = forms.ChoiceField(
#             choices=get_my_choices() )

# ------------------------------


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















