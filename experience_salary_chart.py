# ============================================================
# EXPERIENCE VS SALARY ANALYTICS
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def experience_salary_chart(df):

    # ========================================================
    # 1. DATA VALIDATION
    # ========================================================

    required_columns = [
        "experience_years",
        "basic_salary"
    ]

    for column in required_columns:

        if column not in df.columns:

            st.error(
                f"Required column '{column}' is missing from the dataset."
            )

            return


    # ========================================================
    # 2. COPY DATA
    # ========================================================

    salary_df = df.copy()


    # ========================================================
    # 3. CLEAN DATA
    # ========================================================

    salary_df["experience_years"] = pd.to_numeric(
        salary_df["experience_years"],
        errors="coerce"
    )

    salary_df["basic_salary"] = pd.to_numeric(
        salary_df["basic_salary"],
        errors="coerce"
    )


    # Remove invalid records

    salary_df = salary_df.dropna(
        subset=[
            "experience_years",
            "basic_salary"
        ]
    )


    # ========================================================
    # 4. CREATE EXPERIENCE GROUPS
    # ========================================================

    def create_experience_group(years):

        if years <= 2:

            return "0-2 Years"

        elif years <= 5:

            return "3-5 Years"

        elif years <= 10:

            return "6-10 Years"

        else:

            return "10+ Years"


    salary_df["experience_group"] = (

        salary_df["experience_years"]
        .apply(create_experience_group)

    )


    # ========================================================
    # 5. CALCULATE AVERAGE SALARY
    # ========================================================

    salary_summary = (

        salary_df
        .groupby("experience_group", sort=False)
        ["basic_salary"]
        .mean()
        .reset_index()
    )


    # ========================================================
    # 6. KEEP EXPERIENCE ORDER LOGICAL
    # ========================================================

    experience_order = [

        "0-2 Years",
        "3-5 Years",
        "6-10 Years",
        "10+ Years"

    ]


    salary_summary["experience_group"] = pd.Categorical(

        salary_summary["experience_group"],

        categories=experience_order,

        ordered=True

    )


    salary_summary = (

        salary_summary
        .sort_values("experience_group")
    )


    # ========================================================
    # 7. CREATE FIGURE
    # ========================================================

    fig, ax = plt.subplots(

        figsize=(7, 5),

        dpi=120

    )


    # Transparent background

    fig.patch.set_alpha(0)

    ax.set_facecolor("none")


    # ========================================================
    # 8. CREATE BAR CHART
    # ========================================================

    bars = ax.bar(

        salary_summary["experience_group"].astype(str),

        salary_summary["basic_salary"],

        width=0.55,

        color="#BF6DF9",

        edgecolor="none"

    )


    # ========================================================
    # 9. ADD SALARY VALUES ABOVE BARS
    # ========================================================

    for bar in bars:

        height = bar.get_height()


        ax.text(

            bar.get_x()
            + bar.get_width() / 2,

            height,

            f"₹{height:,.0f}",

            ha="center",

            va="bottom",

            fontsize=9,

            fontweight="bold",

            color="white"

        )


    # ========================================================
    # 10. TITLE
    # ========================================================

    ax.set_title(

        "Average Salary by Experience Level",

        fontsize=14,

        fontweight="bold",

        color="white",

        pad=15

    )


    # ========================================================
    # 11. AXIS LABELS
    # ========================================================

    ax.set_xlabel(

        "Experience Level",

        fontsize=10,

        color="white",

        labelpad=8

    )


    ax.set_ylabel(

        "Average Salary",

        fontsize=10,

        color="white",

        labelpad=8

    )


    # ========================================================
    # 12. TICK LABEL COLORS
    # ========================================================

    ax.tick_params(

        axis="x",

        colors="white",

        labelsize=9

    )


    ax.tick_params(

        axis="y",

        colors="white",

        labelsize=9

    )


    # ========================================================
    # 13. FORMAT Y-AXIS
    # ========================================================

    ax.yaxis.set_major_formatter(

        plt.FuncFormatter(

            lambda value, position:

            f"₹{value / 1000:.0f}K"

        )

    )


    # ========================================================
    # 14. GRID
    # ========================================================

    ax.grid(

        axis="y",

        linestyle="--",

        alpha=0.25,

        color="#94A3B8"

    )


    ax.set_axisbelow(True)


    # ========================================================
    # 15. REMOVE UNNECESSARY BORDERS
    # ========================================================

    ax.spines["top"].set_visible(False)

    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_visible(False)


    ax.spines["bottom"].set_color(

        "#64748B"

    )


    # ========================================================
    # 16. LAYOUT
    # ========================================================

    plt.tight_layout()


    # ========================================================
    # 17. DISPLAY IN STREAMLIT
    # ========================================================

    st.pyplot(

        fig,

        width="stretch"

    )


    # ========================================================
    # 18. CLOSE FIGURE
    # ========================================================

    plt.close(fig)