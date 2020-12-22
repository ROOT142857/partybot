import discord
import math
from poker import *
from moneymanage import *
from discord.ext import commands

bot = commands.Bot(command_prefix = '$',status=discord.Status.online)

token = 'NzkwNDgyMTM5NDg1MTc1ODM5.X-BP3A.vaQP82Pce4bgSRKmv-t0ZgFscQo'

NowParty = []

Money = {}

Censor_object = ['ㅅㅂ','ㅆㅂ','ㅆ바','ㅅ바','ㅆ발','ㅅ발','시발','씨발','개새끼','병신','싸발','씹새끼','십새끼']
Censor_object_minor = []

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name) # 토큰으로 로그인 된 bot 객체에서 discord.User 클래스를 가져온 뒤 name 프로퍼티를 출력
    print(bot.user.id) # 위와 같은 클래스에서 id 프로퍼티 출력
    print('이게 되네?')
    print('------')

@bot.event
async def on_message(message):
    message_content = message.content
    message_author = message.author
    for i in Censor_object:
        if message_content.find(i)>=0 and not message_author.bot:
            await message.channel.send("%s님! 바른말 고운말을 사용합시다!"%(message_author.nick))
            await message.delete()
    if message_content == '!현재파티':
        partymem = ''
        for i in NowParty:
            partymem = partymem + i + ', '
        partymem = partymem +'총인원 : %d명'%(len(NowParty))
        await message.channel.send(partymem)
    if message_content == '!파티참가' and not message_author.nick in NowParty:
        NowParty.append(message_author.nick)
        print(NowParty,len(NowParty))
        await message.channel.send("%s님이 파티에 참가하였습니다"%(message_author.nick)) 
    elif message_content == '!파티참가' and message_author.nick in NowParty:
        await message.channel.send("이미 파티에 참가되어있습니다!")   
    if message_content == '!파티탈퇴' and message_author.nick in NowParty:
        NowParty.remove(message_author.nick)
        await message.channel.send("%s님이 파티에서 탈퇴하였습니다"%(message_author.nick))
    elif message_content == '!파티탈퇴' and not message_author.nick in NowParty:
        await message.channel.send("이미 파티에서 탈퇴되어있습니다!")   
    if message_content == '!파티삭제':
        NowParty.clear()
        await message.channel.purge(limit = 100) 
    try:
        if message_content == '!돈 설정 1000':
                Money[message_author.nick] = 1000
                await message.channel.send("%s님의 소지 금액이 %d으로 초기화되었습니다!"%(message_author.nick,Money[message_author.nick]))
        if message_content == '!파산':
            if not message_author.nick in Money.keys() or Money[message_author.nick] == 0:  
                Money[message_author.nick] = 20 
                await message.channel.send("%s님의 소지 금액이 %d으로 초기화되었습니다!"%(message_author.nick,Money[message_author.nick]))
        if message_content == '!내돈':
            await message.channel.send("%s님의 소지 금액은 %d입니다!"%(message_author.nick,Money[message_author.nick]))
        if '!동전도박' in message_content and not message_author.bot:
            try:
                if message_content.split()[1] == '전재산':
                    cost = Money[message_author.nick]
                else:
                    cost = int(message_content.split()[1])
                if cost > Money[message_author.nick]:
                    await message.channel.send("현재 %s님이 소지하고 계신 금액보다 걸린 돈이 많습니다! 다시 시도해주세요"%(message_author.nick))
                elif cost<0:
                    await message.channel.send("거는 돈을 음수로 하면 안되지 ㅎㅎ")
                else:    
                    Money[message_author.nick] -= cost
                    Odds = [0,1.6]
                    Choiced = random.choice(Odds)
                    Money[message_author.nick] += math.floor(cost*Choiced)
                    if Choiced == 0:
                        await message.channel.send("아쉽습니다~! 다시 한 번 도전하세요~!")
                    elif Choiced == 1.6:
                        await message.channel.send("축.하.합.니.다~!.하.하.하! %d만큼의 이익을 얻으셨군요!"%((math.floor(cost*Choiced))-cost))
            except: 
                pass  
        if '!포커도박' in message_content and not message_content == '!포커도박설명' and not message_author.bot and message_content.find('!포커도박') == 0:
            cost = int(message_content.split()[1])
            totalcost = cost*int(message_content.split()[3])
            trial = int(message_content.split()[3])
            if totalcost > Money[message_author.nick]:
                await message.channel.send("현재 %s님이 소지하고 계신 금액보다 걸린 돈이 많습니다! 다시 시도해주세요"%(message_author.nick))
            elif cost<0 or totalcost<0:
                await message.channel.send("거는 돈을 음수로 하면 안되지 ㅎㅎ")
            elif int(message_content.split()[2]) > 8 or int(message_content.split()[2]) < 0:
                await message.channel.send("정상적인 선택지를 선택해주세요")
            else:
                for x in range(1,trial+1):
                    chsed = 0
                    chosen = int(message_content.split()[2])
                    Money[message_author.nick] -= cost
                    hands = []
                    Odds = [1.5,2,16,30,200,400,700,3000,60000]
                    onehand = randomHand(5)
                    hands.append(onehand)
                    L = countPokerHands(hands)
                    Res = [1]
                    for i in range(8):
                        Res.append(L[i])
                        if L[i] == 1:
                            chsed = i+1 
                    for i in range(9):
                        if i == chosen:
                            Odds[i] *= cost
                        else:
                            Odds[i] = 0
                    earned = math.floor(Res[chsed]*Odds[chsed])
                    Money[message_author.nick] += earned
                    if trial < 5:
                        await message.channel.send("%s님의 예측: %d\n 실제: %d"%(message_author.nick,chosen,chsed))
                        await message.channel.send("(문양(0~3),숫자(1~13)):(%d,%d),(%d,%d),(%d,%d),(%d,%d),(%d,%d)"%(onehand.cards[0].suit,onehand.cards[0].rank,onehand.cards[1].suit,onehand.cards[1].rank,onehand.cards[2].suit,onehand.cards[2].rank,onehand.cards[3].suit,onehand.cards[3].rank,onehand.cards[4].suit,onehand.cards[4].rank)) 
                        await message.channel.send("%d만큼의 금전의 변화가 있어요!"%(earned-cost))
                    else:
                        await message.channel.send("%d번째 시행에서 %s님의 예측: %d, 실제: %d"%(x,message_author.nick,chosen,chsed))
    except:
        await message.channel.send("뭔가 문제가 발생했습니다")
        pass
    if message_content == '!포커설명':
        await message.channel.send("5장의 카드 조합으로 나오는 포커 족보를 맞추면 배당률에 따라 다시 돌려받는 게임이다\n 명령어:(점 무시) !.포커도박 [걸 금액] [0~8:노페어(1.5),원페어(),투페어,트리플,스트레이트,플러시,풀하우스,포카드,스트레이트 플러시] [반복횟수]")
    if message_content == '!안녕':
        await message.channel.send("어 그래 안녕!")
    if message_content == '!집합':
        await message.channel.send("@everyone")
    if message_content == '!집합도배' and message_author.nick == '김동언':
        for i in range(100):
            await message.channel.send("%d번 남음: @everyone"%(100-i))
    try:
        if '!검열신청' in message_content and not message_content.split()[1] in Censor_object and not message_author.bot: 
            Censor_object_minor.append(message_content.split()[1])
            await message.channel.send("<현재 검열 대기 대상>")
            await message.channel.send(Censor_object_minor)
            print(Censor_object_minor)
    except:
        pass
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    latency = bot.latency
    await ctx.send('pong! {}ms'.format(latency*1000))

bot.run(token)