function OccupancyBar({ inside, capacity }) {
  const occupancyPercent = capacity
    ? Math.min(100, Math.round((inside / capacity) * 100))
    : 0;

  return (
    <div className="occupancy">
      <div className="number">{inside}</div>
      <div className="label">Passengers inside</div>
      <div className="progress">
        <div
          className="progress-fill"
          style={{ width: `${occupancyPercent}%` }}
        />
      </div>
      <div className="bus-state">
        Inside: {inside} / {capacity}
      </div>
    </div>
  );
}

export default OccupancyBar;
