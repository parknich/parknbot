import twitchio
from twitchio.channel import Channel
from twitchio.ext import commands, eventsub;
import asyncio
from twitchio.user import User
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, SocialEvent, DisconnectEvent, JoinEvent, LiveEndEvent
from TikTokLive.client.logger import LogLevel
import requests
import lib.config as config
import httpx
import logging
import websockets
import json
import random
import discord
global connected
global message_sent
#TODO: replace flask with quart
# use aiohttp
debug = True
global chat
chat = list()
# Create the twitch client
channel_list = ['hubalubalu', 'parknich']

#esbot = commands.Bot.from_client_credentials(client_id=config.clientid,
#                                         client_secret=config.clientsecret)
#esclient = eventsub.EventSubClient(esbot,
#                                   webhook_secret=config.webhookSecret,
#                                   callback_route='https://parknbot.xyz/twitch-callback')


def iterateFile(file):
    f = open(file, "r")
    for line in f:
        print(line,)


def convertTuple(convertinput):
    output = ''
    char = ''
    for char in convertinput:
        output += char + ' '
    return output
def splitArgs(input_string):
    words = input_string.split()
    if words:
        return words
    else:
        return None  # Handle the case where the string is empty

user_colors = {}
color_codes = {
    "red": "FF0000",
    "blue": "0000FF",
    "green": "008000",
    "firebrick": "B22222",
    "coral": "FF7F50",
    "yellow_green": "9ACD32",
    "orange_red": "FF4500",
    "sea_green": "2E8B57",
    "goldenrod": "DAA520",
    "chocolate": "D2691E",
    "cadet_blue": "5F9EA0",
    "dodger_blue": "1E90FF",
    "hot_pink": "FF69B4",
    "blue_violet": "8A2BE2",
    "spring_green": "00FF7F"
}

async def update_chat(user, content, platform, color='', badges=dict()):
    global chat
    badgesIdentifierList = {
        "moderator": "modBadgeIdent",
        "subscriber": "subBadgeIdent",
        "glhf-pledge": "glhfBadgeIdent",
        "vip": "vipBadgeIdent",
        "tiktokFriend": "tiktokFriendBadgeIdent",
        "tiktokModerator": "tiktokModBadgeIdent"
    }    
    
    # Check if user already has a saved color or if color is provided by Twitch API
    if user not in user_colors and not color:
        # Assign a random color to the user
        user_colors[user] = random.choice(list(color_codes.values()))
    
    # Format the message with the user's color
    if color:
        msg = f'{color} [{platform}] {user}: {content}'
    else:
        msg = f'#{user_colors[user]} [{platform}] {user}: {content}'
    
    # Add badge information if available
    if badges:
        for key in badges:
            if key in badgesIdentifierList:
                if key == 'subscriber':
                    badgesIdentifierList[key] = f'{badgesIdentifierList[key]}{badges[key]}'
                msg = f'{badgesIdentifierList[key]} {msg}'
    
    chat.append(msg)
    
    # Limit chat history to 10 messages
    if len(chat) > 10:
        chat = chat[1:]
    
    # Print chat messages to console
    for message in chat:
        print(message)
    
    # Send chat message to server
    endpoint = 'https://parknbot.xyz:443/dash/obs/chat'
    payload = {'chat': chat, 'auth': config.access_token}
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        if debug:
            print('Sent chat message to server')
    except requests.exceptions.RequestException as e:
        print(f'Failed to send chat message to server: {e}')

async def update_queue_list():
    # Send a POST request with the current queueList as a JSON array to the specified endpoint
    global userSlots
    endpoint = 'https://parknbot.xyz:443/dash/obs/queue'
    payload = {'users': queueList, 'userSlots': userSlots}
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        print(f'{[payload]}')
        print(f"QueueList updated successfully: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to update QueueList: {e}")
## WIP
## TODO: Use JSON format
# def savecommand(tupargs, file='savedcommands.info'):
#    command, permission, result = tupargs
#    print(tupargs)
#    print(command)
#    print(permission)
#    with open(file, 'a') as of:
#        of.write('{' + '\n' + 'command: ' + command + '\n' + 'permission: ' + permission + '\n' + 'result: ' + result + '\n' + '}')

def log(input, log_file='chat.log'):
    print(input)
    with open(log_file, 'a') as of:
        of.write(input + '\n')
        
        
#async def connect_to_server():
#    uri = "ws://localhost:8765"
#    async with websockets.connect(uri) as websocket:
#        while True:
#            message = await websocket.recv()
#            print(f"Received message from server: {message}")
        
        
queueList = list()
usersList = list()
global userSlots
userSlots = int()
userSlots = 3



async def main():
    class DiscordBot():
        class discordClient(discord.Client):
            async def on_ready(self):
                print(f'[DiscordBot] Logged on as {self.user}!')
        intents = discord.Intents.default()
        intents.message_content = True
        client = discordClient(intents=intents)
                
        async def sendTikTokLink(self):
            await self.client.wait_until_ready()
            channel = self.client.get_channel(699715620320706614)  
            while not self.client.is_closed():
                await channel.send('Hey, <@&1222663608559861831> Hubalubalu is live on tiktok: https://www.tiktok.com/@hubalubalu/live')
        async def sendTwitchLink(self):
            await self.client.wait_until_ready()
            channel = self.client.get_channel(699715620320706614)  
            while not self.client.is_closed():
                await channel.send('Hey, <@&1222663580969599056> Hubalubalu is live on twitch: https://twitch.tv/hubalubalu')

                
              

        


    class TikTokBot():
        # Create the client
        tiktokClient: TikTokLiveClient = TikTokLiveClient(unique_id="@hubalubalu") 
        print(f'[TikTok] Created the tiktok client')

        # Listen to an event with a decorator!
        @tiktokClient.on(ConnectEvent)
        async def on_connect(event: ConnectEvent):
            message = '[TikTok] Connected to @{event.unique_id} (Room ID: {tiktokClient.room_id})'
            print(message)
            log(message)

        @tiktokClient.on(CommentEvent)
        async def on_comment(event: CommentEvent) -> None:
            print(f"[TikTok] {event.user.nickname}: {event.comment}")
            if event.comment == "?queue join":
                queueList.append(event.user.nickname)
                await update_queue_list()
            if event.comment == "?queue leave":
                queueList.pop(queueList.index(f'{event.user.nickname}'))
                await update_queue_list()
            #Logging
            channel = 'Hubalubalu'
            user = event.user.nickname
            message = event.comment
            
            fulltiktokmessage = '[in "{channel}"] {user}: {message}'
            log(fulltiktokmessage)
            if (event.user.is_moderator) and (event.user.is_friend):
                await update_chat(user, message, 'tiktokIdent', badges=['vip', 'moderator'])
            elif (event.user.is_moderator) and (event.user.is_friend == False):
                await update_chat(user, message, 'tiktokIdent', badges=['moderator'])
            elif (event.user.is_moderator==False) and (event.user.is_friend==True):
                await update_chat(user, message, 'tiktokIdent', badges=['vip'])
            elif (event.user.is_moderator==False) and (event.user.is_friend == False):
                await update_chat(user, message, 'tiktokIdent')
            chan = twitchBot.get_channel("hubalubalu")
            loop = asyncio.get_event_loop()
            loop.create_task(chan.send(f'[TikTok] {user}: {message}'))

        @tiktokClient.on(DisconnectEvent)
        async def on_disconnect_event(event: DisconnectEvent):
            global connected
            connected=False

        @tiktokClient.on(LiveEndEvent)
        async def on_live_end_event(event: LiveEndEvent):
            global message_sent
            global connected
            message_sent=False
            connected=False
        #@tiktokClient.on(SocialEvent)
        #async def on_social_event(event: SocialEvent):
        #    event.user.
            

        #@tiktokClient.on(DisconnectEvent)
        #async def on_disconnect(event: DisconnectEvent):
        #    


        async def check_loop(self):
            ## Prep
            global connected
            # [TikTok] Enable download info
            print(f'[TikTok] Enabling download info')
            self.tiktokClient.logger.setLevel(LogLevel.INFO.value)
            print(f'[TikTok] Enabled download info')

            # [TikTok] Set the login session ID token BEFORE connecting
            print(f'[TikTok] Setting login session ID')
            self.tiktokClient.web.set_session_id(config.session_id)
            print(f'[TikTok] Set login session ID')
            
            print(f'[TikTok] Connecting...')
            a = False
            connected = False
            # Run 24/7
            while True:
                try:
                    # Check if they're live
                    while not await self.tiktokClient.is_live():
                        self.tiktokClient.logger.info("Client is currently not live. Checking again in 60 seconds.")
                        tiktok_is_live=False
                        connected=False
                        await asyncio.sleep(60)  # Spamming the endpoint will get you blocked
                except httpx.HTTPError as e:
                    # Handle HTTP errors
                    print(f"HTTP error occurred: {e}")
                except httpx.Request as e:
                    # Handle request-related errors (e.g., network issues)
                    print(f"Request error occurred: {e}")
                except httpx.Timeout as e:
                    # Handle timeout errors
                    print(f"Request timeout occurred: {e}")
                except Exception as e:
                    # Catch any other exceptions
                    print(f"An unexpected error occurred: {e}")
                    
                global message_sent
                
                # Connect once they become live
                tiktok_is_live = True
                message_sent = True
                if not message_sent:
                    await DiscordBot.sendTikTokLink(DiscordBot)
                while not connected:
                    self.tiktokClient.logger.info("Requested client is live!, connecting")
                    try:
                        await self.tiktokClient.start()
                        print('started tiktok client')
                        connected = True
                        return
                    except Exception as e:
                        print(f'Failed to connect to TikTokLive: {str(e)}')
                        connected = False
                        await asyncio.sleep(10)
                        return
                
                await asyncio.sleep(60)
        

    class Bot(commands.Bot):
        def __init__(self):
            # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
            # prefix can be a callable, which returns a list of strings or a string...
            # initial_channels can also be a callable which returns a list of strings...
            super().__init__(
                token=config.access_token, prefix="?", initial_channels=channel_list
            )

                
        async def __ainit__(self) -> None:
            self.loop.create_task(esclient.listen(port=4000))
#twitchio.ext.eventsub.event_eventsub_notification_stream_start(event: StreamOnlineData)
            try:
                await esclient.subscribe_channel_stream_start(103187740)
            except twitchio.HTTPException:
                pass

        
        async def event_ready(self):
            # Notify us when everything is ready!
            # We are logged in and ready to chat and use commands...
            print(f"Logged in as | {self.nick}")
            print(f"User id is | {self.user_id}")
            channel = twitchBot.get_channel('Hubalubalu')
            for channel in channel_list:
                c = twitchBot.get_channel(channel)
                await c.send(f'parknbot v0.7DEV connected to {c}!')
            print('parknBot v0.7Dev loaded')
        async def event_channel_join_failure(self, channel: str):
            return await super().event_channel_join_failure(channel)
        async def event_join(self, channel: Channel, user: User):
            usersList.append(channel)
            return await super().event_join(channel, user)
        
        async def event_message(self, message):
            # logging bot messages or some shit idfk...
            fullbotmessage = '[ECHO] [in "{channel}"] ({timestamp}) {user}: {message}'
            fullbotmessageformatted=fullbotmessage.format(channel=message.channel.name, timestamp=message.timestamp, user='parknbot', message=message.content)
            if message.echo:
                log(fullbotmessageformatted)
                return
            # define shit
            author = message.author.name
            content = message.content
            messagetime = message.timestamp
            channel = message.channel.name
            badges = message.author.badges
            color = message.author.color
            fullmessage = '[in "{channel}"] ({timestamp}) {user}: {message}'
            fullmessageformatted=fullmessage.format(channel=channel, timestamp=messagetime, user=author, message=content)
            # Print the contents of our message to console and chatlog.txt...
            log(fullmessageformatted)
            await update_chat(author, content, 'twitchIdent', color, badges, )

            # Since we have commands and are overriding the default `event_message`
            # We must let the bot know we want to handle and invoke our commands...
            await self.handle_commands(message)
        
        @commands.command()
        async def hello(self, ctx: commands.Context):
            await ctx.send(f'Hello {ctx.author.name}!')
        @commands.command()
        async def ping(self, ctx: commands.Context):
            await ctx.send(f'pong')
        @commands.command()
        async def about(self, ctx: commands.Context):
            await ctx.send(f'parknbot is a custom coded bot for the Hubalubalu channel on twitch! :D (By parknich)')
        @commands.command()
        async def discord(self, ctx: commands.Context):
            await ctx.send (f'Discord: https://discord.gg/JYUzZjmZq5')
        @commands.command()
        async def filesay(self, ctx: commands.Context, args):
            if ctx.author.display_name == 'parknich':
                try: 
                    f = open(args, 'r')
                    for line in f:
                        await ctx.send(line)
                except FileNotFoundError:
                    await ctx.send(f"Error: No such file: '{args}'")
        @commands.command()
        async def printUsersListToConsole(self, ctx: commands.Context):
            for user in usersList:
                print(user)
            await ctx.send(f'Printed to console')
        @commands.command()
        async def queue(self, ctx: commands.Context, *args):
            in_game_users = list() # First 4 users are considered in-game
            queue_users = list()  # Remaining users are in the queue
            global userSlots
            
            in_game_users = queueList[:int(userSlots)]  # First 4 users are considered in-game
            queue_users = queueList[int(userSlots):]    # Remaining users are in the queue
            
            if args[0] == "list":
                in_game_users = queueList[:int(userSlots)]  # First 4 users are considered in-game
                queue_users = queueList[int(userSlots):]    # Remaining users are in the queue
                print(userSlots)
                for user in in_game_users:
                    print(user)
                for user in queue_users:
                    print(user)
                in_game_message = "\n".join([f"  {index}. @{user} (In-Game)" for index, user in enumerate(in_game_users, start=1)])
                queue_message = "\n".join([f"  {index}. @{user}" for index, user in enumerate(queue_users, start=len(in_game_users) + 1)])
                
                if in_game_message:
                    await ctx.send(f"In-Game ({len(in_game_users)}): \n{in_game_message}")
                
                if queue_message:
                    await ctx.send(f"In Queue ({len(queue_users)}): \n{queue_message}")
                
                if not in_game_message and not queue_message:
                    await ctx.send("No users in queue.")
            elif args[0] == "test":
                print(userSlots)
            elif args[0] == f"set":
                try:
                    if args[1] == f"userSlots":
                        print(args[2])
                        print(userSlots)
                        userSlots = args[2]
                        await ctx.send('Set userSlots')
                        print(userSlots)
                except Exception as e:
                    print('Unable to set anything')
                    await ctx.send('Invalid arguments:' + e)
            elif args[0] == f"join":
                if ctx.author.display_name not in queueList:
                    try:
                        queueList.append(ctx.author.display_name)
                        await ctx.send(f"@{ctx.author.display_name}, you've been added to the queue!")
                        await update_queue_list()  # Call the function to update the queueList
                    except Exception:
                        await ctx.send(f'Unknown error')
                else:
                    await ctx.send(f'Error 4: @{ctx.author.display_name} already in queue list')
            elif args[0] == f'next':
                if ctx.author.is_mod or ctx.author.is_broadcaster:
                    if queueList:
                        removed_user = queueList.pop(userSlots+1)
                        await update_queue_list()  # Call the function to update the queueList
                    else:
                        await ctx.send(f'The queue is empty.')
                        return
                    if not queueList:
                        if debug:
                            print(f'[DEBUG] Removed {removed_user} from the queue and the queue is now empty')
                        await ctx.send(f'@{removed_user} is done playing and the queue is now empty.')
                    else:
                        next_user = queueList[0]
                        if debug:
                            print(f'[DEBUG] Removed {removed_user} from the queue and added {next_user} to the top')
                        await ctx.send(f'@{removed_user} is done playing and, the next user to play is @{next_user}, go ahead and add them to the party!')
                else:
                    await ctx.send("Error 3: Insufficient permissions")
            elif args[0] == f'remove':
                if ctx.author.is_mod or ctx.author.is_broadcaster:
                    if queueList:
                        if args[1] in queueList:
                            await ctx.send('Removed ' + args[1] + ' from queue')
                            queueList.pop(queueList.index(f'{args[1]}'))
                            await update_queue_list()  # Call the function to update the queueList
                        else:
                            await ctx.send(f'The specified user is not in the queue')
                            return
                    else:
                        await ctx.send(f'The queue is empty.')
                        return
                else:
                    await ctx.send("Error 3: Insufficient permissions")
            elif args[0] == f'leave':
                if queueList:
                    if ctx.author.display_name in queueList:
                        await ctx.send('Removed ' + ctx.author.display_name + ' from queue')
                        queueList.pop(queueList.index(f'{ctx.author.display_name}'))
                        await update_queue_list()  # Call the function to update the queueList
                    else:
                        await ctx.send(f'The specified user is not in the queue')
                        return
                else:
                    await ctx.send(f'The queue is empty.')
                    return
            elif args[0] == f'add':
                try:
                    if ctx.author.is_mod or ctx.author.is_broadcaster:
                            if args[1] in queueList:
                                await ctx.send(f'The user is already in the queue')
                                return
                            else:
                                queueList.append(args[1])
                                await update_queue_list()  # Call the function to update the queueList
                                await ctx.send(f'Added {args[1]} to the queue')
                    else:
                        await ctx.send("Error 3: Insufficient permissions")
                except IndexError:
                    await ctx.send(f'Error 2: Missing argument')
            elif args[0] == f'clear':
                if ctx.author.is_mod or ctx.author.is_broadcaster:
                    usersCleared = bool()
                    if queueList:
                        while not usersCleared:
                            for user in queueList:
                                queueList.pop(0)
                                if not queueList:
                                    usersCleared = True
                                    
                                asyncio.sleep(0.050)
                                
                        await ctx.send(f'Cleared queue')
                        await update_queue_list()  # Call the function to update the queueList
                    else:
                        await ctx.send(f'Queue already empty')
                else:
                    await ctx.send("Error 3: Insufficient permissions")
            else:
                await ctx.send(f'Error 2: Missing argument')
            
        @commands.command()
        async def help(self, ctx: commands.Context, *args):
            if args[0] == f'queue' and not args[1] :
                await ctx.send(f'Available subcommands for "queue": list, join, next')
            elif args[0] == f'queue' and args[1] == 'list':
                await ctx.send(f"queue list: Lists users in queue and their current position (Permission: User+)")
            elif args[0] == f'queue' and args[1] == 'next':
                await ctx.send (f'queue next: Advances to the next user in the queue (Permission: Moderator+)')
            elif args[0] == f'queue' and args[1] == 'join':
                await ctx.send(f'queue join: Joins the queue (Permission: User+)')
        #@commands.command()
        #async def debug(self, ctx: commands.Context, *args):
        #    if args[0] == 'print':
        #        try:
        #            print(globals()[args[1]])
        #            await ctx.send(globals()[args[1]])
        #        except Exception as e:
        #            try:
        #                print(locals()[args[1]])
        #                await ctx.send(locals()[args[1]])
        #            except Exception as e2:
        #                await ctx.send(f'Failed to print: ' + e2)
                
                
                

    
    
    twitchBot = Bot()
    discordBot = DiscordBot()
    #await twitchBot.__ainit__()
    #
    #@esbot.event()
    #async def event_eventsub_notification_stream_start(payload: eventsub.StreamOnlineData) -> None:
    #    print('Twitch Stream Started')
    #    channel = twitchBot.get_channel('hubalubalu')
    #    await channel.send(f'Hubalubalu is now streaming')
    #    await DiscordBot.sendTwitchLink()
    
    ## Init

    await asyncio.gather(twitchBot.start(), TikTokBot.check_loop(TikTokBot), discordBot.client.start(config.discordToken))
asyncio.run(main())
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.


