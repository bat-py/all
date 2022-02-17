from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import SessionPasswordNeededError
import sys
import traceback
import time
import random
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from time import sleep


#    writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
def get_members_list(client, msg):
    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue

    print()
    i = 0
    for g in groups:
        print(str(i) + '- ' + g.title)
        i += 1

    g_index = input(msg)
    target_group = groups[int(g_index)]

    print('Fetching Members...')

    offset = 0
    limit = 9999
    all_participants = []

    while True:
        participants = client(GetParticipantsRequest(
            target_group, ChannelParticipantsSearch(''), offset, limit,
            hash=0
        )) 
        
        if not participants.users:
            break

        all_participants.extend(participants.users)
        offset += len(participants.users)


    my_group_members_list = []

    for user in all_participants:
        if user.username:
            username = user.username
        else:
            username = ""
        if user.first_name:
            first_name = user.first_name
        else:
            first_name = ""
        if user.last_name:
            last_name = user.last_name
        else:
            last_name = ""
        name = (first_name + ' ' + last_name).strip()
        my_group_members_list.append([username, user.id, user.access_hash, name, target_group.title, target_group.id])
    print('Members scraped successfully.\n')

    return my_group_members_list, target_group

def sort_members(my_group_members_list, another_group_members_list):
    my_d = my_group_members_list
    another_d = another_group_members_list

    my_d_id = [j[0] for j in my_d if j[0]]
    another_d_id = [i[0] for i in another_d if i[0]]

    my = set(my_d_id)
    another = set(another_d_id)

    clear_data = another - my
    return list(clear_data)

def fast_join(client, clear_list, target_group):
    users = clear_list
    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue




    target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)
    err = 0
    for user in users:
        try:
            print("Adding {}".format(user))
            if user == "":
                continue
            user_to_add = client.get_input_entity(user)

            client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            print("Waiting 1 Second...")
            time.sleep(1)
        except PeerFloodError:
            print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
            if err == 5:
                print('sim blocked')
                break
            err += 1
        except UserPrivacyRestrictedError:
            print("The user's privacy settings do not allow you to do this. Skipping.")
        except:
            traceback.print_exc()
            print("Unexpected Error")
            continue

def slow_join(client, clear_list, target_group):
    users = clear_list
    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue



    target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

    n = 0

    err = 0

    for user in users:
        n += 1
        if n % 50 == 0:
            time.sleep(900)
        try:
            if user:
                print("Adding {}".format(user))
                user_to_add = client.get_input_entity(user)
                client(InviteToChannelRequest(target_group_entity, [user_to_add]))
                print("Waiting for 60-180 Seconds...")
                time.sleep(random.randrange(60, 180))
        except PeerFloodError:
            if err == 5:
                print('sim blocked')
                break
            err += 1

            print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")

        except UserPrivacyRestrictedError:
            print("The user's privacy settings do not allow you to do this. Skipping.")
        except:
            traceback.print_exc()
            print("Unexpected Error")


if __name__ == '__main__':
    api_id = 5834063
    api_hash = '19562bd0e42c33f334b7735632fbb822'
    phone = input('Enter phone number: ')
    passwd = "Behruz2000"
    

    client = TelegramClient(phone, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        mycode = input("Enter the code:")

        try:
            client.sign_in(phone, mycode, password=passwd)
        except SessionPasswordNeededError:
            client.sign_in(password=passwd)


    my_group = get_members_list(client, 'Choose your group number: ')
    my_group_members_list = my_group[0]
    target_group = my_group[1]

    another_group_members_list = get_members_list(client, 'Choose a group number to scrape members from: ')[0]

    clear_list = sort_members(my_group_members_list, another_group_members_list)

    t = '\n1. Fast join\n2. Slow join by 50 members\nChoose join mode: '
    fast_or_slow_join = int(input(t))

    if fast_or_slow_join == 1:
        fast_join(client, clear_list, target_group)
    elif fast_or_slow_join == 2:
        slow_join(client, clear_list, target_group)
    else:
        exit()





