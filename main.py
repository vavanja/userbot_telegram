import datetime
import time
import asyncio
import webbrowser

from telethon import TelegramClient, functions
from telethon.errors import PeerFloodError
from telethon.tl.types import InputPeerChat

# Go to my.telegram.org
# Create your app
# Copy from here: api_id, api_hash
api_id = 1111111111  # Your api_id
api_hash = 'Your api_hash from https://my.telegram.org/apps'
phone = 'Your phone number'
SLEEP_TIME = 20


async def main():
    async with TelegramClient('session', api_id, api_hash) as client:

        await client.start()

        mode = int(input('Enter 1 to send messages to users or 2 to send by group/chats: '))
        print("-------------------------")

        if mode == 1:
            # Messages by users
            users_base = input('Enter 1000 users numbers: ').split(';')
            print("-------------------------")

            if len(users_base) >= 1:
                print(f'Enter 1000 numbers or less!!!\nYou passed {len(users_base)}')
                users_base = input('Enter 1000 users numbers: ').split(';')

            message = str(input('Enter your message: '))
            print("-------------------------")

            count = 0
            for user in users_base:
                try:
                    await client.send_message(user, message)
                    count += 1
                    print(f"Waiting {SLEEP_TIME} seconds")
                    print("-------------------------")
                    time.sleep(SLEEP_TIME)

                except PeerFloodError:
                    print(
                        "Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
                    await client.disconnect()

                except Exception as e:
                    print('Error:', e)
                    print('Trying to continue....')
                    print("-------------------------")
                    continue

            print(f"Send {count} messages.\nWork is done, i am going to sleep...\nDisconnected")
            print("-------------------------")
            await client.disconnect()

        elif mode == 2:
            # Messages by groups/chats
            chats = []

            all_chats = await client(functions.messages.GetAllChatsRequest(except_ids=[]))
            for _, chat in enumerate(all_chats.chats):
                chats.append(chat.id)

            message = input('Enter your message: ')
            print("-------------------------")

            count = 0
            for group_id in chats:

                try:
                    chat = InputPeerChat(group_id)
                    if chat:
                        await client.send_message(group_id, message)
                        count += 1

                        print(f"Waiting {SLEEP_TIME} seconds")
                        print("-------------------------")
                        time.sleep(SLEEP_TIME)

                except Exception as e:
                    print('Erorr:', e)
                    continue

            print(f"Send {count} messages.\nWork is done, i am going to sleep...\nDisconnected")
            print("-------------------------")
            await client.disconnect()

        else:
            print('Invalid mode. Exiting')
            await client.disconnect()

        html_content = f"<p><b>Sending type:</b> {['By users' if mode == 1 else 'By groups/chats'][0]}," \
                       f" <b>Message:</b> '{message}', <b>Total sended messages:</b> {count}," \
                       f" <b>Time:</b> {datetime.datetime.now()}\n<p>"

        with open('index.html', '+a') as html_file:
            html_file.writelines(html_content)
        time.sleep(1)
        webbrowser.open_new_tab('index.html')


asyncio.run(main())
