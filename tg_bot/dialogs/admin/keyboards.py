from ...load_all import _
from ...modules.keyboard import KeyboardInline, KeyboardReply

bot_user_start = lambda: KeyboardInline([{_("Вебвьюха"): "url:http://example.com"}]).get()

main_menu = lambda: KeyboardInline([{_("Добавить группу"): "add_group", _("Вывести деньги"): "url:http://example.com"},
                                    {_("Группа"): "my_group"}]).get()

established_as_admin = lambda: KeyboardInline([{_("Готово"): "established_as_admin"}]).get()

notifications= lambda: KeyboardInline([{_("Так точно"): "notify_yes", _("Никак нет"): "notify_no"}]).get()
my_group = lambda: KeyboardInline([{_("Пост для донатов"): "donation_post"}, {_("Ссылка для доната"): "donation_link"},
                                   {_("Настройки группы"): "group_settings"}, {_("Назад"): "my_group"}]).get()
donation_post = lambda: KeyboardInline([{_("Запостить"): "post_donation_post"}, {_("Изменить"): "change_donation_post"}]).get()
post_donation_post = lambda: KeyboardInline([{_("К группе"): "my_group"}]).get()
group_donation_post = lambda url: KeyboardInline([{_("Задонатить"): f"url:{url}"}]).get()
