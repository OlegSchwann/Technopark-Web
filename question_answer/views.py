from django.shortcuts import render
import django.http as http
import django.urls as urls
import django.contrib.auth as auth
import question_answer.models as models
import django.contrib.auth.decorators as auth_decorators
import question_answer.data_prepearing as data_prepearing
import question_answer.forms as forms  # мои формы для всех приходящих данных.
from datetime import datetime

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


@auth_decorators.login_required
def adding_question(request):
    if request.method == "POST":
        form = forms.AskForm(request.POST)
        if form.is_valid():
            # сохраняем вопрос и редиректим пользователя на новосозданную страницу
            question = models.Question.objects.create(
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                # внешний ключ пользователя, задавшего вопрос
                profile_id=request.user.profile,
                time=datetime.now())
            # работа по добавлению тегов
            for tag_text in form.cleaned_data['tags']:
                try:
                    tag = models.Tag.objects.filter(text=tag_text).get()
                except models.models.ObjectDoesNotExist:
                    tag = models.Tag(text=tag_text)
                    tag.save()
                question.tags.add(tag)
            question.save()
            http.HttpResponseRedirect('/')
            return http.HttpResponseRedirect(urls.reverse('question', args=[question.id]))
    else:
        form = forms.AskForm()
    print(form)
    return render(request, 'question_answer/adding_question.html', context={'form': form})


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
            user = auth.authenticate(request, username=form.cleaned_data['nickname'],
                                     password=form.cleaned_data['password'])
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
            user = auth.authenticate(request,
                                     username=form.cleaned_data['login'],
                                     password=form.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                return http.HttpResponseRedirect(form.cleaned_data['referer'])
            else:
                form.add_error(field=None, error=forms.ValidationError("Неверный логин или пароль."))
    else:
        url = request.META.get('HTTP_REFERER', '/')
        form = forms.LoginForm(initial={'referer': url})
    return render(request, 'question_answer/authorization_form.html', {"form": form})


# обработчик выхода
def logout_page(request):
    if request.method == 'POST':
        auth.logout(request)
        url = request.META.get("HTTP_REFERER", '/')
        return http.HttpResponseRedirect(url)
    return http.HttpResponse(status=204)  # No content (пользователь не должен сюда заходить)


# страница одного вопроса
def one_question_page(request, question_id=1):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = forms.AnswerForm(request.POST)
            if form.is_valid():
                answer = models.Answer.objects.create(
                    # непосредственно текст ответа
                    text=form.cleaned_data['answer'],
                    # внешний ключ ответившего пользователя
                    profile_id=request.user.profile,
                    # внешний ключ вопроса
                    question_id=models.Question.objects.filter(id=question_id).all()[0],
                    # время ответа
                    time=datetime.now(),
                    # флаг лучшего ответа, ответ отображается первым, если есть. Может поставить только автор вопроса
                    best_answer=False,
                    # рейтинг вопроса
                    rating=0
                )
                answer.save()
                return http.HttpResponseRedirect(
                    urls.reverse('question', args=[question_id]) + "#ansver" + str(answer.id)
                )
        else:
            form = forms.AnswerForm()
    else:
        form = forms.AnswerForm()
    context = prepearer.prepare_data_for_one_question(question_id)
    context['form'] = form
    return render(request, 'question_answer/one_question_page.html', context=context)


# страница вопросов по одному тегу
def one_tag_page(request, tag, page=1):
    context = prepearer.tagged_question(tag=tag, page_number=page)
    return render(request, 'question_answer/one_tag_page.html', context=context)


# страница настроек пользователя
@auth_decorators.login_required
def user_settings(request):
    if request.method == "POST":
        form = forms.SettingsForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.first_name = form.cleaned_data['name']
            request.user.save()
    else:
        form = forms.SettingsForm()
    return render(request, 'question_answer/user_settings.html', {"form": form})

# страница проставления галочки "лучший вопрос"
# и работы с like'ами ответов
@auth_decorators.login_required
def evaluation_of_answers(request):
    if request.method == "POST":
        form = forms.AnswerEvaluationForm(request.POST)
        if form.is_valid():
            answer = models.Answer.objects.filter(id=form.cleaned_data['ansver_id']).get()
            if form.cleaned_data['action'] == 'plus':
                try:
                    like = models.AnswerLike.objects \
                        .filter(profile_id=request.user.profile) \
                        .filter(answer_id=answer).get()
                except models.models.ObjectDoesNotExist:
                    like = models.AnswerLike.objects.create(
                        # id пользователя, поставившего оценку
                        profile_id=request.user.profile,
                        # id оцененного ответа
                        answer_id=answer,
                        # присвоенный статус: int: 1 == '+', -1 == '-'
                        status=+1
                    )
                    like.save()
                    answer.rating += 1
                    answer.save()
                else:
                    if like.status == -1:
                        like.delete()
                        answer.rating += 1
                        answer.save()
            elif form.cleaned_data['action'] == 'minus':
                try:
                    like = models.AnswerLike.objects \
                        .filter(profile_id=request.user.profile) \
                        .filter(answer_id=answer).get()
                except models.models.ObjectDoesNotExist:
                    like = models.AnswerLike.objects.create(
                        # id пользователя, поставившего оценку
                        profile_id=request.user.profile,
                        # id оцененного ответа
                        answer_id=answer,
                        # присвоенный статус: int: 1 == '+', -1 == '-'
                        status=-1
                    )
                    like.save()
                    answer.rating += -1
                    answer.save()
                else:
                    if like.status == +1:
                        like.delete()
                        answer.rating += -1
                        answer.save()
            elif form.cleaned_data['action'] == 'best':
                answer.best_answer = True
                answer.save()
            referer = request.META.get('HTTP_REFERER', '/')
            # A как тут надо поступать с запросом?
            # Eсть достаточно извращённый метод через iframe всё делать, либо js only.
            return http.HttpResponseRedirect(referer)
    return http.HttpResponse(status=204)  # No content

# работа с like'ами вопросов
@auth_decorators.login_required
def evaluation_of_questions(request):
    if request.method == "POST":
        form = forms.QuestionEvaluationForm(request.POST)
        if form.is_valid():
            question = models.Question.objects.filter(id=form.cleaned_data['question_id']).get()
            if form.cleaned_data['action'] == 'plus':
                try:
                    like = models.QuestionLike.objects \
                        .filter(profile_id=request.user.profile) \
                        .filter(question_id=question).get()
                except models.models.ObjectDoesNotExist:
                    like = models.QuestionLike.objects.create(
                        # id пользователя, поставившего оценку
                        profile_id=request.user.profile,
                        # id оцененного ответа, index
                        question_id =question,
                        # присвоенный статус: int: 1 == '+', -1 == '-'
                        status=+1
                    )
                    like.save()
                    question.rating += 1
                    question.save()
                else:
                    if like.status == -1:
                        like.delete()
                        question.rating += 1
                        question.save()
            elif form.cleaned_data['action'] == 'minus':
                try:
                    like = models.QuestionLike.objects \
                        .filter(profile_id=request.user.profile) \
                        .filter(question_id=question).get()
                except models.models.ObjectDoesNotExist:
                    like = models.QuestionLike.objects.create(
                        # id пользователя, поставившего оценку
                        profile_id=request.user.profile,
                        # id оцененного ответа
                        question_id=question,
                        # присвоенный статус: int: 1 == '+', -1 == '-'
                        status=-1
                    )
                    like.save()
                    question.rating += -1
                    question.save()
                else:
                    if like.status == +1:
                        like.delete()
                        question.rating += -1
                        question.save()
            referer = request.META.get('HTTP_REFERER', '/')
            return http.HttpResponseRedirect(referer)
    return http.HttpResponse(status=204)  # No content