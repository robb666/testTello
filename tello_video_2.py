import socket
import cv2
import time


class TelloVideo:
    def __init__(self):
        self.tello_ip = '192.168.10.1'
        self.tello_port = 8889
        self.tello_address = (self.tello_ip, self.tello_port)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', 9000))

        self.start_stream()
        self.show_video()

    def start_stream(self):
        print("[ INFO ] Wysyłanie komend do Tello...")
        # Wejście w tryb SDK
        self.sock.sendto(b'command', self.tello_address)
        time.sleep(1)  # Czekamy na przetworzenie

        # Uruchomienie strumienia
        self.sock.sendto(b'streamon', self.tello_address)
        print("[ INFO ] Strumień uruchomiony. Oczekiwanie na wideo...")
        time.sleep(2)  # Dajemy dronowi czas na rozpoczęcie wysyłania klatek

    def show_video(self):
        # OpenCV potrafi czytać strumień UDP bezpośrednio z portu 11111
        # Flaga udp://@0.0.0.0:11111 mówi FFmpeg, żeby nasłuchiwał na wszystkich interfejsach
        cap = cv2.VideoCapture("udp://@0.0.0.0:11111")

        if not cap.isOpened():
            print("[ ERROR ] Nie można otworzyć strumienia wideo. Czy jesteś połączony z WiFi Tello?")
            return

        print("[ INFO ] Rozpoczęto wyświetlanie wideo. Naciśnij 'q', aby wyjść.")

        while True:
            ret, frame = cap.read()
            if ret:
                # Opcjonalnie: zmniejsz rozmiar okna, jeśli wideo jest za duże
                # frame = cv2.resize(frame, (720, 480))

                cv2.imshow('Tello Camera', frame)

            # Wyjście po naciśnięciu klawisza 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Sprzątanie po zakończeniu
        cap.release()
        cv2.destroyAllWindows()
        self.sock.sendto(b'streamoff', self.tello_address)
        print("[ INFO ] Zakończono połączenie.")


if __name__ == '__main__':
    video = TelloVideo()