from django.conf.urls import url
from django.contrib.auth import views as auth_views
from gallery import views

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^register/$', views.RegisterFormView.as_view()),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='auth_views.login'),
    url(r'^logout/$', auth_views.logout,
                      {'next_page': '/'}, name="auth_views.logout"),
    url(r'^profile/$', views.profile, name='profile'),
]

