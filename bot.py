import telebot
import os
import yt_dlp

API_TOKEN = '8701532400:AAEhFRAlc_gqfiNVsfuFab6pAl7A4eDgOHc'
bot = telebot.TeleBot(API_TOKEN)

# Function to download video using yt-dlp
def download_tiktok(url):
    output_filename = 'tiktok_video.mp4'
    
    # Options for yt-dlp to get video without watermark
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_filename,
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        # Delete old file if exists
        if os.path.exists(output_filename):
            os.remove(output_filename)
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_filename
    except Exception as e:
        print(f"Error: {e}")
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot is Active! Send me a TikTok link.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "tiktok.com" in url:
        status_msg = bot.reply_to(message, "Downloading... please wait.")
        
        video_file = download_tiktok(url)
        
        if video_file and os.path.exists(video_file):
            with open(video_file, 'rb') as video:
                bot.send_video(message.chat.id, video, caption="Downloaded by @Deb_Shuvo_Tools_bot")
            bot.delete_message(message.chat.id, status_msg.message_id)
            os.remove(video_file) # Delete file after sending to save space
        else:
            bot.edit_message_text("Error: Failed to bypass watermark or download video.", message.chat.id, status_msg.message_id)
    else:
        bot.reply_to(message, "Please send a valid TikTok link.")

print("Bot is running with yt-dlp...")
bot.polling()
