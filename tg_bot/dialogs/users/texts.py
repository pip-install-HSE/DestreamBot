from ...load_all import _

currency = lambda: _("Выбери валюту:")

how_much = lambda min_sum: _("Сколько ты хочешь задонатить?\nМинимальная сумма: - ") + f"{min_sum}"

sum_too_low_or_undefined = lambda: _("Сумма слишком маленькая или это не цифра, введите снова!")

message = lambda: _("Введи текст, только текст без кавычек и особых символов")

webview_donation = lambda: _("Жми на кнопку и переходи к оплате!")
