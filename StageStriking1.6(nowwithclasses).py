clear = "\n" * 100

class Player:

  stage_played = ""
  stage_played_key = 0
  winning_player = ""
  losing_player = ""

  def __init__(self):
    
    self.stage_dic = {1:"FOUNTAIN OF DREAMS", 2:"YOSHI'S STORY", 3:"DREAMLAND", 4:"POKEMON STADIUM", 5:"BATTLEFIELD", 6:"FINAL DESTINATION"}
    self.wincount = 0
    self.name = ""
    self.rps_input = ""
    self.rps_winner = None
    self.winner = None
    
player_1 = Player()  
player_2 = Player()

#__________________________________________________________________FUNCTION START

def you_just_sat_at_the_setup():
  
  player_1.name = input("Player 1 type your name here \n")
  player_2.name = input("Player 2 type your name here \n")
  
  def best_of_how_many():
    
    best_of = 0
    while best_of != "3" and best_of != "5" :
      best_of = (input("write 3 for best-of 3, write 5 for best-of 5 \n"))
    return int(best_of)

  best_of = best_of_how_many()
  
  def rock_paper_scissors():

    rps_options = ["ROCK", "PAPER", "SCISSORS"]
    
    def select_rps_options():

      while player_1.rps_input not in rps_options:
        player_1.rps_input = input(str(player_1.name) + " pick either rock, paper or scissors \n").upper()
      print(clear)
  
      while player_2.rps_input not in rps_options:
        player_2.rps_input = input(str(player_2.name) + " pick either rock, paper or scissors \n").upper()
      print(clear)
  
      if player_1.rps_input == player_2.rps_input :
        print("you both picked " + str(player_1.rps_input).lower() + "\n")
        player_1.rps_input = ""
        player_2.rps_input = ""
        select_rps_options()
      
    select_rps_options()
    
    def select_winner():

      if rps_options[rps_options.index(player_1.rps_input)-1] == rps_options[rps_options.index(player_2.rps_input)]:
        print(str(player_1.name) + " wins the RPS ! \n")
        player_1.rps_winner = True
        player_2.rps_winner = False
        
      else :
        print(str(player_2.name) + " wins the RPS ! \n")
        player_2.rps_winner = True
        player_1.rps_winner = False
        
    select_winner()
  
  rock_paper_scissors()
  
  #__________________________________________________________________RPS END, STAGE STRIKING START
  
  def print_stages_dic(dictionnary_of_stages):
    for numbers,stage in sorted(dictionnary_of_stages.items()):
      print(str(numbers) + ":" + stage)
    print("\n")

  def stage_striking():
    
    rps_winner = ""
    rps_loser = ""
    stages_dic = {1:"FOUNTAIN OF DREAMS", 2:"YOSHI'S STORY", 3:"DREAMLAND", 4:"POKEMON STADIUM", 5:"BATTLEFIELD"}
    
    if player_1.rps_winner == True :
      rps_winner = player_1.name
      rps_loser = player_2.name
    else :
      rps_winner = player_2.name
      rps_loser = player_1.name
      
    print(str(rps_winner) + " bans a single stage :")
    print("\n")
  
    print_stages_dic(stages_dic)
    
    rps_winner_selection_1 = int(input("select a number : "))
    stages_dic.pop(rps_winner_selection_1)
    print("\n")
  
    print(str(rps_loser) + " bans two stages :")
    print("\n")
    print_stages_dic(stages_dic)
    rps_loser_selection_2 = int(input("select a number : "))
    stages_dic.pop(rps_loser_selection_2)
    print("\n")
    print_stages_dic(stages_dic)
    rps_loser_selection_3 = int(input("select a number : "))
    stages_dic.pop(rps_loser_selection_3)
    print("\n")
    print_stages_dic(stages_dic)
  
    print(str(rps_winner) + " bans one last stage")
    print("\n")
    rps_winner_selection_4 = int(input("select a number : "))
    stages_dic.pop(rps_winner_selection_4)
  
    def playing_on():
      stage_keys = [1,2,3,4,5]
      stage_keys.remove(rps_winner_selection_1)
      stage_keys.remove(rps_loser_selection_2)
      stage_keys.remove(rps_loser_selection_3)
      stage_keys.remove(rps_winner_selection_4)
      
      for keys in stage_keys :
        
        Player.stage_played_key = keys
        Player.stage_played = stages_dic.pop(keys)
        print("\n")
        print("the first stage is " + Player.stage_played.lower() + "\n")
    playing_on()
  
  stage_striking()
  
  #__________________________________________________________________STAGE STRIKING END, COUNTERPICKING STARTS
  
  def counterpicking():
    
    if best_of == 3 :
      print(str(Player.winning_player) + " bans a stage : \n")
      
      if player_1.winner == True :
        
        try :
          player_1.stage_dic.pop(Player.stage_played_key)
        finally :
          
          print_stages_dic(player_2.stage_dic)
          print("\n")
          
          winning_player_selection = int(input("select a number : "))
          stage_banned = player_2.stage_dic.pop(winning_player_selection)
          print("\n" + str(player_2.name) + " selects a stage : \n")
          print_stages_dic(player_2.stage_dic)
          
          losing_player_selection = int(input("select a number : "))
          stage_picked = player_2.stage_dic.pop(losing_player_selection)
          print("\n")
          print("next game is played on " + stage_picked.lower() + "\n")
    
          player_2.stage_dic.update({winning_player_selection : stage_banned})
          player_2.stage_dic.update({losing_player_selection : stage_picked})
          Player.stage_played_key = losing_player_selection

      if player_2.winner == True :
        
        try :
          player_2.stage_dic.pop(Player.stage_played_key)
        finally :
          
          print_stages_dic(player_1.stage_dic)
          print("\n")
          
          winning_player_selection = int(input("select a number : "))
          stage_banned = player_1.stage_dic.pop(winning_player_selection)
          print("\n" + str(player_1.name) + " selects a stage : \n")
          print_stages_dic(player_1.stage_dic)
          
          losing_player_selection = int(input("select a number : "))
          stage_picked = player_1.stage_dic.pop(losing_player_selection)
          print("\n")
          print("next game is played on " + stage_picked.lower() + "\n")
    
          player_1.stage_dic.update({winning_player_selection : stage_banned})
          player_1.stage_dic.update({losing_player_selection : stage_picked})
          Player.stage_played_key = losing_player_selection

    if best_of == 5 :
      
      if player_1.winner == True :
        
        try :
          player_1.stage_dic.pop(Player.stage_played_key)
        finally :
          print_stages_dic(player_2.stage_dic)
          print("\n")
  
          losing_player_selection = int(input(str(player_2.name) + " select a number : \n"))
          stage_picked = player_2.stage_dic.pop(losing_player_selection)
          print("\n")
          print("next game is played on " + stage_picked.lower() + "\n")
          player_2.stage_dic.update({losing_player_selection : stage_picked})
          Player.stage_played_key = losing_player_selection

      if player_2.winner == True :
        
        try :
          player_2.stage_dic.pop(Player.stage_played_key)
        finally :
          print_stages_dic(player_1.stage_dic)
          print("\n")
  
          losing_player_selection = int(input(str(player_1.name) + " select a number : \n"))
          stage_picked = player_1.stage_dic.pop(losing_player_selection)
          print("\n")
          print("next game is played on " + stage_picked.lower() + "\n")
          player_1.stage_dic.update({losing_player_selection : stage_picked})
          Player.stage_played_key = losing_player_selection
          
    Player.winning_player = ""
    player_1.winner = None
    player_2.winner = None

    defining_the_winner()
    
  def defining_the_winner(): 
    
    while Player.winning_player != player_1.name and Player.winning_player != player_2.name :
      Player.winning_player = input("type the name of the winning player, either {} or {} : \n".format(player_1.name,player_2.name))
    if Player.winning_player == player_1.name:
      player_1.winner = True
      player_1.wincount +=1
    else :
      player_2.winner = True
      player_2.wincount +=1
      
    if best_of == 3:
      if player_1.wincount >=2:
        print("\n" + str(player_1.name) + " wins the set \n")
        you_just_sat_at_the_setup()
      if player_2.wincount >=2:
        print("\n" + str(player_2.name) + " wins the set \n")
        you_just_sat_at_the_setup()
        
    if best_of == 5:
      if player_1.wincount >=3:
        print("\n" + str(player_1.name) + " wins the set \n")
        you_just_sat_at_the_setup()
      if player_2.wincount >=3:
        print("\n" + str(player_2.name) + " wins the set \n")
        you_just_sat_at_the_setup()

      
    counterpicking()
        
  defining_the_winner()
  
you_just_sat_at_the_setup()
  
    
    
  
