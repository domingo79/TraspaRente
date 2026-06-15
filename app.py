import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
from io import BytesIO

# --- Configurazioni Pagina ---
st.set_page_config(
    page_title="Rimuovi Sfondo",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="collapsed"
)
st.title("🖼️ Rimuovi Sfondo da Immagine")
st.caption(
    "Carica un'immagine con sfondo bianco e ottieni una versione con sfondo trasparente.")


def rimuovi_sfondo(img: Image.Image, soglia: int) -> Image.Image:
    """
    Rimuove lo sfondo bianco/chiaro da un'immagine.
    Restituisce una nuova immagine RGBA con sfondo trasparente.

    Args:
        img: immagine originale
        soglia: valore 0-255, più è alto più sfondo viene rimosso
    """
    img = img.convert("RGBA")
    rgb = img.convert("RGB")

    # Le foto hanno spesso ombre o luce non uniforme sul foglio: stimando lo
    # sfondo con una sfocatura ampia e dividendo l'immagine per questa stima
    # si "appiattisce" l'illuminazione, riportando il foglio a bianco uniforme
    # prima di applicare la soglia.
    raggio = max(15, min(rgb.size) // 10)
    sfondo_stimato = rgb.filter(ImageFilter.GaussianBlur(radius=raggio))

    originale = np.asarray(rgb, dtype=np.float32)
    sfondo = np.asarray(sfondo_stimato, dtype=np.float32)
    normalizzato = np.clip(originale / np.maximum(sfondo, 1) * 255, 0, 255)

    dati = np.array(img)
    r, g, b = normalizzato[:, :, 0], normalizzato[:,
                                                  :, 1], normalizzato[:, :, 2]
    maschera_sfondo = (r > soglia) & (g > soglia) & (b > soglia)
    dati[maschera_sfondo, 3] = 0  # Imposta alpha a 0 per i pixel di sfondo

    return Image.fromarray(dati)


def img_to_bytes(img: Image.Image) -> bytes:
    """Converte un'immagine PIL in bytes per il download."""
    buffer = BytesIO()
    #  Il motivo per cui ho fissato PNG è che è l'unico formato che supporta la trasparenza (canale alpha)
    # con qualsiasi altro formato la trasparenza verrebbe persa e lo sfondo tornerebbe bianco
    img.save(buffer, format="PNG")
    return buffer.getvalue()


st.divider()

file = st.file_uploader("Carica un'immagine",
                        accept_multiple_files=False,
                        type=["png", "jpg", "jpeg", "webp", "bmp"],
                        help="Formati supportati: PNG, JPG, JPEG, WEBP, BMP")

if file is not None:
    img_originale = Image.open(file)

    soglia = st.slider("Soglia di rimozione sfondo",
                       min_value=100,
                       max_value=254,
                       value=200,
                       help="Aumenta se lo sfondo non viene rimosso del tutto. Abbassa se spariscono parti della firma."
                       )

    # --- Elaborazione dell'immagine ---
    img_risultato = rimuovi_sfondo(img_originale, soglia)

    # --- Anteprima affiancata ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Immagine Originale")
        st.image(img_originale, use_container_width=True)
    with col2:
        st.subheader("Risultato con Sfondo Trasparente")
        st.image(img_risultato, use_container_width=True)

    # --- Download del risultato ---
    nome_output = file.name.rsplit(".", 1)[0] + "_trasparente.png"

    st.download_button(
        label="⬇️ Scarica Immagine Trasparente",
        data=img_to_bytes(img_risultato),
        file_name=nome_output,
        mime="image/png",
        use_container_width=True
    )
else:
    st.info("⬆️ Carica un'immagine per iniziare.")

    st.divider()

    with st.expander("🔒 **Privacy garantita**", expanded=True):
        st.markdown("""
        - ✅ La tua immagine viene elaborata **solo in memoria**, mai salvata su disco
        - ✅ Alla chiusura della sessione tutto viene eliminato automaticamente
        - ✅ Puoi verificare il risultato in anteprima prima di scaricare
        """)
