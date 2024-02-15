#todo : Build castling logic (hard)


import itertools
import copy

def the_game():

  #Ask what length the user wants the board to be
  """def define_row_length():
    row_length = 0
    while row_length <= 3 or row_length > 8 or row_length == 5 :
      row_length = int(input("how many cases per row ? (4,6,7 or 8)" + "\n"))
    return row_length"""
  

  #prints the board 
  def print_grid(grid, row_length):
      grid_to_print = [*grid.items()]

      for row in range(row_length):
        row_to_print = grid_to_print[(0+row)*row_length:(1+row)*row_length]
        final_row = []

        for case in row_to_print:
          if len(case[1]) < 8 :
            new_case = (case[0], " "*round((8-len(case[1]))/2) + case[1] + " "*round((8-len(case[1]))/2))
            if "Queen" in case[1]:
              new_case = (case[0], case[1] + " ")
            elif "Empty" in case[1]:
              new_case = (case[0]," "*8)
          else :
            new_case = case
            
          final_row.append(new_case)
        print(final_row)


  #Create the grid and puts the pieces on it
  def make_and_populate_a_grid(row_length):
    
    def make_a_squared_grid(grid_size) :
      possible_coordinates = [i for i in range(1, grid_size +1)]
      
      grid = itertools.product(possible_coordinates, repeat=2 )
      
      grid_dict = dict(zip(grid, itertools.repeat("Empty")))
      return grid_dict
    grid = make_a_squared_grid(row_length)

    
    def populate_grid(grid, row_length):
      
      def populate_grid_with_pawns(grid, row_length):
        BPawn_counter = 1
        WPawn_counter = 1
        for coordinates in grid :
          if coordinates[0] == 2 :
            grid.update({coordinates : f"BPawn{BPawn_counter}"})
            BPawn_counter += 1
          if coordinates[0] == row_length - 1 :
            grid.update({coordinates : f"WPawn{WPawn_counter}"})
            WPawn_counter += 1
      populate_grid_with_pawns(grid, row_length)

      def populate_grid_with_piece(grid, row_length, piece, offset):
        if row_length % 2 == 0 :
          for coordinates in grid :
            if coordinates[0] == 1 and coordinates[1] == row_length / 2 - offset :
              grid.update({coordinates : f"B{piece}1"})
            if coordinates[0] == 1 and coordinates[1] == row_length / 2 + (offset + 1) :
              grid.update({coordinates : f"B{piece}2"})
            if coordinates[0] == row_length and coordinates[1] == row_length / 2 - offset :
              grid.update({coordinates : f"W{piece}1"})
            if coordinates[0] == row_length and coordinates[1] == row_length / 2 + (offset + 1) :
              grid.update({coordinates : f"W{piece}2"})  
        else :
          for coordinates in grid :
            if coordinates[0] == 1 and coordinates[1] == round(row_length/ 2 ) - offset :
              grid.update({coordinates : f"B{piece}1"})
            if coordinates[0] == 1 and coordinates[1] == round(row_length/ 2 ) + offset :
              grid.update({coordinates : f"B{piece}2"}) 
            if coordinates[0] == row_length and coordinates[1] == round(row_length/ 2 ) - offset :
              grid.update({coordinates : f"W{piece}1"})
            if coordinates[0] == row_length and coordinates[1] == round(row_length/ 2 ) + offset :
              grid.update({coordinates : f"W{piece}2"})  
      # offset : bishop = 1, knight = 2, rook = 3
      populate_grid_with_piece(grid, row_length, "Bishop", 1)
      populate_grid_with_piece(grid, row_length, "Knight", 2)
      populate_grid_with_piece(grid, row_length, "Rook", 3)

      def populate_grid_with_q_and_k(grid, row_length):
        if row_length % 2 == 0 :
          for coordinates in grid :
            if coordinates[0] == 1 and coordinates[1] == row_length / 2 :
              grid.update({coordinates : "BQueen1"})
            if coordinates[0] == 1 and coordinates[1] == row_length / 2 + 1 :
              grid.update({coordinates : "BKing1"})
            if coordinates[0] == row_length and coordinates[1] == row_length / 2 :
              grid.update({coordinates : "WQueen1"})
            if coordinates[0] == row_length and coordinates[1] == row_length / 2 + 1 :
              grid.update({coordinates : "WKing1"})  
        else :
          for coordinates in grid :
            if coordinates[0] == 1 and coordinates[1] == round(row_length/ 2 ) :
              grid.update({coordinates : "BKing1"})
            if coordinates[0] == row_length and coordinates[1] == round(row_length/ 2 ) :
              grid.update({coordinates : "WKing1"})
      populate_grid_with_q_and_k(grid, row_length)        
        
    populate_grid(grid,row_length )
      
    print_grid(grid, row_length)
    return grid #create a squared grid (a dictionnary) of length row_length then populate the grid with pieces.

  #row_length = define_row_length()
  row_length = 8
  playground = make_and_populate_a_grid(row_length)


  def game_logic(grid) :
      turn_count = 1
      anti_turn = "B"
      turn = "W"
      #handles the logic for whose turn it is "B" or "W" (goes to next turn when called)
      def next_turn():
          nonlocal turn
          nonlocal anti_turn
          nonlocal turn_count
          if turn == "W":
            turn = "B"
            anti_turn = "W"
            turn_count += 1
          else : 
              turn = "W"
              anti_turn = "B"
              turn_count += 1 

      list_of_elements_on_board = []
      list_of_coordinates_on_board = []
      #updates list of elements on board and the list of coordinates on board
      def update_grid(grid):
        nonlocal list_of_elements_on_board
        nonlocal list_of_coordinates_on_board
        #updates the list_of_elements_on_board from the grid
        list_of_elements_on_board = [*grid.values()]
        #updates the list of coordinates from the grid (redundant after the first time)
        list_of_coordinates_on_board = [*grid]

      rollback_copy = {}
      #Makes a copy of the grid before the main one is used to check for checks
      def make_rollbackcopy(grid):
        nonlocal rollback_copy
        rollback_copy = copy.deepcopy(grid)

      
      #Function definitions for piece movement (returns a list of possible move for a given piece_location):
      def move_pawn(turn, piece_location, grid = playground):
              list_of_possible_moves = []
              
              if turn == "W" :
                #pawn move logic for white  
                if grid.get((piece_location[0] - 1, piece_location[1])) == "Empty" :
                  list_of_possible_moves.append((piece_location[0] - 1, piece_location[1]))
                  if piece_location[0] == row_length - 1 and grid.get((piece_location[0] - 2, piece_location[1])) == "Empty" :
                    list_of_possible_moves.append((piece_location[0] - 2, piece_location[1]))
                #pawn capture logic for white
                if piece_location[1] < row_length :
                  if (grid.get((piece_location[0] - 1, piece_location[1] + 1 ))).startswith("B") :
                    list_of_possible_moves.append((piece_location[0] - 1, piece_location[1] + 1))
                  #en-passant capture logic
                  if last_piece_to_move[1:-1] == "Pawn" :
                    if (grid.get((piece_location[0], piece_location[1] + 1 ))) == last_piece_to_move :
                      list_of_possible_moves.append((piece_location[0] - 1, piece_location[1] + 1))
                if piece_location[1] > 1 :
                  if (grid.get((piece_location[0] - 1, piece_location[1] - 1 ))).startswith("B") :
                    list_of_possible_moves.append((piece_location[0] - 1, piece_location[1] - 1))  
                  #en-passant capture logic
                  if last_piece_to_move[1:-1] == "Pawn" :
                    if (grid.get((piece_location[0], piece_location[1]  - 1 ))) == last_piece_to_move :
                      list_of_possible_moves.append((piece_location[0] - 1, piece_location[1] - 1))
                
              elif turn == "B"  :
                #pawn move logic for black  
                if grid.get((piece_location[0] + 1, piece_location[1])) == "Empty" :
                  list_of_possible_moves.append((piece_location[0] + 1, piece_location[1]))
                  if piece_location[0] == 2 and grid.get((piece_location[0] + 2, piece_location[1])) == "Empty" :
                    list_of_possible_moves.append((piece_location[0] + 2, piece_location[1]))
                #pawn capture logic for black
                if piece_location[1] < row_length :
                  if (grid.get((piece_location[0] + 1, piece_location[1] + 1 ))).startswith("W") :
                    list_of_possible_moves.append((piece_location[0] + 1, piece_location[1] + 1))
                #en-passant capture logic
                  if last_piece_to_move[1:-1] == "Pawn" :
                    if (grid.get((piece_location[0], piece_location[1] + 1 ))) == last_piece_to_move :
                      list_of_possible_moves.append((piece_location[0] + 1, piece_location[1] + 1))
                if piece_location[1] > 1 :
                  if (grid.get((piece_location[0] + 1, piece_location[1] - 1 ))).startswith("W") :
                    list_of_possible_moves.append((piece_location[0] + 1, piece_location[1] - 1))  
                #en-passant capture logic
                  if last_piece_to_move[1:-1] == "Pawn" :
                    if (grid.get((piece_location[0], piece_location[1]  - 1 ))) == last_piece_to_move :
                      list_of_possible_moves.append((piece_location[0] + 1, piece_location[1] - 1))
              return list_of_possible_moves
      
      def move_rook(turn, anti_turn, piece_location, grid = playground):
              list_of_possible_moves = []
              #Rook move and capture logic on the Y axis 
                #Rook move and capture logic on the Y axis ( from row_length to 1 / UP )
              for digit in range(row_length-1): 
                try :
                  if grid.get((piece_location[0] - (1+digit), piece_location[1])) == "Empty" :
                    list_of_possible_moves.append((piece_location[0] - (1+digit), piece_location[1]))
                  elif grid.get((piece_location[0] - (1+digit), piece_location[1])).startswith(anti_turn):
                    list_of_possible_moves.append((piece_location[0] - (1+digit), piece_location[1]))
                    break
                  elif grid.get((piece_location[0] - (1+digit), piece_location[1])).startswith(turn):
                    break
                except : break
              #Rook move and capture logic on the Y axis ( from 1 to row_length / DOWN )
              for digit in range(row_length-1): 
                try :
                  if grid.get((piece_location[0] + (1+digit), piece_location[1])) == "Empty" :
                    list_of_possible_moves.append((piece_location[0] + (1+digit), piece_location[1]))
                  elif grid.get((piece_location[0] + (1+digit), piece_location[1])).startswith(anti_turn):
                    list_of_possible_moves.append((piece_location[0] + (1+digit), piece_location[1]))
                    break
                  elif grid.get((piece_location[0] + (1+digit), piece_location[1])).startswith(turn):
                    break
                except : break
            #Rook move and capture logic on the X axis
              #Rook move and capture logic on the X axis ( from row_length to 1 / LEFT )
              for digit in range(row_length-1): 
                try :
                  if grid.get((piece_location[0], piece_location[1] - (1+digit))) == "Empty" :
                    list_of_possible_moves.append((piece_location[0], piece_location[1] - (1+digit)))
                  elif grid.get((piece_location[0], piece_location[1] - (1+digit))).startswith(anti_turn):
                    list_of_possible_moves.append((piece_location[0], piece_location[1] - (1+digit)))
                    break
                  elif grid.get((piece_location[0], piece_location[1] - (1+digit))).startswith(turn):
                    break
                except : break
              #Rook move and capture logic on the X axis ( from 1 to row_length / RIGHT )
              for digit in range(row_length-1):
                try :
                  if grid.get((piece_location[0], piece_location[1] + (1+digit))) == "Empty" :
                    list_of_possible_moves.append((piece_location[0], piece_location[1] + (1+digit)))
                  elif grid.get((piece_location[0], piece_location[1] + (1+digit))).startswith(anti_turn):
                    list_of_possible_moves.append((piece_location[0], piece_location[1] + (1+digit)))
                    break
                  elif grid.get((piece_location[0], piece_location[1] + (1+digit))).startswith(turn):
                    break
                except : break
              return list_of_possible_moves
      def move_bishop(turn, anti_turn, piece_location, grid = playground):
              list_of_possible_moves = []
              
              #Bishop move and capture logic
                #Bishop move and capture logic on DIAG UP-LEFT :
              for digit in range(row_length-1): 
                try :
                  if grid.get((piece_location[0] - (1+digit), piece_location[1] - (1+digit))) == "Empty" :
                    list_of_possible_moves.append((piece_location[0] - (1+digit), piece_location[1] - (1+digit)))
                  elif grid.get((piece_location[0] - (1+digit), piece_location[1] - (1+digit))).startswith(anti_turn):
                    list_of_possible_moves.append((piece_location[0] - (1+digit), piece_location[1] - (1+digit)))
                    break
                  elif grid.get((piece_location[0] - (1+digit), piece_location[1] - (1+digit))).startswith(turn):
                    break
                except : break
                  
              #Bishop move and capture logic on DIAG UP-RIGHT :
              for digit in range(row_length-1): 
                try :
                  if grid.get((piece_location[0] - (1+digit), piece_location[1] + (1+digit))) == "Empty" :
                    list_of_possible_moves.append(((piece_location[0] - (1+digit), piece_location[1] + (1+digit))))
                  elif grid.get((piece_location[0] - (1+digit), piece_location[1] + (1+digit))).startswith(anti_turn):
                    list_of_possible_moves.append(((piece_location[0] - (1+digit), piece_location[1] + (1+digit))))
                    break
                  elif grid.get((piece_location[0] - (1+digit), piece_location[1] + (1+digit))).startswith(turn):
                    break
                except : break
                  
              #Bishop move and capture logic on DIAG DOWN-LEFT :
              for digit in range(row_length-1): 
                try :
                  if grid.get((piece_location[0] + (1+digit), piece_location[1] - (1+digit))) == "Empty" :
                    list_of_possible_moves.append(((piece_location[0] + (1+digit), piece_location[1] - (1+digit))))
                  elif grid.get((piece_location[0] + (1+digit), piece_location[1] - (1+digit))).startswith(anti_turn):
                    list_of_possible_moves.append(((piece_location[0] + (1+digit), piece_location[1] - (1+digit))))
                    break
                  elif grid.get((piece_location[0] + (1+digit), piece_location[1] - (1+digit))).startswith(turn):
                    break
                except : break
      
              #Bishop move and capture logic on DIAG DOWN-RIGHT :
              for digit in range(row_length-1): 
                try :
                  if grid.get((piece_location[0] + (1+digit), piece_location[1] + (1+digit))) == "Empty" :
                    list_of_possible_moves.append(((piece_location[0] + (1+digit), piece_location[1] + (1+digit))))
                  elif grid.get((piece_location[0] + (1+digit), piece_location[1] + (1+digit))).startswith(anti_turn):
                    list_of_possible_moves.append(((piece_location[0] + (1+digit), piece_location[1] + (1+digit))))
                    break
                  elif grid.get((piece_location[0] + (1+digit), piece_location[1] + (1+digit))).startswith(turn):
                    break
                except : break
              return list_of_possible_moves
      def move_knight(turn, piece_location, grid = playground):
              list_of_possible_moves = []
          
              #Knight move and capture logic 
            #Knight move and capture logic on the Y axis 
              #Knight move and capture logic on Y-Top-Left :
              try :
                if not grid.get((piece_location[0] - 2, piece_location[1] - 1)).startswith(turn):
                  list_of_possible_moves.append((piece_location[0] - 2, piece_location[1] - 1))
              except : pass
              #Knight move and capture logic on Y-Top-Right :
              try :
                if not grid.get((piece_location[0] - 2, piece_location[1] + 1)).startswith(turn):
                  list_of_possible_moves.append((piece_location[0] - 2, piece_location[1] + 1))
              except : pass
              #Knight move and capture logic on Y-Bottom-Left :
              try :
                if not grid.get((piece_location[0] + 2, piece_location[1] - 1)).startswith(turn):
                  list_of_possible_moves.append((piece_location[0] + 2, piece_location[1] - 1))
              except : pass
              #Knight move and capture logic on Y-Bottom-Right :
              try :
                if not grid.get((piece_location[0] + 2, piece_location[1] + 1)).startswith(turn):
                  list_of_possible_moves.append((piece_location[0] + 2, piece_location[1] + 1))
              except : pass  
            #Knight move and capture logic on the X axis 
              #Knight move and capture logic on X-Top-Left :
              try :
                if not grid.get((piece_location[0] - 1, piece_location[1] - 2)).startswith(turn):
                  list_of_possible_moves.append((piece_location[0] - 1, piece_location[1] - 2))
              except : pass
              #Knight move and capture logic on X-Top-Right :
              try :
                if not grid.get((piece_location[0] - 1, piece_location[1] + 2)).startswith(turn):
                  list_of_possible_moves.append((piece_location[0] - 1, piece_location[1] + 2))
              except : pass
              #Knight move and capture logic on X-Bottom-Left :
              try :
                if not grid.get((piece_location[0] + 1, piece_location[1] - 2)).startswith(turn):
                  list_of_possible_moves.append((piece_location[0] + 1, piece_location[1] - 2))
              except : pass
              #Knight move and capture logic on X-Bottom-Right :
              try :
                if not grid.get((piece_location[0] + 1, piece_location[1] + 2)).startswith(turn):
                  list_of_possible_moves.append((piece_location[0] + 1, piece_location[1] + 2))
              except : pass
              return list_of_possible_moves
      def move_queen(turn, anti_turn, piece_location, grid = playground):
              list_of_possible_moves = []
              
            #Queen move and capture logic
              #Queen move and capture logic on the Y axis 
                #Queen move and capture logic on the Y axis ( from row_length to 1 / UP )
              for digit in range(row_length-1): 
                try :
                  if grid.get((piece_location[0] - (1+digit), piece_location[1])) == "Empty" :
                    list_of_possible_moves.append((piece_location[0] - (1+digit), piece_location[1]))
                  elif grid.get((piece_location[0] - (1+digit), piece_location[1])).startswith(anti_turn):
                    list_of_possible_moves.append((piece_location[0] - (1+digit), piece_location[1]))
                    break
                  elif grid.get((piece_location[0] - (1+digit), piece_location[1])).startswith(turn):
                    break
                except : break
              #Queen move and capture logic on the Y axis ( from 1 to row_length / DOWN )
              for digit in range(row_length-1): 
                try :
                  if grid.get((piece_location[0] + (1+digit), piece_location[1])) == "Empty" :
                    list_of_possible_moves.append((piece_location[0] + (1+digit), piece_location[1]))
                  elif grid.get((piece_location[0] + (1+digit), piece_location[1])).startswith(anti_turn):
                    list_of_possible_moves.append((piece_location[0] + (1+digit), piece_location[1]))
                    break
                  elif grid.get((piece_location[0] + (1+digit), piece_location[1])).startswith(turn):
                    break
                except : break
            #Queen move and capture logic on the X axis
              #Queen move and capture logic on the X axis ( from row_length to 1 / LEFT )
              for digit in range(row_length-1): 
                try :
                  if grid.get((piece_location[0], piece_location[1] - (1+digit))) == "Empty" :
                    list_of_possible_moves.append((piece_location[0], piece_location[1] - (1+digit)))
                  elif grid.get((piece_location[0], piece_location[1] - (1+digit))).startswith(anti_turn):
                    list_of_possible_moves.append((piece_location[0], piece_location[1] - (1+digit)))
                    break
                  elif grid.get((piece_location[0], piece_location[1] - (1+digit))).startswith(turn):
                    break
                except : break
              #Queen move and capture logic on the X axis ( from 1 to row_length / RIGHT )
              for digit in range(row_length-1):
                try :
                  if grid.get((piece_location[0], piece_location[1] + (1+digit))) == "Empty" :
                    list_of_possible_moves.append((piece_location[0], piece_location[1] + (1+digit)))
                  elif grid.get((piece_location[0], piece_location[1] + (1+digit))).startswith(anti_turn):
                    list_of_possible_moves.append((piece_location[0], piece_location[1] + (1+digit)))
                    break
                  elif grid.get((piece_location[0], piece_location[1] + (1+digit))).startswith(turn):
                    break
                except : break
              #Queen move and capture logic on DIAG UP-LEFT :
              for digit in range(row_length-1): 
                try :
                  if grid.get((piece_location[0] - (1+digit), piece_location[1] - (1+digit))) == "Empty" :
                    list_of_possible_moves.append((piece_location[0] - (1+digit), piece_location[1] - (1+digit)))
                  elif grid.get((piece_location[0] - (1+digit), piece_location[1] - (1+digit))).startswith(anti_turn):
                    list_of_possible_moves.append((piece_location[0] - (1+digit), piece_location[1] - (1+digit)))
                    break
                  elif grid.get((piece_location[0] - (1+digit), piece_location[1] - (1+digit))).startswith(turn):
                    break
                except : break
              #Queen move and capture logic on DIAG UP-RIGHT :
              for digit in range(row_length-1): 
                try :
                  if grid.get((piece_location[0] - (1+digit), piece_location[1] + (1+digit))) == "Empty" :
                    list_of_possible_moves.append(((piece_location[0] - (1+digit), piece_location[1] + (1+digit))))
                  elif grid.get((piece_location[0] - (1+digit), piece_location[1] + (1+digit))).startswith(anti_turn):
                    list_of_possible_moves.append(((piece_location[0] - (1+digit), piece_location[1] + (1+digit))))
                    break
                  elif grid.get((piece_location[0] - (1+digit), piece_location[1] + (1+digit))).startswith(turn):
                    break
                except : break
              #Queen move and capture logic on DIAG DOWN-LEFT :
              for digit in range(row_length-1): 
                try :
                  if grid.get((piece_location[0] + (1+digit), piece_location[1] - (1+digit))) == "Empty" :
                    list_of_possible_moves.append(((piece_location[0] + (1+digit), piece_location[1] - (1+digit))))
                  elif grid.get((piece_location[0] + (1+digit), piece_location[1] - (1+digit))).startswith(anti_turn):
                    list_of_possible_moves.append(((piece_location[0] + (1+digit), piece_location[1] - (1+digit))))
                    break
                  elif grid.get((piece_location[0] + (1+digit), piece_location[1] - (1+digit))).startswith(turn):
                    break
                except : break
              #Queen move and capture logic on DIAG DOWN-RIGHT :
              for digit in range(row_length-1): 
                try :
                  if grid.get((piece_location[0] + (1+digit), piece_location[1] + (1+digit))) == "Empty" :
                    list_of_possible_moves.append(((piece_location[0] + (1+digit), piece_location[1] + (1+digit))))
                  elif grid.get((piece_location[0] + (1+digit), piece_location[1] + (1+digit))).startswith(anti_turn):
                    list_of_possible_moves.append(((piece_location[0] + (1+digit), piece_location[1] + (1+digit))))
                    break
                  elif grid.get((piece_location[0] + (1+digit), piece_location[1] + (1+digit))).startswith(turn):
                    break
                except : break
              return list_of_possible_moves
      def move_king(turn, piece_location, grid = playground):
                  list_of_possible_moves = []
                  
                  try :
                      if not grid.get((piece_location[0] - 1, piece_location[1] - 1 )).startswith(turn) :
                          list_of_possible_moves.append((piece_location[0] - 1, piece_location[1] - 1))
                  except : pass
                  try :
                      if not grid.get((piece_location[0] - 1, piece_location[1])).startswith(turn) :
                          list_of_possible_moves.append((piece_location[0] - 1, piece_location[1]))
                  except : pass
                  try :
                      if not grid.get((piece_location[0] - 1, piece_location[1] + 1)).startswith(turn) :
                          list_of_possible_moves.append((piece_location[0] - 1, piece_location[1] + 1))
                  except : pass
                  try :
                      if not grid.get((piece_location[0], piece_location[1] - 1 )).startswith(turn) :
                          list_of_possible_moves.append((piece_location[0], piece_location[1] - 1 ))
                  except : pass
                  try :
                      if not grid.get((piece_location[0], piece_location[1] + 1 )).startswith(turn) :
                          list_of_possible_moves.append((piece_location[0], piece_location[1] + 1 ))
                  except : pass
                  try :
                      if not grid.get((piece_location[0] + 1, piece_location[1] - 1 )).startswith(turn) :
                          list_of_possible_moves.append((piece_location[0] + 1, piece_location[1] - 1 ))
                  except : pass
                  try :
                      if not grid.get((piece_location[0] + 1, piece_location[1])).startswith(turn) :
                          list_of_possible_moves.append((piece_location[0] + 1, piece_location[1]))
                  except : pass
                  try :
                      if not grid.get((piece_location[0] + 1, piece_location[1] + 1)).startswith(turn) :
                          list_of_possible_moves.append((piece_location[0] + 1, piece_location[1] + 1))
                  except : pass
                  return list_of_possible_moves   

      def king_safety_check(grid, turn, anti_turn):
        king_position = list(grid.keys())[list(grid.values()).index(f"{turn}King1")]
        list_of_threat_to_king = []
      
        for coordinates, piece_ in grid.items():
          if piece_ == "Empty" or piece_.startswith(turn) :
            continue
          
          piece = piece_[1:-1]
          if piece == "Pawn":
            if turn == "B":
              if coordinates[1] < row_length :
                    list_of_threat_to_king.append((coordinates[0] - 1, coordinates[1] + 1))
              if coordinates[1] > 1 :
                    list_of_threat_to_king.append((coordinates[0] - 1, coordinates[1] - 1))
            elif turn == "W"  :
              if coordinates[1] < row_length :
                  list_of_threat_to_king.append((coordinates[0] + 1, coordinates[1] + 1))
              if coordinates[1] > 1 :
                  list_of_threat_to_king.append((coordinates[0] + 1, coordinates[1] - 1))     
                  
          if piece == "Rook":
            list_of_threat_temp = move_rook(anti_turn, turn, coordinates, grid)
            for threat in list_of_threat_temp :
              list_of_threat_to_king.append(threat)
              
          if piece == "Bishop":
            list_of_threat_temp = move_bishop(anti_turn, turn, coordinates, grid)
            for threat in list_of_threat_temp :
              list_of_threat_to_king.append(threat)
              
          if piece == "Knight":
            list_of_threat_temp = move_knight(anti_turn, coordinates, grid)
            for threat in list_of_threat_temp :
              list_of_threat_to_king.append(threat)
              
          if piece == "Queen":
            list_of_threat_temp = move_queen(anti_turn, turn, coordinates, grid)
            for threat in list_of_threat_temp :
              list_of_threat_to_king.append(threat)
              
          if piece == "King":
            list_of_threat_temp = move_king(anti_turn, coordinates, grid)
            for threat in list_of_threat_temp :
              list_of_threat_to_king.append(threat)
          
        if king_position in list_of_threat_to_king :
          return False
        else : 
          return True   
        
      # Checks if player is in pat :  
      def check_for_legal_moves(grid, turn, anti_turn):
        temp_grid = copy.deepcopy(grid)

        def filter_for_pieces_of_player(coordinates):
          if grid[coordinates].startswith(turn) :
            return True
          else : return False

        coordinates_of_pieces_to_test = filter(filter_for_pieces_of_player, grid)

        for coordinates in coordinates_of_pieces_to_test :

          if "Pawn" in grid[coordinates] :
            for move in move_pawn(turn, coordinates):
              temp_grid.update({coordinates : "Empty"})
              temp_grid.update({move : grid[coordinates]})
              if king_safety_check(temp_grid, turn, anti_turn) == False :
                temp_grid = copy.deepcopy(grid)
              else : return False

          elif "Rook" in grid[coordinates] :
            for move in move_rook(turn, anti_turn, coordinates):
              temp_grid.update({coordinates : "Empty"})
              temp_grid.update({move : grid[coordinates]}) 
              if king_safety_check(temp_grid, turn, anti_turn) == False :
                temp_grid = copy.deepcopy(grid)
              else : return False

          elif "Knight" in grid[coordinates] :
            for move in move_knight(turn, coordinates):
              temp_grid.update({coordinates : "Empty"})
              temp_grid.update({move : grid[coordinates]})
              if king_safety_check(temp_grid, turn, anti_turn) == False :
                temp_grid = copy.deepcopy(grid)
              else : return False

          elif "Bishop" in grid[coordinates] :
            for move in move_bishop(turn, anti_turn, coordinates):
              temp_grid.update({coordinates : "Empty"})
              temp_grid.update({move : grid[coordinates]})          
              if king_safety_check(temp_grid, turn, anti_turn) == False :
                temp_grid = copy.deepcopy(grid)
              else : return False

          elif "Queen" in grid[coordinates] :
            for move in move_queen(turn, anti_turn, coordinates):
              temp_grid.update({coordinates : "Empty"})
              temp_grid.update({move : grid[coordinates]})         
              if king_safety_check(temp_grid, turn, anti_turn) == False :
                temp_grid = copy.deepcopy(grid)
              else : return False

          elif "King" in grid[coordinates] :
            for move in move_king(turn, coordinates):
              temp_grid.update({coordinates : "Empty"})
              temp_grid.update({move : grid[coordinates]})
              if king_safety_check(temp_grid, turn, anti_turn) == False :
                temp_grid = copy.deepcopy(grid)
              else : return False

        return True
              
      #placeholder for better en-passant logic 1/2
      last_piece_to_move = ''
      pieces_that_moved = []
      def is_a_valid_en_passant_candidate(input):
        if input not in pieces_that_moved : 
          pieces_that_moved.append(input)
          return input
        else : 
          return ''
          

      #big game function with the logic for every pieces, called every turn.
      def move(turn, grid): 
        nonlocal list_of_elements_on_board
        nonlocal list_of_coordinates_on_board
        
      #handles player input like : "WPawn1" , also handles Resign and Score.
        def player_entry(turn):
          piece = ""
          while turn + piece not in list_of_elements_on_board :
            piece = input("\n" + "Write the name of the piece you wish to move (Pawn1 for exemple)" + "\n")
            if piece == "Resign":
              if turn == "W":
                print("\n" + "Black won !" + "\n")
                the_game()
              else :
                print("\n" + "White won !" + "\n")
                the_game()
            elif piece == "Advantage":
              def calculate_advantage(turn):
                list_of_friendly_pieces = []
                list_of_enemy_pieces = []
                for piece in list_of_elements_on_board :
                  if piece.startswith(turn):
                    list_of_friendly_pieces.append(piece[1:-1])
                  elif piece != "Empty":
                    list_of_enemy_pieces.append(piece[1:-1])
                player_score = list_of_friendly_pieces.count("Pawn")*2 + list_of_friendly_pieces.count("Bishop")*3 + list_of_friendly_pieces.count("Knight")*3 + list_of_friendly_pieces.count("Rook")*5 + list_of_friendly_pieces.count("Queen")*9
                opponent_score = list_of_enemy_pieces.count("Pawn")*2 + list_of_enemy_pieces.count("Bishop")*3 + list_of_enemy_pieces.count("Knight")*3 + list_of_enemy_pieces.count("Rook")*5 + list_of_enemy_pieces.count("Queen")*9
                score = player_score - opponent_score
                return score
              print("\n" + f"your Advantage is {calculate_advantage(turn)}")
            elif piece == "Help" :
              print("\n" + "Available commands are : PiecenamePiecenumber, Resign, Advantage, Help")
          return turn + piece
        player_input = player_entry(turn)
          
        #direct the input to the corresponding piece function
        def which_piece(player_input):
          piece = player_input[1:-1]
          piece_location = list_of_coordinates_on_board[list_of_elements_on_board.index(player_input)]

          #2checks if the selected piece has legal moves
          def has_possible_moves(list_of_possible_moves, piece_location):    
              if list_of_possible_moves == []:
                print("This piece has no available moves")
                move(turn, grid)
              else :
                where_to(list_of_possible_moves, piece_location)    
          #3present the player with a selection of possible moves for the selected piece, then delete the piece at old position and create the piece at the selected position (contains pawn promotion logic and en-passant logic)
          def where_to(list_of_possible_moves, piece_location):
            nonlocal last_piece_to_move
            dict_of_options = {}
            
            counter = 0
            for moves in list_of_possible_moves :
              counter +=1
              dict_of_options.update({str(counter) : moves})
              
            print("\n" + "your options are : " + "\n"  )
            for counter, moves in dict_of_options.items() :
              print(int(counter), " : ", moves)
            print("\n")
            new_coordinate_key = ""
            while new_coordinate_key not in dict_of_options:  
              new_coordinate_key = input(f"Where do you want {player_input} to move to ?" + "\n")
            print("\n")
            
            def pawn_promotion():
              nonlocal player_input
              dict_of_possible_promotions = {}
              list_of_possible_promotions = ["Queen", "Rook", "Bishop", "Knight"]
              if piece == "Pawn" :
                if player_input[:1] == "W" :
                  if dict_of_options.get(new_coordinate_key)[0] == 1 :
                    print("\n" + "Promote to a Queen, Rook, Bishop or Knight" + "\n")
                    counter = 0
                    for pieces in list_of_possible_promotions :
                      counter += 1
                      dict_of_possible_promotions.update({counter : pieces})
      
                    print("\n" + "your options are : " + "\n"  )
                    for pieces in dict_of_possible_promotions.items() :
                      print(pieces)
                      
                    player_selection = int(input(f"what are you promoting to? (1 to {len(list_of_possible_promotions)})" + "\n"))
                    new_player_input = player_input[:1] + dict_of_possible_promotions.get(player_selection) + "1"
                    counter = 1
                    while new_player_input in list_of_elements_on_board :
                      counter +=1 
                      new_player_input = new_player_input[:-1] + str(counter)
      
                    player_input = new_player_input
                    
        
                if player_input[:1] == "B"  :
                  if dict_of_options.get(new_coordinate_key)[0] == row_length :
                    print("\n" + "Promote to a Queen, Rook, Bishop or Knight" + "\n")
                    counter = 0
                    for pieces in list_of_possible_promotions :
                      counter += 1
                      dict_of_possible_promotions.update({counter : pieces})
      
                    print("\n" + "your options are : " + "\n"  )
                    for pieces in dict_of_possible_promotions.items() :
                      print(pieces)
                      
                    player_selection = int(input(f"what are you promoting to? (1 to {len(list_of_possible_promotions)})" + "\n"))
                    new_player_input = player_input[:1] + dict_of_possible_promotions.get(player_selection) + "1"
                    counter = 1
                    while new_player_input in list_of_elements_on_board :
                      counter +=1 
                      new_player_input = new_player_input[:-1] + str(counter)
      
                    player_input = new_player_input
            pawn_promotion()
            
            #placeholder for better en-passant logic 2/2
            if player_input[1:-1] == 'Pawn':
                if turn == "W" and grid[dict_of_options.get(new_coordinate_key)] == "Empty" :
                    try :
                        if grid[(dict_of_options.get(new_coordinate_key)[0] + 1, dict_of_options.get(new_coordinate_key)[1])] == last_piece_to_move :
                            grid.update({(dict_of_options.get(new_coordinate_key)[0] + 1, dict_of_options.get(new_coordinate_key)[1]) : "Empty"})
                    except : pass

                elif turn == "B" and grid[dict_of_options.get(new_coordinate_key)] == "Empty":
                    try :
                        if grid[(dict_of_options.get(new_coordinate_key)[0] - 1, dict_of_options.get(new_coordinate_key)[1])] == last_piece_to_move :
                            grid.update({(dict_of_options.get(new_coordinate_key)[0] - 1, dict_of_options.get(new_coordinate_key)[1]) : "Empty"})
                    except : pass
            last_piece_to_move = is_a_valid_en_passant_candidate(player_input)

            grid.update({piece_location : "Empty"})
            grid.update({dict_of_options.get(new_coordinate_key) : player_input}) 
          
          #1makes list of possible move if the selected piece is a Pawn
          if piece == "Pawn" :
            has_possible_moves(move_pawn(turn, piece_location), piece_location)
              
          #1makes list of possible move if the selected piece is a Rook
          elif piece == "Rook" :
            has_possible_moves(move_rook(turn, anti_turn, piece_location), piece_location)   
            
          #1makes list of possible move if the selected piece is a Bishop
          elif piece == "Bishop" :
            has_possible_moves(move_bishop(turn, anti_turn, piece_location), piece_location)    
                    
          #1makes list of possible move if the selected piece is a Knight
          elif piece == "Knight" :
            has_possible_moves(move_knight(turn, piece_location), piece_location)
                            
          #1makes list of possible move if the selected piece is a Queen
          elif piece == "Queen" :
            has_possible_moves(move_queen(turn, anti_turn, piece_location), piece_location)     
      
          #1makes list of possible move if the selected piece is a King  
          elif piece == "King" :
            has_possible_moves(move_king(turn, piece_location), piece_location)
          
        which_piece(player_input)


      #Game logic Alpha PLACEHOLDER 
      make_rollbackcopy(playground)
      update_grid(playground)
      def game_flow(playground):
          while True == True :
              if king_safety_check(playground, turn, anti_turn) == False :
                if check_for_legal_moves(playground, turn, anti_turn) == True :
                  def ask_to_play_again():
                    answer = ""
                    while answer != "Y" and answer != "N":
                      answer = input("\nDo you want to play again ? Y/N\n")
                    if answer == "Y":
                      print("\n")
                      the_game()
                    elif answer == "N":
                      print("\n Hope you had fun ! Goodbye !")
                  if turn == "W":
                    print("\n" + f"Black won on turn {turn_count} !\n")
                    ask_to_play_again()
                  if turn == "B":
                    print("\n" + f"White won on turn {turn_count} !\n")
                    ask_to_play_again()
              if king_safety_check(playground, turn, anti_turn) == True :
                if check_for_legal_moves(playground, turn, anti_turn) == True :
                    print("\n" + "it's a draw " + "\n")
                    ask_to_play_again()
              print("\n" + f"{turn} to move")
              if king_safety_check(playground, turn, anti_turn) == False :
                  print("\n" + "Your king is in check") 
              move(turn, playground)
              update_grid(playground)
              if king_safety_check(playground, turn, anti_turn) == False :
                  print("\n" + "This would put your king in check" + "\n") 
                  playground = copy.deepcopy(rollback_copy)
                  update_grid(playground)
                  print_grid(playground, row_length)
              else :
                  update_grid(playground)
                  print_grid(playground, row_length)
                  make_rollbackcopy(playground)
                  next_turn()
      game_flow(playground)
    
  game_logic(playground)
 
the_game()

   


       