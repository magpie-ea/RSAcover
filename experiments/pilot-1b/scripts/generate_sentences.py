import csv
import pandas as pd
import numpy as np

def encode_subject(NPforms, Grouped, Color1, Color2, Shape1, Shape2):
    if NPforms == "sum":
        realised_subject = "The shapes"
    else:
        if Grouped == "Color":
            realised_subject = f"The {Color1} shapes and the {Color2} shapes"
        else:
            realised_subject = f"The {Shape1}s and the {Shape2}s"
    return realised_subject

def convert_number_to_word(n):
    num_words = {
        0: "zero",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine"
    }
    return num_words.get(n, "Number out of range")

def generate_experiment_sentences(source_file = "../experiments/pilot-1/trials/items.csv", target_file = "../experiments/pilot-1/trials/items.csv"):
    df = pd.read_csv(source_file, encoding="utf-8").reset_index(drop=True)
    print(df.head())
    fillerNr_list = list(range(901, 925))
    for i, row in df.iterrows():
        if row.itemNr not in fillerNr_list:
            realised_subject = encode_subject(row.F1_NPforms, row.Grouped, row.Color1, row.Color2, row.Shape1, row.Shape2)
        elif row.F1_NPforms == "+filler":
            if row.F2_matchness == "first":
                if row.Grouped == "Color":
                    realised_subject = f"The {convert_number_to_word(row.Number1)} {row.Color1} objects"
                else:
                    realised_subject = f"The {convert_number_to_word(row.Number1)} {row.Shape1}s"
            else:
                if row.Grouped == "Color":
                    realised_subject = f"The {convert_number_to_word(row.Number2)} {row.Color2} objects"
                else:
                    realised_subject = f"The {convert_number_to_word(row.Number2)} {row.Shape2}s"
        elif row.F1_NPforms == "-filler":
            if row.F2_matchness == "first":
                random_number = np.random.choice([i for i in range(row.Number1, 9)])
                if row.Grouped == "Color":
                    realised_subject = f"The {convert_number_to_word(random_number)} {row.Color1} objects"
                else:
                    realised_subject = f"The {convert_number_to_word(random_number)} {row.Shape1}s"
            else:
                random_number = np.random.choice([i for i in range(row.Number2, 9)])
                if row.Grouped == "Color":
                    realised_subject = f"The {convert_number_to_word(random_number)} {row.Color2} objects"
                else:
                    realised_subject = f"The {convert_number_to_word(random_number)} {row.Shape2}s"
        
        realised_predicate = "separated" if row.Predicate == "separated" else "grouped"
        realised_sentence = f"{realised_subject} are {realised_predicate}."
        df['linguisticContext'] = df['linguisticContext'].astype(str)
        df.at[i, 'linguisticContext'] = str(realised_sentence)
    
    return df, target_file

def main():
    # Set seed for reproducibility
    # The seed used for the experiment was 1
    np.random.seed(1)

    # Generate sentences for the practice trials
    # df_practice, target_file_practice = generate_experiment_sentences(source_file="all_practice_stimuli_without_sentences.csv", target_file="all_practice_stimuli_with_sentences.csv")
    # df_practice.to_csv(target_file_practice, encoding="utf-8", index=False)

    # Generate sentences for the experiment trials
    df_experiment, target_file_experiment = generate_experiment_sentences(source_file="../trials/items.csv", target_file="../trials/items.csv")
    df_experiment.to_csv(target_file_experiment, encoding="utf-8", index=False)

if __name__=='__main__':
    main()