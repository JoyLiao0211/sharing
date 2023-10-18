import discord
import numpy
import os
import random
import datetime

"================================================================================="

last_message={}
async def check_3_same_message(message):
    global last_message
    if message.author==client.user:
        last_message[message.channel]=["",0]
    if message.channel not in last_message:
        last_message[message.channel]=[message.content,1]
    elif message.content==last_message[message.channel][0]:
        last_message[message.channel][1]+=1
    else:
        last_message[message.channel]=[message.content,1]
    if last_message[message.channel][1]==3:
        await message.channel.send(message.content)
        last_message[message.channel][1]=0

yege={}
async def check_yegebomb(message):
    yege_str=list("野格炸彈我的最愛")
    global yege
    if message.channel not in yege:
        yege[message.channel]=0
    if message.content != yege_str[yege[message.channel]]:
        yege[message.channel]=0
    if message.content == yege_str[yege[message.channel]]:
        yege[message.channel]+=1
        if yege[message.channel] < len(yege_str):
            await message.channel.send(yege_str[yege[message.channel]])
        yege[message.channel]+=1
    if yege[message.channel] >= len(yege_str):
        yege[message.channel] = 0

async def QQhahaha(message):
    QQ=["qq","QQ","qQ","Qq","哭哭"]
    for Q in QQ:
        if Q in message.content:
            await message.channel.send("哈哈哈")
            return

async def CFhandle(message):
    from bot_data import cf
    message_list=message.content.split()
    if message_list[0]=="set":
        if len(message_list)<2:
            await message.channel.send("wrong format! correct format:```set <handle>```")
            return
        await message.channel.send(cf.send_request(message.author.id,message_list[1]))
    elif message_list[0]=="verify":
        await message.channel.send(cf.check(message.author.id))
    else:
        await message.channel.send("wrong format! correct format:```set <handle>```or```verify```")

async def Baluting_board(message):
    mes_list=message.content.split()
    if mes_list[0] != "!Baluting":
        return
    from bot_data import baluting as bl
    if len(mes_list)==1:
        await message.channel.send(bl.enter())
        return
    if mes_list[1] == "post":
        if len(mes_list) != 4:
            await message.channel.send("wrong format! correct format:\n```\n!Baluting post <from> <content>\n```")
            return
        await message.channel.send(bl.post(mes_list[2],mes_list[3]))
    elif mes_list[1] == "pull":
        await message.channel.send(bl.pull())
    elif mes_list[1] == "exit":
        await message.channel.send(bl.exit())

async def XXlee(message):
    XXlst=["xx","XX","插","好日子"]
    flg=False
    str=message.content.lower()
    for XX in XXlst:
        if XX in str:
            await message.channel.send("https://media.discordapp.net/attachments/1159739169996812342/1159739748148052038/ezgif-1-fa359b3a1a.gif?ex=65321ece&is=651fa9ce&hm=65ca5f62d04aa6f1807bd30c8c7f9d240856cc60b41f17a336e760b99abac83e&")
            return

distribution={}
async def pick_someone(message):
    global distribution
    if len(distribution)==0:
        with open("bot_data/distr.txt","r") as file:
            distribution=eval(file.read())
    if message.author.id not in distribution:
        distribution[message.author.id]=10
    distribution[message.author.id]+=0.3
    # print(f"distribution[{message.author.name}]={distribution[message.author.id]}")
    if message.content == "抽到我的機率":
        await message.channel.send(f"抽到 {message.author.name} 的機率是 {int(distribution[message.author.id])/10} %")
    elif "抽一個人" in message.content:
        s=0.0
        members=message.guild.members
        for member in members:
            if member.id not in distribution:
                distribution[member.id]=10
            s+=distribution[member.id]
        print(s)
        for key in distribution:
            distribution[key]*=1000/s
        chosenid = random.choices(list(distribution.keys()), list(distribution.values()), k=1)[0]
        await message.channel.send(f"抽到 <@{chosenid}> 了",allowed_mentions=discord.AllowedMentions(users=False))
    with open("bot_data/distr.txt","w") as file:
        file.write(str(distribution))

async def pick_me(message):
    message_content=message.content.replace("ㄌ","了")
    if "抽到我了" not in message.content:
        return
    await message.channel.send(f"抽到 <@{message.author.id}> 了",allowed_mentions=discord.AllowedMentions(users=False))

async def zhong(message):
    zhong_reply_map={
        "需要解釋":"# 我需要解釋",
        "我不知道":"# 我不知道",
        "教授對不起":"# 教授對不起",
        "我不會git":"# 我不會ＧＩＴ",
        "施廣霖":"# 施～廣～霖～",
        "施~廣~霖~":"# 施～廣～霖～",
        "施～廣～霖":"# 施～廣～霖～"
    }
    str=message.content.lower()
    for key in zhong_reply_map.keys():
        if key in str:
            await message.channel.send(zhong_reply_map[key])
    zhong_react_list=["你要不要承認","表揚"]
    for key in zhong_react_list:
        if key in str:
            await message.add_reaction("🀄")
            break

last_che_message = None
async def default_react(message):
    # if message.channel.id==1162707874464682115: #哦鴨測機
    #     await message.channel.send("https://tenor.com/view/shake-head-anime-bocchi-the-rock-bocchi-the-rock-gif-bocchi-gif-27212768")
    # if message.author.id==764866433120206848: # 我
    #     await message.add_reaction("8️⃣")
    #     await message.add_reaction("🇼")
    #     await message.add_reaction("🇨")
    #     await message.add_reaction("🇵")
    if message.author.id==844093945616269323: #arctan
        await message.add_reaction("<:hao:1163133973795446935>")
    str=(message.content).lower()
    for member in message.guild.members:
        str=str.replace(f"<@{member.id}>",f"{member.display_name}")
    for emoji in message.guild.emojis:
        str=str.replace(f"{emoji.id}","")
    # print(str)
    if message.author.id==527891741055909910: #cheissmart ,"妻","漆","欺","棲","戚","淒"
        global last_che_message
        last_che_str = ""
        if last_che_message is not None:
            last_che_str = (last_che_message.content).lower();
            for member in message.guild.members:
                last_che_str=last_che_str.replace(f"<@{member.id}>",f"{member.display_name}")
            for emoji in message.guild.emojis:
                last_che_str=last_che_str.replace(f"{emoji.id}","")
        P7=["p7","seven","闖關","cco"]
        P7_2=["p", "7","闖", "關"]
        P7_st=["p", "闖"]
        P7_ed=["7", "關"]
        if sum([1 if p7 in str else 0 for p7 in P7]) > 0:
            await message.channel.send("https://tenor.com/view/shake-head-anime-bocchi-the-rock-bocchi-the-rock-gif-bocchi-gif-27212768")
        elif sum([1 if p7 in str else 0 for p7 in P7_2]) > 1:
            await message.channel.send("https://tenor.com/view/shake-head-anime-bocchi-the-rock-bocchi-the-rock-gif-bocchi-gif-27212768")
        elif sum([1 if p7 in last_che_str else 0 for p7 in P7_st]) > 0 and sum([1 if p7 in str else 0 for p7 in P7_ed]) > 0:
            await message.channel.send("https://tenor.com/view/shake-head-anime-bocchi-the-rock-bocchi-the-rock-gif-bocchi-gif-27212768")
        last_che_message = message
    
    cp8w=["8w"]
    if (message.author.id==364761561866174465 and "wiwi" in str) or (message.author.id==331730758555402240 and "8e7" in str) or sum([1 if cp in str else 0 for cp in cp8w]) > 0:
        await message.add_reaction("8️⃣")
        await message.add_reaction("🇼")
        await message.add_reaction("🇨")
        await message.add_reaction("🇵")
        return
    eights=["8","eight","八","8️⃣","８","🎱"]
    no_eights=["8w"]
    if sum([1 if eight in str else 0 for eight in eights]) > 0 and sum([1 if noteight in str else 0 for noteight in no_eights]) == 0:
        await message.add_reaction("8️⃣")
    
    sadge=["封鎖"]
    if sum([1 if sad in str else 0 for sad in sadge]) > 0:
        await message.add_reaction("😢")


async def upd_cf_roles(guild):
    from bot_data import cf
    import time
    with open("bot_data/handle/handle.txt","r") as f:
        handle_map=eval(f.read())
    role_ids=[1164186643129970789,1164186598338998342,1164186553606733824]
    roles=[guild.get_role(roid) for roid in role_ids]
    for member in guild.members:
        if member.id not in handle_map:
            continue
        rating=-1
        while rating<0:
            time.sleep(0.3)
            rating=cf.get_rating(handle_map[member.id]["handle"])
        # if handle_map[member.id]["rating"] == rating:
        #     continue
        handle_map[member.id]["rating"]=rating
        lst=[False,False,False]
        if rating >= 2100:
            lst[2]=True
        elif rating >= 1900:
            lst[1]=True
        elif rating >= 1600:
            lst[0]=True
        for i in range(3):
            if lst[i]:
                await member.add_roles(roles[i])
            elif not lst[i]:
                await member.remove_roles(roles[i])
        print(member.name,lst,rating)
    with open("bot_data/handle/handle.txt","w") as f:
        f.write(str(handle_map))

"================================================================================="

last_upd_time=None
async def check_ver(message):
    if(message.content=="check ver"):
        await message.channel.send(f"last upd: {last_upd_time}")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    global last_upd_time
    last_upd_time=datetime.datetime.now().replace(microsecond=0)
    print("on ready")

@client.event
async def on_message(message):
    # print(f"{message.author.display_name}, {message.author.global_name}, {message.author.name}")
    if message.channel.id == 1162707874464682115: #哦鴨測機
        print("測機")
    # return
    if message.author==client.user:
        global last_message
        last_message[message.channel]=["",0]
        return
    if message.channel.id==1162757642045903009: # CF手把
        await CFhandle(message)
        return
    if len(message.content)==0:
        return
    if message.channel.id==1157685969135345785: # 重要訊息
        return
    await check_3_same_message(message)
    await check_ver(message)
    if message.channel.id==1141778910955180032: # 真的依某
        return
    await QQhahaha(message)
    await check_yegebomb(message)
    await pick_someone(message)
    await pick_me(message)
    await Baluting_board(message)
    await XXlee(message)
    await zhong(message)
    await default_react(message)

    

if __name__ == "__main__":
    TOKEN=""
    with open("../data.txt","r") as data:
        TOKEN=eval(data.read())["TOKEN"]
    client.run(TOKEN)
    print("owo??")

