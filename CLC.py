import re
import os

def get_song_list(file_path):
    with open(file_path, 'r') as file:
        contents = file.read()

    song_list = re.findall(r"\s*\d+\.\s*(.+)", contents)
    return song_list

def check_duplicates(song_list, new_song):
    match = re.match(r"(.+) by (.+)", new_song)
    if match:
        song_name = match.group(1).strip()
        artist_name = match.group(2).strip()
    else:
        song_name = new_song.strip()
        artist_name = input("Enter the artist name, Example {03 greedo}: ").strip()
        new_song = f"{song_name} by {artist_name}"

    if new_song in song_list:
        print(f"{new_song} is already in the list.")
    else:
        print(f"{new_song} is not in the list.")
        choice = input("Do you want to add this song to the list? (yes/no): ")
        if choice.lower() == "yes":
            add_song(file_path, new_song)
            reformat_song_list(file_path)


def print_list(file_path, artist=None):
    song_list = get_song_list(file_path)

    if not song_list:
        print("No songs in the list.")
    else:
        grouped_songs = group_songs_by_artist(song_list)

        if artist:
            if artist in grouped_songs:
                print(f"\n\t{artist}")
                for i, song in enumerate(grouped_songs[artist], start=1):
                    print(f"\t{i}. {song}")
            else:
                print(f"No songs found for the artist '{artist}'.")
        else:
            print("\nSong List:")
            for artist, songs in grouped_songs.items():
                print(f"\n\t{artist}")
                for i, song in enumerate(songs, start=1):
                    print(f"\t{i}. {song}")
            print("\nSUMMARY:")
            total_songs = 0
            for artist, songs in grouped_songs.items():
                artist_total = len(songs)
                print(f"{artist}: {artist_total}")
                total_songs += artist_total
            print(f"Overall total songs: {total_songs}")

def add_song(file_path, song):
    # Extract the song name and artist name
    match = re.match(r"(.+) by (.+)", song)
    if match:
        song_name = match.group(1).strip()
        artist_name = match.group(2).strip()
    else:
        song_name = song.strip()
        artist_name = input("Enter the artist name (enter 'unknown' if unknown): ").strip()
        if artist_name == "":
            artist_name = "unknown"

    # Check if either the song name or artist name is blank
    if song_name == "" or artist_name == "":
        print("Song name and artist name cannot be blank.")
    else:
        new_song = f"{song_name} by {artist_name}"
        with open(file_path, 'a') as file:
            file.write(f"\n 1.{new_song}")
        print("Song added successfully.")


def set_target_list():
    file_path = input("Enter the path of the target list file: ")
    song_list = get_song_list(file_path)
    return file_path, song_list

def test_get_song_list():
    # Create a sample playlist file
    file_path = "test_playlist.md"
    with open(file_path, 'w') as file:
        file.write("KILLSTATION\n")
        file.write("\t1. vengence by killstation\n")
        file.write("\t2. oxytoca by killstation\n")
        file.write("\t3. always here you and i by killstation\n")
        file.write("\t4. opal by killstation\n")
        file.write("\t5. cement by killstation\n")
        file.write("\t6. mud by killstation\n")
        file.write("XXXTENTACION\n")
        file.write("\t1. uh oh thots by xxxtentacion\n")
        file.write("\t2. i spoke to the devil in miami he said everything would be fine by xxxtentacion\n")
        file.write("\t3. carry on by xxxtentacion\n")
        file.write("\t4. save me by xxxtentacion\n")
        file.write("\t5. ok shorty by xxxtentacion\n")
        file.write("\t6. ugly by xxxtentacion\n")
        file.write("\t7. face it by xxxtentacion\n")
        file.write("\t8. a ghetto christmas carol by xxxtentacion\n")
        file.write("\t9. whoa mind in awe by xxxtentacion\n")

    # Call the get_song_list function
    song_list = get_song_list(file_path)

    # Print the song list
    print("\nSong List:")
    print_list(file_path)

    # Verify the returned song list
    expected_song_list = [
        "vengence by killstation",
        "oxytoca by killstation",
        "always here you and i by killstation",
        "opal by killstation",
        "cement by killstation",
        "mud by killstation",
        "uh oh thots by xxxtentacion",
        "i spoke to the devil in miami he said everything would be fine by xxxtentacion",
        "carry on by xxxtentacion",
        "save me by xxxtentacion",
        "ok shorty by xxxtentacion",
        "ugly by xxxtentacion",
        "face it by xxxtentacion",
        "a ghetto christmas carol by xxxtentacion",
        "whoa mind in awe by xxxtentacion"
    ]
    assert song_list == expected_song_list

    # Cleanup: Delete the sample playlist file
    os.remove(file_path)
    print("\nget_song_list test passed.")

def group_songs_by_artist(song_list):
    grouped_songs = {}
    current_artist = None

    for song in song_list:
        match = re.match(r"(.+) by (.+)", song)
        if match:
            artist = match.group(2).strip()
            if artist != current_artist:
                grouped_songs[artist] = []
                current_artist = artist
            grouped_songs[artist].append(match.group(1).strip())

    return grouped_songs

def reformat_song_list(file_path):
    song_list = get_song_list(file_path)
    if not song_list:
        print("No songs in the list.")
        return

    # Sort the song list alphabetically by artist
    song_list.sort(key=lambda song: re.match(r".+ by (.+)", song).group(1))

    # Rewrite the file with the reformatted song list
    with open(file_path, 'w') as file:
        for i, song in enumerate(song_list, start=1):
            file.write(f"{i}. {song}\n")

    print("Song list reformatted successfully.")




# Example usage
file_path = "playlist.md"
song_list = get_song_list(file_path)

while True:
    print("   -----WELCOME TO CLC-----")
    print("      --Check List Cat-- ")
    print("\nOptions:")
    print("-- find -------- Check a song in the list --")
    print("-- list -------- Print the existing list ---")
    print("-- set list ---- Set a target list ---------")
    print("-- test -------- Test get_song_list --------")
    print("-- add --------- add a song to the list ----")
    print("-- reformat ---- reformat selected list ----")
    print("-- help -------- show help menu ------------")
    print("-- end --------- exit ----------------------")
    choice = input("Enter your choice: ")

    if choice == "find":
        new_song = input("Enter a new song name, Example {never bend}: ")
        check_duplicates(song_list, new_song)
    elif choice == "list":
        artist = input("Enter the artist name (leave blank for all artists): ")
        print_list(file_path, artist)
    elif choice == "set list":
        file_path, song_list = set_target_list()
        print("NEW LIST SET")
    elif choice == "test":
        test_get_song_list()
    elif choice == "add":
        new_song = input("Enter a new song name: ")
        artist = input("Enter the artist name: ")
        song = f"{new_song} by {artist}"
        add_song(file_path, song)
        song_list = get_song_list(file_path)
        print("Song added successfully.")
        reformat_song_list(file_path)

    elif choice.lower() == "reformat":
        reformat_song_list(file_path)
    elif choice.lower() == "help":
        print("\n--- Help ---")
        print("\n--- Summary ---")
        print("Introducing Check List Cat (CLC.py), your trusty feline companion in managing your song lists with a touch of humor and a whole lot of functionality.") 
        print("CLC.py is here to save the day and make organizing your playlists a breeze!")
        print("Check List Cat (CLC.py) is not your ordinary song list manager.")
        print("It's a clever tool designed to bring joy and efficiency to game developers and music enthusiasts alike. With its playful nature and powerful features, CLC.py will have you purring with delight as you effortlessly manage your song collections.")
        print("This script, lovingly named Check List Cat (CLC.py), allows you to wrangle your extensive song lists with ease.")
        print("Whether you're a game developer seeking to maintain a vast library of in-game music or a music enthusiast looking to organize your personal playlists, CLC.py has got you covered.")
        print("It works seamlessly with text files and even supports Markdown (.md) file format, making it versatile for your needs.")
        print("Imagine having Check List Cat (CLC.py) by your side, helping you keep track of your songs and reducing those pesky data entry errors.")
        print("Its purpose? To provide a reliable and convenient solution for managing long playlists, while adding a dash of whimsy to your music management tasks.")
        print("The delightful features of Check List Cat (CLC.py) include the ability to effortlessly view, print, and filter your song list by artist.")
        print("Whether you're searching for songs from a specific artist or creating artist-specific playlists, CLC.py makes it a breeze.")
        print("It also includes a 'Check a song in the list' feature, allowing you to quickly verify if a song is already included in the list, preventing those accidental duplicates.")
        print("Furthermore, Check List Cat (CLC.py) lets you set a target list, enabling you to work with different song collections or switch between projects seamlessly.")
        print("It's all about flexibility and simplicity when it comes to managing your songs.")
        print("So, embrace the charm and functionality of Check List Cat (CLC.py), your ultimate companion in managing your song lists.")
        print("Let CLC.py take the lead, so you can focus on what truly matters ")
        print("creating unforgettable gaming experiences or curating the perfect music playlists.")
        print("Get ready to purrfect your song list management with Check List Cat (CLC.py)!")
        print("PS. check out my website @ therealoz.tech ")
        print("\n--- Commands ---")
        print("- find - Check a song in the list:")
        print("   - Verify if a song is already in the list.")
        print("   - Enter the name of the song and the artist separately.")
        print("   - If song is not found you'll be prompted to add it.")
        print("- list - Print the existing list:")
        print("   - Display the entire song list or filter by an artist.")
        print("   - If an artist name is provided, only songs by that artist will be shown.")
        print("- set list - Set a target list:")
        print("   - Specify a different file as the target song list. Needed to work if your playlist isnt saved as playlist.md in the same directory as script")
        print("   - Enter the path of the target list file if not in the same directory")
        print("- test - Test get_song_list:")
        print("   - Run a test to verify the functionality of the get_song_list function.")
        print("- add - Add a song to the list:")
        print("   - Append a new song to the existing song list.")
        print("   - Enter the name of the song and the artist separately.")
        print("   - automatically reformats list.")
        print("- reformat - Reformat the song list:")
        print("   - Rearrange the song list to ensure it is properly organized and functioning.")
        print("   - This function sorts the song list alphabetically by artist name and updates the song numbers accordingly.")
        print("   - Use this option if you want to reorganize the song list and update the file manually this function is called at the end of every add.")
        print("- help -")
        print("   - Display this help message.")
    elif choice.lower() == "end":
        break
    else:
        print("Invalid choice. Please try again.")
