import os
import sqlite3
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from parser import Seller


load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
DB_PATH = "resell.db"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

# Создаём один экземпляр Seller для проверки ссылок
seller_checker = Seller()

# ------------------ KEYBOARDS ------------------

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Добавить подписку")],
        [KeyboardButton(text="📌 Мои подписки")],
    ],
    resize_keyboard=True,
)

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Отмена")]],
    resize_keyboard=True,
)

# ------------------ STATES ------------------

user_states = {}


def reset_state(user_id: int):
    """
    Reset the state for a user. Removes the user from the state dictionary.

    Args:
        user_id (int): Telegram user ID.
    """
    if user_id in user_states:
        user_states.pop(user_id)


# ------------------ DB ------------------

def get_conn():
    """
    Get a SQLite connection to the database.

    Returns:
        sqlite3.Connection: Database connection with row_factory set to sqlite3.Row.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def add_user(tg_id: int):
    """
    Add a Telegram user to the database if not exists.

    Args:
        tg_id (int): Telegram user ID.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (tg_id) VALUES (?)", (tg_id,))
    conn.commit()
    conn.close()


def get_user_id(tg_id: int):
    """
    Retrieve internal user ID from Telegram ID.

    Args:
        tg_id (int): Telegram user ID.

    Returns:
        int | None: Internal user ID or None if not found.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE tg_id = ?", (tg_id,))
    row = cur.fetchone()
    conn.close()
    return row["id"] if row else None


def add_subscription(user_id: int, query: str, url: str):
    """
    Add a new subscription for a user.

    Args:
        user_id (int): Internal user ID.
        query (str): Subscription name.
        url (str): Avito search URL.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO subscriptions (user_id, query, url) VALUES (?, ?, ?)",
        (user_id, query, url),
    )
    conn.commit()
    conn.close()


def get_subscriptions(user_id: int):
    """
    Retrieve all subscriptions of a user.

    Args:
        user_id (int): Internal user ID.

    Returns:
        list[sqlite3.Row]: List of subscription rows.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM subscriptions WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_subscription(sub_id: int, user_id: int):
    """
    Delete a subscription by ID for a specific user.

    Args:
        sub_id (int): Subscription ID.
        user_id (int): Internal user ID.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM subscriptions WHERE id = ? AND user_id = ?",
        (sub_id, user_id),
    )
    conn.commit()
    conn.close()


def get_new_items_for_user(user_id: int):
    """
    Retrieve new items for a user that have not been sent yet.

    Args:
        user_id (int): Internal user ID.

    Returns:
        list[sqlite3.Row]: List of new item rows.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT items.*
        FROM items
        JOIN subscriptions
          ON items.query_name = subscriptions.query
        WHERE subscriptions.user_id = ?
          AND items.id NOT IN (
              SELECT item_id FROM sent_items WHERE user_id = ?
          )
        """,
        (user_id, user_id),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def mark_item_sent(user_id: int, item_id: int):
    """
    Mark an item as sent to a user to avoid duplicate notifications.

    Args:
        user_id (int): Internal user ID.
        item_id (int): Item ID.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO sent_items (user_id, item_id) VALUES (?, ?)",
        (user_id, item_id),
    )
    conn.commit()
    conn.close()


# ------------------ HANDLERS ------------------

@router.message(Command("start"))
async def start(message: types.Message):
    """
    Handle the /start command. Adds the user to the database and shows the main menu.

    Args:
        message (types.Message): Incoming Telegram message.
    """
    reset_state(message.from_user.id)
    add_user(message.from_user.id)

    await message.answer(
        "Привет 👋\n"
        "Я отслеживаю новые товары по твоим подпискам.\n\n"
        "Выбирай действие кнопками 👇",
        reply_markup=main_kb,
    )


# ❌ CANCEL

@router.message(lambda m: m.text == "❌ Отмена")
async def cancel(message: types.Message):
    """
    Cancel current action and reset state.

    Args:
        message (types.Message): Incoming Telegram message.
    """
    reset_state(message.from_user.id)
    await message.reply("Ок, отменено 👍", reply_markup=main_kb)


# ➕ ADD SUBSCRIPTION

@router.message(lambda m: m.text == "➕ Добавить подписку")
async def add_sub_button(message: types.Message):
    """
    Start the process of adding a new subscription.

    Args:
        message (types.Message): Incoming Telegram message.
    """
    reset_state(message.from_user.id)
    user_states[message.from_user.id] = {"step": "wait_url"}

    await message.reply(
        "🔗 Пришли ссылку на поиск Avito\n\n"
        "⚠️ Важно:\n"
        "— Регион: «Во всех регионах»\n"
        "— Сортировка: «По дате»",
        reply_markup=cancel_kb,
    )


# 👉 Получение URL + проверка

@router.message(
    lambda m: m.from_user.id in user_states
    and user_states[m.from_user.id]["step"] == "wait_url"
)
async def add_sub_get_url(message: types.Message):
    """
    Receive the URL from the user, validate it, and ask for subscription name.

    Args:
        message (types.Message): Incoming Telegram message.
    """
    url = message.text.strip()
    await message.reply("⏳ Проверяю ссылку...")

    is_valid = await asyncio.to_thread(seller_checker.correct_link, url)

    if not is_valid:
        await message.reply(
            "❌ Неверная ссылка.\n\n"
            "Убедись, что:\n"
            "— выбран регион «Во всех регионах»\n"
            "— сортировка стоит «По дате»\n\n"
            "Попробуй отправить ссылку снова.",
            reply_markup=cancel_kb,
        )
        return

    user_states[message.from_user.id]["url"] = url
    user_states[message.from_user.id]["step"] = "wait_query"

    await message.reply(
        "✅ Ссылка корректна!\n\n"
        "✏️ Теперь пришли название подписки",
        reply_markup=cancel_kb,
    )


# 👉 Получение названия

@router.message(
    lambda m: m.from_user.id in user_states
    and user_states[m.from_user.id]["step"] == "wait_query"
)
async def add_sub_get_query(message: types.Message):
    """
    Receive subscription name and save subscription to the database.

    Args:
        message (types.Message): Incoming Telegram message.
    """
    data = user_states.pop(message.from_user.id)
    user_id = get_user_id(message.from_user.id)

    add_subscription(user_id, message.text, data["url"])

    await message.reply(
        f"✅ Подписка «{message.text}» добавлена",
        reply_markup=main_kb,
    )


# 📌 LIST + DELETE SUBS

@router.message(lambda m: m.text == "📌 Мои подписки")
async def subs_button(message: types.Message):
    """
    Show all subscriptions of the user with options to view or delete.

    Args:
        message (types.Message): Incoming Telegram message.
    """
    reset_state(message.from_user.id)
    user_id = get_user_id(message.from_user.id)
    subs = get_subscriptions(user_id)

    if not subs:
        await message.reply("📭 Подписок пока нет", reply_markup=main_kb)
        return

    text = "<b>📌 Мои подписки:</b>\n\n"
    keyboard = []

    for index, s in enumerate(subs, start=1):
        text += f"{index}. <b>{s['query']}</b>\n"
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"🔎 {s['query']}",
                    url=s["url"],
                ),
                InlineKeyboardButton(
                    text="❌",
                    callback_data=f"del_sub:{s['id']}",
                ),
            ]
        )

    kb = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await message.reply(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=kb,
        link_preview_options=types.LinkPreviewOptions(is_disabled=True),
    )


@router.callback_query(lambda c: c.data.startswith("del_sub:"))
async def delete_sub_callback(callback: types.CallbackQuery):
    """
    Handle deletion of a subscription via inline button.

    Args:
        callback (types.CallbackQuery): Callback query from inline button.
    """
    sub_id = int(callback.data.split(":")[1])
    user_id = get_user_id(callback.from_user.id)

    delete_subscription(sub_id, user_id)

    await callback.message.edit_text("❌ Подписка удалена")
    await callback.answer()


# ------------------ SCRAPER LOOP ------------------

async def scrap_and_notify():
    """
    Infinite loop that scrapes new items and notifies users.
    Runs in background using asyncio.
    """
    seller = Seller()

    try:
        while True:
            await asyncio.to_thread(seller.scrap)

            conn = get_conn()
            cur = conn.cursor()
            cur.execute("SELECT id, tg_id FROM users")
            users = cur.fetchall()
            conn.close()

            for user in users:
                items = get_new_items_for_user(user["id"])

                for item in items:
                    text = (
                        f"🆕 <b>{item['query_name']}</b>\n"
                        f"Цена: {item['price']} ₽\n"
                        f"<a href='{item['url']}'>Открыть объявление</a>"
                    )

                    try:
                        if item["image_url"]:
                            await bot.send_photo(
                                user["tg_id"],
                                item["image_url"],
                                caption=text,
                                parse_mode=ParseMode.HTML,
                            )
                        else:
                            await bot.send_message(
                                user["tg_id"],
                                text,
                                parse_mode=ParseMode.HTML,
                            )

                        mark_item_sent(user["id"], item["id"])

                    except Exception as e:
                        print("SEND ERROR:", e)

            await asyncio.sleep(600)

    finally:
        seller.close()


# ------------------ MAIN ------------------

async def main():
    """
    Main entry point for the bot. Sets up router and starts polling.
    """
    dp.include_router(router)
    asyncio.create_task(scrap_and_notify())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
