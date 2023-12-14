from translator import Translator
import matplotlib.pyplot as plt
import numpy as np

translator = Translator(language='english')

num_segments = 9
metrics = []

audio_path = 'split/segment_'
different_path = 'split/speaker_'

# Calculate metrics for comparisons within the same set (audio segments)
for i in range(num_segments):
    for j in range(i + 1, num_segments):
        print(f"Calculating metrics between {i+1} and {j+1}")
        cosine = translator.calculate_metrics(speaker_1=f'{audio_path}{i+1}.wav', speaker_2=f'{audio_path}{j+1}.wav')
        metrics.append({'cosine': cosine, 'type': 'same_set'})

# Calculate metrics for comparisons within a different set (different audio segments)
for i in range(num_segments):
    for j in range(i + 1, num_segments):
        print(f"Calculating metrics between {i+1} and {j+1}")
        cosine = translator.calculate_metrics(speaker_1=f'{different_path}{i+1}.wav', speaker_2=f'{different_path}{j+1}.wav')
        metrics.append({'cosine': cosine, 'type': 'different_set'})

# Calculate metrics for comparisons between the output and each audio segment
for i in range(num_segments):
    cosine = translator.calculate_metrics(speaker_1='results/output.wav', speaker_2=f'{audio_path}{i+1}.wav')
    metrics.append({'cosine': cosine, 'type': 'output_comparison'})

# Extract data and colors for plotting
data = [entry['cosine'] for entry in metrics]
colors = np.where(np.array([entry['type'] for entry in metrics]) == 'same_set', 'blue',
                  np.where(np.array([entry['type'] for entry in metrics]) == 'different_set', 'green', 'red'))

# Plotting
plt.hist(data, bins=100, edgecolor='black', color=colors)
plt.title('Distribution of Cosine Similarity Metrics')
plt.xlabel('Cosine Similarity')
plt.ylabel('Frequency')
plt.savefig('output_plot.png')