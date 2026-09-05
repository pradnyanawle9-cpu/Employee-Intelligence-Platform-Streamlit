import matplotlib.pyplot as plt
import streamlit as st


def department_chart(df, selected_department):
    # ==========================================
    # DEPARTMENT-WISE EMPLOYEE COUNT
    # ==========================================
    department_df = (
        df.groupby("department_name")
        .size()
        .reset_index(name="Employees")
        .sort_values("Employees", ascending=True)  # Ascending for Horizontal Chart
        .reset_index(drop=True)
    )

    if department_df.empty:
        st.info("No department data available.")
        return

    # ==========================================
    # FIGURE (Perfect Height Ratio)
    # ==========================================
    fig, ax = plt.subplots(figsize=(8, 4.6))

    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    # ==========================================
    # COLORS
    # ==========================================
    selected_color = "#A855F7"
    faded_color = "#33264D"

    if selected_department == "All":
        bar_colors = ["#A855F7" for _ in department_df["department_name"]]
    else:
        bar_colors = [
            selected_color
            if dept == selected_department
            else faded_color
            for dept in department_df["department_name"]
        ]

    # ==========================================
    # HORIZONTAL BARS
    # ==========================================
    y_position = range(len(department_df))
    bars = ax.barh(
        y_position,
        department_df["Employees"],
        height=0.6,
        color=bar_colors,
        edgecolor="none",
    )

    # ==========================================
    # Y-AXIS & X-AXIS LABELS
    # ==========================================
    ax.set_yticks(y_position)
    ax.set_yticklabels(
        department_df["department_name"],
        color="#A9B8C8",
        fontsize=9,
    )

    max_value = department_df["Employees"].max()

    # Value labels on right of bars
    for bar, value in zip(bars, department_df["Employees"]):
        ax.text(
            bar.get_width() + max_value * 0.02,
            bar.get_y() + bar.get_height() / 2,
            f"{value:,}",
            ha="left",
            va="center",
            color="#FFFFFF",
            fontsize=9,
            fontweight="bold",
        )

    # ==========================================
    # TITLE & STYLING
    # ==========================================
    ax.set_title(
        "Employees By Department",
        fontsize=14,
        fontweight="bold",
        color="white",
        loc="left",
        pad=15,
    )

    ax.tick_params(axis="x", colors="#66788A", labelsize=8, length=0)
    ax.tick_params(axis="y", length=0)

    ax.grid(
        axis="x",
        linestyle="-",
        linewidth=0.6,
        alpha=0.15,
        color="#9FB3C8",
    )
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_xlim(0, max_value * 1.15)

    # Margin Adjustment for Perfect Alignment
    plt.subplots_adjust(left=0.25, right=0.9, top=0.88, bottom=0.1)

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)