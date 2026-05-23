import BUS_STATES from "../constants/busStates";

function StatsBar({ buses }) {
  const total = buses.size;

  const counts = Object.fromEntries(
    Object.keys(BUS_STATES).map((state) => [
      state,
      [...buses.values()].filter((b) => b.state === state).length,
    ]),
  );

  return (
    <div className="stats-bar">
      <div className="stat">
        <span className="stat-value">{total}</span>
        <span className="stat-label">Total</span>
      </div>
      {Object.entries(BUS_STATES).map(([state, config]) => (
        <div className="stat" key={state}>
          <span className={`stat-value ${state.toLowerCase()}`}>
            {counts[state]}
          </span>
          <span className="stat-label">
            {config.icon} {state}
          </span>
        </div>
      ))}
    </div>
  );
}

export default StatsBar;
