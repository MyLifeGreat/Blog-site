from django.urls import path
from .views import index,register_page,create_profile,login_page,post_detail,post_share

urlpatterns = [
    path('',index,name='index'),
    path('sign_up',register_page,name='register_page'),
    path('create_profile',create_profile,name="create_profile"),
    path('login_page',login_page,name="login_page"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',post_detail,name="post_detail"),
    path('<int:post_id>/share/',post_share,name='post_share'),



]