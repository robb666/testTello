import cv2
import time
import threading
from flask import Flask, Response
from djitellopy import Tello


app = Flask(__name__)
tello = Tello()


@app.route('/')
def index():
    return "Wideo dostępne pod adresem: <a href='/stream'>/stream</a>"


@app.route('/stream')
def stream():
    def generate():
        while True:
            # Pobieranie najnowszej klatki prosto z drona
            frame = tello.get_frame_read().frame
            # Kodowanie do JPEG
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue

            # Tworzenie strumienia MJPEG dla przeglądarki
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

            time.sleep(1 / 30)  # Ograniczenie do ~30 FPS

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


def run_flask():
    # Uruchomienie serwera na porcie 9999 (wyłączamy logi dla czytelności konsoli)
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host='127.0.0.1', port=9999, debug=False, use_reloader=False)


if __name__ == '__main__':
    # 1. Połączenie z dronem i włączenie wideo
    print("Łączenie z dronem...")
    tello.connect()
    print(f"Bateria: {tello.get_battery()}%")
    if tello.get_battery() < 15:
        print("[ ERROR ] Bateria jest zbyt słaba na lot! Naładuj drona.")
        tello.streamoff()
        exit()
    tello.streamon()

    # 2. Uruchomienie Flaska w osobnym wątku
    threading.Thread(target=run_flask, daemon=True).start()
    print("Serwer wideo działa pod adresem: http://127.0.0.1:9999/stream")

    # Czekamy chwilę na ustabilizowanie obrazu
    time.sleep(3)

    # 3. Sekwencja lotu (Program zablokuje się na każdej komendzie, dopóki dron jej nie ukończy!)
    try:
        print("Start...")
        tello.takeoff()

        print("Wykonuję kwadrat...")
        for _ in range(4):
            tello.move_forward(50)
            tello.rotate_clockwise(90)

    except Exception as e:
        print(f"Błąd podczas lotu: {e}")

    finally:
        print("Zakończanie działania...")
        try:
            # Próbujemy wylądować, ale jeśli dron już stoi na ziemi, ignorujemy błąd
            tello.land()
        except Exception:
            pass

        try:
            tello.streamoff()
        except Exception:
            pass

        print("Zakończono połączenie.")