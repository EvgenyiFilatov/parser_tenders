# Проект Сбор тендеров

Этот проект описывает процесс сбора информации о тендерах с [веб-сайта](https://rostender.info/extsearch?page=1) и сохранения этих данных в базе данных SQLite. Также предоставляется возможность взаимодействовать с этой базой данных через командную строку или веб-интерфейс с использованием FastAPI.

## Основные компоненты проекта

### 1. parse_tenders.py

Этот файл содержит скрипт для парсинга тендеров и их сохранения в базу данных:

- Импортируемые библиотеки:
  - requests для выполнения HTTP-запросов.
  - BeautifulSoup для парсинга HTML-страниц.
  - sqlite3 для работы с базой данных SQLite.

- Функция parse_tenders:
  - Создает таблицу tenders в базе данных (если она не существует).
  - Удаляет все существующие записи в таблице перед началом парсинга.
  - Цикл while используется для перехода через страницы с тендерами до достижения максимального количества тендеров (MAX_TENDERS).
  - Для каждого тендера извлекаются и сохраняются следующие данные:
    - Номер тендера.
    - Название.
    - Адрес доставки.
    - Начальная цена.
    - Категории заказчиков.
    - Ссылка на тендер.

### 2. tender_cli.py

Этот скрипт предоставляет интерфейс командной строки для взаимодействия с базой данных:

- Импортируемые библиотеки:
  - argparse для обработки аргументов командной строки.
  - sqlite3 для работы с базой данных SQLite.

- Функция main:
  - Определяет аргумент командной строки --limit для лимитирования количества выводимых тендеров.
  - Получает данные из базы данных и выводит их в формате таблицы.
  - Ограничивает длину выводимых данных с помощью срезов.

### 3. main.py

Этот файл используется для создания веб-сервиса на базе FastAPI для доступа к данным тендеров через HTTP-запросы:

- Импортируемые библиотеки:
  - FastAPI для создания веб-приложений.
  - sqlite3 для работы с базой данных SQLite.
  - parse_tenders импортируется для запуска функции парсинга.

- Главная логика:
  - Веб-сервис запускается на событии старта программы и вызывает функцию parse_tenders.
  - Создается GET-эндпоинт /tenders, который возвращает список тендеров из базы данных, принимая параметр limit для ограничения количества возвращаемых записей.

## Установка и использование
Склонируйте репозиторий:

    https://github.com/EvgenyiFilatov/parser_tenders.git

### Требования

Установите зависимости проекта:
  
    pip install -r requirements.txt
  

### Запуск парсинга

Перейдите в директорию с проектом:
    
    cd parser_tenders

Для запуска процесса парсинга:

    python parse_tenders.py


### Использование через командную строку

Для просмотра тендеров в командной строке:

    python tender_cli.py --limit 10


### Запуск веб-сервиса

Для запуска FastAPI сервера:

    uvicorn main:app --reload


После этого, вы сможете обратиться к веб-сервису.

Примеры запросов:

1. Парсинг тендеров:

    http://127.0.0.1:8000/parse-tenders

    Ответ:

        {"message":"Tenders parsed and stored successfully."}


2. Запрос к БД по умолчанию выдает 10 тендеров:
    
    http://127.0.0.1:8000/tenders

    Ответ:

        [{"id":1501,"tender_number_span":"Тендер №85583647","title":"Тендер продукты питания (мясо говядина бескостное тазобедренный отруб) для нужд фгбоу д/с 258 в Новосибирске","delivery_address":"город Новосибирск","initial_price":"96 000 ₽","customer_branches":"Мясо, Мясные продукты, Продукция животноводства и охоты","link":"https://rostender.info/region/novosibirskaya-oblast/novosibirsk/85583647-tender-produkty-pitaniya-myaso-govyadina-beskostnoe-tazobedrennyj-otrub-dlya-nujd-fgbou-ds-258"},{"id":1502,"tender_number_span":"Тендер №85583645","title":"Тендер журналы по внеурочной деятельности, мел канцелярский в Севске","delivery_address":"Севский район,  село Бересток","initial_price":"2 510 ₽","customer_branches":"Канцелярские принадлежности","link":"https://rostender.info/region/bryanskaya-oblast/sevsk/85583645-tender-jurnaly-po-vneurochnoj-deyatelnosti-mel-kancelyarskij"},{"id":1503,"tender_number_span":"Тендер №85583644","title":"Тендер на поставку средств индивидуальной защиты – комбинезонов одноразовых для работы с биомассой для обеспечения деятельности санкт-петербургского государственного казенного учреждения \"поисково-спасательная служба санкт-петербурга\" в Санкт-Петербурге","delivery_address":"Санкт-Петербург","initial_price":"591 858 ₽","customer_branches":"Средства индивидуальной защиты","link":"https://rostender.info/region/sankt-peterburg-gorod/85583644-tender-postavka-sredstv-individualnoj-zashchity-kombinezonov-odnorazovyh-dlya-raboty-s-biomassoj-dlya-obespecheniya-deyatelnosti-sankt"},{"id":1504,"tender_number_span":"Тендер №85583627","title":"Тендер на поставку , доставку, разгрузку, сборку стола ученического для оснащения объекта строительство многофункционального центра детей и молодежи в селе белый яр, ул. промышленная, 7","delivery_address":"Алтайский район,  село Белый Яр","initial_price":"—","customer_branches":"Мебель, Элементы интерьера, Учебное оборудование и материалы","link":"https://rostender.info/region/hakasiya-respublika/85583627-tender-postavka-dostavku-razgruzku-sborku-stola-uchenicheskogo-dlya-osnashcheniya-obekta-stroitelstvo-mnogofunkcionalnogo-centra-detej-i"},{"id":1505,"tender_number_span":"Тендер №85583642","title":"Тендер на поставку полотенец бумажных и салфеток нестерильных в Ставрополе","delivery_address":"г. Ставрополь","initial_price":"82 207 ₽","customer_branches":"Хозяйственные товары, Товары широкого потребления, Бытовая химия и парфюмерия","link":"https://rostender.info/region/stavropolskij-kraj/stavropol/85583642-tender-postavka-polotenec-bumajnyh-i-salfetok-nesterilnyh"},{"id":1506,"tender_number_span":"Тендер №85583641","title":"Тендер на поставку хозяйственных товаров в Наро-Фоминске","delivery_address":"гп. Калининец Наро-Фоминский р-н","initial_price":"35 220 ₽","customer_branches":"Хозяйственные товары, Товары широкого потребления, Бытовая химия и парфюмерия","link":"https://rostender.info/region/moskovskaya-oblast/naro-fominsk/85583641-tender-postavka-hozyajstvennyh-tovarov"},{"id":1507,"tender_number_span":"Тендер №85583624","title":"Тендер на оказание услуг грузоперевозящей техникой для нужд зао удмуртнефть-бурение","delivery_address":"Респ. Удмуртская","initial_price":"—","customer_branches":"Услуги грузовых автомобильных перевозок","link":"https://rostender.info/region/udmurtskaya-respublika/85583624-tender-okazanie-uslug-gruzoperevozyashchej-tehnikoj-dlya-nujd-zao-udmurtneft-burenie"},{"id":1508,"tender_number_span":"Тендер №85583626","title":"Тендер на услуги по завозу пищевой и технической жидкости воды для нужд буровых бригад при строительстве скважин на месторождениях пао удмуртнефть имени в.и. кудинова","delivery_address":"Респ. Удмуртская","initial_price":"—","customer_branches":"Автомобильные и моторные масла, смазки, технические жидкости, Обеспечение водоснабжением, подвоз воды","link":"https://rostender.info/region/udmurtskaya-respublika/85583626-tender-uslugi-po-zavozu-pishchevoj-i-tehnicheskoj-jidkosti-vody-dlya-nujd-burovyh-brigad-pri-stroitelstve-skvajin-na-mestorojdeniyah-pao"},{"id":1509,"tender_number_span":"Тендер №85583625","title":"Тендер укрепление антитеррористической безопасности; оказание услуг по обеспечению охраны в Белоярском","delivery_address":"Тюменская обл;г. Белоярский","initial_price":"516 800 ₽","customer_branches":"Охранные услуги, Инкассация","link":"https://rostender.info/tender/85583625"},{"id":1510,"tender_number_span":"Тендер №85583621","title":"Тендер замок для дверей в Краснодаре","delivery_address":"г. Краснодар","initial_price":"92 000 ₽","customer_branches":"Установка окон и дверей, Производство окон и дверей","link":"https://rostender.info/region/krasnodarskij-kraj/krasnodar/85583621-tender-zamok-dlya-dverej"}]


3. Запрос с указанием параметра limit:

    http://127.0.0.1:8000/tenders?limit=1

    Ответ:

        [{"id":1501,"tender_number_span":"Тендер №85583647","title":"Тендер продукты питания (мясо говядина бескостное тазобедренный отруб) для нужд фгбоу д/с 258 в Новосибирске","delivery_address":"город Новосибирск","initial_price":"96 000 ₽","customer_branches":"Мясо, Мясные продукты, Продукция животноводства и охоты","link":"https://rostender.info/region/novosibirskaya-oblast/novosibirsk/85583647-tender-produkty-pitaniya-myaso-govyadina-beskostnoe-tazobedrennyj-otrub-dlya-nujd-fgbou-ds-258"}]

4. Запросы можно так же выполнять через Swagger:
    
    http://127.0.0.1:8000/docs


### Возможные улучшения

    - Можно рассмотреть внедрение асинхронности с помощью библиотеки AioSQLite.

    - Добавить аутентификацию, авторизацию и ограничить количество запросов в единицу времени для увеличения безопасности.

    - Внедрить фильтрацию и сортировку тендеров на основе различных критериев, таких как начальная цена или категория заказчиков.


