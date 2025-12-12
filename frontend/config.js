const API_CONFIGURATION = {
  development: {
    baseUrl: "http://localhost:8000",
    wsUrl: "ws://localhost:8000",
  },
  production: {
    baseUrl: "https://api.modtrade.com",
    wsUrl: "wss://api.modtrade.com",
  },
};

function getApiConfig() {
  const isDev =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1";
  return isDev ? API_CONFIGURATION.development : API_CONFIGURATION.production;
}

const API_ENDPOINTS = {
  HEALTH: "/health",
  ANALYZE: "/analyze",
  SUMMARY: "/summary",
  MARKET_DATA: "/market/data",
  MARKET_SYMBOLS: "/market/symbols",
  SIGNALS_RECENT: "/signals/recent",
  SIGNALS_STATISTICS: "/signals/statistics",
  INDICATORS_LIST: "/indicators/list",
  HISTORY: "/history",
  PORTFOLIO: "/portfolio",
  BACKTEST: "/backtest",
};

const WEBSOCKET_EVENTS = {
  CONNECTED: "connected",
  DISCONNECTED: "disconnected",
  NEW_SIGNAL: "new_signal",
  MARKET_UPDATE: "market_update",
  ERROR: "error",
  RECONNECT_FAILED: "reconnect_failed",
};

export { getApiConfig, API_ENDPOINTS, WEBSOCKET_EVENTS };
