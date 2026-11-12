/* =========================================================
   REUSE — Client Side Script (Charts, Modals, Forms)
========================================================= */

document.addEventListener("DOMContentLoaded", function () {
  // Initialize Chart.js if on Dashboard
  initDashboardCharts();

  // Auto-dismiss alerts after 4 seconds
  const flashMessages = document.querySelectorAll(".flash-msg");
  if (flashMessages.length > 0) {
    setTimeout(() => {
      flashMessages.forEach((msg) => {
        msg.style.opacity = "0";
        msg.style.transition = "opacity 0.4s ease";
        setTimeout(() => msg.remove(), 400);
      });
    }, 4000);
  }
});

// Mobile Sidebar Toggle
function toggleSidebar() {
  const sidebar = document.querySelector(".sidebar");
  if (sidebar) {
    sidebar.classList.toggle("open");
  }
}

// Image Preview on Add Product Form
function handleImagePreview(input) {
  const previewBox = document.getElementById("imagePreviewBox");
  const previewImg = document.getElementById("imagePreviewImg");

  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = function (e) {
      if (previewImg && previewBox) {
        previewImg.src = e.target.result;
        previewBox.style.display = "block";
      }
    };
    reader.readAsDataURL(input.files[0]);
  }
}

function selectPresetImage(url) {
  const hiddenInput = document.getElementById("presetImageInput");
  const previewBox = document.getElementById("imagePreviewBox");
  const previewImg = document.getElementById("imagePreviewImg");

  if (hiddenInput) hiddenInput.value = url;
  if (previewImg && previewBox) {
    previewImg.src = url;
    previewBox.style.display = "block";
  }
}

// Request Item Modal Handler
function openRequestModal(prodId, prodName, prodType) {
  const modal = document.getElementById("requestModal");
  const idInput = document.getElementById("modalProductId");
  const titleSpan = document.getElementById("modalProductTitle");
  const offerField = document.getElementById("modalExchangeOfferGroup");

  if (idInput) idInput.value = prodId;
  if (titleSpan) titleSpan.textContent = prodName;
  if (offerField) {
    offerField.style.display = prodType === "exchange" ? "block" : "none";
  }

  if (modal) {
    modal.style.display = "flex";
  }
}

function closeRequestModal() {
  const modal = document.getElementById("requestModal");
  if (modal) modal.style.display = "none";
}

// Toggle Exchange Preferences on Form
function handleTypeChange(type) {
  const exchangeField = document.getElementById("exchangeLookingForField");
  if (exchangeField) {
    exchangeField.style.display = type === "exchange" ? "block" : "none";
  }
}

// Initialize Charts
function initDashboardCharts() {
  // Category Doughnut Chart
  const catCanvas = document.getElementById("categoryChart");
  if (catCanvas && typeof Chart !== "undefined") {
    new Chart(catCanvas, {
      type: "doughnut",
      data: {
        labels: ["Books", "Clothes", "Electronics", "Furniture", "Household"],
        datasets: [
          {
            data: [412, 310, 264, 198, 145],
            backgroundColor: [
              "#16a34a",
              "#10b981",
              "#0284c7",
              "#f59e0b",
              "#8b5cf6",
            ],
            borderWidth: 2,
            borderColor: "#ffffff",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "right" },
        },
      },
    });
  }

  // Monthly Donations Line Chart
  const lineCanvas = document.getElementById("monthlyDonationsChart");
  if (lineCanvas && typeof Chart !== "undefined") {
    new Chart(lineCanvas, {
      type: "line",
      data: {
        labels: ["Jul", "Aug", "Sep", "Oct", "Nov"],
        datasets: [
          {
            label: "Free Donations",
            data: [62, 85, 110, 142, 175],
            borderColor: "#16a34a",
            backgroundColor: "rgba(22, 163, 74, 0.12)",
            fill: true,
            tension: 0.35,
          },
          {
            label: "Barter Exchanges",
            data: [35, 49, 68, 92, 118],
            borderColor: "#0284c7",
            backgroundColor: "rgba(2, 132, 199, 0.1)",
            fill: true,
            tension: 0.35,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: { y: { beginAtZero: true } },
      },
    });
  }
}

