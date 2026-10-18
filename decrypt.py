import sys, time, hmac, hashlib, unicodedata

PAYLOAD = {
  "checks": [
    {
      "salt": "a1c74081c7ea211f3c132862be4a343f",
      "hash": "dc2d5c3c527913026986aef5283a6f4176ac0624da701dd9447bbd2da891b0ea"
    },
    {
      "salt": "89c51347dd113b38337cc042f6ab52e7",
      "hash": "a54b8ed694e945486f7d56589b54ab91c3ec6d4963e47484b60ee0d7d7d7f585"
    },
    {
      "salt": "9e61af97ed2934cfb23bf37cbf97539b",
      "hash": "933aa6c58c0bbc9db2082435d46834691960e103fe6417a6e2fb86c1850d34a5"
    },
    {
      "salt": "ca57359683c9d3b4a06afbd995abed9a",
      "hash": "bff7cb3f9ef4f627c88119ca19c1c627c449a3f67593f85c5598e2f2723923c4"
    },
    {
      "salt": "44651bbf2e2a70b184ddbf7f10a4ac95",
      "hash": "a790bcbe32392cbda072665d3d2666360f0b27034f8131beb22cfd19691c9d47"
    }
  ],
  "salt": "1319a2b7077e2d403ab3d90f89a94ecd",
  "blob": "e18337",
  "tag": "3bde3b9a8342cb5715489a3470e8828ad5c9ad4d3321c2f180f95e9171eac3e1"
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
    ("¿Cuántos años llevamos juntos?",
     "Checkpoint 5 failed. Integrity check error.", ""),
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
    slow("¡Feliz cumpleaños mi vida! Ya no queda nada para vernos y pasar las mejores navidades ❤️\n")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyboardInterrupt, EOFError):
        print(f"\n{R}[-] Protocolo abortado.{X}"); sys.exit(1)
