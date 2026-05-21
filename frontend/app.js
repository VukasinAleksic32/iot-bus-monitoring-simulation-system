const socket = io("http://localhost:5000");

// Centralized bus state configuration
const BUS_STATES = {
  TRAVEL: {
    icon: "➡️",
    label: (bus) => `Travelling to stop #${bus.stop + 1}`,
  },
  STOP: {
    icon: "📍",
    label: (bus) => `Stop #${bus.stop}`,
  },
  REST: {
    icon: "🅿️",
    label: () => "Terminal",
  },
};

// Single bus card
function createBusCard(bus) {
  const card = document.createElement("div");
  const stateClass = bus.state.toLowerCase();
  card.className = `card ${stateClass}`;
  card.id = `bus-${bus.bus_id}`;

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

// Render all buses
function renderAll(buses) {
  buses.sort((a, b) => a.line_number - b.line_number);

  const container = document.getElementById("bus-container");
  const fragment = document.createDocumentFragment();

  buses.forEach((bus) => {
    fragment.appendChild(createBusCard(bus));
  });

  container.replaceChildren(fragment);
}

// Update single bus card in place
function updateBus(bus) {
  const existing = document.getElementById(`bus-${bus.bus_id}`);
  const newCard = createBusCard(bus);

  if (existing) {
    existing.replaceWith(newCard);
  } else {
    document.getElementById("bus-container").appendChild(newCard);
  }
}

// Initial state on connect
socket.on("initial_state", (buses) => renderAll(buses));

// Live updates
socket.on("bus_update", (bus) => updateBus(bus));
