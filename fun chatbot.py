import random
import json
import requests
from datetime import datetime

class EmotionalChatbot:
    def __init__(self):
        self.name = "FunBot"
        self.mood = "happy"
        self.convhistory = []
        self.user_mood = "neutral"

        self.sad_words = ["sad", "unhappy", "depressed", "crying", "hurt", "upset"]
        self.happy_words =["happy", "joyful", "exicted", "glad", "cheerful", "great","good","awesome"]
        self.angry_words = ["angry", "mad", "furious", "hate", "annoyed", "irritated", "frustrated", "pissed" ]

        self.fallback_jokes = ["why don't scientists trust atoms? Because they make up everything!",
                               "Why did the scarecrow win an award? Because he was outstanding in his field!",  
                               "Why don't eggs tell jokes? They'd crack each other up!"] 
        
        self.fallback_facts = [
            "Honey never spoils. Archaeologists have found 3000-year-old honey that's still edible!",
            "Octopuses have three hearts and blue blood!",
            "A day on Venus is longer than a year on Venus!",
            "Bananas are berries, but strawberries aren't!",
            "The shortest war in history was between Britain and Zanzibar in 1896 and lasted only 38 minutes!"]
    
    def get_joke(self):
        apis =["https://official-joke-api.appspot.com/random_joke",
            "https://v2.jokeapi.dev/joke/Any?type=single",
            "https://icanhazdadjoke.com/"]
        
        for api_url in apis:
            try:
                headers ={"Accept":"application/json"} if "icanhazdadjoke" in api_url else {}
                response = requests.get(api_url, headers=headers, timeout=5)

                if response.status_code ==200:
                    data = response.json()

                    if "icanhazdadjoke" in api_url:
                        return data["joke"]
                    elif "official-joke-api" in api_url:
                        return f"{data["setup"]} - {data["punchline"]}"
                    elif "jokeapi" in api_url:
                        return data["joke"] if "joke" in data else f"{data.get("setup","")} - { data.get("delivery", "")}"
            except requests.RequestException:
                continue  
        return random.choice(self.fallback_jokes)     #incase APIS fail
    def get_fact(self):
        facts= [
            "https://uselessfacts.jsph.pl/api/v2/facts/random",
            "https://catfact.ninja/fact",
            "https://dog-api.kinduff.com/api/facts"
        ]
        for api_url in facts:
            try:
                headers={"Accept":"application/json"} if "uselessfacts" in api_url else{}
                response = requests.get(api_url, headers=headers, timeout=5)
                if response.status_code==200:
                    data = response.json()

                    if "uselessfacts" in api_url:
                        return f"🤯{data["text"]}"
                    elif "catfact" in api_url:
                        return f"🐱{data["text"]}"
                    elif "dog-api" in api_url:
                        return f"🐶{data["text"][0]}"
            except requests.RequestException:
                continue
        
        try:
            number = random.randint(1,1000)
            response = requests.get(f"http://numbersapi.com/{number}/trivia", timeout=5)
            if response.status_code == 200:
                return f"🔢{response.text}"
        except:
            pass
        

        return f"📚 {random.choice (self.fallback_facts)}"
    def know_emotion(self,text):
        text_lower=text.lower()

        sad_idn = sum(1 for word in self.sad_words if word in text_lower)
        happy_idn = sum(1 for word in self.happy_words if word in text_lower)
        angry_idn = sum(1 for word in self.angry_words if word in text_lower)

        if sad_idn > happy_idn and sad_idn > angry_idn:
            return "sad"
        elif happy_idn >sad_idn and happy_idn>angry_idn:
            return "happy"
        elif angry_idn >sad_idn and angry_idn>happy_idn:
            return "angry"
        else:
            return "neutral"

    def get_replies(self, user_input):
        self.user_mood = self.know_emotion(user_input)

        self.convhistory.append({
            "user":user_input,
            "bot":"",
            "mood":self.user_mood,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

        if any(cmd in user_input.lower() for cmd  in ["joke", "tell me a joke", "make me laugh"]):
            
            joke = self.get_joke()
            return f"😂😂🤣😂{joke}😂🤣😂🤣"
        
        elif any(cmd in user_input.lower()for cmd in ["fact","tell me a fact","tell me something interesting"]):

            fact = self.get_fact()
            return f"👽{fact}"
        
        
        emotional_replies = {
            "sad": [
                "I'm sorry you're feeling down. Would you like to hear a joke or a fun fact to cheer you up?",
                "It's okay to feel sad sometimes. Remember, this too shall pass! 🌈",
                "I'm here for you. Sometimes learning something new can help shift our perspective!"
            ],
            "happy": [
                "It's wonderful to see you so happy! Your joy is contagious! 😊",
                "Great to see you in such a good mood! Want to celebrate with a fun fact?",
                "Your happiness brightens the conversation! 🌟"
            ],
            "angry": [
                "I sense some frustration. Take a deep breath - you've got this! 💪",
                "It's okay to feel angry sometimes. How about we channel that energy into learning something new?",
                "Let's take a moment to breathe together. In... and out..."
            ],
            "neutral": [
                "How's your day going?",
                "What would you like to talk about?",
                "Ready for some interesting conversation?"
            ]
        }

        replies = random.choice(emotional_replies[self.user_mood])

        if random.random() < 0.3:
            if random.choice([True,False]):
                replies += f"\n\nlet me tell you a joke to lighten up you day: {self.get_joke()}"
            else:
                replies += f"\n\nHere is something interestion informantion for you: {self.get_fact()}"

        return replies
    
    def start_bot(self):
        print(f"🤖 Hello! I'm {self.name}!")
        print("I can sense your mood and chat with you!")
        print("Special commands: 'joke', 'fact', 'exit'")
        print("Type 'exit' to end the conversation\n")

        while True:
            user_input = input("You: ")

            if user_input.lower() == "exit":
                print ("🤖 Goodbye! Take care!")
                break
            replies = self.get_replies(user_input)
            if self.convhistory:

                self.convhistory[-1]["bot"]=replies
            print(f"🤖 {self.name}: {replies}\n")

if __name__ =="__main__":
    bot =EmotionalChatbot()
    bot.start_bot()