from django.shortcuts import render, get_object_or_404
from .models import Book, Cart, Purchased
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render, redirect
from random import randint, shuffle
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm


# Create your views here.

def main(request):
    number_of_books_in_feed = 3
    books_for_feed = list(Book.objects.all())
    shuffle(books_for_feed)
    books_for_feed = books_for_feed[:number_of_books_in_feed]
    cart = get_or_set_cart(request)
    return render(request, 'app/main.html', {'books_for_feed': books_for_feed,
        'cart': cart})

def search(request):
    cart = get_or_set_cart(request)
    return render(request, 'app/search.html', {'cart': cart})

def book_info(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    authors = book.author.all()
    cart = get_or_set_cart(request)
    button_caption = 'add_to_cart'
    if request.user.is_authenticated():
        purchased = Purchased.objects.filter(user=request.user).filter(book__id=book_id)
        if len(purchased) > 0:
            button_caption = 'purchased'
    if len(cart.book.filter(id=book_id)) > 0:
        button_caption = 'added_to_cart'
    return render(request, 'app/book.html', {'book': book, 'authors': authors,
        'cart': cart, 'button_caption': button_caption})

def search_handler(request):
    if not request.is_ajax():
        redirect('/')
    title = request.GET.get('title')
    category = request.GET.get('category')
    author = request.GET.get('author')
    filtered_objects = Book.objects.filter(title__icontains=title).filter(
        category__name__icontains=category).filter(author__name__icontains=author).distinct()
    filtered_objects_grouped_into_rows = []
    books_per_row = 4
    for i in range(len(filtered_objects)):
   	    if i % books_per_row == 0:
   	        filtered_objects_grouped_into_rows.append([])
   	    filtered_objects_grouped_into_rows[-1].append(filtered_objects[i])
    cart = get_or_set_cart(request)
    return HttpResponse(render_to_string('app/search_result.html',
   	    {'filtered_objects_grouped_into_rows': filtered_objects_grouped_into_rows, 
        'width_for_book': 12 / books_per_row, 'cart': cart}))
   	

def about(request):
    cart = get_or_set_cart(request)
    return render(request, 'app/about.html', {'cart': cart})

def account_login(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        cart = get_or_set_cart(request)
        return render(request, 'app/account_login.html', {'cart': cart})

def authenticate_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse('success')
    else:
        return HttpResponse('fail')

def register_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if len(username) < 3:
        return HttpResponse('too short username')
    if len(username) < 6:
        return HttpResponse('too short password')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return HttpResponse('try to login now')
    return HttpResponse('this username is already in use')

def account_logout(request):
    logout(request)
    return redirect('/')

@login_required
def account_profile(request):
    cart = get_or_set_cart(request)
    purchased_books = [purchase.book for purchase in Purchased.objects.filter(user=request.user)]
    return render(request, 'app/profile.html', {'cart': cart, 'purchased_books': purchased_books})

def add_to_cart(request):
    if not request.is_ajax():
        redirect('/')
    book_id = request.POST.get('book_id')
    book = Book.objects.get(id=book_id)
    cart = get_or_set_cart(request)
    if len(cart.book.filter(id=book.id)) == 0:
        cart.book.add(book)
        cart.save()
    return HttpResponse(request)

def del_from_cart(request):
    if not request.is_ajax():
        redirect('/')
    book_id = request.POST.get('book_id')
    book = Book.objects.get(id=book_id)
    cart = get_or_set_cart(request)
    if len(cart.book.filter(id=book.id)) > 0:
        cart.book.remove(book)
        cart.save()
    return HttpResponse(request)

def cart(request):
    cart = get_or_set_cart(request)
    return render(request, 'app/cart.html', {'cart': cart})

@csrf_exempt
def paypal_success(request):
    """
    Tell user we got the payment.
    """
    cart = get_or_set_cart(request)
    cart.archive = True
    cart.save()
    for book_id in request.POST.get('item_name').split(','):
        purchase = Purchased()
        purchase.user = request.user
        purchase.book = Book.objects.get(id = book_id)
        purchase.save()
    #purchased_books = [purchase.book for purchase in Purchased.objects.filter(user=request.user).distinct()]
    redirect('profile')
    #ret (request, 'app/profile.html', {'cart': cart, 'purchased_books': purchased_books})

@login_required
def paypal_pay(request):
    """
    Page where we ask user to pay with paypal.
    """
    cart = get_or_set_cart(request)
    paypal_dict = {
        "business": "skripniuk.v-facilitator@gmail.com",
        "amount": str(cart.total_price()),
        "currency_code": "RUB",
        "item_name": cart.books_ids_list(),
        "notify_url": reverse('paypal-ipn'),
        "return_url": "http://localhost:8000/payment/success/",
        "cancel_return": "http://localhost:8000/payment/",
        "custom": str(request.user.id)
    }
    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, "paypal_dict": paypal_dict}
    return render(request, "app/payment.html", context)


def get_or_set_cart(request):
    if request.user.is_authenticated():
        token = request.session.get('token', 'absent')
        if token != 'absent':
            cart = get_object_or_404(Cart, token=token)
            if len(cart.book.all()) != 0:   #user created nonempty cart and then logged in
                carts = Cart.objects.filter(user=request.user).filter(archive=False)
                for cart_iter in carts:
                    cart_iter.archive = True
                    cart_iter.save()
                cart.user = request.user
                cart.save()
            del request.session['token']
        else:
            carts = Cart.objects.filter(user=request.user).filter(archive=False)
            if len(carts) == 0:
                cart = Cart()
                cart.user = request.user
                cart.save()
            else:
                cart = carts[0]
            return cart
    else:
        token = request.session.get('token', 'absent')
        if token == 'absent':
            cart = Cart()
            cart.save()
            request.session['token'] = cart.token
        else:
            cart = get_object_or_404(Cart, token=token)
        return cart