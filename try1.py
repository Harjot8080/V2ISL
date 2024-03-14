import nltk
from nltk import CFG, ChartParser

# Function to generate a CFG from a list of terminals
def generate_grammar(terminals):
    grammar_rules = []
    for term in terminals:
        rule = f"{term[1].upper()} -> '{term[0].lower()}'"
        grammar_rules.append(rule)
    grammar_str = "\n".join(grammar_rules)
    return CFG.fromstring(grammar_str)

# Function to rephrase a given English sentence into SOV format
def rephrase_to_sov(sentence, pos_tags):
    # Generate a CFG dynamically from the input sentence's terminals
    grammar = generate_grammar(pos_tags)

    # Define a context-free grammar for English sentences in SOV format
    english_sov_grammar = CFG.fromstring("""
        S -> NP VP
        NP -> Pronoun | ProperNoun | Det CommonNoun
        VP -> Verb NP | Verb
        Pronoun -> PRP | PRP$ | WP | WP$ | EX
        ProperNoun -> NNP | NNPS
        Det -> DT | PDT | WDT
        CommonNoun -> NN | NNS | WP
        Verb -> VB | VBD | VBG | VBN | VBP | VBZ | MD
    """)

    # Create a parser using the SOV grammar
    parser = ChartParser(english_sov_grammar)

    # Parse the sentence
    try:
        parsed_trees = parser.parse([pos for _, pos in pos_tags])
        for tree in parsed_trees:
            # Extract subject, object, and verb from the parse tree
            subject = ""
            object_ = ""
            verb = ""
            for subtree in tree.subtrees():
                if subtree.label() == "NP":
                    if not subject:
                        subject = " ".join(pos_tags[i][0] for i in range(len(pos_tags)) if pos_tags[i][1] == "NP")
                    else:
                        if not object_:
                            object_ = " ".join(pos_tags[i][0] for i in range(len(pos_tags)) if pos_tags[i][1] == "NP")
                        else:
                            object_ += " " + " ".join(pos_tags[i][0] for i in range(len(pos_tags)) if pos_tags[i][1] == "NP")
                elif subtree.label() == "Verb":
                    verb = " ".join(pos_tags[i][0] for i in range(len(pos_tags)) if pos_tags[i][1] == "Verb")
            # Print the input sentence and rephrased sentence in SOV format
            print("Input sentence:", sentence)
            print("Rephrased sentence (SOV):", subject, object_, verb)
            break  # Only consider the first parse tree
    except ValueError as e:
        print("Parsing Error:", e)

# User input for English sentence with part-of-speech tags
user_sentence = input("Enter an English sentence with part-of-speech tags (e.g., John/NN loves/VB the/DT cat/NN): ")

# Split user input into words and part-of-speech tags
pos_tags = [pair.split("/") for pair in user_sentence.split()]

# Rephrase the user-provided sentence into SOV format
rephrase_to_sov(user_sentence, pos_tags)
