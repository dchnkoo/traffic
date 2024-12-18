from aiogram.dispatcher.event.handler import CallbackType
from aiogram import Router, F, filters, enums
from aiogram.enums import chat_type


def extract_message_filters(*routers: Router) -> tuple[CallbackType]:
    return tuple(i.callback for j in routers for i in j.message._handler.filters)


clear_router = Router()

without_state = Router()
without_state.message.filter(filters.StateFilter(None))

only_msg_router = Router()
only_msg_router.message.filter(
    F.content_type == enums.ContentType.TEXT,
)

no_command = Router()
no_command.message.filter(~F.text.startswith("/"))

private_clear = Router()
private_clear.message.filter(F.chat.type == chat_type.ChatType.PRIVATE)

private_without_state = Router()
private_without_state.message.filter(
    *extract_message_filters(private_clear, without_state),
)

private_only_msg = Router()
private_only_msg.message.filter(
    *extract_message_filters(private_clear, only_msg_router)
)

private_only_msg_without_state = Router()
private_only_msg_without_state.message.filter(
    *extract_message_filters(without_state, private_only_msg)
)
