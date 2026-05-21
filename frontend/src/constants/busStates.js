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

export default BUS_STATES;
