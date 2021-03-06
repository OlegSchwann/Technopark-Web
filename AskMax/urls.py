from django.conf import settings
from django.conf.urls.static import static

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
    path('', views.new_questions, ),
    path('<int:page>/', views.new_questions, name='new'),
    # cписок “лучших” вопросов(URL= /hot/)
    path('hot/', views.hot_questions),
    path('hot/<int:page>/', views.hot_questions, name='hot'),
    # cписок вопросов по тэгу(URL= /tag/blablabla/)
    path('tag/<str:tag>/', views.one_tag_page, name='tag'),
    path('tag/<str:tag>/<int:page>/', views.one_tag_page, name='tag_page'),
    # cтраница одного вопроса со списком ответов(URL= /question/35/)
    path('question/<int:question_id>/', views.one_question_page, name='question'),
    # форма логина(URL= /login/)
    path('login/', views.authorization_page, name='login'),
    # обработчик logout, только POST
    path('logout/', views.logout_page, name='logout'),
    # форма регистрации(URL= /signup/)
    path('signup/', views.register_page, name='signup'),
    # форма создания вопроса(URL= /ask/)
    path('ask/', views.adding_question, name='ask'),
    path('settings/', views.user_settings, name='settings'),
    # точка проставления галочки "лучший вопрос" и работы с like'ами ответов. POST only.
    path('evaluation_of_answers/', views.evaluation_of_answers, name='evaluation_of_answers'),
    # точка проставления like'ов для вопросов. POST only.
    path('evaluation_of_questions/', views.evaluation_of_questions, name='evaluation_of_questions')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
