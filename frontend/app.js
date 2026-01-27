const API_URL = "http://localhost:5000/api/buses";
const REFRESH_INTERVAL_MS = 1000;

// Centralized bus state configuration
const BUS_STATES = {
  TRAVEL:{
    icon: "➡️",
    label: (bus) => `Travelling to stop #${bus.stop + 1}`,
  },
  STOP:{
    icon: "📍",
    label: (bus) => `Stop #${bus.stop}`,
  },
  REST:{
    icon: "🅿️",
    label: () => "Terminal",
  },
};

// Single bus card
function createBusCard(bus){
  const card = document.createElement("div");
  const stateClass = bus.state.toLowerCase();

  card.className = `card ${stateClass}`;

  const occupancyPercent = bus.capacity
  ? Math.min(100, Math.round((bus.inside / bus.capacity) * 100))
  : 0;

  const stateConfig = BUS_STATES[bus.state] ?? {
    icon: "❓",
    label: () => "Unknown state",
  };
  
  // Card HTML
  card.innerHTML = `
    <div class="card-header">
      <div class="bus-icon">🚌</div>
      <div class="bus-title">${bus.line_name}</div>
      <div class="status-badge ${stateClass}">
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
      <div class="stop-label">${stateConfig.icon}</div>
      <div class="stop-number">${stateConfig.label(bus)}</div>
    </div>
  `;

  return card;
}

// Load and render buses
async function loadBuses() {
  try {
    const res = await fetch(API_URL);
    const buses = await res.json();

    // Sort by line number
    buses.sort((a, b) => a.line_number - b.line_number);

    const container = document.getElementById("bus-container");
    const fragment = document.createDocumentFragment();
    
    buses.forEach((bus) => {
      fragment.appendChild(createBusCard(bus));
    });
    
    // DOM update
    container.replaceChildren(fragment);
    
  } catch (err) {
    console.error("Error loading buses:", err);
  }
}

// Initial load
loadBuses();

// Refresh every 1s
setInterval(loadBuses, REFRESH_INTERVAL_MS);