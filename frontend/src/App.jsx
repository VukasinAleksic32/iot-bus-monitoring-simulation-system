import useBuses from "./hooks/useBuses";
import BusGrid from "./components/BusGrid";

function App() {
  const buses = useBuses();

  return (
    <>
      <h1 className="title">Bus Occupancy Dashboard</h1>
      <BusGrid buses={buses} />
    </>
  );
}

export default App;
