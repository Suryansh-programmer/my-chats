from telethon import TelegramClient, functions, types


# # Your API credentials from https://my.telegram.org
# api_id = '29482431'
# api_hash = 'f6d3d53a435d6ac1ba2388508f7bdb38'
# # phone_number = '+919753441978'

# # # Initialize the client
# # client = TelegramClient('+919753441978', api_id, api_hash)
# phone_number = '+919826494059'

# # Initialize the client
# client = TelegramClient('+919826494059', api_id, api_hash)

# async def create_and_add_user():
#     await client.start(phone=phone_number)
    
#     # Step 1: Create a supergroup/channel
#     result = await client(functions.channels.CreateChannelRequest(
#         title='Testing shadow',          # Supergroup name
#         about='This is a test supergroup.',  # Description
#         megagroup=True                # Ensure it's a supergroup
#     ))
    
#     print("Supergroup created successfully.")
    
#     # Get the channel details
#     channel = result.chats[0]
#     print(channel.id)
#     # # Step 2: Add a user to the supergroup
#     # with open("index.txt", 'r') as file:
#     #     # Read the file lines, strip whitespace, and filter non-empty lines
#     #     users = [line.strip() for line in file if line.strip()]
#     # print("Starting........")
#     # for user_to_add in users:
#     #     try:
#     #         # user_entity = await client.get_entity(user_to_add)
#     #         # print(f"User entity fetched: {user_entity}")
#     #         # await client(functions.messages.InviteToChannelRequestt(
#     #         #     chat_id=channel.id,       # ID of the supergroup
#     #         #     user_id=user_entity,      # The user to add
#     #         #     fwd_limit=0               # Forwarded messages limit
#     #         # ))
#     #         await client(functions.channels.InviteToChannelRequest(
#     #             channel=channel,
#     #             users=users           # Add user by ID
#     #         ))
#     #         print("User added successfully.")
#     #     except Exception as e:
#     #         print(f"Error adding user: {e}")
#     #         with open("indexerror.txt","a") as file:
#     #             file.write(f"{user_to_add}\n")

# # Run the event loop
# with client:
#     client.loop.run_until_complete(create_and_add_user())


from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch


# Your API credentials from https://my.telegram.org
api_id = '29482431'
api_hash = 'f6d3d53a435d6ac1ba2388508f7bdb38'
# phone_number = '+919753441978'

# # Initialize the client
# client = TelegramClient('+919753441978', api_id, api_hash)
phone_number = '+919826494059'

# Initialize the client
client = TelegramClient('+919826494059', api_id, api_hash)


async def fetch_all_participants(channel):
    offset = 0
    limit = 100
    all_participants = []
    hash_value = 0

    while True:
        participants = await client(GetParticipantsRequest(
            channel=channel,
            filter=ChannelParticipantsSearch(''),
            offset=offset,
            limit=limit,
            hash=hash_value
        ))
        print(participants.users)
        all_participants.extend(participants.users)
        if not participants.users:  # If no more users, break the loop
            break
        hash_value += 1  # Update the hash for the next request
        offset += limit  # Move the offset to the next batch
    print(all_participants)
    return all_participants

with client:
    client.loop.run_until_complete(fetch_all_participants(2310692631))
