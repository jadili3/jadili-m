import base64
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
import keys
# from cart import *
from .orders.models import Order


unformatted_time = datetime.now()
formatted_time = unformatted_time.strftime("%Y%m%d%H%M%S")
# print(formatted_time, "this is the formatted time")

data_to_be_encoded = keys.business_shortCode + keys.lipa_na_mpesa_passkey + formatted_time 
encoded_string = base64.b64encode(data_to_be_encoded.encode())
decoded_password = encoded_string.decode('utf-8')


  
consumer_key = keys.consumer_key
consumer_secret = keys.consumer_secret
api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
  
r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
  


json_response = r.json() #{'access_token': 'zqNte7R18kA1z29GgNPre0eNDvEr', 'expires_in': '3599'}

my_access_token = json_response['access_token']


def lipa_na_mpesa():
    
    access_token = my_access_token 
   
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    headers = { "Authorization": "Bearer %s" % access_token }

    request = {
        "BusinessShortCode": keys.business_shortCode ,
        "Password": decoded_password,
        "Timestamp": formatted_time ,
        "TransactionType": "CustomerPayBillOnline",
        "Amount":  '%.2f' % order.total_cost(),
        "PartyA": keys.phone_number,
        "PartyB": keys.business_shortCode,
        "PhoneNumber": keys.phone_number,
        "CallBackURL": "https://curioeffect.co.ke/mcheckout",
        "AccountReference": "8686",
        "TransactionDesc": "buyitem"
      }
      
    response = requests.post(api_url, json = request, headers=headers)
      
    print (response.text)

lipa_na_mpesa()


def client_price(request, id, slug):
    product = Product.objects.get(id=id, slug=slug )
    client = Client.objects.get(user=request.user)
    client_orders = client.no_of_orders
    price1 =float(product.price)-float(product.) * 0.1
    price_discount_1 = float(product.price)-float(price1) 
    price2 =  float(product.price) * 0.25
    price_discount_2 = float(product.price)-float(price2) 
    price3 =  float(product.price) * 0.40
    price_discount_3 = float(product.price)-float(price3)
    cart_product_form = CartAddProductForm()
    if request.method == 'POST':
            # create a form instance and populate it with data from the request:
        form = NegotiateForm(request.POST)
            # check whether it's valid:
        if form.is_valid():

                # process the data in form.cleaned_data as required
            client_price=form.cleaned_data['client_price']
            request.session['client_price'] = client_price
        if client.has_discount:
                if client.no_of_orders < 1:
                    product.price = product.price
                    messages.success(request, ('Sorry! based on your purchase history we cannot give you a discount at the moment, eligible for a 0% percent discount , price is still ' '{}'.format(product.price)))

                elif client.no_of_orders < 3:
                    
                    messages.success(request, (' but based on your purchase history, we can offer a discount of KSH ' '{}'.format(price_discount_1 )))

                elif client.no_of_orders ==3 and client.no_of_orders < 5:
                    messages.success(request, (' but based on your purchase history, we can offer a discount of KSH ' '{}'.format(price_discount_2 )))
                else:
                    messages.success(request,('  but based on your purchase history, we can offer a discount of KSH ' '{}'.format(price_discount_3))) 
        else:
                messages.info(
                    request, ('Unfortunately ou are not eligible for any loan!'))
        return render(request, 'shop/product/client.html',{
            'form': form,
            'product': product,
            'price1':price1,
            'price2':price2,
            'price3':price3,
            'cart_product_form': cart_product_form,
            'client_orders':client_orders,
            'client_price':client_price,
            'local_css_urls': ["css3/easy-responsive-tabs.css",
                            "css3/material-kit.min1036.css",
                            "css3/demo.css",
                            "css3/vertical-nav.css"],
            'local_js_urls': [ "core/jquery.min.js",
                           "core/popper.min.js",
                           "core/bootstrap-material-design.min.js",
                           "js3/vertical-nav.js",
                           "js3/material-kit.min1036.js",
                           "js3/demo.js",
                           "js3/buttons.js",
                           "js3/modernizr.js",                         
                           "js3/bootstrap.min.js",                           
                           "js3/plugins/moment.min.js ",
                           "js3/plugins/bootstrap-datetimepicker.js",
                           "js3/plugins/jquery.flexisel.js",
                           "js3/plugins/jquery.sharrre.js",
                           "js3/plugins/nouislider.min.js",
                           "js3/plugins/bootstrap-selectpicker.js",
                           "js3/plugins/bootstrap-tagsinput.js",
                           "js3/plugins/jasny-bootstrap.min.js"],
            })
            
                # ...
                # redirect to a new URL:
