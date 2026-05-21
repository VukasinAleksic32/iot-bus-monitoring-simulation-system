import BUS_STATES from "../constants/busStates";
import OccupancyBar from "./OccupancyBar";

function BusCard({ bus }) {
  const stateClass = bus.state.toLowerCase();

  const stateConfig = BUS_STATES[bus.state] ?? {
    icon: "❓",
    label: () => "Unknown state",
  };

  return (
    <div className={`card ${stateClass}`}>
      <div className="card-header">
        <div className="bus-icon">🚌</div>
        <div className="bus-title">{bus.line_name}</div>
        <div className={`status-badge ${stateClass}`}>{bus.state}</div>
      </div>
      <OccupancyBar inside={bus.inside} capacity={bus.capacity} />
      <div className="footer">
        <div className="stop-label">{stateConfig.icon}</div>
        <div className="stop-number">{stateConfig.label(bus)}</div>
      </div>
    </div>
  );
}

export default BusCard;
