from ...load_all import _

bot_user_start = lambda: _("Сходи на платформу, затем вернись и дай мне откуда-то токен")

main_menu = lambda json_data: _("<b>ГЛАВНОЕ МЕНЮ</b>\n\nТебя зовут") + f"{json_data['username']}" + _("Твой баланс") + f"{json_data['balance']['balance']} {json_data['balance']['currency']}"
error_token = lambda: _("Извините, но токен неправильный, попробуйте отправить снова")
add_group = lambda: _("Добавьте, пожалуйста, бота в группу и передайте ему права администратора")
notifications = lambda: _("Отлично, бот добавлен, теперь скажите, хотите ли Вы сообщать в группе о новых донатах")
