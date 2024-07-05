import time
import threading
import pandas as pd

def chequeoDatos(df):
    print(df.isnull().values.any())

if __name__ == '__main__':
    df = pd.read_table('archivos/FootProfile1.xyz', skiprows=2, delim_whitespace=True, names=["X", "Y", "Z"])

    to = time.time()
    for i in range(10):
        chequeoDatos(df)
        print("Tiempo en serie: ", time.time() - to)
        to = time.time()

    to = time.time()
    # Usando hilos en lugar de procesos
    t=[]
    for i in range(10):
        t.append(threading.Thread(target=chequeoDatos, args=(df,)))
        t[i].start()
    for i in range(10):
        t[i].join()
    print("Tiempo en paralelo con hilos: ", time.time() - to)