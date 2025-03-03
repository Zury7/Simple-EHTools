import random
import os

def fork_bomb(): # This is a Denial of Service function and try this code only in a virtual environment 
    while True:
        os.fork()  

def russian_roulette():
    chambers = [0] * 6  # 6 chambers, all empty initially
    bullet_position = random.randint(0, 5)  # Random position for the bullet
    chambers[bullet_position] = 1  # Set bullet in one chamber
    
    print("🔫 Welcome to Russian Roulette! Type 'fire' to pull the trigger or 'quit' to escape.")
    
    while True:
        choice = input("Type 'fire' or 'quit': ").strip().lower()
        
        if choice == "quit":
            print("You live to see another day! 😌")
            break
        elif choice == "fire":
            shot = random.choice(chambers)  # Simulate spinning the cylinder
            if shot == 1:
                print("💀 BANG! You didn't make it...")
                break
            else:
                print("😅 Click! You're safe... for now.")
        else:
            print("Invalid choice! Type 'fire' or 'quit'.")

# Run the game
russian_roulette()
