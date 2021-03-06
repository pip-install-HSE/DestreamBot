import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.deep_linking import get_start_link

from typing import *

from tortoise.exceptions import DoesNotExist

from ...db.models import BotUser, Group
from ...load_all import dp, bot
from . import texts, keyboards
from ...modules.api import API, BadResponseStatus
from ...modules.filters import Button, IsBotNewChatMember, IsItNotGroup
from ...config import moderators
from tortoise.query_utils import Q


class States(StatesGroup):
    token = State()
    add_group = State()
    notifications = State()
    change_donation_post = State()


@dp.message_handler(CommandStart(deep_link=""), IsItNotGroup(), state="*")
async def bot_user_start(message: types.Message, state: FSMContext, bot_user: BotUser):
    if not bot_user.token:
        await States.token.set()
        await message.answer(texts.bot_user_start(), reply_markup=keyboards.bot_user_start())
    else:
        await menu(message, await API(bot_user.token).get.user(), bot_user)


async def menu(message: types.Message, user: dict, bot_user: BotUser):
    await message.answer(
        texts.main_menu(user),
        reply_markup=keyboards.main_menu(await bot_user.groups.all().order_by("id")))


@dp.callback_query_handler(Button("menu"), state="*")
async def callback_menu(callback: types.CallbackQuery, bot_user: BotUser):
    await menu(callback.message, await API(bot_user.token).get.user(), bot_user)
    await callback.answer()


@dp.callback_query_handler(Button("reset_token_yes"), state="*")
@dp.message_handler(commands="delete_all", state="*")
async def delete_all(message_or_call: [types.Message, types.CallbackQuery], state: FSMContext, bot_user: BotUser):
    if isinstance(message_or_call, types.CallbackQuery):
        await message_or_call.answer()
        message = message_or_call.message
    else:
        message = message_or_call
    await bot_user.delete()
    bot_user = await BotUser.create(tg_id=message.chat.id)
    await bot_user_start(message, state, bot_user)


@dp.callback_query_handler(Button("reset_token"), state="*")
async def reset_token(callback: types.CallbackQuery, bot_user: BotUser):
    await callback.message.answer(texts.reset_token_confirm(), reply_markup=keyboards.reset_token_confirm())
    await callback.answer()


@dp.message_handler(IsItNotGroup(), state=States.token)
async def token(message: types.Message, state: FSMContext, bot_user: BotUser):
    try:
        user = await API(message.text).get.user()
    except BadResponseStatus:
        await message.answer(texts.error_token())
    else:
        bot_user.token = message.text
        await bot_user.save()
        await menu(message, user, bot_user)
        await state.reset_state(with_data=False)


@dp.callback_query_handler(Button("add_group"), state="*")
async def add_group(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message
    await message.answer(texts.add_group())
    await message.answer(f"destream-{message.chat.id}")
    await States.add_group.set()
    await callback.answer()


@dp.message_handler(content_types=types.ContentTypes.LEFT_CHAT_MEMBER, state="*")
async def left_chat_member(message: types.Message, state: FSMContext, bot_user: Union[BotUser, None] = None):
    if message.left_chat_member.id == (await bot.me).id:
        group = await Group.get(tg_id=message.chat.id)
        await group.delete()


@dp.channel_post_handler(lambda message: re.findall(r"destream-(\d+)", message.text), state="*")
@dp.message_handler(IsBotNewChatMember(), content_types=types.ContentTypes.NEW_CHAT_MEMBERS, state="*")
async def new_chat_member(message: types.Message, state: FSMContext, bot_user: Union[BotUser, None] = None):
    channel = False
    if message.chat.type == "channel":
        channel = True
    admin_id = re.findall(r"destream-(\d+)", message.text)[0] if channel else message.from_user.id
    chat = message.chat
    bot_user, _ = await BotUser.get_or_create(tg_id=admin_id) if channel else (bot_user, False)
    group_id, group_name = chat.id, chat.title
    group = await Group.get_or_none(tg_id=group_id)
    if group:
        group.admin, group.username = bot_user, group_name
        await group.save()
    else:
        await Group.create(tg_id=group_id, admin=bot_user, username=group_name)
    for moderator in moderators:
        try:
            await bot.send_message(moderator, f"New group: {group_id}\nAdmin: {admin_id}\n{group_name}")
        except:
            pass
    await state.storage.set_state(user=admin_id, state=States.notifications.state)
    await state.storage.update_data(user=admin_id, data={"group_id": group_id})
    try:
        await bot.send_message(chat_id=admin_id, text=texts.established_as_admin(),
                               reply_markup=keyboards.established_as_admin())
    except:
        pass
    try:
        await message.delete()
    except:
        pass


@dp.callback_query_handler(Button("established_as_admin"), state="*")
async def established_as_admin(callback: types.CallbackQuery, state: FSMContext, bot_user: BotUser):
    group_id = (await state.get_data())["group_id"]
    try:
        msg = await bot.send_message(chat_id=group_id, text="test", disable_notification=True)
    except:
        await callback.answer(texts.not_established_as_admin())
    else:
        await msg.delete()
        await callback.message.answer(text=texts.notifications(), reply_markup=keyboards.notifications())
        await callback.answer()


@dp.callback_query_handler(Button("notify_", True), state=States.notifications)
async def notify(callback: types.CallbackQuery, state: FSMContext):
    group_id = (await state.get_data()).get("group_id")
    notify = True if "yes" in callback.data else False
    await Group.filter(tg_id=group_id).update(is_report_donations=notify)
    await callback.message.answer(text=texts.notify(notify), reply_markup=keyboards.menu())
    await state.reset_state(with_data=False)
    await callback.answer()


async def get_min_sum(admin: BotUser):
    x = (await API(admin.token).get.user())["donationLimits"]
    return "\n".join(f"От {i['minAmount']} до {i['maxAmount']} {i['currency']}" for i in x)


@dp.callback_query_handler(Button("my_group", True), state="*")
async def my_group(callback: types.CallbackQuery, state: FSMContext, bot_user: BotUser):
    try:
        group_id = int(callback.data.split(":")[-1])
    except:
        group_id = (await state.get_data()).get("group_id")
    await state.update_data({"group_id": group_id})
    try:
        group = await Group.get(tg_id=group_id)
        assert group is not None
        await callback.message.answer(texts.my_group(group.username, await get_min_sum(bot_user)),
                                          reply_markup=keyboards.my_group(group.is_report_donations))
        await callback.answer()
    except (AssertionError, DoesNotExist):
        await callback.answer(texts.before_access__add_group())
        await menu(callback.message, await API(bot_user.token).get.user(), bot_user)


@dp.callback_query_handler(Button("report_donations"), state="*")
async def report_donations(callback: types.CallbackQuery, state: FSMContext, bot_user: BotUser):
    group_id = (await state.get_data()).get("group_id")
    is_report_donations = not (await Group.get(tg_id=group_id)).is_report_donations
    await Group.filter(tg_id=group_id).update(is_report_donations=is_report_donations)
    try:
        await callback.message.edit_reply_markup(keyboards.my_group(is_report_donations))
    except:
        await callback.answer(texts.changed_is_report_donations(is_report_donations))


@dp.callback_query_handler(Button("donation_post"), state="*")
async def donation_post(callback: types.CallbackQuery, state: FSMContext, bot_user: BotUser):
    group_id = (await state.get_data()).get("group_id")
    group = await Group.get(tg_id=group_id)
    await callback.message.answer(texts.donation_post(group.donation_post), reply_markup=keyboards.donation_post())
    await callback.answer()


@dp.callback_query_handler(Button("donation_text"), state="*")
async def donation_text(callback: types.CallbackQuery, state: FSMContext, bot_user: BotUser):
    group_id = (await state.get_data()).get("group_id")
    group = await Group.get(tg_id=group_id)
    start_link = await get_start_link(group.tg_id, True)
    message = callback.message
    await message.answer(f"{group.donation_post}\n\n{start_link}", reply_markup=keyboards.back_to_donation_post())
    await callback.answer()


@dp.callback_query_handler(Button("change_donation_post"), state="*")
async def change_donation_post(callback: types.CallbackQuery):
    await callback.message.answer(texts.set_donation_post())
    await States.change_donation_post.set()
    await callback.answer()


@dp.message_handler(IsItNotGroup(), state=States.change_donation_post)
async def real_change_donation_post(message: types.Message, state: FSMContext, bot_user: BotUser):
    group_id = (await state.get_data()).get("group_id")
    await Group.filter(tg_id=group_id).update(donation_post=message.text)
    await message.answer(texts.donation_post(message.text), reply_markup=keyboards.donation_post())
    await state.reset_state(with_data=False)


@dp.callback_query_handler(Button("post_donation_post"), state="*")
async def change_donation_post(callback: types.CallbackQuery, state: FSMContext, bot_user: BotUser):
    group_id = (await state.get_data()).get("group_id")
    group = await Group.get(tg_id=group_id)
    start_link = await get_start_link(group.tg_id, True)
    await bot.send_message(chat_id=group.tg_id, text=group.donation_post,
                           reply_markup=keyboards.group_donation_post(start_link))
    await callback.message.answer(texts.post_donation_post(), reply_markup=keyboards.post_donation_post())
    await callback.answer()


@dp.callback_query_handler(Button("donation_link"), state="*")
async def any_callback(callback: types.CallbackQuery, state: FSMContext, bot_user: BotUser):
    group_id = (await state.get_data()).get("group_id")
    group = await Group.get(tg_id=group_id)
    start_link = await get_start_link(group.tg_id, True)
    message = callback.message
    await message.answer(f"{start_link}", reply_markup=keyboards.back_to_group_settings())
    await callback.answer()


@dp.callback_query_handler(state="*")
async def any_callback(callback: types.CallbackQuery):
    await callback.answer(texts.maintenance())


@dp.message_handler(lambda message: "/start" not in message.text, IsItNotGroup(), state="*")
async def any_message(message: types.Message):
    await message.answer(texts.any_message())
