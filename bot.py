#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.


import logging
from typing import Dict
from core import *
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ['Esametro', 'Distico Elegiaco'],
    ['Fine'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for input."""
    update.message.reply_text(
        "Seleziona un tipo di verso o di strofe ",
        reply_markup=markup,
    )

    return CHOOSING


def regular_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data['metro'] = text
    update.message.reply_text(
        f'Hai selezionato **{text}**. Inviami dei versi!',
        parse_mode=ParseMode.MARKDOWN)

    return TYPING_REPLY


def received_information(update: Update, context: CallbackContext) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    metro = user_data['metro']
    versi = text.split("\n")
    risposta = []
    versi = [x.strip() for x in versi if x.strip() != ""]
    for index, versoOriginale in enumerate(versi):
        if metro == "Esametro" or (metro == "Distico Elegiaco" and index % 2 == 0):
            verso = Esametro(versoOriginale)
        elif (metro == "Distico Elegiaco") and (index % 2 == 1):
            verso = Pentametro(versoOriginale)
        verso.dividiInSillabe()
        soluzioni = verso.risolvi()
        if len(soluzioni) == 0:
            risposta.append("❌    <i>NESSUNA SOLUZIONE ("+str(verso)+")</i>")
        elif len(soluzioni) == 1:
            risposta.append(soluzioni[0])
        else:
            [risposta.append("❔    <i>"+str(x)+"</i>") for x in soluzioni]
            risposta.append("")

    update.message.reply_text(
        "📜<b> La scansione metrica è:</b>\n\n" +
        "\n".join(risposta).replace("à", "<b>à</b>")
        .replace("è", "<b>è</b>")
        .replace("ì", "<b>ì</b>")
        .replace("ò", "<b>ò</b>")
        .replace("ù", "<b>ù</b>")
        .replace("À", "<b>À</b>")
        .replace("È", "<b>È</b>")
        .replace("Ì", "<b>Ì</b>")
        .replace("Ò", "<b>Ò</b>")
        .replace("Ù", "<b>Ù</b>"),
        reply_markup=markup,
        parse_mode=ParseMode.HTML
    )

    return CHOOSING


def done(update: Update, context: CallbackContext) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    token_file = open("TOKEN")
    token = token_file.readline()
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                Filters.regex(
                    '^(Esametro|Distico Elegiaco|Fine)$'), regular_choice
            ),
            MessageHandler(
                Filters.text & ~(Filters.regex(
                    '^(Esametro|Distico Elegiaco|Fine)$')), start
            )
        ],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex(
                        '^(Esametro|Distico Elegiaco)$'), regular_choice
                )
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex(
                        '^(Esametro|Distico Elegiaco|Fine)$')), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command |
                                     Filters.regex('^(Esametro|Distico Elegiaco|Fine)$')),
                    received_information,
                ),
                MessageHandler(
                    Filters.regex(
                        '^(Esametro|Distico Elegiaco|Fine)$'), regular_choice
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Fine$'), done)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
