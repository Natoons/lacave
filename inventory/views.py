from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from inventory.forms import UserRegistry, ProductForm
from inventory.models import Product, CATEGORY
from django.utils import timezone
from datetime import timedelta

@login_required
def index(request):
    users = User.objects.all()[:2]
    products = Product.objects.all()[:2]
    reg_users = len(User.objects.all())
    all_prods = len(Product.objects.all())
    context = {
        "title": "Home",
        "users": users,
        "products": products,
        "count_users": reg_users,
        "count_products": all_prods,
    }
    return render(request, 'inventory/index.html', context)

@login_required
def products(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm()
    context = {
        "title": "Products",
        "products": products,
        "form": form
    }
    return render(request, 'inventory/products.html', context)

@login_required
def last_products(request):
    # Récupération des produits pour aujourd'hui
    today_products = Product.objects.filter(datetime__date=timezone.now().date())
    # Récupération des produits pour la dernière semaine
    last_week_products = Product.objects.filter(datetime__gte=timezone.now() - timedelta(days=7))

    # Récupération des produits pour le dernier mois
    last_month_products = Product.objects.filter(datetime__gte=timezone.now() - timedelta(days=30))

    # Récupération des produits pour l'année en cours
    this_year_products = Product.objects.filter(datetime__year=timezone.now().year)

    # Initialisation d'un dictionnaire pour stocker les quantités totales par catégorie pour chaque période
    category_totals_today = {category[0]: 0 for category in CATEGORY}
    category_totals_last_week = {category[0]: 0 for category in CATEGORY}
    category_totals_last_month = {category[0]: 0 for category in CATEGORY}
    category_totals_this_year = {category[0]: 0 for category in CATEGORY}


    # Calcul des quantités totales pour chaque catégorie pour la dernière semaine
    for product in last_week_products:
        category_totals_last_week[product.category] += product.quantity

    # Calcul des quantités totales pour chaque catégorie pour le dernier mois
    for product in last_month_products:
        category_totals_last_month[product.category] += product.quantity

    # Calcul des quantités totales pour chaque catégorie pour l'année en cours
    for product in this_year_products:
        category_totals_this_year[product.category] += product.quantity

    # Calcul des quantités totales pour chaque catégorie pour aujourd'hui
    for product in today_products:
        category_totals_today[product.category] += product.quantity

    context = {
        "title": "Product Statistics",
        "category_totals_today": category_totals_today,
        "category_totals_last_week": category_totals_last_week,
        "category_totals_last_month": category_totals_last_month,
        "category_totals_this_year": category_totals_this_year,
    }
    return render(request, 'inventory/product_statistics.html', context)


@login_required
def user_product_quantities(request):
    users = User.objects.all()
    user_product_quantities = []

    prix_unitaires = {
        'DryFly GIN': 155,
        'Rocky Mountain GIN': 175,
        'Few American GIN': 170,
        'DryFly Vodka': 180,
        'Hooch Vodka Citron': 195,
        'Journeyman Whisky': 125,
        'FireWater Whisky': 150,
        'Tequila': 210,
        'Violetta': 240,
    }

    # Définir les plages de temps pour lesquelles vous voulez calculer les quantités
    time_ranges = {
        'Day': timedelta(days=1),
        'Week': timedelta(weeks=1),
        'Month': timedelta(days=30),  # Peut nécessiter des ajustements pour les mois précis
        'Year': timedelta(days=365),  # Peut nécessiter des ajustements pour les années précises
    }

    for user in users:
        user_data = {'user': user, 'category_totals': {}}

        for time_range, delta in time_ranges.items():
            # Calculer la date de début de la période
            start_date = timezone.now() - delta

            # Récupérer tous les produits associés à cet utilisateur pour cette période
            user_products = Product.objects.filter(username=user, datetime__gte=start_date)

            # Initialiser un dictionnaire pour stocker les quantités totales par catégorie
            category_totals = {category[0]: 0 for category in CATEGORY}

            # Calculer les quantités totales pour chaque catégorie pour cette période
            for product in user_products:
                category_totals[product.category] += product.quantity

            # Ajouter les quantités totales par catégorie pour cette période
            user_data['category_totals'][time_range] = category_totals

        user_product_quantities.append(user_data)

    context = {
        'user_product_quantities': user_product_quantities,
        'prix_unitaires': prix_unitaires,
    }

    return render(request, 'inventory/user_product_quantities.html', context)

@login_required
def user_graph_quantities(request):
    users = User.objects.all()
    user_graph_quantities = []

    # Calculer la date de début et de fin de la période d'un mois
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)

    dates_list = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in
                  range(31)]  # 31 jours pour inclure la date de fin
    for user in users:
        # Récupérer tous les produits associés à cet utilisateur pour la période d'un mois
        user_products = Product.objects.filter(username=user, datetime__gte=start_date, datetime__lte=end_date)

        # Initialiser une liste pour stocker les quantités de produits par jour
        daily_quantities = [0] * 30  # 30 jours

        # Calculer les quantités de produits pour chaque jour
        for product in user_products:
            day_index = (product.datetime - start_date).days
            daily_quantities[day_index] += product.quantity

        user_data = {'user': user, 'daily_quantities': daily_quantities}
        user_graph_quantities.append(user_data)

    context = {
        'user_graph_quantities': user_graph_quantities,
        'dates_list': dates_list,
    }

    return render(request, 'inventory/user_graph_quantities.html', context)

@login_required
def user_category_graphs(request):
    users = User.objects.all()
    categories = [category[0] for category in CATEGORY]  # Récupérer les catégories disponibles

    # Calculer la date de début et de fin de la période d'un mois
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)

    # Créer la liste des dates pour le mois en cours
    dates_list = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(31)]  # 31 jours pour inclure la date de fin

    user_category_graphs_data = []

    for user in users:
        user_data = {'user': user, 'category_data': {}}

        for category in categories:
            # Récupérer tous les produits de cette catégorie associés à cet utilisateur pour la période d'un mois
            user_category_products = Product.objects.filter(username=user, category=category, datetime__gte=start_date, datetime__lte=end_date)

            # Initialiser une liste pour stocker les quantités de produits par jour
            daily_quantities = [0] * 31  # 31 jours

            # Calculer les quantités de produits pour chaque jour
            for product in user_category_products:
                day_index = (product.datetime - start_date).days
                daily_quantities[day_index] += product.quantity

            user_data['category_data'][category] = daily_quantities

        user_category_graphs_data.append(user_data)

    context = {
        'user_category_graphs_data': user_category_graphs_data,
        'categories': categories,
        'dates_list': dates_list
    }

    return render(request, 'inventory/user_category_graphs.html', context)

@login_required
def users(request):
    users = User.objects.all()
    context = {
        "title": "Users",
        "users": users
    }
    return render(request, 'inventory/users.html', context)

@login_required
def user(request):
    context = {
        "profile": "User Profile"
    }
    return render(request, 'inventory/user.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistry(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistry()
    context = {
        "register": "Register",
        "form": form
    }
    return render(request, 'inventory/register.html', context)
