from django.urls import path
from .views import (
    index,
    register_page,
    create_profile,
    login_page,
    post_detail,
    post_share,
    login,
    logout_user,
    category_detail,
    my_posts,
    create_page,
    create_post_save
)

urlpatterns = [
    path('',index,name='index'),
    path('sign_up',register_page,name='register_page'),
    path('create_profile',create_profile,name="create_profile"),
    path('login_page',login_page,name="login_page"),
    path('login',login,name="login"),
    path('logout_user',logout_user,name="logout_user"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',post_detail,name="post_detail"),
    path('<int:post_id>/share/',post_share,name='post_share'),
    path('category/<int:id>/',category_detail,name='category_detail'),
    path('my_posts/',my_posts,name='my_posts'),
    path('create_page/',create_page,name='create_page'),
    path('create_post_save',create_post_save,name='create_post_save'),
]