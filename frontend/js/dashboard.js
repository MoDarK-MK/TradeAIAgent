/* ═══════════════════════════════════════════════════════════════════ */
/* DASHBOARD APPLICATION LOGIC                                          */
/* ═══════════════════════════════════════════════════════════════════ */

/**
 * Dashboard Application Class
 */
class Dashboard {
  constructor() {
    this.currentAnalysis = null;
    this.uploadedFile = null;
    this.init();
  }

  init() {
    this.cacheElements();
    this.setupEventListeners();
    this.restoreTheme();
    this.setupWebSocket();
  }

  /**
   * Cache DOM elements
   */
  cacheElements() {
    // Header
    this.header = document.querySelector(".header");
    this.themeToggleBtn = document.querySelector(".theme-toggle-btn");
    this.hamburgerBtn = document.querySelector(".hamburger-btn");
    this.searchInput = document.querySelector(".search-input");

    // Sidebar
    this.sidebar = document.querySelector(".sidebar");
    this.sidebarToggleBtn = document.querySelector(".sidebar-toggle-btn");

    // Main content
    this.mainContent = document.querySelector(".main-content");
    this.pageHeader = document.querySelector(".page-header");

    // Upload area
    this.uploadArea = document.getElementById("uploadArea");
    this.uploadPreview = document.getElementById("uploadPreview");
    this.uploadPlaceholder = this.uploadArea.querySelector(
      ".upload-placeholder"
    );
    this.previewImage = document.getElementById("previewImage");
    this.fileInput = document.getElementById("fileInput");
    this.btnClear = this.uploadArea.querySelector(".btn-clear");

    // Form inputs
    this.symbolInput = document.getElementById("symbol");
    this.timeframeSelect = document.getElementById("timeframe");
    this.capitalInput = document.getElementById("capital");
    this.riskPercentInput = document.getElementById("riskPercent");

    // Buttons
    this.analyzeBtn = document.getElementById("analyzeBtn");
    this.presetButtons = document.querySelectorAll(".preset-buttons .btn");

    // Results section
    this.analysisResults = document.getElementById("analysisResults");
    this.emptyState = document.querySelector(".empty-state");
    this.loadingIndicator = document.getElementById("loadingIndicator");

    // Signal display
    this.signalBadge = document.getElementById("signalBadge");
    this.signalType = document.getElementById("signalType");
    this.signalConfidence = document.getElementById("signalConfidence");
    this.qualityMeter = document.getElementById("qualityMeter");
    this.qualityScore = document.getElementById("qualityScore");

    // Trade ladder
    this.entryPrice = document.getElementById("entryPrice");
    this.tp1Price = document.getElementById("tp1Price");
    this.tp2Price = document.getElementById("tp2Price");
    this.tp3Price = document.getElementById("tp3Price");
    this.slPrice = document.getElementById("slPrice");
    this.tp1Distance = document.getElementById("tp1Distance");
    this.tp2Distance = document.getElementById("tp2Distance");
    this.tp3Distance = document.getElementById("tp3Distance");
    this.slDistance = document.getElementById("slDistance");

    // Stats
    this.positionSize = document.getElementById("positionSize");
    this.riskReward = document.getElementById("riskReward");
    this.maxRisk = document.getElementById("maxRisk");
    this.confluences = document.getElementById("confluences");

    // Indicators
    this.indicatorsGrid = document.getElementById("indicatorsGrid");
  }

  /**
   * Setup event listeners
   */
  setupEventListeners() {
    // Header
    this.themeToggleBtn.addEventListener("click", () => this.toggleTheme());
    this.hamburgerBtn.addEventListener("click", () => this.toggleMobileMenu());
    this.searchInput.addEventListener(
      "input",
      debounce(() => this.search(), 300)
    );

    // Sidebar
    this.sidebarToggleBtn.addEventListener("click", () => this.toggleSidebar());

    // Upload area
    this.uploadArea.addEventListener("click", () => this.fileInput.click());
    this.uploadArea.addEventListener("dragover", (e) => this.handleDragOver(e));
    this.uploadArea.addEventListener("dragleave", (e) =>
      this.handleDragLeave(e)
    );
    this.uploadArea.addEventListener("drop", (e) => this.handleFileDrop(e));
    this.fileInput.addEventListener("change", (e) => this.handleFileSelect(e));
    if (this.btnClear) {
      this.btnClear.addEventListener("click", (e) => {
        e.stopPropagation();
        this.clearUpload();
      });
    }

    // Form inputs
    this.symbolInput.addEventListener("change", () => this.validateForm());
    this.capitalInput.addEventListener("change", () => this.validateForm());
    this.riskPercentInput.addEventListener("change", () => this.validateForm());

    // Preset buttons
    this.presetButtons.forEach((btn) => {
      btn.addEventListener("click", (e) =>
        this.applyPreset(e.target.dataset.preset)
      );
    });

    // Analyze button
    this.analyzeBtn.addEventListener("click", () => this.analyzeChart());

    // Close mobile menu when clicking on navigation
    document.querySelectorAll(".sidebar-link").forEach((link) => {
      link.addEventListener("click", () => this.closeMobileMenu());
    });

    // Close menus on outside click
    document.addEventListener("click", (e) => {
      if (
        !e.target.closest(".profile-menu") &&
        document.querySelector(".profile-dropdown")
      ) {
        // Profile dropdown will auto-close via CSS
      }
    });

    // Keyboard shortcuts
    document.addEventListener("keydown", (e) => this.handleKeyboard(e));
  }

  /**
   * Handle file drag over
   */
  handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    this.uploadArea.classList.add("drag-over");
  }

  /**
   * Handle file drag leave
   */
  handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    this.uploadArea.classList.remove("drag-over");
  }

  /**
   * Handle file drop
   */
  handleFileDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    this.uploadArea.classList.remove("drag-over");

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      this.handleFileSelect({ target: { files } });
    }
  }

  /**
   * Handle file selection
   */
  handleFileSelect(e) {
    const file = e.target.files[0];

    if (!file) return;

    // Validate file
    if (!file.type.startsWith("image/")) {
      showToast("Please select a valid image file", "error");
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      showToast("File size must be less than 10MB", "error");
      return;
    }

    this.uploadedFile = file;
    this.displayPreview(file);
    showToast("Chart uploaded successfully", "success", 2000);
  }

  /**
   * Display file preview
   */
  displayPreview(file) {
    const reader = new FileReader();

    reader.onload = (e) => {
      this.previewImage.src = e.target.result;
      this.uploadPlaceholder.style.display = "none";
      this.uploadPreview.style.display = "block";
    };

    reader.readAsDataURL(file);
  }

  /**
   * Clear uploaded file
   */
  clearUpload() {
    this.uploadedFile = null;
    this.fileInput.value = "";
    this.uploadPlaceholder.style.display = "block";
    this.uploadPreview.style.display = "none";
    showToast("Chart removed", "info", 1500);
  }

  /**
   * Validate form
   */
  validateForm() {
    let isValid = true;

    if (!this.symbolInput.value.trim()) {
      clearFieldError(this.symbolInput);
      isValid = false;
    } else {
      clearFieldError(this.symbolInput);
    }

    if (!validateField(this.capitalInput)) {
      showFieldError(this.capitalInput, "Capital must be a valid number");
      isValid = false;
    } else {
      clearFieldError(this.capitalInput);
    }

    if (!validateField(this.riskPercentInput)) {
      showFieldError(this.riskPercentInput, "Risk must be between 0.5% and 5%");
      isValid = false;
    } else {
      clearFieldError(this.riskPercentInput);
    }

    return isValid;
  }

  /**
   * Apply preset configuration
   */
  applyPreset(preset) {
    const presets = {
      conservative: { capital: 5000, riskPercent: 1 },
      balanced: { capital: 10000, riskPercent: 2 },
      aggressive: { capital: 20000, riskPercent: 3 },
    };

    if (presets[preset]) {
      const config = presets[preset];
      this.capitalInput.value = config.capital;
      this.riskPercentInput.value = config.riskPercent;
      showToast(
        `${preset.charAt(0).toUpperCase() + preset.slice(1)} preset applied`,
        "info",
        1500
      );
    }
  }

  /**
   * Analyze chart
   */
  async analyzeChart() {
    // Validate form
    if (!this.validateForm()) {
      showToast("Please fill in all required fields correctly", "error");
      return;
    }

    if (!this.uploadedFile) {
      showToast("Please upload a chart image", "error");
      return;
    }

    // Prepare form data
    const formData = new FormData();
    formData.append("file", this.uploadedFile);
    formData.append("symbol", this.symbolInput.value);
    formData.append("timeframe", this.timeframeSelect.value);
    formData.append("capital", this.capitalInput.value);
    formData.append("risk_percent", this.riskPercentInput.value);

    // Show loading state
    this.showLoading();

    try {
      // Call API
      const result = await withErrorHandling(api.analyzeChart(formData), {
        onError: () => this.hideLoading(),
      });

      // Store result
      this.currentAnalysis = result;

      // Display results
      this.displayResults(result);
      showToast("Analysis complete!", "success", 2000);
    } catch (error) {
      console.error("Analysis failed:", error);
      this.hideLoading();
    }
  }

  /**
   * Display analysis results
   */
  displayResults(analysis) {
    this.hideLoading();

    // Update signal
    const signal = analysis.signal || {};
    const signalType = signal.type || "HOLD";

    this.signalBadge.textContent = signalType;
    this.signalBadge.className = `signal-badge ${signalType.toLowerCase()}`;
    this.signalType.textContent = signalType;
    this.signalConfidence.textContent = `${signal.confidence || 0}%`;

    const quality = signal.quality_score || 0;
    this.qualityScore.textContent = Math.round(quality);
    this.qualityMeter.style.width = `${quality}%`;

    // Update trade setup
    const entry = analysis.entry || {};
    const tp = analysis.take_profit || {};
    const sl = analysis.stop_loss || {};

    this.entryPrice.textContent = formatNumber(entry.price || 0, 2);
    this.tp1Price.textContent = formatNumber(tp.tp1?.price || 0, 2);
    this.tp2Price.textContent = formatNumber(tp.tp2?.price || 0, 2);
    this.tp3Price.textContent = formatNumber(tp.tp3?.price || 0, 2);
    this.slPrice.textContent = formatNumber(sl.price || 0, 2);

    // Update distances
    const entryVal = entry.price || 0;
    this.tp1Distance.textContent = `+${formatNumber(
      Math.abs(tp.tp1?.price - entryVal || 0),
      0
    )}`;
    this.tp2Distance.textContent = `+${formatNumber(
      Math.abs(tp.tp2?.price - entryVal || 0),
      0
    )}`;
    this.tp3Distance.textContent = `+${formatNumber(
      Math.abs(tp.tp3?.price - entryVal || 0),
      0
    )}`;
    this.slDistance.textContent = `-${formatNumber(
      Math.abs(sl.price - entryVal || 0),
      0
    )}`;

    // Update stats
    const risk = analysis.risk_reward || {};
    this.positionSize.textContent = analysis.position_size || "0.00";
    this.riskReward.textContent = `${formatNumber(risk.ratio || 0, 1)}:1`;
    this.maxRisk.textContent = formatCurrency(analysis.max_risk || 0);
    this.confluences.textContent = analysis.confluence_count || 0;

    // Update indicators
    this.displayIndicators(analysis.indicators || []);

    // Show results, hide empty state
    this.analysisResults.style.display = "block";
    this.emptyState.style.display = "none";

    // Animate results
    this.analysisResults.classList.add("animate-slide-up");
    setTimeout(
      () => this.analysisResults.classList.remove("animate-slide-up"),
      500
    );

    // Scroll to results
    scrollToElement(this.analysisResults, 100);
  }

  /**
   * Display technical indicators
   */
  displayIndicators(indicators) {
    this.indicatorsGrid.innerHTML = "";

    const indicatorItems = [
      { name: "RSI", value: indicators.rsi || "0.00", status: "bullish" },
      { name: "MACD", value: indicators.macd || "0.00", status: "bullish" },
      {
        name: "BB",
        value: indicators.bollinger_bands || "0.00",
        status: "neutral",
      },
      { name: "ATR", value: indicators.atr || "0.00", status: "bullish" },
      { name: "ADX", value: indicators.adx || "0.00", status: "bullish" },
      {
        name: "Stoch",
        value: indicators.stochastic || "0.00",
        status: "bearish",
      },
    ];

    indicatorItems.forEach((item) => {
      const el = createElement("div", { class: "indicator-item" }, "");
      el.innerHTML = `
        <span class="indicator-name">${item.name}</span>
        <div style="display: flex; align-items: center; gap: 8px;">
          <span class="indicator-value">${item.value}</span>
          <span class="indicator-status ${item.status}"></span>
        </div>
      `;
      this.indicatorsGrid.appendChild(el);
    });
  }

  /**
   * Show loading state
   */
  showLoading() {
    this.analyzeBtn.disabled = true;
    this.analyzeBtn.style.pointerEvents = "none";
    this.loadingIndicator.style.display = "flex";
  }

  /**
   * Hide loading state
   */
  hideLoading() {
    this.analyzeBtn.disabled = false;
    this.analyzeBtn.style.pointerEvents = "auto";
    this.loadingIndicator.style.display = "none";
  }

  /**
   * Toggle theme
   */
  toggleTheme() {
    const current = getThemePreference();
    const next = current === "light" ? "dark" : "light";
    setTheme(next);
    this.updateThemeIcon(next);
  }

  /**
   * Update theme icon
   */
  updateThemeIcon(theme) {
    const sunIcon = document.querySelector(".icon-sun");
    const moonIcon = document.querySelector(".icon-moon");

    if (theme === "dark") {
      sunIcon.style.display = "block";
      moonIcon.style.display = "none";
    } else {
      sunIcon.style.display = "none";
      moonIcon.style.display = "block";
    }
  }

  /**
   * Restore theme from storage
   */
  restoreTheme() {
    const theme = getThemePreference();
    setTheme(theme);
    this.updateThemeIcon(theme);
  }

  /**
   * Toggle sidebar
   */
  toggleSidebar() {
    const isOpen = this.sidebar.getAttribute("data-open") === "true";
    this.sidebar.setAttribute("data-open", !isOpen);
    this.sidebarToggleBtn.setAttribute("aria-expanded", !isOpen);
  }

  /**
   * Close sidebar
   */
  closeSidebar() {
    this.sidebar.setAttribute("data-open", "false");
    this.sidebarToggleBtn.setAttribute("aria-expanded", "false");
  }

  /**
   * Toggle mobile menu
   */
  toggleMobileMenu() {
    const isOpen = this.hamburgerBtn.getAttribute("aria-expanded") === "true";
    this.hamburgerBtn.setAttribute("aria-expanded", !isOpen);
    this.sidebar.setAttribute("data-open", !isOpen);
  }

  /**
   * Close mobile menu
   */
  closeMobileMenu() {
    this.hamburgerBtn.setAttribute("aria-expanded", "false");
    this.sidebar.setAttribute("data-open", "false");
  }

  /**
   * Setup WebSocket for real-time signals
   */
  setupWebSocket() {
    // Optional: Initialize WebSocket for real-time updates
    // initializeWebSocket()
    //   .then(() => {
    //     signalWS.on('signal', (data) => {
    //       console.log('Real-time signal received:', data);
    //       // Update UI with real-time data
    //     });
    //   })
    //   .catch(error => {
    //     console.error('Failed to connect WebSocket:', error);
    //   });
  }

  /**
   * Search functionality
   */
  search() {
    const query = this.searchInput.value.toLowerCase();
    if (query) {
      console.log("Searching for:", query);
      // Implement search logic here
    }
  }

  /**
   * Handle keyboard shortcuts
   */
  handleKeyboard(e) {
    // Cmd/Ctrl + K: Focus search
    if ((e.metaKey || e.ctrlKey) && e.key === "k") {
      e.preventDefault();
      this.searchInput.focus();
    }

    // Escape: Close menus
    if (e.key === "Escape") {
      this.closeMobileMenu();
    }

    // Cmd/Ctrl + Enter: Analyze
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      this.analyzeChart();
    }
  }
}

/* ═══════════════════════════════════════════════════════════════════ */
/* INITIALIZE DASHBOARD WHEN DOM READY                                 */
/* ═══════════════════════════════════════════════════════════════════ */

let dashboard;

document.addEventListener("DOMContentLoaded", () => {
  dashboard = new Dashboard();
  console.log("Dashboard initialized");
});

// Handle page unload (cleanup WebSocket)
window.addEventListener("beforeunload", () => {
  disconnectWebSocket();
});
