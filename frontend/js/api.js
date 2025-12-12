/* ═══════════════════════════════════════════════════════════════════ */
/* API INTEGRATION MODULE                                               */
/* ═══════════════════════════════════════════════════════════════════ */

/**
 * API Configuration
 */
const API_CONFIG = {
  baseUrl: "http://localhost:8000/api",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
};

/**
 * API Request Class
 */
class APIRequest {
  constructor(config = {}) {
    this.config = { ...API_CONFIG, ...config };
  }

  /**
   * Make HTTP request
   * @param {string} method - HTTP method
   * @param {string} endpoint - API endpoint
   * @param {Object} options - Request options
   * @returns {Promise} Response data
   */
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

  /**
   * GET request
   */
  get(endpoint, options = {}) {
    return this.request("GET", endpoint, options);
  }

  /**
   * POST request
   */
  post(endpoint, body, options = {}) {
    return this.request("POST", endpoint, { ...options, body });
  }

  /**
   * PUT request
   */
  put(endpoint, body, options = {}) {
    return this.request("PUT", endpoint, { ...options, body });
  }

  /**
   * DELETE request
   */
  delete(endpoint, options = {}) {
    return this.request("DELETE", endpoint, options);
  }

  /**
   * POST with FormData (for file uploads)
   */
  async postForm(endpoint, formData, options = {}) {
    const url = `${this.config.baseUrl}${endpoint}`;

    const config = {
      method: "POST",
      headers: {
        ...options.headers,
        // Don't set Content-Type for FormData, browser will set it
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

/**
 * Custom API Error class
 */
class APIError extends Error {
  constructor(message, status = 0, details = {}) {
    super(message);
    this.name = "APIError";
    this.status = status;
    this.details = details;
  }
}

/**
 * Trading API Service
 */
class TradingAPI {
  constructor() {
    this.api = new APIRequest();
  }

  /**
   * Analyze trading chart
   * @param {FormData|Object} data - Analysis parameters
   * @returns {Promise} Analysis result
   */
  async analyzeChart(data) {
    if (data instanceof FormData) {
      return this.api.postForm("/analyze", data);
    }
    return this.api.post("/analyze", data);
  }

  /**
   * Get analysis summary
   * @returns {Promise} Summary data
   */
  async getSummary() {
    return this.api.get("/summary");
  }

  /**
   * Get available indicators
   * @returns {Promise} List of indicators
   */
  async getIndicators() {
    return this.api.get("/indicators/list");
  }

  /**
   * Get trading history
   * @param {Object} params - Query parameters
   * @returns {Promise} History data
   */
  async getHistory(params = {}) {
    const queryString = buildQueryString(params);
    const endpoint = `/history${queryString ? "?" + queryString : ""}`;
    return this.api.get(endpoint);
  }

  /**
   * Get portfolio data
   * @returns {Promise} Portfolio data
   */
  async getPortfolio() {
    return this.api.get("/portfolio");
  }

  /**
   * Execute trade
   * @param {Object} tradeData - Trade parameters
   * @returns {Promise} Trade execution result
   */
  async executeTrade(tradeData) {
    return this.api.post("/trades/execute", tradeData);
  }

  /**
   * Get trade details
   * @param {string} tradeId - Trade ID
   * @returns {Promise} Trade data
   */
  async getTrade(tradeId) {
    return this.api.get(`/trades/${tradeId}`);
  }

  /**
   * Close trade
   * @param {string} tradeId - Trade ID
   * @param {Object} closeData - Close parameters
   * @returns {Promise} Close result
   */
  async closeTrade(tradeId, closeData) {
    return this.api.post(`/trades/${tradeId}/close`, closeData);
  }

  /**
   * Get performance metrics
   * @returns {Promise} Performance data
   */
  async getPerformance() {
    return this.api.get("/performance");
  }

  /**
   * Health check
   * @returns {Promise} Server status
   */
  async healthCheck() {
    return this.api.get("/health");
  }
}

/**
 * WebSocket Manager for real-time signals
 */
class SignalWebSocket {
  constructor(url = "ws://localhost:8000/ws/signals") {
    this.url = url;
    this.ws = null;
    this.listeners = {};
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 3000;
  }

  /**
   * Connect to WebSocket
   */
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

  /**
   * Attempt to reconnect
   */
  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Reconnecting (attempt ${this.reconnectAttempts})...`);

      setTimeout(() => {
        this.connect().catch(() => {
          // Retry will happen in onclose
        });
      }, this.reconnectDelay);
    } else {
      console.error("Max reconnect attempts reached");
      this.emit("reconnect_failed");
    }
  }

  /**
   * Disconnect WebSocket
   */
  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  /**
   * Send message
   * @param {Object} data - Data to send
   */
  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  /**
   * Listen to events
   * @param {string} event - Event name
   * @param {function} callback - Callback function
   */
  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(callback);
  }

  /**
   * Remove event listener
   * @param {string} event - Event name
   * @param {function} callback - Callback function
   */
  off(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event] = this.listeners[event].filter(
        (cb) => cb !== callback
      );
    }
  }

  /**
   * Emit event
   * @param {string} event - Event name
   * @param {*} data - Event data
   */
  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach((callback) => {
        callback(data);
      });
    }
  }

  /**
   * Check if connected
   * @returns {boolean} Connection status
   */
  isConnected() {
    return this.ws && this.ws.readyState === WebSocket.OPEN;
  }
}

/* ═══════════════════════════════════════════════════════════════════ */
/* GLOBAL API INSTANCES                                                 */
/* ═══════════════════════════════════════════════════════════════════ */

// Create global API instance
const api = new TradingAPI();

// Create WebSocket instance (don't connect automatically)
let signalWS = null;

/**
 * Initialize WebSocket connection
 * @returns {Promise}
 */
async function initializeWebSocket() {
  if (!signalWS) {
    signalWS = new SignalWebSocket();
  }

  return signalWS.connect();
}

/**
 * Disconnect WebSocket
 */
function disconnectWebSocket() {
  if (signalWS) {
    signalWS.disconnect();
  }
}

/* ═══════════════════════════════════════════════════════════════════ */
/* ERROR HANDLER MIDDLEWARE                                            */
/* ═══════════════════════════════════════════════════════════════════ */

/**
 * Handle API errors
 * @param {APIError} error - API error
 */
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

/**
 * Wrap API call with error handling
 * @param {Promise} apiCall - API call promise
 * @param {Object} options - Options
 * @returns {Promise}
 */
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

/* ═══════════════════════════════════════════════════════════════════ */
/* EXPORT FOR MODULE USAGE                                             */
/* ═══════════════════════════════════════════════════════════════════ */

// if (typeof module !== 'undefined' && module.exports) {
//   module.exports = {
//     APIRequest,
//     APIError,
//     TradingAPI,
//     SignalWebSocket,
//     api,
//     initializeWebSocket,
//     disconnectWebSocket,
//     handleAPIError,
//     withErrorHandling
//   };
// }
