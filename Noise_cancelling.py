print("Project Idea - Noise Cancelling Headphones")
print("This project will use a microphone to pick up ambient noise and then generate an opposite sound wave to cancel out the noise. The user will be able to adjust the volume of the noise cancelling effect using a potentiometer.")

while True:
    print("\nWelcome to the Active Noise Cancellation Simulator!")
    print("This program simulates the functionality of noise cancelling headphones.")
    print("You can record a new audio file, load an existing audio file, apply noise cancelling effect, adjust volume, and view the frequency spectrum of the audio file.")
    print("Choose what action you'd like to run")
    print("1. Record new Audio File")
    print("2. Load existing Audio File")
    print("3. Apply noise cancelling effect to audio file")
    print("4. Adjust volume of noise cancelling effect")
    print("5. Show frequency spectrum of audio file")

    user_input = input("Please input your choice (1-5): ")

    if user_input == "1":
    print("Recording new audio file...")
    # Code to record new audio file goes here
    elif user_input == "2":
    print("Loading existing audio file...")
    # Code to load existing audio file goes here
    elif user_input == "3":
    print("Applying noise cancelling effect to audio file...")
    # Code to apply noise cancelling effect goes here
    elif user_input == "4":
    print("Adjusting volume of noise cancelling effect...")
    # Code to adjust volume of noise cancelling effect goes here
    elif user_input == "5":
    print("Showing frequency spectrum of audio file...")
    # Code to show frequency spectrum goes here
    else:
    print("Invalid input. Please choose a number between 1 and 5.")

    cont = input("\nWould you like to process another file? Enter Y for Yes or N for No: ").strip().upper()
    if cont == "N":
        print("\nExiting Active Noise Cancellation Simulator. Thank you!")
         break