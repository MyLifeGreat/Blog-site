
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import redirect, render,get_object_or_404
from .models import Post, Profile,Category
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login,logout
from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Post



def index(request):
    posts = Post.objects.all()

    categories = Category.objects.all()
    q = request.GET.get('q')
    if q:
        posts = posts.filter(Q(title__contains=q))
    context = {
        "posts":posts,
        "categories":categories
        
    }
    return render(request,'index.html',context)



def register_page(request):
    return render(request, 'register.html')


def create_profile(request):
    if request.method != "POST":
        return HttpResponse("Xatolik yuz berdi")
    else:
        username = request.POST.get("username")
        ism = request.POST.get("first_name")
        familiya = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = Profile.objects.create_user(
                username = username,
                first_name = ism,
                last_name = familiya,
                email = email,
                password = password,
            )
            user.save()
            return HttpResponseRedirect("/")
        except:
            return HttpResponseRedirect("register_page")

def login_page(request):
    return render(request,'login.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def login(request):
    if request.method != "POST":
        return HttpResponse("Xato Sorov")
    else:
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user != None:
            auth_login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request,"Xato Kirish")
            return HttpResponseRedirect("sign_up")



def post_detail(request,year,month,day,post):
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year = year,
        publish__month = month,
        publish__day  = day
    )
    # # Comments
    comments = post.comments.filter(active=True) # #
    new_comment = None
    if request.method == 'POST': # # 
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        "post":post,
        "comments":comments,
        "new_comment":new_comment,
        "comment_form":comment_form, 
    }
    return render(request, 'blog/post/detail.html',context)




# # Email send
def post_share(request,post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST) # # formani ichida post qilinyatgon narsani ovoladi
        if form.is_valid(): # # formani togriligini tekshiradi
            cd = form.cleaned_data # # formadan xosil bolgan obektlarni dikshiniri korinishda ovoladi
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} sizga {post.title} ni o'qishni tavsiya qiladi."
            message = f"Salom, yaxshimisiz?. Quyidagi linkdagi postni o'qib ko'ring.{post_url}\n\nComents:{cd['comments']}"
            send_mail(subject,message,settings.EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',{'post':post,'form':form,'sent':sent})

def category_detail(request,id):
    category = get_object_or_404(Category,id=id)
    posts = Post.objects.filter(categroy=category)
    categories = Category.objects.all()
    context = {
        "posts":posts,
        "categories":categories
    }
    return render(request,'index.html',context)


def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    context = {
        "posts":posts
    }
    return render(request, 'my_posts.html',context)


def create_page(request):
    categories = Category.objects.all()

    return render(request, 'create_post.html',{"categories":categories})

def create_post_save(request):
    if request.method != "POST":
        return HttpResponse("Xato sorov")
    else:
        title = request.POST.get("title")
        slug = request.POST.get("slug")
        category_id = request.POST.get("category")
        category = get_object_or_404(Category, id=category_id)
        body = request.POST.get("body")
        status = request.POST.get("status")
        image = request.FILES['image']
        tags = request.POST.get("tags")
        try:
            post = Post.objects.create(
                categroy = category,
                title = title,
                slug = slug,
                author= request.user,
                body = body,
                status = status,
                image = image,
                tags = tags,
            )
            post.save()
            return HttpResponseRedirect('my_posts')
        except:
            return HttpResponseRedirect('create_page')


def post_delet(request,id):
    posts = get_object_or_404(Post,id=id)
    posts.delete()
    return HttpResponseRedirect("/my_posts")

def post_edit(request, id):
    posts = get_object_or_404(Post, id=id)
    categories = Category.objects.all()
    context = {
        'posts':posts,
        "categories":categories
    }
    return render(request, 'edit.html',context)


def edit_post_save(request):
    if request.method != "POST":
        return HttpResponse("Xato sorov")
    else:
        post_id = request.POST.get("id")
        title = request.POST.get("title")
        slug = request.POST.get("slug")
        category_id = request.POST.get("category")
        category = get_object_or_404(Category,id=category_id)
        body = request.POST.get("body")
        status = request.POST.get("status")
        tags = request.POST.get("tags")
        try:
            post = get_object_or_404(Post, id=post_id)
            post.title = title
            post.slug = slug
            post.categroy = category
            post.body = body
            post.status = status
            post.tags = tags
            post.save()
            return HttpResponseRedirect('my_posts')
        except:
            return HttpResponseRedirect('post_edit',kwargs={"id":post_id})