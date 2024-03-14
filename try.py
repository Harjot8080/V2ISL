import nltk
from nltk import CFG, ChartParser

# Define a context-free grammar for English sentences in SOV format
english_sov_grammar = CFG.fromstring("""
    S -> NP VP
    NP -> Pronoun | ProperNoun | Det CommonNoun
    VP -> Verb NP | Verb
    Pronoun -> "I" | "you" | "he" | "she" | "it" | "we" | "they"
    ProperNoun -> "john" | "mary" | "alice" | "bob"
    Det -> "the" | "a"
    CommonNoun -> "book" | "cat" | "dog" | "ball" | "pen" | "house" | "apple"
    Verb -> "read" | "write" | "see" | "love" | "eat" | "throw" | "catch"
""")

# Function to rephrase a given English sentence into SOV format
def rephrase_to_sov(sentence):
    # Tokenize the sentence
    tokens = nltk.word_tokenize(sentence.lower())  # Convert to lowercase for easier parsing

    # Create a parser using the SOV grammar
    parser = ChartParser(english_sov_grammar)

    # Parse the sentence
    try:
        parsed_trees = parser.parse(tokens)
        for tree in parsed_trees:
            # Extract subject, object, and verb from the parse tree
            subject = ""
            object_ = ""
            verb = ""
            for subtree in tree.subtrees():
                if subtree.label() == "NP":
                    if not subject:
                        subject = " ".join(subtree.leaves())
                    else:
                        if not object_:
                            object_ = " ".join(subtree.leaves())
                        else:
                            object_ += " " + " ".join(subtree.leaves())
                elif subtree.label() == "Verb":
                    verb = " ".join(subtree.leaves())
            # Print the input sentence and rephrased sentence in SOV format
            print("Input sentence:", sentence)
            print("Rephrased sentence (SOV):", subject, object_, verb)
            break  # Only consider the first parse tree
    except ValueError as e:
        print("Parsing Error:", e)

# User input for English sentence
user_sentence = input("Enter an English sentence: ")

# Rephrase the user-provided sentence into SOV format
rephrase_to_sov(user_sentence)
