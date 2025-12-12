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

function formatCurrency(value, currency = "USD") {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
}

function formatPercent(value, decimals = 1) {
  return value.toFixed(decimals) + "%";
}

function formatNumber(value, decimals = 0) {
  return value.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function debounce(func, delay = 300) {
  let timeoutId;
  return function debounced(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
}

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

function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

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

function clearFieldError(field) {
  field.classList.remove("error");

  let errorEl = field.nextElementSibling;
  if (errorEl && errorEl.classList.contains("form-error")) {
    errorEl.classList.remove("show");
  }
}

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

function getThemePreference() {
  const stored = localStorage.getItem("theme-preference");
  if (stored) return stored;

  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function setTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("theme-preference", theme);
}

function toggleTheme() {
  const current = getThemePreference();
  const next = current === "light" ? "dark" : "light";
  setTheme(next);
}

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

function scrollToElement(element, offset = 80) {
  if (typeof element === "string") {
    element = document.querySelector(element);
  }

  if (element) {
    const top = element.getBoundingClientRect().top + window.scrollY - offset;
    window.scrollTo({ top, behavior: "smooth" });
  }
}

function generateId() {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

function delay(ms = 1000) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function getUrlParams() {
  const params = {};
  const searchParams = new URLSearchParams(window.location.search);

  for (const [key, value] of searchParams.entries()) {
    params[key] = value;
  }

  return params;
}

function buildQueryString(params) {
  const searchParams = new URLSearchParams();

  for (const [key, value] of Object.entries(params)) {
    if (value !== null && value !== undefined) {
      searchParams.append(key, value);
    }
  }

  return searchParams.toString();
}

function deepClone(obj) {
  return JSON.parse(JSON.stringify(obj));
}

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

function delegateEvent(parent, selector, eventType, handler) {
  parent.addEventListener(eventType, (event) => {
    const element = event.target.closest(selector);
    if (element) {
      handler.call(element, event);
    }
  });
}

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

function formatNumberWithCommas(value) {
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function calculatePercentageChange(oldValue, newValue) {
  if (oldValue === 0) return 0;
  return ((newValue - oldValue) / oldValue) * 100;
}

function isValidEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

function isValidNumber(value) {
  return !isNaN(parseFloat(value)) && isFinite(value);
}

function debounceAsync(fn, delay) {
  let timeoutId;
  return async function (...args) {
    clearTimeout(timeoutId);
    return new Promise((resolve) => {
      timeoutId = setTimeout(async () => {
        resolve(await fn(...args));
      }, delay);
    });
  };
}

function throttle(fn, limit) {
  let inThrottle;
  return function (...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => {
        inThrottle = false;
      }, limit);
    }
  };
}

function getRandomElement(array) {
  return array[Math.floor(Math.random() * array.length)];
}

function retryAsync(fn, maxAttempts = 3, delayMs = 1000) {
  return (async function attempt(n = 0) {
    try {
      return await fn();
    } catch (error) {
      if (n < maxAttempts) {
        await new Promise((resolve) =>
          setTimeout(resolve, delayMs * Math.pow(2, n))
        );
        return attempt(n + 1);
      } else {
        throw error;
      }
    }
  })();
}
