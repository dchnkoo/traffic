from abc import ABC, abstractmethod

from aiogram.utils.chat_action import ChatActionSender
from aiogram.client.default import Default
from aiogram import enums, types, Bot

from functools import partial

import typing as _t


class ChatModel(ABC):
    
    @property
    @abstractmethod
    def chat_id(self):
        ...

    @property
    @abstractmethod
    def bot(self) -> "Bot":
        ...

    @property
    def delete_message(self):
        return partial(self.bot.delete_message, self.chat_id)

    @property
    def get_chat(self):
        return partial(self.bot.get_chat, self.chat_id)
    
    @property
    def get_chat_member(self):
        return partial(self.bot.get_chat_member, self.chat_id)
    
    @property
    def leave_chat(self):
        return partial(self.bot.leave_chat, self.chat_id)
    
    async def send_message(
        self,
        text: str,
        business_connection_id: _t.Optional[str] = None,
        message_thread_id: _t.Optional[int] = None,
        parse_mode: _t.Optional[_t.Union[str, Default]] = enums.ParseMode.MARKDOWN_V2,
        entities: _t.Optional[list["types.MessageEntity"]] = None,
        link_preview_options: _t.Optional[_t.Union["types.LinkPreviewOptions", Default]] = Default(
            "link_preview"
        ),
        disable_notification: _t.Optional[bool] = None,
        protect_content: _t.Optional[_t.Union[bool, Default]] = Default("protect_content"),
        allow_paid_broadcast: _t.Optional[bool] = None,
        message_effect_id: _t.Optional[str] = None,
        reply_parameters: _t.Optional["types.ReplyParameters"] = None,
        reply_markup: _t.Optional[
            _t.Union["types.InlineKeyboardMarkup", "types.ReplyKeyboardMarkup", "types.ReplyKeyboardRemove", "types.ForceReply"]
        ] = None,
        allow_sending_without_reply: _t.Optional[bool] = None,
        disable_web_page_preview: _t.Optional[_t.Union[bool, Default]] = Default(
            "link_preview_is_disabled"
        ),
        reply_to_message_id: _t.Optional[int] = None,
        request_timeout: _t.Optional[int] = None,
    ) -> "types.Message":
        async with ChatActionSender.typing(
            self.chat_id, self.bot, message_thread_id=message_thread_id
        ):
            return await self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                business_connection_id=business_connection_id,
                message_effect_id=message_effect_id,
                message_thread_id=message_thread_id,
                parse_mode=parse_mode,
                entities=entities,
                link_preview_options=link_preview_options,
                disable_notification=disable_notification,
                protect_content=protect_content,
                allow_paid_broadcast=allow_paid_broadcast,
                reply_parameters=reply_parameters,
                reply_markup=reply_markup,
                allow_sending_without_reply=allow_sending_without_reply,
                disable_web_page_preview=disable_web_page_preview,
                reply_to_message_id=reply_to_message_id,
                request_timeout=request_timeout
            )
        
    async def set_my_commands(
        self,
        commands: list["types.BotCommand"],
        language_code: _t.Optional[str] = None,
        request_timeout: _t.Optional[int] = None,
    ) -> bool:
        return await self.bot.set_my_commands(
            commands=commands,
            scope=types.BotCommandScopeChat(chat_id=self.chat_id),
            language_code=language_code,
            request_timeout=request_timeout,
        )
    
    async def edit_message_text(
        self,
        text: str,
        business_connection_id: _t.Optional[str] = None,
        message_id: _t.Optional[int] = None,
        inline_message_id: _t.Optional[str] = None,
        parse_mode: _t.Optional[_t.Union[str, Default]] = enums.ParseMode.MARKDOWN_V2,
        entities: _t.Optional[list[types.MessageEntity]] = None,
        link_preview_options: _t.Optional[_t.Union[types.LinkPreviewOptions, Default]] = Default(
            "link_preview"
        ),
        reply_markup: _t.Optional[types.InlineKeyboardMarkup] = None,
        disable_web_page_preview: _t.Optional[_t.Union[bool, Default]] = Default(
            "link_preview_is_disabled"
        ),
        request_timeout: _t.Optional[int] = None,
    ) -> _t.Union[types.Message, bool]:
        return await self.bot.edit_message_text(
            text=text,
            business_connection_id=business_connection_id,
            chat_id=self.chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            reply_markup=reply_markup,
            disable_web_page_preview=disable_web_page_preview,
            request_timeout=request_timeout,
        )
