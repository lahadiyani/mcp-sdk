# providers/ — External World Adapters

## Tujuan Folder Ini

Folder `providers/` berisi adapter ke dunia eksternal:

* LLM
* Image generation
* Audio / speech
* API pihak ketiga
* Model inference remote

> **Providers BUKAN core MCP.**
> Mereka adalah *impure boundary* yang sengaja dipisahkan.

---

## Prinsip Wajib Providers

### 1. Providers ≠ Core

Providers:

* ❌ Tidak boleh mengandung logic routing MCP
* ❌ Tidak boleh mengakses `Dispatcher`
* ❌ Tidak boleh membuat `MCPRequest` / `MCPResponse`
* ❌ Tidak boleh menyimpan state global

Providers:

* ✅ Boleh async
* ✅ Boleh IO
* ✅ Boleh network
* ✅ Boleh retry / timeout
* ✅ Boleh fail

---

### 2. Providers Adalah Adapter, Bukan Tool

Perbedaan penting:

| Layer               | Fungsi                |
| ------------------- | --------------------- |
| `providers/`        | Bicara ke dunia luar  |
| `core/tools/`       | Logic MCP murni       |
| `core/contracts.py` | Interface antar layer |

**Tools memanggil provider, bukan sebaliknya.**

```
Tool → Provider → External API
```

Bukan:

```
Provider → Dispatcher ❌
Provider → MCPResponse ❌
```

---

### 3. Providers Tidak Boleh Mengubah Shape Data MCP

Provider:

* menerima input Python biasa
* mengembalikan data Python biasa

Transformasi ke/dari MCP:

* dilakukan di `core/tools/*`
* bukan di provider

---

## Struktur Folder

```
providers/
├─ __init__.py
│
├─ pollinations/
│  ├─ __init__.py
│  ├─ text.py      # Text / LLM adapter
│  ├─ image.py     # Image generation adapter
│  └─ audio.py     # Audio / transcription adapter
│
└─ README.md
```

Setiap subfolder:

* mewakili satu vendor / backend
* tidak boleh bercampur vendor lain

---

## Kontrak Implisit Provider

Setiap provider module **HARUS**:

* Stateless
* Bisa dipanggil berulang
* Tidak menyimpan cache global
* Tidak logging secara agresif
* Tidak crash MCP (raise error terkontrol)

Contoh gaya API (konseptual):

```python
async def generate_text(prompt: str, **options) -> str:
    ...
```

atau

```python
def generate_image(prompt: str, **options) -> bytes:
    ...
```

---

## Error Handling Rules

Provider **boleh**:

* raise exception Python
* return error object internal

Provider **tidak boleh**:

* raise `MCPError`
* tahu `MCPErrorCode`

Mapping error → MCP:

* dilakukan di **tool layer**
* bukan di provider

---

## Async vs Sync

Providers **boleh async**.

Core MCP:

* tidak peduli async atau sync
* tool bertanggung jawab mengadaptasi

Jika async:

* tool yang memanggil harus eksplisit async-aware

---

## Logging & Observability

Providers:

* boleh pakai `utils.logging.get_logger`
* default ke `stderr`
* tidak boleh konfigurasi global logging

No:

```python
logging.basicConfig(...)  # ❌
```

Yes:

```python
from utils.logging import get_logger
log = get_logger(__name__)
```

---

## Dependency Rules

Providers:

* **boleh** punya dependency berat (SDK, client, dll)
* **tidak boleh** bocor ke core

Core MCP harus:

* tetap bisa di-import tanpa providers

Ini menjaga:

* testability
* minimal footprint
* deployment fleksibel
