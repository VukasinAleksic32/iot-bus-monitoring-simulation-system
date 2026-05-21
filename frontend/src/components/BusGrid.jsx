import BusCard from "./BusCard";

function BusGrid({ buses }) {
  // Sort by line number
  const sorted = [...buses.values()].sort(
    (a, b) => a.line_number - b.line_number,
  );

  return (
    <div className="grid">
      {sorted.map((bus) => (
        <BusCard key={String(bus.bus_id)} bus={bus} />
      ))}
    </div>
  );
}

export default BusGrid;
