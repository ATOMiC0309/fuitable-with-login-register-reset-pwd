from django.urls import path
from .views import (ProductList, AllProductList, detail, product_by_category, rate, user_register, user_login,
                    user_logout, user_email)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path('', ProductList.as_view(), name='index'),

                  path('products/', AllProductList.as_view(), name='all_products'),
                  path('product/<int:product_id>/', detail, name='detail'),
                  path('product-by/<int:pk>/', product_by_category, name="product_by_category"),

                  path('rate/<int:post_id>/<int:rating>/', rate),

                  path('login/', user_login, name="login"),
                  path('logout/', user_logout, name="logout"),
                  path('register/', user_register, name="register"),

                  path('subscribe/', user_email, name="user_email"),

                  path('reset-password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
                  path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
                       name="password_reset_confirm"),
                  path('reset-password-complete/',
                       auth_views.PasswordResetCompleteView.as_view(template_name='shop/reset_done.html'),
                       name="password_reset_complete"),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
