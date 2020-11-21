from ...load_all import _
from ...modules.keyboard import KeyboardInline, KeyboardReply
from itertools import islice

def chunks(data, SIZE=10000):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k:data[k] for k in islice(it, SIZE)}

bot_user_start = lambda: KeyboardInline([{_("Вебвьюха"): "url:http://example.com"}]).get()

main_menu = lambda groups: KeyboardInline([{_("Добавить группу"): "add_group", _("Вывести деньги"): "url:http://example.com"}] +
                                          [i for i in chunks({g.username: f"my_group:{g.tg_id}" for g in groups}, 2)]
                                          ).get()

menu = lambda : KeyboardInline([{"Меню": "menu"}]).get()

established_as_admin = lambda: KeyboardInline([{_("Готово"): "established_as_admin"}]).get()

notifications= lambda: KeyboardInline([{_("Так точно"): "notify_yes", _("Никак нет"): "notify_no"}]).get()
my_group = lambda: KeyboardInline([{_("Пост для донатов"): "donation_post"}, {_("Ссылка для доната"): "donation_link"},
                                   {_("Размещать инфо о донатах"): "report_donations"}, {_("Назад"): "menu"}]).get()
donation_post = lambda: KeyboardInline([{_("Запостить"): "post_donation_post"},
                                        {_("Изменить"): "change_donation_post"},
                                        {_("Назад"): "my_group"}]).get()
post_donation_post = lambda: KeyboardInline([{_("К группе"): "my_group"}]).get()
group_donation_post = lambda url: KeyboardInline([{_("Задонатить"): f"url:{url}"}]).get()
