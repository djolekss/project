# ZdravPaw – Veterinarska web aplikacija

ZdravPaw je web aplikacija razvijena kao praktičan zadatak po zahtevu profesora, sa ciljem da se prikaže razumevanje fullstack razvoja koristeći Flask i MySQL.

Aplikacija omogućava korisnicima da registruju svoje naloge, dodaju ljubimce, zakazuju preglede, dok administratori mogu upravljati terminima i unositi dijagnoze. Takođe sadrži poseban admin panel za upravljanje sistemom.

---

## 🛠️ Tehnologije

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, JavaScript (jQuery)
- **Baza podataka:** MySQL (baza: `zdravpaw3`)
- **Templating sistem:** Jinja2 (Flask `render_template`)

---

## 📋 Funkcionalnosti

### 🔐 Korisnici
- Registracija i prijava korisnika
- Prikaz korisničkog profila
- Odjava i zaštita ruta

### 🐾 Ljubimci
- Dodavanje ljubimaca korisniku
- Prikaz svih ljubimaca registrovanog korisnika

### 📅 Termini
- Zakazivanje termina za pregled
- Prikaz zakazanih termina po korisniku
- Administrator odobrava ili odbija termine

### 📋 Istorija bolesti
- Lekar unosi dijagnozu i terapiju nakon pregleda
- Pretraga po imenu ljubimca
- Čuvanje podataka o istoriji bolesti u bazi

### 👮 Admin panel
- Poseban `Blueprint` (`admin.py`) za administraciju
- Pregled svih termina
- Odobravanje i odbijanje termina od strane admina

---
