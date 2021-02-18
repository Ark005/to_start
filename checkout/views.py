import stripe
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from cart.models import Order, Cart
from . models import BillingForm, BillingAddress
from django.views.generic.base import TemplateView

from .forms import TestForm


stripe.api_key = settings.STRIPE_SECRET_KEY 

def checkout(request):

    # Checkout view
    form = BillingForm
    test_form = TestForm
    
    order_qs = Order.objects.filter(user= request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_total = order_qs[0].get_totals() 
    context = {"form": form, "order_items": order_items, "order_total": order_total}
    # Getting the saved saved_address
    saved_address = BillingAddress.objects.filter(user = request.user)
    if saved_address.exists():
        savedAddress = saved_address.first()
        context = {"form": form, "order_items": order_items, "order_total": order_total, "savedAddress": savedAddress, "test_form": test_form}
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

# def send_email(request):
#     # sendMail('and444petr@gmail.com', 'av269van@gmail.com', "Тест",  )
#     # send_mail('Subject here', 'Here is the message.', 'from@example.com',
#     # ['av269van@gmail.com'], fail_silently=False)

#     # email = request.POST.get('email', '')

#     # Куда отправлять для теста
#     # email = 'av269van@gmail.com'
#     email = request.user.email
#     print(email)
#     # print("   ", request.user.email)
#     # print("email = ", email)

#     data = """
#     Hello there!

#     I wanted to personally write an email in order to welcome you to our platform.\
#      We have worked day and night to ensure that you get the best service. I hope \
#     that you will continue to use our service. We send out a newsletter once a \
#     week. Make sure that you read it. It is usually very informative.

#     Cheers!
#     ~ Yasoob
#     """
#     send_mail('Welcome!', data, "Yasoob", [email], fail_silently=False)
#     return redirect("checkout:index")


from django.template import Template, Context
from docx import Document
from lxml import etree

def create_document_email(email_addr, name):
    destination_document = Document('doc/document.docx')
    with open('doc/document.xml') as f:
        template_text = f.read()
    template = Template(template_text)
    text = 'Мой тестовый документ'
    email_addr = 'tdnbsdsdsdd@jj.com'
    template_xml = template.render(Context({'Title': name, 'text':text, 'email': email_addr}))

    # template_xml = template.render(Context({'Title': name, 'abzac':text, 'Email': email_addr}))
    

    target_xml_tree = etree.fromstring(template_xml.encode('utf-8'))
    # target_xml_tree = etree.fromstring(template_xml.encode('ascii'))
    target_body = target_xml_tree[0]
    root = destination_document._element
    root.replace(root.body, target_body)
    destination_document.save('doc/test.docx')

# import mimetypes
# content_type = mimetypes.guess_type(instance.presentation.name)[0]


# Новаяя вьюха
from django.core.mail import EmailMessage
def send_email(request):

    if request.method == "POST":
        name = request.POST.get("name")
        # sendMail('and444petr@gmail.com', 'av269van@gmail.com', "Тест",  )
        # send_mail('Subject here', 'Here is the message.', 'from@example.com',
        # ['av269van@gmail.com'], fail_silently=False)

        # email = request.POST.get('email', '')

        # Куда отправлять для теста
        # email = 'av269van@gmail.com'
        email = '005ark@gmail.com'


        # email = request.user.email
        print(email)

        create_document_email('testt_email@ghgdh.com', name)

        # template_name = 'emailattachment.html'

        subject = 'Welcome!'
        message = 'Hi, Dogovor.'

        # mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

        mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
        

        # filename, content and mimetype. filename is the name of the file attachment as it will appear 
        # in the email, content is the data that will be contained inside the attachment and mimetype is 
        # the optional MIME type for the attachment. If you omit mimetype, the MIME content type will be 
        # guessed from the filename of the attachment.

        # message.attach('design.png', img_data, 'image/png')
        # (filename, content, mimetype)

        content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

        # with open('test.docx', encoding='utf-8') as f:
        with open('doc/test.docx', 'rb') as f:
            mail.attach('dogovor.docx', f.read(), content_type)
        mail.send()
    else:
        pass

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