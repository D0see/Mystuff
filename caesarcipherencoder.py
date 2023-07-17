def caesar_cipher_encoder(offset, message):

  alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
  messageinlist = message.split(" ")
  message_decoded = []
  
  for words in messageinlist :
    word_decoded=[]
    message_decoded.append(word_decoded)
    for symbols in words :
      if symbols != "!" and symbols != "?" and symbols != ".":
        letters_decoded = alphabet[alphabet.index(symbols)-offset]
        word_decoded.append(letters_decoded)
      else :
        word_decoded.append(symbols)
  
  message_finalized = []
  
  for words in message_decoded:
    joined_words = ""
    for letters in words:
      joined_words += letters
      if len(words) == len(joined_words):
        message_finalized.append(joined_words)
  
  final_message = (" ").join(message_finalized)
  return final_message

