from djitellopy import Tello
import time

tello = Tello()
tello.connect()

print(f"Bateria: {tello.get_battery()}%")
print("Odczyt z czujnika odległości (ToF). Naciśnij Ctrl+C, aby przerwać.\n")

try:
    while True:
        # Odczyt odległości od podłoża (w centymetrach)
        tof_distance = tello.get_distance_tof()

        # Odczyt osi Z (żebyś widział, jak grawitacja ma się do wysokości)
        agz = tello.get_acceleration_z()

        print(f"\rWysokość nad podłożem (ToF): {tof_distance} cm | Przyspieszenie Z: {agz:6.1f} ",
              end="", flush=True)

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nZakończono odczyt.")