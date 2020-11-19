from ...load_all import _

bot_user_start = lambda: _("Сходи на платформу, затем вернись и дай мне откуда-то токен")

main_menu = lambda json_data: _("<b>ГЛАВНОЕ МЕНЮ</b>\n\nТебя зовут: ") + f"{json_data['username']}\n" + _("Твой баланс: ") + f"{json_data['balance']['balance']} {json_data['balance']['currency']}\n\n" + _("История донатов\n") + f"!ссылка не подъехала!"
error_token = lambda: _("Извините, но токен неправильный, попробуйте отправить снова")
add_group = lambda: _("Добавьте, пожалуйста, бота в группу.")
established_as_admin = lambda: _("Отлично, бот добавлен, теперь установите его в качестве администратора и нажмите на кнопку 'готово'.")
not_established_as_admin = lambda: _("Вы не установили бота админом, попробуйте снова!")
notifications = lambda: _("Здорово, бот теперь админ, теперь скажите, хотите ли Вы сообщать в группе о новых донатах")
notify_yes = lambda: _("Хорошо! Поделюсь информацией о всех донатах и предложу выложить в группу.")
notify_no = lambda: _("Как скажите! Но не проблема будет посмотреть донаты на сайте, заходите...")

before_access__add_group = lambda: _("Перед тем, как пытаться получить дотсуп к группе, добавьте её!")

my_group = lambda group_username, min_sum: f"<b>{group_username}</b>\n\n" + _("Помни о том, что среди твоих подписчиков могут оказаться модераторы\n\n") + f"{min_sum}"
any_message = lambda: _("Отправьте /start для начала работы с ботом")
donation_post = lambda: _("Вот Ваш пост")

new_donation = lambda d: \
    f"{d['sender']}"+_(" сделал донат на сумму ") + f"{d['amount']} {d['currency']}" + _(" и написал текст: ") + f"{d['message']}"
