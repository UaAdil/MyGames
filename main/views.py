from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import BoardGame, Category
from django.http import JsonResponse
from django.contrib.auth import logout
from django.db.models import Q


from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def profile_view(request):
    return render(request, 'main/profile.html', {
        'user': request.user
    })

def auth_view(request):
    reg_form = RegisterForm()
    login_form = AuthenticationForm()

    if request.method == 'POST':
        if 'register' in request.POST:
            reg_form = RegisterForm(request.POST)
            if reg_form.is_valid():
                user = reg_form.save()
                login(request, user)
                messages.success(request, 'Вы успешно зарегистрировались!')
                return redirect('home')
        elif 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.username}!')
                return redirect('home')

    return render(request, 'main/auth.html', {
        'reg_form': reg_form,
        'login_form': login_form
    })

def logout_view(request):
    logout(request)
    messages.success(request, "Вы вышли из аккаунта.")
    return redirect('home')

def home(request):
    new_games = BoardGame.objects.filter(is_new=True)
    best_games = BoardGame.objects.filter(is_best=True)
    games = BoardGame.objects.all()
    categories = Category.objects.all()
    return render(request, 'main/home.html', {
        'new_games': new_games,
        'best_games': best_games,
        'games': games,
        'categories': categories,
    })

def catalog_view(request):
    games = BoardGame.objects.all()
    categories = Category.objects.all()

    query = request.GET.get('q')
    if query:
        games = games.filter(name__icontains=query)

    category_id = request.GET.get('category')
    if category_id:
        games = games.filter(categories__id=category_id)

    sort = request.GET.get('sort')
    if sort == 'price_asc':
        games = games.order_by('price')
    elif sort == 'price_desc':
        games = games.order_by('-price')
    elif sort == 'new':
        games = games.filter(is_new=True)
    elif sort == 'discount':
        games = games.filter(discount_percent__gt=0)

    context = {
        'games': games,
        'categories': categories,
        'query': query or '',
        'selected_category': int(category_id) if category_id else None,
        'sort': sort,
    }

    return render(request, 'main/catalog.html', context)


def ajax_search(request):
    q = request.GET.get('q', '')
    games = BoardGame.objects.filter(name__icontains=q)[:5]

    results = []
    for game in games:
        results.append({
            'id': game.pk or game.id,
            'name': game.name,
            'image': game.image.url if game.image else '',
            'url': reverse('game_detail', args=[game.pk])
        })
    return JsonResponse({'results': results})


def contacts(request):
    return render(request, 'main/contacts.html')

def checkout_view(request):
    cart = request.session.get('cart', {})
    games = []
    total = 0

    for pk, quantity in cart.items():
        try:
            pk = int(pk)
            game = BoardGame.objects.get(pk=pk)
            game.quantity = quantity
            game.total_price = game.price * quantity
            games.append(game)
            total += game.total_price
        except (BoardGame.DoesNotExist, ValueError, TypeError):
            continue  # если pk некорректен или игры нет

    return render(request, 'main/payment.html', {
        'games': games,
        'total': total
    })


def process_payment(request):
    if request.method == 'POST':
        # Здесь будет логика обработки платежа (в будущем)
        messages.success(request, "Ваш заказ успешно оформлен! 🧾")
        return redirect('home')
    return redirect('checkout')

def game_detail(request, pk):
    game = get_object_or_404(BoardGame, pk=pk)
    return render(request, 'main/details.html', {'game': game})


def cart(request):
    cart = request.session.get('cart', {})
    games = []
    total = 0

    for pk, quantity in cart.items():
        if pk == 'null' or not pk.isdigit():
            continue  # пропускаем неправильные ключи
        game = get_object_or_404(BoardGame, pk=int(pk))
        game.quantity = quantity
        game.total_price = game.price * quantity
        games.append(game)
        total += game.total_price

    return render(request, 'main/cart.html', {'games': games, 'total': total})


def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    messages.success(request, f"Игра добавлена в корзину.")
    return redirect(request.META.get('HTTP_REFERER', 'catalog'))

def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session['cart'] = cart
    return redirect('cart')

def cart(request):
    cart = request.session.get('cart', {})
    games = []
    total = 0
    quantities = {}
    item_totals = {}

    for pk, qty in cart.items():
        if not pk or not str(pk).isdigit():
            continue
        try:
            game = BoardGame.objects.get(id=int(pk))
            game.quantity = qty
            game.total_price = game.price * qty
            games.append(game)
            total += game.total_price
            quantities[pk] = qty
            item_totals[pk] = game.total_price
        except BoardGame.DoesNotExist:
            continue

    return render(request, 'main/cart.html', {
        'games': games,
        'total': total,
        'quantities': quantities,
        'item_totals': item_totals,
    })


def increase_quantity(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

def decrease_quantity(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        if cart[str(pk)] > 1:
            cart[str(pk)] -= 1
        else:
            del cart[str(pk)]
    request.session['cart'] = cart
    return redirect('cart')


def favorites_view(request):
    favorites = request.session.get('favorites', [])
    games = BoardGame.objects.filter(pk__in=favorites)

    return render(request, 'main/favorites.html', {'games': games})


def toggle_favorite(request, pk):
    favorites = request.session.get('favorites', [])
    pk = str(pk)
    game = get_object_or_404(BoardGame, pk=pk)

    if pk in favorites:
        favorites.remove(pk)
        messages.info(request, f"Игра «{game.name}» удалена из избранного.")
    else:
        favorites.append(pk)
        messages.success(request, f"Игра «{game.name}» добавлена в избранное.")

    request.session['favorites'] = favorites
    return redirect(request.META.get('HTTP_REFERER', 'catalog'))
