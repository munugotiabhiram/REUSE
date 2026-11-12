# REUSE — Smart Reuse & Recycling Management System (IMS)

## 1. Project Overview
**REUSE** is a modern, responsive, and eco-friendly web-based Information Management System (IMS). The platform connects individuals who have unused products with people who need them. Users can donate, exchange, request, and reuse products such as clothes, books, electronics, furniture, household items, and sporting goods to eliminate landfill waste and promote a circular economy.

---

## 2. Key Features Implemented

### 2.1 Design & Theming
- **Eco-Friendly Visual Identity:** Clean palette based on vibrant Emerald & Forest Green (`#16a34a`, `#10b981`, `#14532d`), soft light greys (`#f8fafc`, `#f1f5f9`), crisp white surfaces, and dark contrast typography.
- **Micro-Interactions & Feedback:** Rounded cards (`border-radius: 18px`), FontAwesome 6 icons, smooth CSS transitions, toast notifications, and celebratory **confetti animations** upon successful donation or reuse completion.
- **Dark Mode Support:** Quick toggle between light and dark themes.
- **Fully Responsive:** Adapts to desktop, tablet, and mobile with an off-canvas drawer navigation.

### 2.2 Navigation (Single Page Application)
- **Dashboard:** Platform overview, hero banner, core stat cards, community challenge, and recent activity timeline.
- **Browse Products:** Filterable product marketplace with live keyword search, category pills, condition filters, and sorting.
- **Add New Product:** Listing form with drag-and-drop image upload, live preview, donation vs. exchange options, and estimated item weight for eco-impact scoring.
- **Donate Items:** Filtered view showcasing 100% free community donations.
- **Exchange Items:** Circular barter marketplace to swap unused goods.
- **My Requests:** Two-way tracking for **Sent Requests** (items you requested) and **Incoming Requests** (requests on your items) with Accept, Decline, and Hand Over actions.
- **My Products:** Inventory management for listed goods (Mark as Reused, Delete, Edit).
- **Analytics Dashboard:** Four interactive Chart.js charts and environmental impact tables.
- **Notifications:** Real-time alert center with unread badges.
- **Profile & Impact:** Personal eco-scorecard displaying total donations, exchanges, weight diverted, and sustainability badges.
- **Admin Portal:** Moderation console to approve/reject listings, manage registered users, and audit active transactions.
- **Authentication:** Login and account registration modal with quick demo role switchers.

### 2.3 Dashboard Statistics
- **Total Products Available:** Real-time count of active listings.
- **Total Products Reused:** Count of completed items saved from disposal.
- **Total Donations:** Cumulative community donations count.
- **Pending Requests:** Outstanding requests requiring response.
- **Total Registered Users:** Platform community members.
- **Environmental Impact Metrics:**
  - *Landfill Waste Diverted (kg):* Cumulative weight saved.
  - *Estimated CO₂ Emissions Avoided (kg/tons):* Lifecycle carbon reduction equivalent.
  - *Active Barter Exchanges:* Ongoing barter swaps.

### 2.4 Interactive Charts (Chart.js)
1. **Products Reused by Category:** Doughnut chart illustrating distribution across Books, Clothes, Electronics, Furniture, and Household.
2. **Monthly Donations & Exchanges:** Multi-line/area chart highlighting monthly growth in community participation.
3. **Total Waste Reduced (kg):** Monthly bar chart tracking kilograms diverted.
4. **Donation vs. Exchange Statistics:** Proportional split between free giving and barter trades.

---

## 3. File Structure

```
eventhub/
├── reuse_dashboard.html      # Complete frontend SPA (HTML, CSS, JS, Charts, Modals)
├── server_reuse.js           # Lightweight Node.js server with REST APIs & static hosting
├── reuse_data_store.json     # JSON persistence for products, requests, users, and activities
├── start_reuse.bat           # One-click Windows batch launcher
├── start_reuse.ps1           # PowerShell launcher
└── REUSE_DOCUMENTATION.md    # Documentation and feature guide
```

---

## 4. How to Run

### Method 1: Double-Click Standalone (No Installation Needed)
Simply double-click or open `reuse_dashboard.html` in any web browser (Chrome, Edge, Firefox). The application runs completely in client-side mode with persistent state saved in `localStorage`.

### Method 2: Launch via Node.js Server
1. Double-click `start_reuse.bat` or run:
   ```powershell
   node server_reuse.js
   ```
2. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

---

## 5. Demo Accounts
- **Regular User:** `sarah.green@example.org` (Role: Eco Champion)
- **Admin / Moderator:** `admin@reuse-ims.org` (Role: System Admin)

