from ...modules.keyboard import *

currency = lambda: KeyboardInline([{"RUB": "RUB", "EUR": "EUR"}, {"USD": "USD"}]).get()

webview_donation = lambda url: KeyboardInline([{"Перейти": f"url:{url}"}]).get()