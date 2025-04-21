from smartcard.System import readers
from smartcard.Exceptions import NoCardException, CardConnectionException
import time
import asyncio
import websockets
import json
from smartcard.util import toHexString
import requests
import os
import pathlib

GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]

r = readers()
reader = r[0]
connection = reader.createConnection()

last_uid = None
tag_present = False

# Mendapatkan path absolut ke direktori hw.html
IMAGES_DIR = 'downloaded_images'

def read_database(filename: str):
    import json
    result = None

    data = []
    with open(filename, "r") as f:
        data = f.read()
    data = json.loads(data)
    return data 

def query(database, q):
    for item in database:
        if item.get("TagUUID") == q:
            return item
    return None

def download_images(toy_number, gallery_images):
    save_folder = str(IMAGES_DIR)
    os.makedirs(save_folder, exist_ok=True)
    
    # Cek apakah sudah ada file dengan prefix toy_number
    prefix = f"{toy_number}_"
    existing_files = sorted([f for f in os.listdir(save_folder) if f.startswith(prefix)])
    
    if existing_files:
        print(f"Files with prefix {prefix} already exist: {existing_files}")
        return existing_files
    
    # Jika tidak ada file yang sesuai, lakukan download
    downloaded_files = []
    counter = 1
    
    for url in gallery_images:
        if url.startswith("http"):
            try:
                ext = ".jpg" if "jpg" in url else ".png"
                filename = f"{toy_number}_{counter:03d}{ext}"
                filepath = os.path.join(save_folder, filename)
                
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                with open(filepath, "wb") as f:
                    f.write(response.content)
                
                print(f"Downloaded: {filename}")
                downloaded_files.append(filename)
                counter += 1
                
            except Exception as e:
                print(f"Failed to download {url} - {e}")
    
    return sorted(downloaded_files)

async def handle_client(websocket):
    print("New client connected")
    r = readers()
    last_uid = None
    
    try:
        while True:
            if len(r) > 0:
                reader = r[0]
                try:
                    connection = reader.createConnection()
                    connection.connect()
                    
                    get_uid = [0xFF, 0xCA, 0x00, 0x00, 0x00]
                    data, sw1, sw2 = connection.transmit(get_uid)
                    uid = toHexString(data).replace(' ', '')
                    
                    if uid:
                        if uid != last_uid:  # Hanya kirim jika UID baru berbeda
                            print(f"NFC Tag detected: {uid}")
                            result = query(database=database, q=uid)
                            print("Result")
                            print(result)
                            if result:
                                # Kirim status downloading
                                await websocket.send(json.dumps({
                                    "downloading": True,
                                    "Col #": result.get("Col #", "Unknown"),
                                    "Series": result.get("Series", "Unknown"),
                                    "Toy #": result.get("Toy #", "Unknown")
                                }))
                                
                                # Download images jika diperlukan
                                if "Gallery Images" in result and "Toy #" in result:
                                    downloaded_files = download_images(result["Toy #"], result["Gallery Images"])
                                    result["downloaded_images"] = downloaded_files
                                
                                print(f"Sending data for UID: {uid}")
                                result["downloading"] = False
                                await websocket.send(json.dumps(result))
                            last_uid = uid
                    
                except Exception as e:
                    if last_uid is not None:  # Tag telah dilepas
                        print("Tag removed from reader")
                        await websocket.send(json.dumps({"tag_removed": True}))
                        last_uid = None
                    time.sleep(1)
                    
            await asyncio.sleep(0.1)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    except Exception as e:
        print(f"Error in handle_client: {str(e)}")

async def main():
    print("Loading database...")
    global database
    with open('database.json', 'r') as f:
        database = json.load(f)
    print("Database loaded successfully")
    
    print("Starting WebSocket server...")
    async with websockets.serve(handle_client, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
