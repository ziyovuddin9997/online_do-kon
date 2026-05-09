from django.urls import path

from app_main.views import (products, signin, signout, signup,
                            product_detail, profile, cart, transactions,
                            delete_cart_product, buy)


urlpatterns = [
    path('', products, name='products'),                                        # http://localhost:8000
    path('signin/', signin, name='signin'),                                     # http://localhost:8000/login
    path('signup/', signup, name='signup'),                                     # http://localhost:8000/login
    path('signout/', signout, name='signout'),                                  # http://localhost:8000/login
    path('product-detail/<uuid:id>/', product_detail, name='product_detail'),   # http://localhost:8000/product-detail/2/
    path('profile/', profile, name='profile'),                                  # http://localhost:8000/profile/
    path('cart/', cart, name='cart'),                                           # http://localhost:8000/profile/
    path('transactions/', transactions, name='transactions'),
    path('delete-cart-product/<int:id>/', delete_cart_product, name='delete_cart_prouduct'),
    path('buy/', buy, name='buy')
]
