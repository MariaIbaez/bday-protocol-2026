# bday-protocol-2026
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
    
    # Checkpoint 1
    ans1 = input("[?] Checkpoint 1: Number of the street in Ridgewood (e.g. 455): ")
    if ans1.strip() != "455":  # Cambia por el número real de su portal
        slow_print("[-] Checkpoint 1 failed. Aborting handshake.")
        return

    # Checkpoint 2
    ans2 = input("[?] Checkpoint 2: City where this package originated: ")
    if ans2.strip().lower() not in ["pamplona", "madrid"]:
        slow_print("[-] Checkpoint 2 failed. Unauthorized origin.")
        return

    slow_print("\n[+] Integrity checks passed. Decrypting 3-digit master combination...")
    time.sleep(1.5)

    # AQUÍ PONES EL CÓDIGO REAL DE TU CANDADO
    combination = "7 - 4 - 2"

    print("\n" + "="*50)
    print(f"       SUCCESS! LOCK COMBINATION:  [ {combination} ]")
    print("="*50)
    slow_print("\nEnter the digits on the physical lock to open the box.\nHappy Birthday!\n")

if __name__ == "__main__":
    main()
