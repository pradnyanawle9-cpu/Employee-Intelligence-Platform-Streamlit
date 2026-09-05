import streamlit as st
import matplotlib.pyplot as plt


def employee_status_chart(df):

    # ============================================================
    # EMPLOYEE STATUS DISTRIBUTION
    # ============================================================

    if df.empty:
        st.info("No employee status data available.")
        return

    # ------------------------------------------------------------
    # Clean status column
    # ------------------------------------------------------------

    status_series = (
        df["employee_status"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    # Remove empty status values
    status_series = status_series[
        status_series != ""
    ]

    if status_series.empty:
        st.info("No employee status data available.")
        return

    # ------------------------------------------------------------
    # Count ACTUAL statuses in filtered data
    # ------------------------------------------------------------

    status_df = (
        status_series
        .value_counts()
        .rename_axis("employee_status")
        .reset_index(name="Employees")
    )

    # ============================================================
    # STATUS COLORS
    # ============================================================

    status_colors = {

        "Active": "#4EB8E1",

        "On Leave": "#77C0A9",

        "Inactive": "#F773B5",

    }

    # ------------------------------------------------------------
    # Use only colors for statuses that actually exist
    # ------------------------------------------------------------

    colors = [
        status_colors.get(
            status,
            "#94A3B8"
        )
        for status in status_df["employee_status"]
    ]

    # ============================================================
    # FIGURE
    # ============================================================

    fig, ax = plt.subplots(
        figsize=(6.2, 4.0)
    )

    fig.patch.set_alpha(0)

    ax.set_facecolor("none")

    # ============================================================
    # DONUT
    # ============================================================

    wedges, _ = ax.pie(

        status_df["Employees"],

        colors=colors,

        startangle=90,

        counterclock=False,

        radius=1.0,

        wedgeprops={
            "width": 0.34,
            "edgecolor": "#071426",
            "linewidth": 2
        }

    )

    # ============================================================
    # TOTAL EMPLOYEES
    # ============================================================

    total_employees = status_df["Employees"].sum()

    ax.text(
        0,
        0.08,

        f"{total_employees:,}",

        ha="center",
        va="center",

        fontsize=22,

        fontweight="bold",

        color="white"
    )

    ax.text(
        0,
        -0.15,

        "Current Employees",

        ha="center",
        va="center",

        fontsize=9,

        color="#94A3B8"
    )

    # ============================================================
    # LEGEND
    # ============================================================

    legend_labels = []

    for status, value in zip(
        status_df["employee_status"],
        status_df["Employees"]
    ):

        percentage = (
            value / total_employees
        ) * 100

        legend_labels.append(
            f"{status}  ({value:,} • {percentage:.1f}%)"
        )

    legend = ax.legend(

        wedges,

        legend_labels,

        title="Status Breakdown",

        loc="center left",

        bbox_to_anchor=(
            1.03,
            0.5
        ),

        frameon=False,

        fontsize=9,

        title_fontsize=10,

        labelcolor="#E2E8F0",

        handlelength=1.0,

        handletextpad=0.7
    )

    # Legend title
    plt.setp(
        legend.get_title(),

        color="white",

        weight="bold"
    )

    # ============================================================
    # TITLE
    # ============================================================

    ax.set_title(

        "Employee Status Distribution",

        fontsize=13,

        fontweight="bold",

        color="white",

        loc="left",

        pad=10
    )

    # ============================================================
    # CLEAN AXIS
    # ============================================================

    ax.set_axis_off()

    # ============================================================
    # LAYOUT
    # ============================================================

    plt.subplots_adjust(

        left=0.0,

        right=0.63,

        top=0.88,

        bottom=0.05
    )

    # ============================================================
    # DISPLAY
    # ============================================================

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)