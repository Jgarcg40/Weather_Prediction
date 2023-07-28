import subprocess

def main():
    print("Ejecutando AEMET_API_Historico-Leon.py desde el main...")
    try:
        subprocess.run(['python', 'AEMET_API_Historico-Leon.py'], check=True)
        print("AEMET_API_Historico-Leon.py se ha ejecutado correctamente")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar AEMET_API_Historico-Leon.py {e.returncode}")

if __name__ == "__main__":
    main()