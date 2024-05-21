import discord
from discord.ext import commands
from dotenv import load_dotenv
import google.generativeai as genai
import os
import json
import time
class AIcog(commands.Cog):
    def __init__(self,client):
        # Token
        load_dotenv()
        genai.configure(api_key=os.getenv('GOOGLE_AI_TOKEN'))
        self.historychat = {}
        self.model = model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        self.client = client

    async def messagedebug(self,ctx):
        print (f'{ctx.message.author.name} {ctx.message.author.id} : "{ctx.message.content}"')

    def usercode(self,ctx) ->str:
        return str(ctx.message.author.name) + '_' + str(ctx.message.author.id)

    @commands.command(help="Do some prefixed things \n Transcribe audios \n Describe Images \n Describe Figures")
    async def googleai(self,ctx):
        await self.messagedebug(ctx)
        #model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        text = ctx.message.content.replace(".googleai", "")

        if len(ctx.message.attachments) > 0:
            # response
            await ctx.send('Analisando arquivo...')
            #abrir json de config
            jsonprompt = open('cogs\\AiConf.json')
            super = json.load(jsonprompt)

            #verificando o tipo de arquivo
            for attachment in ctx.message.attachments:
                for type in super.keys():
                    for format in super[type]['FileFormats']:
                        if format in attachment.filename:
                            filetype = type

                await attachment.save(attachment.filename)
                your_file = genai.upload_file(path=attachment.filename)
                while your_file.state.name == "PROCESSING":
                    print('Waiting for video to be processed.')
                    await ctx.send(f"{your_file.name}: Uploading file, please wait")
                    time.sleep(10)
                    your_file = genai.get_file(your_file.name)

                if text == "":
                    prompt = super[filetype]['Prompt']
                else:
                    prompt = text

                response = self.model.generate_content([prompt, your_file], safety_settings={'SEXUAL': 'BLOCK_NONE'})
                await ctx.send("Google AI " + attachment.filename + " : " + str(response.text))
                os.remove(attachment.filename)

        else:
            if text != "":
                response = self.model.generate_content(text)
                await ctx.send("Google AI " + str(response.text))
            else:
                await ctx.send('no Understand')

    @commands.command(help = "Start a chat, .aichat your request or response")
    async def aichat(self,ctx):

        await self.messagedebug(ctx)
        usc = self.usercode(ctx)
        text = ctx.message.content.replace(".aichat", "")

        your_file = ""
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                await attachment.save(attachment.filename)
                your_file = genai.upload_file(path=attachment.filename)
                while your_file.state.name == "PROCESSING":
                    print('Waiting for video to be processed.')
                    await ctx.send(f"{your_file.name}: Uploading file, please wait")
                    time.sleep(10)
                    your_file = genai.get_file(your_file.name)

        if not (usc in self.historychat.keys()):
            self.historychat[usc] = self.model.start_chat(history=[])

        response = self.historychat[usc].send_message([text, your_file])

        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                os.remove(attachment.filename)

        await ctx.send(str(response.text))

    @commands.command(help = 'clear your chat history')
    async def aichatclear(self, ctx):
        await self.messagedebug(ctx)
        usc = self.usercode(ctx)
        self.historychat[usc] = self.model.start_chat(history=[])
        await ctx.send('Chat cleared!')


    @commands.command(help = 'show your chat history')
    async def myhistory(self, ctx):
        await self.messagedebug(ctx)
        usc = self.usercode(ctx)
        await ctx.send(self.historychat[usc].history)

    @commands.command(help = 'Show all bot users!')
    async def getallusers(self, ctx):
        if '284146826196549633' == str(ctx.message.author.id):
            await self.messagedebug(ctx)
            for k in self.historychat.keys():
                await ctx.send(k)

async def setup(client):
    await client.add_cog(AIcog(client))