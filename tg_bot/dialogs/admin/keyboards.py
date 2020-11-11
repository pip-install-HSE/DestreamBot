from ...load_all import _
from ...modules.keyboard import KeyboardInline, KeyboardReply

bot_user_start = lambda: KeyboardInline([{_("Вебвьюха"): "url:http://example.com"}]).get()

main_menu = lambda: KeyboardInline([{_("Добавить группу"): "add_group", _("Вывести деньги"): "url:http://example.com"},
                                    {_("Группа"): "my_group"}]).get()
check_bot_is_admin = lambda: KeyboardInline([{_("Проверить"): "bot_is_admin"}]).get()
# _("Перешлите сообщение из группы, в которую Вы хотите подключить бота"
notifications= lambda: KeyboardInline([{_("Так точно"): "yes", _("Никак нет"): "no"}]).get()
my_group = lambda: KeyboardInline([{_("Пост для донатов")}]).get()