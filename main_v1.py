from PIL import Image
import numpy as np
import os

# --- Configurazioni ---
INPUT_PATH = 'input/firma.png'
OUTPUT_PATH = 'output/firma_trasparente.png'
SOGLIA = 200  # Soglia per determinare i pixel da rendere trasparenti (0-255)


def rimuovi_sfondo(input_path: str, output_path: str, soglia: int) -> None:
    """
    Rimuove lo sfondo bianco da un'immagine (es. firma su foglio).
    I pixel più chiari della soglia diventano trasparenti.

    Args:
        input_path: percorso immagine originale
        output_path: percorso immagine contrasparenza
        soglia: valore 0-255, più è alto più sfondo viene rimosso
    """
    img = Image.open(input_path).convert("RGBA")
    dati = np.array(img)

    # Crea una maschera per i pixel da rendere trasparenti
    r, g, b, a = dati[:, :, 0], dati[:, :, 1], dati[:, :, 2], dati[:, :, 3]

    maschera_sfondo = (r > soglia) & (g > soglia) & (b > soglia)
    dati[maschera_sfondo, 3] = 0  # Imposta alpha a 0 per i pixel di sfondo

    risultato = Image.fromarray(dati)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    risultato.save(output_path)
    print(f"✅ Fatto! Immagine salvata in: {output_path}")


# --- Esecuzione ---
if __name__ == "__main__":
    rimuovi_sfondo(INPUT_PATH, OUTPUT_PATH, SOGLIA)
