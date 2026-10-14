dict={}
while True:
    print("dictonary management/n")
    print("1. Add a word")
    print("2. Search for meaning")
    print("3. Display all words")
    print("4. Update meaning")
    print("5. Delete word")
    print("6. Exit")

    choice=input("Enter your choice: ")

    if choice == "1":
        word=input("Enter the word: ").lower()
        meaning=input("Enter the meaning: ")
        dict[word]= meaning
        print("word added sucessfully!")

    elif choice == "2":
        word=input("Enter the word: ").lower()
        if word in dict:
            print("meaning:",dict[word])
        else:
            print("Word is not found in dictonary.")

    elif choice == "3":
        if dict:
            print("Words and their meanings/n")
            for word,meaning in dict.items():
                print(f"{word}={meaning}")
        else:
            print("Dictonary is empty.")

    elif choice == "4":
        word=input("enter the word to updated meaning: ").lower()
        if word in dict:
            new_mean=input("Enter the meaning: ")
            dict[word]=new_mean
            print("Meaning updated sucessfully!")
            print("Updated meaning:",dict[word])
        else:
            print("Word not found in dictonary.")
    elif choice == "5":
        word=input("enter the word: ").lower()
        if word in dict:
            del dict[word]
            print("Deleted the word sucessfully..!")
            print(f"dictonariy is {dict}")
        else:
            print("Word not found in dictonary.")

    elif choice == "6":
        print("Exited")
        break



