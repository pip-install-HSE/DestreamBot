from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.deep_linking import decode_payload, get_start_link
from tortoise.exceptions import DoesNotExist

from ...db.models import BotUser, Group
from ...load_all import dp, bot
from . import texts, keyboards
from ...modules.api import API, BadResponseStatus
from ...modules.filters import Button, IsBotNewChatMember


class States(StatesGroup):
    token = State()
    add_group = State()
    notifications = State()
    change_donation_post = State()


@dp.message_handler(CommandStart(deep_link=""), state="*")
async def bot_user_start(message: types.Message, state: FSMContext, bot_user: BotUser):
    if not bot_user.token:
        await States.token.set()
        await message.answer(texts.bot_user_start(), reply_markup=keyboards.bot_user_start())
    else:
        await menu(message, await API(bot_user.token).get.user())


async def menu(message: types.Message, user: dict):
    await message.answer(
        texts.main_menu(user),
        reply_markup=keyboards.main_menu())


@dp.callback_query_handler(Button("menu"))
async def callback_menu(callback: types.CallbackQuery, bot_user: BotUser):
    await menu(callback.message, await API(bot_user.token).get.user())
    await callback.answer()


@dp.message_handler(state=States.token)
async def token(message: types.Message, state: FSMContext, bot_user: BotUser):
    try:
        user = await API(message.text).get.user()
    except BadResponseStatus:
        await message.answer(texts.error_token())
    else:
        bot_user.token = message.text
        await bot_user.save()
        await menu(message, user)
        await state.reset_state(with_data=False)


@dp.callback_query_handler(Button("add_group"), state="*")
async def add_group(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message
    await message.answer(texts.add_group())
    await States.add_group.set()
    await callback.answer()


@dp.message_handler(IsBotNewChatMember(), content_types=types.ContentTypes.NEW_CHAT_MEMBERS, state="*")
async def new_chat_member(message: types.Message, state: FSMContext, bot_user: BotUser):
    admin_id = message.from_user.id
    await state.storage.set_state(user=admin_id, state=States.notifications.state)
    await bot.send_message(chat_id=admin_id, text=texts.established_as_admin(), reply_markup=keyboards.established_as_admin())
    group, _ = await Group.get_or_create(admin=bot_user)
    group.username = message.chat.title
    group.tg_id = message.chat.id
    await group.save()


@dp.callback_query_handler(Button("established_as_admin"), state="*")
async def established_as_admin(callback: types.CallbackQuery, state: FSMContext, bot_user: BotUser):
    message = callback.message
    group_id = (await bot_user.groups.all().order_by("-id").first()).tg_id
    try:
        msg = await bot.send_message(chat_id=group_id, text="test")
    except:
        await callback.answer(texts.not_established_as_admin())
    else:
        await msg.delete()
        await bot.send_message(chat_id=message.chat.id, text=texts.notifications(), reply_markup=keyboards.notifications())
        await callback.answer()


@dp.callback_query_handler(Button("notify_yes"), state="*")
async def notify_yes(callback: types.CallbackQuery, state: FSMContext, bot_user: BotUser):
    message = callback.message
    await bot_user.groups.all().order_by("-id").first().update(is_report_donations=True)
    await bot.send_message(chat_id=message.chat.id, text=texts.notify_yes())
    await callback.answer()


@dp.callback_query_handler(Button("notify_no"), state=States.notifications)
async def notify_no(callback: types.CallbackQuery, state: FSMContext, bot_user: BotUser):
    message = callback.message
    await bot_user.groups.all().order_by("-id").first().update(is_report_donations=False)
    await bot.send_message(chat_id=message.chat.id, text=texts.notify_no())
    await state.reset_state(with_data=False)
    await callback.answer()


async def get_min_sum(group: Group):
    x = (await API(group.admin.token).get.user())["donationLimits"]
    return "\n".join(f"От {i['minAmount']} до {i['maxAmount']} {i['currency']}" for i in x)


@dp.callback_query_handler(Button("my_group"), state="*")
async def my_group(callback: types.CallbackQuery, bot_user: BotUser):
    message = callback.message
    if group := await bot_user.groups.all().order_by("-id").prefetch_related("admin").first():
        await message.answer(texts.my_group(group.username, await get_min_sum(group)), reply_markup=keyboards.my_group())
        await callback.answer()
    else:
        await callback.answer(texts.before_access__add_group())


@dp.callback_query_handler(Button("donation_post"), state="*")
async def donation_post(callback: types.CallbackQuery, state: FSMContext,  bot_user: BotUser):
    message = callback.message
    group = await bot_user.groups.all().order_by("-id").first()
    await message.answer(texts.donation_post(group.donation_post), reply_markup=keyboards.donation_post())
    await callback.answer()


@dp.callback_query_handler(Button("change_donation_post"), state="*")
async def change_donation_post(callback: types.CallbackQuery):
    await callback.message.answer(texts.set_donation_post())
    await States.change_donation_post.set()
    await callback.answer()


@dp.message_handler(state=States.change_donation_post)
async def real_change_donation_post(message: types.Message, state: FSMContext, bot_user: BotUser):
    await bot_user.groups.all().order_by("-id").first().update(donation_post=message.text)
    await message.answer(texts.donation_post(message.text), reply_markup=keyboards.donation_post())
    await state.reset_state(with_data=False)


@dp.callback_query_handler(Button("post_donation_post"), state="*")
async def change_donation_post(callback: types.CallbackQuery, bot_user: BotUser):
    group = await bot_user.groups.all().order_by("-id").first()
    start_link = await get_start_link(group.tg_id, True)
    await bot.send_message(chat_id=group.tg_id, text=group.donation_post, reply_markup=keyboards.group_donation_post(start_link))
    await callback.message.answer(texts.post_donation_post(), reply_markup=keyboards.post_donation_post())
    await callback.answer()


@dp.callback_query_handler(state="*")
async def any_callback(callback: types.CallbackQuery):
    await callback.answer(texts.maintenance())


@dp.message_handler(lambda message: "/start" not in message.text, state="*")
async def any_message(message: types.Message):
    await message.answer(texts.any_message())
# @dp.callback_query_handler(Button("add_group"), state="*"):
# await state.reset_state(with_data=False)
