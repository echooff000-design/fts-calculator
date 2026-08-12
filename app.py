import io
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Configure page settings
st.set_page_config(page_title="FTS Calculator", layout="centered")

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

    for b in BRANDS:
        c1, c2 = st.columns(2)
        sec_val = c1.number_input(
            f"{b} (Sec) [{m}]", min_value=0, value=0, step=1, key=f"{m}_{b}_sec"
        )
        tert_val = c2.number_input(
            f"{b} (Tert) [{m}]",
            min_value=0,
            value=0,
            step=1,
            key=f"{m}_{b}_tert",
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

# Display Summary Report using Native Components
st.markdown("---")
st.subheader("Summary Report")

# Generate HTML string
rows_html = ""
for m in MONTHS:
    rows_html += f"""
    <tr class="hdr-month">
        <td colspan="3">{m}</td>
    </tr>
    """
    for b in BRANDS:
        sec, tert = inputs[(m, b)]
        sec_disp = str(sec) if sec > 0 else ""
        tert_disp = str(tert) if tert > 0 else ""
        rows_html += f"""
        <tr>
            <td class="lbl-brand">{b}</td>
            <td style="background-color: white;">{sec_disp}</td>
            <td style="background-color: white;">{tert_disp}</td>
        </tr>
        """
    m_sec, m_tert = month_totals[m]
    rows_html += f"""
    <tr class="row-total">
        <td>Total</td>
        <td>{m_sec}</td>
        <td>{m_tert}</td>
    </tr>
    """

full_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{
        margin: 0;
        padding: 0;
        font-family: Arial, sans-serif;
        background-color: transparent;
    }}
    .fts-table {{
        width: 100%;
        max-width: 400px;
        margin: 0 auto;
        border-collapse: collapse;
        font-weight: bold;
        font-size: 14px;
        text-align: center;
        border: 2px solid #000;
    }}
    .fts-table th, .fts-table td {{
        border: 1px solid #000;
        padding: 6px 8px;
    }}
    .hdr-main {{ background-color: #002060; color: white; }}
    .hdr-month {{ background-color: #C6EFCE; color: #006100; text-align: center; }}
    .lbl-brand {{ background-color: #7030A0; color: white; text-align: left; padding-left: 10px; }}
    .row-total {{ background-color: #00B0F0; color: black; }}
    .row-grand {{ background-color: #FCE4D6; color: black; text-align: left; }}
    .row-points {{ background-color: #E2EFDA; color: black; }}
    .row-tour {{ background-color: #003300; color: white; text-align: left; }}
</style>
</head>
<body>
<table class="fts-table">
    <thead>
        <tr class="hdr-main">
            <th>Brand</th>
            <th>Secondary</th>
            <th>Tertiary</th>
        </tr>
    </thead>
    <tbody>
        {rows_html}
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
    </tbody>
</table>
</body>
</html>
"""

# Render via html component to avoid markdown raw text escaping issues
components.html(full_html, height=1150, scrolling=False)


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
