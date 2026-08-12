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

# Outlet Name Input Section
outlet_name = st.text_input("Outlet Name", value="", placeholder="Enter Outlet Name here...")

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

# Display Summary Report
st.markdown("---")
st.subheader("Summary Report")

outlet_display_str = outlet_name.strip() if outlet_name.strip() else "N/A"

# Build HTML Table Rows
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
            <td class="cell-val">{sec_disp}</td>
            <td class="cell-val">{tert_disp}</td>
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
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
    * {{
        box-sizing: border-box;
    }}
    body {{
        margin: 0;
        padding: 0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: transparent;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    #reportCaptureArea {{
        padding: 10px;
        background-color: white;
        width: 100%;
        max-width: 400px;
        border-radius: 6px;
    }}
    .fts-table {{
        width: 100%;
        margin: 0 auto;
        border-collapse: collapse;
        font-weight: bold;
        font-size: clamp(11px, 3.2vw, 14px);
        text-align: center;
        border: 2px solid #000;
        cursor: pointer;
        user-select: none;
    }}
    .fts-table th, .fts-table td {{
        border: 1px solid #000;
        padding: 5px 4px;
        word-break: break-word;
        vertical-align: middle;
    }}
    .hdr-outlet {{ background-color: #FFC000; color: black; text-align: center; font-size: clamp(12px, 3.5vw, 15px); }}
    .hdr-main {{ background-color: #002060; color: white; text-align: center; }}
    .hdr-month {{ background-color: #C6EFCE; color: #006100; text-align: center; }}
    .lbl-brand {{ background-color: #7030A0; color: white; text-align: left; padding-left: 8px; width: 40%; }}
    .cell-val {{ background-color: white; width: 30%; text-align: center; }}
    .row-total {{ background-color: #00B0F0; color: black; text-align: center; }}
    .row-grand {{ background-color: #FCE4D6; color: black; text-align: center; }}
    .row-points {{ background-color: #E2EFDA; color: black; text-align: center; }}
    .row-tour {{ background-color: #003300; color: white; text-align: center; }}
    
    .hint-text {{
        font-size: 11px;
        color: #555;
        margin-top: 6px;
        margin-bottom: 12px;
        text-align: center;
    }}
    
    .btn-share {{
        background-color: #25D366;
        color: white;
        border: none;
        padding: 12px 20px;
        font-size: 14px;
        font-weight: bold;
        border-radius: 6px;
        cursor: pointer;
        width: 100%;
        max-width: 320px;
        margin-top: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }}
    .btn-share:active {{
        background-color: #1EBE5D;
    }}
</style>
</head>
<body>

<div id="reportCaptureArea">
    <table class="fts-table" id="summaryTable">
        <thead>
            <tr class="hdr-outlet">
                <td colspan="3">Outlet Name: {outlet_display_str}</td>
            </tr>
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
</div>

<div class="hint-text">💡 <i>Tip: Triple-click anywhere on the table to download photo snap directly</i></div>

<button class="btn-share" onclick="shareReportImage()">
    📲 Share Report Image
</button>

<script>
// Triple-click handler for download
let clickCount = 0;
let clickTimer = null;

document.getElementById('summaryTable').addEventListener('click', function() {{
    clickCount++;
    if (clickTimer) clearTimeout(clickTimer);
    
    if (clickCount === 3) {{
        clickCount = 0;
        // Trigger download button in parent window
        window.parent.document.querySelector("button[kind='primary'], button[data-testid='stBaseButton-secondary']").click();
    }} else {{
        clickTimer = setTimeout(function() {{
            clickCount = 0;
        }}, 400);
    }}
}});

// Native Share API for capturing entire table as PNG
async function shareReportImage() {{
    const area = document.getElementById('reportCaptureArea');
    
    try {{
        const canvas = await html2canvas(area, {{ scale: 2, useCORS: true }});
        canvas.toBlob(async function(blob) {{
            const fileName = 'FTS_Report_{outlet_display_str.replace(" ", "_")}.png';
            const file = new File([blob], fileName, {{ type: 'image/png' }});
            
            if (navigator.canShare && navigator.canShare({{ files: [file] }})) {{
                await navigator.share({{
                    files: [file],
                    title: 'FTS Summary Report — {outlet_display_str}',
                    text: 'FTS Summary Report image for {outlet_display_str}'
                }});
            }} else {{
                // Fallback direct image download
                const link = document.createElement('a');
                link.download = fileName;
                link.href = canvas.toDataURL('image/png');
                link.click();
            }}
        }}, 'image/png');
    }} catch (err) {{
        console.error("Error generating image report:", err);
    }}
}}
</script>

</body>
</html>
"""

# Render via HTML iframe component
components.html(full_html, height=1300, scrolling=False)


# Function to render image snapshot via Matplotlib for direct download
def generate_snapshot_image():
    fig, ax = plt.subplots(figsize=(4, 11.5), dpi=200)
    ax.axis("off")

    table_data = [
        [f"Outlet Name: {outlet_display_str}", "", ""],
        ["Brand", "Secondary", "Tertiary"],
    ]
    cell_colors = [
        ["#FFC000", "#FFC000", "#FFC000"],
        ["#002060", "#002060", "#002060"],
    ]

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
        if r == 0:
            cell.get_text().set_color("black")
            cell.get_text().set_weight("bold")
        elif r == 1:
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
    file_name=f"FTS_Calculator_{outlet_display_str.replace(' ', '_')}.png",
    mime="image/png",
)
