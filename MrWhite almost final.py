# 2 known bugs : 1st if you don't put an interger in the first prompt for how many players there is, and 2nd
# if you misspell the name of the eliminated player it will generate a new turn_order
import random

rules = """In this game, everyone gets the same word, except Mr white who doesn't get a word, and the imposter(s) who get a slightly different one.

Each turn you will each say a SINGLE word (following the order generated). \n 
you must try to convince everyone else you have the correct word but without giving too much away if you actually do (as to not help the imposters).

At the end of each turn, and after discussing it thoroughly, you will vote out the most suspicious player.
If Mister White is voted out he can still win by guessing the word.

Imposters can only win by voting everyone out (remember they don't immediately know they are imposters).

Civilians need to eliminate both the imposters and Mr White. If after a vote a single Civilian remains he is also eliminated for the game.
"""

def role_selection(number_of_players):
  role_list=[]
  for players in range(number_of_players):
    role_list.append("Civilian")
    
  number_of_imposters = 2 + round(number_of_players//6)
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
  number_of_players = int(input("How many players ? (at least 5)\n"))
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


    

    
    
    