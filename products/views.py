from django.shortcuts import render
from django.views.generic import ListView, DetailView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .filters import ProductFilter, CategoryFilter
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse
from django.core import serializers
from .forms import FriendForm, ProductForm
from .models import Friend, Product, Category, SubCategory

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound

from django.views import View

class Home(ListView):
    model = Product
    template_name = 'products/home.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        return context

# выводит категории
def home(request):
    category_list = Category.objects.all()
    category_filter = CategoryFilter(request.GET, queryset=category_list)
    return render(request, 'products/home.html', {'filter': category_filter})



class ProductDetail(LoginRequiredMixin, DetailView):
	model = Product



def postFriend(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = FriendForm(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)

def postProduct(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = ProductForm(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)



def checkNickName(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        nick_name = request.GET.get("nick_name", None)
        # check for the nick name in the database.
        if Friend.objects.filter(nick_name = nick_name).exists():
            # if nick_name found return not valid new friend
            return JsonResponse({"valid":False}, status = 200)
        else:
            # if nick_name not found, then user can create a new friend.
            return JsonResponse({"valid":True}, status = 200)

    return JsonResponse({}, status = 400)




def indexView(request, slug):
    form = ProductForm()
    products = Product.objects.all()

    # Для примера берем первый объект модели Product
    # object = Product.objects.first()

    # object = Product.objects.get(slug = slug)

    try:
        product = Product.objects.get(slug = slug)
    except ObjectDoesNotExist:
        product = None
        # return HttpResponseNotFound("<h2>Not Found</h2>")
        # return JsonResponse(status=404, data={'status':'false','message':"Object Does Not Exist"})

    # return render(request, "product/<slug>/", {"form": form, "friends": friends})
    return render(request, "products/product_detail.html", {"form": form, "products": products, "object": product})

def new_indexView(request, slug):
    form = ProductForm()
    # products = Product.objects.all()
    
    try:
        product = Product.objects.get(slug = slug)
    except ObjectDoesNotExist:
        product = None

    return render(request, "products/products_details.html", {"form": form, "products": [product]})



# def boxView1(request):
#     form = BoxForm()
#     boxes = Box.objects.all()
#     return render(request, "box1.html", {"form": form, "boxes": boxes})



# def postFriend(request):
#     # request should be ajax and method should be POST.
#     if request.is_ajax and request.method == "POST":
#         # get the form data
#         form = FriendForm(request.POST)
#         # save the data and after fetch the object in instance
#         if form.is_valid():
#             instance = form.save()
#             # serialize in new friend object in json
#             ser_instance = serializers.serialize('json', [ instance, ])
#             # send to client side.
#             return JsonResponse({"instance": ser_instance}, status=200)
#         else:
#             # some form errors occured.
#             return JsonResponse({"error": form.errors}, status=400)

#     # some error occured
#     return JsonResponse({"error": ""}, status=400)

def postProduct(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":

        print('GET request AJAX')
        # get the form data
        form = ProductForm(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():

            # старое
            # instance = form.save()
            # # serialize in new friend object in json
            # ser_instance = serializers.serialize('json', [ instance, ])

            print(form.cleaned_data['box_size'])
            #print(form.cleaned_data['dob'])
            print(form.cleaned_data['tirazh'])
            #print(form.cleaned_data['name'])
            data = form.cleaned_data

            # product = Product.objects.get(id =1).update(box_size=form.data['box_size'], tirazh= data['tirazh'])
            try:
                # product = Product.objects.get(id =1)
                product = Product.objects.first()
                print(product)
                if product == None:
                    product = Product.objects.create(id = 1, name = "default_name", slug='default', price =10, tirazh =10, box_size = '50х50х35')



            # except Exception as e:
            # except ObjectDoesNotExist:
            # except products.models.Product.DoesNotExist:
            except Product.DoesNotExist:
                print('11111111111111')
                product = Product.objects.create(id = 1, name = "default_name", slug='default', price =10, tirazh =10, box_size = '50х50х35')
                print(product)
                # product.save()

           


            product.box_size=form.data['box_size']
            product.tirazh= data['tirazh']

            product.save()
            ser_instance = serializers.serialize('json', [ product, ])




            # send to client side.

            # MyModel.objects.filter(field1='Computer').update(field2='cool')
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)

"""

class FriendView(View):
    form_class = FriendForm
    template_name = "products/product_detail.html"

    def get(self, *args, **kwargs):
        form = self.form_class()
        friends = Friend.objects.all()
        return render(self.request, self.template_name, 
            {"form": form, "friends": friends})

    def post(self, *args, **kwargs):
        # request should be ajax and method should be POST.
        if self.request.is_ajax and self.request.method == "POST":
            # get the form data
            form = self.form_class(self.request.POST)
            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
                # serialize in new friend object in json
                ser_instance = serializers.serialize('json', [ instance, ])
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        # some error occured
        return JsonResponse({"error": ""}, status=400)
"""
from .forms import SubproductForm

from django.shortcuts import render, HttpResponse

# def get_subcategory(request, subcategory):
#     print("subcategory", subcategory)

#     product_list  = Product.objects.filter(subcategory = subcategory)
#     product_filter = ProductFilter(request.GET, queryset=product_list)

#     return render(request, 'products/subcategory_products.html', {'filter': product_filter})

# возвращает субкатегории
def get_subcategory(request, category):
    print("category", category)

    subcategory_list  = SubCategory.objects.filter(category = category)
    # product_filter = ProductFilter(request.GET, queryset=product_list)

    return render(request, 'products/subcategories.html', {'subcategories': subcategory_list})

def get_products(request, category, subcategory):
    print("category", subcategory)

    product_list  = Product.objects.filter(category = subcategory)
    # product_filter = ProductFilter(request.GET, queryset=product_list)

    return render(request, 'products/subcategory_products.html', {'products': product_list})


def products_by_category(request, category):
    print("category", category)

    product_list  = Product.objects.filter(category = category)
    # product_filter = ProductFilter(request.GET, queryset=product_list)

    return render(request, 'products/category_products.html', {'products': product_list})



    # return render(request, 'products/home.html', {'filter': product_filter})


    # if request.method == "POST":
    #     form = SubproductForm(request.POST)
    #     if form.is_valid():
    #         subcategory = form.cleaned_data["name"]
    #         subcategory_product = Product.objects.filter(subcategory = subcategory)
    # return HttpResponse("<h2>Hello, !!</h2>")

def show_subcategory(request):
    if request.method == "POST":
        form = SubproductForm(request.POST)
        if form.is_valid():
            subcategory = form.cleaned_data["name"]
            subcategory_product = Product.objects.filter(subcategory = subcategory)

        return render(request, 'products/sub_test.html', {'subcategory_product': subcategory_product})

    elif request.method == "GET":
        my_form = SubproductForm()
        # return render(request, 'products/subproduct.html', {'form': my_form})
        return render(request, 'products/sub_test.html', {'form': my_form})



