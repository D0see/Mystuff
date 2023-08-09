
import random
import csv

rules = """In this game, all players receive the same word, except for Mr. White, who receives no words, and the imposters, who get a slightly different one.

During each turn, each player will say only one word in the order generated.

The goal is to convince everyone else that you have the correct word without giving away too much information that might help the imposters.

After each turn, there will be a discussion, and the group will vote to eliminate the most suspicious player.

If Mr. White is voted out, he still has a chance to win by correctly guessing the word.

The imposters can only win by ending up alone with a civilian.

The civilians must eliminate both the imposters and Mr. White. If, after a vote, only one civilian remains, they are also eliminated from the game.
"""
civ_eliminated = []
imp_eliminated = []
scoreboard = {}

def clear(): 
  print("\n"* 50)

def print_scoreboard():
  print("\n")
  print(scoreboard)
  print("\n")
  
def role_selection(number_of_players):
  role_list=[]
  for players in range(number_of_players):
    role_list.append("Civilian")
    
  number_of_imposters = 1 + round(number_of_players//3.5)#formerly 2 + round(player//7)
  imposters_index = random.sample(range(number_of_players),number_of_imposters)
  role_list[imposters_index[0]] = "Mr White"
  
  for indices in imposters_index:
    if imposters_index.index(indices) > 0:
      role_list[indices] = "Imposter"
  return role_list

def words_generator():
  the_words = []
  list1 = ["Cat", "Skateboard", "Tabacco"]
  list2 = ["Dog", "RollerBlades", "Marijuana"]
  
  with open("File.csv", "r") as bigwordslist :#csv containing words : row == word1,word2
    reader = csv.reader(bigwordslist)
    for row in reader:
      names = row[0]
      list_of_names = names.split(",")
      list1.append(list_of_names[0])
      list2.append(list_of_names[1])
  
  which_word_pair = random.randint(0,(len(list1)-1))
  the_words.append(list1[which_word_pair])
  the_words.append(list2[which_word_pair])
  return the_words

def names_and_roles_of_players(number_of_players,list_of_roles,word1="word1",word2="word2"):
  list_of_players = []
  for player in (range(number_of_players)):
    input_to_clear = ""
    player_name = input("Player {number} Enter your name\n".format(number=player+1))
    list_of_players.append(player_name)
    if list_of_roles[player] == "Civilian":
      print("your word is {word}".format(word=word1) + "\n")
      while input_to_clear != "y".upper() :
        input_to_clear = input("Enter Y to continue" + "\n").upper()
      clear()
    elif list_of_roles[player] == "Imposter":
      print("your word is {word}".format(word=word2) + "\n")
      while input_to_clear != "y".upper() :
        input_to_clear = input("Enter Y to continue" + "\n").upper()
      clear()
    elif list_of_roles[player] == "Mr White":
      print("You are Mr.White, good luck." + "\n")
      while input_to_clear != "y".upper() :
        input_to_clear = input("Enter Y to continue" + "\n").upper()
      clear()
  return list_of_players


def turn(list_of_players, list_of_roles):
  turn_order = (random.sample(list_of_players,len(list_of_players)))
  try :
    #This is who Mr White is
    mr_white = list_of_players[list_of_roles.index("Mr White")]    
    #here we're taking Mr white out of the turn order and reinserting him further into the list so he has no chance of starting
    turn_order.remove(mr_white)
    new_mister_white_placement = (random.randint(1, len(list_of_players)-1))
    turn_order.insert((new_mister_white_placement),mr_white)
  finally :
    return turn_order

def update_scoreboard (list_of_players, list_of_roles, role = ""):
    global scoreboard
    if scoreboard == {} :
      scoreboard = {player : 0 for player in list_of_players}
    else :
      for player in list_of_players :
        if player not in scoreboard :
          scoreboard.update({player : 0 })   
    if role == "Civilian" :
      for player in list_of_players + civ_eliminated :
        scoreboard.update({ player : scoreboard.get(player) +2 })
      print_scoreboard() 
    if role == "Imposter" :
      for player in list_of_players + imp_eliminated :
        if list_of_roles[list_of_players.index(player)] == "Imposter" :
          scoreboard.update({ player : scoreboard.get(player) +3 })
      print_scoreboard()
    if role == "Mr White" :
      for player in list_of_players :
        if list_of_roles[list_of_players.index(player)] != "Imposter"  and list_of_roles[list_of_players.index(player)] != "Civilian" :
          scoreboard.update({player : scoreboard.get(player) + 4})
      print_scoreboard()
    

def vote_against_least_convincing(list_of_players, list_of_roles, two_similar_words):
  global imp_eliminated
  global civ_eliminated 
  killed = ""
  while killed not in list_of_players :
    killed = input("Who are you voting against this round?\n")
    
  if list_of_roles[list_of_players.index(killed)] == "Civilian" or list_of_roles[list_of_players.index(killed)] == "Imposter" :
    if list_of_players.count(killed) == -1 :
      print("thats not a valid choice")
    if list_of_players.count(killed) == 1 :
      print("{role} eliminated".format(role=list_of_roles[list_of_players.index(killed)]))
      if list_of_roles[list_of_players.index(killed)] == "Civilian" :
        civ_eliminated.append(killed)
      if list_of_roles[list_of_players.index(killed)] == "Imposter" :
        imp_eliminated.append(killed)
      list_of_roles.pop(list_of_players.index(killed))
      list_of_players.remove(killed)   
  else :
    guess = input("Mr White, i'm sorry but you got found out, try and guess the word now.\n")
    if guess == two_similar_words[0]:
      print("Mr White! We won! Yeah Science!")
      update_scoreboard(list_of_players, list_of_roles, "Mr White")
      the_game()
    else : 
      print("Oh no, Mr White, we lost...")
      list_of_roles.pop(list_of_players.index(killed))
      list_of_players.remove(killed)
     
def the_game():
  global civ_eliminated
  global imp_eliminated
  civ_eliminated = []
  imp_eliminated = []
  print(rules)
  def select_number_of_players():
    number_of_players = input("How many players ? (at least 5)" + "\n")
    print("\n")
    try : 
      int(number_of_players)
    except : 
      return select_number_of_players()
    else :
      return int(number_of_players)
      
  number_of_players = select_number_of_players()  
  list_of_roles = role_selection(number_of_players)
  two_similar_words = words_generator()
  list_of_players = names_and_roles_of_players(number_of_players,list_of_roles,two_similar_words[0],two_similar_words[1])
  
  update_scoreboard(list_of_players, list_of_roles)

  while (list_of_roles.count("Imposter") > 0 or (list_of_roles.count("Mr White") == 1 and list_of_roles.count("Civilian") > 1)) and (len(list_of_roles) > 2) :
    print("\n")
    print(turn(list_of_players, list_of_roles))
    print("\n")
    vote_against_least_convincing(list_of_players, list_of_roles, two_similar_words)
  else :
    if list_of_roles.count("Civilian") >= 2 :
      print("Civilians won !")
      update_scoreboard (list_of_players, list_of_roles, "Civilian")
      the_game()
    elif (list_of_roles.count("Imposter") > 0 and list_of_roles.count("Mr White") == 0):
      print("Imposters won !")
      update_scoreboard (list_of_players, list_of_roles, "Imposter")
      the_game()
    elif (list_of_roles.count("Mr White") == 1):
      print("Mr White, what a play!")
      update_scoreboard (list_of_players, list_of_roles, "Mr White")
      the_game()
  
the_game()


    
