from telethon.sync import TelegramClient

class TelegramBot:
    def __init__(self, config_file='telegram_api.txt'):
        self.client = None
        self.config = self.read_config(config_file)

    def read_config(self, file_path):
        config = {}
        with open(file_path, 'r') as f:
            for line in f:
                key, value = line.strip().split('=')
                config[key] = value
        return config

    async def send_message(self, message):
        if self.client is None:
            print("Inisialisasi client...")
            api_id = self.config['api_id']
            api_hash = self.config['api_hash']
            session_name = 'aye'
            
            # Inisialisasi Telethon Client
            self.client = TelegramClient(session_name, api_id, api_hash)
            await self.client.start()  # Mulai client dan otentikasi

        chat_id = self.config['receiver_username']
        await self.client.send_message(chat_id, message)

    def send_telegram(self, message):
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.send_message(message))

# Inisialisasi bot
telegram_bot = TelegramBot()