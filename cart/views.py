from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Cart, Order
from products.models import Product



# Add to Cart View

def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)    
    order_item, created = Cart.objects.get_or_create(
        item=item,
        user=request.user,
        purchased=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, f"{item.name} тираж изменён")
            return redirect("mainapp:cart-home")
        else:
            order.orderitems.add(order_item)
            messages.info(request, f"{item.name} товар добавлен в вашу корзину")
            return redirect("mainapp:cart-home")
    else:
        order = Order.objects.create(
            user=request.user)
        order.orderitems.add(order_item)
        messages.info(request, f"{item.name} товар добавлен в вашу корзину")
        return redirect("mainapp:cart-home")




# Remove item from cart

def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    cart_qs = Cart.objects.filter(user=request.user, item=item)
    if cart_qs.exists():
        cart = cart_qs[0]
        # Checking the cart quantity
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart_qs.delete()
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user,
            )[0]
            order.orderitems.remove(order_item)
            messages.warning(request, "Этот товар был удаллён из корзины.")
            return redirect("mainapp:home")
        else:
            messages.warning(request, "Этого товара не было в вашей корзине")
            return redirect("mainapp:home")
    else:
        messages.warning(request, "У вас нет активного заказа")
        return redirect("mainapp:home")


# Cart View

def CartView(request):

    user = request.user

    carts = Cart.objects.filter(user=user, purchased=False)
    orders = Order.objects.filter(user=user, ordered=False)

    if carts.exists():
        if orders.exists():
            order = orders[0]
            return render(request, 'cart/home.html', {"carts": carts, 'order': order})
        else:
            messages.warning(request, "У вас нет никакого товара в вашей корзине")
            return redirect("mainapp:home")
		
    else:
        messages.warning(request, "У вас нет никакого товара в вашей корзине")
        return redirect("mainapp:home")



# Decrease the quantity of the cart :

def decreaseCart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} товар удален из корзины.")
            messages.info(request, f"{item.name} количество обновилось.")
            return redirect("mainapp:cart-home")
        else:
            messages.info(request, f"{item.name} количество обновилось.")
            return redirect("mainapp:cart-home")
    else:
        messages.info(request, "У вас нет активного заказа")
        return redirect("mainapp:cart-home")
