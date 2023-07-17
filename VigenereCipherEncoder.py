def vigenere_cipher_encoder(keyword, message):
  alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

  keyword_value_list = []
  while len(keyword_value_list) < len(message):
    for letters in keyword:
      keyword_value_list.append(alphabet.index(letters))
      
  messageinlist = message.split(" ")
  message_encoded = []
  counter = 0
  for words in messageinlist:
    message_encoded.append(" ")
    for symbols in words:
      if symbols != "!" and symbols != "?" and symbols != "." and symbols != "," and symbols != "'":
        encoded_symbol = alphabet[alphabet.index(symbols)- keyword_value_list[counter]]
        message_encoded.append(encoded_symbol)
        counter +=1
      else:
        message_encoded.append(symbols)

  message_finalized = ""
  for symbols in message_encoded:
    message_finalized += symbols

  return message_finalized

print (vigenere_cipher_encoder("chameaudecampagne", "bonjour j'aime beaucoup les animaux les chenilles et les cheveaux" ))





    
    









    
    







