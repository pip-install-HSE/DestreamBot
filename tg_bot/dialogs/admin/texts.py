from ...load_all import _

bot_user_start = lambda: _("Сходи на платформу, затем вернись и дай мне откуда-то токен")

main_menu = lambda token: _("<b>ГЛАВНОЕ МЕНЮ</b>\n\n") + f"{token}"
