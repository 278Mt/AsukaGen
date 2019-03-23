import pandas as pd
from janome.tokenizer import Tokenizer

# if you write "import pandas" sur "janome", it will be raised ERROR

def token_matrix(name):

    txt = "resources/"+name+".txt"
    with open(txt, mode="r") as file:
        messages = file.read().split("\n")

    messages_tokens = []
    tok = Tokenizer()
    for i in range(len(messages)):
        tokens = tok.tokenize(messages[i], wakati=True)

        messages_tokens.append(tokens)


    print(messages_tokens)


if __name__ == "__main__":

    name = "アスカ"
    token_matrix(name)
