import requests
import pprint
import json


def req(var):
    h = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.get(var, headers=h)
    return r


ngrok_url = "https://f4ca914b.ngrok.io"

BOOT_TOKEN = '949480708:AAEBUxQtVyUuFJTxJX7byAiF4ur5oHy-BcA'

h = "https://api.telegram.org/bot841238697:AAEV2SXf19DW6HWL3fn_7rVzwCoE6WctoVc/getUpdates"

set_hooks = f"https://api.telegram.org/bot{BOOT_TOKEN}/setWebhook?url={ngrok_url}"

update = f"https://api.telegram.org/bot{BOOT_TOKEN}/getUpdates?url={ngrok_url}"

delete = f"https://api.telegram.org/bot{BOOT_TOKEN}/deleteWebhook?url={ngrok_url}"
get_info = f"https://api.telegram.org/bot{BOOT_TOKEN}/getMe"
get_winfo = f"https://api.telegram.org/bot{BOOT_TOKEN}/getWebhookInfo"


response = req(set_hooks)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(response.headers)
pp.pprint(json.loads(response.content))
