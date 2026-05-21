import { useState, useEffect } from "react";
import { io } from "socket.io-client";
import { SOCKET_URL } from "../constants/config";

function useBuses() {
  const [buses, setBuses] = useState(new Map());

  useEffect(() => {
    const socket = io(SOCKET_URL);

    // Initial state on connect
    socket.on("initial_state", (busArray) => {
      setBuses(new Map(busArray.map((b) => [String(b.bus_id), b])));
    });

    // Live updates
    socket.on("bus_update", (bus) => {
      setBuses((prev) => new Map(prev).set(String(bus.bus_id), bus));
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return buses;
}

export default useBuses;
