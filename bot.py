from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler, MessageHandler, \
    filters

from gpt import ChatGptService
from util import (load_message, load_prompt, send_text, send_image, show_main_menu, send_text_buttons, Dialog,
                  send_html)
import credentials, os

# Buttons handler for different functions
async def default_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    query = update.callback_query.data
    if dialog.mode == "random":
        if query == 'more_btn':
            await random(update, context)
        elif query == 'end_btn':
            await start(update, context)
    elif dialog.mode == "cv":
        if query == 'cv_start_over':
            await cv(update, context)
        elif query == 'cv_end_btn':
            await start(update, context)

# Buttons handler for the 'quiz' function
async def quiz_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    query = update.callback_query.data
    if dialog.mode == "quiz" or dialog.mode == "quiz_started":
        if query == 'quiz_prog':
            dialog.mode = "quiz_started"
            dialog.quiz_theme = "quiz_prog"
            await quiz_questions(update, context)
        elif query == 'quiz_math':
            dialog.mode = "quiz_started"
            dialog.quiz_theme = "quiz_math"
            await quiz_questions(update, context)
        elif query == 'quiz_biology':
            dialog.mode = "quiz_started"
            dialog.quiz_theme = "quiz_biology"
            await quiz_questions(update, context)
        elif query == 'quiz_more':
            dialog.quiz_theme = "quiz_more"
            await quiz_questions(update, context)
        elif query == 'quiz_change_theme':
            dialog.mode = "quiz_change_theme"
            dialog.quiz_theme = "quiz_change_theme"
            await quiz(update, context)
        elif query == 'quiz_end_btn':
            dialog.mode = "quiz_ended"
            dialog.quiz_theme = "quiz_ended"
            await start(update, context)

# Buttons handler for the 'talk' function
async def talk_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    query = update.callback_query.data
    if dialog.mode == "talk":
        if query == 'talk_1':
            await cobain(update, context)
        elif query == 'talk_2':
            await queen(update, context)
        elif query == 'talk_3':
            await tolkien(update, context)
        elif query == 'talk_4':
            await nietzsche(update, context)
        elif query == 'talk_5':
            await hawking(update, context)
        elif query == 'talk_end_btn':
            dialog.mode = "dialog_ended"
            await start(update, context)

# Buttons handler for the 'translator' function
async def translator_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    query = update.callback_query.data
    if dialog.mode == "translator":
        if query == 'translate_english':
            dialog.translation = "started"
            dialog.mode = "english"
            await languages(update, context)
        elif query == 'translate_german':
            dialog.translation = "started"
            dialog.mode = "german"
            await languages(update, context)
        elif query == 'translate_italian':
            dialog.translation = "started"
            dialog.mode = "italian"
            await languages(update, context)
        elif query == 'translate_french':
            dialog.translation = "started"
            dialog.mode = "french"
            await languages(update, context)
        elif query == 'translate_spanish':
            dialog.translation = "started"
            dialog.mode = "spanish"
            await languages(update, context)
        elif query == 'translate_change':
            dialog.translation = "None"
            dialog.mode = "change_lang"
            await translator(update, context)
        elif query == 'translate_end':
            dialog.translation = "not started"
            dialog.mode = "ended"
            await start(update, context)

# Buttons handler for the 'recommendations' function
async def recommendations_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    query = update.callback_query.data
    if dialog.mode == "recommendations" or dialog.mode == "recommendations_started":
        if query == 'recommendations_movies':
            dialog.mode = "recommendations_started"
            dialog.category = "movies"
            await category(update, context)
        elif query == 'recommendations_books':
            dialog.mode = "recommendations_started"
            dialog.category = "books"
            await category(update, context)
        elif query == 'recommendations_music':
            dialog.mode = "recommendations_started"
            dialog.category = "music"
            await category(update, context)
        elif query == 'recommendations_dislike':
            dialog.mode = "recommendations_started"
            dialog.category = "dislike"
            await category(update, context)
        elif query == 'recommendations_end_btn':
            dialog.mode = "recommendations_ended"
            dialog.category = "ended"
            await start(update, context)

# The 'Start' function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "default"
    text = load_message('main')
    await send_image(update, context, 'main')
    await send_html(update, context, text)
    await show_main_menu(update, context, {
        'start': 'Головне меню',
        'random': 'Дізнатися випадковий цікавий факт 🧠',
        'gpt': 'Задати питання чату GPT 🤖',
        'talk': 'Поговорити з відомою особистістю 👤',
        'quiz': 'Взяти участь у квізі ❓',
        'translator': 'Перекласти на обрану мову',
        'voice_chat_gpt': 'Голосовий ChatGPT',
        'recommendations': 'Рекомендації щодо фільмів, книг та музики',
        'image_recognition': 'Розпізнавання зображень',
        'cv': 'Згенерувати резюме'
        # Додати команду в меню можна так:
        # 'command': 'button text'
    })


# The 'Random' function
async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "random"
    text = load_message('random')
    await send_image(update, context, 'random')
    await send_text(update, context, text)
    prompt = load_message('random')
    chat_gpt.set_prompt(prompt)
    content = await chat_gpt.send_question(prompt, "Дай цікавий факт")
    await send_text_buttons(update, context, content, {
        "more_btn" : "Хочу ще факт",
        "end_btn" : "Закінчити"
    })


# The 'GPT' function
async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_message('gpt')
    await send_image(update, context, 'gpt')
    await send_text(update, context, text)
    dialog.mode = "gpt"
    prompt = load_prompt('gpt')
    chat_gpt.set_prompt(prompt)


# The 'Talk' function
async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_message('talk')
    await send_image(update, context, 'talk')
    dialog.mode = "talk"
    await send_text_buttons(update, context, text, {
        "talk_1" : "Курт Кобейн - Соліст гурту 'Nirvana'",
        "talk_2" : "Єлизавета II - Королева Об'єднаного Королівства",
        "talk_3" : "Джон Толкін - Автор 'Володаря Перснів'",
        "talk_4" : "Фрідріх Ніцше - Філософ",
        "talk_5" : "Стівен Гокінг - Астрофізик",
        "talk_end_btn": "Закінчити"
    })

# The function to imitate conversation between a user and Cobain. A part of the 'Talk' function
# It sends a picture of him and sets a prompt to ChatGPT to impersonate him
async def cobain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "dialog_started"
    await send_image(update, context, 'talk_cobain')
    await send_text(update, context, 'Привіт. Кобейн говорить. Шо там по питаннях?')
    prompt = load_prompt("talk_cobain")
    chat_gpt.set_prompt(prompt)

# The function to imitate conversation between a user and Hawking. A part of the 'Talk' function
# It sends a picture of him and sets a prompt to ChatGPT to impersonate him
async def hawking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "dialog_started"
    await send_image(update, context, 'talk_hawking')
    await send_text(update, context, "Вітаю. Це Сті́вен Ві́льям Го́кінг. Радий зустрічі.")
    prompt = load_prompt("talk_hawking")
    chat_gpt.set_prompt(prompt)

# The function to imitate conversation between a user and Nietzsche. A part of the 'Talk' function
# It sends a picture of him and sets a prompt to ChatGPT to impersonate him
async def nietzsche(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "dialog_started"
    await send_image(update, context, 'talk_nietzsche')
    await send_text(update, context, "Guten Tag. Подискутуємо?")
    prompt = load_prompt("talk_nietzsche")
    chat_gpt.set_prompt(prompt)

# The function to imitate conversation between a user and Queen. A part of the 'Talk' function
# It sends a picture of her and sets a prompt to ChatGPT to impersonate her
async def queen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "dialog_started"
    await send_image(update, context, 'talk_queen')
    await send_text(update, context, "Наливайте 'Ерл Ґрей', до Вас Королева говорить.")
    prompt = load_prompt("talk_queen")
    chat_gpt.set_prompt(prompt)

# The function to imitate conversation between a user and Tolkien. A part of the 'Talk' function
# It sends a picture of him and sets a prompt to ChatGPT to impersonate him
async def tolkien(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "dialog_started"
    await send_image(update, context, 'talk_tolkien')
    await send_text(update, context, "Вітання із Середзем'я. Запитуйте.")
    prompt = load_prompt("talk_tolkien")
    chat_gpt.set_prompt(prompt)


# The 'Quiz' function
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_message('quiz')
    await send_image(update, context, 'quiz')
    dialog.mode = "quiz"
    chat_gpt.set_prompt("quiz")
    await send_text_buttons(update, context, text, {
        "quiz_prog": "Програмування мовою Python",
        "quiz_math": "Математичні теорій - теорії алгоритмів, теорії множин та матаналізу",
        "quiz_biology": "Біологія",
        "quiz_end_btn": "Закінчити"
    })

# The function to handle text messages for the 'quiz' function only.
# It gets a message from a user (in the 'text' var) and sends it to chatGPT
# Then it gets an answer from chatGPT (in the 'answer' var) and sends it back to the user adding few buttons
async def handle_quiz_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # if dialog.mode == "quiz_prog" or dialog.mode == "quiz_math" or dialog.mode == "quiz_biology":
    text = update.message.text
    await chat_gpt.add_message(text)
    answer = await chat_gpt.send_message_list()
    await send_text_buttons(update, context, answer, {
        "quiz_more": "Інше питання на ту ж тему",
        "quiz_change_theme": "Змінити тему",
        "quiz_end_btn": "Закінчити"
    })

# The function to handle question according to the category button clicked.
# It sends a mini-prompt about the category to chatGPT, receives a question, and sends it to the user
async def quiz_questions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if dialog.quiz_theme == "quiz_prog":
        await send_image(update, context, 'quiz')
        await chat_gpt.add_message('Python')
        answer = await chat_gpt.send_message_list()
        await send_text(update, context, answer)
    elif dialog.quiz_theme == "quiz_math":
        await send_image(update, context, 'quiz')
        await chat_gpt.add_message('Math')
        answer = await chat_gpt.send_message_list()
        await send_text(update, context, answer)
    elif dialog.quiz_theme == "quiz_biology":
        await send_image(update, context, 'quiz')
        await chat_gpt.add_message('Biology')
        answer = await chat_gpt.send_message_list()
        await send_text(update, context, answer)
    elif dialog.quiz_theme == "quiz_more":
        await send_image(update, context, 'quiz')
        await chat_gpt.add_message('більше')
        answer = await chat_gpt.send_message_list()
        await send_text(update, context, answer)


# The 'Voice ChatGPT' function
async def voice_chat_gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_message('voice_chat_gpt')
    await send_image(update, context, 'voice_chat_gpt')
    await send_text(update, context, text)
    dialog.mode = "voice_chat_gpt"


# The 'Movies, Books, Music recommendations' function
async def recommendations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_message('recommendations')
    await send_image(update, context, 'recommendations')
    chat_gpt.set_prompt("recommendations")
    dialog.mode = "recommendations"
    await send_text_buttons(update, context, text, {
        "recommendations_movies": "Фільми",
        "recommendations_books": "Книги",
        "recommendations_music": "Музика",
        "recommendations_end_btn": "Закінчити"
    })

# The function to handle text messages for the 'recommendations' function only.
# It sends text to chatGPT, receives text, and sends it to the user adding a couple of buttons
async def handle_rec_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await chat_gpt.add_message(text)
    answer = await chat_gpt.send_message_list()
    await send_text_buttons(update, context, answer, {
        "recommendations_dislike": "Не подобається",
        "recommendations_end_btn": "Закінчити"
    })

# The function to handle different categories depending on the chosen button.
async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if dialog.category == "movies":
        await chat_gpt.add_message("Фільми")
        answer = await chat_gpt.send_message_list()
        await send_text(update, context, answer)
    elif dialog.category == "books":
        await chat_gpt.add_message("Книги")
        answer = await chat_gpt.send_message_list()
        await send_text(update, context, answer)
    elif dialog.category == "music":
        await chat_gpt.add_message("Музика")
        answer = await chat_gpt.send_message_list()
        await send_text(update, context, answer)
    elif dialog.category == "dislike":
        await chat_gpt.add_message("Не подобається. Надішли інше у тій же категорії та жанрі")
        answer = await chat_gpt.send_message_list()
        await send_text_buttons(update, context, answer, {
            "recommendations_dislike": "Не подобається",
            "recommendations_end_btn": "Закінчити"
        })


# The 'Translation' function
async def translator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_message('translator')
    await send_image(update, context, 'translator')
    dialog.mode = "translator"
    prompt = load_prompt('translator')
    chat_gpt.set_prompt(prompt)
    await send_text_buttons(update, context, text, {
        "translate_english" : "Англійська",
        "translate_german" : "Німецька",
        "translate_italian" : "Італійська",
        "translate_french" : "Французька",
        "translate_spanish" : "Іспанська",
        "translate_end": "Закінчити"
    })

# The function to handle text messages for the 'translator' function only.
# It sends text to be translated to chatGPT, receives translated text, and sends it to the user adding few buttons
async def handle_translator_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await chat_gpt.add_message(text)
    answer = await chat_gpt.send_message_list()
    await send_text_buttons(update, context, answer, {
        "translate_change" : "Змінити мову",
        "translate_end": "Закінчити"
    })

# The function to handle question according to the language button clicked.
# It sends a mini-prompt about the language to choose to chatGPT, and greets user using the choose language,
# and begins waiting for the user to input something to translate
async def languages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_image(update, context, 'translator')
    if dialog.mode == "english":
        await chat_gpt.add_message('english')
        answer = await chat_gpt.send_message_list()
        await send_text(update, context, answer)
        dialog.mode = "translator"
    elif dialog.mode == "german":
        await chat_gpt.add_message('german')
        answer = await chat_gpt.send_message_list()
        await send_text(update, context, answer)
        dialog.mode = "translator"
    elif dialog.mode == "italian":
        await chat_gpt.add_message('italian')
        answer = await chat_gpt.send_message_list()
        await send_text(update, context, answer)
        dialog.mode = "translator"
    elif dialog.mode == "french":
        await chat_gpt.add_message('french')
        answer = await chat_gpt.send_message_list()
        await send_text(update, context, answer)
        dialog.mode = "translator"
    elif dialog.mode == "spanish":
        await chat_gpt.add_message('spanish')
        answer = await chat_gpt.send_message_list()
        await send_text(update, context, answer)
        dialog.mode = "translator"


# The "Image recognition" function
async def image_recognition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "image_recognition"
    text = load_message('image_recognition')
    await send_image(update, context, 'image_recognition')
    await send_text(update, context, text)
    prompt = load_prompt('image_recognition')
    chat_gpt.set_prompt(prompt)

# The function to handle images.
# It downloads an image, and sends its path to the 'recognize_image' function in the 'gpt.py' module,
# receives an answer, and sends it to the user
# The picture must be less than 10 MB due to the chat version restrictions
async def handle_image_recognition_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.photo[-1].file_id
    bot = update.get_bot()
    file = await bot.get_file(file_id)
    path = await file.download_to_drive("image.jpg")
    answer = await chat_gpt.recognize_image(path, chat_gpt.client)
    await send_text(update, context, answer)
    if os.path.exists(path):
        os.remove(path)


# The 'curriculum vitae' function
async def cv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_message('cv')
    await send_image(update, context, 'cv')
    prompt = load_prompt('cv')
    chat_gpt.set_prompt(prompt)
    dialog.mode = "cv"
    await send_text(update, context, text)

# The function to handle text messages for the 'curriculum vitae' function only.
async def handle_cv_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await chat_gpt.add_message(text)
    answer = await chat_gpt.send_message_list()
    await send_text_buttons(update, context, answer, {
        "cv_start_over": "Почати спочатку",
        "cv_end_btn": "На головну"
    })


# Unique voice handler function
# It gets a voice file ID, downloads the file, and sends it to a function in the 'gpt.py' module to get text from audio
# Then, it sends the text to ChatGPT, receives text answer, converts it to audio, and sends it back to the user
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.voice.file_id
    bot = update.get_bot()
    file = await bot.get_file(file_id)
    path = await file.download_to_drive('user_voice.mp3')
    text = await chat_gpt.speech_to_text(path, chat_gpt.client)
    await chat_gpt.add_message(text)
    text_answer = await chat_gpt.send_message_list()
    await chat_gpt.text_to_speech(text_answer, chat_gpt.client)
    chat_id = update.message.chat_id
    await bot.send_voice(chat_id, "answer.mp3")


# Unique text handler function. It gets a message from a user (in the 'text' var) and sends it to chatGPT
# Then it gets an answer from chatGPT (in the 'answer' var) and sends it back to the user
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await chat_gpt.add_message(text)
    answer = await chat_gpt.send_message_list()
    await send_text(update, context, answer)


# The function to decide how to handle messages depending on the dialog.mode status
# So that chatGPT doesn't answer to the same theme when a different mode is enabled
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if dialog.mode == "gpt":
        await handle_text_message(update, context)
    if dialog.mode == "dialog_started":
        await handle_text_message(update, context)
    if dialog.mode == "quiz_started":
        await handle_quiz_message(update, context)
    if dialog.translation == "started":
        await handle_translator_message(update, context)
    if dialog.mode == "voice_chat_gpt":
        await handle_voice(update, context)
    if dialog.mode == "recommendations_started":
        await handle_rec_message(update, context)
    if dialog.mode == "image_recognition":
        await handle_text_message(update, context)
    if dialog.mode == "cv":
        await handle_cv_message(update, context)

chat_gpt = ChatGptService(credentials.ChatGPT_TOKEN)
app = ApplicationBuilder().token(credentials.BOT_TOKEN).build()
dialog = Dialog()

# Зареєструвати обробник команди можна так:
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('random', random))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(CommandHandler('talk', talk))
app.add_handler(CommandHandler('quiz', quiz))
app.add_handler(CommandHandler('translator', translator))
app.add_handler(CommandHandler('voice_chat_gpt', voice_chat_gpt))
app.add_handler(CommandHandler('recommendations', recommendations))
app.add_handler(CommandHandler('image_recognition', image_recognition))
app.add_handler(CommandHandler('cv', cv))
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.add_handler(MessageHandler(filters.VOICE, handle_voice))
app.add_handler(MessageHandler(filters.PHOTO, handle_image_recognition_message))

# Зареєструвати обробник колбеку можна так:
# app.add_handler(CallbackQueryHandler(app_button, pattern='^app_.*'))
app.add_handler(CallbackQueryHandler(quiz_callback_handler, pattern='^quiz_.*'))
app.add_handler(CallbackQueryHandler(talk_callback_handler, pattern='^talk_.*'))
app.add_handler(CallbackQueryHandler(translator_callback_handler, pattern='^translate_.*'))
app.add_handler(CallbackQueryHandler(recommendations_callback_handler, pattern='^recommendations_.*'))
app.add_handler(CallbackQueryHandler(default_callback_handler))
app.run_polling()