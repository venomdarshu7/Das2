import logging
import math
from FileStream import __version__
from FileStream.bot import FileStream
from FileStream.server.exceptions import FIleNotFound
from FileStream.utils.bot_utils import gen_linkx, verify_user
from FileStream.config import Telegram
from FileStream.utils.database import Database
from FileStream.utils.translation import LANG, BUTTON
from pyrogram import filters, Client
from random import choice
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.enums.parse_mode import ParseMode
import asyncio

db = Database(Telegram.DATABASE_URL, Telegram.SESSION_NAME)

EMOJIS = [
        "👍", "👎", "❤", "🔥", 
        "🥰", "👏", "😁", "🤔",
        "🤯", "😱", "🤬", "😢",
        "🎉", "🤩", "🤮", "💩",
        "🙏", "👌", "🕊", "🤡",
        "🥱", "🥴", "😍", "🐳",
        "❤‍🔥", "🌚", "🌭", "💯",
        "🤣", "⚡", "🍌", "🏆",
        "💔", "🤨", "😐", "🍓",
        "🍾", "💋", "🖕", "😈",
        "😴", "😭", "🤓", "👻",
        "👨‍💻", "👀", "🎃", "🙈",
        "😇", "😨", "🤝", "✍",
        "🤗", "🫡", "🎅", "🎄",
        "☃", "💅", "🤪", "🗿",
        "🆒", "💘", "🙉", "🦄",
        "😘", "💊", "🙊", "😎",
        "👾", "🤷‍♂", "🤷", "🤷‍♀",
        "😡"
]

STICKERS_IDS = ('CAACAgUAAxkBAAJiEmZ9wGpouK36GTLvSNipAj1UJINmAAIzDwACMld5Vq_5dLIkZKbZNQQ CAACAgUAAxkBAAJiG2Z94C_lIJQ-gtK4FOsjDk3dXXL9AAKIDAACX3ZYV3POKhr3mXUINQQ CAACAgUAAxkBAAJiMGZ_I9m2qjeXD4YwSFbHVJmWQOoHAALeCgACARFYV-wqL2ZeqpL4NQQ CAACAgUAAxkBAAJiMWZ_I9q2WXd6XX8UcGIYNPAUneYbAAJ6DwACeD9QV2EoARqmyYFQNQQ CAACAgUAAxkBAAJiNmZ_I-Qv7KQ7zvg4Lg5tvTiYwv4OAAJUDQACUShRV4t4aj9xXS0BNQQ CAACAgUAAxkBAAJiOWZ_I-bvHq7iGOSuUmg7xWAWYbDNAAKfEgACza1hV6x0FsXrtM8nNQQ CAACAgUAAxkBAAJiZWaAcljRI_HeSqvdKbuJWXHbpe7-AAKFDQACnaNgVzof05wAAXDjsDUE CAACAgUAAxkBAAJiZmaAclnxPo_HPKA_R4NYKb05ulcFAALoCwACd4thV49b_Uqh3qhTNQQ CAACAgUAAxkBAAJia2aAclvYoXpWW0ezQPuvI1DOdoZIAAKSEQACiXRgVxPhb2AYPT6hNQQ CAACAgUAAxkBAAJibmaAcl_roqxZpIBP2ZoGXoT3eJzHAAJuDAACiX1gVwtjKqyQ6bTQNQQ CAACAgUAAxkBAAJidGaAcmKH0nYXxVaQPX1_xg5w6IraAAIQDAACAVxgV4yJyW3974W-NQQ CAACAgUAAxkBAAJid2aAcmXYEVIeoP_obaJ2dObRfb-vAAIvEAACbJRgV2LzAaS8DJ4ZNQQ CAACAgUAAxkBAAJieGaAcmjCRUX3-FcyKUxQySGcOqbrAAJQDQACunFgV6b_SvOa2Y7QNQQ CAACAgUAAxkBAAJifWaAcmjBn7DQD0iDFVzhUILnKNvkAAKgEAACwJ2hV8JWS9RpAzqsNQQ CAACAgUAAxkBAAJigGaAcmzgCFIDGDJJg_FOyiM8VTSoAAK8DQAC5XthV2Ar4vHaamOYNQQ').split()


@FileStream.on_message(filters.command('start') & filters.private)
async def start(bot: Client, message: Message):
    if not await verify_user(bot, message):
        return
    usr_cmd = message.text.split("_")[-1]

    if usr_cmd == "/start":
        if Telegram.START_PIC:
            await message.react(choice(EMOJIS), big=True),
            m=await message.reply_sticker(sticker=random.choice(STICKERS_IDS))
            await asyncio.sleep(0.5)
            await m.delete()
            await message.reply_photo(
                photo=Telegram.START_PIC,
                caption=LANG.START_TEXT.format(message.from_user.mention, FileStream.username),
                parse_mode=ParseMode.HTML,
                reply_markup=BUTTON.START_BUTTONS
            )
        else:
            await message.react(choice(EMOJIS), big=True),
            m=await message.reply_sticker(sticker=random.choice(STICKERS_IDS))
            await asyncio.sleep(0.5)
            await m.delete()
            await message.reply_text(
                text=LANG.START_TEXT.format(message.from_user.mention, FileStream.username),
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                reply_markup=BUTTON.START_BUTTONS
            )
    else:
        if "stream_" in message.text:
            try:
                file_check = await db.get_file(usr_cmd)
                file_id = str(file_check['_id'])
                if file_id == usr_cmd:
                    reply_markup, stream_text = await gen_linkx(m=message, _id=file_id,
                                                                name=[FileStream.username, FileStream.fname])
                    await message.reply_text(
                        text=stream_text,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                        reply_markup=reply_markup,
                        quote=True
                    )

            except FIleNotFound as e:
                await message.reply_text("File Not Found")
            except Exception as e:
                await message.reply_text("Something Went Wrong")
                logging.error(e)

        elif "file_" in message.text:
            try:
                file_check = await db.get_file(usr_cmd)
                db_id = str(file_check['_id'])
                file_id = file_check['file_id']
                file_name = file_check['file_name']
                if db_id == usr_cmd:
                    filex = await message.reply_cached_media(file_id=file_id, caption=f'**{file_name}**')
                    await asyncio.sleep(3600)
                    try:
                        await filex.delete()
                        await message.delete()
                    except Exception:
                        pass

            except FIleNotFound as e:
                await message.reply_text("**File Not Found**")
            except Exception as e:
                await message.reply_text("Something Went Wrong")
                logging.error(e)

        else:
            await message.reply_text(f"**Invalid Command**")

@FileStream.on_message(filters.private & filters.command(["about"]))
async def start(bot, message):
    if not await verify_user(bot, message):
        return
    if Telegram.START_PIC:
        await message.react(choice(EMOJIS), big=True),
        m=await message.reply_sticker(sticker=random.choice(STICKERS_IDS))
        await asyncio.sleep(0.5)
        await m.delete()
        await message.reply_photo(
            photo=Telegram.START_PIC,
            caption=LANG.ABOUT_TEXT.format(FileStream.fname, __version__),
            parse_mode=ParseMode.HTML,
            reply_markup=BUTTON.ABOUT_BUTTONS
        )
    else:
        await message.react(choice(EMOJIS), big=True),
        m=await message.reply_sticker(sticker=random.choice(STICKERS_IDS))
        await asyncio.sleep(0.5)
        await m.delete()
        await message.reply_text(
            text=LANG.ABOUT_TEXT.format(FileStream.fname, __version__),
            disable_web_page_preview=True,
            reply_markup=BUTTON.ABOUT_BUTTONS
        )

@FileStream.on_message((filters.command('help')) & filters.private)
async def help_handler(bot, message):
    if not await verify_user(bot, message):
        return
    if Telegram.START_PIC:
        await message.react(choice(EMOJIS), big=True),
        m=await message.reply_sticker(sticker=random.choice(STICKERS_IDS))
        await asyncio.sleep(0.5)
        await m.delete()
        await message.reply_photo(
            photo=Telegram.START_PIC,
            caption=LANG.HELP_TEXT.format(Telegram.OWNER_ID),
            parse_mode=ParseMode.HTML,
            reply_markup=BUTTON.HELP_BUTTONS
        )
    else:
        await message.react(choice(EMOJIS), big=True),
        m=await message.reply_sticker(sticker=random.choice(STICKERS_IDS))
        await asyncio.sleep(0.5)
        await m.delete()
        await message.reply_text(
            text=LANG.HELP_TEXT.format(Telegram.OWNER_ID),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=BUTTON.HELP_BUTTONS
        )

# ---------------------------------------------------------------------------------------------------

@FileStream.on_message(filters.command('files') & filters.private)
async def my_files(bot: Client, message: Message):
    if not await verify_user(bot, message):
        return
    user_files, total_files = await db.find_files(message.from_user.id, [1, 10])

    file_list = []
    async for x in user_files:
        file_list.append([InlineKeyboardButton(x["file_name"], callback_data=f"myfile_{x['_id']}_{1}")])
    if total_files > 10:
        file_list.append(
            [
                InlineKeyboardButton("◄", callback_data="N/A"),
                InlineKeyboardButton(f"1/{math.ceil(total_files / 10)}", callback_data="N/A"),
                InlineKeyboardButton("►", callback_data="userfiles_2")
            ],
        )
    if not file_list:
        file_list.append(
            [InlineKeyboardButton("ᴇᴍᴘᴛʏ", callback_data="N/A")],
        )
    file_list.append([InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")])
    await message.reply_photo(photo=Telegram.FILE_PIC,
                              caption="Total files: {}".format(total_files),
                              reply_markup=InlineKeyboardMarkup(file_list))


