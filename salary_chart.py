# ==========================================
# SALARY ANALYTICS CHART
# ==========================================

import streamlit as st
import matplotlib.pyplot as plt


# ==========================================
# SALARY CHART FUNCTION
# ==========================================

def salary_chart(df):


    # ==========================================
    # DEPARTMENT-WISE AVERAGE SALARY
    # ==========================================

    salary_df = (

        df.groupby(
            "department_name"
        )[

            "basic_salary"

        ]

        .mean()

        .sort_values(
            ascending=False
        )

        .reset_index()

    )


    # ==========================================
    # RENAME COLUMNS
    # ==========================================

    salary_df.columns = [

        "department_name",

        "Average Salary"

    ]


    # ==========================================
    # EMPTY DATA HANDLING
    # ==========================================

    if salary_df.empty:

        st.info(

            "No salary data available"

        )

        return


    # ==========================================
    # CREATE FIGURE
    # ==========================================

    fig, ax = plt.subplots(

        figsize=(8.5, 5.5)

    )


    # ==========================================
    # TRANSPARENT BACKGROUND
    # ==========================================

    fig.patch.set_alpha(0)

    ax.set_facecolor(

        "none"

    )


    # ==========================================
    # HORIZONTAL BAR CHART
    # ==========================================

    bars = ax.barh(

        salary_df[
            "department_name"
        ],

        salary_df[
            "Average Salary"
        ],

        height=0.55,

        color="#38BDF8",

        edgecolor="none"

    )


    # ==========================================
    # HIGHEST SALARY ON TOP
    # ==========================================

    ax.invert_yaxis()


    # ==========================================
    # SALARY VALUE LABELS
    # ==========================================

    for bar in bars:

        salary_value = bar.get_width()

    ax.annotate(

    f"₹{salary_value:,.0f}",

    xy=(salary_value, bar.get_y() + bar.get_height() / 2),

    xytext=(8, 0),

    textcoords="offset points",

    va="center",

    ha="left",

    fontsize=9,

    color="white",

    fontweight="bold"

)
        


    # ==========================================
    # TITLE
    # ==========================================

    ax.set_title(

        "Average Salary By Department",

        fontsize=16,

        fontweight="bold",

        color="white",

        loc="left",

        pad=15

    )


    # ==========================================
    # REMOVE UNNECESSARY ELEMENTS
    # ==========================================

    ax.spines[

        "top"

    ].set_visible(False)


    ax.spines[

        "right"

    ].set_visible(False)


    ax.spines[

        "left"

    ].set_visible(False)


    ax.spines[

        "bottom"

    ].set_visible(False)


    # ==========================================
    # AXIS STYLING
    # ==========================================

    ax.tick_params(

        axis="y",

        colors="white",

        labelsize=9,

        length=0

    )


    ax.tick_params(

        axis="x",

        colors="#8FA3B8",

        labelsize=8,

        length=0

    )


    # ==========================================
    # X-AXIS FORMAT
    # ==========================================

    ax.xaxis.set_major_formatter(

        plt.FuncFormatter(

            lambda x, pos:

            f"₹{x / 1000:.0f}K"

        )

    )


    # ==========================================
    # GRID
    # ==========================================

    ax.grid(

        axis="x",

        linestyle="--",

        alpha=0.15

    )


    # ==========================================
    # LAYOUT
    # ==========================================

    plt.tight_layout()


    # ==========================================
    # DISPLAY
    # ==========================================

    st.pyplot(

        fig,

        use_container_width=True

    )


    # ==========================================
    # CLOSE FIGURE
    # ==========================================

    plt.close(

        fig

    )