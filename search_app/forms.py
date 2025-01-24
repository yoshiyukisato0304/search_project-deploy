from django import forms
from .models import Product,Category

class SearchForm(forms.Form):
    query = forms.CharField(
    label='検索キーワード',
    max_length=100, # CharField で max_length が有効です
    required=False,
    widget=forms.TextInput(attrs={'placeholder': '検索したいキーワードを入力'}))
    category = forms.ModelChoiceField(label='カテゴリ', queryset=Category.objects.all(), required=False)
    
class SearchFormforCompare(forms.Form):
    query = forms.CharField(label='検索', required=False)
    category = forms.ModelChoiceField(label='カテゴリ', queryset=Category.objects.all(), required=False)
    min_price = forms.DecimalField(label='最低価格', required=False)
    max_price = forms.DecimalField(label='最高価格', required=False)


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

        exclude = ['createuser']

class ProductCompareForm(forms.Form):
    product1 = forms.ModelChoiceField(queryset=Product.objects.all(), label="商品1")
    product2 = forms.ModelChoiceField(queryset=Product.objects.all(), label="商品2")