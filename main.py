from pathlib import Path
import mainDraw

def main():
    mainDraw.daily_refresh()
    divar_root = Path("divar_results")
    root = Path("./")
    if not divar_root.exists():
        print("divar_results directory not found.")
        return

    folders = [f for f in divar_root.iterdir() if f.is_dir()]
    if not folders:
        print("No folders found in divar_results.")
        return

    # --- Generate reports ---
    for folder in folders:
        report_path = f"{folder.name}_report.html"
        print(f"Generating report for {folder.name} -> {report_path}")
        mainDraw.drawer(str(report_path), str(folder))

    # --- Create index.html ---
    # --- Create index.html ---
    index_file = Path("index.html")
    html_lines = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "  <meta charset='utf-8'>",
        "  <meta name='viewport' content='width=device-width,initial-scale=1'>",
        "  <title>Divar Results Index</title>",
        "  <style>",
        "    :root{",
        "      --bg:#121212; --card:#1e1e2e; --muted:#90a4ae; --text:#e0e0e0; --accent:#ffab40;",
        "      --btn-bg:#171722; --btn-hover:#23232b;",
        "    }",
        "    html,body{height:100%;margin:0;padding:0;background:var(--bg);color:var(--text);font-family:'Segoe UI', Roboto, Arial, sans-serif;}",
        "    .wrap{max-width:1100px;margin:28px auto;padding:28px;}",
        "    header{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:24px;}",
        "    h1{margin:0;font-size:1.6rem;color:var(--accent);font-weight:600}",
        "    .subtitle{color:var(--muted);font-size:0.95rem}",
        "    .grid{display:flex;flex-wrap:wrap;row-gap:30px;column-gap:12px;margin-top:18px}",
        "    .btn{",
        "      display:inline-flex;align-items:center;justify-content:center;gap:8px;",
        "      padding:12px 18px;text-decoration:none;border-radius:10px;min-width:220px;flex-shrink:0;height:auto;",
        "      background:linear-gradient(180deg,var(--btn-bg),var(--card));box-shadow:0 6px 18px rgba(0,0,0,0.6);color:var(--text);",
        "      border:1px solid rgba(255,255,255,0.03);transition:transform .15s ease,box-shadow .15s ease,background .15s;",
        "    }",
        "    .btn .name{font-weight:600}",
        "    .btn .meta{font-size:0.85rem;color:var(--muted)}",
        "    .btn:hover{transform:translateY(-6px);box-shadow:0 14px 30px rgba(0,0,0,0.7);background:var(--btn-hover)}",
        "    .controls{display:flex;gap:12px;align-items:center;flex-wrap:wrap}",
        "    .search{padding:8px 12px;border-radius:8px;background:#0f0f12;border:1px solid rgba(255,255,255,0.03);color:var(--text)}",
        "    footer{margin-top:28px;color:var(--muted);font-size:0.85rem;text-align:center}",
        "    @media (max-width:640px){.btn{min-width:100%;justify-content:flex-start;padding:12px;border-radius:12px}}",
        "  </style>",
        "</head>",
        "<body>",
        "  <div class='wrap'>",
        "    <header>",
        "      <div>",
        "        <h1>Reports</h1>",
        "        <div class='subtitle'>Divar scrape results — open a folder to view its report</div>",
        "      </div>",
        "      <div class='controls'>",
        "        <!-- optional search -->",
        "        <input class='search' placeholder='Filter reports (client-side)...' oninput=\"(function(){const q=this.value.toLowerCase();document.querySelectorAll('.btn').forEach(b=>{b.style.display = (b.datasetName.toLowerCase().includes(q)||b.datasetMeta.toLowerCase().includes(q)) ? 'inline-flex' : 'none';});}).call(this)\" />",
        "      </div>",
        "    </header>",
        "",
        "    <div class='grid'>",
        "      <!-- Buttons for each folder will be inserted here -->",
        "      <!-- Example: <a class='btn' href='FOLDERNAME_report.html'>FOLDERNAME</a> -->",
        "    </div>",
        "",
        "    <footer>",
        "      Generated reports — open locally in your browser. <span style='color:var(--muted)'>Dark, modern theme</span>",
        "    </footer>",
        "  </div>",
        "",
        "  <script>",
        "    document.addEventListener('DOMContentLoaded', ()=>{",
        "      document.querySelectorAll('.grid a.btn').forEach(a=>{",
        "        a.datasetName = a.dataset.name || a.textContent.trim();",
        "        a.datasetMeta = a.dataset.meta || '';",
        "      });",
        "    });",
        "  </script>",
        "</body>",
        "</html>",
    ]
    
        
    for folder in folders:
        link = f"{folder.name}_report.html"
        html_lines.append(f"  <a class='btn' href='{link}'>{folder.name}</a>")
    html_lines += ["</body>", "</html>"]

    index_file.write_text("\n".join(html_lines), encoding="utf-8")
    print(f"Index created at: {index_file}")

if __name__ == "__main__":
    main()
