import requests
import json
from urllib.parse import unquote
from solana.keypair import Keypair
import base58
import os
from mnemonic import Mnemonic  

login_url = "https://api.paws.community/v1/user/auth"
wallet_url = "https://api.paws.community/v1/user/sol-wallet"


headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Origin": "https://app.paws.community",
    "Referer": "https://app.paws.community/",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
}


with open('data.txt', 'r') as file:
    lines = file.readlines()


def generate_solana_wallet():

    keypair = Keypair.generate()  

    public_key = keypair.public_key
    public_key_base58 = base58.b58encode(bytes(public_key)).decode()  

    mnemonic = generate_mnemonic()

    username = "username_placeholder"  

    with open('wallet.txt', 'a') as wallet_file:
        wallet_file.write(f"Wallet {len(open('wallet.txt').readlines()) // 3 + 1}:\n")
        wallet_file.write(f"Username: {username}\n")
        wallet_file.write(f"Mnemonic: {mnemonic}\n")
        wallet_file.write(f"Public Key: {public_key_base58}\n")
    
    return public_key_base58

def generate_mnemonic():

    mnemo = Mnemonic("english")

    mnemonic = mnemo.generate(strength=256)  
    return mnemonic

def process_line(line):

    decoded_data = unquote(line.strip())

    wallet_address = generate_solana_wallet()

    payload = {
        "data": decoded_data
    }

    response = requests.post(login_url, headers=headers, json=payload)

    if response.status_code == 200 or response.status_code == 201:
        print("Login successful!")
        response_data = response.json()

        token = response_data['data'][0]  
        user_info = response_data['data'][1]  
        print(f"JWT Token: {token}")
        print(f"User Info: {json.dumps(user_info, indent=4)}")
        
        connect_wallet(token, wallet_address)
    else:
        print(f"Failed to login. Status code: {response.status_code}")
        print("Response Text:", response.text)

def connect_wallet(token, wallet_address):
    wallet_payload = {
        "wallet": wallet_address
    }

    wallet_headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    wallet_response = requests.post(wallet_url, headers=wallet_headers, json=wallet_payload)
    
    if wallet_response.status_code == 201:
        print("Wallet connected successfully!")
        print("Wallet Response:", wallet_response.json())
    else:
        print(f"Failed to connect wallet. Status code: {wallet_response.status_code}")
        print("Wallet Response Text:", wallet_response.text)

for line in lines:
    process_line(line)
