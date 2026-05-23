import useBuses from "./hooks/useBuses";
import BusGrid from "./components/BusGrid";
import StatsBar from "./components/StatsBar";

function App() {
  const buses = useBuses();

  return (
    <div className="container">
      <h1 className="title">Bus Occupancy Dashboard</h1>
      <StatsBar buses={buses} />
      <BusGrid buses={buses} />
    </div>
  );
}

export default App;
