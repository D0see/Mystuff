def vigenere_cipher_decoder(keyword, message):
  alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

  keyword_value_list = []
  while len(keyword_value_list) < len(message):
    for letters in keyword:
      keyword_value_list.append(alphabet.index(letters))
      
  messageinlist = message.split(" ")
  message_decoded = []
  counter = 0
  for words in messageinlist:
    message_decoded.append(" ")
    for symbols in words:
      if symbols != "!" and symbols != "?" and symbols != "." and symbols != ",":
        decoded_symbol = alphabet[alphabet.index(symbols)+ keyword_value_list[counter]]
        message_decoded.append(decoded_symbol)
        counter +=1
      else:
        message_decoded.append(symbols)

  message_finalized = ""
  for symbols in message_decoded:
    message_finalized += symbols

  return message_finalized

print (vigenere_cipher_decoder("friends", "txm srom vkda gl lzlgzr qpdb? fepb ejac! ubr imn tapludwy mhfbz cza ruxzal wg zztcgcexxch!" ))



    
    







