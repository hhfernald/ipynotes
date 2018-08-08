import fnmatch
import glob
import os
import random
import shutil
import time

# Create a very large number of fake notes, to test how well IPyNotes
# bears up, and how well the filter works.

folders = {'animals': ['badger', 'bear', 'bison', 'camel', 'cat', 'cougar',
                       'cow', 'deer', 'dinosaur', 'dog', 'duck', 'eel',
                       'elephant', 'elk', 'flamingo', 'fox', 'frog', 'goat',
                       'gopher', 'goose', 'horse', 'jaguar', 'kangaroo', 'lion',
                       'lizard', 'mouse', 'otter', 'ox', 'penguin', 'pig',
                       'rabbit', 'rat', 'sheep', 'snake', 'spider', 'swan',
                       'tiger', 'turtle', 'weasel', 'wolf', 'yak', 'zebra'],
                       
           'continents': ['Africa', 'Antarctica', 'Asia', 'Australia',
                          'Europe', 'North America', 'South America'],
                          
           'planets': ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter',
                       'Saturn', 'Uranus', 'Neptune', 'Pluto'],
                       
           'zodiac': ['Aries', 'Taurus', 'Gemini', 'Cancer',
                      'Leo', 'Virgo', 'Libra', 'Scorpio',
                      'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'],
                      
           'months': ['January', 'February', 'March', 'April',
                      'May', 'June', 'July', 'August',
                      'September', 'October', 'November', 'December'],
                      
           'colors': ['red', 'orange', 'yellow', 'green', 'blue', 'purple',
                      'violet', 'magenta', 'black', 'brown', 'gray', 'silver',
                      'white', 'gold']}

sentences = ["A mad boxer shot a quick, gloved jab to the jaw of his dizzy"
             " opponent.",
             "A quart jar of oil mixed with zinc oxide makes a very bright"
             " paint.",
             "A quick movement of the enemy will jeopardize six gunboats.",
             "Amazingly few discotheques provide jukeboxes.",
             "Back in June we delivered oxygen equipment of the same size.",
             "Blowzy red vixens fight for a quick jump.",
             "Brawny gods just flocked up to quiz and vex him.",
             "Bright vixens jump; dozy fowl quack.",
             "By Jove, my quick study of lexicography won a prize.",
             "Crazy Frederick bought many very exquisite opal jewels.",
             "Ebenezer unexpectedly bagged two tranquil aardvarks with his"
             " jiffy vacuum cleaner.",
             "Few black taxis drive up major roads on quiet hazy nights.",
             "Few quips galvanized the mock jury box.",
             "Five hexing wizard bots jump quickly.",
             "Five or six big jet planes zoomed quickly by the tower.",
             "Forsaking monastic tradition, twelve jovial friars gave up"
             " their vocation for a questionable existence on the flying"
             " trapeze.",
             "Fred specialized in the job of making very quaint wax toys.",
             "Go, lazy fat vixen; be shrewd, jump quick.",
             "GQ jock wears vinyl tuxedo for showbiz promo.",
             "Grumpy wizards make a toxic brew for the jovial queen.",
             "Grumpy wizards make toxic brew for the evil queen and Jack.",
             "How quickly daft jumping zebras vex.",
             "Jack amazed a few girls by dropping the antique onyx vase!",
             "Jack quietly moved up front and seized the big ball of wax.",
             "Jackdaws love my big sphinx of quartz.",
             "Jaded zombies acted quaintly but kept driving their oxen"
             " forward.",
             "Jelly-like above the high wire, six quaking pachyderms kept the"
             " climax of the extravaganza in a dazzling state of flux.",
             "Jim quickly realized that the beautiful gowns are expensive.",
             "Jumpy halfling dwarves pick quartz box.",
             "Just keep examining every low bid quoted for zinc etchings.",
             "Just work for improved basic techniques to maximize your typing"
             " skill.",
             "Levi Lentz packed my bag with six quarts of juice.",
             "Mr. Jock, TV quiz PhD, bags few lynx.",
             "My ex pub quiz crowd gave joyful thanks.",
             "My faxed joke won a pager in the cable TV quiz show.",
             "My girl wove six dozen plaid jackets before she quit.",
             "No kidding: Lorenzo called off his trip to visit Mexico City"
             " just because they told him the conquistadores were extinct.",
             "Pack my box with five dozen liquor jugs.",
             "Pack my red box with five dozen quality jugs.",
             "Playing jazz vibe chords quickly excites my wife.",
             "Quick wafting zephyrs vex bold Jim.",
             "Schwarzkopf vexed Iraq big-time in July.",
             "Six big juicy steaks sizzled in a pan as five workmen left the"
             " quarry.",
             "Six crazy kings vowed to abolish my quite pitiful jousts.",
             "Sixty zippers were quickly picked from the woven jute bag.",
             "Sphinx of black quartz, judge my vow!",
             "Sympathizing would fix Quaker objectives.",
             "The explorer was frozen in his big kayak just after making queer"
             " discoveries.",
             "The five boxing wizards jump quickly.",
             "The job requires extra pluck and zeal from every young wage"
             " earner.",
             "The lazy major was fixing Cupid’s broken quiver.",
             "The public was amazed to view the quickness and dexterity of the"
             " juggler.",
             "The quick brown fox jumps over the lazy dog.",
             "The quick onyx goblin jumps over the lazy dwarf.",
             "The vixen jumped quickly on her foe barking with zeal.",
             "Then a cop quizzed Mick Jagger’s ex-wives briefly.",
             "Turgid saxophones blew over Mick's jazzy quaff.",
             "Two driven jocks help fax my big quiz.",
             "Vexed nymphs go for quick waltz job.",
             "Waltz, bad nymph, for quick jigs vex!",
             'Watch “Jeopardy!”, Alex Trebek’s fun TV quiz game.',
             "Waxy and quivering, jocks fumble the pizza.",
             "We promptly judged antique ivory buckles for the next prize.",
             "When zombies arrive, quickly fax judge Pat.",
             "Whenever the black fox jumped the squirrel gazed suspiciously.",
             "While making deep excavations we found some quaint bronze"
             " jewelry.",
             "Who packed five dozen old quart jugs in my box?",
             "Woven silk pyjamas exchanged for blue quartz.",
             ]

root = "fake_notes"
categories = list(folders)
sentence_counts = [2, 3, 4, 5]
file_count = 20000

# Create the files.

shutil.rmtree(root, ignore_errors=True)
for i in range(file_count):
    folder = random.choice(categories)
    subfolder = random.choice(folders[folder])
    folder_path = os.path.join(root, folder, subfolder)
    file_path = os.path.join(folder_path, str(i) + ".md")
    sentence_count = random.choice(sentence_counts)
    file_sentences = []
    for j in range(sentence_count):
        sentence = random.choice(sentences)
        file_sentences.append(sentence)
    os.makedirs(folder_path, exist_ok=True)
    with open(file_path, mode='w') as f:
        f.write(" ".join(file_sentences))

print("Wrote", "{:,}".format(file_count), "files.")

# See how fast the files can be searched.

print("Reloading file paths...")
start_time = int(round(time.time() * 1000))
files = []
for root, __, filenames in os.walk(root):
    for filename in fnmatch.filter(filenames, '*.md'):
        files.append(os.path.join(root, filename))
end_time = int(round(time.time() * 1000))
print("...took", end_time - start_time, "ms")

print("Searching files...")
terms = ['dozen', 'sphinx', 'vixens']
for term in terms:
    start_time = int(round(time.time() * 1000))
    
    file_count = 0
    for file in files:
        with open(file) as f:
            text = f.read()
        if term in text:
            file_count += 1

    end_time = int(round(time.time() * 1000))
    print("Files containing '" + term + "':", file_count)
    print("--- Search took", end_time - start_time, "ms")

print("Done.")

