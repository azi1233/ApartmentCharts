#!/usr/bin/env python3
from flask import Flask, render_template
import plotly.graph_objs as go
import plotly.offline as pyo
from pathlib import Path
from datetime import datetime
import json, os
import threading,schedule, time

app = Flask(__name__)
DIVAR_RESULTS = Path("./divar_results")

def load_all_summaries():
    summaries = []
    for folder in sorted(DIVAR_RESULTS.iterdir()):
        if not folder.is_dir():
            continue
        for file in folder.glob("summary_*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    ts = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
                    summaries.append((ts, data))
            except Exception:
                pass
    summaries.sort(key=lambda x: x[0])
    return summaries

def make_chart(summaries):
    import plotly.subplots as sp

    timestamps = [s[0] for s in summaries]

    # Price-related data
    overall = [s[1]["overall_avg_price_per_sqm"] for s in summaries]
    overall_count = [s[1]["valid_for_averages"] for s in summaries]

    def get_age_data(interval):
        return [s[1]["age_intervals"][interval]["avg"] for s in summaries], [
            s[1]["age_intervals"][interval]["count"] for s in summaries
        ]

    def get_size_data(interval):
        return [s[1]["size_intervals"][interval]["avg"] for s in summaries], [
            s[1]["size_intervals"][interval]["count"] for s in summaries
        ]

    age0_4, cnt0_4 = get_age_data("0-4")
    age5_9, cnt5_9 = get_age_data("5-9")
    age10_14, cnt10_14 = get_age_data("10-14")
    age15_20, cnt15_20 = get_age_data("15-20")

    size_small, cnt_small = get_size_data("<80")
    size_mid, cnt_mid = get_size_data("80-120")
    size_large, cnt_large = get_size_data(">120")

    # Create a subplot layout: 2 rows, 1 column
    fig = sp.make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        row_heights=[0.7, 0.3],
        subplot_titles=("Average Price per m² Over Time", "Number of Listings Over Time"),
    )

    # --- Chart 1: Price per sqm lines ---
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=overall,
            mode="lines+markers",
            name=f"Overall Avg ({overall_count[-1]})",
            line=dict(width=3, color="#ff9800"),
            legendgroup="price",
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=age0_4,
            mode="lines+markers",
            name=f"Age 0–4 ({cnt0_4[-1]})",
            line=dict(color="#4caf50"),
            legendgroup="price",
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=age5_9,
            mode="lines+markers",
            name=f"Age 5–9 ({cnt5_9[-1]})",
            line=dict(color="#2196f3"),
            legendgroup="price",
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=age10_14,
            mode="lines+markers",
            name=f"Age 10–14 ({cnt10_14[-1]})",
            line=dict(color="#9c27b0"),
            legendgroup="price",
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=age15_20,
            mode="lines+markers",
            name=f"Age 15–20 ({cnt15_20[-1]})",
            line=dict(color="#f44336"),
            legendgroup="price",
        ),
        row=1, col=1
    )

    # --- Add size-based lines ---
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=size_small,
            mode="lines+markers",
            name=f"Size <80m² ({cnt_small[-1]})",
            line=dict(color="#8bc34a", dash="dot"),
            legendgroup="size",
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=size_mid,
            mode="lines+markers",
            name=f"Size 80–120m² ({cnt_mid[-1]})",
            line=dict(color="#03a9f4", dash="dot"),
            legendgroup="size",
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=size_large,
            mode="lines+markers",
            name=f"Size >120m² ({cnt_large[-1]})",
            line=dict(color="#e91e63", dash="dot"),
            legendgroup="size",
        ),
        row=1, col=1
    )

    # --- Chart 2: Listing volume bars ---
    total_posts = [s[1]["total_posts"] for s in summaries]
    valid_posts = [s[1]["valid_for_averages"] for s in summaries]

    fig.add_trace(
        go.Bar(
            x=timestamps,
            y=total_posts,
            name="Total Listings",
            marker_color="rgba(100, 149, 237, 0.7)",
            legendgroup="volume",
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Bar(
            x=timestamps,
            y=valid_posts,
            name="Valid Listings (for averages)",
            marker_color="rgba(255, 152, 0, 0.7)",
            legendgroup="volume",
        ),
        row=2, col=1
    )

    fig.update_layout(
        template="plotly_dark",
        hovermode="x unified",
        height=850,
        margin=dict(t=80, b=40, l=60, r=20),
        legend_tracegroupgap=160,
    )

    fig.update_yaxes(title_text="Price (IRR)", row=1, col=1)
    fig.update_yaxes(title_text="Listings", row=2, col=1)
    fig.update_xaxes(title_text="Timestamp", row=2, col=1)

    return pyo.plot(fig, include_plotlyjs=False, output_type="div")


@app.route("/")
def index():
    summaries = load_all_summaries()
    if not summaries:
        return "<p>No summary JSON files found.</p>"

    chart_html = make_chart(summaries)
    latest = summaries[-1][1]
    latest_ts = summaries[-1][0].strftime("%Y-%m-%d %H:%M")

    last_data = {
        "timestamp": latest_ts,
        "overall": latest["overall_avg_price_per_sqm"],
        "age0_4": latest["age_intervals"]["0-4"]["avg"],
        "age5_9": latest["age_intervals"]["5-9"]["avg"],
        "age10_14": latest["age_intervals"]["10-14"]["avg"],
        "age15_20": latest["age_intervals"]["15-20"]["avg"],
    }

    return render_template("index.html", chart_html=chart_html, last_data=last_data)

def daily_refresh():
    print("Refreshing data at 22:00…")
    # your scraper or data updater here, e.g.:
    os.system("python3.13 runner.py")

def schedule_thread():
    schedule.every().day.at("00:08").do(daily_refresh)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
 threading.Thread(target=schedule_thread, daemon=True).start()
 app.run(host="0.0.0.0", port=8000, debug=True)
 