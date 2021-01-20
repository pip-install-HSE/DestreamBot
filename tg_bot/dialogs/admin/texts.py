from ...load_all import _

bot_user_start = lambda: _("Привет, я бот destream. \n\n"
                           "Я помогу тебе принять донаты от твоих подписчиков группы или канала."
                           "Для того, чтобы принимать донаты, сначала зарегистрируйся на платформе destream, а затем "
                           "скопируй мне токен из раздела API в настройках платформы.")

main_menu = lambda json_data: _("<b>Привет, ") + f"{json_data['username']}!</b>\n\n" + \
                              _("Твой баланс ") + f"{json_data['balance']['balance']} {json_data['balance']['currency']}"
error_token = lambda: _("Извините, но токен неправильный, попробуйте отправить снова")
add_group = lambda: _("Добавь бота админом в группу или канал\n\n"
                      "<b>ПРИ ДОБАВЛЕНИИ В КАНАЛ</b>\n"
                      "Необходимо опубликовать пост с текстом из следующего сообщения в канал. "
                      "(Пост будет автоматически удалён после проверки)")
established_as_admin = lambda: _("Здорово, ты сделал бота администратором!\n\n"
                                 "Бот также пригласит в группу или канал сотрудника destream для проверки "
                                 "контента на соответствие правилам")
not_established_as_admin = lambda: _("Вы не установили бота админом, попробуйте снова!")
notifications = lambda: _("Сообщать ли в группе или канале о новых донатах?")
notify = lambda notify_: notify_yes() if notify_ else notify_no()
notify_yes = lambda: _("Хорошо! Поделюсь информацией о всех донатах.")
notify_no = lambda: _("Как скажите! Но не проблема будет посмотреть донаты на сайте, заходите...")

before_access__add_group = lambda: _("Перед тем, как пытаться получить дотсуп к группе, добавьте её!")

changed_is_report_donations = lambda is_rep: _("Теперь размещаю!") if is_rep else _("Больше не размещаю!")

my_group = lambda group_username, min_sum: f"<b>{group_username}</b>\n\n" + _("Минимальная сумма ") + f"{min_sum}\n\n"
any_message = lambda: _("Отправьте /start для начала работы с ботом")
maintenance = lambda: _("Данный раздел находится в разработке!")
donation_post = lambda post: _("Текст поста:\n\n") + post

set_donation_post = lambda: _("Пришли новый текст поста 1 сообщением")
post_donation_post = lambda: _("Мы разместили твой пост")

new_donation = lambda d: \
    f"<b>{d['additionalParameters']['don_name']}</b>" + _(" сделал донат на сумму ") + f"<b>{d['amount']} {d['currency']}</b>" + _(
        " и написал текст: \n") + f"<i>{d['message']}</i>"

delete_all = lambda: _("Всё удалено. Нажмите /start для начала работы с ботом")
