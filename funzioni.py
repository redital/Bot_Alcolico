# -*- coding: iso-8859-15 -*-
from PIL import Image, ImageFont, ImageDraw
from telebot import types
import telebot
from datetime import datetime

API_TOKEN = token

bot = telebot.TeleBot(API_TOKEN)

AGGIORNAMENTO=False



def formattazione(message, **opzioni):

    lista=["first","last","username","id","text", "data"]
    for i in lista:
        if (i not in opzioni.keys()):
            opzioni[i]=False

    if (message.from_user.username==None):
        opzioni["first"]=True
        opzioni["last"]=True
        opzioni["id"]=True
        opzioni["username"]=False


    body=""
    if (opzioni["first"]):
        if (message.from_user.first_name!=None):
            body = '{first}'.format(first= str(message.from_user.first_name.encode("ascii", "replace"))[2:-1])
            if (not opzioni["username"] and not message.from_user.last_name==None):
                body = body + ', '
            #else:
                #body = body + ' '

    if (opzioni["last"]):
        if (message.from_user.last_name!=None):
            body = body + '{last}'.format(last= str(message.from_user.last_name.encode("ascii", "replace"))[2:-1])
        if (opzioni["username"]):
            body = body + ', '

    if (opzioni["username"]):
        if (message.from_user.username!=None):
            body = body + '{username}'.format(username=message.from_user.username)
    if (opzioni["id"]):
        body = body + ', {id}'.format(id=message.chat.id)
    if (opzioni["data"]):
        body = body + ': {data}'.format(data=datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))
    if (opzioni["text"]):
        body = body + ': {text}'.format(text=message.text)
    #body=body+"\n"

    return body


def chiudi_partite():
    partite=[]
    for i in open("partite.txt","r").readlines():
        if (i.split(" \t")[-1]== "partita in corso\n"):
            for j in open("info_user.txt","r").readlines():
                if (i.split(":")[0] in j.split(", ")):
                    try:
                        bot.send_message(j.split(", ")[2],"Ho chiuso la tua partita per motivi tecnici",types.ReplyKeyboardRemove())
                        print("ho cambiato " + j.split(", ")[1] + " " + j.split(", ")[2])
                    except:
                        print("ho provato a mandare un messaggio a " + j.split(", ")[1] + " ma non ci sono riuscito")
                    break
                if (i.split(":")[0] == j.replace("\n","")):
                    try:
                        bot.send_message(j.split(", ")[-1],"Ho chiuso la tua partita per motivi tecnici",types.ReplyKeyboardRemove())
                        print("ho cambiato " + j.split(", ")[0] + " " + j.split(", ")[-1].replace("\n",""))
                    except:
                        print("ho provato a mandare un messaggio a " + j.split(", ")[0] + " ma non ci sono riuscito")
                    break
        partite.append(i.split(" \t")[0] + " \tpartita conclusa\n")


    file  = open("partite.txt", "w")
    for i in partite:
        file.write(i)



def genera_carta(text):
    #text=text.encode('cp1252').decode('utf-8')
    size=145
    n_char_riga=26
    if (len(text)<51):
        size=200
        n_char_riga=17
    elif(len(text)<202):
        size=145
        n_char_riga=23
    else:
        size=120
        n_char_riga=28
    #text=text.encode('cp1252').decode('utf-8')
    font = ImageFont.truetype("MADE TOMMY Bold_PERSONAL USE.otf", size)
    img = Image.open("carta_fronte_sf.png")
    draw = ImageDraw.Draw(img)

    i=n_char_riga
    testo=""
    #forti dubbi su i inizializzato in questo modo
    g=len(text)
    while(i<g):
        parole=text.split("\n")[-2].split(" ")
        tmp=""
        for j in parole:
            if(len(tmp+j)<n_char_riga):
                tmp=tmp+j+" "
            else:
                testo=testo+tmp+"\n"
                break
        text=testo + text[len(testo)-1:len(text)]
        #text=text[0:i] + "\n" + text[i:len(text)]
        i=i+len(tmp)
    n_righe=len(text.split("\n"))-1
    centro=int(img.height/2)
    #draw.text((355,centro-121), "----------", (0,0,0), font=font)
    draw.text((320,int(centro-121*((n_righe/2)+1))), text, (0,0,0), font=font)

    #draw.text(posozione angolo in alto a sinistra, testo, colore, font)
    #draw.text((355,700), text, (0,0,0), font=font)
    draw = ImageDraw.Draw(img)
    ratio=0.15
    new_width=int(img.width*ratio)
    new_height=int(img.height*ratio)
    new_size=(new_width,new_height)
    img=img.resize(new_size)
    return img




def manda_mess():
    markup=types.ReplyKeyboardRemove()
    for i in open("info_user.txt","r").readlines():
        messaggio = open("circolare.txt","r").read()#.encode('cp1252').decode('utf-8')
        try:
            bot.send_message(i.split(" ")[-1], "Ciao " + i.split(" ")[0] + "!\n" + messaggio , reply_markup=markup)
        except:
            print("non sono riusciuto a scrivere a " + i)





if(AGGIORNAMENTO):
    manda_mess()

