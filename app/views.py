from django.shortcuts import render
from .forms import *
from .models import *
from .link_log_st import log_st, link_st


# home page
def home(request):
    # make link on navbar active
    link_st.__init__()
    link_st.home = 'active'

    context = {
        'title': 'Главная',
        'pagename': 'Булочная - Теплый Хлеб',
        'logged': log_st.is_logged_in,
        'LinkStatus': link_st,
    }
    return render(request, 'home.html', context)


# products page
def products(request):
    link_st.__init__()
    link_st.products = 'active'
    context = {
        'title': 'Продукты',
        'pagename': 'Продукты',
        'logged': log_st.is_logged_in,
        'LinkStatus': link_st,
        'products': Product.objects.all(),
        'is_logged_in': log_st.is_logged_in,
    }
    # Search algorithm
    if request.method == 'GET':
        if 'search-button' in request.GET and isinstance(request.GET['search'], str) and request.GET['search'] != '':
            if Search(request.GET).is_valid():
                search = request.GET['search']
                context['search'] = search
                if Product.objects.filter(title__icontains=search):
                    # getting all products which corresponds to the search
                    context['products'] = Product.objects.filter(title__icontains=search)
                else:
                    context['products'] = ''
    # Add to cart selected product
    if request.method == 'POST':
        if 'add_product' in request.POST and isinstance(request.POST['add_product'], str) and Product.objects.get(title=request.POST['add_product']):
            Product.objects.get(title=request.POST['add_product']).buyer.add(User.objects.get(email=log_st.email))
    return render(request, 'products.html', context)


# about page
def about(request):
    link_st.__init__()
    link_st.about = 'active'
    context = {
        'title': 'Информация',
        'pagename': 'Информация',
        'logged': log_st.is_logged_in,
        'LinkStatus': link_st,
    }
    return render(request, 'about.html', context)


# log_in page
def log_in(request):
    link_st.__init__()
    link_st.log_in = 'active'
    context = {
        'title': 'Войти',
        'pagename': 'Войти',
        'logged': False,
        'LinkStatus': link_st,
    }
    # Log_in
    if request.method == 'POST':
        form = UserLogin(request.POST)
        context['form'] = form
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Verify inputs using database
            if User.objects.filter(email=email) and User.objects.get(email=email).password == password:
                link_st.__init__()
                link_st.home = 'active'
                log_st.log_in(email)
                return render(request, 'home.html', {
                    'title': 'Главная',
                    'pagename': 'Булочная',
                    'logged': True,
                    'LinkStatus': link_st,

                })
            else:
                context['error'] = 'Неверный логин или пароль'
    return render(request, 'login.html', context)


# sign_up page
def sing_up(request):
    # a function to fill inputs if an error was made
    def fill_inputs(email, first_name, last_name, psw, psw_repeat):
        context['email'] = email
        context['first_name'] = first_name
        context['last_name'] = last_name
        context['password'] = psw
        context['repeat_password'] = psw_repeat

    link_st.__init__()
    link_st.sign_up = 'active'
    context = {
        'title': 'Регистрация',
        'pagename': 'Регистрация',
        'logged': False,
        'LinkStatus': link_st,
        'error': ''
    }
    # Sign_up
    if request.method == 'POST':
        form = UserRegister(request.POST)
        context['form'] = form
        if form.is_valid():
            # getting data from form's inputs
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['password_repeat']
            if password != repeat_password:
                context['error'] = 'Пароли не совпадают'
                fill_inputs(email, first_name, last_name, password, repeat_password)
            # if user already exists
            elif User.objects.filter(email=email):
                context['error'] = 'Пользователь уже существует'
                fill_inputs(email, first_name, last_name, password, repeat_password)
            else:
                # Creating user
                User.objects.create(email=email, first_name=first_name, last_name=last_name, password=password)
                link_st.__init__()
                link_st.home = 'active'
                log_st.log_in(email)
                # return home page
                return render(request, 'home.html', {
                    'title': 'Главная',
                    'pagename': 'Булочная',
                    'logged': True,
                    'LinkStatus': link_st,
                })
    return render(request, 'sign_up.html', context)


# profile_ info page
def profile_info(request):
    # if the button was clicked update user data
    if request.method == 'POST':
        User.objects.filter(email=log_st.email).update(
            email=request.POST['email'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'])

    link_st.__init__()
    link_st.profile_info = 'active'
    context = {
        'title': 'Профиль',
        'pagename': 'Профиль',
        'logged': True,
        'LinkStatus': link_st,
        'email': User.objects.get(email=log_st.email).email,
        'first_name': User.objects.get(email=log_st.email).first_name,
        'last_name': User.objects.get(email=log_st.email).last_name,
    }
    return render(request, 'profile_info.html', context)


# cart page
def cart(request):
    link_st.__init__()
    link_st.cart = 'active'
    context = {
        'title': 'Корзина',
        'pagename': 'Корзина',
        'logged': True,
        'LinkStatus': link_st,
        'total_price': 0,
        'products': ''
    }

    # post methods
    if request.method == 'POST':
        # remove one product
        if 'product_to_remove' in request.POST and isinstance(request.POST['product_to_remove'], str) and log_st.is_logged_in:
            Product.objects.get(title=request.POST['product_to_remove']).buyer.remove(User.objects.get(email=log_st.email))
        else:
            # if the project was restarted
            context['warn'] = 'Войдите в свой профиль!'
        # remove all products (buy all products)
        if 'buy-button' in request.POST and isinstance(request.POST['buy-button'], str):
            User.objects.get(email=log_st.email).product.clear()
            context['total_price'] = 0
            context['products'] = ''

    # getting all selected products
    products_ = Product.objects.filter(buyer__email=log_st.email)
    if products_:
        context['products'] = products_
        for product in products_:
            context['total_price'] += product.price

    return render(request, 'cart.html', context)


# log_out algorithm
def log_out(request):
    link_st.__init__()
    link_st.home = 'active'
    log_st.log_out()
    context = {
        'title': 'Главная',
        'pagename': 'Булочная',
        'logged': log_st.is_logged_in,
        'LinkStatus': link_st,
    }
    return render(request, 'home.html', context)
