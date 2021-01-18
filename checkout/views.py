import stripe
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from cart.models import Order, Cart
from . models import BillingForm, BillingAddress
from django.views.generic.base import TemplateView


stripe.api_key = settings.STRIPE_SECRET_KEY 

def checkout(request):

    # Checkout view
    form = BillingForm
    
    order_qs = Order.objects.filter(user= request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_total = order_qs[0].get_totals() 
    context = {"form": form, "order_items": order_items, "order_total": order_total}
    # Getting the saved saved_address
    saved_address = BillingAddress.objects.filter(user = request.user)
    if saved_address.exists():
        savedAddress = saved_address.first()
        context = {"form": form, "order_items": order_items, "order_total": order_total, "savedAddress": savedAddress}
    if request.method == "POST":
        saved_address = BillingAddress.objects.filter(user = request.user)
        if saved_address.exists():

            savedAddress = saved_address.first()
            form = BillingForm(request.POST, instance=savedAddress)
            if form.is_valid():
                billingaddress = form.save(commit=False)
                billingaddress.user = request.user
                billingaddress.save()
        else:
            form = BillingForm(request.POST)
            if form.is_valid():
                billingaddress = form.save(commit=False)
                billingaddress.user = request.user
                billingaddress.save()
                
    return render(request, 'checkout/index.html', context)

from django.core.mail import send_mail


# import textwrap
# import smtplib

# def sendMail(FROM,TO,SUBJECT,TEXT,SERVER):
    
#     """this is some test documentation in the function"""
#     message = textwrap.dedent("""\
#         From: %s
#         To: %s
#         Subject: %s
#         %s
#         """ % (FROM, ", ".join(TO), SUBJECT, TEXT))
#     # Send the mail
#     server = smtplib.SMTP(SERVER)
#     server.sendmail(FROM, TO, message)
#     server.quit()

from django.shortcuts import redirect

def send_email(request):
    # sendMail('and444petr@gmail.com', 'av269van@gmail.com', "Тест",  )
    # send_mail('Subject here', 'Here is the message.', 'from@example.com',
    # ['av269van@gmail.com'], fail_silently=False)

    # email = request.POST.get('email', '')

    # Куда отправлять для теста
    # email = 'av269van@gmail.com'
    email = request.user.email
    print(email)
    # print("   ", request.user.email)
    # print("email = ", email)

    data = """
    Hello there!

    I wanted to personally write an email in order to welcome you to our platform.\
     We have worked day and night to ensure that you get the best service. I hope \
    that you will continue to use our service. We send out a newsletter once a \
    week. Make sure that you read it. It is usually very informative.

    Cheers!
    ~ Yasoob
    """
    send_mail('Welcome!', data, "Yasoob", [email], fail_silently=False)
    return redirect("checkout:index")




def payment(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    order_qs = Order.objects.filter(user= request.user, ordered=False)
    order_total = order_qs[0].get_totals() 
    totalCents = float(order_total * 100);
    total = round(totalCents, 2)
    if request.method == 'POST':
        charge = stripe.Charge.create(amount=total,
            currency='usd',
            description=order_qs,
            source=request.POST['stripeToken'])
        print(charge)
        
    return render(request, 'checkout/payment.html', {"key": key, "total": total})




def charge(request):
    order = Order.objects.get(user=request.user, ordered=False)
    orderitems = order.orderitems.all()
    order_total = order.get_totals() 
    totalCents = int(float(order_total * 100))
    if request.method == 'POST':
        charge = stripe.Charge.create(amount=totalCents,
            currency='inr',
            description=order,
            source=request.POST['stripeToken'])
        print(charge)
        if charge.status == "succeeded":
            orderId = get_random_string(length=16, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            print(charge.id)
            order.ordered = True
            order.paymentId = charge.id
            order.orderId = f'#{request.user}{orderId}'
            order.save()
            cartItems = Cart.objects.filter(user=request.user)
            for item in cartItems:
                item.purchased = True
                item.save()
        return render(request, 'checkout/charge.html', {"items": orderitems, "order": order })



def oderView(request):

    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {
            "orders": orders
        }
    except:
        messages.warning(request, "You do not have an active order")
        return redirect('/')
    return render(request, 'checkout/order.html', context)