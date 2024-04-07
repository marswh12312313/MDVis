import pandas as pd
import matplotlib.pyplot as plt
import argparse

def load_data(file_path):
    """Loads RMSD data from a .dat file."""
    return pd.read_csv(file_path, delim_whitespace=True, skiprows=2)

def merge_data(data_path_1, data_path_2):
    """Merges the RMSD data from two .dat files based on the frame column."""
    data_1 = load_data(data_path_1)
    data_2 = load_data(data_path_2)
    data_1.columns = ['Frame', 'Protein_RMSD']
    data_2.columns = ['Frame', 'Ligand_RMSD']
    return pd.merge(data_1, data_2, on='Frame')

def plot_rmsd(data, title='Nucleic-Protein RMSD', protein_color='#1D2B53', ligand_color='#7E2553'):
    """Plots the RMSD data for protein and ligand with specified colors."""
    fig, ax1 = plt.subplots(figsize=(14, 9))

    # RNA (or Protein) RMSD
    line1, = ax1.plot(data['Frame'], data['Protein_RMSD'], label='Protein RMSD', color=protein_color, linewidth=2.5)
    ax1.set_xlabel('Time (nsec)', fontsize=16)
    ax1.set_ylabel('Protein RMSD (Å)', color=protein_color, fontsize=16)
    ax1.tick_params(axis='y', labelcolor=protein_color, labelsize=14, width=2.5)

    # Ligand RMSD
    ax2 = ax1.twinx()
    line2, = ax2.plot(data['Frame'], data['Ligand_RMSD'], label='Nucleic RMSD', color=ligand_color, linewidth=2.5)
    ax2.set_ylabel('Nucleic RMSD (Å)', color=ligand_color, fontsize=16)
    ax2.tick_params(axis='y', labelcolor=ligand_color, labelsize=14, width=2.5)

    # Adjustments for Time (nsec)
    nsec_ticks = range(0, 1001, 100)
    ax1.set_xticks(nsec_ticks)
    ax1.set_xticklabels([f"{x * 0.1:.1f}" for x in nsec_ticks], fontsize=14)

    # Combined Legend
    plt.legend([line1, line2], ['Protein RMSD', 'Nucleic RMSD'], loc='upper left', fontsize=14)

    # Title
    ax1.set_title(title, fontsize=18)

    # Removing grid lines
    ax1.grid(False)
    ax2.grid(False)

    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Plot Nucleic-Ligand RMSD data.')
    parser.add_argument('-P', '--protein', required=True, help='Path to the RNA or protein data file.')
    parser.add_argument('-L', '--ligand', required=True, help='Path to the ligand data file.')

    args = parser.parse_args()

    # Load and merge the data
    merged_data = merge_data(args.protein, args.ligand)

    # Plot the merged data
    plot_rmsd(merged_data)

if __name__ == '__main__':
    main()
    