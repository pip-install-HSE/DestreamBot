from typing import Dict

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters.state import StatesGroup, State

from . import texts, keyboards
from ...db.models import *
from ...load_all import dp
from ...modules.api import API
from ...modules.filters import IsUserSubscriber


class States(StatesGroup):
    how_much = State()
    message = State()


@dp.message_handler(IsUserSubscriber(), state="*")
async def subscriber_start_currency(message: types.Message, state: FSMContext, bot_user: BotUser, group_id: int):
    await message.answer(texts.currency(), reply_markup=keyboards.currency())
    await States.how_much.set()
    await state.update_data({"group_id": group_id})


def get_limit(donation_limits: list, currency: float):
    for limit in donation_limits:
        if limit["currency"] == currency:
            return limit
    return False


@dp.callback_query_handler(state=States.how_much)
async def subscriber_how_much(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data({"currency": callback.data})
    group_admin = await get_admin((await state.get_data()).get("group_id"))
    limit = get_limit(group_admin['donationLimits'], callback.data)
    await callback.message.answer(texts.how_much(f"{limit['minAmount']} {limit['currency']}"))


async def get_admin(group_id: [str, int]):
    token = (await Group.get(tg_id=group_id).prefetch_related("admin")).admin.token
    return await API(token).get.user()


@dp.message_handler(state=States.how_much)
async def subscriber_how_much_msg(message: types.Message, state: FSMContext):
    state_data = (await state.get_data())
    group_admin = await get_admin(state_data.get("group_id"))
    try:
        amount = float(message.text)
    except:
        await message.answer(texts.sum_too_low_or_undefined())
    else:
        if ((limit := get_limit(group_admin['donationLimits'], state_data.get("currency")))
                and limit["maxAmount"] > amount > limit["minAmount"]):
            await state.update_data({"amount": amount})
            await message.answer(texts.message())
            await States.message.set()
        else:
            await message.answer(texts.sum_too_low_or_undefined())


@dp.message_handler(state=States.message)
async def subscriber_message(message: types.Message, state: FSMContext):
    state_data = (await state.get_data())
    group_id = state_data.get("group_id")
    token = (await Group.get(tg_id=group_id).prefetch_related("admin")).admin.token
    url = await API(token).post.donation(currency=state_data.get("currency"), amount=state_data.get("amount"),
                                         message=message.text,
                                         additional_parameters={"usr_tg_id": message.chat.id, "group_id": group_id})
    await message.answer(texts.webview_donation(), reply_markup=keyboards.webview_donation(url))
