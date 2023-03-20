from django.shortcuts import render

# Create your views here.
import razorpay

from .models import Coffee
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = int(request.POST.get("amount"))*100
        client = razorpay.Client(auth=("rzp_test_UYsyGTN1AzTAbS", "p77LMw9BbaYRVkQlRcYYP0iB"))
        payment = client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
        print(payment)
        coffee = Coffee(name = name, amount=amount,payment_id=payment['id'] )
        coffee.save()
        return render(request, "index.html", {'payment':payment})

    return render(request, "index.html")


@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        print(a)
        order_id = ""
        for k,v in a.items():
            if k == 'razorpay_order_id':
                order_id = v
                break
        user = Coffee.objects.filter(order_id=order_id).first()
        user.paid = True
        user.save()
        print()
        print(order_id)
    return render(request, "success.html")