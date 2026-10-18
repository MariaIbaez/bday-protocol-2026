
import sys, time, hmac, hashlib, unicodedata

PAYLOAD = {
  "checks": [
    {
      "salt": "8252305411c5ec80ba6367197b396099",
      "hash": "9ff284a2d6456e56b8d84b4838cc0ea91253e647a3463213d5e96dbd7dab083d"
    },
    {
      "salt": "441853108b5f56698d9fa732d146972c",
      "hash": "89a9d8b722f1777f2f476781fde11111628933a50540ee9ad204bac32d3613b2"
    },
    {
      "salt": "0ea309d4d1b05aecc62ae0e9067d1bc2",
      "hash": "dff13660966e9fb0f93f5c977fec4a6f649772a47afd858d9aa2beca36b88135"
    },
    {
      "salt": "4380803e0cc7cc063dc4a1754e86c983",
      "hash": "b72b1ddf6b8e5829ee89950d4a6bb8a304683c4cc627d7c279957d66a32f8986"
    }
  ],
  "salt": "160cf4b0cd380cfe928643724b2c565a",
  "blob": "bd2386",
  "tag": "666ca8735a8d30870cdaf9864464197b74569147bdd9c5b8836491d701767dc6"
}

CHECKPOINTS = [
    ("Ciudad donde empezó nuestra historia",
     "Checkpoint 1 failed. Handshake rechazado.", ""),
    ("Un viaje que recordaré toda la vida (todos, pero este especialmente)",
     "Checkpoint 2 failed. Access denied.", ""),
    ("¿A dónde vamos a ir cuando vuelvas?",
     "Checkpoint 3 failed. Target unknown.", ""),
    ("¿Cuántos años llevamos juntos?",
     "Checkpoint 4 failed. Identidad no confirmada.", ""),
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
    return " ".join({"cinco": "5"}.get(w, w) for w in "".join(c if c.isalnum() else " " for c in s).split())

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
