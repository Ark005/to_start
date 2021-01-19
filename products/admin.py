from django.contrib import admin

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from products.models import Category, Product, SubCategory, BoxType1, BoxType2,Post,FolderType1

admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(SubCategory)
 
admin.site.register(Post)

# нужен чтобы наследовать дочерние модели
class ModelAChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = Product  # Optional, explicitly set here.

    # By using these `base_...` attributes instead of the regular ModelAdmin `form` and `fieldsets`,
    # the additional fields of the child models are automatically added to the admin form.
    
    """
    то же что ModelAdmin.form 
    base_form = ...
    """

    # то же что и ModelAdmin.fieldset для обычных  моделей
    # Позволяет изменить макет страниц добавления и редактирования объекта.

    """
    base_fieldsets = (
        ...
    )
    """


# Child модель
@admin.register(BoxType1)
class ModelBAdmin(ModelAChildAdmin):
    base_model = BoxType1  # Explicitly set here!
    # define custom features here

# Child модель
@admin.register(BoxType2)
class ModelBAdmin(ModelAChildAdmin):
    base_model = BoxType2  # Explicitly set here!
    # define custom features here


@admin.register(FolderType1)
class ModelBAdmin(ModelAChildAdmin):
    base_model = FolderType1  # Explicitly set here!
    # define custom features here

# Базовая модель
@admin.register(Product) # Декоратор для регистрации
class ProductParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = Product  # Optional, explicitly set here.
    child_models = (BoxType2, BoxType1,FolderType1)
    list_filter = (PolymorphicChildModelFilter,)  # This is optional