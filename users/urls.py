from django.urls import path
from .views import login_user, logout_user, signup_user


urlpatterns = [
    path('login/', login_user, name='user-login'),
    path('logout/', logout_user, name='user-logout'),
    path('signup/', signup_user, name='user-signup'),
]