import discord
from discord.ext import commands
import mysql.connector
from mysql.connector import Error


try:
    connection = mysql.connector.connect(host='localhost',
                                         database='bot',
                                         user='discord',
                                         password='Asdf@123')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        cursor = connection.cursor()

except Error as e:
    print("Error while connecting to MySQL", e)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

client = commands.Bot(command_prefix= '--', intents=intents)


@client.event
async def on_member_join(member):
    guild = member.guild
    welcome_channel = discord.utils.get(guild.channels, name='welcome')
    await welcome_channel.send(f'Welcome {member.mention} to the server!, Nice to meet you')   


@client.event
async def on_reaction_add(reaction, user):
    guild = user.guild
    reaction_channel = discord.utils.get(guild.channels, name='reaction')
    await reaction_channel.send(f"{user.mention} reacted with {reaction.emoji} to {reaction.message.author.mention}'s message")


@client.command(name='create')
async def create(context, param):
    role = discord.utils.get(context.guild.roles, name=param)

    if role:
        await context.channel.send(f'{role} already exists')
        # await context.author.add_roles(role)

    else:
        new_role = await context.guild.create_role(name=param)
        await context.author.add_roles(new_role)
        await context.channel.send(f'{param} role created and assigned to {context.author.mention}')  


@client.command(name='register')
async def register(context, param):
    name = str(param.lower())
    query1 = f"SELECT * FROM user WHERE user_name = '{name}'"
    query2 = f"INSERT INTO user (user_name) VALUES ('{name}')"
    cursor.execute(query1)

    user = cursor.fetchall()

    if user:
        await context.channel.send(f'{name} already exists')

    else:
        cursor.execute(query2)
        connection.commit()
        await context.channel.send(f'{param} added to database')


@client.command(name='fetch')
async def fetch(context):
    role = context.author.roles
    flag = False
    for i in role:
        if i.name == 'admin':
            flag = True
            break
    print(flag)
    if flag:
        query = f"SELECT * FROM user"
        cursor.execute(query)
        users = cursor.fetchall()
        context.channel.send('Users are:')
        for user in users:
            await context.channel.send(user[0])
        
    else:
        await context.channel.send('You are not authorized to view users')  


client.run('MTA3MzcwNzAyOTc1NzE3Nzg1Nw.GsS6IU.z1Ma5J6SHW94CdXbgIwzqolf5TEQqyLBGftOYk')