from generate_pictures import generate_experiment_stimuli
from generate_sentences import generate_experiment_sentences
import numpy as np
import pandas as pd

def main():

    # Set seed for reproducibility
    # The seed used for the experiment was 1
    np.random.seed(1)

    # Generate the stimuli for the practice trials
    stimuli_tables = 'stimuli_tables'

    # Generate sentences for the practice trials
    df_practice, target_file_practice = generate_experiment_sentences(source_file=f"{stimuli_tables}/all_practice_stimuli_without_sentences.csv", target_file=f"{stimuli_tables}/all_practice_stimuli_with_sentences.csv")
    df_practice.to_csv(target_file_practice, encoding="utf-8", index=False)

    # Generate sentences for the experiment trials
    df_experiment, target_file_experiment = generate_experiment_sentences(source_file=f"{stimuli_tables}/all_stimuli_without_sentences.csv", target_file=f"{stimuli_tables}/all_stimuli_with_sentences.csv")
    df_experiment.to_csv(target_file_experiment, encoding="utf-8", index=False)

    # Generate sentences for the practice trials
    generate_experiment_stimuli(source_file=f"{stimuli_tables}/all_practice_stimuli_with_sentences.csv", output_file=f"{stimuli_tables}/all_practice_stimuli_final.csv", practice=True)
    
    # Generate sentences for the experiment trials
    generate_experiment_stimuli(source_file=f"{stimuli_tables}/all_stimuli_with_sentences.csv", output_file=f"{stimuli_tables}/all_stimuli_final.csv")

if __name__ == "__main__":
    main()