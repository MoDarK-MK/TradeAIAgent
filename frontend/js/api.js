const API_CONFIG = {
  baseUrl: "http://localhost:8000/api",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
};

class APIRequest {
  constructor(config = {}) {
    this.config = { ...API_CONFIG, ...config };
  }

  async request(method, endpoint, options = {}) {
    const url = `${this.config.baseUrl}${endpoint}`;

    const config = {
      method,
      headers: {
        ...this.config.headers,
        ...options.headers,
      },
      timeout: this.config.timeout,
    };

    if (options.body) {
      config.body = JSON.stringify(options.body);
    }

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new APIError(
          error.message || `HTTP ${response.status}`,
          response.status,
          error
        );
      }

      const data = await response.json();
      return data;
    } catch (error) {
      if (error instanceof APIError) {
        throw error;
      }
      throw new APIError(error.message, 0, error);
    }
  }

  get(endpoint, options = {}) {
    return this.request("GET", endpoint, options);
  }

  post(endpoint, body, options = {}) {
    return this.request("POST", endpoint, { ...options, body });
  }

  put(endpoint, body, options = {}) {
    return this.request("PUT", endpoint, { ...options, body });
  }

  delete(endpoint, options = {}) {
    return this.request("DELETE", endpoint, options);
  }

  async postForm(endpoint, formData, options = {}) {
    const url = `${this.config.baseUrl}${endpoint}`;

    const config = {
      method: "POST",
      headers: {
        ...options.headers,
      },
      timeout: this.config.timeout,
      body: formData,
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new APIError(
          error.message || `HTTP ${response.status}`,
          response.status,
          error
        );
      }

      const data = await response.json();
      return data;
    } catch (error) {
      if (error instanceof APIError) {
        throw error;
      }
      throw new APIError(error.message, 0, error);
    }
  }
}

class APIError extends Error {
  constructor(message, status = 0, details = {}) {
    super(message);
    this.name = "APIError";
    this.status = status;
    this.details = details;
  }
}

class TradingAPI {
  constructor() {
    this.api = new APIRequest();
  }

  async analyzeChart(data) {
    if (data instanceof FormData) {
      return this.api.postForm("/analyze", data);
    }
    return this.api.post("/analyze", data);
  }

  async getSummary() {
    return this.api.get("/summary");
  }

  async getIndicators() {
    return this.api.get("/indicators/list");
  }

  async getHistory(params = {}) {
    const queryString = buildQueryString(params);
    const endpoint = `/history${queryString ? "?" + queryString : ""}`;
    return this.api.get(endpoint);
  }

  async getPortfolio() {
    return this.api.get("/portfolio");
  }

  async executeTrade(tradeData) {
    return this.api.post("/trades/execute", tradeData);
  }

  async getTrade(tradeId) {
    return this.api.get(`/trades/${tradeId}`);
  }

  async closeTrade(tradeId, closeData) {
    return this.api.post(`/trades/${tradeId}/close`, closeData);
  }

  async getPerformance() {
    return this.api.get("/performance");
  }

  async healthCheck() {
    return this.api.get("/health");
  }

  async getMarketData(symbol = "BTC/USD", limit = 100) {
    return this.api.get(`/market/data?symbol=${symbol}&limit=${limit}`);
  }

  async getAvailableSymbols() {
    return this.api.get("/market/symbols");
  }

  async getRecentSignals(limit = 10) {
    return this.api.get(`/signals/recent?limit=${limit}`);
  }

  async getSignalsStatistics() {
    return this.api.get("/signals/statistics");
  }
}

class SignalWebSocket {
  constructor(url = "ws://localhost:8000/ws/signals") {
    this.url = url;
    this.ws = null;
    this.listeners = {};
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 3000;
  }

  connect() {
    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
          console.log("WebSocket connected");
          this.reconnectAttempts = 0;
          this.emit("connected");
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            this.emit("signal", data);
          } catch (error) {
            console.error("Failed to parse message:", error);
          }
        };

        this.ws.onerror = (error) => {
          console.error("WebSocket error:", error);
          this.emit("error", error);
          reject(error);
        };

        this.ws.onclose = () => {
          console.log("WebSocket disconnected");
          this.emit("disconnected");
          this.attemptReconnect();
        };
      } catch (error) {
        reject(error);
      }
    });
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Reconnecting (attempt ${this.reconnectAttempts})...`);

      setTimeout(() => {
        this.connect().catch(() => {});
      }, this.reconnectDelay);
    } else {
      console.error("Max reconnect attempts reached");
      this.emit("reconnect_failed");
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(callback);
  }

  off(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event] = this.listeners[event].filter(
        (cb) => cb !== callback
      );
    }
  }

  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach((callback) => {
        callback(data);
      });
    }
  }

  isConnected() {
    return this.ws && this.ws.readyState === WebSocket.OPEN;
  }
}

const api = new TradingAPI();

let signalWS = null;

async function initializeWebSocket() {
  if (!signalWS) {
    signalWS = new SignalWebSocket();
  }

  return signalWS.connect();
}

function disconnectWebSocket() {
  if (signalWS) {
    signalWS.disconnect();
  }
}

function handleAPIError(error) {
  console.error("API Error:", error);

  let message = error.message;
  let type = "error";

  if (error.status === 0) {
    message = "Failed to connect to server. Please check your connection.";
  } else if (error.status === 400) {
    message = error.details?.message || "Invalid request parameters";
  } else if (error.status === 401) {
    message = "Authentication failed. Please log in again.";
  } else if (error.status === 403) {
    message = "You do not have permission to access this resource.";
  } else if (error.status === 404) {
    message = "Resource not found.";
  } else if (error.status === 429) {
    message = "Too many requests. Please try again later.";
    type = "warning";
  } else if (error.status >= 500) {
    message = "Server error. Please try again later.";
  }

  showToast(message, type);
  return { message, type };
}

async function withErrorHandling(apiCall, options = {}) {
  try {
    return await apiCall;
  } catch (error) {
    handleAPIError(error);

    if (options.onError) {
      options.onError(error);
    }

    throw error;
  }
}
