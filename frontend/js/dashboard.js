
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

  cacheElements() {
    this.header = document.querySelector(".header");
    this.themeToggleBtn = document.querySelector(".theme-toggle-btn");
    this.hamburgerBtn = document.querySelector(".hamburger-btn");
    this.searchInput = document.querySelector(".search-input");

    this.sidebar = document.querySelector(".sidebar");
    this.sidebarToggleBtn = document.querySelector(".sidebar-toggle-btn");

    this.mainContent = document.querySelector(".main-content");
    this.pageHeader = document.querySelector(".page-header");

    this.uploadArea = document.getElementById("uploadArea");
    this.uploadPreview = document.getElementById("uploadPreview");
    this.uploadPlaceholder = this.uploadArea.querySelector(
      ".upload-placeholder"
    );
    this.previewImage = document.getElementById("previewImage");
    this.fileInput = document.getElementById("fileInput");
    this.btnClear = this.uploadArea.querySelector(".btn-clear");

    this.symbolInput = document.getElementById("symbol");
    this.timeframeSelect = document.getElementById("timeframe");
    this.capitalInput = document.getElementById("capital");
    this.riskPercentInput = document.getElementById("riskPercent");

    this.analyzeBtn = document.getElementById("analyzeBtn");
    this.presetButtons = document.querySelectorAll(".preset-buttons .btn");

    this.analysisResults = document.getElementById("analysisResults");
    this.emptyState = document.querySelector(".empty-state");
    this.loadingIndicator = document.getElementById("loadingIndicator");

    this.signalBadge = document.getElementById("signalBadge");
    this.signalType = document.getElementById("signalType");
    this.signalConfidence = document.getElementById("signalConfidence");
    this.qualityMeter = document.getElementById("qualityMeter");
    this.qualityScore = document.getElementById("qualityScore");

    this.entryPrice = document.getElementById("entryPrice");
    this.tp1Price = document.getElementById("tp1Price");
    this.tp2Price = document.getElementById("tp2Price");
    this.tp3Price = document.getElementById("tp3Price");
    this.slPrice = document.getElementById("slPrice");
    this.tp1Distance = document.getElementById("tp1Distance");
    this.tp2Distance = document.getElementById("tp2Distance");
    this.tp3Distance = document.getElementById("tp3Distance");
    this.slDistance = document.getElementById("slDistance");

    this.positionSize = document.getElementById("positionSize");
    this.riskReward = document.getElementById("riskReward");
    this.maxRisk = document.getElementById("maxRisk");
    this.confluences = document.getElementById("confluences");

    this.indicatorsGrid = document.getElementById("indicatorsGrid");
  }

  setupEventListeners() {
    this.themeToggleBtn.addEventListener("click", () => this.toggleTheme());
    this.hamburgerBtn.addEventListener("click", () => this.toggleMobileMenu());
    this.searchInput.addEventListener(
      "input",
      debounce(() => this.search(), 300)
    );

    this.sidebarToggleBtn.addEventListener("click", () => this.toggleSidebar());

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

    this.symbolInput.addEventListener("change", () => this.validateForm());
    this.capitalInput.addEventListener("change", () => this.validateForm());
    this.riskPercentInput.addEventListener("change", () => this.validateForm());

    this.presetButtons.forEach((btn) => {
      btn.addEventListener("click", (e) =>
        this.applyPreset(e.target.dataset.preset)
      );
    });

    this.analyzeBtn.addEventListener("click", () => this.analyzeChart());

    document.querySelectorAll(".sidebar-link").forEach((link) => {
      link.addEventListener("click", () => this.closeMobileMenu());
    });

    document.addEventListener("click", (e) => {
      if (
        !e.target.closest(".profile-menu") &&
        document.querySelector(".profile-dropdown")
      ) {
      }
    });

    document.addEventListener("keydown", (e) => this.handleKeyboard(e));
  }

  handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    this.uploadArea.classList.add("drag-over");
  }

  handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    this.uploadArea.classList.remove("drag-over");
  }

  handleFileDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    this.uploadArea.classList.remove("drag-over");

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      this.handleFileSelect({ target: { files } });
    }
  }

  handleFileSelect(e) {
    const file = e.target.files[0];

    if (!file) return;

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

  displayPreview(file) {
    const reader = new FileReader();

    reader.onload = (e) => {
      this.previewImage.src = e.target.result;
      this.uploadPlaceholder.style.display = "none";
      this.uploadPreview.style.display = "block";
    };

    reader.readAsDataURL(file);
  }

  clearUpload() {
    this.uploadedFile = null;
    this.fileInput.value = "";
    this.uploadPlaceholder.style.display = "block";
    this.uploadPreview.style.display = "none";
    showToast("Chart removed", "info", 1500);
  }

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

  async analyzeChart() {
    if (!this.validateForm()) {
      showToast("Please fill in all required fields correctly", "error");
      return;
    }

    if (!this.uploadedFile) {
      showToast("Please upload a chart image", "error");
      return;
    }

    const formData = new FormData();
    formData.append("file", this.uploadedFile);
    formData.append("symbol", this.symbolInput.value);
    formData.append("timeframe", this.timeframeSelect.value);
    formData.append("capital", this.capitalInput.value);
    formData.append("risk_percent", this.riskPercentInput.value);

    this.showLoading();

    try {
      const result = await withErrorHandling(api.analyzeChart(formData), {
        onError: () => this.hideLoading(),
      });

      this.currentAnalysis = result;

      this.displayResults(result);
      showToast("Analysis complete!", "success", 2000);
    } catch (error) {
      console.error("Analysis failed:", error);
      this.hideLoading();
    }
  }

  displayResults(analysis) {
    this.hideLoading();

    const signal = analysis.signal || {};
    const signalType = signal.type || "HOLD";

    this.signalBadge.textContent = signalType;
    this.signalBadge.className = `signal-badge ${signalType.toLowerCase()}`;
    this.signalType.textContent = signalType;
    this.signalConfidence.textContent = `${signal.confidence || 0}%`;

    const quality = signal.quality_score || 0;
    this.qualityScore.textContent = Math.round(quality);
    this.qualityMeter.style.width = `${quality}%`;

    const entry = analysis.entry || {};
    const tp = analysis.take_profit || {};
    const sl = analysis.stop_loss || {};

    this.entryPrice.textContent = formatNumber(entry.price || 0, 2);
    this.tp1Price.textContent = formatNumber(tp.tp1?.price || 0, 2);
    this.tp2Price.textContent = formatNumber(tp.tp2?.price || 0, 2);
    this.tp3Price.textContent = formatNumber(tp.tp3?.price || 0, 2);
    this.slPrice.textContent = formatNumber(sl.price || 0, 2);

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

    const risk = analysis.risk_reward || {};
    this.positionSize.textContent = analysis.position_size || "0.00";
    this.riskReward.textContent = `${formatNumber(risk.ratio || 0, 1)}:1`;
    this.maxRisk.textContent = formatCurrency(analysis.max_risk || 0);
    this.confluences.textContent = analysis.confluence_count || 0;

    this.displayIndicators(analysis.indicators || []);

    this.analysisResults.style.display = "block";
    this.emptyState.style.display = "none";

    this.analysisResults.classList.add("animate-slide-up");
    setTimeout(
      () => this.analysisResults.classList.remove("animate-slide-up"),
      500
    );

    scrollToElement(this.analysisResults, 100);
  }

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

  showLoading() {
    this.analyzeBtn.disabled = true;
    this.analyzeBtn.style.pointerEvents = "none";
    this.loadingIndicator.style.display = "flex";
  }

  hideLoading() {
    this.analyzeBtn.disabled = false;
    this.analyzeBtn.style.pointerEvents = "auto";
    this.loadingIndicator.style.display = "none";
  }

  toggleTheme() {
    const current = getThemePreference();
    const next = current === "light" ? "dark" : "light";
    setTheme(next);
    this.updateThemeIcon(next);
  }

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

  restoreTheme() {
    const theme = getThemePreference();
    setTheme(theme);
    this.updateThemeIcon(theme);
  }

  toggleSidebar() {
    const isOpen = this.sidebar.getAttribute("data-open") === "true";
    this.sidebar.setAttribute("data-open", !isOpen);
    this.sidebarToggleBtn.setAttribute("aria-expanded", !isOpen);
  }

  closeSidebar() {
    this.sidebar.setAttribute("data-open", "false");
    this.sidebarToggleBtn.setAttribute("aria-expanded", "false");
  }

  toggleMobileMenu() {
    const isOpen = this.hamburgerBtn.getAttribute("aria-expanded") === "true";
    this.hamburgerBtn.setAttribute("aria-expanded", !isOpen);
    this.sidebar.setAttribute("data-open", !isOpen);
  }

  closeMobileMenu() {
    this.hamburgerBtn.setAttribute("aria-expanded", "false");
    this.sidebar.setAttribute("data-open", "false");
  }

  setupWebSocket() {
  }

  search() {
    const query = this.searchInput.value.toLowerCase();
    if (query) {
      console.log("Searching for:", query);
    }
  }

  handleKeyboard(e) {
    if ((e.metaKey || e.ctrlKey) && e.key === "k") {
      e.preventDefault();
      this.searchInput.focus();
    }

    if (e.key === "Escape") {
      this.closeMobileMenu();
    }

    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      this.analyzeChart();
    }
  }
}


let dashboard;

document.addEventListener("DOMContentLoaded", () => {
  dashboard = new Dashboard();
  console.log("Dashboard initialized");
});

window.addEventListener("beforeunload", () => {
  disconnectWebSocket();
});
