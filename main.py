from telethon import TelegramClient, functions, types
import time 
import re
# Your API credentials from https://my.telegram.org
api_id = '29482431'
api_hash = 'f6d3d53a435d6ac1ba2388508f7bdb38'
phone_number = '+919826494059'

# Initialize the client
client = TelegramClient('+919826494059', api_id, api_hash)

async def create_and_add_user():
    await client.start(phone=phone_number)
    
    # # Step 1: Create a supergroup
    # result = await client(functions.channels.CreateChannelRequest(
    #     title='My Supergroup',         # Supergroup name
    #     about='This is a test supergroup.',  # Description
    #     megagroup=True                 # Ensure it's a supergroup
    # ))
    # print("Supergroup created successfully.")
    
    # Get the channel details
    # channel = result.chats[0]
    with open("output.txt", 'r') as file:
        # Read the file lines, strip whitespace, and filter non-empty lines
        phone_numbers = [line.strip() for line in file if line.strip()]
    # Step 2: Add a contact
    index= 0 
    tries = 0 
    for i in phone_numbers:

        contact_phone = i
        
        try:
            if tries>=19:
                time.sleep(50)
            # Import contact
            contact = await client(functions.contacts.ImportContactsRequest(
                contacts=[types.InputPhoneContact(
                    client_id=0,
                    phone=contact_phone,
                     first_name="unknown",
                last_name=''             # Leave last name empty
                )]
            ))
            
            # Step 3: Add the user to the supergroup
            user = contact.users[0]       # Fetch the user details from the contact import result
            if index==0:print(user)
            index += 1 
            with open("ids.txt","a") as file:
                file.write(f"{str(user.id)}\n")
            # await client(functions.channels.InviteToChannelRequest(
            #     channel=channel,
            #     users=[user.id]            # Add user by ID
            # ))
            print("User added successfully.")
            tries += 1
            time.sleep(3)
        
        except Exception as e:
            print(f"Error adding user: {e}")
            with open("error.txt","a") as file:
                file.write(f"{e}\n")
            if "list index out of range" in str(e):
                print(contact)
                with open("index.txt","a") as file:
                    file.write(f"{i}\n")
            else:
                with open("retry.txt","a") as file:
                    file.write(f"{i}\n")
            if "A wait of" in str(e):
                match = re.search(r"A wait of (\d+) seconds", str(e))
                if match:
                    seconds = int(match.group(1))
                    print(f"Extracted seconds: {seconds}")
                    time.sleep(seconds)
                else:
                    print("No seconds found in the message.")


# Run the event loop
with client:
    client.loop.run_until_complete(create_and_add_user())
