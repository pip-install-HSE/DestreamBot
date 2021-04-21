from ...load_all import _
from ...modules.keyboard import KeyboardInline, KeyboardReply
from itertools import islice

def chunks(data, SIZE=10000):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k:data[k] for k in islice(it, SIZE)}


bot_user_start = lambda: KeyboardInline([{_("▶ Перейти в Destream"): "url:https://destream.net/"}, {"❓Служба поддержки": "url:https://destream.net/"}]).get()

main_menu = lambda groups: KeyboardInline([{"История донатов": "url:https://destream.net/", _("Вывести деньги"): "url:https://destream.net/"}] +
                                          [{"🔄 Сменить токен": "reset_token"}] +
                                          [i for i in chunks({f"{j+1}. {g.username}": f"my_group:{g.tg_id}" for j, g in enumerate(groups)}, 2)] +
                                          [{_("➕ Добавить группу"): "add_group"}]
                                          ).get()

menu = lambda : KeyboardInline([{"Меню": "menu"}]).get()

established_as_admin = lambda: KeyboardInline([{_("Готово"): "established_as_admin"}]).get()

notifications= lambda: KeyboardInline([{_("✅ Да"): "notify_yes", _("❌ Нет"): "notify_no"}]).get()
my_group = lambda is_report: KeyboardInline([{_("Сообщение для сбора донатов"): "donation_post"},
                                             {_("Ссылка на сбор донатов"): "donation_link"},
                                   {_("Не сообщать о новых донатах") if is_report else _("Сообщать о новых донатах"): "report_donations"},
                                    {_("⬅ Назад"): "menu"}]).get()
donation_post = lambda: KeyboardInline([{_("Запостить"): "post_donation_post", _("Текст поста"): "donation_text"},
                                        {_("Изменить"): "change_donation_post"},
                                        {_("⬅ Назад"): "my_group"}]).get()
post_donation_post = lambda: KeyboardInline([{_("К группе"): "my_group"}, {_("⬅ Назад"): "donation_post"}]).get()
group_donation_post = lambda url: KeyboardInline([{_("Задонатить"): f"url:{url}"}]).get()

back_to_donation_post = lambda: KeyboardInline([{_("⬅ Назад"): "donation_post"}]).get()
back_to_group_settings = lambda: KeyboardInline([{_("⬅ Назад"): "my_group"}]).get()
reset_token_confirm= lambda: KeyboardInline([{_("✅ Да"): "reset_token_yes", _("❌ Нет"): "menu"}]).get()