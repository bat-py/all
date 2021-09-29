from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
import random


def numbers_handler():
    with open('number.txt', 'r') as numbers:
        contacts = numbers.readlines()

    filtred = list(
        filter(lambda item: item != '\n' and not item.startswith('998') and not item.startswith('+998'), contacts))
    contacts = [i.replace(' ', '').replace('\n', '').replace('-', '').replace('+', '') for i in filtred]

    ready_contacts = []
    for i in contacts:
        if len(i) == 11 and i.startswith('1'):
            ready_contacts.append(i)
        elif len(i) == 10:
            ready_contacts.append('1' + i)

    return ready_contacts


def choose_group(client):
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

    g_index = input('Choose your group number: ')
    target_group = groups[int(g_index)]

    return target_group

def main():
    client = TelegramClient(phone, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        mycode = input("Enter the code:")

        try:
            client.sign_in(phone, mycode, password=passwd)
        except SessionPasswordNeededError:
            client.sign_in(password=passwd)

    phone_numbers = numbers_handler()
    target_group = choose_group(client)

#    print(target_group.id)

    for phone_number in phone_numbers:
        # add user to contact
        contact = InputPhoneContact(client_id=0, phone=phone_number, first_name=phone_number, last_name='')
        result = client(ImportContactsRequest([contact]))

        # add contact to your group
        #client(AddChatUserRequest(user_id=result.users[0], fwd_limit=0, chat_id=target_group))

    # remote contact



if __name__ == '__main__':
    api_id = 5193417
    api_hash = '55909d877eef1f996884aee6734dddb9'
    phone = input('Phone: ')
    passwd = input('Password: ')

    main()