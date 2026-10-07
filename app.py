import streamlit as st

from apputil import *

# load Titanic dataset
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

st.write(
'''
# Titanic Visualization 1

'''
)
st.write("Did women and children in higher passenger classes survive at higher rates "
         "than men and passengers in lower classes?")
# generate and display the figure
fig1 = visualize_demographic()
st.plotly_chart(fig1, use_container_width=True)

st.write(
'''
# Titanic Visualization 2
'''
)
# compare last name counts with the family size table
names = last_names()
st.write(
    f"There are {len(names)} unique last names, and {(names > 1).sum()} of them are shared "
    "by more than one passenger. This roughly agrees with the family size table, which shows "
    "many passengers traveling with family. It doesn't match exactly though, some unrelated "
    "passengers share a common last name, and some family members have different last names."
)

st.write("Do passengers in larger families pay higher average fares, and does that depend on class?")
# generate and display the figure
fig2 = visualize_families()
st.plotly_chart(fig2, use_container_width=True)