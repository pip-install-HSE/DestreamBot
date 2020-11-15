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


@dp.callback_query_handler(state=States.how_much)
async def subscriber_how_much(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data({"currency": callback.data})
    await callback.message.answer(texts.how_much())


def get_limit(donation_limits: list, currency: float):
    for limit in donation_limits:
        if limit["currency"] == currency:
            return limit
    return False


@dp.message_handler(state=States.how_much)
async def subscriber_how_much_msg(message: types.Message, state: FSMContext):
    state_data = (await state.get_data())
    group_id = state_data.get("group_id")
    currency = state_data.get("currency")
    token = (await Group.get(tg_id=group_id)).admin.token
    group_admin = await API(token).get.user()
    try:
        amount = float(message.text)
    except:
        await message.answer(texts.sum_too_low_or_undefined())
    else:
        if ((limit := get_limit(group_admin['donationLimits'], currency))
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
    token = (await Group.get(tg_id=group_id)).admin.token
    url = API(token).post.donation(currency=state_data.get("currency"), amount=state_data.get("amount"),
                                   message=message.text)
    await message.answer(texts.webview_donation(), reply_markup=keyboards.webview_donation(url))
