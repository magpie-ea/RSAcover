import csv
import pandas as pd
import numpy as np

def encode_subject(NPforms, Grouped, Color1, Color2, Shape1, Shape2):
    if NPforms == "sum":
        realised_subject = "The objects"
    else:
        if Grouped == "Color":
            realised_subject = f"The {Color1} and the {Color2} ones"
        else:
            realised_subject = f"The {Shape1}s and the {Shape2}s"
    return realised_subject

def generate_experiment_sentences(source_file = "../items/items.csv", target_file = "../items/items_w.Sentence.csv"):
    df = pd.read_csv(source_file, encoding="utf-8").reset_index(drop=True)
    print(df.head())

    for i, row in df.iterrows():
        realised_subject = encode_subject(row.F1_NPforms, row.Grouped, row.Color1, row.Color2, row.Shape1, row.row.Shape2)
        realised_predicate = "separated" if row.Predicate == "separated" else "grouped"
        realised_sentence = f"{realised_subject} are {realised_predicate}."
        df.loc[i, 'linguisticContext'] = realised_sentence
    return df, target_file

def main():
    # Set seed for reproducibility
    # The seed used for the experiment was 1
    np.random.seed(1)

    # Generate sentences for the practice trials
    # df_practice, target_file_practice = generate_experiment_sentences(source_file="all_practice_stimuli_without_sentences.csv", target_file="all_practice_stimuli_with_sentences.csv")
    # df_practice.to_csv(target_file_practice, encoding="utf-8", index=False)

    # Generate sentences for the experiment trials
    df_experiment, target_file_experiment = generate_experiment_sentences()
    df_experiment.to_csv(target_file_experiment, encoding="utf-8", index=False)

if __name__=='__main__':
    main()