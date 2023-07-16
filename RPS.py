

def Rock_Paper_scissors():
  legal_moves = ["Rock", "Paper", "Scissors"]
  Games_to_win = input("Enter an interger for how many wins it takes to win \n")
  player_1_win_counter = 0
  player_2_win_counter = 0
  if Games_to_win.isnumeric() :
    while player_1_win_counter < int(Games_to_win) and player_2_win_counter < int(Games_to_win) :
      player_one_input = input("player1 input your choice : \n")
      player_two_input = input("player2 input your choice :  \n")

      if player_one_input == "Well" or player_two_input == "Well":
        print("We don't play with those in this part of town, it's what you would call an ")
    
      if legal_moves.count(player_one_input) == 0 or legal_moves.count(player_two_input) == 0:
        print("illegal choice ! (don't forget to capitalize the first letter !)")
    
      elif player_one_input == player_two_input:
        print("It's a tie!")
    
      elif (player_one_input == "Rock" and player_two_input == "Scissors") or (player_one_input == "Scissors" and player_two_input == "Paper") or (player_one_input == "Paper" and player_two_input == "Rock"):
        print("player 1 wins")
        player_1_win_counter += 1
      
      else: 
        print("player 2 wins")
        player_2_win_counter += 1
    
    else:
      print("Player 1 : "+ str(player_1_win_counter) + "\n" "Player 2 : " + str(player_2_win_counter))
      Play_again = input ("Play again? (Yes or No) \n")
        
      if Play_again == "Yes" :
          Rock_Paper_scissors()
      else:
        print("Ok ! Goodbye !")
  else:
    Rock_Paper_scissors()


Rock_Paper_scissors()
    