from telethon import TelegramClient

# Fungsi untuk membaca API ID, Hash, dan informasi lain dari file .txt
def read_api_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            credentials[key] = value
    return credentials

# Baca API dari file
api_credentials = read_api_credentials('telegram_api.txt')

# Ekstrak nilai dari dict
api_id = int(api_credentials['api_id'])
api_hash = api_credentials['api_hash']
phone_number = api_credentials['phone_number']
receiver_username = api_credentials['receiver_username']

# sesuaikan nama session jika punya .session / buat nama baru
session_name = 'aye'
client = TelegramClient(session_name, api_id, api_hash)

async def send_telegram_message(message):
    # Start the client session
    async with client:
        await client.send_message(receiver_username, message)
        print(f"Pesan berhasil dikirim ke {receiver_username}")
