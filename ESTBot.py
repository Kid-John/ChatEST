import sqlite3
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, Updater, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

BOT_TOKEN = "7051552531:AAHI4LzZ9OQfDeRZv_eQUgTZ26Vv0oNQ-qY"

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    context.user_data['score'] = 0
    context.user_data['domanda_corrente'] = 0
    context.user_data['domande'] = []
    context.user_data['domande_totali'] = 0
    context.user_data['domande_risposte'] = set() 

    await mostra_categorie(update)

async def mostra_categorie(update: Update) -> None:
    categorie = [
        [InlineKeyboardButton("Penetration Testing", callback_data="category_Penetration Testing")],
        [InlineKeyboardButton("Vulnerability Scanning", callback_data="category_Vulnerability Scanning")],
        [InlineKeyboardButton("Security Code Review", callback_data="category_Security Code Review")],
        [InlineKeyboardButton("Ethical Hacking", callback_data="category_Ethical Hacking")],
        [InlineKeyboardButton("📖Approfondimenti📖", callback_data="more_info")]
    ]
    reply_markup = InlineKeyboardMarkup(categorie)

    if update.message:
        await update.message.reply_text("Benvenuto nel Bot per l'Educazione per il Security Testing!!\nSe ti serve approfondire o verificare le tue conoscenze sul Security Testing, questo è il bot perfetto per TE! \nSeleziona una categoria per iniziare oppure seleziona Approfondimenti per studiare tutte le categorie/tipologie di Security Testing:\n ⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️", reply_markup=reply_markup)
    else:
        await update.callback_query.message.reply_text("Seleziona una categoria per ricominciare e migliorare il tuo punteggio oppure seleziona Approfondimenti per studiare tutte le categorie/metodologie:", reply_markup=reply_markup)
       
async def prendi_domanda(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    data = query.data.split('_', 1)
    if data[0] == "category":
        categoria = data[1]
        context.user_data['categoria'] = categoria
        context.user_data['score'] = 0
        context.user_data['domanda_corrente'] = 0
        context.user_data['domande'] = []
        context.user_data['domande_totali'] = 0
        context.user_data['domande_risposte'] = set() 
        context.user_data['powerup_message_id'] = 0

        conn = sqlite3.connect('domandeQuiz.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM domande WHERE categoria = ? ORDER BY RANDOM() LIMIT 10", (categoria,))
            domande_ids = cursor.fetchall()
            domande_ids = [d[0] for d in domande_ids]

            context.user_data['domande'] = domande_ids
            context.user_data['domande_totali'] = len(domande_ids)



            print(f"Categoria selezionata: {categoria}")
            print(f"ID Domande recuperate: {domande_ids}")

            if context.user_data['domande_totali'] > 0:
                await fai_domanda(update, context)
            else:
                await update.callback_query.message.reply_text("Nessuna domanda disponibile.")
                await mostra_categorie(update)
        except sqlite3.Error as e:
            print(f"Errore durante la query SQL: {e}")
            await query.message.reply_text("Errore durante il recupero delle domande.")
        finally:
            conn.close()
    else: 
        query.answer()

async def fai_domanda(update: Update, context: CallbackContext) -> None:
    if update.message:
        chat_id = update.message.chat_id
    elif update.callback_query:
        chat_id = update.callback_query.message.chat_id

    if update.message:
        if context.user_data['domanda_corrente'] >= context.user_data['domande_totali']:
            await update.message.reply_text(f"Quiz completato! Il tuo punteggio è: {context.user_data['score']} su {context.user_data['domande_totali']}")
            if context.user_data['score'] >= 7:
                meme7 = "https://spinnaker-watches.com/cdn/shop/articles/idiot_box_029_640x550_crop_center.jpg?v=1716955039"
                await context.bot.send_photo(chat_id = chat_id, photo=meme7, caption= "Complimentii!!!")
            
            elif 5 <= context.user_data['score'] <= 6:
                meme6 = "https://acmi-website-media-prod.s3.ap-southeast-2.amazonaws.com/media/images/confused_travolta_original_acmi.original.jpg"
                await context.bot.send_photo(chat_id = chat_id, photo=meme6, caption= "Bravo, ma puoi fare di meglio")

            elif 2<= context.user_data['score'] <= 4:
                meme4 = "https://preview.redd.it/k9fsul2ixgp61.jpg?width=1080&crop=smart&auto=webp&s=f76d2e60cf8fee3f5e2d626e86c30bdbf25afca6"
                await context.bot.send_photo(chat_id = chat_id, photo=meme4, caption= "Ritenta, sarai più fortunato")
            
            else:
                meme1 = "https://i.pinimg.com/originals/5c/73/a6/5c73a60f462c39c04e687194cf94447a.jpg"
                await context.bot.send_photo(chat_id = chat_id, photo=meme1, caption= "Male Male")
            
            await mostra_categorie(update)
            return
    
    else: 
        if context.user_data['domanda_corrente'] >= context.user_data['domande_totali']:
            await update.callback_query.message.reply_text(f"Quiz completato!\n Il tuo punteggio è: {context.user_data['score']} su {context.user_data['domande_totali']}")
            if context.user_data['score'] >= 7:
                meme7 = "https://spinnaker-watches.com/cdn/shop/articles/idiot_box_029_640x550_crop_center.jpg?v=1716955039"
                await context.bot.send_photo(chat_id = chat_id, photo=meme7, caption= "Complimentii!!!")
            
            elif 5 <= context.user_data['score'] <= 6:
                meme6 = "https://acmi-website-media-prod.s3.ap-southeast-2.amazonaws.com/media/images/confused_travolta_original_acmi.original.jpg"
                await context.bot.send_photo(chat_id = chat_id, photo=meme6, caption= "Bravo, ma puoi fare di meglio")

            elif 2<= context.user_data['score'] <= 4:
                meme4 = "https://preview.redd.it/k9fsul2ixgp61.jpg?width=1080&crop=smart&auto=webp&s=f76d2e60cf8fee3f5e2d626e86c30bdbf25afca6"
                await context.bot.send_photo(chat_id = chat_id, photo=meme4, caption= "Ritenta, sarai più fortunato")
            
            else:
                meme1 = "https://i.pinimg.com/originals/5c/73/a6/5c73a60f462c39c04e687194cf94447a.jpg"
                await context.bot.send_photo(chat_id = chat_id, photo=meme1, caption= "Male Male")
            
            await mostra_categorie(update)
            return
            
    id_domanda = context.user_data['domande'][context.user_data['domanda_corrente']]
    
    conn = sqlite3.connect('domandeQuiz.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT domanda, risposta_1, risposta_2, risposta_3, risposta_corretta FROM domande WHERE id = ?", (id_domanda,))
        domanda = cursor.fetchone()

        if domanda:
            domanda_testo = domanda[0]
            risposte = [domanda[1], domanda[2], domanda[3], domanda[4]]
            random.shuffle(risposte)

            testo_powerup = "\n⚡ *Power-up disponibili* ⚡\nUsa un power-up per ottenere un vantaggio! "


            powerup = [
                [InlineKeyboardButton("🔥 2X Punti", callback_data="2x")],
                [InlineKeyboardButton("⏩ SKIP", callback_data="skip")]
            ]

            keyboard = [[InlineKeyboardButton(risposta, callback_data=f"answer_{id_domanda}_{risposta.replace(' ', '_')}")] for risposta in risposte]
            reply_markup_domande = InlineKeyboardMarkup(keyboard)

            reply_markup_powerup = InlineKeyboardMarkup(powerup)

            context.user_data['domanda_corrente'] += 1
            context.user_data['risposta_corretta'] = domanda[4]
            context.user_data['domande_risposte'].add(id_domanda)

            await update.callback_query.message.edit_text(domanda_testo, reply_markup=reply_markup_domande, parse_mode = "Markdown")
    
            if 'powerup_message_id' in context.user_data:
                await context.bot.send_message(chat_id=chat_id, text=testo_powerup, reply_markup=reply_markup_powerup, parse_mode='Markdown')
                del context.user_data['powerup_message_id']
        else:
            await update.callback_query.message.reply_text(f"Domanda con ID {id_domanda} non trovata.")
    except sqlite3.Error as e:
        print(f"Errore durante la query SQL: {e}")
        await update.callback_query.message.reply_text("Errore durante il recupero della domanda.")
    finally:
        conn.close()

async def controllo_risposta(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split('_',2)
    if data[0] == "answer":
        id_domanda = int(data[1])
        risposta_utente = data[2].replace('_', ' ')


        print(f"Ricevuto callback: id_domanda={id_domanda}, risposta_utente={risposta_utente}")

        if context.user_data.get('powerup_2x', False):
            
            if risposta_utente.lower() == context.user_data['risposta_corretta'].lower():
                context.user_data['score'] += 2
                await query.answer("Risposta corretta! Hai ottenuto 2 punti grazie al power-up 2X!")
            else:
                context.user_data['score'] -= 1
                await query.answer("Risposta errata! Hai perso 1 punto!")

            del context.user_data['powerup_2x']
        elif context.user_data.get('powerup_skip', False):
            
            if risposta_utente.lower() == context.user_data['risposta_corretta'].lower():
                context.user_data['score'] += 0
                await query.answer("Domanda Saltata!")
            else:
                context.user_data['score'] -= 0
                await query.answer("Domanda Saltata!")

            del context.user_data['powerup_skip']
        else:
            if risposta_utente.lower() == context.user_data['risposta_corretta'].lower():
                context.user_data['score'] += 1
            else:
                context.user_data['score'] -= 0.25
        
        domanda_corrente = context.user_data.get('domanda_corrente', 0)
        if domanda_corrente % 10 == 0:
            await update.callback_query.message.edit_text("QUIZ COMPLETATO!")
            context.user_data['powerup_2x_used'] = False
            context.user_data['powerup_skip_used'] = False

        await fai_domanda(update, context)
    
    else: 
        query.answer()
 
async def gestione_approfondimenti(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    if query.data == "more_info":
        link_paper = [
            "Penetration Testing: https://ieeexplore.ieee.org/abstract/document/4402456?casa_token=_Epv9hdjo-kAAAAA:umyn0EO10c4LHjY1CLXMZiuI9j6_F8Y6LkogrpqazQfNHiBWvnl6nJ5sAPfougJ0RQRRI2DTJQ",
            "Vulnerability Scanning: https://www.emerald.com/insight/content/doi/10.1108/09685221111173058/full/html?casa_token=YzfPZglToCwAAAAA:w2uweugRupe3OvTCNC7a-bO7hrFP5pW9x21zzn3aFBKwvo7Poji2rjqAxO7NdQVoL68zOKcXOWXir2VN9GKcOrFjvJjTkhaznHQG6O0ZAkdW_7AjWBRx",
            "Security Code Review: https://link.springer.com/chapter/10.1007/978-3-642-36563-8_14",
            "Ethical Hacking: https://ieeexplore.ieee.org/abstract/document/5386933"
        ]
    
    messaggio = "Ecco alcuni link per approfondire le varie tipologie di security testing:\n\n" + "\n".join(link_paper)
        
    await query.message.reply_text(messaggio)

async def gestione_powerup(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    powerup = query.data

    domande_totali = context.user_data.get('domande_totali', 0)
    domanda_corrente = context.user_data.get('domanda_corrente', 0)

    if powerup == "2x":

        if context.user_data.get('powerup_2x_used', False) and domanda_corrente < domande_totali and (domanda_corrente % 10) != 0:
            await query.answer("⚡ Power-up 2X già utilizzato! Può essere utilizzato solo una volta ogni 10 domande.")
        else:
            context.user_data['powerup_2x'] = True
            context.user_data['powerup_2x_used'] = True  
            await query.answer("⚡ Power-up 2X attivato! Le risposte corrette daranno 2 punti, le errate toglieranno 1 punto.")

    elif powerup == "skip":
        
        if context.user_data.get('powerup_skip_used', False) and domanda_corrente < domande_totali and (domanda_corrente % 10) != 0:
            await query.answer("⏩ Power-up SKIP già utilizzato! Può essere utilizzato solo una volta ogni 10 domande.")
        else:
            context.user_data['powerup_skip'] = True
            context.user_data['powerup_skip_used'] = True  
            await query.answer("⏩ Power-up SKIP attivato! Clicca su qualsiasi risposta e questa non toglierà punti.")


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(prendi_domanda, pattern="^category_"))
    application.add_handler(CallbackQueryHandler(controllo_risposta, pattern="^answer_"))
    application.add_handler(CallbackQueryHandler(gestione_approfondimenti, pattern="^more_info"))
    application.add_handler(CallbackQueryHandler(gestione_powerup, pattern="^(2x|skip)$"))

    application.run_polling()

if __name__ == '__main__':
    main()
