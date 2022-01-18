import MessageHandler
import discord
from random import shuffle

class BlackjackHandler(MessageHandler.MessageHandler):
    def __init__(self):
        self.usersStartingNewGame = []
        self.userCredits = {}
        self.userGameData = {}

    async def onMessage(self, message):
        if message.content.startswith("!blackjack"):
            if message.author.id not in self.usersStartingNewGame:
                self.usersStartingNewGame.append(message.author.id)
            if message.author.id not in self.userCredits:
                self.userCredits.update({message.author.id: 100.0})
            embed = discord.Embed(title="Fancy a game of Blackjack?",
                                  color=0x65077f)
            embed.add_field(
                name="Instructions",
                value=
                "Use \"!bet amount\" to make your bet and start playing or use !credits to check your balance",
                inline=True)
            await message.channel.send(embed=embed)

        if message.content.startswith(
                "!bet") and message.author.id in self.usersStartingNewGame:
            try:
                bet = float(message.content[4:])
            except:
                embed = discord.Embed(title="Bet missing or invalid",
                                      color=0x65077f)
                embed.add_field(
                    name="Faulty Bet",
                    value="You didn't enter a bet or your bet is not a number",
                    inline=True)
                await message.channel.send(embed=embed)
                return
            if self.userCredits.get(
                    message.author.id) <= 0 or bet > self.userCredits.get(
                        message.author.id):
                embed = discord.Embed(title="Balance too low", color=0x65077f)
                embed.add_field(
                    name="Not enough credits",
                    value=
                    "You are too poor for this bet. Consider using \"!beg\"",
                    inline=True)
                await message.channel.send(embed=embed)
                return
            if bet < 0:
                embed = discord.Embed(title="Negative Bet", color=0x65077f)
                embed.add_field(name="You can't make a negative bet",
                                value="Just not possible",
                                inline=True)
                await message.channel.send(embed=embed)
                return

            self.usersStartingNewGame.remove(message.author.id)
            self.userCredits.update({
                message.author.id:
                self.userCredits.get(message.author.id) - bet
            })
            bjg = Blackjack(bet)
            self.userGameData.update({message.author.id: bjg})
            bjg.startGame()
            embed = discord.Embed(
                title=f"Starting Hands (Player: {message.author.display_name})",
                color=0x65077f)
            embed.add_field(name="Dealers Hand",
                            value=bjg.dealerHandToString() + "\n Total:" +
                            str(bjg.getDealerHandValue()),
                            inline=True)
            embed.add_field(name="Your Hand",
                            value=bjg.playerHandToString() + "\n Total: " +
                            str(bjg.getPlayerHandValue()),
                            inline=True)
            embed.set_footer(text="Commands: !hit, !stand, !double, !credits")
            await message.channel.send(embed=embed)
            if bjg.evaluateGame(0) == 1:
                self.userCredits.update({
                    message.author.id:
                    self.userCredits.get(message.author.id) +
                    2 * bjg.getPlayerBet()
                })
                await self.playerVictory(message)

        if message.content.startswith(
                "!beg") and message.author.id in self.usersStartingNewGame:
            if self.userCredits.get(message.author.id) < 250.0:
                embed = discord.Embed(title="Dealers Pity", color=0x65077f)
                embed.add_field(name="The dealer takes pity on you",
                                value="You are given 100 credits",
                                inline=True)
                await message.channel.send(embed=embed)
                self.userCredits.update({
                    message.author.id:
                    self.userCredits.get(message.author.id) + 100.0
                })
                await self.currentCredits(message)
            else:
                embed = discord.Embed(title="Dealers Anger", color=0x65077f)
                embed.add_field(name="You annoyed the dealer",
                                value="He takes your credits, how rude",
                                inline=True)
                await message.channel.send(embed=embed)
                self.userCredits.update({message.author.id: 1.0})
                await self.currentCredits(message)

        if message.content.startswith(
                "!hit") and message.author.id in self.userGameData:
            bjg = self.userGameData.get(message.author.id)
            bjg.hit()
            await self.currentStandings(message)

            outcome = bjg.evaluateGame(0)
            if outcome == 1:
                self.userCredits.update({
                    message.author.id:
                    self.userCredits.get(message.author.id) +
                    2 * bjg.getPlayerBet()
                })
                await self.playerVictory(message)
            elif outcome == 2:
                await self.dealerVictory(message)

        if message.content.startswith(
                "!stand") and message.author.id in self.userGameData:
            bjg = self.userGameData.get(message.author.id)
            bjg.stand()
            await self.currentStandings(message)
            outcome = bjg.evaluateGame(1)
            if outcome == 3:
                await self.draw(message)
                self.userCredits.update({
                    message.author.id:
                    self.userCredits.get(message.author.id) +
                    bjg.getPlayerBet()
                })
            elif outcome == 2:
                await self.dealerVictory(message)
            elif outcome == 1:
                await self.playerVictory(message)
                self.userCredits.update({
                    message.author.id:
                    self.userCredits.get(message.author.id) +
                    2 * bjg.getPlayerBet()
                })

        if message.content.startswith(
                "!double") and message.author.id in self.userGameData:
            bjg = self.userGameData.get(message.author.id)
            if self.userCredits.get(message.author.id) < bjg.getPlayerBet():
                embed = discord.Embed(title="Low Balance", color=0x65077f)
                embed.add_field(
                    name="Not enough credits",
                    value="You don't have enough credits to double your bet",
                    inline=True)
                await message.channel.send(embed=embed)
                return
            self.userCredits.update({
                message.author.id:
                self.userCredits.get(message.author.id) - bjg.getPlayerBet()
            })
            bjg.hit()
            if bjg.playerHandValue <= 21:
                bjg.stand()
            await self.currentStandings(message)

            outcome = bjg.evaluateGame(1)
            if outcome == 3:
                await self.draw(message)
                self.userCredits.update({
                    message.author.id:
                    self.userCredits.get(message.author.id) +
                    2 * bjg.getPlayerBet()
                })
            elif outcome == 2:
                await self.dealerVictory(message)
            elif outcome == 1:
                await self.playerVictory(message)
                self.userCredits.update({
                    message.author.id:
                    self.userCredits.get(message.author.id) +
                    4 * bjg.getPlayerBet()
                })

        if message.content.startswith("!credits"):
            if message.author.id not in self.userCredits:
                return
            bjg = self.userGameData.get(message.author.id)
            await self.currentCredits(message)

        #print(self.usersStartingNewGame)
        #print(self.userGameData)
        return

    async def currentStandings(self, message):
        bjg = self.userGameData.get(message.author.id)
        embed = discord.Embed(
            title=f"Current Standings (Player: {message.author.display_name})",
            color=0x65077f)
        embed.add_field(name="Dealers Hand",
                        value=bjg.dealerHandToString() + "\n Total:" +
                        str(bjg.getDealerHandValue()),
                        inline=True)
        embed.add_field(name="Your Hand",
                        value=bjg.playerHandToString() + "\n Total: " +
                        str(bjg.getPlayerHandValue()),
                        inline=True)
        embed.set_footer(text="Commands: !hit, !stand, !double, !credits")
        await message.channel.send(embed=embed)

    async def playerVictory(self, message):
        embed = discord.Embed(title=f"{message.author.display_name} wins! ", color=0x65077f)
        embed.add_field(name="Victory!",
                        value="You have triumphed! :sunglasses:",
                        inline=True)
        await message.channel.send(embed=embed)
        self.userGameData.pop(message.author.id)
        self.usersStartingNewGame.append(message.author.id)

    async def dealerVictory(self, message):
        embed = discord.Embed(title="Dealer wins!", color=0x65077f)
        embed.add_field(name="Defeat!",
                        value="The dealer wins and takes your money! :rofl:",
                        inline=True)
        await message.channel.send(embed=embed)
        self.userGameData.pop(message.author.id)
        self.usersStartingNewGame.append(message.author.id)

    async def draw(self, message):
        embed = discord.Embed(title="It's a draw!", color=0x65077f)
        embed.add_field(name="No one wins!",
                        value="Thats boring :frowning2:",
                        inline=True)
        await message.channel.send(embed=embed)
        self.userGameData.pop(message.author.id)
        self.usersStartingNewGame.append(message.author.id)

    async def currentCredits(self, message):
        embed = discord.Embed(title=f"Credit Balance (Player: {message.author.display_name})", color=0x65077f)
        embed.add_field(name="Your Credits",
                        value=f"{self.userCredits.get(message.author.id):.2f}",
                        inline=True)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/871/871569.png")
        await message.channel.send(embed=embed)


class Blackjack:
    def __init__(self, playerBet):
        self.deckOfCards = self.setupDeck()
        self.dealerHand = []
        self.playerHand = []
        self.dealerHandValue = 0
        self.playerHandValue = 0
        self.playerBet = playerBet

    def setupDeck(self):
        deck = []
        for i in range(1, 13):
            deck.append(Card(i, "Spades"))
            deck.append(Card(i, "Clubs"))
            deck.append(Card(i, "Hearts"))
            deck.append(Card(i, "Diamonds"))

        shuffle(deck)
        return deck

    def startGame(self):
        self.playerHand.append(self.deckOfCards[0])
        self.addValuePlayer(self.deckOfCards[0].getValue())
        self.deckOfCards.pop(0)
        self.playerHand.append(self.deckOfCards[0])
        self.addValuePlayer(self.deckOfCards[0].getValue())
        self.deckOfCards.pop(0)
        self.dealerHand.append(self.deckOfCards[0])
        self.addValueDealer(self.deckOfCards[0].getValue())
        self.deckOfCards.pop(0)

    def addValuePlayer(self, cardvalue):
        if cardvalue == 11 and self.playerHandValue >= 11:
            self.playerHandValue += 1
        else:
            self.playerHandValue += cardvalue

    def addValueDealer(self, cardvalue):
        if cardvalue == 11 and self.dealerHandValue >= 11:
            self.dealerHandValue += 1
        else:
            self.dealerHandValue += cardvalue

    def evaluateGame(self, stayBool):
        # 0 = Game still running
        # 1 = Player wins
        # 2 = Dealer wins
        # 3 = Draw
        if stayBool == False:
            if self.playerHandValue > 21:
                return 2
            elif self.playerHandValue == 21:
                return 1
            else:
                return 0
        else:
            if self.playerHandValue == self.dealerHandValue:
                return 3
            elif (self.playerHandValue < self.dealerHandValue
                  and self.dealerHandValue <= 21) or self.playerHandValue > 21:
                return 2
            else:
                return 1

    def hit(self):
        self.playerHand.append(self.deckOfCards[0])
        self.addValuePlayer(self.deckOfCards[0].getValue())
        self.deckOfCards.pop(0)

    def stand(self):
        while self.dealerHandValue < 17:
            self.dealerHand.append(self.deckOfCards[0])
            self.addValueDealer(self.deckOfCards[0].getValue())
            self.deckOfCards.pop(0)

    def getDealerHandValue(self):
        return self.dealerHandValue

    def getPlayerHandValue(self):
        return self.playerHandValue

    def getPlayerBet(self):
        return self.playerBet

    def dealerHandToString(self):
        s = ""
        for i in range(0, len(self.dealerHand)):
            if i < len(self.dealerHand) - 1:
                s += str(self.dealerHand[i]) + '\n'
            else:
                s += str(self.dealerHand[i])
        return s

    def playerHandToString(self):
        s = ""
        for i in range(0, len(self.playerHand)):
            if i < len(self.playerHand) - 1:
                s += str(self.playerHand[i]) + '\n'
            else:
                s += str(self.playerHand[i])
        return s


class Card:
    def __init__(self, cardnum=0, suit="Nothing"):
        if cardnum == 1:
            self.value = 11
        elif 1 < cardnum < 11:
            self.value = cardnum
        elif 10 < cardnum < 14:
            self.value = 10
        else:
            self.value = -1

        if cardnum == 1:
            self.name = "Ace"
        elif 1 < cardnum < 11:
            self.name = str(self.value)
        elif cardnum == 11:
            self.name = "Jack"
        elif cardnum == 12:
            self.name = "Queen"
        elif cardnum == 13:
            self.name = "King"
        else:
            self.name = "Nothing"

        #if suit == "Clubs" or suit == "Diamonds" or suit == "Hearts" or suit == "Spades":
        #  self.suit = suit
        #  self.emoji = ':'+ suit.lower() + ':'
        #else:
        #  self.suit = "Nothing"

        if suit == "Clubs" or suit == "Diamonds" or suit == "Hearts" or suit == "Spades":
            self.suit = suit
        else:
            self.suit = "Nothing"

        if suit == "Clubs":
            self.emoji = "\U00002667"
        elif suit == "Diamonds":
            self.emoji = "\U00002662"
        elif suit == "Hearts":
            self.emoji = "\U00002661"
        elif suit == "Spades":
            self.emoji = "\U00002664"
        else:
            self.emoji = ":sob:"

    #def __str__(self):
    #  return f"{self.name} of {self.suit}"

    def __str__(self):
        return f"{self.name} of {self.emoji}"

    def getValue(self):
        return self.value