"""AskMax URL Configuration

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
from django.urls import path
from question_answer import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    # cписок новых вопросов(главная страница) (URL = /)
    path('', views.all_questions, name='new'),
    # cписок “лучших” вопросов(URL= /hot/)
    path('hot/<str:page>/', views.hot_questions, name='hot'),
    # cписок вопросов по тэгу(URL= /tag/blablabla/)
    path('tag/<str:tag>/', views.one_tag_page, name='tag'),
    # cтраница одного вопроса со списком ответов(URL= /question/35/)
    path('question/<int:question_id>/', views.one_question_page, name='question'),
    # форма логина(URL= /login/)
    path('login/', views.authorization_page, name='login'),
    # форма регистрации(URL= /signup/)
    path('signup/', views.register_page, name='signup'),
    # форма создания вопроса(URL= /ask/)
    path('ask/', views.adding_question, name='ask'),
    path('settings/', views.user_settings, name='settings')
]
