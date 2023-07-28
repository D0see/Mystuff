clear = "\n" * 100

rps_options = ["ROCK", "PAPER", "SCISSORS"]
rps_winner = ""
rps_loser = ""

stages_dic = {1:"FOUNTAIN OF DREAMS", 2:"YOSHI'S STORY", 3:"DREAMLAND", 4:"POKEMON STADIUM", 5:"BATTLEFIELD"}
stages_dic_player_1 = {1:"FOUNTAIN OF DREAMS", 2:"YOSHI'S STORY", 3:"DREAMLAND", 4:"POKEMON STADIUM", 5:"BATTLEFIELD", 6:"FINAL DESTINATION"}
stages_dic_player_2 = {1:"FOUNTAIN OF DREAMS", 2:"YOSHI'S STORY", 3:"DREAMLAND", 4:"POKEMON STADIUM", 5:"BATTLEFIELD", 6:"FINAL DESTINATION"}

stage_played = ""
stage_played_key = 0
player_1 = ""
player_2 = ""
player_1_win_count = 0
player_2_win_count = 0
winning_player = ""
losing_player = ""

def print_stages_dic(dictionnary_of_stages):
  for numbers,stage in sorted(dictionnary_of_stages.items()):
    print(str(numbers) + ":" + stage)
  print("\n")

def best_of_how_many():
  best_of = 0
  while best_of != 3 and best_of != 5 :
    best_of = int((input("write 3 for best-of 3, write 5 for best-of 5 \n")))
  return best_of

#__________________________________________________________________FUNCTION START
def you_just_sat_at_the_setup():
  
  best_of = best_of_how_many()
  
  def rock_paper_scissors():
    global player_1
    global player_2
    player_1 = input("Player 1, type your name here \n")
    player_2 = input("Player 2, type your name here \n")
    player_1_input = ""
    player_2_input = ""
  
    
    def select_rps_options():
      nonlocal player_2_input
      nonlocal player_1_input
      
      while player_1_input not in rps_options:
        player_1_input = input(str(player_1) + " pick either rock, paper or scissors \n").upper()
      print(clear)
  
      while player_2_input not in rps_options:
        player_2_input = input(str(player_2) + " pick either rock, paper or scissors \n").upper()
      print(clear)
  
      if player_1_input == player_2_input :
        print("you both picked " + str(player_1_input).lower() + "\n")
        player_1_input = ""
        player_2_input = ""
        select_rps_options()
      
    select_rps_options()
    
    def select_winner():
      global rps_winner
      global rps_loser
      if rps_options[rps_options.index(player_1_input)-1] == rps_options[rps_options.index(player_2_input)]:
        print(str(player_1) + " wins ! \n")
        rps_winner = player_1
        rps_loser = player_2
      else :
        print(str(player_2) + " wins ! \n")
        rps_winner = player_2
        rps_loser = player_1
    select_winner()
  
  rock_paper_scissors()
  
  #__________________________________________________________________RPS END, STAGE STRIKING START
    
  
  def stage_striking(rps_winner, rps_loser):
    global stages_dic
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
        global stage_played
        global stage_played_key
        stage_played_key = keys
        stage_played = stages_dic.pop(keys)
        print("\n")
        print("the first stage is " + stage_played.lower() + "\n")
    playing_on()
  
  stage_striking(rps_winner, rps_loser)
  
  #__________________________________________________________________STAGE STRIKING END, COUNTERPICKING STARTS
  
  def counterpicking():
    global winning_player
    global losing_player
    global stage_played_key
    print("\n")
    
    
    if best_of == 3 :
      print(str(winning_player) + " bans a stage : \n")
      if winning_player == player_1:
        stages_dic_player_1.pop(stage_played_key)
        print_stages_dic(stages_dic_player_2)
        print("\n")
        
        winning_player_selection = int(input("select a number : "))
        stage_banned = stages_dic_player_2.pop(winning_player_selection)
        print("\n" + str(player_2) + " selects a stage : \n")
        print_stages_dic(stages_dic_player_2)
        
        losing_player_selection = int(input("select a number : "))
        stage_picked = stages_dic_player_2.pop(losing_player_selection)
        print("\n")
        print("next game is played on " + stage_picked.lower() + "\n")
  
        stages_dic_player_2.update({winning_player_selection : stage_banned})
        stages_dic_player_2.update({losing_player_selection : stage_picked})
        stage_played_key = losing_player_selection

        
  
      if winning_player == player_2:
        stages_dic_player_2.pop(stage_played_key)
        print_stages_dic(stages_dic_player_1)
        print("\n")
        
        winning_player_selection = int(input("select a number : "))
        stage_banned = stages_dic_player_1.pop(winning_player_selection)
        print("\n" + str(player_1) + " selects a stage : \n")
        print_stages_dic(stages_dic_player_1)
        
        losing_player_selection = int(input("select a number : "))
        stage_picked = stages_dic_player_1.pop(losing_player_selection)
        print("\n")
        print("next game is played on " + stage_picked.lower() + "\n")
  
        stages_dic_player_1.update({winning_player_selection : stage_banned})
        stages_dic_player_1.update({losing_player_selection : stage_picked})
        stage_played_key = losing_player_selection

        
    if best_of == 5 :
      
      if winning_player == player_1:
        stages_dic_player_1.pop(stage_played_key)
        print_stages_dic(stages_dic_player_2)
        print("\n")

        losing_player_selection = int(input(str(losing_player) + " select a number : "))
        stage_picked = stages_dic_player_2.pop(losing_player_selection)
        print("\n")
        print("next game is played on " + stage_picked.lower() + "\n")
        stages_dic_player_2.update({losing_player_selection : stage_picked})
        stage_played_key = losing_player_selection

      if winning_player == player_2:
        stages_dic_player_2.pop(stage_played_key)
        print_stages_dic(stages_dic_player_1)
        print("\n")

        losing_player_selection = int(input(str(losing_player) + " select a number : \n"))
        stage_picked = stages_dic_player_1.pop(losing_player_selection)
        print("\n")
        print("next game is played on " + stage_picked.lower() + "\n")
        stages_dic_player_1.update({losing_player_selection : stage_picked})
        stage_played_key = losing_player_selection
        
    
    winning_player = ""
    losing_player = ""

    defining_the_winner()
    
  def defining_the_winner(): 
    global player_1_win_count
    global player_2_win_count
    global winning_player
    global losing_player
    while winning_player != player_1 and winning_player != player_2 :
      winning_player = input("type the name of the winning player, either {} or {} : \n".format(player_1,player_2))
    if winning_player == player_1:
      losing_player = player_2
      player_1_win_count +=1
    else :
      losing_player = player_1
      player_2_win_count +=1
      
    if best_of == 3:
      if player_1_win_count >=2:
        print("\n" + str(player_1) + " wins the set \n")
        you_just_sat_at_the_setup()
      if player_2_win_count >=2:
        print("\n" + str(player_2) + " wins the set \n")
        you_just_sat_at_the_setup()
    if best_of == 5:
      if player_1_win_count >=3:
        print("\n" + str(player_1) + " wins the set \n")
        you_just_sat_at_the_setup()
      if player_2_win_count >=3:
        print("\n" + str(player_2) + " wins the set \n")
        you_just_sat_at_the_setup()
    counterpicking()
        
  defining_the_winner()
  
you_just_sat_at_the_setup()
  
    
    
  
