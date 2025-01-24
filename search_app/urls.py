from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name ='search_app'

urlpatterns = [
    path('', views.search_view),
    path('search/', views.search_view, name='search_view'),#メインになるホーム画面のURL.
    path('product/new/', views.product_create, name='product_create'),#商品作成画面のURL.
    path('product/<int:pk>/', views.product_detail, name='product_detail'),#商品詳細へのURL.
    path('product/<int:pk>/edit/', views.product_update,name='product_update'),#商品の更新画面へのURL.
    path('product/<int:pk>/delete', views.product_delete,name='product_delete'),#商品の削除画面へのURL.
    path('product/', views.product_list, name='product_list'),#自分の作成した商品の一覧.
    path('product/<int:product_id>/favorite/', views.favorite_product, name='favorite_product'),#お気に入りの登録用 アクセスした時点で登録される.
    path('favorite_list/', views.favorite_list, name='favorite_list'), #お気に入りの一覧.
    path('product_compere/',views.compare_products, name='compare'),#比較画面のURL
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)