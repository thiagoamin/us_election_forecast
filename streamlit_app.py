import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

unemployment = pd.read_csv('datasets/unemployment.csv')
incumbent_party = pd.read_csv('datasets/incumbent_party.csv')
election_result = pd.read_csv('datasets/election_results.csv')

unemployment['state'] = unemployment['state'].str.upper()
election_result['state'] = election_result['state'].str.upper()

unemployment['election_year'] = unemployment['election_year'].astype(int)
election_result['election_year'] = election_result['election_year'].astype(int)
incumbent_party['election_year'] = incumbent_party['election_year'].astype(int)

merged_data = (
    unemployment
    .merge(incumbent_party, on='election_year', how='inner')
    .merge(election_result, on=['election_year', 'state'], how='inner')
)

print("Number of rows in merged_data:", merged_data.shape[0])
print("Number of columns in merged_data:", merged_data.shape[1])

min_year = unemployment['election_year'].min()
max_year = unemployment['election_year'].max()

st.title("Election and Unemployment Analysis")

state = st.selectbox("Select a State", merged_data['state'].unique())
year_range = st.slider("Select Year Range", int(min_year), int(max_year), (int(min_year), int(max_year)))

filtered_data = merged_data[
    (merged_data['state'] == state) & 
    (merged_data['election_year'] >= year_range[0]) & 
    (merged_data['election_year'] <= year_range[1])
]

fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.plot(
    filtered_data['election_year'],
    filtered_data['adjusted_percentage_votes_republican'],
    color='blue',
    marker='o',
    label='% Republican Votes (Adjusted)'
)
ax1.set_ylabel('% Republican Votes', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

for _, row in filtered_data.iterrows():
    if row['is_gop_incumbent'] == 1:
        ax1.annotate('GOP Incumbent', (row['election_year'], row['adjusted_percentage_votes_republican']),
                     textcoords="offset points", xytext=(0, 10), ha='center', color='red')

ax2 = ax1.twinx()
ax2.plot(
    filtered_data['election_year'],
    filtered_data['unemployement_1year_change'],
    color='purple',
    linestyle='--',
    label='Unemployement (1 year change)'
)
ax2.plot(
    filtered_data['election_year'],
    filtered_data['unemployement_4year_change'],
    color='orange',
    linestyle='--',
    label='Unemployement (4 year change)'
)
ax2.plot(
    filtered_data['election_year'],
    filtered_data['unemployement_1_year_average'],
    color='gray',
    linestyle='--',
    label='Unemployement (1 year average)'
)
ax2.plot(
    filtered_data['election_year'],
    filtered_data['uneployement_4_year_average'],
    color='green',
    linestyle='--',
    label='Unemployement (4 year average)'
)
ax2.set_ylabel('Unemployment Metrics', color='green')
ax2.tick_params(axis='y', labelcolor='green')

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

plt.title(f"Election and Unemployment Trends in {state} ({year_range[0]}-{year_range[1]})")
plt.tight_layout()

st.pyplot(fig)