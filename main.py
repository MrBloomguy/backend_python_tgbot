#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

import logging
import asyncio
import json

from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ApplicationBuilder, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}\n\nSelect your token to buy",
        # reply_markup=ForceReply(selective=True),
        reply_markup =InlineKeyboardMarkup([[InlineKeyboardButton("ETH", callback_data='ETH'), InlineKeyboardButton("xDAI", callback_data='xDAI')]])
    )
    return START

    #     uint256 _buyThreshold, // price at which we want to trigger a buy (token 1 buy token 2)
    #     uint256 _sellThreshold, // price at which we want to trigger a sell (token 2 buy token 1)
    #     uint256 _slippageTolerance, // slippage tolerance
    #     uint256 _buyClipSize, // amount of token 1 to buy token 2
    #     uint256 _sellClipSize, // amount of token 2 to buy token 1
    #     address _swapRouter // address of swap router

async def token2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.callback_query.data
    user = update.effective_user
    # text = update.message.text
    context.user_data['token1'] = text

    await context.bot.send_message(user.id,
        f"Select your token to sell",
        reply_markup =InlineKeyboardMarkup([[InlineKeyboardButton("USDC", callback_data='USDC'), InlineKeyboardButton("DAI", callback_data='DAI')]])
    )
    return TOKEN2

async def buy_threshold(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    try:
        context.user_data['token2'] = update.callback_query.data
    except:
        await update.message.reply_text("Please enter a valid token")
        return TOKEN2
    await context.bot.send_message(user.id,
        # f"Hi {user.mention_html()}!\n\nSet your buy threshold",
        f"Set your buy threshold",
        reply_markup=ForceReply(selective=True),
    )
    return BUY_THRESHOLD

# Seeting sell threshold
async def sell_threshold(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    try:
        context.user_data['buy_threshold'] = float(text)
    except Exception as e:
        user = update.effective_user
        await update.message.reply_text("Please enter a valid number")
        return BUY_THRESHOLD

    await update.message.reply_html(
        f"Set your sell threshold",
        reply_markup =InlineKeyboardMarkup([[InlineKeyboardButton("Sell Threshold", callback_data='1')]])
    )
    return  SELL_THRESHOLD

async def buy_clip_size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    try:
        context.user_data['sell_threshold'] = float(text)
    except Exception as e:
        user = update.effective_user
        await update.message.reply_text("Please enter a valid number")
        return BUY_THRESHOLD

    await update.message.reply_html(
        f"Set your buy clip size",
        reply_markup =InlineKeyboardMarkup([[InlineKeyboardButton("Buy Clip Size", callback_data='1')]])
    )
    return  BUY_CLIP_SIZE

async def sell_clip_size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    try:
        context.user_data['buy_clip_size'] = float(text)
    except Exception as e:
        user = update.effective_user
        # user.
        await update.message.reply_text("Please enter a valid number")
        return BUY_THRESHOLD

    await update.message.reply_html(
        f"Set your sell clip size",
        reply_markup =InlineKeyboardMarkup([[InlineKeyboardButton("Sell Clip Size", callback_data='1')]])
    )
    return  SELL_CLIP_SIZE

async def submit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    try:
        context.user_data['sell_clip_size'] = float(text)
    except:
        user = update.effective_user
        update.message.reply_text("Please enter a valid number")
        return SELL_CLIP_SIZE
    a = context.user_data
    url = f"https://twap-cow-2.vercel.app/?token1={a['token1']}&token2={a['token2']}&buyThreshold={a['buy_threshold']}&sellThreshold={a['sell_threshold']}&buyClipSize={a['buy_clip_size']}&sellClipSize={a['sell_clip_size']}&slippageTolerance=0.1"
    print(url)
    await update.message.reply_text(f'Your order of {context.user_data["token1"]}/{context.user_data["token2"]} is:\n\nBuy Threshold: {context.user_data["buy_threshold"]}\nSell Threshold: {context.user_data["sell_threshold"]}\nBuy Clip Size: {context.user_data["buy_clip_size"]}\nSell Clip Size: {context.user_data["sell_clip_size"]}', reply_markup=ReplyKeyboardMarkup.from_button(KeyboardButton( text="Link your wallet!", web_app=WebAppInfo(url=url))))

    return SUBMIT 

# Handle incoming WebAppData
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Print the received data and remove the button."""
    # Here we use `json.loads`, since the WebApp sends the data JSON serialized string
    # (see webappbot.html)
    data = json.loads(update.effective_message.web_app_data.data)
    await update.message.reply_html(
        text=(
            f"Your trade just executed"
        ),
        reply_markup=ReplyKeyboardRemove(),
    )


async def send_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # text = update.message.text
    # context.user_data['sell_clip_size'] = float(text)
    user = update.effective_user
    context.bot.send_message(user.id, 'Recieved!')
    print('finish')

    return  

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Nuke the user message."""
    await update.message.reply_text("Your trade has been cancelled")

START, BUY_THRESHOLD, SELL_THRESHOLD, BUY_CLIP_SIZE, SELL_CLIP_SIZE, SUBMIT, TOKEN2 = range(7)

async def run_forever_hack():
    while True:
        await asyncio.sleep(1)

async def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    tg_token = '6842717160:AAE2-3fASHzoWtMagUtAd4E6K1XKFBDhnpo'
    app:Application = ApplicationBuilder().token(tg_token).read_timeout(30).write_timeout(30).concurrent_updates(True).build() 
    # app: Application = ptb_app
    async with app:
        # app = ApplicationBuilder().token(tg_token).read_timeout(40).write_timeout(40).build()

        # TODO: add block=False to all handlers
        entry_points = [CommandHandler('start', start), CommandHandler('cancel', cancel)]
        conv_handler = ConversationHandler(
            entry_points=entry_points,
            states={
                BUY_THRESHOLD: [MessageHandler(~filters.COMMAND, sell_threshold)],
                SELL_THRESHOLD: [MessageHandler(~filters.COMMAND, buy_clip_size)],
                BUY_CLIP_SIZE: [MessageHandler(~filters.COMMAND, sell_clip_size)],
                SELL_CLIP_SIZE: [MessageHandler(~filters.COMMAND, submit)],
                START: [CallbackQueryHandler(token2)],
                TOKEN2: [CallbackQueryHandler(buy_threshold)],
                SUBMIT: [CallbackQueryHandler(send_all)]
            },
            fallbacks=[CommandHandler('fallback', help_command)], allow_reentry=True)

        app.add_handler(conv_handler)
        await app.start()
        await app.updater.start_polling()
        await run_forever_hack()
        
        await app.updater.stop()
        await app.stop()


# if __name__ == "__main__":
#     main()
if __name__ == '__main__':
    asyncio.run(main())