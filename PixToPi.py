import asyncio
from mavsdk import System

async def main():
    drone = System()
    await drone.connect(system_address="udp://:14540")  # Local MAVSDK server default

    print("Waiting for drone...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone discovered!")
            break

    print("\nReading telemetry data...\n")

    async for telemetry in drone.telemetry.position_velocity_ned():
        gps = await drone.telemetry.gps_info()
        attitude = await drone.telemetry.attitude_euler()
        airspeed = await drone.telemetry.ground_speed_ned()
        altitude = telemetry.position

        print(f"GPS: {gps}")
        print(f"Attitude: Roll={attitude.roll_deg:.2f}, Pitch={attitude.pitch_deg:.2f}, Yaw={attitude.yaw_deg:.2f}")
        print(f"Airspeed: {airspeed}")
        print(f"Altitude: North={altitude.north_m:.2f}, East={altitude.east_m:.2f}, Down={altitude.down_m:.2f}")
        print("--------")

        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
