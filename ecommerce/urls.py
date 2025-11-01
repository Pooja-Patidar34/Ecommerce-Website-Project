from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='/admin/login/'), name='logout'),
    path('accounts/',include('accounts.urls')),
    path('',include('products.urls')),
    path('cart/',include('cart.urls')),
    path('admin/',include('admin.urls')),
    path('order/',include('order.urls'))
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
