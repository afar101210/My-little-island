#!/usr/bin/env python3
"""
Escanea todos los perpetuos USDT-M de Binance durante el crash del 10/10/2025
y lista cuales subieron (o tuvieron mechas fuertes al alza) mientras BTC caia.

Usa el archivo publico data.binance.vision (velas de 1m oficiales), que:
  - funciona desde servidores de EE.UU. (GitHub Actions), donde fapi da 451
  - incluye pares que ya fueron deslistados

Salida: resultados.md + crash_1010_resultados.csv
"""
import csv
import io
import re
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import requests

DIA = "2025-10-10"
START = datetime(2025, 10, 10, 20, 0, tzinfo=timezone.utc)   # ventana UTC
END = datetime(2025, 10, 10, 22, 0, tzinfo=timezone.utc)
START_MS = int(START.timestamp() * 1000)
END_MS = int(END.timestamp() * 1000)
TRAMO_MIN = 15  # minutos del peor tramo de BTC

LISTADO = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision"
ARCHIVO = "https://data.binance.vision/data/futures/um/daily/klines/{s}/1m/{s}-1m-" + DIA + ".zip"

S = requests.Session()


def http_get(url, **kw):
    for intento in range(5):
        try:
            r = S.get(url, timeout=30, **kw)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            return r
        except requests.RequestException:
            time.sleep(2 * (intento + 1))
    return None


def simbolos():
    prefijo = "data/futures/um/daily/klines/"
    out, marker = [], ""
    while True:
        r = http_get(LISTADO, params={"delimiter": "/", "prefix": prefijo, "marker": marker})
        xml = r.text
        encontrados = re.findall(r"<Prefix>" + re.escape(prefijo) + r"([^/<]+)/</Prefix>", xml)
        out += encontrados
        if "<IsTruncated>true</IsTruncated>" not in xml or not encontrados:
            break
        m = re.findall(r"<NextMarker>([^<]+)</NextMarker>", xml)
        marker = m[-1] if m else prefijo + encontrados[-1] + "/"
    return sorted({s for s in out if s.endswith("USDT")})


def velas(sym):
    r = http_get(ARCHIVO.format(s=sym))
    if r is None:
        return None
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        texto = z.read(z.namelist()[0]).decode()
    k = []
    for fila in csv.reader(io.StringIO(texto)):
        if not fila or not fila[0].isdigit():  # salta cabecera
            continue
        t = int(fila[0])
        if START_MS <= t < END_MS:
            k.append((t, float(fila[1]), float(fila[2]), float(fila[3]), float(fila[4])))
    return k


def peor_tramo(btc):
    peor, idx = 0.0, 0
    for i in range(len(btc) - TRAMO_MIN):
        ret = btc[i + TRAMO_MIN][4] / btc[i][1] - 1
        if ret < peor:
            peor, idx = ret, i
    return btc[idx][0], btc[idx + TRAMO_MIN][0], peor


def ret_en(k, t0, t1):
    tramo = [x for x in k if t0 <= x[0] <= t1]
    if len(tramo) < 2 or tramo[0][1] == 0:
        return None
    return tramo[-1][4] / tramo[0][1] - 1


def hhmm(ms):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%H:%M")


def main():
    syms = simbolos()
    print(f"{len(syms)} simbolos USDT-M en el archivo")

    btc = velas("BTCUSDT")
    t0, t1, caida = peor_tramo(btc)
    print(f"Peor tramo BTC: {hhmm(t0)}-{hhmm(t1)} UTC ({caida:.2%})")

    def analizar(sym):
        k = velas(sym)
        if not k or len(k) < 30 or k[0][1] == 0:
            return None
        o = k[0][1]
        return {
            "symbol": sym,
            "ret_tramo_btc": ret_en(k, t0, t1),
            "ret_2h": k[-1][4] / o - 1,
            "mecha_arriba": max(x[2] for x in k) / o - 1,
            "mecha_abajo": min(x[3] for x in k) / o - 1,
        }

    with ThreadPoolExecutor(max_workers=16) as ex:
        res = [r for r in ex.map(analizar, syms) if r]
    print(f"{len(res)} con datos en la ventana")

    with open("crash_1010_resultados.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(res[0].keys()))
        w.writeheader()
        w.writerows(res)

    pct = lambda v: "n/a" if v is None else f"{v:+.1%}"
    lineas = [
        f"# Crash 10/10/2025 — perps USDT-M Binance",
        "",
        f"Ventana: 20:00–22:00 UTC. Peor tramo de BTC: **{hhmm(t0)}–{hhmm(t1)} UTC ({caida:.2%})**. "
        f"Analizados: {len(res)} pares (incluye deslistados).",
        "",
    ]

    def tabla(titulo, filas):
        lineas.extend([f"## {titulo}", "",
                       "| Par | En tramo BTC | Ventana 2h | Mecha arriba | Mecha abajo |",
                       "|---|---|---|---|---|"])
        for r in filas[:25]:
            lineas.append(f"| {r['symbol']} | {pct(r['ret_tramo_btc'])} | {pct(r['ret_2h'])} | "
                          f"{pct(r['mecha_arriba'])} | {pct(r['mecha_abajo'])} |")
        if not filas:
            lineas.append("| (ninguno) | | | | |")
        lineas.append("")

    tabla(f"Subieron mientras BTC caía ({hhmm(t0)}–{hhmm(t1)} UTC)",
          sorted([r for r in res if (r["ret_tramo_btc"] or -1) > 0], key=lambda r: -r["ret_tramo_btc"]))
    tabla("Cerraron verdes la ventana 20:00–22:00 UTC",
          sorted([r for r in res if r["ret_2h"] > 0], key=lambda r: -r["ret_2h"]))
    tabla("Mayores mechas al alza (aunque cerraran rojo)",
          sorted(res, key=lambda r: -r["mecha_arriba"]))
    tabla("Mayores mechas a la baja",
          sorted(res, key=lambda r: r["mecha_abajo"]))

    md = "\n".join(lineas)
    with open("resultados.md", "w") as f:
        f.write(md)
    print(md)


if __name__ == "__main__":
    main()
