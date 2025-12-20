"""Stressz teszt szkript.

Ez a szkript multiprocessing-gel terheli a CPU-t tesztelés céljából.
"""

import multiprocessing
import time


def stress_test() -> None:
    """Stressz teszt függvény.

    20 másodpercig terheli a CPU-t egyszerű műveletekkel.
    """
    print("Számítás indul...")
    # Ez a ciklus 20 másodpercig pörgeti a processzort
    end_time = time.time() + 20
    while time.time() < end_time:
        _ = 100 * 100  # Egyszerű művelet végtelenítve


if __name__ == "__main__":
    # Elindítjuk annyi szálon, ahány mag van a laptopban
    processes = []
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=stress_test)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    print("Teszt vége.")
