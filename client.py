import socket

# Sunucu Bağlantı Bilgileri
HOST = "localhost"
PORT = 8888

# İstemci Soketini Oluşturma
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Sunucudan şehir bilgisini al
message = client.recv(1024).decode()
print(message)

while True:
    # Kullanıcıdan tahmin al
    guess = input("Sıcaklık tahmininizi girin (veya 'END' yazarak çıkın): ")

    client.send(guess.encode())

    if guess.upper() == "END":
        print("Bağlantı kapatıldı.")
        break

    # Sunucudan geri bildirimi al
    response = client.recv(1024).decode()
    print(response)

    # Doğru tahmin yapıldıysa çık
    if "Doğru tahmin" in response or "3 tahmin hakkınız bitti" in response:
        break

client.close()
