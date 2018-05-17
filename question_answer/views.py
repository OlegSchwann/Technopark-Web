from django.shortcuts import render
import django.http as http
import question_answer.data_prepearing as data_prepearing
import question_answer.forms as forms  # мои формы для всех приходящих данных.
import question_answer.models as models
import django.contrib.auth as auth

prepearer = data_prepearing.QuestionManager()


# Create your views here.


# главная страница '/'
# показывает заданные вопросы списком
def hot_questions(request, page=1):
    context = prepearer.new_questions(page_number=page)
    return render(request, 'question_answer/hot_questions.html', context=context)


def all_questions(request, page=1):
    context = prepearer.best_question(page_number=page)
    return render(request, 'question_answer/all_questions.html', context=context)


def adding_question(request):
    return render(request, 'question_answer/adding_question.html', {})


# форма регистрации
def register_page(request):
    # Если данный запрос типа POST, тогда
    if request.method == "POST":
        # Создаем экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = forms.SignupForm(request.POST)
        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            user = models.User.objects.create_user(
                username=form.cleaned_data['nickname'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            user.first_name = form.cleaned_data['name']
            user.save()
            profile = models.Profile()
            profile.user = user
            profile.avatar_link = 'http://localhost:8080/static/avatar.jpeg'
            # TODO: понять, как сохранить картинку из form.changed_data['avatar']
            profile.save()
            user = auth.authenticate(request, username=form.cleaned_data['nickname'], password=form.cleaned_data['password'])
            # Переход на корневую страницу
            return http.HttpResponseRedirect('/')
    else:
        form = forms.SignupForm()
    return render(request, 'question_answer/registration_form.html', {"form": form})


# форма входа
def authorization_page(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                return http.HttpResponseRedirect(form.cleaned_data['referer'])
            else:
                form.add_error(field=None, error=forms.ValidationError("Неверный логин или пароль."))
    else:
        try:
            url = request.META['HTTP_REFERER']
        except AttributeError:
            url = '/'
        form = forms.LoginForm(initial={'referer': url})
    return render(request, 'question_answer/authorization_form.html', {"form": form})

# обработчик выхода
def logout_page(request):
    if request.method == 'POST':
        auth.logout(request)
        try:
            url = request.META["HTTP_REFERER"]
        except AttributeError:
            url = '/'
        return http.HttpResponseRedirect(url)
    return http.HttpResponse(status=204)  # No content (пользователь не должен сюда заходить)

# страница одного вопроса
def one_question_page(request, question_id=1):
    context = prepearer.prepare_data_for_one_question(question_id)
    return render(request, 'question_answer/one_question_page.html', context=context)


# страница вопросов по одному тегу
def one_tag_page(request, tag, page=1):
    context = prepearer.tagged_question(tag=tag, page_number=page)
    return render(request, 'question_answer/one_tag_page.html', context=context)


# страница настроек пользователя
def user_settings(request):
    # if request.method == "POST":
    #     form = forms.SettingsForm(request.POST)
    #     if form.is_valid():
    #         pass
    # else:
    #     form = forms.SettingsForm()
    #
    # if
    return render(request, 'question_answer/user_settings.html', {})
