async function loadBuses() {
  try {
    const res = await fetch("http://localhost:5000/api/buses");
    const buses = await res.json();

    // Sort by line number
    buses.sort((a, b) => a.line_number - b.line_number);

    const container = document.getElementById("bus-container");
    container.innerHTML = "";

    buses.forEach((bus) => {
      const card = document.createElement("div");
      card.className = "card";
      card.classList.add(bus.state.toLowerCase());

      const occupancyPercent = Math.min(
        100,
        Math.round((bus.inside / bus.capacity) * 100),
      );

      // Footer text
      let stopText = "";
      let stopIcon = "📍";

      if (bus.state === "STOP") {
        stopText = `Stop #${bus.stop}`;
      } else if (bus.state === "TRAVEL") {
        stopIcon = "➡️";
        stopText = `Travelling to stop #${bus.stop + 1}`;
      } else if (bus.state === "REST") {
        stopIcon = "🅿️";
        stopText = "Terminal";
      }

      // Card HTML
      card.innerHTML = `
        <div class="card-header">
          <div class="bus-icon">🚌</div>
          <div class="bus-title">${bus.line_name}</div>
          <div class="status-badge ${bus.state.toLowerCase()}">
            ${bus.state}
          </div>
        </div>

        <div class="occupancy">
          <div class="number">${bus.inside}</div>
          <div class="label">Passengers inside</div>

          <div class="progress">
            <div
              class="progress-fill"
              style="width: ${occupancyPercent}%"
            ></div>
          </div>

          <div class="bus-state">
            Capacity: ${bus.inside} / ${bus.capacity}
          </div>
        </div>

        <div class="footer">
          <div class="stop-label">${stopIcon}</div>
          <div class="stop-number">${stopText}</div>
        </div>
      `;

      container.appendChild(card);
    });
  } catch (err) {
    console.error("Error loading buses:", err);
  }
}

// Initial load
loadBuses();

// Refresh every 1s
setInterval(loadBuses, 1000);
