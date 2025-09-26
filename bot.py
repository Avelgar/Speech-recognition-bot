import os
import io
import speech_recognition as sr
from pydub import AudioSegment
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
# Токены
BOT_TOKEN = "Ваш токен бота"  # Ваш токен бота

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /start"""
    welcome_text = (
        "🎨 Добро пожаловать в бот-генератор изображений!\n\n"
        "Я умею:\n"
        "• Конвертировать голосовые сообщения в текст\n"
        "• Распознавать текст из видео-сообщений\n"
        "• Извлекать аудио из видеофайлов и преобразовывать в текст\n"
        "Просто отправьте мне сообщение в нужном формате!"
    )
    await update.message.reply_text(welcome_text)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка голосовых сообщений"""
    voice = update.message.voice
    file = await voice.get_file()
    
    # Скачиваем голосовое сообщение
    await file.download_to_drive("voice.ogg")
    
    try:
        # Конвертируем OGG в WAV
        audio = AudioSegment.from_ogg("voice.ogg")
        audio.export("voice.wav", format="wav")
        
        # Распознаем текст
        recognizer = sr.Recognizer()
        with sr.AudioFile("voice.wav") as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="ru-RU")
                # Отвечаем на исходное сообщение с распознанным текстом
                await update.message.reply_text(
                    f"🎤 Распознанный текст:\n\n{text}", 
                    reply_to_message_id=update.message.message_id
                )
            except sr.UnknownValueError:
                await update.message.reply_text(
                    "Речь не распознана. Попробуйте говорить четче.", 
                    reply_to_message_id=update.message.message_id
                )
            except Exception as e:
                await update.message.reply_text(
                    f"Ошибка распознавания: {str(e)}", 
                    reply_to_message_id=update.message.message_id
                )
    
    except Exception as e:
        await update.message.reply_text(
            f"Ошибка обработки голосового сообщения: {str(e)}", 
            reply_to_message_id=update.message.message_id
        )
    
    # Удаляем временные файлы
    if os.path.exists("voice.ogg"):
        os.remove("voice.ogg")
    if os.path.exists("voice.wav"):
        os.remove("voice.wav")

async def handle_video_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка видео-сообщений (кружочков)"""
    video_note = update.message.video_note
    file = await video_note.get_file()
    
    # Скачиваем видео-сообщение
    await file.download_to_drive("video_note.mp4")
    
    try:
        # Извлекаем аудио из видео
        audio = AudioSegment.from_file("video_note.mp4")
        audio.export("audio_from_video.wav", format="wav")
        
        # Распознаем текст
        recognizer = sr.Recognizer()
        with sr.AudioFile("audio_from_video.wav") as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="ru-RU")
                # Отвечаем на исходное сообщение с распознанным текстом
                await update.message.reply_text(
                    f"🎥 Распознанный текст из видео-сообщения:\n\n{text}", 
                    reply_to_message_id=update.message.message_id
                )
            except sr.UnknownValueError:
                await update.message.reply_text(
                    "Речь не распознана. Попробуйте говорить четче.", 
                    reply_to_message_id=update.message.message_id
                )
            except Exception as e:
                await update.message.reply_text(
                    f"Ошибка распознавания: {str(e)}", 
                    reply_to_message_id=update.message.message_id
                )
    
    except Exception as e:
        await update.message.reply_text(
            f"Ошибка обработки видео: {str(e)}", 
            reply_to_message_id=update.message.message_id
        )
    
    # Удаляем временные файлы
    if os.path.exists("video_note.mp4"):
        os.remove("video_note.mp4")
    if os.path.exists("audio_from_video.wav"):
        os.remove("audio_from_video.wav")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка обычных видеофайлов"""
    video = update.message.video
    file = await video.get_file()
    
    # Скачиваем видеофайл
    video_filename = f"video_{video.file_id}.mp4"
    await file.download_to_drive(video_filename)
    
    try:
        # Извлекаем аудио из видео
        audio = AudioSegment.from_file(video_filename)
        audio_filename = f"audio_from_{video.file_id}.wav"
        audio.export(audio_filename, format="wav")
        
        # Распознаем текст
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_filename) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="ru-RU")
                # Отвечаем на исходное сообщение с распознанным текстом
                await update.message.reply_text(
                    f"🎬 Распознанный текст из видеофайла:\n\n{text}", 
                    reply_to_message_id=update.message.message_id
                )
            except sr.UnknownValueError:
                await update.message.reply_text(
                    "Речь не распознана. Попробуйте говорить четче.", 
                    reply_to_message_id=update.message.message_id
                )
            except Exception as e:
                await update.message.reply_text(
                    f"Ошибка распознавания: {str(e)}", 
                    reply_to_message_id=update.message.message_id
                )
    
    except Exception as e:
        await update.message.reply_text(
            f"Ошибка обработки видеофайла: {str(e)}", 
            reply_to_message_id=update.message.message_id
        )
    
    # Удаляем временные файлы
    if os.path.exists(video_filename):
        os.remove(video_filename)
    if os.path.exists(audio_filename):
        os.remove(audio_filename)

async def handle_other_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка всех остальных сообщений"""
    await update.message.reply_text(
        "Я понимаю следующие типы сообщений:\n"
        "• Голосовые сообщения\n"
        "• Видео-сообщения (кружочки)\n"
        "• Обычные видеофайлы\n\n"
        "Отправьте мне один из этих форматов!",
        reply_to_message_id=update.message.message_id
    )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Обработчики
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(MessageHandler(filters.VIDEO_NOTE, handle_video_note))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.add_handler(MessageHandler(filters.ALL, handle_other_messages))
    
    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()