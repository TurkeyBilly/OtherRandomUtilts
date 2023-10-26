"""
Background: A substitution cipher is a cipher that replaces 
each letterin the alphabet with another letter. We keep track 
of which letter mapsto which using a key. A key is a jumbled 
version of the alphabet, wherethe first character replaces A,
the second character replaces B, etc. Forexample, using the 
key 'SOGYFEZXLANKJIMPURDCWTHVOB' would turnCAB'into 'GSQ'
With this in mind, write the function encodeSubstitutionCipher(msg,key) 
which takes a message and a key as described above, and returns
the encoded message. You can assume that the key uses uppercaseletters,
but case should be preserved when encoding the message.Non-letter 
characters should remain unchanged. For example, using the key
'SOGYFEZXLANKJIMPURDCWTHVOB' would turn 'Cab z?'into'Gsq B?
Only after you have written encodeSubstitutionCipher(msg, key)
write the function decodeSubstitutionCipher(encodedMsg, key)
which takes a message that has been encoded with the given key, and
returns the original decoded message.
"""


def encodeSub(msg: str, key: str) -> str:
    result = ""

    for char in msg:
        if not char.isalpha():
            result += char
            continue

        if char.isupper():
            state = "A"
        else:
            state = "a"

        position = ord(char) - ord(state)

        if char.isupper():
            result += key[position]
        else:
            result += key[position].lower()

    return result

# simplied version
def encodeSub(msg: str, key: str) -> str:
    result = ""

    for char in msg:
        if not char.isalpha():
            result += char
            continue

        origin = "A" if char.isupper() else "a"
        position = ord(char) - ord(origin)

        cipher_char = key[position] if char.isupper() else key[position].lower()
        result += cipher_char

    return result

assert encodeSub("Cab Z?", "SQGYFEZXLANKJIMPURDCWTHVOB") == "Gsq B?"
assert encodeSub("CAB", "SQGYFEZXLANKJIMPURDCWTHVOB") == "GSQ"

def decodeSub(encodedMsg: str, key: str) -> str:
    result = ""
    for char in encodedMsg:
        if not char.isalpha():
            result += char
            continue

        position = key.index(char.upper())
        origin = "A" if char.isupper() else "a"
        decoded_char = chr(ord(origin) + position)
        result += decoded_char
    
    return  result

assert decodeSub("Gsq B?", "SQGYFEZXLANKJIMPURDCWTHVOB") == "Cab Z?"