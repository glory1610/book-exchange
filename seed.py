"""
Скрипт для заповнення бази даних тестовими даними.
"""

import mysql.connector
import random
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

# Конфігурація бази даних
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'SQL1610@slava',
    'database': 'book_exchange'
}

# Список регіонів України
regions = ["Київ", "Львів", "Одеса", "Харків", "Дніпро", "Запоріжжя", "Рівне", "Миколаїв", "Хмельницький", "Луцьк"]

# Список емодзі для аватарок
avatars = ["👨", "👩", "🧑", "👦", "👧", "👨‍🦰", "👩‍🦰", "👨‍🦱", "👩‍🦱", "👨‍🦲",
           "👩‍🦲", "👨‍🦳", "👩‍🦳", "🧔", "🧑‍🦰", "🧑‍🦱", "🧑‍🦲", "🧑‍🦳"]

# Дані для користувачів
users_data = [
    {"username": "book_lover", "email": "book_lover@example.com", "password": "password1",
     "full_name": "Іван Петренко", "phone_number": "+380991234567"},
    {"username": "reader2022", "email": "reader2022@example.com", "password": "password2",
     "full_name": "Марія Коваленко", "phone_number": "+380992234567"},
    {"username": "lit_fan", "email": "lit_fan@example.com", "password": "password3",
     "full_name": "Олег Сидоренко", "phone_number": "+380993234567"},
    {"username": "bookworm", "email": "bookworm@example.com", "password": "password4",
     "full_name": "Анна Шевченко", "phone_number": "+380994234567"},
    {"username": "page_turner", "email": "page_turner@example.com", "password": "password5",
     "full_name": "Віктор Мельник", "phone_number": "+380995234567"},
    {"username": "novel_reader", "email": "novel_reader@example.com", "password": "password6",
     "full_name": "Наталія Бондаренко", "phone_number": "+380996234567"},
    {"username": "story_lover", "email": "story_lover@example.com", "password": "password7",
     "full_name": "Андрій Кравченко", "phone_number": "+380997234567"},
    {"username": "ukr_books", "email": "ukr_books@example.com", "password": "password8",
     "full_name": "Софія Ткаченко", "phone_number": "+380998234567"},
    {"username": "lit_master", "email": "lit_master@example.com", "password": "password9",
     "full_name": "Максим Лисенко", "phone_number": "+380999234567"},
    {"username": "poetry_fan", "email": "poetry_fan@example.com", "password": "password10",
     "full_name": "Юлія Попович", "phone_number": "+380990234567"},
    {"username": "classic_reader", "email": "classic_reader@example.com", "password": "password11",
     "full_name": "Дмитро Савченко", "phone_number": "+380991134567"},
    {"username": "book_collector", "email": "book_collector@example.com", "password": "password12",
     "full_name": "Олена Григоренко", "phone_number": "+380992134567"},
    {"username": "fantasy_reader", "email": "fantasy_reader@example.com", "password": "password13",
     "full_name": "Ігор Захарченко", "phone_number": "+380993134567"},
    {"username": "sci_fi_lover", "email": "sci_fi_lover@example.com", "password": "password14",
     "full_name": "Валентина Романенко", "phone_number": "+380994134567"},
    {"username": "history_buff", "email": "history_buff@example.com", "password": "password15",
     "full_name": "Сергій Павленко", "phone_number": "+380995134567"}
]

# Дані для книг
books_data = [
    {"title": "Кобзар", "author": "Тарас Шевченко", "genre_id": 11,
     "description": "Збірка поетичних творів Тараса Шевченка."},
    {"title": "Лісова пісня", "author": "Леся Українка", "genre_id": 12,
     "description": "Драма-феєрія про кохання між лісовою міфічною істотою і людиною."},
    {"title": "Зів'яле листя", "author": "Іван Франко", "genre_id": 11,
     "description": "Збірка ліричних поезій про нещасливе кохання."},
    {"title": "Тореадори з Васюківки", "author": "Всеволод Нестайко", "genre_id": 13,
     "description": "Пригоди двох друзів-підлітків з українського села."},
    {"title": "Земля", "author": "Ольга Кобилянська", "genre_id": 5,
     "description": "Соціально-психологічна повість про трагедію селянської родини."},
    {"title": "Чорна рада", "author": "Пантелеймон Куліш", "genre_id": 5,
     "description": "Історичний роман про події в Україні після смерті Богдана Хмельницького."},
    {"title": "Місто", "author": "Валер'ян Підмогильний", "genre_id": 12,
     "description": "Роман про становлення молодої людини в місті."},
    {"title": "Intermezzo", "author": "Михайло Коцюбинський", "genre_id": 12,
     "description": "Новела про відновлення духовних сил людини на лоні природи."},
    {"title": "Мина Мазайло", "author": "Микола Куліш", "genre_id": 12,
     "description": "Комедія про українізацію та ставлення до національного питання."},
    {"title": "1984", "author": "Джордж Орвелл", "genre_id": 1,
     "description": "Роман-антиутопія про тоталітарне суспільство."},
    {"title": "Гаррі Поттер і філософський камінь", "author": "Дж. К. Роулінг", "genre_id": 2,
     "description": "Перша книга серії про юного чарівника."},
    {"title": "Володар перснів", "author": "Дж. Р. Р. Толкін", "genre_id": 2,
     "description": "Епічний роман у жанрі фентезі."},
    {"title": "Майстер і Маргарита", "author": "Михайло Булгаков", "genre_id": 12,
     "description": "Роман про візит диявола в Москву."},
    {"title": "Злочин і кара", "author": "Федір Достоєвський", "genre_id": 12,
     "description": "Психологічний роман про моральні дилеми."},
    {"title": "Маленький принц", "author": "Антуан де Сент-Екзюпері", "genre_id": 13,
     "description": "Філософська казка для дітей і дорослих."},
    {"title": "Сто років самотності", "author": "Габріель Гарсія Маркес", "genre_id": 12,
     "description": "Роман у стилі магічного реалізму."},
    {"title": "Гордість та упередження", "author": "Джейн Остін", "genre_id": 3,
     "description": "Роман про життя англійської провінції початку XIX століття."},
    {"title": "Хіба ревуть воли, як ясла повні", "author": "Панас Мирний", "genre_id": 12,
     "description": "Соціально-психологічний роман про долю селянина."},
    {"title": "Тіні забутих предків", "author": "Михайло Коцюбинський", "genre_id": 12,
     "description": "Повість про кохання на тлі гуцульських традицій."},
    {"title": "7 звичок надзвичайно ефективних людей", "author": "Стівен Кові", "genre_id": 20,
     "description": "Книга про особистісний розвиток."},
    {"title": "Sapiens: Коротка історія людства", "author": "Ювал Ной Харарі", "genre_id": 7,
     "description": "Книга про еволюцію людства від давніх часів до сьогодення."},
    {"title": "Атлант розправив плечі", "author": "Айн Ренд", "genre_id": 12,
     "description": "Філософський роман про індивідуалізм."},
    {"title": "Тихий Дон", "author": "Михайло Шолохов", "genre_id": 5,
     "description": "Роман про життя донських козаків."},
    {"title": "Війна і мир", "author": "Лев Толстой", "genre_id": 5,
     "description": "Історичний роман про Росію під час наполеонівських війн."},
    {"title": "Ідіот", "author": "Федір Достоєвський", "genre_id": 12,
     "description": "Роман про доброго і чесного князя Мишкіна."},
    {"title": "Собаче серце", "author": "Михайло Булгаков", "genre_id": 1,
     "description": "Сатирична повість про експеримент професора Преображенського."},
    {"title": "Марсіанин", "author": "Енді Вейр", "genre_id": 1,
     "description": "Роман про астронавта, якого помилково вважають загиблим і залишають на Марсі."},
    {"title": "Зелені пагорби Африки", "author": "Ернест Хемінгуей", "genre_id": 7,
     "description": "Нефікційна книга про африканське сафарі."},
    {"title": "Мистецтво війни", "author": "Сунь-Цзи", "genre_id": 16,
     "description": "Давньокитайський трактат про військову стратегію."},
    {"title": "Джейн Ейр", "author": "Шарлотта Бронте", "genre_id": 12,
     "description": "Роман про життя і кохання сироти Джейн Ейр."},
    {"title": "Камінний хрест", "author": "Василь Стефаник", "genre_id": 12,
     "description": "Збірка новел про життя галицького селянства."},
    {"title": "Хмельницький", "author": "Іван Нечуй-Левицький", "genre_id": 5,
     "description": "Історичний роман про Богдана Хмельницького."},
    {"title": "Диво", "author": "Павло Загребельний", "genre_id": 5,
     "description": "Роман про будівництво Софіївського собору."},
    {"title": "Рекреації", "author": "Юрій Андрухович", "genre_id": 12,
     "description": "Постмодерністський роман про літературний фестиваль."},
    {"title": "Солодка Даруся", "author": "Марія Матіос", "genre_id": 12,
     "description": "Драма про трагічну долю дівчини в буковинському селі."},
    {"title": "Чорний ворон", "author": "Василь Шкляр", "genre_id": 5,
     "description": "Історичний роман про повстанський рух в Україні 1920-х років."},
    {"title": "Дім на горі", "author": "Валерій Шевчук", "genre_id": 12,
     "description": "Роман-балада про українське провінційне місто."},
    {"title": "Лебедина зграя", "author": "Василь Земляк", "genre_id": 12,
     "description": "Роман про життя українського села."},
    {"title": "Польові дослідження з українського сексу", "author": "Оксана Забужко", "genre_id": 12,
     "description": "Автобіографічний роман-есе."},
    {"title": "Нація", "author": "Марія Матіос", "genre_id": 12,
     "description": "Збірка новел про долю української нації."},
    {"title": "Записки українського самашедшого", "author": "Ліна Костенко", "genre_id": 12,
     "description": "Роман-щоденник інтелігента часів незалежності."},
    {"title": "Я, Побєда і Берлін", "author": "Кузьма Скрябін", "genre_id": 7,
     "description": "Автобіографічна книга про подорож до Німеччини."},
    {"title": "Місто", "author": "Валер'ян Підмогильний", "genre_id": 12,
     "description": "Роман про життя молодого сільського хлопця в Києві."},
    {"title": "Вершники", "author": "Юрій Яновський", "genre_id": 12,
     "description": "Роман у новелах про громадянську війну в Україні."},
    {"title": "Людина в пошуках справжнього сенсу", "author": "Віктор Франкл", "genre_id": 14,
     "description": "Книга про досвід виживання в концтаборі та пошук сенсу життя."},
    {"title": "Думай повільно... вирішуй швидко", "author": "Деніел Канеман", "genre_id": 14,
     "description": "Книга про два типи мислення та прийняття рішень."},
    {"title": "21 урок для 21 століття", "author": "Ювал Ной Харарі", "genre_id": 6,
     "description": "Книга про виклики сучасного світу."}
]


# Функція для підключення до бази даних
def connect_to_db():
    try:
        connection = mysql.connector.connect(**db_config)
        print("З'єднання з базою даних успішно встановлено")
        return connection
    except mysql.connector.Error as e:
        print(f"Помилка підключення до бази даних: {e}")
        return None


# Функція для додавання тестових користувачів
def add_users(connection):
    cursor = connection.cursor()
    user_ids = []

    try:
        for user in users_data:
            # Додаємо випадковий регіон та аватарку
            region = random.choice(regions)
            avatar_symbol = random.choice(avatars)

            # Хешування пароля
            hashed_password = generate_password_hash(user["password"])
            # Виконуємо запит
            cursor.execute(
                """INSERT INTO users 
                   (username, email, password, full_name, phone_number, region, avatar_symbol) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE
                       password = VALUES(password),
                       full_name = VALUES(full_name),
                       phone_number = VALUES(phone_number),
                       region = VALUES(region),
                       avatar_symbol = VALUES(avatar_symbol)""",
                (user["username"], user["email"], hashed_password,
                 user["full_name"], user["phone_number"], region, avatar_symbol)
            )

            user_ids.append(cursor.lastrowid)

        connection.commit()
        print(f"Додано {len(users_data)} користувачів")
        return user_ids
    except mysql.connector.Error as e:
        print(f"Помилка при додаванні користувачів: {e}")
        connection.rollback()
        return []
    finally:
        cursor.close()


# Функція для додавання тестових книг
def add_books(connection, user_ids):
    cursor = connection.cursor()
    book_ids = []

    try:
        for book in books_data:
            # Обираємо випадкового власника
            owner_id = random.choice(user_ids)
            is_free = random.choice([True, False])

            status_options = ["доступна", "доступна", "зарезервована"]
            status = random.choice(status_options)

            # Виконуємо запит
            cursor.execute(
                """INSERT INTO books 
                   (title, author, description, genre_id, owner_id, is_free, status) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (book["title"], book["author"], book["description"],
                 book["genre_id"], owner_id, is_free, status)
            )
            book_ids.append(cursor.lastrowid)

        connection.commit()
        print(f"Додано {len(books_data)} книг")
        return book_ids
    except mysql.connector.Error as e:
        print(f"Помилка при додаванні книг: {e}")
        connection.rollback()
        return []
    finally:
        cursor.close()


# Функція для додавання відгуків про книги
def add_book_reviews(connection, user_ids, book_ids):
    cursor = connection.cursor()
    review_count = 0

    try:
        # Додаємо від 20 до 40 випадкових відгуків
        for _ in range(random.randint(20, 40)):
            book_id = random.choice(book_ids)

            # Отримуємо інформацію про власника книги
            cursor.execute("SELECT owner_id FROM books WHERE id = %s", (book_id,))
            owner_id = cursor.fetchone()[0]

            # Обираємо випадкового користувача, який не є власником
            available_users = [user_id for user_id in user_ids if user_id != owner_id]
            if not available_users:
                continue

            user_id = random.choice(available_users)
            rating = random.randint(3, 5)  # Більше позитивних відгуків

            comments = [
                "Чудова книга! Рекомендую всім.",
                "Одна з моїх улюблених книг.",
                "Цікавий сюжет, але трохи затягнуто.",
                "Дуже сподобалась, особливо головний герой.",
                "Читається легко, отримав задоволення.",
                "Не міг відірватися, поки не дочитав до кінця.",
                "Гарний стиль написання, рекомендую.",
                "Сподобалося, але очікував більшого.",
                "Дуже цікава книга з непередбачуваним фіналом.",
                "Варто прочитати хоча б раз у житті."
            ]
            comment = random.choice(comments)

            # Перевіряємо, чи не залишав цей користувач вже відгук
            cursor.execute(
                "SELECT id FROM book_reviews WHERE book_id = %s AND user_id = %s",
                (book_id, user_id)
            )
            if cursor.fetchone():
                continue

            # Додаємо відгук
            cursor.execute(
                """INSERT INTO book_reviews 
                   (user_id, book_id, rating, comment) 
                   VALUES (%s, %s, %s, %s)""",
                (user_id, book_id, rating, comment)
            )
            review_count += 1

        # Оновлюємо рейтинги книг
        cursor.execute("""
            UPDATE books b 
            SET rating = (SELECT AVG(rating) FROM book_reviews WHERE book_id = b.id),
                rating_count = (SELECT COUNT(*) FROM book_reviews WHERE book_id = b.id)
            WHERE b.id IN (SELECT book_id FROM book_reviews GROUP BY book_id)
        """)

        connection.commit()
        print(f"Додано {review_count} відгуків про книги")
    except mysql.connector.Error as e:
        print(f"Помилка при додаванні відгуків про книги: {e}")
        connection.rollback()
    finally:
        cursor.close()


# Функція для додавання бажань
def add_wishlist_items(connection, user_ids):
    cursor = connection.cursor()
    wishlist_count = 0

    try:
        # Кожен користувач має від 1 до 5 бажань
        for user_id in user_ids:
            num_wishes = random.randint(1, 5)

            for _ in range(num_wishes):
                book = random.choice(books_data)
                title = book["title"]
                author = book["author"]
                genre_id = book["genre_id"]

                # Перевіряємо, чи вже є таке бажання
                cursor.execute(
                    """SELECT id FROM wishlist 
                       WHERE user_id = %s AND title = %s AND author = %s""",
                    (user_id, title, author)
                )
                if cursor.fetchone():
                    continue

                # Додаємо бажання
                cursor.execute(
                    """INSERT INTO wishlist 
                       (user_id, title, author, genre_id) 
                       VALUES (%s, %s, %s, %s)""",
                    (user_id, title, author, genre_id)
                )
                wishlist_count += 1

        connection.commit()
        print(f"Додано {wishlist_count} елементів списку бажаного")
    except mysql.connector.Error as e:
        print(f"Помилка при додаванні списку бажаного: {e}")
        connection.rollback()
    finally:
        cursor.close()


# Функція для додавання обмінів
def add_exchanges(connection, user_ids, book_ids):
    cursor = connection.cursor()
    exchange_count = 0

    exchange_ids = []

    try:
        # Додаємо від 10 до 15 випадкових обмінів
        for _ in range(random.randint(10, 15)):
            # Обираємо випадкову книгу
            book_id = random.choice(book_ids)

            # Отримуємо інформацію про власника книги
            cursor.execute("SELECT owner_id, status FROM books WHERE id = %s", (book_id,))
            result = cursor.fetchone()
            owner_id, status = result

            # Якщо книга вже видана, пропускаємо
            if status == "підтверджена":
                continue

            # Обираємо випадкового позичальника, який не є власником
            available_users = [user_id for user_id in user_ids if user_id != owner_id]
            if not available_users:
                continue

            borrower_id = random.choice(available_users)

            # Обираємо випадковий статус обміну
            exchange_status_options = ["запит", "прийнято", "відхилено", "отримано"]
            exchange_status = random.choice(exchange_status_options)

            # Визначаємо дати
            start_date = datetime.now() - timedelta(days=random.randint(1, 30))
            end_date = None
            if exchange_status == "отримано":
                end_date = start_date + timedelta(days=random.randint(5, 15))

            # Оновлюємо статус книги в залежності від статусу обміну
            book_status = "доступна"
            if exchange_status == "запит":
                book_status = "зарезервована"
            elif exchange_status == "прийнято":
                book_status = "підтверджена"

            cursor.execute(
                "UPDATE books SET status = %s WHERE id = %s",
                (book_status, book_id)
            )

            # Додаємо обмін
            if end_date:
                cursor.execute(
                    """INSERT INTO exchanges 
                       (book_id, borrower_id, status, start_date, end_date) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (book_id, borrower_id, exchange_status, start_date, end_date)
                )
            else:
                cursor.execute(
                    """INSERT INTO exchanges 
                       (book_id, borrower_id, status, start_date) 
                       VALUES (%s, %s, %s, %s)""",
                    (book_id, borrower_id, exchange_status, start_date)
                )

            exchange_id = cursor.lastrowid
            exchange_ids.append((exchange_id, owner_id, borrower_id, exchange_status))
            exchange_count += 1

        connection.commit()
        print(f"Додано {exchange_count} обмінів")
        return exchange_ids
    except mysql.connector.Error as e:
        print(f"Помилка при додаванні обмінів: {e}")
        connection.rollback()
        return []
    finally:
        cursor.close()


# Функція для додавання повідомлень
def add_messages(connection, exchange_data):
    cursor = connection.cursor()
    message_count = 0

    try:
        for exchange_id, owner_id, borrower_id, status in exchange_data:
            # Кількість повідомлень залежить від статусу обміну
            if status == "запит":
                message_count_range = (1, 3)
            elif status == "прийнято":
                message_count_range = (2, 5)
            elif status == "відхилено":
                message_count_range = (1, 2)
            else:  # повернуто
                message_count_range = (3, 7)

            num_messages = random.randint(*message_count_range)

            for i in range(num_messages):
                # Визначаємо відправника і отримувача
                if i % 2 == 0:
                    sender_id = borrower_id
                    receiver_id = owner_id
                else:
                    sender_id = owner_id
                    receiver_id = borrower_id

                # Тексти повідомлень залежать від статусу і номера повідомлення
                if status == "запит":
                    messages = [
                        "Доброго дня! Мене цікавить ваша книга. Чи можна її позичити?",
                        "Так, звичайно. Коли вам зручно зустрітися?",
                        "Може в середу після обіду?"
                    ]
                elif status == "прийнято":
                    messages = [
                        "Дякую, що погодились дати книгу!",
                        "Нема за що. Сподіваюся, вона вам сподобається.",
                        "Коли планується повернення?",
                        "Десь через два тижні, якщо вам підходить.",
                        "Так, цілком. Приємного читання!"
                    ]
                elif status == "відхилено":
                    messages = [
                        "На жаль, не можу дати книгу зараз.",
                        "Розумію, дякую за відповідь."
                    ]
                else:  # повернуто
                    messages = [
                        "Хотів би повернути книгу. Коли вам зручно?",
                        "Завтра після роботи підійде.",
                        "Чудово, тоді до завтра!",
                        "Книга сподобалась?",
                        "Так, дуже! Особливо сподобався головний герой.",
                        "Радий, що вам сподобалось. Є ще кілька подібних книг, якщо цікаво.",
                        "Обов'язково гляну. Дякую за рекомендацію!"
                    ]

                # Обираємо повідомлення в залежності від номера
                if i < len(messages):
                    message_text = messages[i]
                else:
                    message_texts = [
                        "Дякую за співпрацю!",
                        "Завжди радий допомогти.",
                        "Чи є у вас ще цікаві книги?",
                        "Так, маю кілька. Подивіться мій профіль.",
                        "Обов'язково подивлюсь."
                    ]
                    message_text = random.choice(message_texts)

                # Час повідомлення
                message_time = datetime.now() - timedelta(days=random.randint(1, 20),
                                                          hours=random.randint(0, 23),
                                                          minutes=random.randint(0, 59))

                # Статус прочитання
                is_read = random.choice([True, True, True, False])  # 75% прочитаних

                # Додаємо повідомлення
                cursor.execute(
                    """INSERT INTO messages 
                       (sender_id, receiver_id, content, is_read, created_at) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (sender_id, receiver_id, message_text, is_read, message_time)
                )
                message_count += 1

        connection.commit()
        print(f"Додано {message_count} повідомлень")
    except mysql.connector.Error as e:
        print(f"Помилка при додаванні повідомлень: {e}")
        connection.rollback()
    finally:
        cursor.close()


# Функція для додавання відгуків про користувачів
def add_user_reviews(connection, exchange_data):
    cursor = connection.cursor()
    review_count = 0

    try:
        for _, owner_id, borrower_id, status in exchange_data:
            if status != "отримано":
                continue  # Відгуки можна залишати тільки після завершення обміну

            # Визначаємо, хто кому залишає відгук (власник позичальнику і навпаки)
            review_pairs = [(owner_id, borrower_id), (borrower_id, owner_id)]

            for reviewer_id, user_id in review_pairs:
                # Вирішуємо, чи залишати відгук (80% ймовірність)
                if random.random() > 0.8:
                    continue

                # Перевіряємо, чи не залишав вже відгук
                cursor.execute(
                    "SELECT id FROM user_reviews WHERE reviewer_id = %s AND user_id = %s",
                    (reviewer_id, user_id)
                )
                if cursor.fetchone():
                    continue

                # Обираємо рейтинг (більше високих оцінок)
                rating = random.randint(4, 5) if random.random() < 0.8 else random.randint(1, 3)

                # Обираємо коментар
                positive_comments = [
                    "Чудовий користувач, все пройшло гладко.",
                    "Дуже пунктуальна і відповідальна людина.",
                    "Рекомендую! Книгу повернув вчасно і в гарному стані.",
                    "Приємно мати справу з такими людьми.",
                    "Все відмінно, обов'язково співпрацюватиму ще.",
                    "Дякую за хороший обмін!"
                ]

                neutral_comments = [
                    "Нормальний обмін, без проблем.",
                    "Все відбулося за домовленістю.",
                    "Загалом все добре.",
                    "Книгу повернув, хоча трохи пізніше домовленого терміну."
                ]

                negative_comments = [
                    "На жаль, книгу повернув із запізненням.",
                    "Книга повернута в не найкращому стані.",
                    "Складно було домовитися про час зустрічі.",
                    "Комунікація могла бути кращою."
                ]

                if rating >= 4:
                    comment = random.choice(positive_comments)
                elif rating == 3:
                    comment = random.choice(neutral_comments)
                else:
                    comment = random.choice(negative_comments)

                # Додаємо відгук
                cursor.execute(
                    """INSERT INTO user_reviews 
                       (reviewer_id, user_id, rating, comment) 
                       VALUES (%s, %s, %s, %s)""",
                    (reviewer_id, user_id, rating, comment)
                )
                review_count += 1

        # Оновлюємо рейтинги користувачів
        cursor.execute("""
            UPDATE users u 
            SET rating = (SELECT AVG(rating) FROM user_reviews WHERE user_id = u.id),
                rating_count = (SELECT COUNT(*) FROM user_reviews WHERE user_id = u.id)
            WHERE u.id IN (SELECT user_id FROM user_reviews GROUP BY user_id)
        """)

        connection.commit()
        print(f"Додано {review_count} відгуків про користувачів")
    except mysql.connector.Error as e:
        print(f"Помилка при додаванні відгуків про користувачів: {e}")
        connection.rollback()
    finally:
        cursor.close()


# Основна функція
def main():
    connection = connect_to_db()
    if not connection:
        return

    try:
        print("Заповнення бази даних тестовими даними...")
        user_ids = add_users(connection)
        if not user_ids:
            return

        book_ids = add_books(connection, user_ids)
        if not book_ids:
            return

        add_book_reviews(connection, user_ids, book_ids)
        add_wishlist_items(connection, user_ids)

        exchange_data = add_exchanges(connection, user_ids, book_ids)
        if exchange_data:
            add_messages(connection, exchange_data)
            add_user_reviews(connection, exchange_data)

        print("Заповнення бази даних успішно завершено!")
    except Exception as e:
        print(f"Помилка при заповненні бази даних: {e}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()