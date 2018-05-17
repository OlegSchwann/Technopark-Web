import django.forms as forms
from django.core.exceptions import ValidationError
import question_answer.models as models

# Форма логина. Располагается по URL /login/. Пользователь логин/пароль.
# Дополнительно в GET параметрах передается параметр continue -
# URL на который нужно отправить пользователя после успешной авторизации.
# При неудачной авторизации нужно отображать сообщение об ошибке.

class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField()
    referer = forms.CharField(required=False)  # куда переадресовать пользователя после регистрации.



# Форма регистрации. Располагается по URL /signup/.
# Пользователь вводит все необходимые поля (email, имя, пароль).
# После успешной регистрации отправляется на главную страницу.
class SignupForm(forms.Form):
    nickname = forms.CharField()
    name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    confirm_password = forms.CharField()
    avatar = forms.ImageField(required=False)

    # Валидация проходит в этом методе
    def clean(self):
        # Определяем правило валидации
        if self.cleaned_data.get('password') != self.cleaned_data.get('confirm_password'):
            # Выбрасываем ошибку, если пароли не совпали
            raise forms.ValidationError('Пароли не совпадают.')
        return self.cleaned_data

    # валидация длинны пароля
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password.__len__() < 10:
            raise forms.ValidationError(
                'Пароль слишком короткий, < 10 символов. '
                '<a href="https://xkcd.ru/936/">Несколько несвязных слов будут хорошим паролем.</a>')
        return password

    def clean_nickname(self):
        # осуществляем проверку на уникальность имени.
        nickname = self.cleaned_data.get('nickname')
        nickname_count = models.User.objects.filter(username=nickname).count()
        if nickname_count > 0:
            raise forms.ValidationError("Имя уже используется, попоробуйте другое.")
        return nickname

# Сылка "выход". Располагается на каждой странице в шапке сайта.
# Видна только авторизованным пользователям.
# После выхода пользователь остается на текущей странице.



# Форма редактирования профиля. Располагается по URL /profile/edit.
# Доступна только для авторизованоого пользователя.
# Пользователь видит все необходимые поля: email, nick, avatar.
# После сохранения остается на странице.

class SettingsForm(forms.Form):
    email = forms.EmailField()
    nickname = forms.CharField()
    name = forms.CharField()

# Форма добавления вопроса. Располагается по URL /ask/.
# Пользователь вводит название, текст и тэги вопроса.
# После успешного добавления отправляется на страницу вопроса.



# Форма добавления ответа. Располагается на странице вопроса URL /question/<id>.
# Пользователь вводит только текст ответа.
# После успешного добавления необходимо отправить пользователя на нужную старницу ответов данного вопроса
# и проскролить страницу так, чтобы добавленный ответ был виден.
