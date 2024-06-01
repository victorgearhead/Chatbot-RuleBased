import pandas as pd
import re

# Load data
data = pd.read_csv('games-features.csv')

class RuleBot:
    negative_res = ("no", "nope", "nah", "naw", "not a chance", "sorry", "no thanks")
    exit_commands = ("quit", "exit", "goodbye", "bye", "later", "thank you")

    random_question = "Please specify more or elaborate, maybe like name or genre or category"

    def __init__(self):
        self.gamebabble = {
            'search_for_free': r'free',
            'search_for_paid': r'paid',
            'search_for_subscription': r'subscription',
            'search_for_mac': r'mac',
            'search_for_linux': r'linux',
            'search_for_windows': r'windows',
            'search_by_type': r'singleplayer|multiplayer|coop|mmo|vr|nongame|indie|action|adventure|casual|strategy|rpg|simulation|freetoplay|sports|racing',
            'details': r'details|information|what is|what|tell me about'
        }
        self.type_of_game = None
        self.list = data
    
    def greet(self):
        will_help = input("Hi, I am a Game Recommendation Assistant. I can recommend a game or give details about it. Would you like some help?\n").lower()
        if will_help in self.negative_res:
            print("Have a Nice Play!")
            return 
        self.chat()
    
    def make_exit(self, reply):
        if reply.lower() in self.exit_commands:
            print("Have a Nice Play!")
            return True
        return False

    def chat(self):
        reply = input("What type of game are you looking for?\n").lower()
        self.type_of_game = reply
        while not self.make_exit(reply):
            if not self.match_reply(reply):
                break
    
    def match_reply(self, reply):
        for intent, regex_pattern in self.gamebabble.items():
            if re.search(regex_pattern, reply):
                if intent == 'search_for_free':
                    return self.search_for_free()
                elif intent == 'search_for_subscription':
                    return self.search_for_subscription()
                elif intent == 'search_for_paid':
                    return self.search_for_paid()
                elif intent == 'search_for_mac':
                    return self.search_for_mac()
                elif intent == 'search_for_linux':
                    return self.search_for_linux()
                elif intent == 'search_for_windows':
                    return self.search_for_windows()
                elif intent == 'search_by_type':
                    return self.search_for_type(reply)
                elif intent == 'details':
                    return self.give_details()
        
        return self.no_match_intent()
    
    def filter_games(self, column_name, value=True):
        normalized_values = self.list[column_name].astype(str).str.lower()
        return self.list[normalized_values == str(value).lower()]

    def search_for_paid(self):
        self.list = self.filter_games('PurchaseAvail', 'true')
        self.display_games()
        return self.ask_for_more_features()
    
    def search_for_free(self):
        self.list = self.filter_games('IsFree', 'true')
        self.display_games()
        return self.ask_for_more_features()
    
    def search_for_subscription(self):
        self.list = self.filter_games('SubscriptionAvail', 'true')
        self.display_games()
        return self.ask_for_more_features()
    
    def search_for_mac(self):
        self.list = self.filter_games('PlatformMac', 'true')
        self.display_games()
        return self.ask_for_more_features()
    
    def search_for_windows(self):
        self.list = self.filter_games('PlatformWindows', 'true')
        self.display_games()
        return self.ask_for_more_features()
    
    def search_for_linux(self):
        self.list = self.filter_games('PlatformLinux', 'true')
        self.display_games()
        return self.ask_for_more_features()
    
    def give_details(self):
        iname = input("Please provide the game name:\n").strip().lower()
        game_details = self.list[self.list['Game'].str.lower() == iname]
        if not game_details.empty:
            print('Here is the description:')
            print(game_details['DetailedDescrip'].values[0])
            print("Price:")
            print(game_details['PriceInitial'].values[0])
        else:
            print("Sorry, I couldn't find the game you're looking for.")
        return self.ask_for_more_features()
    
    def search_for_type(self, type):
        type_game = {
            'singleplayer': 'SinglePlayer',
            'multiplayer': 'Multiplayer',
            'coop': 'Cooperative',
            'mmo': 'MMO',
            'vr': 'VRSupport',
            'nongame': 'NonGame',
            'action': 'Action',
            'adventure': 'Adventure',
            'casual': 'Casual',
            'strategy': 'Strategy',
            'rpg': 'RPG',
            'simulation': 'Simulation',
            'freetoplay': 'FreeToPlay',
            'sports': 'Sports',
            'racing': 'Racing',
            'indie': 'Indie'
        }
        for key, column_name in type_game.items():
            if re.search(key, type):
                self.list = self.filter_games(column_name, 'true')
                self.display_games()
                break
        return self.ask_for_more_features()

    def ask_for_more_features(self):
        say = input("Would you like to add any other features or filters?\n").strip().lower()
        if say in self.negative_res:
            print("Have a Nice Play!")
            return False
        else:
            self.match_reply(say)
            return True

    def display_games(self):
        if not self.list.empty:
            print('Here are the games:')
            print(self.list[['Game', 'PriceInitial']])
        else:
            print('No games found matching the criteria.')

    def no_match_intent(self):
        print(self.random_question)
        return False

# Create an instance of the bot and start the conversation
bot = RuleBot()
bot.greet()
