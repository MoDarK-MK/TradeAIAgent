/* ═══════════════════════════════════════════════════════════════════ */
/* UTILITY FUNCTIONS                                                    */
/* ═══════════════════════════════════════════════════════════════════ */

/**
 * Show a toast notification
 * @param {string} message - Notification message
 * @param {string} type - 'success', 'error', 'warning', or 'info'
 * @param {number} duration - Duration in ms (0 = no auto-dismiss)
 */
function showToast(message, type = "info", duration = 4000) {
  const container = document.getElementById("toastContainer");

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;

  const icons = {
    success: "✅",
    error: "❌",
    warning: "⚠️",
    info: "ℹ️",
  };

  const titles = {
    success: "Success",
    error: "Error",
    warning: "Warning",
    info: "Information",
  };

  toast.innerHTML = `
    <span class="toast-icon">${icons[type]}</span>
    <div class="toast-content">
      <div class="toast-title">${titles[type]}</div>
      <div class="toast-message">${message}</div>
    </div>
    <button class="toast-close" aria-label="Close notification">×</button>
  `;

  container.appendChild(toast);

  const closeBtn = toast.querySelector(".toast-close");
  closeBtn.addEventListener("click", () => {
    toast.style.animation = "slideIn 0.3s ease-out reverse";
    setTimeout(() => toast.remove(), 300);
  });

  if (duration > 0) {
    setTimeout(() => {
      if (toast.parentElement) {
        toast.style.animation = "slideIn 0.3s ease-out reverse";
        setTimeout(() => toast.remove(), 300);
      }
    }, duration);
  }
}

/**
 * Format currency values
 * @param {number} value - Value to format
 * @param {string} currency - Currency code (default: USD)
 * @returns {string} Formatted currency string
 */
function formatCurrency(value, currency = "USD") {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
}

/**
 * Format percentage
 * @param {number} value - Value to format
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted percentage
 */
function formatPercent(value, decimals = 1) {
  return value.toFixed(decimals) + "%";
}

/**
 * Format large numbers with commas
 * @param {number} value - Value to format
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted number
 */
function formatNumber(value, decimals = 0) {
  return value.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Debounce function - delays execution until after calls stop
 * @param {function} func - Function to debounce
 * @param {number} delay - Delay in ms
 * @returns {function} Debounced function
 */
function debounce(func, delay = 300) {
  let timeoutId;
  return function debounced(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
}

/**
 * Throttle function - limits execution frequency
 * @param {function} func - Function to throttle
 * @param {number} limit - Time limit in ms
 * @returns {function} Throttled function
 */
function throttle(func, limit = 300) {
  let lastFunc;
  let lastRan;
  return function (...args) {
    if (!lastRan) {
      func(...args);
      lastRan = Date.now();
    } else {
      clearTimeout(lastFunc);
      lastFunc = setTimeout(() => {
        if (Date.now() - lastRan >= limit) {
          func(...args);
          lastRan = Date.now();
        }
      }, limit - (Date.now() - lastRan));
    }
  };
}

/**
 * Validate email address
 * @param {string} email - Email to validate
 * @returns {boolean} Valid email
 */
function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

/**
 * Validate form field
 * @param {HTMLElement} field - Form field element
 * @returns {boolean} Field is valid
 */
function validateField(field) {
  const value = field.value.trim();
  const type = field.getAttribute("type");

  if (!value) {
    return false;
  }

  if (type === "email") {
    return validateEmail(value);
  }

  if (type === "number") {
    const num = parseFloat(value);
    const min = field.getAttribute("min");
    const max = field.getAttribute("max");

    if (min && num < parseFloat(min)) return false;
    if (max && num > parseFloat(max)) return false;
    return !isNaN(num);
  }

  return true;
}

/**
 * Show field error
 * @param {HTMLElement} field - Form field element
 * @param {string} message - Error message
 */
function showFieldError(field, message) {
  field.classList.add("error");

  let errorEl = field.nextElementSibling;
  if (!errorEl || !errorEl.classList.contains("form-error")) {
    errorEl = document.createElement("div");
    errorEl.className = "form-error";
    field.parentNode.insertBefore(errorEl, field.nextSibling);
  }

  errorEl.textContent = message;
  errorEl.classList.add("show");
}

/**
 * Clear field error
 * @param {HTMLElement} field - Form field element
 */
function clearFieldError(field) {
  field.classList.remove("error");

  let errorEl = field.nextElementSibling;
  if (errorEl && errorEl.classList.contains("form-error")) {
    errorEl.classList.remove("show");
  }
}

/**
 * Copy text to clipboard
 * @param {string} text - Text to copy
 * @returns {Promise<boolean>} Copy success
 */
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    showToast("Copied to clipboard!", "success", 2000);
    return true;
  } catch (err) {
    showToast("Failed to copy", "error", 2000);
    return false;
  }
}

/**
 * Animate number counter
 * @param {HTMLElement} element - Element to animate
 * @param {number} target - Target number
 * @param {number} duration - Duration in ms
 */
function animateCounter(element, target, duration = 1000) {
  const start = parseFloat(element.textContent) || 0;
  const increment = (target - start) / (duration / 16);
  let current = start;

  const interval = setInterval(() => {
    current += increment;

    if (
      (increment > 0 && current >= target) ||
      (increment < 0 && current <= target)
    ) {
      current = target;
      clearInterval(interval);
    }

    element.textContent = formatNumber(current, 1);
  }, 16);
}

/**
 * Get theme preference
 * @returns {string} 'light' or 'dark'
 */
function getThemePreference() {
  const stored = localStorage.getItem("theme-preference");
  if (stored) return stored;

  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

/**
 * Set theme
 * @param {string} theme - 'light' or 'dark'
 */
function setTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("theme-preference", theme);
}

/**
 * Toggle theme
 */
function toggleTheme() {
  const current = getThemePreference();
  const next = current === "light" ? "dark" : "light";
  setTheme(next);
}

/**
 * Check if element is in viewport
 * @param {HTMLElement} element - Element to check
 * @returns {boolean} Is visible in viewport
 */
function isInViewport(element) {
  const rect = element.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <=
      (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

/**
 * Scroll to element smoothly
 * @param {HTMLElement|string} element - Element or selector
 * @param {number} offset - Offset from top
 */
function scrollToElement(element, offset = 80) {
  if (typeof element === "string") {
    element = document.querySelector(element);
  }

  if (element) {
    const top = element.getBoundingClientRect().top + window.scrollY - offset;
    window.scrollTo({ top, behavior: "smooth" });
  }
}

/**
 * Generate unique ID
 * @returns {string} Unique ID
 */
function generateId() {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Delay execution
 * @param {number} ms - Milliseconds to delay
 * @returns {Promise} Resolves after delay
 */
function delay(ms = 1000) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Parse URL parameters
 * @returns {Object} URL parameters
 */
function getUrlParams() {
  const params = {};
  const searchParams = new URLSearchParams(window.location.search);

  for (const [key, value] of searchParams.entries()) {
    params[key] = value;
  }

  return params;
}

/**
 * Build query string from object
 * @param {Object} params - Parameters object
 * @returns {string} Query string
 */
function buildQueryString(params) {
  const searchParams = new URLSearchParams();

  for (const [key, value] of Object.entries(params)) {
    if (value !== null && value !== undefined) {
      searchParams.append(key, value);
    }
  }

  return searchParams.toString();
}

/**
 * Deep clone object
 * @param {Object} obj - Object to clone
 * @returns {Object} Cloned object
 */
function deepClone(obj) {
  return JSON.parse(JSON.stringify(obj));
}

/**
 * Merge objects
 * @param {Object} target - Target object
 * @param {Object} source - Source object
 * @returns {Object} Merged object
 */
function mergeObjects(target, source) {
  const result = { ...target };

  for (const key in source) {
    if (source.hasOwnProperty(key)) {
      if (typeof source[key] === "object" && source[key] !== null) {
        result[key] = mergeObjects(result[key] || {}, source[key]);
      } else {
        result[key] = source[key];
      }
    }
  }

  return result;
}

/**
 * Event delegation helper
 * @param {HTMLElement} parent - Parent element
 * @param {string} selector - Child selector
 * @param {string} eventType - Event type
 * @param {function} handler - Event handler
 */
function delegateEvent(parent, selector, eventType, handler) {
  parent.addEventListener(eventType, (event) => {
    const element = event.target.closest(selector);
    if (element) {
      handler.call(element, event);
    }
  });
}

/**
 * Create element with attributes
 * @param {string} tag - HTML tag
 * @param {Object} attrs - Attributes object
 * @param {string|HTMLElement} content - Element content
 * @returns {HTMLElement} Created element
 */
function createElement(tag, attrs = {}, content = "") {
  const element = document.createElement(tag);

  for (const [key, value] of Object.entries(attrs)) {
    if (key === "class") {
      element.classList.add(...value.split(" "));
    } else if (key.startsWith("data-")) {
      element.setAttribute(key, value);
    } else if (key === "innerHTML") {
      element.innerHTML = value;
    } else {
      element.setAttribute(key, value);
    }
  }

  if (typeof content === "string") {
    element.textContent = content;
  } else if (content instanceof HTMLElement) {
    element.appendChild(content);
  }

  return element;
}

/* ═══════════════════════════════════════════════════════════════════ */
/* EXPORT FOR MODULE USAGE (if needed)                                 */
/* ═══════════════════════════════════════════════════════════════════ */

// if (typeof module !== 'undefined' && module.exports) {
//   module.exports = {
//     showToast,
//     formatCurrency,
//     formatPercent,
//     formatNumber,
//     debounce,
//     throttle,
//     validateEmail,
//     // ... other exports
//   };
// }
