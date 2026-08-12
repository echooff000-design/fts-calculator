import io
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Configure page settings
st.set_page_config(page_title="FTS Calculator", layout="centered")

# Custom CSS for table styling matching your exact layout & colors
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .fts-table {
        width: 100%;
        max-width: 420px;
        margin: auto;
        border-collapse: collapse;
        font-family: Arial, sans-serif;
        font-weight: bold;
        font-size: 14px;
        text-align: center;
        border: 2px solid #000;
    }
    .fts-table th, .fts-table td {
        border: 1px solid #000;
        padding: 5px 8px;
    }
    .hdr-main { background-color: #002060; color: white; }
    .hdr-month { background-color: #C6EFCE; color: #006100; text-align: center; }
    .lbl-brand { background-color: #7030A0; color: white; text-align: left; padding-left: 10px; }
    .row-total { background-color: #00B0F0; color: black; }
    .row-grand { background-color: #FCE4D6; color: black; text-align: left; }
    .row-points { background-color: #E2EFDA; color: black; }
    .row-tour { background-color: #003300; color: white; text-align: left; }
    </style>
""",
    unsafe_allow_html=True,
)

# Month Configuration & Point Multipliers derived directly from Excel logic
MONTHS = ["Aug'26", "Sep'26", "Oct'26"]
BRANDS = [
    "IBDC",
    "MHW",
    "BLGLM",
    "BLGOR",
    "MHFB",
    "SMG",
    "SMGP",
    "SIW",
    "Monarch",
]

POINTS_CONFIG = {
    "Aug'26": {
        "IBDC": (25, 5),
        "MHW": (45, 10),
        "BLGLM": (10, 5),
        "BLGOR": (10, 5),
        "MHFB": (35, 10),
        "SMG": (150, 75),
        "SMGP": (150, 75),
        "SIW": (300, 150),
        "Monarch": (300, 150),
    },
    "Sep'26": {
        "IBDC": (20, 5),
        "MHW": (40, 10),
        "BLGLM": (10, 5),
        "BLGOR": (10, 5),
        "MHFB": (30, 10),
        "SMG": (150, 75),
        "SMGP": (150, 75),
        "SIW": (300, 150),
        "Monarch": (300, 150),
    },
    "Oct'26": {
        "IBDC": (20, 5),
        "MHW": (40, 10),
        "BLGLM": (10, 5),
        "BLGOR": (10, 5),
        "MHFB": (30, 10),
        "SMG": (150, 75),
        "SMGP": (150, 75),
        "SIW": (300, 150),
        "Monarch": (300, 150),
    },
}


def get_calculated_tour(total_points):
    if total_points >= 12000:
        return "4N/ 5D Mauritius"
    elif total_points >= 9000:
        return "6N/ 7D Ladakh"
    elif total_points >= 6000:
        return "4N/ 5D Manali"
    else:
        return "Not Eligible"


st.title("FTS Calculator")
st.write("Enter Secondary and Tertiary values below to compute target points:")

# Data Input Form
inputs = {}
total_calculated_points = 0
grand_sec = 0
grand_tert = 0

month_totals = {}

for m in MONTHS:
    st.subheader(f"Data Input — {m}")
    m_sec_sum = 0
    m_tert_sum = 0

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Secondary ({m})**")
    with col2:
        st.markdown(f"**Tertiary ({m})**")

    for b in BRANDS:
        c1, c2 = st.columns(2)
        sec_val = c1.number_input(
            f"{b} (Sec)", min_value=0, value=0, step=1, key=f"{m}_{b}_sec"
        )
        tert_val = c2.number_input(
            f"{b} (Tert)", min_value=0, value=0, step=1, key=f"{m}_{b}_tert"
        )

        inputs[(m, b)] = (sec_val, tert_val)
        m_sec_sum += sec_val
        m_tert_sum += tert_val

        # Point calculation
        pts_sec, pts_tert = POINTS_CONFIG[m][b]
        total_calculated_points += (sec_val * pts_sec) + (
            tert_val * pts_tert
        )

    month_totals[m] = (m_sec_sum, m_tert_sum)
    grand_sec += m_sec_sum
    grand_tert += m_tert_sum

calculated_tour = get_calculated_tour(total_calculated_points)

# Display Summary Table in HTML/CSS
st.markdown("---")
st.subheader("Summary Report")

table_html = f"""
<table class="fts-table">
    <tr class="hdr-main">
        <th>Brand</th>
        <th>Secondary</th>
        <th>Tertiary</th>
    </tr>
"""

for m in MONTHS:
    table_html += f"""
    <tr class="hdr-month">
        <td colspan="3">{m}</td>
    </tr>
    """
    for b in BRANDS:
        sec, tert = inputs[(m, b)]
        table_html += f"""
        <tr>
            <td class="lbl-brand">{b}</td>
            <td style="background-color: white;">{sec if sec > 0 else ''}</td>
            <td style="background-color: white;">{tert if tert > 0 else ''}</td>
        </tr>
        """
    m_sec, m_tert = month_totals[m]
    table_html += f"""
    <tr class="row-total">
        <td>Total</td>
        <td>{m_sec}</td>
        <td>{m_tert}</td>
    </tr>
    """

table_html += f"""
    <tr class="row-grand">
        <td>Grand Total</td>
        <td>{grand_sec}</td>
        <td>{grand_tert}</td>
    </tr>
    <tr class="row-points">
        <td>Total Point</td>
        <td colspan="2">{total_calculated_points}</td>
    </tr>
    <tr class="row-tour">
        <td>Calculated Tour</td>
        <td colspan="2">{calculated_tour}</td>
    </tr>
</table>
"""

st.markdown(table_html, unsafe_allow_html=True)


# Function to render image snapshot via Matplotlib for direct download
def generate_snapshot_image():
    fig, ax = plt.subplots(figsize=(4, 11), dpi=200)
    ax.axis("off")

    table_data = [["Brand", "Secondary", "Tertiary"]]
    cell_colors = [["#002060", "#002060", "#002060"]]

    for m in MONTHS:
        table_data.append([m, "", ""])
        cell_colors.append(["#C6EFCE", "#C6EFCE", "#C6EFCE"])
        for b in BRANDS:
            sec, tert = inputs[(m, b)]
            table_data.append(
                [b, str(sec) if sec > 0 else "", str(tert) if tert > 0 else ""]
            )
            cell_colors.append(["#7030A0", "#FFFFFF", "#FFFFFF"])
        m_sec, m_tert = month_totals[m]
        table_data.append(["Total", str(m_sec), str(m_tert)])
        cell_colors.append(["#00B0F0", "#00B0F0", "#00B0F0"])

    table_data.append(["Grand Total", str(grand_sec), str(grand_tert)])
    cell_colors.append(["#FCE4D6", "#FCE4D6", "#FCE4D6"])

    table_data.append(["Total Point", str(total_calculated_points), ""])
    cell_colors.append(["#E2EFDA", "#E2EFDA", "#E2EFDA"])

    table_data.append(["Calculated Tour", str(calculated_tour), ""])
    cell_colors.append(["#003300", "#003300", "#003300"])

    tab = ax.table(
        cellText=table_data,
        cellColours=cell_colors,
        loc="center",
        cellLoc="center",
    )
    tab.scale(1, 1.3)

    # Styling cells
    for (r, c), cell in tab.get_celld().items():
        cell.set_edgecolor("black")
        cell.set_linewidth(1)
        # Font color adjustments
        if r == 0:
            cell.get_text().set_color("white")
            cell.get_text().set_weight("bold")
        elif table_data[r][0] in BRANDS and c == 0:
            cell.get_text().set_color("white")
            cell.get_text().set_weight("bold")
        elif table_data[r][0] == "Calculated Tour":
            cell.get_text().set_color("white")
            cell.get_text().set_weight("bold")
        else:
            cell.get_text().set_weight("bold")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.1)
    buf.seek(0)
    plt.close(fig)
    return buf


st.markdown("---")
img_buf = generate_snapshot_image()
st.download_button(
    label="📷 Download Table Snap (PNG)",
    data=img_buf,
    file_name="FTS_Calculator_Snapshot.png",
    mime="image/png",
)
