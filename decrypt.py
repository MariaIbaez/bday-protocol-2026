import sys
import time

def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def main():
    slow_print("\n[+] INITIATING PHYSICAL DECRYPTION PROTOCOL...")
    time.sleep(0.5)
    slow_print("[+] Target hardware: TSA-Approved Combination Lock\n")
    
    # Checkpoint 1: Años juntos
    ans1 = input("[?] Checkpoint 1: ¿Cuántos años llevamos juntos?: ")
    if ans1.strip() != "5":
        slow_print("[-] Checkpoint 1 failed. Aborting handshake.")
        return

    # Checkpoint 2: Perritos
    ans2 = input("[?] Checkpoint 2: ¿Cuántos perritos vamos a tener?: ")
    if ans2.strip() != "2":
        slow_print("[-] Checkpoint 2 failed. Aborting handshake.")
        return

    # Checkpoint 3: Día de reencuentro
    ans3 = input("[?] Checkpoint 3: ¿Qué día de diciembre nos volvemos a ver?: ")
    if ans3.strip() != "23":
        slow_print("[-] Checkpoint 3 failed. Aborting handshake.")
        return

    slow_print("\n[+] Integrity checks passed. Decrypting master combination...")
    time.sleep(1.2)

    # AQUÍ PONES LA COMBINACIÓN REAL DE TU CANDADO
    combination = "7 - 4 - 2"

    print("\n" + "="*50)
    print(f"       SUCCESS! LOCK COMBINATION:  [ {combination} ]")
    print("="*50)
    slow_print("\nIntroduce los dígitos en el candado físico para abrir la caja.")
    slow_print("¡Feliz cumpleaños! Ya queda nada para el 23 de diciembre ❤️\n")

if __name__ == "__main__":
    main()
