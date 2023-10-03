import os, sys
from collections import deque

os.chdir(os.path.dirname(__file__))
print(os.getcwd())

print('Before starting place all the files you want to check in the script directory')
print('The most common words will be at least 4 characters long')

proceed = 'N'
while proceed != 'Y' :
    proceed = input('\n' + 'Type Y when ready' + '\n').upper()
print('\n')
print('---------------------------------------------')

list_of_files_in_directory = (os.listdir(os.path.join(os.path.dirname(__file__))))

files_to_check = []
for file in list_of_files_in_directory :
    if file.endswith('.txt') :
        files_to_check.append(file)
        
print(files_to_check)
print('---------------------------------------------')


for file_name in files_to_check :
    with open(file_name, 'r') as file :
        text = file.read()
        text_as_list = list(text)

        number_of_letters = 0
        number_of_spaces = 0
        number_of_special_chars = 0
        for letter in text :
            if letter.isalpha():
                number_of_letters += 1
            elif letter == ' ':
                number_of_spaces += 1
            elif letter.isascii() and letter != '\n':
                number_of_special_chars += 1
                if letter == '\'' or letter == '.' :
                    text_as_list[text_as_list.index(letter)] =  ' '
                else :
                    text_as_list.remove(letter)

        number_of_words = 0
        previous_letter = ' '
        for letter in text_as_list :
            if letter == ' ' and previous_letter == ' ':
                previous_letter = letter 
            elif letter.isalpha() and previous_letter == ' ':
                number_of_words += 1
                previous_letter = letter
            else :
                previous_letter = letter

        text_without_special_chars = ''
        for elem in text_as_list :
            text_without_special_chars += elem.upper()
        list_text_without_special_chars = text_without_special_chars.split(' ')
        list_of_unique_words = deque(set(list_text_without_special_chars))
        list_of_unique_words.popleft()

        list_of_elem_to_remove = []
        for elem in list_of_unique_words :
            if len(elem) < 4 :
                list_of_elem_to_remove.append(elem)
        for elem in list_of_elem_to_remove :
            if elem in list_of_unique_words :
                list_of_unique_words.remove(elem)


        def get_most_common_word(list_of_unique_words, list_text_without_special_chars) :
            most_common_word = []
            most_common_word_occurence = 0
            for word in list_of_unique_words:
                if list_text_without_special_chars.count(word) > most_common_word_occurence :
                    most_common_word = [word]
                    most_common_word_occurence = list_text_without_special_chars.count(word)
                elif list_text_without_special_chars.count(word) == most_common_word_occurence :
                    most_common_word.append(word)
                else : 
                    continue
            return most_common_word, most_common_word_occurence
        
        def remove_word(list_of_unique_words, word : list):
            for elem in word :
                list_of_unique_words.remove(elem)

        most_common_word, most_common_word_occurence = get_most_common_word(list_of_unique_words, list_text_without_special_chars)
        remove_word(list_of_unique_words, most_common_word)            

        second_most_common_word, second_most_common_word_occurence = get_most_common_word(list_of_unique_words, list_text_without_special_chars)
        remove_word(list_of_unique_words, second_most_common_word) 

        third_most_common_word, third_most_common_word_occurence = get_most_common_word(list_of_unique_words, list_text_without_special_chars)
     
        




        print('\n')
        print(f'{file_name} :')
        print('number of letters =', number_of_letters)
        print('number of spaces =', number_of_spaces)
        print('number of special characters =', number_of_special_chars)
        print('number of words = ', number_of_words)
        print('most common word(s) =', most_common_word, f'appearing {most_common_word_occurence} times')
        print('second most common word(s) =', second_most_common_word, f'appearing {second_most_common_word_occurence} times')
        print('third most common word(s) =', third_most_common_word, f'appearing {third_most_common_word_occurence} times')
        print('\n')
        print('---------------------------------------------')

def file_search():
    user_input = input('type the exact sentence to search for \n')
    match_for_user_input = []
    for file_name in files_to_check :
        with open(file_name, 'r') as file :
            text = file.read()
            if user_input in text :
                match_for_user_input.append(file_name)

    print(f'your input appear in {match_for_user_input}')
    file_search()

file_search()

