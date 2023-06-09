import os
import discord

env_type = os.getenv('ENV_TYPE')

# Define the role IDs in your .env file
if env_type == 'dev':
    ARCH_PIRATE_ROLE_ID = int(os.environ["DEV_ARCH_PIRATE_ROLE_ID"])
    CORSAIR_ROLE_ID = int(os.environ["DEV_CORSAIR_ROLE_ID"])
    DESPOILER_ROLE_ID = int(os.environ["DEV_DESPOILER_ROLE_ID"])
    RAIDER_ROLE_ID = int(os.environ["DEV_RAIDER_ROLE_ID"])
else:  # 'prod' or any other value
    ARCH_PIRATE_ROLE_ID = int(os.environ["ARCH_PIRATE_ROLE_ID"])
    CORSAIR_ROLE_ID = int(os.environ["CORSAIR_ROLE_ID"])
    DESPOILER_ROLE_ID = int(os.environ["DESPOILER_ROLE_ID"])
    RAIDER_ROLE_ID = int(os.environ["RAIDER_ROLE_ID"])

async def assign(interaction, leaderboard_data):
    guild = interaction.guild # This is a discord.Guild object
    role_ids = [ARCH_PIRATE_ROLE_ID, CORSAIR_ROLE_ID, DESPOILER_ROLE_ID]
    for idx, (user_id, _) in enumerate(leaderboard_data):
        user = await guild.fetch_member(user_id) # Fetch the user corresponding to user_id
        if user:
            # Remove existing roles
            for role_id in role_ids:
                role = guild.get_role(role_id)
                if role in user.roles:
                    await user.remove_roles(role)
            # Assign new role based on leaderboard position
            if idx == 0:
                await user.add_roles(guild.get_role(ARCH_PIRATE_ROLE_ID))
            elif idx == 1:
                await user.add_roles(guild.get_role(CORSAIR_ROLE_ID))
            elif idx == 2:
                await user.add_roles(guild.get_role(DESPOILER_ROLE_ID))
            else:
                await user.add_roles(guild.get_role(RAIDER_ROLE_ID))
