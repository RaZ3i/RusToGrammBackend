pip install -r requirements.txt - установка зависимостей
(В файле много лишних зависимостей - В ДАЛЬНЕЙШЕМ УБРАТЬ!!!!!!!!!!!!!!!!!!!!)


ОПИСАНЕ API
Примечание:
    Дописать ответы в случае исключений

РАЗДЕЛ АУТЕНТИФИКАЦИИ И РЕГИСТРАЦИИ

Аутентификация
POST-метод
http://127.0.0.1:8134/auth/login/
Записывает access_token в cookie
INPUT:
    {
    "username": str,
    "password": str
    }
OUTPUT:
    {
    "success": true,
    "access token": str
    }

Регистрация
POST-метод
http://127.0.0.1:8134/auth/register/
INPUT:
    {
      "login": str,
      "phone": str,
      "email": str,
      "long_hashed_password": str,
      "short_hashed_password": str
    }
OUTPUT:
    {
    "success": true
    }

Выход
POST-метод
http://127.0.0.1:8134/auth/logout/
Удаляет access_token из cookie
OUTPUT:
    {
    "success": true
    }


РАЗДЕЛ ОПЕРАЦИЙ ПОЛЬЗОВАТЕЛЯ

Изменение информации о пользователе
PATCH-метод
http://127.0.0.1:8134/profile/modify_my_info/
Принимает access_token из cookie
INPUT:
    {
    "user_name": str | None
    "description": str | None
    "nickname": str | None
    }
OUTPUT:
    {
    "success": true,
    "changed": true
    }

Подписка на другого пользователя
POST-метод
http://127.0.0.1:8134/profile/subscribe_at/{sub_id}
Принимает access_token из cookie
INPUT:
    {
    "sub_id": int
    }
OUTPUT:
    {
    "success": true,
    }

Загрузка аватара
POST-метод
http://127.0.0.1:8134/profile/upload_avatar
Принимает access_token из cookie
INPUT:
    {
    "avatar": jpeg/png
    }
OUTPUT:
    {
    "success": true,
    "avatar_link": str
    }
Примечание:
    Необходмо доделать проверку на расширение загружаемого файла.

Создание поста
POST-метод
http://127.0.0.1:8134/profile/creat_post
Принимает access_token из cookie
INPUT:
    {
    "description": str,
    "files": list[jpeg/png]
    }
OUTPUT:
    {
    "success": true
    }
Примечание:
    В данный момент функция работает не совсем корректно.
    При загрузке больше 10 файлов не срабатывает исключение.
    Необходимо доделать.


РАЗДЕЛ ИНФОРМАЦИИ О ПОЛЬЗОВАТЕЛЕ

Получение информации о пользователе по его id
GET-метод
http://127.0.0.1:8134/profile/get_user_info_by_id/{user_id}
INPUT:
    {
    "user_id": int
    }
OUTPUT:
    {
      "user_id": int,
      "id": int,
      "user_name": str,
      "description": str,
      "private_account": bool,
      "user_profile_id": int,
      "nickname": str,
      "avatar_link": str | null
    }

Получение аватара пользователя по его id
GET-метод
http://127.0.0.1:8134/profile/get_avatar_by_id/{user_id}
INPUT:
    {
    "user_id": int
    }
OUTPUT:
    jpeg/png

Получения списка подписок пользователя
GET-метод
http://127.0.0.1:8134/profile/subscribes_list/
В данный момент функция принимает access_token из cookie.
Необходмо переделать, чтобы функция принимала user_id
OUTPUT:
    [
      {
        "user_id": int,
        "nickname": str,
        "avatar_link": str | null
      },
      {
        "user_id": int,
        "nickname": str,
        "avatar_link": str | null
      },
        ...
    ]

Получения кол-ва подписок пользователя
GET-метод
http://127.0.0.1:8134/profile/subscribes_count/
В данный момент функция принимает access_token из cookie.
Необходмо переделать, чтобы функция принимала user_id
OUTPUT:
    {
    "count": int,
    "success": true
    }

Получения списка подписчиков пользователя
GET-метод
http://127.0.0.1:8134/profile/subscribers_list/
В данный момент функция принимает access_token из cookie.
Необходмо переделать, чтобы функция принимала user_id
OUTPUT:
    [
      {
        "user_id": int,
        "nickname": str,
        "avatar_link": str | null
      },
      {
        "user_id": int,
        "nickname": str,
        "avatar_link": str | null
      },
        ...
    ]

Получения кол-ва подписчиков пользователя
GET-метод
http://127.0.0.1:8134/profile/subscribers_count/
В данный момент функция принимает access_token из cookie.
Необходмо переделать, чтобы функция принимала user_id
OUTPUT:
    {
    "count": int,
    "success": true
    }

Получение информации о текущем пользователе
GET-метод
http://127.0.0.1:8134/profile/subscribers_count/
Принимает access_token из cookie.
OUTPUT:
    {
      "user_id": int,
      "user_name": str,
      "description": str,
      "nickname": str,
      "private_account": bool,
      "avatar_link": str | null
    }

Получение списка пользователей
GET-метод
http://127.0.0.1:8134/profile/users_list/
INPUT:
    {
    "page": int,
    "perpage": int
    }
OUTPUT:
    [
        {
          "user_id": int,
          "user_name": str,
          "description": str,
          "nickname": str,
          "private_account": bool,
          "avatar_link": str | null
        },
        ...
    ]
Примечание:
    page:
        default = 1
        max = 50
        min = 1
    perpage:
        default = 3
        max = 100
        min = 1
