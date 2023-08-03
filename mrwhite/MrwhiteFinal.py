import random
import csv

rules = """In this game, all players receive the same word, except for Mr. White, who receives a different word, and the imposters, who also get a slightly different one.

During each turn, each player will say only one word in the order generated.

The goal is to convince everyone else that you have the correct word without giving away too much information that might help the imposters.

After each turn, there will be a discussion, and the group will vote to eliminate the most suspicious player.

If Mr. White is voted out, he still has a chance to win by correctly guessing the word.

The imposters can only win by voting out all the other players, but they don't know who the other imposters are initially.

The civilians must eliminate both the imposters and Mr. White. If, after a vote, only one civilian remains, they are also eliminated from the game.
"""

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
  list_of_players=[]
  for player in (range(number_of_players)):
    list_of_players.append(input("Player {number} Enter your name\n".format(number=player+1)))
    if list_of_roles[player] == "Civilian":
      print("your word is {word}".format(word=word1))
    elif list_of_roles[player] == "Imposter":
      print("your word is {word}".format(word=word2))
    elif list_of_roles[player] == "Mr White":
      print("You are Mr.White, good luck.")
  return list_of_players

def turn(list_of_players, list_of_roles):
  turn_order = (random.sample(list_of_players,len(list_of_players)))
  #This is who Mr White is
  mr_white = list_of_players[list_of_roles.index("Mr White")]    
  #here we're taking Mr white out of the turn order and reinserting him further into the list so he has no chance of starting
  turn_order.remove(mr_white)
  turn_order.insert((random.randint(1, len(list_of_players))-1),mr_white)
  return turn_order

def vote_against_least_convincing(list_of_players, list_of_roles, two_similar_words):
  killed = ""
  while killed not in list_of_players :
    killed = input("Who are you voting against this round?\n")
  
  if killed != list_of_players[list_of_roles.index("Mr White")]:
    if list_of_players.count(killed) == -1 :
      print("thats not a valid choice")
    if list_of_players.count(killed) == 1 :
      print("{role} eliminated".format(role=list_of_roles[list_of_players.index(killed)]))
      list_of_roles.pop(list_of_players.index(killed))
      list_of_players.remove(killed)
  if killed == list_of_players[list_of_roles.index("Mr White")]:
    guess = input("Mr White, i'm sorry but you got found out, try and guess the word now.\n")
    if guess == two_similar_words[0]:
      print("Mr White! We won! Yeah Science!")
      the_game()
    else : 
      print("Oh no, Mr White, we lost...")
        
def the_game():
  print(rules)
  def select_number_of_players():
    number_of_players = input("How many players ? (at least 5)\n")
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
  
  while (list_of_roles.count("Imposter") > 0 or list_of_roles.count("Mr White") > 0) and list_of_roles.count("Civilian") >= 2 :
    print(turn(list_of_players, list_of_roles))
    vote_against_least_convincing(list_of_players, list_of_roles, two_similar_words)
  else :
    if list_of_roles.count("Civilian") >= 2 :
      print("Civilians won !")
      the_game()
    elif (list_of_roles.count("Imposter") > 0 and list_of_roles.count("Mr White") == 0):
      print("Imposters won !")
      the_game()
    elif (list_of_roles.count("Imposter") == 0 and list_of_roles.count("Mr White") == 1):
      print("Mr White, what a play!")
      the_game()
  
the_game()


    

    
    
    