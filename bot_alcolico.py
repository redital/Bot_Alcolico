# -*- coding: iso-8859-15 -*-
from telebot import types
import telebot

from random import randint
from io import BytesIO
from time import sleep

from funzioni import*
from config import API_TOKEN




chiudi_partite()


MESSAGGIO={}
PATH_FILE_ORDINI = "ordini/"


bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    info=[]
    info=open("info_user.txt","r").read()
    file=open("info_user.txt","a")
    body= formattazione(message,first=True,last=True,username=True,id=True)
    if(str(body) not in info):
        file.write(body +"\n")
        file.close()


    bot.send_message( message.chat.id,
"""\
Ciao! Siete pronti a sbronzarvi?\nDigita (o premi su) /new_game per iniziare una nuova partita
Ricordati che in ogni momento puoi digitare (o premere su) /help per conoscere la lista dei comandi e cosa fanno.
Se ti va, lascia un feedback! Digita /feedback seguito dal tuo messaggio per farci sapere cosa ne pensi del bot, segnalare problemi, dare dei consigli su come migliorarlo, suggerire nuovi ordini etc.

N.B. Questo bot � hostato su un server gratuito, pu� capitare che venga staccato per dare priorit� ad altro. Se usando questo bot dovessi vedere che non risponde, contatta @AculeoCrepuscolare
""")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message( message.chat.id,
"""\
Il gioco � semplice, lo capirai subito (se non sei gi� troppo sbronzo/a).
Digita (o premi su) /new_game per iniziare una nuova partita.
Si gioca a turni, al proprio turno il giocatore prende il telefono con cui si sta giocando e digiter�(o premer�) /pesca.
Io dar� un ordine e star� a lui/lei decidere se eseguirlo o bere.
Quando avrete finito digitate (o premete) /kill_game.
Se volete lasciarmi qualche feedback digitate (o tenete premuto) /feedback e scrivete quello che volete dirmi.

Riassumendo i comandi:
/start\t\t\t- inizializza il bot
/help\t\t\t- spiega a cosa serve il bot e mostra la lista dei comandi
/new_game\t\t- inizia una nuova partita
/kill_game\t\t- chiude la partita in corso
/pesca\t\t\t- se una partita � in corso mostra l'ordine che deve eseguire il giocatore corrente
/feedback\t\t- scrivi un messaggio dopo aver digitato questo comando (es: /feedback ci sono pochi ordini) e verr� recapitato al creator

""")

def gen_markup(message):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Pesca", callback_data="Pesca")
    markup.add(item1)
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id,None)

    if call.data == "Pesca":
        body=""
        if ('username' in call.message.json["chat"].keys()):
            body = body + '{username}'.format(username=call.message.json["chat"]["username"])
        else:
            if ('first_name' in call.message.json["chat"].keys()):
                body = '{first} '.format(first= str(call.message.json["chat"]["first_name"].encode("ascii", "replace"))[2:-1])
            if ('last_name' in call.message.json["chat"].keys()):
                body = body + '{last}, '.format(last= str(call.message.json["chat"]["last_name"].encode("ascii", "replace"))[2:-1])
            body = body + ', {id}'.format(id=call.message.json["chat"]["id"])
        #print(MESSAGGIO)


        try:
            pesca(MESSAGGIO[body])
        except:
           bot.send_message(call.message.chat.id, "Oh, ti ho detto che la partita � finita!\nSe vuoi iniziarne un'altra digita (o premi) /new_game")






@bot.message_handler(commands=['new_game'])
def new_game(message):
    global MESSAGGIO
    MESSAGGIO[formattazione(message, username=True)]=message

    lista_ordini=open("base_di_dati_ordini.txt","r",errors='ignore',encoding='utf8').readlines()
    file=open(PATH_FILE_ORDINI + "ordini" + formattazione(message,username=True) + ".txt","w")
    for i in lista_ordini:
        file.write(i)
    file.close


    partite=[]
    for i in open("partite.txt","r",encoding='utf8').readlines():
        partite.append(i.split(" ")[0] + " \t" + i.split("\t")[-1])
        

    file=open("partite.txt","a")
    body=formattazione(message,username=True,data=True)

    check=body.split(" ")[0] + " \tpartita in corso\n"
    if(check not in partite):
        file.write(body+ " \tpartita in corso"+"\n")
        file.close()

        bot.send_message ( message.chat.id,
"""\
Ok, iniziamo!
Decidete un ordine, a turno ogni giocatore ricever� il telefono e pescher� una carta premendo sul pulsante "Pesca" oppure pu� digitare(o premere) /pesca.
Sulla carta star� scritto cosa fare ma sar� lui/lei a decidere se farlo o bere.
Quando avrete finito digitate (o premete) /kill_game
""")

    else:
        file.close()
        bot.send_message(message.chat.id, "Sei ubriaco/a ancor prima di cominciare? Sveglia! Vedi che la partita � gi� in corso!")

@bot.message_handler(commands=['pesca'])
def pesca(message):
    global MESSAGGIO
    MESSAGGIO[formattazione(message, username=True)]=message

    try:
        bot.edit_message_reply_markup(message.chat.id,message.message_id-1)
    except:
        pass

    partite=[]
    for i in open("partite.txt","r").readlines():
        partite.append(i.split(" ")[0] + " \t" + i.split("\t")[-1])

    file=open("partite.txt","a")
    body=formattazione(message,username=True,data=True)
    check=body.split(" ")[0] + " \tpartita in corso\n"
    if(check not in partite):
        bot.send_message(message.chat.id, "Zi...cosa vuoi pescare se non c'è nessuna partita in corso?\nDigitare (o premere) /new_game per iniziarne una")
    else:
        lista_ordini=open(PATH_FILE_ORDINI + "ordini" + formattazione(message,username=True) + ".txt","r").readlines()
        if (lista_ordini==[]):
            lista_ordini=open("base_di_dati_ordini.txt","r").readlines()
        ordine=lista_ordini.pop(randint(0,len(lista_ordini)-1))#.encode('cp1252').decode('utf-8')
        file=open(PATH_FILE_ORDINI + "ordini" + formattazione(message,username=True) + ".txt","w")
        for i in lista_ordini:
            file.write(i)
        file.close()

        bio = BytesIO()
        bio.name = 'image.png'
        genera_carta(ordine).save(bio, 'PNG')
        bio.seek(0)
        bot.send_photo(message.chat.id,photo=bio, reply_markup=gen_markup(message))
        #bot.send_message(message.chat.id, ordine, reply_markup=gen_markup(message))


@bot.message_handler(commands=['kill_game'])
def kill_game(message):

    try:
        bot.edit_message_reply_markup(message.chat.id,message.message_id-1)
    except:
        pass


    trovato=False
    partite=[]
    for i in open("partite.txt","r").readlines():
        if (i.split("\t")[-1]=="partita in corso\n" and i.split(":")[0]==formattazione(message,username=True)):
            trovato=True
            i=i.split("\t")[0]+" \tpartita conclusa\n"
        partite.append(i)

    file=open("partite.txt","w")
    for i in partite:
        file.write(i)
    file.close()

    if(trovato):
        bot.send_message(message.chat.id, "Ok, effettivamente mi sembrate gi� piuttosto sbronzi, chiudiamola qui... Tornatevene a casa che fate schifo!")
    else:
        bot.send_message(message.chat.id, "Sei ubriaco/a ancor prima di cominciare? Sveglia! Vedi che non c'� nessuna partita in corso!")


@bot.message_handler(commands=['feedback'])
def feedback(message):
    if (message.text=="/feedback"):
        bot.send_message(message.chat.id, 'Scrivi qualcosa dopo "/feedback" ')
    else:
        file=open("feedback.txt","a")
        body=formattazione(message,username=True,text=True) + "\n"
        file.write(body)
        file.close()
        bot.send_message(message.chat.id, "Grazie per il feedback zi!")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    body = '{message}\n' \
           '--\n' \
           '{first}, {last}\n' \
           '{username}, {id}'.format(message=message.text, first=message.from_user.first_name,
                                     last=message.from_user.last_name, username=message.from_user.username,
                                     id=message.chat.id)

    bot.reply_to(message, "Oh ma sei gi� sbronzo/a? Sono un bot, che ne so che significa")



try:
    #bot.polling()
    bot.polling(none_stop=True)
except:
    sleep(1)
    bot.polling(none_stop=True)
