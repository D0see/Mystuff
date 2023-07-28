clear = "\n" * 100

rps_options = ["ROCK", "PAPER", "SCISSORS"]
rps_winner = ""
rps_loser = ""

stages_dic = {1:"FOUNTAIN OF DREAMS", 2:"YOSHI'S STORY", 3:"DREAMLAND", 4:"POKEMON STADIUM", 5:"BATTLEFIELD"}

def print_stages_dic():
  for numbers,stage in stages_dic.items():
    print(str(numbers) + ":" + stage)
  print("\n")
  
def rock_paper_scissors():
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
      print("you both picked " + str(player_1_input) + "\n")
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

def stage_striking(rps_winner, rps_loser):
  global stages_dic
  print(str(rps_winner) + " bans a single stage :")
  print("\n")

  print_stages_dic()
  
  rps_winner_selection_1 = int(input("select a number : "))
  stages_dic.pop(rps_winner_selection_1)
  print("\n")

  print(str(rps_loser) + " bans two stages :")
  print("\n")
  print_stages_dic()
  rps_loser_selection_2 = int(input("select a number : "))
  stages_dic.pop(rps_loser_selection_2)
  print("\n")
  print_stages_dic()
  rps_loser_selection_3 = int(input("select a number : "))
  stages_dic.pop(rps_loser_selection_3)

  print_stages_dic()

  print(str(rps_winner) + " bans one last stage")
  rps_winner_selection_4 = int(input("select a number : "))
  stages_dic.pop(rps_winner_selection_4)

  def playing_on():
    stage_keys = [1,2,3,4,5]
    stage_keys.remove(rps_winner_selection_1)
    stage_keys.remove(rps_loser_selection_2)
    stage_keys.remove(rps_loser_selection_3)
    stage_keys.remove(rps_winner_selection_4)
    
    for keys in stage_keys :
      stage_played = stages_dic.pop(keys)
      print("\n")
      print("the first stage is " + stage_played.lower())
  playing_on()

stage_striking(rps_winner, rps_loser)