from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from secret import key #serve a collegare il chatbot a telegram
import json

def load_restaurants():
    with open('chatbot1/dati.json', 'r') as file:
        data = json.load(file)
    
    restaurants = [
        {
            'name': restaurant['name'],
            'latitude': float(restaurant['lat']),
            'longitude': float(restaurant['lon'])
        }
        for restaurant in data
    ]
    
    return restaurants

def find_nearest_restaurant(user_lat, user_lon):
    restaurants = load_restaurants()
    
    def distance(lat1, lon1, lat2, lon2):
        return ((lat2 - lat1)**2 + (lon2 - lon1)**2)**0.5
    
    nearest = min(restaurants, key=lambda r: distance(user_lat, user_lon, r['latitude'], r['longitude']))
    return nearest

async def hello(update, context):
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def echo(update, context):
    await update.message.reply_text(update.message.text)

async def photo_handler(update, context):
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive("chatbot/img/user_photo.jpg")
    #await update.message.reply_text(f'photo received {user}')
    chat_id = update.message.chat.id
    await context.bot.send_document(chat_id=chat_id, document=open('chatbot/img/user_photo.jpg', 'rb'))

async def process_location(update, context):
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message
    user_location = message.location

    user = message.from_user
    print(f"You talk with user {user['first_name']} and his user ID: {user['id']}")
    msg = f'Ti trovi presso lat={user_location.latitude}&lon={user_location.longitude}'
    r = find_nearest_restaurant(user_location.latitude, user_location.longitude)
    if r:
        msg += f'\nIl ristorante più vicino è {r["name"]} alla latitudine {r["latitude"]} e longitudine {r["longitude"]}'
    await message.reply_text(msg)

print('starting')

app = ApplicationBuilder().token(key).build()
app.add_handler(CommandHandler("hello", hello))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
app.add_handler(MessageHandler(filters.LOCATION, process_location))
app.run_polling()