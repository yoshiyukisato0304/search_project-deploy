from django.shortcuts import render, get_object_or_404,get_list_or_404, redirect
from .models import Product, Category
from .forms import ProductForm, SearchForm, ProductCompareForm ,SearchFormforCompare
from django.core.paginator import Paginator
from django.shortcuts import render
import random
from django.http import HttpResponseBadRequest

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES,)
        if form.is_valid():#フォームが有効かの確認.
            product = form.save(commit=False)
            product.createuser = request.user  # ログインしているユーザーをセット.
            product.save()  # 保存.
            return redirect('search_app:search_view')
    else:
        form = ProductForm()
        return render(request, 'search_app/product_form.html', {'form': form})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    product_list = Product.objects.filter(category=product.category)
    product_list_as_list = list(product_list)

    # 現在のproductを除外
    product_list_as_list = [p for p in product_list_as_list if p != product]

    if len(product_list_as_list) >= 5:
        random_products = random.sample(product_list_as_list, min(5, len(product_list_as_list)))
    else:
        random_products = product_list_as_list

    recommendedfirst = None  # 初期値をNoneに設定
    recommendlist = []  # 初期値を空リストに設定
    recommendedlistempty = 0

    if random_products:  # random_productsが空でない場合のみ処理
        if len(random_products) > 1:
            recommendedfirst = random_products[0]
            recommendlist = random_products[1:]
        elif len(random_products) ==1 :
            recommendedfirst = random_products[0]
        else:
            recommendedlistempty = 1


    return render(request, 'search_app/product_detail.html', {'product': product, 'recommendedfirst': recommendedfirst, 'recommendedlist': recommendlist, 'recommendedlistempty':recommendedlistempty})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('search_app:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    # product オブジェクトをテンプレートに渡す
    return render(request, 'search_app/product_form.html', {'form': form, 'product':
    product})
    43


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'search_app/product_confirm_delete.html', {'product': product})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'search_app/product_list.html', {'products': products})


def search_view(request):

    form = SearchForm(request.GET or None)
    results = Product.objects.all() # クエリセットの初期化
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            results = results.filter(name__icontains=query) # ここでの filter はクエリセットに適用
    
    # カテゴリフィルタリング
    category_name = request.GET.get('category')
    if category_name:
        try:
    # カテゴリ名に基づいてカテゴリ ID を取得
            category = Category.objects.get(id=category_name)
            results = results.filter(category_id=category.id)
        except Category.DoesNotExist:
            results = results.none() # 存在しないカテゴリの場合、結果を空にする
            category = None

    # 価格のフィルタリング（最低価格・最高価格） 
    min_price = request.GET.get('min_price') 
    max_price = request.GET.get('max_price') 
    if min_price: 
        results = results.filter(price__gte=min_price) 
    if max_price: 
        results = results.filter(price__lte=max_price) 

    sort_by = request.GET.get('sort', 'name') 
    if sort_by == 'price_asc': 
        results = results.order_by('price') 
    elif sort_by == 'price_desc': 
        results = results.order_by('-price') 
    else:
        results = results.order_by('name')  # デフォルトの並び替え
 
    # クエリセットをリストに変換せず、直接 Paginator に渡す
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
 
    return render(request, 'search_app/search.html', {'form': form, 'page_obj': page_obj})



def favorite_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product in request.user.favorite_place.all():
        request.user.favorite_place.remove(product)
    else:
        request.user.favorite_place.add(product)
    return redirect('search_app:product_detail', pk=product.id)

def favorite_list(request):
    favorite_products = request.user.favorite_place.all()
    return render(request, 'search_app/favorite_list.html', {'favorite_products': favorite_products})

def compare_products(request):
    form = SearchFormforCompare(request.GET or None)
    results = Product.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            results = results.filter(name__icontains=query)

    category_name = request.GET.get('category')
    if category_name:
        try:
            category = Category.objects.get(id=category_name) #category_nameにはpkのidが渡されている.
            results = results.filter(category=category) # category_idではなくcategoryで直接フィルタ.
        except Category.DoesNotExist:
            results = Product.objects.none()

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        results = results.filter(price__gte=min_price)
    if max_price:
        results = results.filter(price__lte=max_price)

    if request.method == 'POST':
        product_id = request.POST.get('product')
        if not product_id:
            return HttpResponseBadRequest("Invalid product selection.")

        if 'product1_id' not in request.session:
            request.session['product1_id'] = int(product_id)
            return redirect(request.path + '?step=1&' + request.GET.urlencode()) # URLパラメータを保持
        else:
            product1_id = request.session.pop('product1_id')
            product1 = get_object_or_404(Product, id=product1_id)
            product2 = get_object_or_404(Product, id=product_id)
            context = {'product1': product1, 'product2': product2}
            return render(request, 'search_app/compare_result.html', context)

    step = int(request.GET.get('step', 0))
    context = {'products': results, 'step': step, 'form': form} # フィルタリングされた結果を渡す
    return render(request, 'search_app/compare_choice.html', context)
