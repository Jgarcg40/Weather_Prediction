import subprocess

def main():
    print("Ejecutando AEMET_API_Historico-Leon.py desde el main...")
    try:
        subprocess.run(['python', 'AEMET_API_Historico-Leon.py'], check=True)
        print("AEMET_API_Historico-Leon.py se ha ejecutado correctamente")
        print("Ejecutando Train_Model.py desde el main...")
        subprocess.run(['python', 'Train_Model.py'], check=True)
        print("Train_Model.py se ha ejecutado correctamente")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar un archivo: {e.returncode}")

if __name__ == "__main__":
    main()
