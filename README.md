# 🖼️ TraspaRente

> Ottimo per rimuovere lo sfondo bianco/chiaro da immagini, ottenendo un file PNG con trasparenza. L'elaborazione è 100% locale, nessun dato inviato a server esterni.
>
> **Nota:** l'algoritmo è ottimale per sfondi uniformi chiari (firme su carta, loghi su bianco, ecc.). Per sfondi complessi si consiglia un approccio basato su modelli ML.

---

## 🚀 Provalo subito

**👉 [trasparente.streamlit.app](https://trasparente.streamlit.app/)**

Nessuna installazione richiesta — apri il link e inizia subito.

---

## 🔒 Privacy

L'elaborazione avviene **interamente in memoria RAM** durante la sessione Streamlit:

- Nessuna immagine viene salvata su disco
- Nessun dato viene trasmesso a server esterni o API di terze parti
- Alla chiusura della sessione, tutto viene eliminato automaticamente

---

## ✨ Funzionalità

- ⬆️ **Caricamento immagine** — supporta PNG, JPG, JPEG, WEBP, BMP
- ↔️ **Soglia regolabile** — controlla quanta parte dello sfondo viene rimossa
- 👁️ **Anteprima affiancata** — confronta originale e risultato in tempo reale
- ⬇️ **Download immediato** — scarica il PNG con trasparenza con un clic
- 🔒 **Privacy garantita** — nessun dato salvato su disco o trasmesso in rete

---

## 🧠 Come funziona

L'algoritmo opera direttamente sui pixel dell'immagine:

1. L'immagine viene convertita in modalità **RGBA** (aggiunge canale alpha)
2. Viene costruita una **maschera booleana** sui pixel in cui R, G e B sono tutti maggiori della soglia scelta
3. Il canale alpha di quei pixel viene impostato a `0` → **trasparenti**
4. Il risultato viene esportato in **PNG**, l'unico formato raster che preserva la trasparenza

---

## ⚙️ Parametro soglia

| Valore | Effetto |
|---|---|
| **Basso** (es. 100) | Rimuove solo i bianchi puri — conserva più dettagli |
| **Bilanciato** (es. 200) | Giusto compromesso — conserva i dettagli |
| **Alto** (es. 240) | Rimuove anche i grigi chiari — rischia di cancellare tratti sottili |

Regola lo slider fino a trovare il bilanciamento ideale per la tua immagine.

---


## 📄 Licenza

Distribuito sotto licenza **MIT** — vedi il file [`LICENSE`](./LICENSE).
