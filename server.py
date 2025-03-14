import socket
import pandas as pd
import random

# Sunucu Ayarları
HOST = "localhost"
PORT = 8888

# Excel dosyasını yükleme
df = pd.read_excel("weathers.xlsx")  # Excel dosyanızın adını kontrol edin

# Sunucu Soketini Oluşturma
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Sunucu başlatıldı, istemci bekleniyor...")

client_socket, client_address = server.accept()
print(f"Bağlantı sağlandı: {client_address}")

# Rastgele bir şehir seç
city, actual_temp = random.choice(df.values)

# İstemciye şehir bilgisi gönder
client_socket.send(f"Tahmin yap: {city}".encode())

attempts = 0  # Yanlış tahmin sayacı

while True:
    # İstemciden tahmini al
    guess = client_socket.recv(1024).decode()

    if guess.upper() == "END":
        print("Bağlantı sonlandırıldı.")
        client_socket.close()
        break

    try:
        guess_temp = int(guess)
    except ValueError:
        client_socket.send("Geçersiz giriş, lütfen sayı girin.".encode())
        continue

    # %10 tolerans ile doğru tahmin kontrolü
    tolerance = actual_temp * 0.1
    if abs(guess_temp - actual_temp) <= tolerance:
        client_socket.send(f"Tebrikler! Doğru tahmin: {actual_temp}°C".encode())
        break
    else:
        attempts += 1
        if attempts >= 3:
            client_socket.send(f"3 tahmin hakkınız bitti! Doğru sıcaklık: {actual_temp}°C".encode())
            break
        hint = "Daha Yüksek" if guess_temp < actual_temp else "Daha Düşük"
        client_socket.send(f"Yanlış tahmin. {hint}".encode())

client_socket.close()
server.close()
