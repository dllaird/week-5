import plotly.express as px
import pandas as pd


# location of the Titanic dataset"
TITANIC_URL = 'https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv'


def load_titanic():
    """Load the dataset and rename columns to lowercase underscore format."""
    df = pd.read_csv(TITANIC_URL)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df


def survival_demographics():
    """Summarize survival by passenger class, sex, and age group."""
    df = load_titanic()

    # classify passengers into age categories
    df['age_group'] = pd.cut(
        df['age'],
        bins=[0, 12, 19, 59, float('inf')],
        labels=['Child', 'Teen', 'Adult', 'Senior'],
        include_lowest=True,
    )

    # group by demographic and compute survival rate
    summary = (
        df.groupby(['pclass', 'sex', 'age_group'], observed=False)
        .agg(n_passengers=('survived', 'size'),
             n_survivors=('survived', 'sum'))
    )

    # make sure every combination of appears
    all_combos = pd.MultiIndex.from_product(
        [sorted(df['pclass'].unique()),
         sorted(df['sex'].unique()),
         df['age_group'].cat.categories],
        names=['pclass', 'sex', 'age_group'],
    )
    # fill in 0 for groups with no passengers
    summary = summary.reindex(all_combos, fill_value=0).reset_index()

    # survival rate = survivors / passengers
    summary['survival_rate'] = summary['n_survivors'] / summary['n_passengers']

    # keep age_group as an ordered category
    summary['age_group'] = pd.Categorical(
        summary['age_group'],
        categories=['Child', 'Teen', 'Adult', 'Senior'],
        ordered=True,
    )

    summary = summary.sort_values(['pclass', 'sex', 'age_group']).reset_index(drop=True)
    return summary


def visualize_demographic():
    """Did women and children in higher classes have a higher survival rate?"""
    summary = survival_demographics()

    # one bar per age group, colored by sex, with a panel for each class
    fig = px.bar(
        summary,
        x='age_group',
        y='survival_rate',
        color='sex',
        barmode='group',
        facet_col='pclass',
        hover_data=['n_passengers', 'n_survivors'],
        category_orders={'age_group': ['Child', 'Teen', 'Adult', 'Senior'],
                         'pclass': [1, 2, 3]},
        labels={'age_group': 'Age Group',
                'survival_rate': 'Survival Rate',
                'sex': 'Sex',
                'pclass': 'Class'},
        title='Titanic Survival Rate by Class, Sex, and Age Group',
    )
    # show the y-axis as percentages
    fig.update_yaxes(tickformat='.0%')
    return fig


def family_groups():
    """Summarize ticket fares by family size and passenger class."""
    df = load_titanic()

    # family size = siblings/spouses + parents/children + the passenger
    df['family_size'] = df['sibsp'] + df['parch'] + 1

    # group by family size and class and compute fare stats
    summary = (
        df.groupby(['pclass', 'family_size'])
        .agg(n_passengers=('fare', 'size'),
             avg_fare=('fare', 'mean'),
             min_fare=('fare', 'min'),
             max_fare=('fare', 'max'))
        .reset_index()
    )

    # sort by class, then family size
    summary = summary.sort_values(['pclass', 'family_size']).reset_index(drop=True)
    return summary


def last_names():
    """Count how many passengers share each last name."""
    df = load_titanic()

    # last names come before the comma
    last = df['name'].str.split(',').str[0].str.strip()
    return last.value_counts()


def visualize_families():
    """Do larger families pay more for their tickets, and does it depend on class?"""
    summary = family_groups()
    # treat class as a label so each class gets its own color
    summary['pclass'] = summary['pclass'].astype(str)

    # one line per class showing average fare as family size grows
    fig = px.line(
        summary,
        x='family_size',
        y='avg_fare',
        color='pclass',
        markers=True,
        hover_data=['n_passengers', 'min_fare', 'max_fare'],
        category_orders={'pclass': ['1', '2', '3']},
        labels={'family_size': 'Family Size',
                'avg_fare': 'Average Fare',
                'pclass': 'Class'},
        title='Average Titanic Ticket Fare by Family Size and Class',
    )
    # show the y-axis in dollars
    fig.update_yaxes(tickprefix='$')
    return fig
