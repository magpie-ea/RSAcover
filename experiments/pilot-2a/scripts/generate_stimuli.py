import numpy as np
import pandas as pd
import argparse
import os
import csv
import random
import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import entropy
    
def generate_experiment_sentences(source_file_path, target_file_path):
    '''
    Generate the experiment sentences based on the provided CSV file.
    The function reads the CSV file, processes the data, and generates sentences
    based on the specified conditions. The generated sentences are then saved
    back to the CSV file.

    Parameters:
    source_file_path (str): Path to the source CSV file containing the data.
    target_file_path (str): Path to the target CSV file where the generated sentences will be saved.
    '''
    color_list = ["red", "green", "blue", "yellow", "grey", "orange", "brown", "purple"]
    shape_list = ["circles", # circle
                    "crosses", # cross
                    "squares", # square
                    "triangles", # triangle
                    "diamonds", # diamond
                    "stars"] # star
    df = pd.read_csv(source_file_path, encoding="utf-8").reset_index(drop=True)
    print(df.head())
    itemNr_list = list(range(1, 145)) + list(range(801,804))
    filler_itemNr_list = list(range(901, 925))
    for i, row in df.iterrows():
            # Write the sampled colors and shapes to the dataframe
        if row.alternative == "no":
                colors = random.sample(color_list, 2)
                shapes  = random.sample(shape_list, 2)
        else:
                colors = random.sample(color_list, 3)
                shapes  = random.sample(shape_list, 2)
        
        row.Color1 = colors[0]
        row.Color2 = colors[1]
        row.Shape1 = shapes[0]
        row.Shape2 = shapes[1] if row.alternative == "yes" else None
        row.Color3 = colors[2] if row.alternative == "yes" else None

        # Realise the subject based on the NPforms and Sampled colors and shapes for experiment items
        if row.itemNr in itemNr_list:
            # Realise the subject based on the NPforms and Sampled colors and shapes
            if row.F1_NP == "definiteP":
                realised_subject = f"The {row.Shape1}"
            elif row.F1_NP == "conjunction":
                realised_subject = f"The {row.Color1} {row.Shape1} and the {row.Color2} {row.Shape1}"

            realised_predicate = "grouped"
            realised_sentence = f"{realised_subject} are {realised_predicate}."
            
            df.at[i, 'Color1'] = str(colors[0])
            df.at[i, 'Color2'] = str(colors[1])
            df.at[i, 'Shape1'] = str(shapes[0])
            df.at[i, 'Shape2'] = str(shapes[1]) if row.alternative == "yes" else None
            df.at[i, 'Color3'] = str(colors[2]) if row.alternative == "yes" else None

        # Realise the subject based on the NPforms and Sampled colors and shapes for filler items
        if row.itemNr in filler_itemNr_list:
            if row.F1_NP == 'all':
                if row.is_filler == "yes_true":
                    df.at[i, 'Color1'] = colors[0]
                    df.at[i, 'Color2'] = colors[0]
                    df.at[i, 'Shape1'] = shapes[0]
                    realised_sentence = f"All of the {shapes[0]} are {colors[0]}."
                
                if row.is_filler == "yes_false":
                    shape = shapes[0]
                    color = colors[0]
                    df.at[i, 'Color1'] = color
                    df.at[i, 'Color2'] = color
                    df.at[i, 'Shape1'] = shape
                    realised_sentence = f"All of the {shape} are {colors[1]}."
            
            if row.F1_NP == 'some':
                if row.is_filler == "yes_true":
                    shape = shapes[0]
                    color = colors[0]
                    df.at[i, 'Color1'] = colors[0]
                    df.at[i, 'Color2'] = colors[1]
                    df.at[i, 'Shape1'] = shape
                    realised_sentence = f"Some of the {shape} are {colors[0]}."
                
                if row.is_filler == "yes_false":
                    shape = shapes[0]
                    color = colors[0]
                    df.at[i, 'Color1'] = colors[0]
                    df.at[i, 'Color2'] = colors[0]
                    df.at[i, 'Shape1'] = shape
                    realised_sentence = f"Some of the {shape} are {colors[1]}."

        # Save the generated sentences to the dataframe
        df['linguisticContext'] = df['linguisticContext'].astype(str)
        df.at[i, 'linguisticContext'] = str(realised_sentence)
        df.to_csv(target_file_path, encoding="utf-8", index=False)
    return df


# --- Helper functions ---

def get_quadrant_center(quadrant, canvas_size=10):
    half = canvas_size / 2
    offset = half / 2
    centers = {
        1: (offset, canvas_size - offset),
        2: (canvas_size - offset, canvas_size - offset),
        3: (offset, offset),
        4: (canvas_size - offset, offset)
    }
    return centers[quadrant]

def compute_color_entropy(colors):
    values, counts = np.unique(colors, return_counts=True)
    probs = counts / counts.sum()
    return entropy(probs, base=2)

def compute_spatial_entropy(points, canvas_size=10, grid_size=10):
    hist, _, _ = np.histogram2d(points[:, 0], points[:, 1],
                                 bins=grid_size,
                                 range=[[0, canvas_size], [0, canvas_size]])
    probs = hist.flatten() / hist.sum()
    probs = probs[probs > 0]
    return entropy(probs, base=2)

def apply_quadrant_padding(points, center, canvas_size, padding=0.8):
    """Clamp points to remain within quadrant bounds, respecting padding."""
    half = canvas_size / 2
    offset = half / 2
    min_x = center[0] - offset + padding
    max_x = center[0] + offset - padding
    min_y = center[1] - offset + padding
    max_y = center[1] + offset - padding

    # Clamp all points to stay within this bounding box
    points[:, 0] = np.clip(points[:, 0], min_x, max_x)
    points[:, 1] = np.clip(points[:, 1], min_y, max_y)
    return points

# --- Main function ---

def generate_cluster_with_alternative(df,
                                      min_dots=30, max_dots=60,
                                      alt_min=10, alt_max=25,
                                      spread=0.5, radius=10, padding=0.8,
                                      canvas_size=10, screen_size=5):
    '''
    Generate scatter plots with clusters of dots based on the provided DataFrame.
    The function creates scatter plots with different colors and shapes based on the
    specified conditions. The generated plots are saved as PNG files.
    The function also calculates color and spatial entropy for the generated clusters.
    Parameters:
    df (pd.DataFrame): DataFrame containing the data for generating clusters.
    min_dots (int): Minimum number of dots in the main cluster.
    max_dots (int): Maximum number of dots in the main cluster.
    alt_min (int): Minimum number of dots in the alternative cluster.
    alt_max (int): Maximum number of dots in the alternative cluster.
    spread (float): Spread of the dots in the clusters.
    radius (int): Radius of the dots in the scatter plot.
    canvas_size (int): Size of the canvas for the scatter plot.
    screen_size (int): Size of the screen for the scatter plot.
    Returns:
    df (pd.DataFrame): Updated DataFrame with color and spatial entropy values.
    '''
    shape_dict = {
        "circles": "o",
        "crosses": "P",
        "squares": "s",
        "triangles": "^",
        "diamonds": "D",
        "stars": "*"
    }

    color_entropies = []
    spatial_entropies = []

    for i, row in df.iterrows():
        has_alt = str(row['alternative']).strip().lower() == "yes"
        vis_type = str(row['F2_visual']).strip().lower()

        colors = [row['Color1'], row['Color2']]
        shapes = [row['Shape1']]
        if has_alt:
            colors.append(row['Color3'])
            shapes.append(row['Shape2'])

        shapes = [shape_dict.get(s.strip().lower(), "o") for s in shapes]
        used_quadrants = []
        num_main_dots = np.random.randint(min_dots, max_dots + 1)

        padding = 0.8  # set desired padding inside each quadrant

        # --- Main cluster generation ---
        if vis_type == "notgrouped" and not has_alt:
            num_main_dots = num_main_dots // 2
            center_main = (canvas_size / 2, canvas_size / 2)
            dots_main = np.random.randn(num_main_dots, 2) * spread + np.array(center_main)
            dots_main = apply_quadrant_padding(dots_main, center_main, canvas_size, padding = 0.5)
            color_choices = np.random.choice(colors[:2], num_main_dots)
            dots_main_parts = [(dots_main, color_choices)]

        elif vis_type == "notgrouped":
            main_quadrant = random.choice([q for q in range(1, 5) if q not in used_quadrants])
            center_main = get_quadrant_center(main_quadrant, canvas_size)
            used_quadrants.append(main_quadrant)
            dots_main = np.random.randn(num_main_dots, 2) * spread + np.array(center_main)
            dots_main = apply_quadrant_padding(dots_main, center_main, canvas_size, padding)
            color_choices = np.random.choice(colors[:2], num_main_dots)
            dots_main_parts = [(dots_main, color_choices)]

        elif vis_type in ["colorgrouped", "randomgrouped"]:
            main_quadrants = random.sample([q for q in range(1, 5) if q not in used_quadrants], 2)
            used_quadrants.extend(main_quadrants)
            center_main_1 = get_quadrant_center(main_quadrants[0], canvas_size)
            center_main_2 = get_quadrant_center(main_quadrants[1], canvas_size)
            n1 = num_main_dots // 2
            n2 = num_main_dots - n1
            dots1 = np.random.randn(n1, 2) * spread + np.array(center_main_1)
            dots2 = np.random.randn(n2, 2) * spread + np.array(center_main_2)
            dots1 = apply_quadrant_padding(dots1, center_main_1, canvas_size, padding)
            dots2 = apply_quadrant_padding(dots2, center_main_2, canvas_size, padding)
            if vis_type == "colorgrouped":
                dots_main_parts = [
                    (dots1, np.array([colors[0]] * n1)),
                    (dots2, np.array([colors[1]] * n2))
                ]
            else:
                c1 = np.random.choice(colors[:2], n1)
                c2 = np.random.choice(colors[:2], n2)
                dots_main_parts = [
                    (dots1, c1),
                    (dots2, c2)
                ]

        # --- Alternative cluster (if applicable) ---
        if has_alt:
            remaining_quadrants = [q for q in range(1, 5) if q not in used_quadrants]
            alt_quadrant = random.choice(remaining_quadrants)
            used_quadrants.append(alt_quadrant)
            center_alt = get_quadrant_center(alt_quadrant, canvas_size)
            num_alt_dots = np.random.randint(alt_min, alt_max + 1)
            dots_alt = center_alt + spread * np.random.randn(num_alt_dots, 2)
            dots_alt = apply_quadrant_padding(dots_alt, center_alt, canvas_size, padding)
            alt_color = colors[2]
            alt_shape = shapes[1]
        else:
            dots_alt = np.empty((0, 2))
            alt_color = None
            alt_shape = None

        # --- Plotting and entropy calculation ---
        all_points = []
        all_colors = []

        fig, ax = plt.subplots(figsize=(screen_size, screen_size))
        fig.patch.set_facecolor("lightgrey")
        ax.set_facecolor("lightgrey")

        for dots, color_array in dots_main_parts:
            for color in np.unique(color_array):
                indices = color_array == color
                ax.scatter(dots[indices, 0], dots[indices, 1],
                           c=color, alpha=0.9,
                           marker=shapes[0],
                           s=radius**2,
                           edgecolor='black', linewidth=1)
                all_points.append(dots[indices])
                all_colors.extend(color_array[indices])

        if has_alt and len(dots_alt) > 0:
            ax.scatter(dots_alt[:, 0], dots_alt[:, 1],
                       c=alt_color, alpha=0.9,
                       marker=alt_shape,
                       s=radius**2,
                       edgecolor='black', linewidth=1)
            all_points.append(dots_alt)
            all_colors.extend([alt_color] * len(dots_alt))

        ax.set_xlim(0, canvas_size)
        ax.set_ylim(0, canvas_size)
        ax.axis('off')

        os.makedirs("../pictures/", exist_ok=True)
        filename = f"../pictures/img_l{row['List']}_i{row['itemNr']}.png"
        plt.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close()

        # --- Entropy calculations ---
        points_array = np.vstack(all_points)
        color_entropy = compute_color_entropy(all_colors)
        spatial_entropy = compute_spatial_entropy(points_array, canvas_size)

        color_entropies.append(color_entropy)
        spatial_entropies.append(spatial_entropy)

    df['color_entropy'] = color_entropies
    df['spatial_entropy'] = spatial_entropies

    return df

def main():

    # Set seed for reproducibility
    # The seed used for the experiment was 1
    np.random.seed(1)

    # Define the command line arguments
    source_file_path = "../trials/items.csv"
    target_file_path = "../trials/items.csv"

    # Generate the stimuli
    df = generate_experiment_sentences(source_file_path, target_file_path)

    # Generate the scatter plots
    df = generate_cluster_with_alternative(df,
                                       min_dots=12, max_dots=20,
                                       alt_min=5, alt_max=10,
                                       spread=0.5, radius=12,
                                       padding=0.8,
                                       canvas_size=5, screen_size=5)
    
    # Save the updated dataframe to a new CSV file
    df.to_csv(target_file_path, encoding="utf-8", index=False)
    print("Stimuli generation completed.")

if __name__ == "__main__":
    main()