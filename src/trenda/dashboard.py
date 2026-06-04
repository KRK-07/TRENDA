from __future__ import annotations


def render_dashboard() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Trenda Dashboard</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #07111f;
      --bg-elevated: rgba(10, 20, 35, 0.88);
      --panel: rgba(15, 26, 44, 0.92);
      --border: rgba(150, 180, 255, 0.16);
      --text: #e6edf7;
      --muted: #93a4c3;
      --accent: #7dd3fc;
      --accent-2: #a78bfa;
      --good: #34d399;
      --bad: #fb7185;
      --warn: #fbbf24;
      --shadow: 0 18px 60px rgba(0, 0, 0, 0.35);
    }

    * { box-sizing: border-box; }
    html, body { margin: 0; min-height: 100%; background:
      radial-gradient(circle at top left, rgba(125, 211, 252, 0.18), transparent 30%),
      radial-gradient(circle at top right, rgba(167, 139, 250, 0.16), transparent 24%),
      linear-gradient(180deg, #040814 0%, var(--bg) 100%); color: var(--text); font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }

    body { padding: 32px 20px 48px; }
    .shell { max-width: 1280px; margin: 0 auto; }
    .hero {
      display: grid;
      grid-template-columns: 1.6fr 1fr;
      gap: 20px;
      align-items: stretch;
      margin-bottom: 20px;
    }
    .hero-card, .panel, .metric {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 24px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(16px);
    }
    .hero-card { padding: 28px; overflow: hidden; position: relative; }
    .hero-card::after {
      content: "";
      position: absolute;
      inset: auto -90px -120px auto;
      width: 280px;
      height: 280px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(125, 211, 252, 0.22), transparent 64%);
      pointer-events: none;
    }
    .eyebrow {
      display: inline-flex;
      gap: 8px;
      align-items: center;
      padding: 8px 12px;
      border-radius: 999px;
      border: 1px solid rgba(125, 211, 252, 0.24);
      background: rgba(12, 23, 39, 0.8);
      color: var(--accent);
      font-size: 12px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 16px;
    }
    h1 { margin: 0 0 10px; font-size: clamp(2.4rem, 5vw, 4.3rem); line-height: 0.98; letter-spacing: -0.05em; }
    .lead { max-width: 62ch; color: var(--muted); font-size: 1.03rem; line-height: 1.6; margin: 0; }
    .stats { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
    .metric { padding: 18px; min-height: 120px; display: flex; flex-direction: column; justify-content: space-between; }
    .metric .label { color: var(--muted); font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.08em; }
    .metric .value { font-size: 2rem; font-weight: 700; letter-spacing: -0.04em; }
    .metric .hint { color: var(--muted); font-size: 0.92rem; }
    .grid { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 18px; }
    .panel { padding: 22px; }
    .span-4 { grid-column: span 4; }
    .span-6 { grid-column: span 6; }
    .span-8 { grid-column: span 8; }
    .span-12 { grid-column: span 12; }
    .panel h2 { margin: 0 0 8px; font-size: 1.08rem; }
    .panel p.subtle { margin: 0 0 18px; color: var(--muted); font-size: 0.95rem; }
    .field-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
    .field-grid.three { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    label { display: flex; flex-direction: column; gap: 8px; color: var(--muted); font-size: 0.82rem; letter-spacing: 0.04em; text-transform: uppercase; }
    input, textarea, button {
      border-radius: 16px;
      border: 1px solid rgba(148, 163, 184, 0.22);
      background: rgba(5, 12, 25, 0.75);
      color: var(--text);
      font: inherit;
    }
    input, textarea { padding: 14px 16px; outline: none; }
    textarea { min-height: 118px; resize: vertical; }
    input:focus, textarea:focus { border-color: rgba(125, 211, 252, 0.7); box-shadow: 0 0 0 3px rgba(125, 211, 252, 0.12); }
    button {
      padding: 13px 16px;
      cursor: pointer;
      transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
      font-weight: 600;
      background: linear-gradient(135deg, rgba(125, 211, 252, 0.18), rgba(167, 139, 250, 0.18));
    }
    button:hover { transform: translateY(-1px); border-color: rgba(125, 211, 252, 0.45); box-shadow: 0 10px 28px rgba(5, 12, 25, 0.35); }
    .result {
      margin-top: 16px;
      padding: 16px;
      border-radius: 18px;
      background: rgba(2, 8, 23, 0.58);
      border: 1px solid rgba(148, 163, 184, 0.14);
      min-height: 124px;
      white-space: pre-wrap;
      overflow-x: auto;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      color: #dbeafe;
    }
    .signal-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 12px;
    }
    .buy { background: rgba(52, 211, 153, 0.14); color: #86efac; }
    .sell { background: rgba(251, 113, 133, 0.14); color: #fda4af; }
    .hold { background: rgba(251, 191, 36, 0.14); color: #fcd34d; }
    .curve {
      width: 100%;
      height: 220px;
      margin-top: 14px;
      border-radius: 18px;
      background: linear-gradient(180deg, rgba(15, 23, 42, 0.68), rgba(2, 6, 23, 0.68));
      border: 1px solid rgba(148, 163, 184, 0.14);
      overflow: hidden;
    }
    .footer-note { color: var(--muted); font-size: 0.9rem; margin-top: 14px; }
    .top-actions {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 18px;
    }
    .status-line {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 12px;
      margin-top: 16px;
      color: var(--muted);
      font-size: 0.92rem;
    }
    .live-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      border: 1px solid rgba(125, 211, 252, 0.22);
      background: rgba(5, 12, 25, 0.58);
      color: var(--accent);
    }
    .inline-toggle {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      text-transform: none;
      letter-spacing: 0;
      font-size: 0.95rem;
    }
    .ghost-button {
      background: rgba(5, 12, 25, 0.55);
    }
    @media (max-width: 1024px) {
      .hero, .stats, .field-grid, .field-grid.three { grid-template-columns: 1fr; }
      .span-4, .span-6, .span-8 { grid-column: span 12; }
      body { padding: 16px; }
    }
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <div class="hero-card">
        <div class="eyebrow">Trenda Control Center</div>
        <h1>Signals, portfolio health, and backtests in one view.</h1>
        <p class="lead">Run a quick market read, generate a technical signal, inspect portfolio exposure, and compare a simple SMA strategy against buy-and-hold without leaving the dashboard.</p>
        <div class="top-actions">
          <label class="live-pill inline-toggle">
            <input type="checkbox" id="live-refresh-toggle" checked />
            Live polling
          </label>
          <label class="live-pill inline-toggle">
            Poll interval (s)
            <input id="poll-interval" type="number" min="5" max="3600" step="5" value="30" style="width:80px;margin-left:8px;" />
          </label>
        </div>
        <div class="status-line">
          <span id="live-status">Live updates are on.</span>
          <span id="last-refresh-at">Waiting for first refresh.</span>
        </div>
      </div>
      <div class="stats">
        <div class="metric">
          <div class="label">Live panels</div>
          <div class="value">4</div>
          <div class="hint">Market, signal, portfolio, and backtest views.</div>
        </div>
        <div class="metric">
          <div class="label">Signal engine</div>
          <div class="value">SMA + RSI</div>
          <div class="hint">Trend direction, momentum, and volatility scoring.</div>
        </div>
        <div class="metric">
          <div class="label">Backtest model</div>
          <div class="value">Long only</div>
          <div class="hint">Simple crossover benchmark for fast iteration.</div>
        </div>
      </div>
    </section>

    <section class="grid">
      <article class="panel span-4">
        <h2>Market snapshot</h2>
        <p class="subtle">Fetch the latest close, change, and volume for any symbol.</p>
        <form id="market-form">
          <label>
            Symbol
            <input name="symbol" value="AAPL" autocomplete="off" />
          </label>
          <div style="height: 12px"></div>
          <button type="submit">Load snapshot</button>
        </form>
        <div class="result" id="market-result">Awaiting input...</div>
      </article>

      <article class="panel span-4">
        <h2>Trading signal</h2>
        <p class="subtle">Blend trend, RSI, and volatility into a directional bias.</p>
        <form id="signal-form">
          <label>
            Symbol
            <input name="symbol" value="AAPL" autocomplete="off" />
          </label>
          <div style="height: 12px"></div>
          <button type="submit">Generate signal</button>
        </form>
        <div class="result" id="signal-result">Awaiting input...</div>
      </article>

      <article class="panel span-4">
        <h2>Backtest</h2>
        <p class="subtle">Compare a crossover strategy against buy-and-hold.</p>
        <form id="backtest-form">
          <div class="field-grid three">
            <label>Symbol <input name="symbol" value="AAPL" autocomplete="off" /></label>
            <label>Initial cash <input name="initial_cash" type="number" step="100" value="10000" /></label>
            <label>Tx cost bps <input name="transaction_cost_bps" type="number" step="0.1" value="0" /></label>
          </div>
          <div style="height: 12px"></div>
          <div class="field-grid">
            <label>Short window <input name="short_window" type="number" value="10" /></label>
            <label>Long window <input name="long_window" type="number" value="30" /></label>
          </div>
          <div style="height: 12px"></div>
          <button type="submit">Run backtest</button>
        </form>
        <div class="result" id="backtest-result">Awaiting input...</div>
        <div id="backtest-curve" class="curve"></div>
      </article>

      <article class="panel span-12">
        <h2>Watchlist</h2>
        <p class="subtle">Comma-separated symbols to automatically refresh together.</p>
        <div style="display:flex;gap:12px;align-items:center;margin-bottom:12px;">
          <textarea id="watchlist" style="flex:1;min-height:48px;">AAPL,MSFT</textarea>
          <div style="display:flex;flex-direction:column;gap:8px;">
            <button id="update-watchlist">Update</button>
            <button id="clear-watchlist" class="ghost-button">Clear</button>
          </div>
        </div>
        <div class="result" id="watchlist-result">No symbols watched.</div>
      </article>

      <article class="panel span-12">
        <h2>Portfolio analyzer</h2>
        <p class="subtle">Paste a holdings JSON array and calculate market value, cost basis, and unrealized P&amp;L.</p>
        <form id="portfolio-form">
          <div class="field-grid">
            <label>
              Cash
              <input name="cash" type="number" step="1" value="0" />
            </label>
            <label>
              Holdings JSON
              <textarea name="holdings">[{"symbol":"AAPL","quantity":10,"average_cost":180},{"symbol":"MSFT","quantity":5,"average_cost":300}]</textarea>
            </label>
          </div>
          <div style="height: 12px"></div>
          <button type="submit">Analyze portfolio</button>
        </form>
        <div class="result" id="portfolio-result">Awaiting input...</div>
      </article>
    </section>

    <p class="footer-note">Endpoints are powered by the same backend used by the dashboard, so the UI stays consistent with API responses.</p>
  </main>

  <script>
    const pretty = (value) => JSON.stringify(value, null, 2);
    let refreshIntervalMs = 30000;
    let refreshTimer = null;

    const renderSignalBadge = (action) => `<span class="signal-pill ${action}">${action}</span>`;

    const renderCurve = (strategy, benchmark) => {
      const width = 1000;
      const height = 220;
      const allValues = [...strategy, ...benchmark];
      const min = Math.min(...allValues);
      const max = Math.max(...allValues);
      const scaleX = (index, length) => (index / Math.max(length - 1, 1)) * width;
      const scaleY = (value) => height - ((value - min) / Math.max(max - min, 1)) * (height - 24) - 12;
      const path = (series) => series.map((value, index) => `${index === 0 ? 'M' : 'L'} ${scaleX(index, series.length).toFixed(2)} ${scaleY(value).toFixed(2)}`).join(' ');
      return `
        <svg viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" width="100%" height="100%" aria-label="Backtest curves">
          <defs>
            <linearGradient id="strategyGradient" x1="0" x2="1" y1="0" y2="0">
              <stop offset="0%" stop-color="#7dd3fc" />
              <stop offset="100%" stop-color="#a78bfa" />
            </linearGradient>
            <linearGradient id="benchmarkGradient" x1="0" x2="1" y1="0" y2="0">
              <stop offset="0%" stop-color="#34d399" />
              <stop offset="100%" stop-color="#10b981" />
            </linearGradient>
          </defs>
          <path d="${path(benchmark)}" fill="none" stroke="url(#benchmarkGradient)" stroke-width="3" opacity="0.7" />
          <path d="${path(strategy)}" fill="none" stroke="url(#strategyGradient)" stroke-width="4" />
        </svg>
      `;
    };

    const setResult = (id, value) => {
      document.getElementById(id).innerHTML = value;
    };

    const fetchJson = async (url, options = {}) => {
      const response = await fetch(url, {
        headers: { "Content-Type": "application/json" },
        ...options,
      });
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || "Request failed");
      }
      return payload;
    };

    const liveEnabled = () => document.getElementById("live-refresh-toggle").checked;

    const setRefreshStatus = (message) => {
      document.getElementById("live-status").textContent = message;
      document.getElementById("last-refresh-at").textContent = `Last refreshed: ${new Date().toLocaleTimeString()}`;
    };

    const getWatchlistSymbols = () => {
      const raw = document.getElementById("watchlist").value || "";
      return Array.from(new Set(raw.split(/[,\\s]+/).map(s => s.trim().toUpperCase()).filter(Boolean)));
    };

    const renderWatchlist = (items) => {
      if (!items || items.length === 0) {
        setResult("watchlist-result", "No symbols watched.");
        return;
      }

      const parts = items.map(it => {
        const market = it.market ? `Market:\n${JSON.stringify(it.market, null, 2)}` : "";
        const signal = it.signal ? `Signal:\n${JSON.stringify(it.signal, null, 2)}` : "";
        const error = it.error ? `Error: ${it.error}` : "";
        const body = [market, signal, error].filter(Boolean).join('\\n\\n');
        return `<div style="margin-bottom:12px;"><strong>${it.symbol}</strong>\n<pre>${body}</pre></div>`;
      });
      setResult("watchlist-result", parts.join('\\n'));
    };

    const loadWatchlist = async () => {
      const symbols = getWatchlistSymbols();
      if (!symbols.length) {
        renderWatchlist([]);
        return;
      }

      const results = [];
      await Promise.all(symbols.map(async (s) => {
        try {
          const market = await fetchJson(liveEnabled() ? `/market/live/${encodeURIComponent(s)}` : `/market/${encodeURIComponent(s)}`);
          const signal = await fetchJson(liveEnabled() ? `/signals/live/${encodeURIComponent(s)}` : `/signals/${encodeURIComponent(s)}`);
          results.push({ symbol: s, market, signal });
        } catch (err) {
          results.push({ symbol: s, market: null, signal: null, error: String(err) });
        }
      }));

      renderWatchlist(results);
    };

    const loadMarketSnapshot = async () => {
      const symbol = new FormData(document.getElementById("market-form")).get("symbol");
      setResult("market-result", "Loading...");
      try {
        const endpoint = liveEnabled() ? `/market/live/${encodeURIComponent(symbol)}` : `/market/${encodeURIComponent(symbol)}`;
        setResult("market-result", pretty(await fetchJson(endpoint)));
      } catch (error) {
        setResult("market-result", `Error: ${error.message}`);
      }
    };

    const loadSignalSnapshot = async () => {
      const symbol = new FormData(document.getElementById("signal-form")).get("symbol");
      setResult("signal-result", "Loading...");
      try {
        const endpoint = liveEnabled() ? `/signals/live/${encodeURIComponent(symbol)}` : `/signals/${encodeURIComponent(symbol)}`;
        const signal = await fetchJson(endpoint);
        setResult(
          "signal-result",
          `${renderSignalBadge(signal.action)}\n${pretty(signal)}`
        );
      } catch (error) {
        setResult("signal-result", `Error: ${error.message}`);
      }
    };

    const refreshLivePanels = async () => {
      if (!liveEnabled() || document.visibilityState !== "visible") {
        setRefreshStatus(liveEnabled() ? "Live polling paused while tab is hidden." : "Live polling is off.");
        return;
      }
      const watchlistSymbols = getWatchlistSymbols();
      await Promise.all([loadMarketSnapshot(), loadSignalSnapshot(), loadWatchlist()]);
      setRefreshStatus(
        watchlistSymbols.length
          ? `Live updates are on for ${watchlistSymbols.length} watched symbol(s).`
          : "Live updates are on."
      );
    };

    document.getElementById("live-refresh-toggle").addEventListener("change", () => {
      if (liveEnabled()) {
        refreshLivePanels();
      } else {
        document.getElementById("live-status").textContent = "Live polling is off.";
        document.getElementById("last-refresh-at").textContent = "";
      }
    });

    document.getElementById("poll-interval").addEventListener("change", (e) => {
      const val = Number(e.currentTarget.value) || 30;
      refreshIntervalMs = Math.max(5000, val * 1000);
      if (refreshTimer) {
        clearInterval(refreshTimer);
        refreshTimer = setInterval(refreshLivePanels, refreshIntervalMs);
      }
    });

    document.getElementById("update-watchlist").addEventListener("click", () => {
      loadWatchlist();
    });

    document.getElementById("clear-watchlist").addEventListener("click", () => {
      document.getElementById("watchlist").value = "";
      renderWatchlist([]);
    });

    document.getElementById("market-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      await loadMarketSnapshot();
    });

    document.getElementById("signal-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      await loadSignalSnapshot();
    });

    document.getElementById("portfolio-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      const form = new FormData(event.currentTarget);
      setResult("portfolio-result", "Loading...");
      try {
        const payload = {
          cash: Number(form.get("cash")),
          holdings: JSON.parse(form.get("holdings")),
        };
        setResult(
          "portfolio-result",
          pretty(await fetchJson("/portfolio/analyze", {
            method: "POST",
            body: JSON.stringify(payload),
          }))
        );
      } catch (error) {
        setResult("portfolio-result", `Error: ${error.message}`);
      }
    });

    document.getElementById("backtest-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      const form = new FormData(event.currentTarget);
      setResult("backtest-result", "Loading...");
      try {
        const payload = {
          symbol: form.get("symbol"),
          initial_cash: Number(form.get("initial_cash")),
          short_window: Number(form.get("short_window")),
          long_window: Number(form.get("long_window")),
          transaction_cost_bps: Number(form.get("transaction_cost_bps")),
        };
        const backtest = await fetchJson("/backtest", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        setResult("backtest-result", pretty(backtest));
        document.getElementById("backtest-curve").innerHTML = renderCurve(backtest.strategy_curve, backtest.buy_and_hold_curve);
      } catch (error) {
        setResult("backtest-result", `Error: ${error.message}`);
      }
    });

    refreshLivePanels();
    refreshTimer = setInterval(refreshLivePanels, refreshIntervalMs);
  </script>
</body>
</html>"""
