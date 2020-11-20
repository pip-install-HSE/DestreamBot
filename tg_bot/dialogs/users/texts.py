from ...load_all import _

currency = lambda: _("Выбери валюту:")

how_much = lambda min_sum, max_sum: _("<b>Сколько</b> ты хочешь задонатить?\n\nМожно донатить от ") + f"<b>{min_sum}</b>" + _(" и до ") + f"<b>{max_sum}.</b>"

sum_too_low_or_undefined = lambda: _("Сумма слишком <i>маленькая</i> или это не цифра, введите снова!")

message = lambda: _("Введи <i>сообщение для доната</i>. Только текст без кавычек и особых символов.")

webview_donation = lambda: _("Жми на кнопку и переходи к оплате!")
