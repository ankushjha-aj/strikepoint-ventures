# StrikePoint Ventures

> Quantitative Research, Financial Markets Software & Systematic Derivatives Trading Desk

[![Deploy to Hetzner](https://github.com/ankushjha-aj/strikepoint-ventures/actions/workflows/deploy.yml/badge.svg)](https://github.com/ankushjha-aj/strikepoint-ventures/actions/workflows/deploy.yml)
[![Node.js](https://img.shields.io/badge/Node.js-22.x-green.svg)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-ISC-gold.svg)]()

---

## 📈 Brand & Identity

- **Name**: **STRIKEPOINT VENTURES**
- **Logo**: Pure mathematical sine wave curve with emerald green positive crest (`#10B981`) and crimson red negative trough (`#EF4444`) without grid lines.
- **Palette**: Deep Navy (`#0B1F3A`), Antique Brass / Gold (`#C29B40`), Emerald Green (`#10B981`), Crimson Red (`#EF4444`).
- **Typography**: Editorial Serif (`Fraunces`) paired with Modern Sans (`Hanken Grotesk`) and Quantitative Monospace (`JetBrains Mono`).

---

## 🧭 Page Architecture & Routes

| Route | Page Name | Description |
| :--- | :--- | :--- |
| `/` | **Home** | Flagship landing page with hero, products, proof points, and insights |
| `/about` | **About Us** | The firm, philosophy, quantitative discipline, and mission |
| `/team` | **Our Team** | Quantitative researchers, mathematical engineers, and mentors |
| `/services` | **Services Hub** | Comprehensive catalog of all capabilities |
| `/services/statistical-edge-finding` | **Quant Edge Research** | Statistical backtesting & strategy validation under NDA |
| `/services/software-solutions` | **Software Solutions** | Financial market execution engines & low-latency terminals |
| `/services/strikepoint-rtx` | **StrikePoint RTX** | Real-time analytics terminal (volatility surfaces & GEX) |
| `/services/strikepoint-vector` | **StrikePoint Vector** | High-performance broker execution engine |
| `/services/proprietary-trading` | **Proprietary Trading** | Automated proprietary desk execution on firm capital |
| `/services/strikepoint-foundation` | **Foundation** | Quant education & financial ecosystem community |
| `/blog` | **Insights & Research** | Quantitative research whitepapers & microstructure analysis |
| `/contact` | **Contact & Onboarding** | Direct desk communication & inquiry form |
| `/api/health` | **API Health Check** | System uptime and status endpoint |

---

## 🛠️ Local Development

### 1. Prerequisites
- Node.js (v18+)
- npm (v9+)

### 2. Install Dependencies
```bash
npm install
```

### 3. Run Development Server
```bash
npm run dev
```
Visit: [http://localhost:9000](http://localhost:9000)

### 4. Build TypeScript
```bash
npm run build
```

### 5. Production Start
```bash
npm start
```

---

## 🚀 Hetzner Production Deployment

- **Server IP**: `65.109.15.215`
- **Application Port**: `9000`
- **Process Manager**: `PM2` (service: `strikepoint-ventures`)
- **App Location**: `/var/www/strikepoint-ventures`

### Deployment Command:
```bash
PORT=9000 pm2 restart strikepoint-ventures || PORT=9000 pm2 start dist/server.js --name strikepoint-ventures
pm2 save
```

---

## 🔄 CI/CD Automation (GitHub Actions)

A GitHub Actions workflow is pre-configured in `.github/workflows/deploy.yml` to automatically build and deploy whenever changes are pushed to the `main` branch.

### Required GitHub Secrets:
1. `HETZNER_HOST`: `65.109.15.215`
2. `HETZNER_USER`: `root`
3. `HETZNER_SSH_KEY`: Content of `~/.ssh/ankush-hetzner`
