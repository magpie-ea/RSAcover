import csv
import pandas as pd
import numpy as np


# Encode the color with case marker
def encode_color(color, case, presence=True):
    if presence:
        if case == "Dat.":
            if color == "braun":
                return "braunen*"
            elif color == "blau":
                return "blauen*"
            elif color == "schwarz":
                return "schwarzen*"
            elif color == "orange":
                return "orangen*"
        else:
            if color == "braun":
                return "braune*"
            elif color == "blau":
                return "blaue*"
            elif color == "schwarz":
                return "schwarze*"
            elif color == "orange":
                return "orange*"
    else:
        return ""

def encode_trajector_color(color):
    if color == "braun":
        return "braune"
    elif color == "blau":
        return "blaue"
    elif color == "schwarz":
        return "schwarze"
    elif color == "orange":
        return "orange"

def encode_preposition(rotation, semantic = True):
    if semantic:
        if rotation == 0:
            return "unter" if np.random.binomial(n = 1, p = 0.5) else "rechts von"
        elif rotation == 1:
            return "unter" if np.random.binomial(n = 1, p = 0.5) else "links von"
        elif rotation == 2:
            return "über" if np.random.binomial(n = 1, p = 0.5) else "links von"
        elif rotation == 3:
            return "über" if np.random.binomial(n = 1, p = 0.5) else "rechts von"
    else: 
        if rotation == 0:
            return "über" if np.random.binomial(n = 1, p = 0.5) else "links von"
        elif rotation == 1:
            return "über" if np.random.binomial(n = 1, p = 0.5) else "rechts von"
        elif rotation == 2:
            return "unter" if np.random.binomial(n = 1, p = 0.5) else "rechts von"
        elif rotation == 3:
            return "unter" if np.random.binomial(n = 1, p = 0.5) else "links von"
        
def encode_verb(verb):
    if verb == "Sein":
        return "ist"
    else:
        return "befindet sich"

def encode_article(nomen, case):
    if case == "Nom.":
        if nomen == "Kreuz" or nomen == "Quadrat" or nomen == "Dreieck":
            return f"das"
        elif nomen == "Kreis" or nomen == "Stern":
            return f"der"
    elif case == "Dat.":
       return "dem"


def generate_experiment_sentences(source_file = "all_stimuli_without_sentences.csv", target_file = "all_stimuli_with_sentences.csv"):
    df = pd.read_csv(source_file, encoding="latin-1", sep=";").reset_index(drop=True)
    print(df.head())

    for i, row in df.iterrows():
        # Encode preposition, verb, color, form, and article
        preposition = encode_preposition(row.rotation_number)
        verb = encode_verb(row.Verb)
        landmark_form = row.Referenzobjekte
        trajector_form = row.Zielobjekte
        trajector_color = row.Farbe_Trajector_1
        landmark_color = row.Farbe_Landmark_1
        article = encode_article(trajector_form, "Nom.")
        overspecification_1 = np.random.binomial(n = 1, p = 0.2)
        overspecification_2 = np.random.binomial(n = 1, p = 0.2)
        df.loc[i, 'preposition'] = preposition

        if (row.second_reference == "N") & (row.second_trajector == "N"):
            trajector_color = encode_color(trajector_color,"Nom.",overspecification_1)
            landmark_color = encode_color(landmark_color,"Dat.",overspecification_2)
            df.loc[i, 'Satz'] = f"{article.capitalize()}*{trajector_color}{trajector_form}*{verb}*{preposition}*dem*{landmark_color}{landmark_form}."
        elif (row.second_reference == "Y") & (row.second_trajector == "N"):
            trajector_color = encode_color(trajector_color,"Nom.",overspecification_1)
            landmark_color = encode_color(landmark_color,"Dat.")
            df.loc[i, 'Satz'] = f"{article.capitalize()}*{trajector_color}{trajector_form}*{verb}*{preposition}*dem*{landmark_color}{landmark_form}."
        elif (row.second_reference == "N") & (row.second_trajector == "Y"):
            trajector_color = encode_color(trajector_color,"Nom.")
            landmark_color = encode_color(landmark_color,"Dat.",overspecification_2)
            df.loc[i, 'Satz'] = f"{article.capitalize()}*{trajector_color}{trajector_form}*{verb}*{preposition}*dem*{landmark_color}{landmark_form}."
        elif (row.second_reference == "Y") & (row.second_trajector == "Y"):
            trajector_color = encode_color(trajector_color,"Nom.")
            landmark_color = encode_color(landmark_color,"Dat.")
            df.loc[i, 'Satz'] = f"{article.capitalize()}*{trajector_color}{trajector_form}*{verb}*{preposition}*dem*{landmark_color}{landmark_form}."   
        
        if row.Condition == "F1":
            df.loc[i, 'Satz'] = f"{article.capitalize()}*{trajector_form}*{verb}*{preposition}*dem*{landmark_color}{landmark_form}."

        if row.Condition == "F2":
            preposition = encode_preposition(row.rotation_number, semantic=False)
            df.loc[i, 'Satz'] = f"{article.capitalize()}*{trajector_color}{trajector_form}*{verb}*{preposition}*dem*{landmark_color}{landmark_form}."

        if row.Condition == "F3":
            df.loc[i, 'Satz'] = f"{preposition.capitalize()}*dem*{landmark_color}{landmark_form}*{verb}*{article}*{trajector_color}{trajector_form}."

    return df, target_file
    #print(df.head())
    #df.to_csv("all_stimuli_with_sentences.csv", encoding="utf-8", index=False)

def main():
    # Set seed for reproducibility
    # The seed used for the experiment was 1
    np.random.seed(1)

    # Generate sentences for the practice trials
    df_practice, target_file_practice = generate_experiment_sentences(source_file="all_practice_stimuli_without_sentences.csv", target_file="all_practice_stimuli_with_sentences.csv")
    df_practice.to_csv(target_file_practice, encoding="utf-8", index=False)

    # Generate sentences for the experiment trials
    df_experiment, target_file_experiment = generate_experiment_sentences(source_file="all_stimuli_without_sentences.csv", target_file="all_stimuli_with_sentences.csv")
    df_experiment.to_csv(target_file_experiment, encoding="utf-8", index=False)

if __name__=='__main__':
    main()