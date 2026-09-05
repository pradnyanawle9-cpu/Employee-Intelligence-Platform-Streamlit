import streamlit as st
import matplotlib.pyplot as plt


def location_chart(df, selected_location):

    # ==========================================
    # LOCATION-WISE EMPLOYEE COUNT
    # ==========================================

    location_df = (
        df.groupby("location_name")
        .size()
        .reset_index(name="Employees")
        .sort_values(
            "Employees",
            ascending=False
        )
        .reset_index(drop=True)
    )

    # ==========================================
    # EMPTY DATA
    # ==========================================

    if location_df.empty:
        st.info("No location data available.")
        return

    # ==========================================
    # FIGURE
    # ==========================================

    fig, ax = plt.subplots(
        figsize=(8.5, 4.8)
    )

    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    # ==========================================
    # PREMIUM BLUE COLOR SYSTEM
    # ==========================================

    selected_color = "#38BDF8"      # Premium Cyan Blue
    faded_color = "#1E3A5F"         # Dark Blue

    # ==========================================
    # DYNAMIC BAR COLORS
    # ==========================================

    if selected_location == "All":

        bar_colors = [
            selected_color
            for _ in location_df["location_name"]
        ]

    else:

        bar_colors = [
            selected_color
            if location == selected_location
            else faded_color
            for location in location_df["location_name"]
        ]

    # ==========================================
    # HORIZONTAL BAR CHART
    # ==========================================

    bars = ax.barh(
        location_df["location_name"],
        location_df["Employees"],
        height=0.58,
        color=bar_colors,
        edgecolor="none"
    )

    # Highest value on top
    ax.invert_yaxis()

    # ==========================================
    # VALUE LABELS
    # ==========================================

    max_value = location_df["Employees"].max()

    for bar, value, location in zip(
        bars,
        location_df["Employees"],
        location_df["location_name"]
    ):

        if (
            selected_location != "All"
            and location == selected_location
        ):

            label_color = "#FFFFFF"

        else:

            label_color = "#8EA9C1"

        ax.text(
            bar.get_width()
            + max_value * 0.015,

            bar.get_y()
            + bar.get_height() / 2,

            f"{value:,}",

            va="center",

            ha="left",

            color=label_color,

            fontsize=10,

            fontweight="bold"
        )

    # ==========================================
    # TITLE
    # ==========================================

    ax.set_title(
        "Employees By Location",
        fontsize=16,
        fontweight="bold",
        color="white",
        loc="left",
        pad=15
    )

    # ==========================================
    # AXIS
    # ==========================================

    ax.set_xlabel("")
    ax.set_ylabel("")

    ax.tick_params(
        axis="x",
        colors="#A9B8C8",
        labelsize=9,
        length=0
    )

    ax.tick_params(
        axis="y",
        colors="#CBD5E1",
        labelsize=9,
        length=0
    )

    # ==========================================
    # GRID
    # ==========================================

    ax.grid(
        axis="x",
        linestyle="-",
        linewidth=0.6,
        alpha=0.15,
        color="#9FB3C8"
    )

    ax.set_axisbelow(True)

    # ==========================================
    # REMOVE BORDER
    # ==========================================

    for spine in ax.spines.values():
        spine.set_visible(False)

    # ==========================================
    # X LIMIT
    # ==========================================

    ax.set_xlim(
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