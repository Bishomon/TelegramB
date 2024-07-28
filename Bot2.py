import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    CallbackQuery
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler, \
    ChatMemberHandler
from telegram.error import BadRequest
import pandas as pd


async def start(update: Update, context: CallbackContext) -> None:
    text1 = """<b>Добрый день!</b> Вы находитесь в чате команды <b>DEMO.Estate.</b> 
Мы оказываем следующие услуги:
- <b>Выкуп имущества с торгов;</b>
- Подбор объектов недвижимости на торгах и на открытом рынке;
- Осмотр объекта недвижимости;
- Доступ к закрытой базе объектов по цене ниже рыночной до <b>40%;</b>
- Оформление земельных участков;
- Консультация по участию в торгах;

<b>Какой у вас вопрос?</b>"""
    sent_message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text1,
        reply_markup=main_menu(), parse_mode='HTML'

    )

    # Сохраняем идентификатор отправленного сообщения в пользовательских данных
    context.user_data['start_message_id'] = sent_message.message_id


def main_menu():
    keyboard = [
        [InlineKeyboardButton("🌐 Больше информации о лоте", callback_data='1')],
        [InlineKeyboardButton("📝 Помощь с выкупом", callback_data='2')],
        [InlineKeyboardButton("📌 Подбор объекта", callback_data='3')],
        [InlineKeyboardButton("🔐 Закрытый каталог объектов", callback_data='4')],
        [InlineKeyboardButton("📑 Другие услуги", callback_data='5')],
       # [InlineKeyboardButton("Закрытый каталог объектов", callback_data='6')],
        #[InlineKeyboardButton("Частые вопросы", callback_data='7')],
        [InlineKeyboardButton("📞 Связь с менеджером", callback_data='8')],
        [InlineKeyboardButton("🏆 О нас", callback_data='9')],

    ]

    return InlineKeyboardMarkup(keyboard)


async def menu_option_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    try:
        await context.bot.delete_message(chat_id=update.effective_chat.id,
                                         message_id=context.user_data.get('start_message_id'))
    except BadRequest:
        print("Start message not found or unable to delete.")

    # Обрабатываем выбор пользователя в зависимости от кнопки
    if query.data == '1':
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            parse_mode = 'HTML',
            text="""&#128681; <b>Для отправки запроса напишите нам:</b>
— Артикул лота;
— Ваше имя;
— Номер телефона;
— Ваш вопрос;
<b>Мы ознакомимся с запросом и предоставим информацию в ближайшее время.</b>""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏅 Хочу всегда видеть полную информацию без ожидания.", callback_data='1.1')],
                [InlineKeyboardButton("🔙 Назад", callback_data='back')]

            ])
        )
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '1.1':
        text2 = """&#128272; <b>Полная информация о лотах представлена в нашем закрытом канале.</b>

<b>Подписчики закрытого канала получают:</b>
1) Скидку на участие в торгах в размере <b>50%.</b>
2) Эксклюзивные предложения рынка залоговых активов банков по цене до <b>40%</b> ниже рынка (по запросу).
3) <b>Ранний доступ</b> ко всем лотам из закрытой базы объектов на торгах (за 7 дней до публикации на бесплатном канале). Это позволит избежать дополнительной конкуренции и успеть зайти на торги через нас (берём 1 человека на 1 торги).
4) <b>Полную информацию о лоте</b> - кадастровые номера объектов, ссылка на торги.
5) Лучшие объекты с торгов по банкротству с дисконтом до <b>40%</b> ниже рынка.

 &#128273; <b>Стоимость ежемесячной подписки - 890₽.</b>"""

        # Здесь вы можете добавить код для обработки кнопки "Назад"
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text2,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎯 Оформить подписку", callback_data='1.2')],
                [InlineKeyboardButton("🔙 Назад", callback_data='1')]]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '1.2':

        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            parse_mode='HTML',
            text="""&#128273; <b>Оформить подписку на закрытый каталог объектов с торгов (ссылка — https://t.me/+o9Hu7rJRWgdmNTZi ) - нажмите.</b>

При оплате картой сервис запомнит её данные и раз в месяц будет автоматически продлять подписку.

По всем вопросам обращайтесь в поддержку @demo_support""",
            reply_markup=InlineKeyboardMarkup([

                [InlineKeyboardButton("Назад", callback_data='1.1')]]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text

        # Обработка других кнопок

    if query.data == '2':
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Выберите интересующую помощь",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚦 Этапы работы", callback_data='2.1')],
                [InlineKeyboardButton("🧮 Тарифы", callback_data='2.2')],
                [InlineKeyboardButton("🔙 Назад", callback_data='back')]
            ])
        )
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '2.1':
        text3 = """&#128218; <b>Выкуп имущества с торгов включает в себя 4 этапа.</b>

&#128215; <b>Этап 1 включает в себя следующие действия:</b>

— Отправьте нам артикул объекта или ссылку на любой ресурс, где вы нашли упоминание об интересующем вас объекте (Авито, ЭТП, Агрегатор и тд).
— Напишите ваше имя и номер телефона, привязанный к Telegram.
— Мы уточним данные и свяжемся с вами.
— Заявки на участие принимаются не позже 5 рабочих дней до окончания подачи заявок на торгах.
— Оплата осуществляется в 2 этапа в соответствии с тарифами: первая часть перед торгами + % от стоимости объекта в день подписания ДКП в случае победы.
— Работа проводится в рамках агентского договора.
— Нажмите кнопку «&#128284; 2 ЭТАП»."""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text3,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔜 Этап 2", callback_data='2.1.1')],
                [InlineKeyboardButton("🔙 Назад", callback_data='2')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '2.1.1':
        text4 = """&#128210 <b>Этап 2</b>
Отправьте нам сканы следующих документов: 
— Паспорт (все 22 страницы от Кремля до Извлечения)
— Свидетельство ИНН (заказывается онлайн на сайте nalog.ru - вход через Госуслуги)
— СНИЛС (скан или скриншот документа из Госуслуг).
<b>Это обязательный пакет документов, необходимый для участия в торгах.</b>
Нажмите кнопку «🔜  Этап 3»."""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text4,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔜 Этап 3", callback_data='2.1.2')],
                [InlineKeyboardButton("🔙 Назад", callback_data='2.1')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]]
                # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '2.1.2':
        text5 = """&#128213; <b>Этап 3</b>
— Подписывается агентский договор;
— Вносится предоплата за подготовку документов;
— Оформляется ЭЦП (при необходимости);
— Регистрируемся на ЭТП, получаем аккредитацию (в случае работы с муниципальными торгами);
— Готовится итоговый пакет документов для участия в торгах;
— Переводится задаток;
— Определяется пороговая цена на аукционе;
— Отправляется заявка на участие в торгах;
— Участвуем в аукционе;
Нажмите кнопку « &#128284; 4 Этап»."""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text5,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔜 Этап 4", callback_data='2.1.3')],
                [InlineKeyboardButton("🔙 Назад", callback_data='2.1.1')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]]
                # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '2.1.3':
        text6 = """&#128216; <b>Этап 4</b>
— В случае победы на аукционе задаток учитывается в итоговой сумме. Оставшуюся часть средств необходимо перевести на реквизиты, указанные в проекте ДКП; 
— ДКП подписывается в течении 5 рабочих дней;
— Полная оплата проводится в срок, обозначенный в проекте ДКП.
— Оплата нашей комиссии осуществляется в день подписания ДКП.

— В случае поражения на аукционе, задаток возвращается обратно на реквизиты, с которых он был переведен. Возврат осуществляется в течении 5-10 рабочих дней.
— По итогам аукциона вам высылается протокол, в котором прописана итоговая цена и победитель.

— <b>В случае отказа победителя от подписания ДКП или отказа от оплаты оставшейся части имущества, задаток не возвращается.</b>"""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text6,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data='2.1.2')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]]
                # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '2.2':
        text7 = """&#128304; <b>Стандартный - 10.000₽ + % после победы</b>
— Подготовка аукционной документации;
— Регистрация участника на ЭТП;
— Получение аккредитации на ЭТП;
— Подача заявки на участие в торгах;
— Участие в торгах;
— Помощь в заключении договора купли-продажи;
— Отзыв заявки/возврат задатка;

 &#128200; <b>Полный - 10.000₽ + % после победы</b>
— Аудит объекта и процедуры (проблемные моменты) 
— Подготовка аукционной документации;
— Подача заявки с регистрацией участника торгов;
— Участие в торгах;
— Помощь в заключении договора купли-продажи;
— Отзыв заявки/возврат задатка;
— Сопровождение в полной оплате и подписании ДКП;
— Регистрация перехода прав собственности в Росреестре;
— Работа с обременениями, в случае их наличия (торги по банкротству);

 &#128188; <b>Для юр.лиц - 20.000₽ + % после победы</b>

 &#128450; <b>Дополнительные услуги:</b>
— Помощь в регистрации на портале ГИС Торги для участия в торгах по реализации государственного или муниципального имущества.
Получите доступ к участию в торгах на площадках:
ЭТП Сбер А; Росэлторг; РТС-тендер; АО «РАД»; Агентство по государственному заказу Республики Татарстан ЗаказРФ; ЭТП «Фабрикант»; ЭТП Газпромбанк; ЭТП ТЭК-Торг - по договоренности;
— Помощь в регистрации на Фабрикант, ЦДТ, Уральский ЭТП и других. - по договоренности.
— Поиск торговой процедуры по вашей ссылке (если нашли объект на Авито с примечанием о продаже через торги) - по договоренности.
— Регистрация права собственности - 10.000р
— Подготовка жалобы в ФАС - 15.000р
— Подготовка судебного иска по итогам торгов - 15.000р"""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text7,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📊 Форматы работы", callback_data='2.2.1')],
                [InlineKeyboardButton("🔙 Назад", callback_data='2')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '2.2.1':
        text8 = """Варианты работы:
         &#128202; <b>Форматы работы:</b>
<b>1)По нотариальной доверенности (лучший вариант для торгов по банкротству)</b>
Преимущества: 
— Не нужно оформлять ЭЦП;
— Не тратим время на регистрацию и аккредитацию на площадке; 
— Вся работа проводится на компьютере агента через наш личный кабинет;
— Иногда хватает агентского договора и нет необходимости ехать к нотариусу и оплачивать доверенность;

<b>2)Через удалённый доступ (лучший вариант для муниципальных торгов)</b>
Преимущества: 
— Мы регистрируем вас на 8 федеральных ЭТП, 
— Получаем аккредитацию на ваш личный аккаунт;
— Все этапы проходят у вас перед глазами, так как работа ведется на вашем компьютере через удаленный доступ;
— Вы переводите задаток на ваш собственный лицензионный счёт.

 &#9203; <b>Сроки оказания услуги (в случае выбор 1 варианта):</b>
1)Получение нотариальной доверенность — 1 день
2)Перевод задатка — 1-2 дня
3)Подготовка документов — 1 день

 &#8987; <b>Сроки оказания услуги (в случае выбор 2 варианта):</b>
1)Получение ЭЦП — 2 дня
2)Регистрация и получение аккредитации на ЭТП — 3 дня
3)Перевод задатка — 1-2 дня
<b>В связи со сложившейся практикой, работу по подготовке к торгам необходимо начинать за 7 дней до окончания подачи заявок.</b>"""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text8,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data='2.2')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text

    if query.data == "3":
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Выберите интересующую помощь",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔺 Подбор объекта с торгов", callback_data='3.1')],
                [InlineKeyboardButton("🔻 Подбор объекта с открытого рынка", callback_data='3.2')],
                [InlineKeyboardButton("🔙 Назад", callback_data='back')]
            ])
        )
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '3.1':
        text9 = """&#128200; <b>По вашему запросу мы подберем ряд объектов, точно подходящих под ваши критерии.</b>

Отправьте нам запрос, мы проверим возможность подобрать объекты и ответим вам в течении 3 рабочих дней.

Стоимость: 10.000 предоплата + выкуп по тарифу "Полный". Работаем по договору оказания услуг."""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text9,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🧮 Тарифы", callback_data='2.2')],
                [InlineKeyboardButton("♦ Отправить заявку", callback_data='3.1.1')],
                [InlineKeyboardButton("🔙 Назад", callback_data='3')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '3.1.1':
        text10 = """&#9830; <b>Оставьте заявку в следующем формате:</b>
— ФИО;
— Номер телефона;
— Вид объекта;
— Локация;
— Площадь;
— Бюджет;
— Особые пожелания;"""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text10,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data='3.1')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '3.2':
        text11 = """&#127919; <b>В команде работают опытные риэлторы, готовые предложить вам эксклюзивные объекты от лучших застройщиков Москвы по специальным ценам.</b>
Вы получите <b>подборку лучших объектов</b> от застройщиков Москвы, а также доступ к <b>pre-sale</b> продажам с преимуществом выбора и скидкой.

При сотрудничестве заключается договор и оплачивается символический задаток в 10.000 рублей, подтверждающий серьёзность намерений обеих сторон сделки.

Мы также можем проверить нашу цену на уже подобранный вами объект.

️ &#9830; <b>Чтобы оставить заявку на подбор, отправьте информацию в следующем формате:</b>
— ФИО;
— Номер телефона;
— Вид объекта;
— Локация;
— Площадь;
— Бюджет;
— Особые пожелания;"""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text11,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data='3')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text

    if query.data == "4":
        text12 = """Выберите интересующий каталог"""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text12,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⛳ Земельные участки (Москва и МО)", callback_data='4.1')],
                [InlineKeyboardButton("🏛 Коммерческая недвижимость (Москва и МО)",url='https://web.telegram.org/a/#-1002035303018')],
                [InlineKeyboardButton("🏡 Жилая недвижимость (Москва и МО)", url='https://web.telegram.org/a/#-1002035303018')],
                [InlineKeyboardButton("🔙 Назад", callback_data='back')]
            ])
        )
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '4.1':
        text13 = """&#128273; <b>Оформить подписку на закрытый каталог объектов с торгов (ссылка - https://t.me/+o9Hu7rJRWgdmNTZi )</b>"""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text13,
            reply_markup=InlineKeyboardMarkup([

                [InlineKeyboardButton("🔙 Назад", callback_data='3')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text



    if query.data == "5":
        text20 = """
        Так же можем предложить вам следующие услуги:
"""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text20,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⛳ Оформление земельного участка", callback_data='5.1')],
                [InlineKeyboardButton("🔎 Осмотр объекта", callback_data='5.2')],
                [InlineKeyboardButton("🔙 Назад", callback_data='back')]
            ])
        )
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '5.1':
        text21 = """&#127957; <b>Один из вариантов приобретения земельных участков — оформление свободной земли, которая принадлежит государству.</b>

Согласно нормам действующего земельного законодательства, предоставление земельных участков гражданам и юридическим лицам в собственность или аренду из земель, находящихся в государственной и муниципальной собственности, осуществляться посредством проведения торгов или, в случаях, определенных законом, без их проведения.
Порядок предоставления земельных участков без проведения торгов устанавливается земельным законодательством и предусматривает следующие процедуры:
— подготовка заинтересованными лицами схемы расположения земельного участка в случае, если земельный участок предстоит образовать и не утвержден проект межевания территории, в границах которой предстоит образовать такой земельный участок;
— подача в уполномоченный орган гражданином или юридическим лицом заявления о предварительном согласовании предоставления земельного участка в случае, если земельный участок предстоит образовать или границы земельного участка подлежат уточнению и принятие этим органом решения о предварительном согласовании предоставления земельного участка.

 &#9989; <b>Таким образом, вы можете выкупить или взять в аренду у государства свободную землю по цене ниже рыночной. Также благодаря этому методу можно подобрать участок с лучшим видом или локацией там, где на открытом рынке подходящих предложений нет.</b>"""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text21,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🧮 Прайс", callback_data='5.1.1')],
                [InlineKeyboardButton("🔙 Назад", callback_data='5')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '5.1.1':
        text22 = """&#128273; <b>Работа под ключ - 150.000₽</b>
1) Предварительное согласование земельного участка;
2) Подбор земельного участка в конкретной локации (радиус от 5 км от предпочтительной локации);
3) Участие в аукционе;
4) Заключение ДКП и регистрация права собственности;"""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text22,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([

                [InlineKeyboardButton("🔙 Назад", callback_data='5.1')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '5.2':
        text23 = """Выберите интересующую вас услугу"""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text23,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🗺 Самостоятельный осмотр", callback_data='5.2.1')],
                [InlineKeyboardButton("📸 Услуга по осмотру объекта", callback_data='5.2.2')],
                [InlineKeyboardButton("⛳ Оформление земельного участка", callback_data='5.2.3')],
                [InlineKeyboardButton("🔙 Назад", callback_data='5')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '5.2.1':
        text24 = """&#128205; Для получения точных координат объекта введите его кадастровый номер в графу поиска на <b>кадастровой карте</b> (гиперссылка — https://rosreestr-doc.ru/кадастровая_карта ). Далее скопируйте координаты в формате 55.754681, 37.621389 и вставьте их в Яндекс.Карты/Google Карты."""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text24,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔎 Нет кадастрового номера", callback_data='5.2.1.1')],
                [InlineKeyboardButton("🔙 Назад", callback_data='5.2')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '5.2.1.1':
        text25 = """&#128681; Отправьте нам артикул лота, ваш вопрос и номер телефона. Мы предоставим информацию в ближайшее время."""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text25,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔰 Хочу всегда видеть полную информацию без ожидания.", callback_data='5.2.1.2')],
                [InlineKeyboardButton("🔙 Назад", callback_data='5.2.1')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '5.2.1.2':
        text26 = """&#128272; <b>Полная информация о лотах представлена в нашем закрытом канале.</b>

<b>Подписчики закрытого канала получают:</b>
1) Скидку на участие в торгах в размере <b>50%.</b>
2) Эксклюзивные предложения рынка залоговых активов банков по цене до <b>40%</b> ниже рынка (по запросу).
3) <b>Ранний доступ</b> ко всем лотам из закрытой базы объектов на торгах (за 7 дней до публикации на бесплатном канале). Это позволит избежать дополнительной конкуренции и успеть зайти на торги через нас (берём 1 человека на 1 торги).
4) <b>Полную информацию о лоте</b> - кадастровые номера объектов, ссылка на торги.
5) Лучшие объекты с торгов по банкротству с дисконтом до <b>40%</b> ниже рынка.

 &#128273; <b>Стоимость ежемесячной подписки - 890₽.</b>"""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text26,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎯 Оформить подписку", callback_data='5.2.1.3')],
                [InlineKeyboardButton("🔙Назад", callback_data='5.2.1.1')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '5.2.1.3':
        text27 = """ &#128273; <b>Оформить подписку на закрытый каталог объектов с торгов (ссылка — https://t.me/+o9Hu7rJRWgdmNTZi ) - нажмите.</b>

При оплате картой сервис запомнит её данные и раз в месяц будет автоматически продлять подписку.

По всем вопросам обращайтесь в поддержку @demo_support"""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text27,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([

                [InlineKeyboardButton("🔙 Назад", callback_data='5.2.1.2')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '5.2.2':
        text29 = """&#127909; <b>В рамках услуги по осмотру объекта осуществляется фото и видео съёмка. Также в формате онлайн оказывается консультация с ответами на вопросы по месту.</b>

Услуга стоит от 5.000 рублей без онлайн консультации и от 7.000 с онлайн консультацией."""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text29,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("♦ Заказать услугу", callback_data='5.2.2.1')],
                [InlineKeyboardButton("🔙 Назад", callback_data='5.2')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '5.2.2.1':
        text30 = """&#9830; Отправьте нам адрес объекта и ссылку на торги, мы проверим возможность осмотра на ближайшее время и ответим вам в течении 24 часов. """
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text30,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([

                [InlineKeyboardButton("🔙 Назад", callback_data='5.2.2')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '5.2.3':
        text40 = """&#127957; <b>Один из вариантов приобретения земельных участков — оформление свободной земли, которая принадлежит государству.</b>

Согласно нормам действующего земельного законодательства, предоставление земельных участков гражданам и юридическим лицам в собственность или аренду из земель, находящихся в государственной и муниципальной собственности, осуществляться посредством проведения торгов или, в случаях, определенных законом, без их проведения.
Порядок предоставления земельных участков без проведения торгов устанавливается земельным законодательством и предусматривает следующие процедуры:
— подготовка заинтересованными лицами схемы расположения земельного участка в случае, если земельный участок предстоит образовать и не утвержден проект межевания территории, в границах которой предстоит образовать такой земельный участок;
— подача в уполномоченный орган гражданином или юридическим лицом заявления о предварительном согласовании предоставления земельного участка в случае, если земельный участок предстоит образовать или границы земельного участка подлежат уточнению и принятие этим органом решения о предварительном согласовании предоставления земельного участка.

 &#9989; <b>Таким образом, вы можете выкупить или взять в аренду у государства свободную землю по цене ниже рыночной. Также благодаря этому методу можно подобрать участок с лучшим видом или локацией там, где на открытом рынке подходящих предложений нет.</b>"""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text40,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🧮 Прайс", callback_data='5.2.3.1')],
                [InlineKeyboardButton("🔙 Назад", callback_data='5.2')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == '5.2.3.1':
        text41 = """&#128273; <b>Работа под ключ - 150.000₽</b>
1) Предварительное согласование земельного участка;
2) Подбор земельного участка в конкретной локации (радиус от 5 км от предпочтительной локации);
3) Участие в аукционе;
4) Заключение ДКП и регистрация права собственности;"""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text41,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([

                [InlineKeyboardButton("🔙 Назад", callback_data='5.2.1')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ]  # Возвращаем основное меню
            ))
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text

    if query.data == "8":
        text31 = """&#128222 Связь с менеджером
Напишите свой вопрос и оставьте свой номер телефона. Мы подробно ответим на ваш вопрос в чате. 
Также здесь вы можете оставить предложение по улучшению сервиса, добавлению категорий лотов или предложение о сотрудничестве.

Если вам было бы удобнее пообщаться по телефону - укажите это в конце вашего вопроса.
       """
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text31,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([

                [InlineKeyboardButton("🔙 Назад", callback_data='back')]
            ])
        )
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text

    if query.data == "9":
        text32 = """&#127942; <b>О нас</b>

Мы - команда высококвалифицированных юристов, специализирующихся на предоставлении широкого спектра услуг по работе с имуществом на электронных торгах. 

Мы предлагаем нашим клиентам профессиональную поддержку в сфере электронных аукционов, обеспечивая защиту их интересов на каждом этапе сделки.

Если вам нужна профессиональная помощь в сфере электронных торгов с недвижимостью, обращайтесь к нам.

Приглашаем к сотрудничеству на постоянной основе.
Возможна постоянная работа по доверенности или через вашу ЭЦП.
По формату партнерства возможна личная встреча в Москве.

<b>Мы открыты к сотрудничеству с агентами и риелторами.</b>
       """
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text32,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📬 Оставить заявку", callback_data='9.1')],
                [InlineKeyboardButton("📞 Связь с менеджером", callback_data='9.2')],
                [InlineKeyboardButton("🔙 Назад", callback_data='back')]
            ])
        )
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == "9.1":
        text33 = """Выберите интересующую вас опцию
          """
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text33,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Помощь с выкупом", callback_data='2')],
                [InlineKeyboardButton("Подбор объекта", callback_data='3')],
                [InlineKeyboardButton("Осмотр объекта", callback_data='5.2')],
                [InlineKeyboardButton("Оформление земельного участка", callback_data='5.2.3')],
                [InlineKeyboardButton("Назад", callback_data='9')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ])
        )
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text
    elif query.data == "9.2":
        text34 = """Контакты менеджера
              """
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text34,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Назад", callback_data='9')],
                [InlineKeyboardButton("Главное меню", callback_data='back')]
            ])
        )
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text

    if query.data == "back":
        text1 = """<b>Добрый день!</b> Вы находитесь в чате команды <b>DEMO.Estate.</b> 
        Мы оказываем следующие услуги:
        - <b>Выкуп имущества с торгов;</b>
        - Подбор объектов недвижимости на торгах и на открытом рынке;
        - Осмотр объекта недвижимости;
        - Доступ к закрытой базе объектов по цене ниже рыночной до <b>40%;</b>
        - Оформление земельных участков;
        - Консультация по участию в торгах;

        <b>Какой у вас вопрос?</b>"""
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text1,
            reply_markup=main_menu(), parse_mode='HTML'

        )

        # Сохраняем идентификатор отправленного сообщения в пользовательских данных
        context.user_data['start_message_id'] = msg.message_id
        context.user_data['start_message_text'] = msg.text


async def handle_user_messages(update: Update, context: CallbackContext) -> None:
    # Проверяем, что сообщение пришло в ответ на предыдущее меню
    if 'start_message_id' in context.user_data:
        # Получаем данные пользователя из context.user_data
        user_data = context.user_data.get('user_data', {})

        # Получаем текст сообщения пользователя
        user_input = update.message.text

        # Получаем имя пользователя
        username = update.message.from_user.username

        # Добавляем данные в словарь пользователя
        user_data['user_input'] = user_input
        user_data['username'] = username
        user_data['question'] = context.user_data['start_message_text']

        # Обновляем данные пользователя в context.user_data
        context.user_data['user_data'] = user_data

        # Прочитайте существующий файл Excel, если он существует
        try:
            existing_df = pd.read_excel('user_data.xlsx')
        except FileNotFoundError:
            existing_df = pd.DataFrame()

        # Создайте новый DataFrame из текущих данных пользователя
        new_data = pd.DataFrame.from_dict(user_data, orient='index').T

        # Объедините существующий DataFrame с новыми данными
        updated_df = pd.concat([existing_df, new_data], ignore_index=True)

        # Запишите обновленные данные в Excel-файл
        updated_df.to_excel('user_data.xlsx', index=False)

        # Добавьте вашу логику для реагирования на сообщение пользователя
        # Например, отправка ответа пользователю
        await update.message.reply_text(f"Спасибо, {username}, для продолжения работы нажмите кнопку рестарт в меню")


def main():
    """Start the bot."""
    application = Application.builder().token("6838830099:AAGbGCibVjtsNMLJ4_K57htuS-R5AZa4Hf4").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(menu_option_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_messages))

    # Run the bot using asyncio.run()
    asyncio.run(application.run_polling(allowed_updates=Update.ALL_TYPES))


if __name__ == '__main__':
    main()
