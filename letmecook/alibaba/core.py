import os

# Bunları envayırımınttan çekmek çok daha güvenli olacak
ACCESS_KEY_ID = os.getenv("ALIBABA_ACCESS_KEY_ID", None)
ACCESS_KEY_SECRET = os.getenv("ALIBABA_ACCESS_KEY_SECRET", None)
