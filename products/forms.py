from .models import  SubCategory, Product, BoxType1, BoxType2,Note1
from django import forms
import datetime

from polymorphic.formsets import polymorphic_modelformset_factory, PolymorphicFormSetChild

ProductFormSet = polymorphic_modelformset_factory(Product, formset_children=(
    PolymorphicFormSetChild(BoxType1),
    PolymorphicFormSetChild(BoxType2),
    PolymorphicFormSetChild(Note1),
), fields = ('tirazh', 'box_size'))



class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass

class ProductFormCommon(forms.Form):
    tirazh = forms.IntegerField()
    box_size = ChoiceFieldNoValidation(choices=[('240х185х120', '240х185х120'), ('270х220х70', '270х220х70')])
    # box_size = forms.CharField(max_length=48)
   

class ProductForm(forms.ModelForm):
    

    def __init__(self, *args, **kwargs):
    

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
        #fields = ('tirazh', 'box_size', 'price')
        fields = ('tirazh', 'box_size')     
        #exclude = ('box_size',)
        

class SubproductForm(forms.Form):
    name = forms.ModelChoiceField(queryset=SubCategory.objects.all())

       
        