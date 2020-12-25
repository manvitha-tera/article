from django.contrib.auth import authenticate,login
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
# Create your views here.r
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View, TemplateView
from django import http
from .models import Token,ArticleModel
from .sendingemail import send_mail
from .forms import ArticleModelForm,EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class IndexView(TemplateView):
    template_name = 'register.html'


class RegisterView(View):
    def post(self,request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')

        queryset=User.objects.filter(Q(username=username)|Q(first_name=first_name)|Q(email=email))
        if queryset:
            for i in queryset:
                if i.username==username:
                    return render(request, 'register.html',{'message' : 'this username already exists'})
                if i.first_name==first_name:
                    return render(request, 'register.html', {'message' : 'this first_name already exists'})
                if i.email==email:
                    return render(request, 'register.html', {'message' : 'this email already exists'})
        else:
            password = request.POST.get('password')
            if password:
                user = User.objects.create(first_name=first_name, last_name=last_name,username=username, email=email)
                user.set_password(password)
                user.save()
                return render(request, 'register.html',{'message':'Successfully registered, Please login.'})
            else:
                return render(request, 'register.html',{'message':'Please enter the password'})


class LoginView(TemplateView):
    template_name = 'login.html'


class LoginUser(View):
    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:
            try:
                user_object = User.objects.get(username=username)
                if user_object:
                    authenticated = authenticate(request, username=username, password=password)
                    if authenticated is not None:
                        login(request, authenticated)
                        return redirect('/dashboard/')
                    else:
                        message = 'invalid password'
                        return render(request, "login.html", {'message': message})
            except ObjectDoesNotExist:
                error = "Invalid details"
                return render(request, 'login.html', {'message1': error})
        else:
            message2 = "must enter username and password in the fields"
            return render(request, 'login.html', {'message2': message2})


# class PasswordResetForm(TemplateView):
#     template_name = 'password_reset_form.html'
#
#
# class PasswordReset(View):
#     model = Token
#
#     def post(self, request, *args, **kwargs):
#         email = request.POST.get('email')
#         queryset = User.objects.filter(email=email)
#         if queryset is not None:
#             token = Token.objects.create(user=request.user)
#             message1 = 'Subject: {}\n\n{}'.format("Reset Password Link",
#                                                   'http://127.0.0.1:8000/password_reset/')
#             message = message1 + str(token.token)
#             send_mail(message)
#             m1 = "password reset link sent to your email id please check inbox else spam in your email"
#             return render(request, 'password_reset_form.html', {"data": m1})
#         else:
#             m2 = "please enter valid email"
#             return redirect('/thanks/', {"data1": m2})
#
# class Reset(TemplateView):
#     template_name = 'password_reset_email.html'
#
#
# class Password_Reset_Done(View):
#     model = Token
#
#     def post(self, request, *args, **kwargs):
#         username = request.POST.get('username')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')
#         token = request.GET.get('token')
#         print(token)
#
#         if password1 == password2:
#             user =User.objects.get(username = request.user)
#             user.set_password(password1)
#             user.save()
#             print(request.user)
#             token = Token.objects.create(user = request.user,is_expired = True)
#             token.save()
#             return render(request, 'password_reset_complete.html')
#         else:
#             # user = User.objects.get(username=request.user)
#             return redirect('password_reset_email.html',{'name':username})


# class ProfileView(TemplateView):
#     template_name = 'profile_view.html'

# class ProfileEditView(View):
#
#     def post(self,request, *args, **kwargs):
#         email = request.POST.get("email")
#         if User.objects.filter(email=email,id= request.user.id):
#             user=User.objects.filter(username=request.user)
#             # username=""
#             # first_name=""
#             # last_name=""
#             if user:
#                 for x in user:
#                     username=x.username
#                     first_name=x.first_name
#                     last_name=x.last_name
#                     return render(request, 'profile_edit.html',
#                       {'username': username, 'first_name': first_name, 'last_name': last_name})
#         else:
#             return render(request, 'profile_view.html',{'msg':'invalid details'})
#           #  print(username,first_name,last_name)
#
#         #     username = request.POST.get("username")
#         #     email = request.POST.get("email")
#         #     first_name = request.POST.get('first_name')
#         #     last_name = request.POST.get('last_name')
#         # res = User.objects.get(username=username)
#         # if email == res.email:
#         #     User(first_name=first_name, last_name=last_name, email=email, username=username,).save()
#         #     message = "profile updated sucessfully"

def updateProfile(request):
    user = get_object_or_404(User,pk = request.user.id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
        return redirect('/dashboard/')
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'profile_edit.html',{'form':form})


# @method_decorator(login_required)
class Dashboard(ListView):
    model = ArticleModel
    template_name = 'article/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'search' in self.request.GET:
            query = self.request.GET.get('search')
            context['article'] = ArticleModel.objects.filter(author__username__icontains=query)
            # return context
        else:
            context['article'] = ArticleModel.objects.filter(published_date__lte=timezone.now())
            # return context
        graph_topics = {}
        graph_topics['News'] = ArticleModel.objects.filter(topic='news').count()
        graph_topics['Architecture'] = ArticleModel.objects.filter(topic='arch').count()
        graph_topics['Health'] = ArticleModel.objects.filter(topic='heal').count()
        context['graph'] = graph_topics
        return  context

@login_required(login_url='/login_view/')
def  article_create(request,):
    if request.method == "POST":
        article = ArticleModelForm(request.POST)
        if article.is_valid():
            post = article.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('article_preview', pk=post.pk)
    else:
        article = ArticleModelForm()
    return render(request, 'article/article_create_view.html', {'article':article})


def article_preview(request,pk):
    article = get_object_or_404(ArticleModel,pk=pk)
    # if article.author == request.user:
    return render(request, 'article/article_detail.html', {'article':article})
    # else:
    #     return http.HttpResponseForbidden('Sorry,you are not allowed to access other article.')
        # return render(request,'article/dashboard.html', {'message':'Sorry,you are not allowed to access other article.'})


# def article_delete(request,pk):
#     article = get_object_or_404(ArticleModel, pk=pk)
#     if article.author == request.user:
#         article.delete()
#         # return redirect('/dashboard/')
#         return http.HttpResponseRedirect('/dashboard/')
#     else:
#         # return http.HttpResponseForbidden("You cannot delete other's posts!")
#         return render(request,'article/article_delete.html',{'article':"You cannot delete other's posts!"})
def article_delete(request,pk):
    article = get_object_or_404(ArticleModel, pk=pk)
    if  article.author == request.user:
        if request.method == "GET":
            article.delete()
        return http.HttpResponseRedirect('/dashboard/')
    else:
        return render(request, 'article/article_delete.html', {'article': "You cannot delete other's posts!"})

def  article_update(request,pk):
    post = get_object_or_404(ArticleModel, pk=pk)
    if post.author == request.user:
        if request.method == "POST":
            article = ArticleModelForm(request.POST, instance=post)
            if article.is_valid():
                post = article.save(commit=False)
                # if post.author == request.user:
                post.save()
                return redirect('article_preview', pk=post.pk)
                    # else:
                        # return http.HttpResponseForbidden("Cannot update other's posts")
                        # return render(request, 'article/article_update.html', {'article': "You cannot update other's posts!"})
        else:
            article = ArticleModelForm(instance=post)
        return render(request, 'article/article_create_view.html', {'article':article})
    else:
        # return http.HttpResponseForbidden("You are not allowed to update other's posts")
        return render(request, 'article/article_update.html', {'article': "You cannot update other's posts!"})


def unpublished_article(request):
    articles= ArticleModel.objects.filter(published_date__isnull=True)
    return render(request,'article/unpublished_article.html',{'articles':articles})


def publish_article(request,pk):
    article = get_object_or_404(ArticleModel, pk=pk)
    article.publish()
    return redirect('/dashboard/')


def article_graph(request):
    graph_topics = {}
    graph_topics['News'] = ArticleModel.objects.filter(topic='news').count()
    graph_topics['Architecture'] = ArticleModel.objects.filter(topic='arch').count()
    graph_topics['Health'] = ArticleModel.objects.filter(topic='heal').count()
    return render(request, "pie_chart.html", {'graph_topics': graph_topics})

