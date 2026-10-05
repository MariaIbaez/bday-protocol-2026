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
    
    # Checkpoint 1: Bilbao
    ans1 = input("[?] Checkpoint 1: Ciudad donde empezó nuestra historia: ")
    if "bilbao" not in ans1.strip().lower():
        slow_print("[-] Checkpoint 1 failed. Aborting handshake.")
        return

    # Checkpoint 2: Menorca
    ans2 = input("[?] Checkpoint 2: Un viaje que recordaré toda la vida (todos, pero este especialmente): ")
    if "menorca" not in ans2.strip().lower():
        slow_print("[-] Checkpoint 2 failed. Access denied.")
        return

    # Checkpoint 3: Luz
    ans3 = input("[?] Checkpoint 3: ¿A dónde vamos a ir cuando vuelvas?: ")
    if "luz" not in ans3.strip().lower():
        slow_print("[-] Checkpoint 3 failed. Target unknown.")
        return

    # Checkpoint 4: Argentino
    ans4 = input("[?] Checkpoint 4: ¿Qué acento nos gusta más usar?: ")
    if "argentino" not in ans4.strip().lower():
        slow_print("[-] Checkpoint 4 failed. Identidad no confirmada, che.")
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
