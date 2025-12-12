# MOD Trade - Frontend Dashboard

Professional enterprise-grade UI/UX for the AI Trading Agent platform. Built with HTML5, CSS3, and Vanilla JavaScript.

## 🎨 Design System

### Color Palette

- **Primary**: `#00D9FF` (Cyan - Trust, Technology)
- **Success**: `#00FF88` (Green - Profit, BUY)
- **Danger**: `#FF3333` (Red - Risk, SELL)
- **Warning**: `#FFAA00` (Orange - Caution)
- **Dark BG**: `#0A0E27` (Professional nighttime)
- **Card BG**: `#1A1F3A` (Elevated surfaces)

### Typography

- **Display (H1)**: 32px, Weight 700
- **Heading (H2)**: 24px, Weight 600
- **Body**: 14px, Weight 400
- **Monospace**: JetBrains Mono (for prices/values)

### Spacing (8px base)

- `xs`: 4px
- `sm`: 8px
- `md`: 16px
- `lg`: 24px
- `xl`: 32px
- `2xl`: 48px

### Border Radius

- `sm`: 4px (tight inputs)
- `md`: 8px (cards, buttons)
- `lg`: 12px (major sections)
- `full`: 9999px (badges)

## 📁 Project Structure

```
frontend/
├── index.html              # Main dashboard page
├── assets/
│   ├── images/            # Icons, logos, graphics
│   └── fonts/             # Custom fonts
├── css/
│   ├── design-system.css  # Color palette, typography, components
│   ├── dashboard.css      # Page-specific styles
│   └── responsive.css     # Mobile, tablet, desktop breakpoints
├── js/
│   ├── utils.js           # Helper functions (format, debounce, etc.)
│   ├── api.js             # API client, WebSocket manager
│   └── dashboard.js       # Main application logic
├── components/            # Reusable component templates
├── pages/                 # Additional pages (history, settings, etc.)
└── README.md             # This file
```

## 🚀 Features

### Dashboard

- Chart image upload (drag-and-drop support)
- Trading parameters configuration
- Quick presets (Conservative, Balanced, Aggressive)
- Real-time analysis results display
- Trade setup visualization (Entry → TP1 → TP2 → TP3 → SL)

### UI Components

- Professional buttons (Primary, Secondary, Success, Danger)
- Glassmorphism cards with hover effects
- Form inputs with validation feedback
- Status badges (BUY, SELL, HOLD)
- Quality meter with animated fill
- Responsive grid layouts

### Interactivity

- Smooth animations and transitions
- Keyboard shortcuts (Cmd+K search, Cmd+Enter analyze, Esc close)
- Mobile-optimized touch targets (44px minimum)
- Drag-and-drop file upload
- Real-time form validation
- Toast notifications

### Accessibility

- WCAG 2.1 AA compliance
- Semantic HTML5
- ARIA labels and landmarks
- Keyboard navigation support
- Focus indicators
- Screen reader friendly
- High contrast mode support
- Reduced motion support

## 📱 Responsive Design

### Breakpoints

- **Mobile**: < 640px (single column stack)
- **Tablet**: 640px - 1024px (2 columns)
- **Desktop**: > 1024px (3 columns optimal)
- **Ultra-wide**: > 1600px (sidebar + main + insights)

### Mobile Optimizations

- Full-width buttons
- Hamburger navigation menu
- Touch-friendly spacing (min 44px)
- Optimized font sizes
- Simplified layouts
- Collapsible sections

## 🎯 Key Sections

### 1. Header

- Logo with brand name
- Main navigation links
- Search functionality
- Notification bell
- Theme toggle (Light/Dark)
- User profile with dropdown
- Mobile hamburger menu

### 2. Sidebar

- Collapsible navigation
- Dashboard, Analysis, Portfolio, History links
- Settings, Documentation, Help links
- Quick stats display (Win Rate, Total Trades)
- Toggle button to collapse

### 3. Main Content

- **Upload Area**: Drag-and-drop chart upload
- **Parameters**: Symbol, timeframe, capital, risk settings
- **Results**: Signal display, trade setup ladder, metrics
- **Indicators**: Technical indicator breakdown

### 4. Results Panel

- Signal badge (BUY/SELL/HOLD)
- Confidence meter with quality score
- Trade ladder showing Entry, TP1-3, SL
- Risk/Reward statistics
- Technical indicators grid
- Action buttons (Execute, Report, Copy)

## 🔧 API Integration

### Endpoints

The frontend connects to these FastAPI backend endpoints:

```javascript
// POST /api/analyze - Analyze chart
POST http://localhost:8000/api/analyze

// GET /api/summary - Get summary
GET http://localhost:8000/api/summary

// GET /api/indicators/list - List indicators
GET http://localhost:8000/api/indicators/list

// WS /ws/signals - Real-time signals (WebSocket)
WS ws://localhost:8000/ws/signals
```

### Error Handling

- User-friendly error messages
- Toast notifications for feedback
- Field validation with error display
- API error handling with retry logic
- Network error recovery

## ⚙️ Configuration

### API Base URL

Edit `API_CONFIG` in `js/api.js`:

```javascript
const API_CONFIG = {
  baseUrl: "http://localhost:8000/api", // Change this
  timeout: 30000,
  headers: { "Content-Type": "application/json" },
};
```

### Theme

- Automatic detection of system preference
- Manual toggle available
- Stored in `localStorage`

```javascript
// Get current theme
const theme = getThemePreference(); // 'light' or 'dark'

// Set theme
setTheme("dark");

// Toggle theme
toggleTheme();
```

## 🎨 Customization

### Color Scheme

Update CSS variables in `css/design-system.css`:

```css
:root {
  --color-primary: #00d9ff;
  --color-success: #00ff88;
  --color-danger: #ff3333;
  /* ... more colors ... */
}
```

### Typography

Modify font sizes and weights:

```css
:root {
  --fs-h1: 32px;
  --fs-body: 14px;
  --fw-bold: 700;
  /* ... more typography ... */
}
```

### Spacing

Adjust spacing system:

```css
:root {
  --sp-md: 16px;
  --sp-lg: 24px;
  /* ... more spacing ... */
}
```

## 🧪 Development

### Local Development

```bash
# 1. Start the FastAPI backend
cd ../app
python -m uvicorn main:app --reload

# 2. Serve the frontend
cd frontend
# Option A: Use Python
python -m http.server 3000

# Option B: Use Node.js http-server
npx http-server -p 3000

# 3. Open in browser
open http://localhost:3000
```

### Browser DevTools

- Use browser DevTools for debugging
- Check Console for errors
- Use Network tab to monitor API calls
- Use Device toolbar for responsive testing

### Performance

- Lazy load images
- Minify CSS/JS for production
- Use CSS variables for fast theme switching
- Hardware acceleration for animations (`will-change`)
- Debounce/throttle event handlers

## 📦 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## ♿ Accessibility Testing

```bash
# Run accessibility audit with browser DevTools
1. Open DevTools
2. Go to Lighthouse tab
3. Run Accessibility audit
```

### WCAG 2.1 Compliance

- ✅ Text has sufficient contrast (4.5:1)
- ✅ All interactive elements are keyboard accessible
- ✅ Forms are labeled and associated with inputs
- ✅ Images have alt text
- ✅ Headings follow proper hierarchy
- ✅ Focus indicators are visible
- ✅ Motion can be disabled

## 🚀 Production Deployment

### Build for Production

```bash
# Minify CSS
css-minify css/*.css -o css/style.min.css

# Minify JS
terser js/*.js -o js/script.min.js

# Update index.html to use minified files
<link rel="stylesheet" href="css/style.min.css">
<script src="js/script.min.js"></script>
```

### Deploy to Web Server

```bash
# Option 1: Serve static files with Nginx
# Copy frontend files to /var/www/html

# Option 2: Deploy with Docker
docker build -f Dockerfile.frontend -t MOD-trade-frontend .
docker run -p 80:80 MOD-trade-frontend

# Option 3: Deploy with Vercel/Netlify
# Connect GitHub repo and deploy automatically
```

### Environment Configuration

```bash
# Create .env file for production
API_BASE_URL=https://api.example.com/api
WEBSOCKET_URL=wss://api.example.com/ws
```

## 📝 Best Practices

### Code Organization

- Keep CSS modular and DRY
- Use semantic HTML
- Follow naming conventions (BEM for CSS)
- Comment complex logic
- Keep functions small and focused

### Performance

- Minimize DOM manipulation
- Use event delegation
- Cache DOM references
- Debounce/throttle handlers
- Load fonts asynchronously

### Security

- Sanitize user input
- Use HTTPS in production
- Implement CORS properly
- Validate on both client and server
- No sensitive data in localStorage

## 🐛 Troubleshooting

### API Connection Issues

```javascript
// Check if API is reachable
fetch("http://localhost:8000/health")
  .then((r) => console.log("API status:", r.status))
  .catch((e) => console.error("API error:", e));
```

### Theme Not Persisting

```javascript
// Clear localStorage and refresh
localStorage.clear();
location.reload();
```

### Form Validation Not Working

```javascript
// Check browser console for errors
// Verify input attributes (type, min, max, required)
```

### WebSocket Connection Failed

```javascript
// Ensure backend is running with WebSocket support
// Check browser console for connection errors
// Verify WebSocket URL in api.js
```

## 📚 Additional Resources

- [CSS Variables Documentation](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)
- [Fetch API Guide](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 📄 License

This frontend is part of the MOD Trade AI Trading Agent project. Licensed under MIT.

## 🤝 Contributing

Contributions are welcome! Please ensure:

- Code follows project conventions
- All changes are tested
- Accessibility is maintained
- Documentation is updated

---

Built with ❤️ for professional traders | © 2025 MOD Trade
