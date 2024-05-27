import discord
from discord.ext import commands
from dotenv import load_dotenv
import google.generativeai as genai
import os
import json
import time
import pickle
import pymupdf
import textwrap
import PIL

class AIcog(commands.Cog):
    #Fist comit
    def __init__(self,client):
        # Token
        load_dotenv()
        genai.configure(api_key=os.getenv('GOOGLE_AI_TOKEN'))
        self.historychat = {}
        self.model = model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        self.client = client
        load_dotenv()
        self.SysMaster = os.getenv('MASTER_USER')

    def loadhystory(self,ctx):
        history = []
        filename = "chat_" + self.usercode(ctx) + ".hist"
        if os.path.exists(".\\AiChats\\"+filename):
            with open(".\\AiChats\\"+filename, "rb") as f:
                history = pickle.load(f)
        return history


    async def savehistory(self,ctx):
        filename = "chat_" + self.usercode(ctx) + ".hist"
        with open(".\\AiChats\\" + filename, 'wb') as file_pi:
            pickle.dump(self.historychat[self.usercode(ctx)].history, file_pi)





    async def messagedebug(self,ctx):
        print (f'{ctx.message.author.name} {ctx.message.author.id} : "{ctx.message.content}"')

    def usercode(self,ctx) ->str:
        return str(ctx.channel.id)


    @commands.command(help = "Start a chat, .aichat your request or response")
    async def aichat(self,ctx):

        await self.messagedebug(ctx)
        usc = self.usercode(ctx)
        originalmessage = ctx.message.content.replace(".aichat", "")

        your_file = ""
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                await attachment.save(attachment.filename)
                if ".pdf" in attachment.filename:
                    #if pdf code here

                    doc = pymupdf.open(attachment.filename)
                    your_file = []
                    userpdfimagefolder = './pdfimages' + usc + '/'
                    if not os.path.exists(userpdfimagefolder):
                        os.makedirs(userpdfimagefolder)
                    texts = []
                    files = []

                    for page in doc:
                        text = page.get_text()
                        texts.append(text)
                        pix = page.get_pixmap()  # render page to an image
                        img = userpdfimagefolder + '.page-' + str(page.number)+ '.png'
                        pix.save(img)
                        image = genai.upload_file(path= img)
                        while image.state.name == "PROCESSING":
                            print('Waiting for video to be processed.')
                            await ctx.send(f"{image.name}: Uploading file, please wait")
                            time.sleep(10)
                            image = genai.get_file(image.name)
                        files.append(image)
                        #your_file.append(f'## Page {page.number} ##')
                        #your_file.append(text)


                    your_file = [originalmessage]
                    for page, (text, image) in enumerate(zip(texts, files)):
                        your_file.append(f'## Page {page} ##')
                        your_file.append(text)
                        your_file.append(image)



                else:
                    your_file = genai.upload_file(path=attachment.filename)
                    while your_file.state.name == "PROCESSING":
                        print('Waiting for video to be processed.')
                        await ctx.send(f"{your_file.name}: Uploading file, please wait")
                        time.sleep(10)
                        your_file = genai.get_file(your_file.name)


        if not (usc in self.historychat.keys()):
            h = self.loadhystory(ctx)
            self.historychat[usc] = self.model.start_chat(history=h)


        response = self.historychat[usc].send_message(your_file)
        await self.savehistory(ctx)



        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                if ".pdf" in attachment.filename:
                    doc.close()
                    files = os.listdir(userpdfimagefolder)
                    for file in files:
                        file_path = os.path.join(userpdfimagefolder, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                os.remove(attachment.filename)



        senttext = response.text

        lines = textwrap.wrap(senttext, 1000, break_long_words=False)
        for txt in lines:
            await ctx.send(txt)



    @commands.command(help = 'clear your chat history')
    async def aichatclear(self, ctx):
        await self.messagedebug(ctx)
        usc = self.usercode(ctx)
        self.historychat[usc] = self.model.start_chat(history=[])
        filename = "chat_" + usc + ".hist"
        if os.path.exists(".\\AiChats\\"+filename):
            os.remove(os.path.join("./AiChats/", filename))

        await ctx.send('Chat cleared!')


    @commands.command(help = 'show your chat history')
    async def myhistory(self, ctx):
        await self.messagedebug(ctx)
        usc = self.usercode(ctx)
        if not (usc in self.historychat.keys()):
            h = self.loadhystory(ctx)
            self.historychat[usc] = self.model.start_chat(history=h)
        lines = textwrap.wrap(str(self.historychat[usc].history), 1000, break_long_words=False)
        for txt in lines:
            await ctx.send(txt)


    @commands.command(help = 'Show all bot users!')
    async def getallusers(self, ctx):

        if self.SysMaster == str(ctx.message.author.id):
            await self.messagedebug(ctx)
            for k in self.historychat.keys():
                await ctx.send(k)

async def setup(client):
    await client.add_cog(AIcog(client))