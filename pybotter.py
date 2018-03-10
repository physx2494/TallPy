import discord, recentparser, asyncio, re, shelve

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def my_background_task(self):
        await self.wait_until_ready()
        counter = 0
        channel = self.get_channel("420247657936584715") # channel ID goes here
        while True:
            updated = recentparser.main_loop()
            #print(updated)
            if len(updated) > 0:
                for thread in updated:
                    url = recentparser.convert_to_url(thread)
                    #print('about to open shelf')
                    with shelve.open('threads') as lookup:
                        _list = []
                        #print('shelf open and list value is {}'.format(_list))
                        #print(thread)
                        #print(url)
                        #print(lookup.keys())
                        await client.send_message(channel, '{}'.format(url))
                        if url in lookup.keys():
                            #print('found thread in lookup keys')
                            for value in lookup[url]:
                                #print('value is {}'.format(value))
                                await client.send_message(channel, '{}'.format(value))
            #print('sleep 60')
            await asyncio.sleep(60) # task runs every 60 seconds


client = MyClient()
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if bool(re.match('!notify', message.content, re.I)):
        user = str(message.author.mention)
        threadraw = re.search("\d\d+", message.content).group()
        thread = recentparser.convert_to_url(threadraw)
        with shelve.open('threads') as lookup:
            #print(thread)
            #print(lookup.keys())
            if thread not in lookup.keys():
                lookup[thread] = [user]
                msg = "I will notify {} when {} is updated and is the only user being notified. To unsubscribe use !unsub {}".format(user, thread, threadraw)
            elif thread in lookup.keys():
                if user in lookup[thread]:
                    msg = '{} was already on my list for that thread. To unsubscribe use !unsub {}'.format(user, thread, threadraw)
                else:
                    _list = lookup[thread]
                    _list.append(user)
                    lookup[thread] = _list
                    msg = "I will notify {} when {} is updated and is the only user being notified. To unsubscribe use !unsub {}".format(
                        user, thread, threadraw)
        await client.send_message(message.channel, msg)
    elif bool(re.match('!unsub', message.content, re.I)):
        user = str(message.author.mention)
        threadraw = re.search("\d\d+", message.content).group()
        thread = recentparser.convert_to_url(threadraw)
        #print(user, threadraw, thread)
        with shelve.open('threads') as lookup:
            if thread not in lookup.keys():
                lookup[thread] = [user]
                msg = "Sorry, but I didn't have anyone being notified for {}".format(thread)
            elif thread in lookup.keys():
                if user in lookup[thread]:
                    _list = lookup[thread]
                    _list.remove(str(user))
                    lookup[thread] = _list
                    msg = '{} has been unsubscribed from {} . To resume notifications please use !notify {}'.format(user, thread, threadraw)
                else:
                    msg = "{} was already unsubscribed from {} . To resume notifications please use !notify {}".format(
                        user, thread, threadraw)
        await client.send_message(message.channel, msg)
client.run('NDE4NDMwMjQ1ODgwOTg3NjU4.DXhdvQ.YxrLwaFujD8mayl6sHzkeZvC9Qs')