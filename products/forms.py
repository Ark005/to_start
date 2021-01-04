from .models import Friend, SubCategory, Product
from django import forms
import datetime



class FriendForm(forms.ModelForm):
    ## change the widget of the date field.
    dob = forms.DateField(
        label='What is your birth date?', 
        # change the range of the years from 1980 to currentYear - 5
        widget=forms.SelectDateWidget(years=range(1980, datetime.date.today().year-5))
    )
    
    def __init__(self, *args, **kwargs):
        super(FriendForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Friend
        #fields = ("__all__")
        fields = ('dob','tirazh')


class ProductForm(forms.ModelForm):
    ## change the widget of the date field.
    dob = forms.DateField(
        label='Дата производства', 
        # change the range of the years from 1980 to currentYear - 5
        widget=forms.SelectDateWidget(years=range(2020, datetime.date.today().year-5))
    )
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for tirazh in self.fields.keys():
            self.fields[tirazh].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Product
        #fields = ("__all__")
        fields = ('tirazh', 'box_size')

# class BoxForm(forms.ModelForm):
  
#     def __init__(self, *args, **kwargs):
#         super(BoxForm, self).__init__(*args, **kwargs)
#         ## add a "form-control" class to each form input
#         ## for enabling bootstrap
#         for name in self.fields.keys():
#             self.fields[name].widget.attrs.update({
#                 'class': 'form-control1',
#             })

#     class Meta:
#         model = Box
#         fields = ("__all__")

class SubproductForm(forms.Form):
    name = forms.ModelChoiceField(queryset=SubCategory.objects.all())

       
        