from ...load_all import _

bot_user_start = lambda: _("Сходи на платформу, затем вернись и дай мне откуда-то токен")

main_menu = lambda json_data: _("<b>ГЛАВНОЕ МЕНЮ</b>\n\nТебя зовут: ") + f"<i>{json_data['username']}</i>\n" + _("Твой баланс: ") + f"<i>{json_data['balance']['balance']} {json_data['balance']['currency']}\n\n</i>" + _("История донатов\n") + f"!ссылка не подъехала!"
error_token = lambda: _("Извините, но токен неправильный, попробуйте отправить снова")
add_group = lambda: _("Добавьте, пожалуйста, бота в группу.")
established_as_admin = lambda: _("Отлично, бот добавлен, теперь установите его в качестве администратора и нажмите на кнопку 'готово'.")
not_established_as_admin = lambda: _("Вы не установили бота админом, попробуйте снова!")
notifications = lambda: _("Здорово, бот теперь админ, теперь скажите, хотите ли Вы сообщать в группе о новых донатах")
notify = lambda notify_: notify_yes() if notify_ else notify_no()
notify_yes = lambda: _("Хорошо! Поделюсь информацией о всех донатах.")
notify_no = lambda: _("Как скажите! Но не проблема будет посмотреть донаты на сайте, заходите...")

before_access__add_group = lambda: _("Перед тем, как пытаться получить дотсуп к группе, добавьте её!")

changed_is_report_donations = lambda is_rep: _("Теперь размещаю!") if is_rep else _("Больше не размещаю!")

my_group = lambda group_username, min_sum: f"<b>{group_username}</b>\n\n" + _("Помни о том, что среди твоих подписчиков могут оказаться модераторы\n\nТвои ограничения по суммам донатов:\n") + f"{min_sum}"
any_message = lambda: _("Отправьте /start для начала работы с ботом")
maintenance = lambda: _("Данный раздел находится в разработке!")
donation_post = lambda post: _("Вот Ваш пост:\n\n") + post

set_donation_post = lambda: _("Отправьте мне текст поста.")
post_donation_post = lambda: _("Мы запостили ваш пост в группу!")

new_donation = lambda d: \
    f"<b>{d['sender']}</b>"+_(" сделал донат на сумму ") + f"<b>{d['amount']} {d['currency']}</b>" + _(" и написал текст: \n") + f"<i>{d['message']}</i>"
