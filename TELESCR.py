import re
import asyncio
from telethon.sync import TelegramClient
from telethon.tl import types
from datetime import datetime
import requests
from config import API_ID, API_HASH, SESSION, SEND_ID

async def main():
    client = TelegramClient('alterchkbot_alpha', API_ID, API_HASH)
    await client.start()

    def filter_cards(text):
        regex = r'\d{16}.*\d{3}'
        matches = re.findall(regex, text)
        if matches:
            return ''.join(matches)
        else:
            return None

    async def alterchkbot(message):
        try:
            rt = 0
            while rt < 6:
                if 'Checking CC. Please wait.🟥' in message.text or 'Checking CC. Please wait.🟧' in message.text or 'Checking CC. Please wait.🟩' in message.text or 'CHECKING CARD 🔴' in message.text:
                    await asyncio.sleep(30)
                    message = await client.get_messages(message.chat_id, ids=message.id)
                    rt += 1
                    continue
                else:
                    break

            if re.search(r'Approved', message.text):
                card = filter_cards(message.text)
                if card is None:
                    return

                # Check if the card has been posted before
                if card_exists_in_alterchkbot_file(card):
                    return

                new_text = re.sub(r'Checked by .* User]', '**Checked ву [˹ᴧŁþнᴧ ꭙ˼](tg://user?id=1057412250)** \n━━━━━━━━━━━━━━━━━',
                                message.text)

                new_text = new_text.replace('Bot by --» Tfp0days☃️', '')
                new_text = new_text.replace('———»Details«———', '━━━━━━━━━━━━━━━━━')
                new_text = new_text.replace('———-»Info«-———-', '━━━━━━━━━━━━━━━━━')
                new_text = new_text.replace('-»', '➻')

                cc = re.search(r'\d{16}', new_text).group(0)
                date = re.search(r'\d{2}\|\d{2}', new_text).group(0)
                cvv = re.search(r'\d{3}', new_text).group(0)
                bin = cc[:6]
                gateway = re.search(r'Gateway: (.+?)\n', message.text).group(0)
                result = re.search(r'Result: (.+?)\n', message.text).group(0)
                status = 'Approved ✅'
                gateway = 'Unknown'
                result = 'Unknown'

                response = requests.get(f"https://bins.antipublic.cc/bins/{bin}")
                if response.status_code == 200:
                    data = response.json()
                    info = data.get('level')
                    bank = data.get('bank')
                    type = data.get('type')
                    country = data.get('country')
                    country_flag = data.get('countryInfo').get('emoji')
                else:
                    info = 'Unknown'
                    bank = 'Unknown'
                    country = 'Unknown'

                current_time = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
                new_text = f"""• Card ⌁
{cc}|{date}|{cvv}

• Status ⌁ {status}
• Gateway ⌁ {gateway}
• Result ⌁ {result}

• Bin  ⌁ ({bin})

• Info ⌁ {info}
• Bank ⌁ {bank}
• Type ⌁ {type}
• Country ⌁ {country} {country_flag}

Check by - ALPHA

• Time : {current_time}"""

                # Post the new credit card to the channel
                await client.send_message(SEND_ID, new_text)

                # Write the new credit card to alterchk.txt
                with open('alterchk.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{cc} - Apprroved ✅\n")

        except Exception as e:
            print(e)

    def card_exists_in_alterchkbot_file(card):
        with open('alterchk.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if card in line:
                    return True
        return False

    @client.on(types.NewMessage)
    async def suck(event):
        if event.text:
            await asyncio.create_task(alterchkbot(event))

    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
