from twitchio.channel import Channel
from twitchio.ext import commands;
import asyncio
from twitchio.user import User
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent
from TikTokLive.client.logger import LogLevel
import requests
import config
import httpx
#TODO: Make it so the first 4 people in queue are considered to be playing, then make it dynamically adjustable via a command
debug = True

# Create the twitch client
channel_list = ['hubalubalu', 'parknich']
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


async def update_queue_list():
    # Send a POST request with the current queueList as a JSON array to the specified endpoint
    endpoint = 'http://127.0.0.1:80/dash/obs/queue'
    payload = {'users': queueList}
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
        
        
queueList = list()
usersList = list()
      

# Create the client
tiktokClient: TikTokLiveClient = TikTokLiveClient(unique_id="@hubalubalu") 
print(f'[TikTok] Created the tiktok client')

# Listen to an event with a decorator!
@tiktokClient.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"[TikTok] Connected to @{event.unique_id} (Room ID: {tiktokClient.room_id})")


@tiktokClient.on(CommentEvent)
async def on_comment(event: CommentEvent) -> None:
    print(f"[TikTok] {event.user.nickname}: {event.comment}")
    if event.comment == "?queue join":
        queueList.append(event.user.nickname)
        await update_queue_list()
    if event.comment == "?queue leave":
        queueList.pop(queueList.index(f'{event.user.nickname}'))
        await update_queue_list()

async def check_loop():
    ## Prep
    
    # [TikTok] Enable download info
    print(f'[TikTok] Enabling download info')
    tiktokClient.logger.setLevel(LogLevel.INFO.value)
    print(f'[TikTok] Enabled download info')

    # [TikTok] Set the login session ID token BEFORE connecting
    print(f'[TikTok] Setting login session ID')
    tiktokClient.web.set_session_id(config.session_id)
    print(f'[TikTok] Set login session ID')

    print(f'[TikTok] Connecting...')
    a = False
    connected = False
    # Run 24/7
    while True:
        try:
            # Check if they're live
            while not await tiktokClient.is_live():
                tiktokClient.logger.info("Client is currently not live. Checking again in 60 seconds.")
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
            
            

        # Connect once they become live
        tiktok_is_live = True
        
        if not connected:
            tiktokClient.logger.info("Requested client is live!, connecting")
            try:
                await tiktokClient.start()
                connected = True
            except Exception:
                print('Failed to connect to TikTokLive')
                connected = False
                return
        else:
            connected = True
        await asyncio.sleep(60)
        


async def main():
    class Bot(commands.Bot):
        def __init__(self):
            # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
            # prefix can be a callable, which returns a list of strings or a string...
            # initial_channels can also be a callable which returns a list of strings...
            super().__init__(
                token=config.access_token, prefix="?", initial_channels=channel_list
            )

        async def event_ready(self):
            # Notify us when everything is ready!
            # We are logged in and ready to chat and use commands...
            print(f"Logged in as | {self.nick}")
            print(f"User id is | {self.user_id}")
            channel = TwitchBot.get_channel('Hubalubalu')
            
            for channel in channel_list:
                c = TwitchBot.get_channel(channel)
                await c.send(f'parknbot v0.5DEV connected to {c}!')
            print('parknBot v0.5Dev loaded')
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
            fullmessage = '[in "{channel}"] ({timestamp}) {user}: {message}'
            fullmessageformatted=fullmessage.format(channel=channel, timestamp=messagetime, user=author, message=content)
            # Print the contents of our message to console and chatlog.txt...
            log(fullmessageformatted)

            
            


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
            if args[0] == f"list":
                message = str()
                
                if not queueList:
                    await ctx.send("The queue is currently empty.")

                for index, user in enumerate(queueList, start=1):
                    message += f" {index}. @{user}\n"

                await ctx.send(f'{len(queueList)} users currently in queue:\n{message}')
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
                        removed_user = queueList.pop(0)
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
                    if queueList:
                        for user in queueList:
                            queueList.pop(0)
                            
                        await ctx.send(f'Cleared queue')
                        await update_queue_list()  # Call the function to update the queueList
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
                
                
                

    TwitchBot = Bot()
    
    ## Init

    await asyncio.gather(TwitchBot.start(), check_loop())
asyncio.run(main())
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.


