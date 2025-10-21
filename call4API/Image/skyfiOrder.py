import json
from datetime import datetime
from pathlib import Path
import csv
class Order:
    def __init__(self, conf):
        self.catalog_folder = Path(conf.get("catalogfolder"))
        self.order_request_folder =  Path(conf.get("orderrequestfolder"))
        self.order_response_folder = Path(conf.get("orderresponsefolder"))
        self.download_image_folder = Path(conf.get("downloadimagefolder"))
        self.deliverable_type = conf.get("deliverabletype")
        self.order_request_file = "order_request.txt"
        self.csv_filename = "orders.csv"

    def order_txt_to_csv(self, txt_path: str = None):
        """
        Legge gli archiveId da un file TXT (uno per riga) e li inserisce in un CSV
        con colonne: archiveId, order_name, status, isImageDownloaded.
        - Evita duplicati (matching su archiveId).
        - Crea il CSV con header se non esiste.
        - Valori iniziali:
            order_name = ""         (verrà riempito dopo aver creato/salvato l'ordine)
            status = ""             (verrà letto dai JSON di risposta ordine)
            isImageDownloaded = "false"  (verrà aggiornato dopo il download)
        Ritorna: (percorso_csv, stats_dict)
        """
        # 1) Sorgente TXT
        if txt_path is None:
            # usa il TXT di default salvato nella cartella degli order request
            txt_path = self.order_request_folder / self.order_request_file
        src = Path(txt_path).expanduser().resolve()
        if not src.exists():
            raise FileNotFoundError(f"File TXT non trovato: {src}")

        # 2) Destinazione CSV (registro)
        dst_dir = self.order_request_folder
        dst_dir.mkdir(parents=True, exist_ok=True)
        csv_path = dst_dir / self.csv_filename

        # 3) Leggi gli ID dal TXT
        raw_lines = src.read_text(encoding="utf-8").splitlines()
        ids = [line.strip() for line in raw_lines if line.strip()]
        if not ids:
            print("Nessun archiveId nel TXT; nessun aggiornamento al CSV.")
            return str(csv_path), {"added": 0, "skipped": 0, "total": 0}

        # 4) Carica eventuali righe esistenti dal CSV
        existing_rows = []
        existing_index = {}  # archiveId -> row
        if csv_path.exists():
            with open(csv_path, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # normalizza chiavi mancanti (per sicurezza)
                    row.setdefault("archiveId", "")
                    row.setdefault("order_name", "")
                    row.setdefault("status", "")
                    row.setdefault("isImageDownloaded", "false")
                    existing_rows.append(row)
                    if row["archiveId"]:
                        existing_index[row["archiveId"]] = row

        # 5) Aggiungi nuovi ID evitando duplicati
        added = 0
        for aid in ids:
            if aid not in existing_index:
                new_row = {
                    "archiveId": aid,
                    "order_name": "",
                    "status": "",
                    "isImageDownloaded": "false",
                }
                existing_rows.append(new_row)
                existing_index[aid] = new_row
                added += 1

        skipped = len(ids) - added
        total = len(existing_rows)

        # 6) Scrivi (o riscrivi) il CSV con header ordinato
        fieldnames = ["archiveId", "order_name", "status", "isImageDownloaded"]
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(existing_rows)

        print(f"Registro aggiornato: {csv_path} (+{added} nuovi, {skipped} duplicati, tot={total})")
        return str(csv_path), {"added": added, "skipped": skipped, "total": total}

    def get_achiveId_toplace(self):
        csv_path = self.order_request_folder / self.csv_filename
        if not csv_path.exists():
            print(f"CSV non trovato: {csv_path}")
            return {"to_order": 0, "ordered": 0, "errors": 0}

        # 1) carica righe esistenti
        with open(csv_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # normalizza colonne minime richieste
        for r in rows:
            r.setdefault("archiveId", "")
            r.setdefault("order_name", "")
            r.setdefault("status", "")
            r.setdefault("isImageDownloaded", "false")

        # 2) seleziona le righe vuote
        candidates_idx = [
            i for i, r in enumerate(rows)
            if r.get("archiveId") and not r.get("order_name") and not r.get("status")
        ]
        if not candidates_idx:
            print("Nessuna riga 'vuota' nel CSV da ordinare.")
            return {"to_order": 0, "ordered": 0, "errors": 0}

        archive_ids = [rows[i]["archiveId"] for i in candidates_idx]
        return archive_ids

    def save_order_response(self, response_data):
        #Salva la/e response JSON degli ordini nella cartella 'order_response_folder'.
        out_dir = self.order_response_folder
        out_dir.mkdir(parents=True, exist_ok=True)

        saved_files = []
        # Se è una singola risposta, la metto in lista
        if isinstance(response_data, dict):
            response_data = [response_data]

        for item in response_data:
            filename = ""
            try:
                #order_id = item['response']['id']
                order_code = item['response']['orderCode']
                created_at = item.get("createdAt", datetime.now().strftime("%Y%m%d"))
                captureTimestamp = (item['response']['archive']['captureTimestamp'], datetime.now().strftime("%Y%m%d"))
                filename = f"order_ID_{order_code}_{created_at}.json"
                out_path = out_dir / filename

                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(item, f, indent=2, ensure_ascii=False)

                print(f"Ordine salvato in {out_path.name}")
                saved_files.append(str(out_path.resolve()))

            except Exception as e:
                print(f"Errore nel salvataggio ordine {filename}: {e}")
        self.update_orders_csv_from_responses(response_data, saved_files)

        return saved_files

    def update_orders_csv_from_responses(self, response_data, saved_files):
        """
        Aggiorna orders.csv usando le risposte dell'API (response_data) e i file JSON salvati (saved_files).
        - Match su 'archiveId' (chiave nel CSV).
        - Compila 'order_name' con il filename JSON salvato.
        - Compila 'status' con lo stato ordine restituito dall'API (o 'ERROR[...]').

        Parametri:
            response_data: list[dict] | dict
                Struttura prevista: {"archiveId": <str>, "status": "ok"|"error", "response": {...}}.
            saved_files: list[str]
                Elenco dei path JSON salvati nello stesso ordine di response_data.

        Ritorna: dict con statistiche {"updated": X, "errors": Y}
        """

        # Normalizza response_data a lista
        if isinstance(response_data, dict):
            response_data = [response_data]
        if saved_files is None:
            saved_files = []

        csv_path = self.order_request_folder / self.csv_filename
        if not csv_path.exists():
            print(f"CSV non trovato: {csv_path}")
            return {"updated": 0, "errors": len(response_data)}

        # Carica CSV
        with open(csv_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Indice archiveId -> idx riga
        index = {}
        for i, r in enumerate(rows):
            r.setdefault("archiveId", "")
            r.setdefault("order_name", "")
            r.setdefault("status", "")
            r.setdefault("isImageDownloaded", "false")
            if r["archiveId"]:
                index[r["archiveId"]] = i

        updated = 0
        errors = 0

        for i, item in enumerate(response_data):
            archive_id = item.get("archiveId")
            if not archive_id or archive_id not in index:
                errors += 1
                continue

            row = rows[index[archive_id]]

            if item.get("status") == "ok":
                api_resp = item.get("response", {}) or {}
                # status dell'ordine restituito dall'API (es. CREATED/PROCESSING/...)
                api_status = api_resp.get("status", "") or "UNKNOWN"

                # Filename del JSON salvato (se disponibile)
                order_filename = ""
                if i < len(saved_files) and saved_files[i]:
                    order_filename = Path(saved_files[i]).name

                row["order_name"] = order_filename
                row["status"] = api_status
                updated += 1
            else:
                code = item.get("code")
                row["status"] = f"ERROR{f'[{code}]' if code else ''}"
                # order_name resta vuoto
                errors += 1

        # Riscrivi CSV
        fieldnames = ["archiveId", "order_name", "status", "isImageDownloaded"]
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)

        print(f"CSV aggiornato: {csv_path} (updated={updated}, errors={errors})")
        return {"updated": updated, "errors": errors}

