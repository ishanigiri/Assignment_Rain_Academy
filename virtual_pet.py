import random
import pickle
import time
import threading

class Pet:
    def __init__(self, name):
        self.name = name
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.consecutive_high_stats = 0

    def feed(self, value):
        self.hunger = min(self.hunger + value, 100)
        print(f"{self.name} has been fed! Hunger increased to {self.hunger}.")
    
    def play(self, value):
        if self.energy >= value:
            self.happiness = min(self.happiness + value, 100)
            self.energy = max(self.energy - value, 0)
            print(f"{self.name} played! Happiness increased to {self.happiness}, Energy decreased to {self.energy}.")
        else:
            print(f"{self.name} is too tired to play. Consider resting.")

    def rest(self, value):
        self.energy = min(self.energy + value, 100)
        self.hunger = max(self.hunger - (value // 4), 0)
        print(f"{self.name} rested! Energy increased to {self.energy}, Hunger decreased to {self.hunger}.")

    def display_stats(self):
        print(f"\n{self.name}'s Stats:")
        print(f"Hunger: {self.hunger}")
        print(f"Happiness: {self.happiness}")
        print(f"Energy: {self.energy}")

    def check_status(self):
        hunger_status = "Above 80" if self.hunger > 80 else "Below 0"
        happiness_status = "Above 80" if self.happiness > 80 else "Below 0"
        energy_status = "Above 80" if self.energy > 80 else "Below 0"

        print(f"\n{self.name}'s Status: ")
        print(f"Hunger: {hunger_status}")
        print(f"Happiness: {happiness_status}")
        print(f"Energy: {energy_status}")

        if self.hunger > 80 and self.happiness > 80 and self.energy > 80:
            print(f"Oh yaay! {self.name} has Win. Game over!")
            return "sick"

        if self.hunger <= 0 or self.happiness <= 0 or self.energy <= 0:
            self.consecutive_high_stats += 3
        else:
            self.consecutive_high_stats = 0

        if self.consecutive_high_stats >= 1:
            print(f"ohh no! {self.name} is sick low stats. You loose, game over!")
            return "win"

        return "continue"

    def random_event(self):
        event = random.choice(["find_toy", "get_sick", "nothing", "restful_day"])
        
        if event == "find_toy":
            happiness_boost = random.randint(10, 20)
            self.happiness = min(self.happiness + happiness_boost, 100)
            print(f"{self.name} found a toy! Happiness increased by {happiness_boost}!")
        
        elif event == "get_sick":
            happiness_drop = random.randint(5, 15)
            self.happiness = max(self.happiness - happiness_drop, 0)
            print(f"{self.name} got sick! Happiness decreased by {happiness_drop}.")
        
        elif event == "restful_day":
            energy_boost = random.randint(5, 10)
            self.energy = min(self.energy + energy_boost, 100)
            print(f"{self.name} had a restful day! Energy increased by {energy_boost}.")
        
        # 'nothing' means no event happened

    def save_game(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.__dict__, f)
        print(f"Game saved for {self.name}.")

    @classmethod
    def load_game(cls, filename):
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
            pet = cls(data['name'])
            pet.__dict__.update(data)
            print(f"Game loaded for {pet.name}.")
            return pet
        except FileNotFoundError:
            print("No saved game found.")
            return None

# Timer function for user input
def timed_input(prompt, timeout):
    print(prompt)
    timer = threading.Timer(timeout, print, args=["\nTime's up! Action will be taken."])
    timer.start()
    try:
        user_input = input(f"(You have {timeout} seconds to respond): ")
    except TimeoutError:
        user_input = None
    timer.cancel()
    return user_input

# Main program
def main():
    print("Welcome to the Virtual Pet Game!")

    choice = timed_input("Would you like to load a saved game? (y/n): ", 10)
    if choice == "y":
        pet = Pet.load_game('saved_game.pkl')
        if not pet:
            pet_name = input("Enter the name of your new pet: ")
            pet = Pet(pet_name)
    else:
        pet_name = input("What would you like to name your pet? ")
        pet = Pet(pet_name)

    print(f"\nCongratulations! You have a new pet named {pet.name}.")

    while True:
        pet.display_stats()

        print("What would you like to do?")
        print("1. Feed")
        print("2. Play")
        print("3. Rest")
        print("4. Save")
        print("5. Quit")

        choice = timed_input("Enter your choice: ", 15)
        if choice == "1":
            value = int(input("Enter the amount of food to feed: "))
            pet.feed(value)
        elif choice == "2":
            value = int(input("Enter the amount of energy to use for playing: "))
            pet.play(value)
        elif choice == "3":
            value = int(input("Enter the amount of energy to restore by resting: "))
            pet.rest(value)
        elif choice == "4":
            pet.save_game('saved_game.pkl')
        elif choice == "5":
            print(f"Goodbye! Take care of {pet.name}!")
            break
        else:
            print("Invalid choice. Please select again.")

        pet.random_event()

        status = pet.check_status()
        if status in ("sick", "win"):
            break


if __name__ == "__main__":
    main()
