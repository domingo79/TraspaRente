import streamlit as st
from PIL import Image
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
    dati = np.array(img)

    # Crea una maschera per i pixel da rendere trasparenti
    r, g, b, a = dati[:, :, 0], dati[:, :, 1], dati[:, :, 2], dati[:, :, 3]
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
        - ✅ Nessun dato viene trasmesso a server esterni
        - ✅ Alla chiusura della sessione tutto viene eliminato automaticamente
        - ✅ Puoi verificare il risultato in anteprima prima di scaricare
        """)
