# ==========================================
# EXPERIENCE ANALYTICS CHART
# ==========================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def experience_chart(df):

    # ==========================================
    # EXPERIENCE GROUPING
    # ==========================================

    experience_df = pd.DataFrame({

        "Experience Group": [

            "0–2 Years",
            "3–5 Years",
            "6–10 Years",
            "10+ Years"

        ],

        "Employees": [

            len(
                df[
                    (df["experience_years"] >= 0) &
                    (df["experience_years"] <= 2)
                ]
            ),

            len(
                df[
                    (df["experience_years"] >= 3) &
                    (df["experience_years"] <= 5)
                ]
            ),

            len(
                df[
                    (df["experience_years"] >= 6) &
                    (df["experience_years"] <= 10)
                ]
            ),

            len(
                df[
                    df["experience_years"] > 10
                ]
            )

        ]

    })


    # ==========================================
    # EMPTY DATA HANDLING
    # ==========================================

    if experience_df["Employees"].sum() == 0:

        st.info(
            "No experience data available."
        )

        return


    # ==========================================
    # FIGURE
    # ==========================================

    fig, ax = plt.subplots(

        figsize=(6,3.2),

        dpi=120

    )


    # ==========================================
    # BACKGROUND
    # ==========================================

    fig.patch.set_facecolor(
        "#071426"
    )

    ax.set_facecolor(
        "#071426"
    )


    # ==========================================
    # PREMIUM COLORS
    # ==========================================

    colors = [

        "#38BDF8",
        "#2DD4BF",
        "#818CF8",
        "#FBBF24"

    ]


    # ==========================================
    # BAR CHART
    # ==========================================

    bars = ax.bar(

        experience_df["Experience Group"],

        experience_df["Employees"],

        color=colors,

        width=0.52,

        edgecolor="none"

    )


    # ==========================================
    # VALUE LABELS
    # ==========================================

    max_value = (

        experience_df["Employees"].max()

    )


    for bar in bars:

        value = bar.get_height()


        ax.text(

            bar.get_x()
            + bar.get_width() / 2,

            value
            + max_value * 0.025,

            f"{int(value):,}",

            ha="center",

            va="bottom",

            color="white",

            fontsize=12,

            fontweight="bold"

        )


    # ==========================================
    # TITLE
    # ==========================================

    ax.set_title(

        "Employee Experience Distribution",

        fontsize=18,

        fontweight="bold",

        color="white",

        loc="left",

        pad=20

    )


    # ==========================================
    # AXIS
    # ==========================================

    ax.set_xlabel("")

    ax.set_ylabel(

        "Employees",

        color="#A9B8C8",

        fontsize=11

    )


    # ==========================================
    # X-AXIS
    # ==========================================

    ax.tick_params(

        axis="x",

        colors="#D6E4F0",

        labelsize=11,

        length=0

    )


    # ==========================================
    # Y-AXIS
    # ==========================================

    ax.tick_params(

        axis="y",

        colors="#A9B8C8",

        labelsize=10,

        length=0

    )


    # ==========================================
    # GRID
    # ==========================================

    ax.grid(

        axis="y",

        linestyle="--",

        linewidth=0.7,

        color="#64748B",

        alpha=0.28

    )


    ax.set_axisbelow(True)


    # ==========================================
    # REMOVE BORDERS
    # ==========================================

    for spine in ax.spines.values():

        spine.set_visible(False)


    # ==========================================
    # Y LIMIT
    # ==========================================

    ax.set_ylim(

        0,

        max_value * 1.18

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


    plt.close(fig)