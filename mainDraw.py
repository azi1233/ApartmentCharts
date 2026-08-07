#!/usr/bin/env python3
#from flask import Flask, render_template
import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.graph_objs as go
from pathlib import Path
from datetime import datetime
import json, os, gzip
import threading,schedule, time
from jinja2 import Environment, FileSystemLoader
import runner


#app = Flask(__name__)


def load_all_summaries(DIVAR_RESULTS):
    summaries = []
    for folder in sorted(DIVAR_RESULTS.iterdir()):
        if not folder.is_dir():
            continue
        for pattern in ("summary_*.json.gz", "summary_*.json"):
            for file in folder.glob(pattern):
                try:
                    if file.suffix == ".gz":
                        opener = lambda f: gzip.open(f, "rt", encoding="utf-8")
                    else:
                        opener = lambda f: open(f, "r", encoding="utf-8")
                    with opener(file) as f:
                        data = json.load(f)
                        ts = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
                        summaries.append((ts, data))
                except Exception:
                    pass
    summaries.sort(key=lambda x: x[0])
    return summaries

def filter_zeros_connect_gaps(timestamps, values, counts):
    filtered_ts = []
    filtered_vals = []
    filtered_counts = []
    for ts, val, cnt in zip(timestamps, values, counts):
        if val != 0:
            filtered_ts.append(ts)
            filtered_vals.append(val)
            filtered_counts.append(cnt)
    return filtered_ts, filtered_vals, filtered_counts

def make_chart(summaries):
    import plotly.subplots as sp
    import plotly.graph_objs as go

    timestamps = [s[0] for s in summaries]
    data_count = len(summaries)
    
    # Trading-style configuration
    is_large_dataset = data_count >= 1000  # Enable advanced features for 1000+ days
    
    # Price-related data
    overall = [s[1]["overall_avg_price_per_sqm"] for s in summaries]
    overall_count = [s[1]["valid_for_averages"] for s in summaries]

    def get_age_data(interval):
        return (
            [s[1]["age_intervals"][interval]["avg"] for s in summaries],
            [s[1]["age_intervals"][interval]["count"] for s in summaries],
        )

    def get_size_data(interval):
        return (
            [s[1]["size_intervals"][interval]["avg"] for s in summaries],
            [s[1]["size_intervals"][interval]["count"] for s in summaries],
        )

    age0_4, cnt0_4 = get_age_data("0-4")
    age5_9, cnt5_9 = get_age_data("5-9")
    age10_14, cnt10_14 = get_age_data("10-14")
    age15_20, cnt15_20 = get_age_data("15-20")

    size_small, cnt_small = get_size_data("<80")
    size_mid, cnt_mid = get_size_data("80-120")
    size_large, cnt_large = get_size_data(">120")

    # Filter out zero values for overall data series
    overall_f, overall_count_f = [], []
    for ts, ov in zip(timestamps, overall):
        if ov != 0:
            overall_f.append(ts)
            overall_count_f.append(ov)

    # Create trading-view subplot layout with enhanced features
    if is_large_dataset:
        # Advanced layout for 1000+ days - trading view style
        fig = sp.make_subplots(
            rows=3,  # Add extra row for volume and indicators
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.5, 0.3, 0.2],  # Price chart larger, volume and indicators smaller
            subplot_titles=(
                "Apartment Price Trends (IRR/m²)", 
                "Market Activity", 
                "Trading Indicators"
            ),
            specs=[[{"secondary_y": False}], [{"secondary_y": True, "type": "bar"}], [{"secondary_y": True, "type": "indicator"}]]
        )
    else:
        # Standard layout for smaller datasets
        fig = sp.make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3],
            subplot_titles=("Average Price per m² Over Time", "Number of Listings Over Time"),
        )

    # --- Chart 1: Overall Price + Age + Size ---
    age_configs = [
        ("0-4", "#00D08B"),
        ("5-9", "#0087FF"),
        ("10-14", "#FF4500"),
        ("15-20", "#DC143C"),
    ]

    latest = summaries[-1][1]
    total_valid = latest["valid_for_averages"]
    age_counts = {label: latest["age_intervals"][label]["count"] for label, _ in age_configs}

    min_price = min(overall_count_f)
    max_price = max(overall_count_f)

    fig.add_trace(
        go.Scatter(
            x=overall_f,
            y=overall_count_f,
            mode="lines+markers",
            name=f"Overall ({total_valid})",
            legendrank=1,
            line=dict(width=4, color="#FF6B35"),
            marker=dict(size=4, color="#FF6B35"),
            connectgaps=True,
            hovertemplate="Overall<br>%{y:,.0f}<extra></extra>",
        ),
        row=1, col=1
    )

    for i, (age_label, color) in enumerate(age_configs):
        age_count = age_counts[age_label]
        age_pairs = [
            (s[0], s[1]["age_intervals"][age_label]["avg"])
            for s in summaries
            if s[1]["age_intervals"][age_label]["avg"] != 0
        ]
        fig.add_trace(
            go.Scatter(
                x=[p[0] for p in age_pairs],
                y=[p[1] for p in age_pairs],
                mode="lines+markers",
                name=f"Age {age_label} ({age_count})",
                legendrank=10 + i,
                line=dict(width=2, color=color),
                marker=dict(size=4, color=color),
                connectgaps=True,
                hovertemplate=f"Age {age_label}<br>%{{y:,.0f}}<extra></extra>",
            ),
            row=1, col=1
        )

    size_configs = [
        ("<80", "#32CD32", "<80m²"),
        ("80-120", "#10B981", "80-120m²"),
        (">120", "#F59E0B", ">120m²"),
    ]

    size_counts = {key: latest["size_intervals"][key]["count"] for key, _, _ in size_configs}

    for i, (size_key, color, label) in enumerate(size_configs):
        size_count = size_counts[size_key]
        size_pairs = [
            (s[0], s[1]["size_intervals"][size_key]["avg"])
            for s in summaries
            if s[1]["size_intervals"][size_key]["avg"] != 0
        ]
        fig.add_trace(
            go.Scatter(
                x=[p[0] for p in size_pairs],
                y=[p[1] for p in size_pairs],
                mode="lines+markers",
                name=f"Size {label} ({size_count})",
                legendrank=20 + i,
                line=dict(width=2, color=color, dash="dot"),
                marker=dict(size=4, color=color),
                connectgaps=True,
                hovertemplate=f"Size {label}<br>%{{y:,.0f}}<extra></extra>",
            ),
            row=1, col=1
        )

    # --- Chart 2: Listing Counts ---
    total_posts = [s[1]["total_posts"] for s in summaries]
    valid_posts = [s[1]["valid_for_averages"] for s in summaries]
    latest_total = latest["total_posts"]
    latest_valid = latest["valid_for_averages"]

    if is_large_dataset:
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=total_posts,
                name=f"Total ({latest_total})",
                legendgroup="listings",
                mode="lines",
                line=dict(width=1, color="rgba(52, 152, 219, 0.8)"),
                fill='tozeroy',
                fillcolor="rgba(52, 152, 219, 0.15)",
                hovertemplate="Total listings: %{y}<extra></extra>"
            ),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=valid_posts,
                name=f"Valid ({latest_valid})",
                legendgroup="listings",
                mode="lines",
                line=dict(width=1, color="rgba(46, 204, 113, 0.8)"),
                fill='tozeroy',
                fillcolor="rgba(46, 204, 113, 0.15)",
                hovertemplate="Valid listings: %{y}<extra></extra>",
            ),
            row=2, col=1
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=total_posts,
                name=f"Total ({latest_total})",
                legendgroup="listings",
                mode="lines+markers",
                marker=dict(size=4, color="rgba(100, 149, 237, 0.8)"),
                line=dict(width=1, color="rgba(100, 149, 237, 0.5)"),
                fill='tozeroy',
                fillcolor="rgba(100, 149, 237, 0.1)",
                hovertemplate="Total listings: %{y}<extra></extra>"
            ),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=valid_posts,
                name=f"Valid ({latest_valid})",
                legendgroup="listings",
                mode="lines+markers",
                marker=dict(size=4, color="rgba(255, 152, 0, 0.8)"),
                line=dict(width=1, color="rgba(255, 152, 0, 0.5)"),
                fill='tozeroy',
                fillcolor="rgba(255, 152, 0, 0.1)",
                hovertemplate="Valid listings: %{y}<extra></extra>",
            ),
            row=2, col=1
        )
    
    # --- Chart 3: Trading Indicators (only for large datasets) ---
    if is_large_dataset and len(overall_f) > 0:
        # Calculate price changes for volatility and momentum
        if len(overall_f) > 1:
            price_changes = [overall_f[i] - overall_f[i-1] for i in range(1, len(overall_f))]
            avg_change = sum(price_changes) / len(price_changes)
            
            # Moving averages
            ma_short = sum(overall_f[-20:]) / len(overall_f[-20:]) if len(overall_f) >= 20 else overall_f[-1]
            ma_long = sum(overall_f[-50:]) / len(overall_f[-50:]) if len(overall_f) >= 50 else overall_f[-1]
            
            # Volatility (standard deviation)
            if len(overall_f) > 10:
                import statistics
                volatility = statistics.stdev(overall_f[-30:])
            else:
                volatility = 0
            
            # Add indicators
            fig.add_trace(
                go.Indicator(
                    mode="number+gauge+delta",
                    value=overall_f[-1],
                    delta=dict(reference=ma_short, valueformat=".2s"),
                    title=dict(text="Current Price"),
                    gauge=dict(
                        axis=dict(range=[None, max(overall_f) * 1.2], tickwidth=1),
                        bar=dict(color="darkblue", thickness=0.3),
                        bgcolor="lightgray",
                        steps=[
                            dict(range=[None, max(overall_f) * 0.7], color="lightgreen"),
                            dict(range=[max(overall_f) * 0.7, max(overall_f) * 0.9], color="yellow"),
                            dict(range=[max(overall_f) * 0.9, max(overall_f)], color="orange")
                        ]
                    ),
                    domain=dict(row=0, column=0),
                    number=dict(font=dict(size=26), valueformat=",.0f")
                ),
                row=3, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=timestamps[-len(ma_short):],
                    y=ma_short,
                    mode="lines",
                    name="MA(20)",
                    legendrank=30,
                    line=dict(color="orange", width=2, dash="dash"),
                    connectgaps=False,
                    hovertemplate="MA(20)<br>%{y:,.0f}<extra></extra>"
                ),
                row=1, col=1
            )

            fig.add_trace(
                go.Scatter(
                    x=timestamps[-len(ma_long):],
                    y=ma_long,
                    mode="lines",
                    name="MA(50)",
                    legendrank=31,
                    line=dict(color="purple", width=2, dash="dot"),
                    connectgaps=False,
                    hovertemplate="MA(50)<br>%{y:,.0f}<extra></extra>"
                ),
                row=1, col=1
            )

    # Enhanced layout configuration
    layout_config = dict(
        template="plotly_dark",
        hovermode="x unified",
        height=1000 if is_large_dataset else 850,
        margin=dict(t=100, b=60, l=80, r=120),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.0,
            xanchor="left",
            x=1.02,
            font=dict(size=13),
            bgcolor="rgba(0,0,0,0.3)",
            bordercolor="rgba(255,255,255,0.1)",
            borderwidth=1
        ),
        showlegend=True,
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.1)",
            type="date"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.1)",
            title_text="Price (IRR/m²)" if not is_large_dataset else "Price (IRR)",
            side="left",
            range=[min_price, None]
        )
    )
    
    if is_large_dataset:
        layout_config.update({
            'yaxis2': dict(title="Listings", side="left"),
            'yaxis3': dict(title="Trading Indicators", side="left", showgrid=False)
        })
    else:
        layout_config.update({
            'yaxis2': dict(title="Listings"),
        })

    fig.update_layout(**layout_config)

    fig.update_yaxes(title_text="Price (IRR/m²)", row=1, col=1, range=[min_price, None])
    fig.update_yaxes(title_text="Listings", row=2, col=1, autorange=True)
    fig.update_xaxes(title_text="Date", row=2, col=1)

    return pyo.plot(fig, include_plotlyjs=False, output_type="div")


#@app.route("/")
#def index():
#    summaries = load_all_summaries()
#    if not summaries:
#        return "<p>No summary JSON files found.</p>"
#
#    chart_html = make_chart(summaries)
#    latest = summaries[-1][1]
#    latest_ts = summaries[-1][0].strftime("%Y-%m-%d %H:%M")
#
#    last_data = {
#        "timestamp": latest_ts,
#        "overall": latest["overall_avg_price_per_sqm"],
#        "age0_4": latest["age_intervals"]["0-4"]["avg"],
#        "age5_9": latest["age_intervals"]["5-9"]["avg"],
#        "age10_14": latest["age_intervals"]["10-14"]["avg"],
#        "age15_20": latest["age_intervals"]["15-20"]["avg"],
#    }

    return render_template("index.html", chart_html=chart_html, last_data=last_data)
def render_report(summaries,OUTPUT_FILE,TEMPLATE_DIR,TEMPLATE_FILE):
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

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template(TEMPLATE_FILE)
    chart_html = make_chart(summaries)
    html_title = str(OUTPUT_FILE)
    html_title=html_title.removesuffix("_report.html")
    html = template.render(chart_html=chart_html, last_data=last_data, report_title=html_title, tab_title=html_title)

    OUTPUT_FILE.write_text(html, encoding="utf-8")
    print(f"Saved report to {OUTPUT_FILE.resolve()}")




def daily_refresh():
    print("Refreshing data at 22:00…")
    # your scraper or data updater here, e.g.:
    runner.run()

def schedule_thread():
    schedule.every().day.at("00:08").do(daily_refresh)
    while True:
        schedule.run_pending()
        time.sleep(60)
           
           
def drawer(outputfile, path_save):
    TEMPLATE_DIR = "templates"
    TEMPLATE_FILE = "template.html"
    OUTPUT_FILE = Path(outputfile)
    DIVAR_RESULTS = Path(path_save)
    #threading.Thread(target=schedule_thread, daemon=True).start()
    #app.run(host="0.0.0.0", port=8000, debug=True)
    summaries = load_all_summaries(DIVAR_RESULTS)
    if not summaries:
       print("No summary JSON files found.")
       exit(1)
    else:
       render_report(summaries,OUTPUT_FILE,TEMPLATE_DIR,TEMPLATE_FILE)