from dotenv import load_dotenv

from src import client

load_dotenv()

client.EmbergardClient().run()
