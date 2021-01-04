from django.shortcuts import render, get_object_or_404
from .models import Category, Product, SubCategory, MiniCategory
from .forms import NegotiateForm
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import Client
from django.db.models import Count

@login_required(login_url ='login:login_redirect')
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    client = Client.objects.get(user=request.user)
    client_orders = client.no_of_orders
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)

    return render(request, 'shop/product/list.html',   context={
        'category': category,
        'categories': categories,
        'products': products,
        'client_orders':client_orders,
        'tab': 'shop',
        'local_css_urls': ["css3/easy-responsive-tabs.css",
                           "css3/material-kit.min1036.css",
                           "css3/demo.css",
                           "css3/vertical-nav.css"],
        'local_js_urls': ["core/jquery.min.js",
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


def subcategory_list(request, subcategory_slug=None):
    subcategory = None
    subcategories = Category.SubCategory.objects.all()
    products = Product.subcategory.objects.filter(available=True)
    if category_slug:
        subcategory = get_object_or_404(SubCategory, slug=SubCategory_slug)
        products = Product.objects.filter(subcategory=subcategory)

    context = {

        'subcategory': subcategory,
        'subcategories': subcategories,
        'products': products,

    }
    return render(request, 'shop/product/sublist.html', context)


def minicategory_list(request, minicategory_slug=None):
    minicategory = None
    minicategories = Category.SubCategory.MiniCategory.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        minicategory = get_object_or_404(MiniCategory, slug=MiniCategory_slug)
        products = Product.objects.filter(minicategory=minicategory)

    context = {

        'minicategory': minicategory,
        'minicategories': minicategories,
        'products': products,

    }

    return render(request, 'shop/product/minilist.html', context)

# @login_required(login_url='/accounts/login/')
# def product_detail(request, id, slug):
#     product = get_object_or_404(Product, id=id, slug=slug, available=True)
#     cart_product_form = CartAddProductForm()
#     context = {
#         'product': product,
#         'cart_product_form': cart_product_form
#     }
#     return render(request, 'shop/product/detail.html', context)

@login_required(login_url ='login:login_redirect')
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    client = Client.objects.get(user=request.user)
    cart_product_form = CartAddProductForm()
    product_tags_ids = Product.tags.values_list('id', flat=True)
    similar_products = Product.objects.filter(tags__in=product_tags_ids)\
    .exclude(id=product.id)
    similar_products = similar_products.annotate(same_tags=Count('tags'))\
    .order_by('-same_tags','-created_at')[:6]
    context = {
        'product': product,
        'client':client,
        'product_tags_ids':product_tags_ids,
        'similar_products':similar_products,
        'cart_product_form': cart_product_form
    }
  
    return render(request, 'shop/product/detail.html',
                  context={
                      'product': product,
                      'cart_product_form': cart_product_form,
                      'product_tags_ids':product_tags_ids,
                      'similar_products':similar_products,
                      'local_css_urls': ["css3/easy-responsive-tabs.css",
                                         "css3/material-kit.min1036.css",
                                         "css3/demo.css",
                                         "css3/vertical-nav.css"],
                      'local_js_urls': ["core/jquery.min.js",
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


# homepage view

def home(request, category_slug=None, subcategory_slug=None, minicategory_slug=None):
    category = None
    subcategory = None
    minicategory = None
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    minicategories = MiniCategory.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        subcategories = SubCategory.objects.filter(category=category)

    # if subcategory_slug:
    #     subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
    #     minicategories = MiniCategory.objects.filter(available=True)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'subcategories': subcategories,
        'minicategories ': minicategories,
        'subcategory': subcategory,
        'minicategory': minicategory,
    }

    return render(request, 'shop/homepage/page/home.html',   context={
        'category': category,
        'categories': categories,
        'products': products,
        'subcategories': subcategories,
        'minicategories': minicategories,
        'subcategory': subcategory,
        'minicategory': minicategory,

        'tab': 'shop',
        'local_css_urls': ["css3/easy-responsive-tabs.css",
                           "css3/material-kit.min1036.css",
                           "css3/demo.css",
                           "css3/vertical-nav.css"],
        'local_js_urls': ["core/jquery.min.js",
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


def log(request):
    return render(request, 'shop/product/login2.html', {
        'tab': 'registration',
        'local_css_urls': ["css3/easy-responsive-tabs.css",
                           "css3/material-kit.min1036.css",
                           "css3/demo.css",
                           "css3/vertical-nav.css"],
        'local_js_urls': ["core/jquery.min.js",
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


def vendorrequest(request):
    return render(request, 'shop/homepage/page/vendorrequest.html', {
        'tab': 'vendor',
        'local_css_urls': ["css3/easy-responsive-tabs.css",
                           "css3/material-kit.min1036.css",
                           "css3/demo.css",
                           "css3/vertical-nav.css"],
        'local_js_urls': ["js3/vertical-nav.js",
                          "js3/material-kit.min1036.js",
                          "js3/demo.js",
                          "js3/buttons.js",
                          "js3/modernizr.js",

                          "js3/jquery.min.js",
                          "js3/bootstrap.min.js",
                          "core/jquery.min.js",
                          "core/popper.min.js",
                          "core/bootstrap-material-design.min.js",
                          "js3/plugins/moment.min.js ",
                          "js3/plugins/bootstrap-datetimepicker.js",
                          "js3/plugins/jquery.flexisel.js",
                          "js3/plugins/jquery.sharrre.js",
                          "js3/plugins/nouislider.min.js",
                          "js3/plugins/bootstrap-selectpicker.js",
                          "js3/plugins/bootstrap-tagsinput.js",
                          "js3/plugins/jasny-bootstrap.min.js"],
    })


def Vendorfaqs(request):
    return render(request, 'shop/homepage/page/vendorfaqs.html', {
        'tab': 'Vendorfaqs',
        'local_css_urls': ["css3/easy-responsive-tabs.css",
                           "css3/material-kit.min1036.css",
                           "css3/demo.css",
                           "css3/vertical-nav.css"],
        'local_js_urls': ["js3/vertical-nav.js",
                          "js3/material-kit.min1036.js",
                          "js3/demo.js",
                          "js3/buttons.js",
                          "js3/modernizr.js",

                          "js3/jquery.min.js",
                          "js3/bootstrap.min.js",
                          "core/jquery.min.js",
                          "core/popper.min.js",
                          "core/bootstrap-material-design.min.js",
                          "js3/plugins/moment.min.js ",
                          "js3/plugins/bootstrap-datetimepicker.js",
                          "js3/plugins/jquery.flexisel.js",
                          "js3/plugins/jquery.sharrre.js",
                          "js3/plugins/nouislider.min.js",
                          "js3/plugins/bootstrap-selectpicker.js",
                          "js3/plugins/bootstrap-tagsinput.js",
                          "js3/plugins/jasny-bootstrap.min.js"],
    })


def homeaccesories(request):
    return render(request, 'shop/product/homeaccesories.html')


def decorbeauty(request):
    return render(request, 'shop/product/decorbeauty.html')


def about(request):
    return render(request, 'shop/product/about.html', {
        'tab': 'Vendorfaqs',
        'local_css_urls': ["css3/easy-responsive-tabs.css",
                           "css3/material-kit.min1036.css",
                           "css3/demo.css",
                           "css3/vertical-nav.css"],
        'local_js_urls': ["js3/vertical-nav.js",
                          "js3/material-kit.min1036.js",
                          "js3/demo.js",
                          "js3/buttons.js",
                          "js3/modernizr.js",

                          "js3/jquery.min.js",
                          "js3/bootstrap.min.js",
                          "core/jquery.min.js",
                          "core/popper.min.js",
                          "core/bootstrap-material-design.min.js",
                          "js3/plugins/moment.min.js ",
                          "js3/plugins/bootstrap-datetimepicker.js",
                          "js3/plugins/jquery.flexisel.js",
                          "js3/plugins/jquery.sharrre.js",
                          "js3/plugins/nouislider.min.js",
                          "js3/plugins/bootstrap-selectpicker.js",
                          "js3/plugins/bootstrap-tagsinput.js",
                          "js3/plugins/jasny-bootstrap.min.js"],
    })


def mens(request):
    return render(request, 'shop/product/mens.html')


def contact(request):
    return render(request, 'shop/product/contact.html', {
        'tab': 'registration',
        'local_css_urls': ["css3/easy-responsive-tabs.css",
                           "css3/material-kit.min1036.css",
                           "css3/demo.css",
                           "css3/vertical-nav.css"],
        'local_js_urls': ["core/jquery.min.js",
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


def womens(request):
    return render(request, 'shop/product/womens.html')


def contact(request):
    return render(request, 'shop/product/contact.html', {
        'tab': 'registration',
        'local_css_urls': ["css3/easy-responsive-tabs.css",
                           "css3/material-kit.min1036.css",
                           "css3/demo.css",
                           "css3/vertical-nav.css"],
        'local_js_urls': ["core/jquery.min.js",
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


def womens(request):
    return render(request, 'shop/product/womens.html')


def contact(request):
    return render(request, 'shop/product/contact.html', {
        'tab': 'registration',
        'local_css_urls': ["css3/easy-responsive-tabs.css",
                           "css3/material-kit.min1036.css",
                           "css3/demo.css",
                           "css3/vertical-nav.css"],
        'local_js_urls': ["core/jquery.min.js",
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


def womens(request):
    return render(request, 'shop/product/womens.html')


def contact(request):
    return render(request, 'shop/product/contact.html', {
        'tab': 'registration',
        'local_css_urls': ["css3/easy-responsive-tabs.css",
                           "css3/material-kit.min1036.css",
                           "css3/demo.css",
                           "css3/vertical-nav.css"],
        'local_js_urls': ["core/jquery.min.js",
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


def womens(request):
    return render(request, 'shop/product/womens.html')


def contact(request):
    return render(request, 'shop/product/contact.html', {
        'tab': 'registration',
        'local_css_urls': ["css3/easy-responsive-tabs.css",
                           "css3/material-kit.min1036.css",
                           "css3/demo.css",
                           "css3/vertical-nav.css"],
        'local_js_urls': ["core/jquery.min.js",
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


def womens(request):
    return render(request, 'shop/product/womens.html')


def contact(request):
    return render(request, 'shop/product/contact.html', {
        'tab': 'registration',
        'local_css_urls': ["css3/easy-responsive-tabs.css",
                           "css3/material-kit.min1036.css",
                           "css3/demo.css",
                           "css3/vertical-nav.css"],
        'local_js_urls': ["core/jquery.min.js",
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


def womens(request):
    return render(request, 'shop/product/womens.html')


def client_price(request, id, slug):
    product = Product.objects.get(id=id, slug=slug )
    request.session['intial_product_price']=str(product.price)
    client = Client.objects.get(user=request.user)
    cart_product_form = CartAddProductForm()
    product_tags_ids = Product.tags.values_list('id', flat=True)
    similar_products = Product.objects.filter(tags__in=product_tags_ids)\
    .exclude(id=product.id)
    similar_products = similar_products.annotate(same_tags=Count('tags'))\
    .order_by('-same_tags','-created_at')[:6]
    if request.method == 'POST':
            # create a form instance and populate it with data from the request:
        form = NegotiateForm(request.POST)
            # check whether it's valid:
        if form.is_valid():

                # process the data in form.cleaned_data as required
            client_price=form.cleaned_data['client_price']
            request.session['client_price'] = request.POST['client_price']
        if client.has_discount:
                if float(client_price) < product.reject_price:
                    messages.success(request, ('Sorry! thats offer is so low kindly add amount ' ))

                elif float(client_price) < product.lowest_price_offer :
                    
                    messages.success(request, (' Please add a little amount  '))

                elif float(client_price) > product.lowest_price_offer and float(client_price) < product.maximum_price_offer :
                    messages.success(request, (' please top up a little amount'))

                elif float(client_price) >= product.maximum_price_offer and float(client_price) < product.price :
                    messages.success(request, (' hey I accept this offer'))
                    request.session['product_id']=product.id
                    product.price = float(client_price)
                    print(product.price)
                    request.session['product.price']=product.price
                    request.session.modified=True
                    print(product.price)
                    print("I love {}.".format(product.price))
                    return render(request, 'shop/product/clientsuccess.html',{
                    'form': form,
                    'product': product,
                    'cart_product_form': cart_product_form,
                    'client_price':client_price,
                    'product_tags_ids':product_tags_ids,
                    'similar_products':similar_products,
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


                elif float(client_price) >= product.price :
                    messages.success(request, (' hey I accept this offer, thank you for the TIP'))
                    request.session['product_id']=product.id
                    product.price= float(client_price)
                    request.session['product.price']=product.price
                    request.session.modified=True
                    print("I love {}.".format(product.price))
                    return render(request, 'shop/product/clientsuccess.html',{
                    'form': form,
                    'product': product,
                    'cart_product_form': cart_product_form,
                    'client_price':client_price,
                    'product_tags_ids':product_tags_ids,
                    'similar_products':similar_products,
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
        else:
                messages.info(
                    request, ('Unfortunately ou are not eligible for any loan!'))
        return render(request, 'shop/product/client.html',{
             'form': form,
            'product': product,
            'cart_product_form': cart_product_form,
            'client_price':client_price,
            'product_tags_ids':product_tags_ids,
            'similar_products':similar_products,
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

        

        # if a GET (or any other method) we'll create a blank form
    else:
        form = NegotiateForm()
        return render(request, 'shop/product/client.html', {
        'form': form,
        'product': product,
        'product_tags_ids':product_tags_ids,
        'similar_products':similar_products,
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
    

@login_required(login_url ='login:login_redirect')
def negotiate(request, id, slug):
    client_price=request.session['client_price']
    product = Product.objects.get(id=id, slug=slug )
    client = Client.objects.get(user=request.user)
    client_orders = client.no_of_orders
    price1 =float(product.price)-float(product.price) * 0.1
    price_discount_1 = float(product.price)-float(product.price1) 
    price2 =  float(product.price) * 0.25
    price3 =  float(product.price) * 0.40
    price_discount_3 = float(product.price)-float(product.price3)
    cart_product_form = CartAddProductForm()
    if client.has_discount:
        if client.no_of_orders < 1:
            product.price = product.price
            messages.success(request, ('Opps! Bummer eligible for a 0% percent discount based on your purchase history, price after discount is still ' '{}'.format(product.price)))

        elif client.no_of_orders < 3:
            product.price=price1
            messages.success(request, (' hey You are eligible for a 10% percent discount based on your purchase history,   lets deduct   ' '{}'.format(price_discount_1)))

        elif client.no_of_orders ==3 and client.no_of_orders < 5:
            product.price=price2
            messages.success(request,(' hey You are eligible for a 40% percent discount based on your purchase history,   lets deduct   ' '{}'.format(price_discount_3)))
        
        else:
            product.price=price3
            messages.success(
                request, ('You will be awarded  a 40% percent discount based on your purchase history'))
    else:
        messages.info(
            request, ('Unfortunately ou are not eligible for any loan!'))
    return render(request, 'shop/discount.html',{
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

