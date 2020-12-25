"""Article_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from app_article import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),

    # path('article_list/', views.ArticleList.as_view()),
    # path('article_preview/<int:pk>/', views.ArticlePreView.as_view(), name ='article_preview'),
    # path('article_create/', views.ArticleCreateView.as_view(), name='article_create'),
    #
    # path('author_filter_list/', views.AuthorFilter),
    #
    # path('article/update/<int:pk>/', views.ArticleUpdate.as_view(),name='article_update'),
    # path('article/delete/<int:pk>/', views.ArticleDelete.as_view(),name='article_delete'),


    path('', views.IndexView.as_view()),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login_view/', views.LoginView.as_view(), name='login_view'),
    path('login_post_view/', views.LoginUser.as_view(), name='login_post_view'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html',
                                                                 email_template_name='password_reset_email.html',
                                                                 subject_template_name='password_reset_subject.txt'),
                                                                 name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
                                                                          name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
                                                     name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
                                                                     name='password_reset_complete'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name = 'password_change.html'),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name = 'password_change_done.html'),
         name='password_change_done'),

    # path('profile_view/', views.ProfileView.as_view(), name='profile_view'),
    # path('profile_edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('update_profile/', views.updateProfile, name='update_profile'),
    path('dashboard/', views.Dashboard.as_view(), name ='dashboard'),
    path('article_create/', views.article_create, name ='article_create'),
    path('article_preview/<int:pk>/', views.article_preview, name ='article_preview'),
    path('article/<int:pk>/delete/', views.article_delete, name ='article_delete'),
    path('article/update/<int:pk>/', views.article_update, name ='article_update'),
    path('unpublished_article/', views.unpublished_article, name ='unpublished_article'),
    path('publish_article/<int:pk>/', views.publish_article, name ='publish_article'),

    # path('article_graph/', views.article_graph, name = 'article_graph' ),

]
