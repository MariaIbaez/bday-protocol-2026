
import sys, time, hmac, hashlib, unicodedata

PAYLOAD = {
  "checks": [
    {
      "salt": "a1146e192a889f3c30a475980de6f175",
      "hash": "6a89585a88a4f6ce034cb143f19defdad1f17df33babf6aeeac5f247bad73735"
    },
    {
      "salt": "be1562801c67981e6b43530fe82a656d",
      "hash": "0979ec9bd53579cf924bc40056a732780c4d77feee783264e8628ebe6ed291ad"
    },
    {
      "salt": "369a27578e56fbe94564f09ccb9d74bc",
      "hash": "4087cf287ea4ff7ba96a1a3aab7e9386c64e91d2918e363d448e0d99b502ebdc"
    },
    {
      "salt": "aa66a3c55a9fbaff6630467c52b71611",
      "hash": "19d70ed74bddb7eec802d82a168332e6a0e9b2a6fc7806ea72c4ce4ad58ba73b"
    }
  ],
  "salt": "6be2e481fdd1455ab38e39bc58ca94b5",
  "blob": "3e37ce",
  "tag": "f5ce9df63de345ce6368cd7b2e6d0d06f402291c4686f3b443a93144c0935c0e"
}

CHECKPOINTS = [
    ("Ciudad donde empezó nuestra historia",
     "Checkpoint 1 failed. Handshake rechazado.", ""),
    ("Un viaje que recordaré toda la vida (todos, pero este especialmente)",
     "Checkpoint 2 failed. Access denied.", ""),
    ("¿A dónde vamos a ir cuando vuelvas?",
     "Checkpoint 3 failed. Target unknown.", ""),
    ("¿Qué acento nos gusta más usar?",
     "Checkpoint 4 failed. Identidad no confirmada, che.", ""),
]
MAX_TRIES = 3
ITER = 200_000

FAST = "--fast" in sys.argv or not sys.stdout.isatty()
if sys.platform == "win32":
    import os; os.system("")
G, R, Y, D, B, X = "\033[92m", "\033[91m", "\033[93m", "\033[2m", "\033[1m", "\033[0m"
if not sys.stdout.isatty():
    G = R = Y = D = B = X = ""

def slow(text="", delay=0.025):
    if FAST:
        print(text); return
    for ch in text:
        sys.stdout.write(ch); sys.stdout.flush(); time.sleep(delay)
    print()

def pause(s):
    if not FAST: time.sleep(s)

def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join("".join(c if c.isalnum() else " " for c in s).split())

def kdf(text, salt):
    return hashlib.pbkdf2_hmac("sha256", text.encode(), salt, ITER)

def check(answer, chk):
    a = norm(answer)
    for cand in [a] + a.split():
        if hmac.compare_digest(kdf(cand, bytes.fromhex(chk["salt"])).hex(), chk["hash"]):
            return cand
    return None

def keystream(key, n):
    out, i = b"", 0
    while len(out) < n:
        out += hashlib.sha256(key + i.to_bytes(4, "big")).digest(); i += 1
    return out[:n]

def decrypt(answers, p):
    key = kdf("|".join(answers), bytes.fromhex(p["salt"]))
    blob = bytes.fromhex(p["blob"])
    if not hmac.compare_digest(hmac.new(key, blob, "sha256").hexdigest(), p["tag"]):
        return None
    return bytes(a ^ b for a, b in zip(blob, keystream(key, len(blob)))).decode()

def bar(label, secs=1.6, width=30):
    if FAST:
        print(f"{label} [{'#'*width}] 100%"); return
    for i in range(width + 1):
        sys.stdout.write(f"\r{label} [{'#'*i}{'.'*(width-i)}] {int(i/width*100):3d}%")
        sys.stdout.flush(); time.sleep(secs / width)
    print()

def main():
    if not PAYLOAD:
        print("Falta el PAYLOAD."); return 1
    slow(f"\n{G}[+] INITIATING PHYSICAL DECRYPTION PROTOCOL...{X}")
    pause(0.5)
    slow(f"{G}[+] Target hardware:{X} TSA-Approved Combination Lock")
    slow(f"{D}    (escribe 'salir' en cualquier momento para abortar){X}\n")

    answers = []
    for n, (prompt, fail_msg, hint) in enumerate(CHECKPOINTS, 1):
        for attempt in range(1, MAX_TRIES + 1):
            raw = input(f"{Y}[?]{X} Checkpoint {n}/{len(CHECKPOINTS)}: {prompt}: ").strip()
            if norm(raw) in ("salir", "exit", "q"):
                slow(f"{R}[-] Protocolo abortado.{X}"); return 1
            found = check(raw, PAYLOAD["checks"][n - 1])
            if found:
                slow(f"{G}[+] Checkpoint {n} OK{X}\n", 0.015)
                answers.append(found); break
            left = MAX_TRIES - attempt
            slow(f"{R}[-] Respuesta incorrecta.{X} " + (f"Te quedan {left} intento(s)." if left else ""), 0.015)
            if hint and attempt == MAX_TRIES - 1:
                slow(f"{D}    pista: {hint}{X}", 0.015)
        else:
            slow(f"{R}[-] {fail_msg}{X}"); return 1

    slow(f"{G}[+] Integrity checks passed.{X}")
    bar("[+] Decrypting master combination")
    combo = decrypt(answers, PAYLOAD)
    if combo is None:
        slow(f"{R}[-] Fallo de descifrado.{X}"); return 1

    line = "=" * 50
    print(f"\n{G}{line}\n   SUCCESS!  LOCK COMBINATION:  {B}[ {combo} ]{X}{G}\n{line}{X}\n")
    slow("Introduce los dígitos en el candado físico para abrir la caja.")
    slow("¡Feliz cumpleaños! Ya no queda nada para el 23 de diciembre ❤️\n")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyboardInterrupt, EOFError):
        print(f"\n{R}[-] Protocolo abortado.{X}"); sys.exit(1)
