from ...load_all import _
from ...modules.keyboard import KeyboardInline, KeyboardReply

bot_user_start = lambda: KeyboardInline([{_("Вебвьюха"): "url:http://example.com"}]).get()



