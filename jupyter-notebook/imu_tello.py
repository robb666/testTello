from djitellopy import Tello
import time

tello = Tello()
tello.connect()

print(f"Bateria: {tello.get_battery()}%")
print("Rozpoczynam odczyt danych z IMU. Naciśnij Ctrl+C, aby przerwać.\n")

try:
    while True:
        # Odczyt danych o nachyleniu (Żyroskop)
        pitch = tello.get_pitch()
        roll = tello.get_roll()
        yaw = tello.get_yaw()

        # Odczyt danych o przyspieszeniu (Akcelerometr)
        agx = tello.get_acceleration_x()
        agy = tello.get_acceleration_y()
        agz = tello.get_acceleration_z()

        # Czyszczenie linii i nadpisywanie tekstu w konsoli (dla czytelności)
        print(f"\r[Żyroskop] Pitch: {pitch:4} | Roll: {roll:4} | Yaw: {yaw:4} || "
              f"[Akcelerometr] X: {agx:6.1f} | Y: {agy:6.1f} | Z: {agz:6.1f}",
              end="", flush=True)

        time.sleep(0.1)  # Tello wysyła dane z częstotliwością ~10Hz (co 100ms)

except KeyboardInterrupt:
    print("\nZakończono odczyt.")