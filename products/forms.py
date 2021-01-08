from .models import Friend, SubCategory, Product, BoxType1, BoxType2
from django import forms
import datetime

from polymorphic.formsets import polymorphic_modelformset_factory, PolymorphicFormSetChild

ProductFormSet = polymorphic_modelformset_factory(Product, formset_children=(
    PolymorphicFormSetChild(BoxType1),
    PolymorphicFormSetChild(BoxType2),
), fields = ('tirazh', 'box_size'))


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


class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass

class ProductFormCommon(forms.Form):
    tirazh = forms.IntegerField()
    box_size = ChoiceFieldNoValidation(choices=[('240х185х120', '240х185х120'), ('270х220х70', '270х220х70')])

    # box_size = forms.CharField(max_length=48)
    



class ProductForm(forms.ModelForm):
    
    
    # def __init__(self, post_data = None, *args, **kwargs):
    def __init__(self, *args, **kwargs):
        # if post_data :
        #     # self.fields.remove('box_size')
        #     # del self.fields['box_size']
        #     self.base_fields.remove('box_size')


        super(ProductForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for tirazh in self.fields.keys():
            self.fields[tirazh].widget.attrs.update({
                'class': 'form-control',
            })



        # отключить валидацию
        # self.fields['box_size'].validators = []

    class Meta:
        model = Product
        #fields = ("__all__")
        # fields = ('tirazh', 'box_size', 'price')
        fields = ('tirazh', 'box_size')
        exclude = ('box_size',)



class SubproductForm(forms.Form):
    name = forms.ModelChoiceField(queryset=SubCategory.objects.all())

       
        