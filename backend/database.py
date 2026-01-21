from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Database setup
engine = create_engine("sqlite:///buses.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


# Model
class Bus(Base):
    __tablename__ = "buses"

    # Identity
    bus_id = Column(String, primary_key=True)

    # Line info
    line_name = Column(String)
    line_number = Column(Integer)

    # State & route
    state = Column(String)
    stop = Column(Integer)

    # Passenger stats (PER ROUTE)
    entered = Column(Integer, default=0)
    exited = Column(Integer, default=0)
    inside = Column(Integer, default=0)

    # Capacity & queues
    capacity = Column(Integer)
    boarding_queue = Column(Integer)
    exit_queue = Column(Integer)

    # Time
    timestamp = Column(Integer)


# Create table
Base.metadata.create_all(engine)


# Save/Update
def save_bus(data):
    session = Session()

    bus = session.get(Bus, data["bus_id"])

    if bus is None:
        bus = Bus(
            bus_id=data["bus_id"],
            line_name=data["line_name"],
            line_number=data["line_number"],
            state=data["state"],
            stop=data["stop"],
            entered=data["entered"],
            exited=data["exited"],
            inside=data["inside"],
            capacity=data["capacity"],
            boarding_queue=data["boarding_queue"],
            exit_queue=data["exit_queue"],
            timestamp=data["timestamp"],
        )
        session.add(bus)
    else:
        bus.line_name = data["line_name"]
        bus.line_number = data["line_number"]
        bus.state = data["state"]
        bus.stop = data["stop"]
        bus.entered = data["entered"]
        bus.exited = data["exited"]
        bus.inside = data["inside"]
        bus.capacity = data["capacity"]
        bus.boarding_queue = data["boarding_queue"]
        bus.exit_queue = data["exit_queue"]
        bus.timestamp = data["timestamp"]

    session.commit()
    session.close()


# Read
def get_all_buses():
    session = Session()
    buses = session.query(Bus).all()

    result = [
        {
            "bus_id": b.bus_id,
            "line_name": b.line_name,
            "line_number": b.line_number,
            "state": b.state,
            "stop": b.stop,
            "entered": b.entered,
            "exited": b.exited,
            "inside": b.inside,
            "capacity": b.capacity,
            "boarding_queue": b.boarding_queue,
            "exit_queue": b.exit_queue,
            "timestamp": b.timestamp,
        }
        for b in buses
    ]

    session.close()
    return result
