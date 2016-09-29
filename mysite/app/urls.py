from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
import social.apps.django_app.urls
import paypal.standard.ipn.urls


from . import views

urlpatterns = [
    url(r'^$', views.main, name="main"),
    url(r'^search/$', views.search, name="search"),
    url(r'^book/(?P<book_id>[0-9]+)/$', views.book_info, name="book_info"),
    url(r'^search_handler/$', views.search_handler, name="search_handler"),
    url(r'^about/$', views.about, name="about"),
    url('', include(social.apps.django_app.urls, namespace='social')),
	url(r'^accounts/logout/$', views.account_logout, name='logout'),
	url(r'^accounts/login/$', views.account_login, name='login'),
	url(r'^authenticate_user/$', views.authenticate_user, name='authenticate'),
	url(r'^register_user/$', views.register_user, name='register'),
	url(r'^accounts/profile/$', views.account_profile, name='profile'),
	url(r'^add_to_cart/$', views.add_to_cart, name='add_to_cart'),
	url(r'^del_from_cart/$', views.del_from_cart, name='del_from_cart'),
	url(r'^cart/$', views.cart, name='cart'),
	url(r'^payment/$', views.paypal_pay, name='payment'),
	url(r'^payment/success/$', views.paypal_success, name='success'),
	url(r'^paypal/', include(paypal.standard.ipn.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)