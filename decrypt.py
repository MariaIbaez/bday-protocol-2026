#!/usr/bin/env python3
"""PROTOCOL-26 // decrypt.py
Solo biblioteca estándar. Las respuestas y la combinación NO están en el código:
la combinación va cifrada y solo se abre con las 4 respuestas correctas.
(Genera PAYLOAD con make_payload.py y pégalo abajo.)
"""
import sys, time, hmac, hashlib, unicodedata

# ---- PEGA AQUÍ EL RESULTADO DE make_payload.py ----
PAYLOAD = None
# ----------------------------------------------------

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
    import os; os.system("")          # activa colores ANSI en Windows
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
    """Acepta la respuesta entera o cualquier palabra suelta (ej. 'el argentino')."""
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
        print("Falta el PAYLOAD. Ejecuta make_payload.py y pégalo en decrypt.py."); return 1
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
