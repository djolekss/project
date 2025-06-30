from flask import Blueprint, render_template, session, redirect, url_for, request
from db import connect, cursor
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')



@admin_bp.route('/')
def admin_dashboard():
    if 'is_admin' not in session or not session['is_admin']:
        return redirect(url_for('login'))
    
    cursor.execute("SELECT COUNT(*) FROM korisnici")
    broj_korisnika = cursor.fetchone()
    connect.commit()

    cursor.execute("SELECT COUNT(*) FROM zivotinje")
    broj_zivotinja = cursor.fetchone()
    connect.commit()

    cursor.execute("SELECT COUNT(*) FROM termini WHERE status = 'na čekanju'")
    termini_na_cekanju = cursor.fetchone()
    connect.commit()

    cursor.execute("""SELECT zivotinje.zivotinja_id, concat(korisnici.ime, ' ', korisnici.prezime) as 'Puni ime', zivotinje.vrsta, zivotinje.rasa, zivotinje.datum_rodjenja
                        FROM zivotinje
                        JOIN korisnici ON zivotinje.korisnik_id = korisnici.korisnik_id""")
    zivotinje = cursor.fetchall()
    connect.commit()

    cursor.execute("SELECT korisnik_id, ime, prezime, email, password FROM korisnici")
    korisnici = cursor.fetchall()
    connect.commit()

    cursor.execute("""SELECT termini.termin_id, concat(korisnici.ime, ' ', korisnici.prezime), concat(veterinari.ime, ' ', veterinari.prezime), termini.datum, termini.vreme, termini.opis, termini.status
                        FROM termini
                        JOIN korisnici ON termini.korisnik_id = korisnici.korisnik_id
                        JOIN veterinari ON termini.veterinar_id = veterinari.veterinar_id
                        """)
    termini = cursor.fetchall()
    connect.commit()

    cursor.execute("SELECT COUNT(*) FROM poruke WHERE status = 'nepročitano'")
    broj_neprocitanih = cursor.fetchone()[0]
    connect.commit()

    return render_template('admin-panel.html', broj_korisnika = broj_korisnika, broj_zivotinja = broj_zivotinja, termini_na_cekanju = termini_na_cekanju, korisnici = korisnici, zivotinje = zivotinje, termini = termini, broj_neprocitanih = broj_neprocitanih)

@admin_bp.route('/izbrisi/<int:korisnik_id>')
def izbrisi(korisnik_id):
    if 'is_admin' not in session or not session['is_admin']:
        return redirect(url_for('login'))
    
    cursor.execute("DELETE FROM korisnici WHERE korisnik_id = %s", (korisnik_id,))
    connect.commit()
    return redirect('/admin')

@admin_bp.route('/azuriraj/<int:korisnik_id>', methods = ['GET', 'POST'])
def azuriraj(korisnik_id):
    if 'is_admin' not in session or not session['is_admin']:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        ime = request.form['ime']
        prezime = request.form['prezime']
        email = request.form['email']

        cursor.execute("""UPDATE korisnici
                            SET ime = %s, prezime = %s, email = %s
                            WHERE korisnik_id = %s""", (ime, prezime, email, korisnik_id))
        connect.commit()
        return redirect('/admin')

    cursor.execute("SELECT * FROM korisnici WHERE korisnik_id = %s", (korisnik_id, ))
    korisnik = cursor.fetchone()

    return render_template('admin-azuriraj-korisnika.html', korisnik = korisnik)

@admin_bp.route('/odbij/<int:termin_id>')
def odbij(termin_id):
    if 'is_admin' not in session or not session['is_admin']:
        return redirect(url_for('login'))

    cursor.execute("""SELECT korisnici.email FROM korisnici 
                      JOIN termini ON korisnici.korisnik_id = termini.korisnik_id
                      WHERE termini.termin_id = %s""", (termin_id, ))

    rezultat = cursor.fetchone()

    if rezultat:
        primalac = rezultat[0]
    else:
        primalac = None

    cursor.execute("UPDATE termini SET status = 'odbijeno' WHERE termin_id = %s", (termin_id, ))
    connect.commit()

    if primalac:
        posalji_email(
            primalac,
            "Vaš termin je odbijen",
            "Poštovani, vaš termin je ODBIJEN. Molimo vas da zakažete novi termin ili nas kontaktirate za više informacija."
        )

    return redirect('/admin')

@admin_bp.route('/odobri/<int:termin_id>')
def odobri(termin_id):
    if 'is_admin' not in session or not session['is_admin']:
        return redirect(url_for('login'))
   
    cursor.execute("""SELECT korisnici.email FROM korisnici 
                      JOIN termini ON korisnici.korisnik_id = termini.korisnik_id
                      WHERE termini.termin_id = %s""", (termin_id, ))
   
    rezultat = cursor.fetchone()
   
    if rezultat:
        primalac = rezultat[0]
    else:
        primalac = None

    cursor.execute("UPDATE termini SET status = 'zakazano' WHERE termin_id = %s", (termin_id, ))
    connect.commit()

    if primalac:
        posalji_email(
            primalac,
            "Vaš termin je odobren",
            "Poštovani, vaš termin je ODOBREN. Vidimo se uskoro!"
        )

    return redirect('/admin')

@admin_bp.route('/dodaj_veterinara', methods = ['GET', 'POST'])
def dodaj_veterinara():
    if 'is_admin' not in session or not session['is_admin']:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        ime = request.form['ime']
        prezime = request.form['prezime']
        email = request.form['email']
        specijalizacija = request.form['specijalizacija']

        cursor.execute("""INSERT INTO veterinari(ime, prezime, email, specijalizacija)
                            VALUES(%s, %s, %s, %s)""", (ime, prezime, email, specijalizacija))
        connect.commit()

    return render_template('dodaj_veterinara.html')

@admin_bp.route('/poruke')
def poruke():
    if 'is_admin' not in session or not session['is_admin']:
        return redirect(url_for('login'))

    cursor.execute("""
        SELECT * FROM poruke
            ORDER BY 
            CASE WHEN status = 'nepročitano' THEN 0 ELSE 1 END,
            poslato DESC
    """)
    poruke = cursor.fetchall()
    connect.commit()

    return render_template('poruke.html', poruke=poruke)

@admin_bp.route('/poruke/<int:poruka_id>')
def poruka_otvori(poruka_id):
    if 'is_admin' not in session or not session['is_admin']:
        return redirect(url_for('login'))

    cursor.execute("""
        UPDATE poruke SET status = 'pročitano' WHERE poruka_id = %s
    """, (poruka_id,))
    connect.commit()

    cursor.execute("""
        SELECT * FROM poruke WHERE poruka_id = %s
    """, (poruka_id,))
    poruka = cursor.fetchone()

    if not poruka:
        return redirect(url_for('admin.poruke'))

    return render_template('pregled_poruke.html', poruka=poruka)

@admin_bp.route('/dodaj_zivotinju', methods = ['GET', 'POST'])
def dodaj_zivotinju():
    if 'is_admin' not in session or not session['is_admin']:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        email = request.form['email']
        vrsta = request.form['vrsta']
        rasa = request.form['rasa']
        ime = request.form['ime']
        datum = request.form['datum_rodjenja']

        cursor.execute("SELECT korisnik_id FROM korisnici WHERE email = %s", (email, ))
        korisnik_id = cursor.fetchone()
        connect.commit()

        if korisnik_id:
            cursor.execute("""INSERT INTO zivotinje(korisnik_id, vrsta, rasa, ime, datum_rodjenja)
			VALUES(%s, %s, %s, %s, %s)""", (korisnik_id[0], vrsta, rasa, ime, datum))
            connect.commit()

            return redirect('/admin')
        
    return render_template('dodaj_zivotinju.html')

@admin_bp.route('/izvrsi/<int:termin_id>', methods=['GET', 'POST'])
def izvrsi(termin_id):
    if 'is_admin' not in session or not session['is_admin']:
        return redirect(url_for('login'))

    if request.method == 'POST':
        dijagnoza = request.form['dijagnoza']
        terapija = request.form['terapija']
        ime_zivotinje = request.form['ime_zivotinje']

        cursor.execute("""
            SELECT korisnik_id FROM termini WHERE termin_id = %s
        """, (termin_id,))
        korisnik = cursor.fetchone()
        if not korisnik:
            return redirect('/admin')

        korisnik_id = korisnik[0]

        cursor.execute("""
            SELECT zivotinja_id FROM zivotinje
            WHERE ime = %s AND korisnik_id = %s
        """, (ime_zivotinje, korisnik_id))
        zivotinja = cursor.fetchone()

        if not zivotinja:
            return "Životinja nije pronađena za datog korisnika.", 400

        zivotinja_id = zivotinja[0]

        from datetime import datetime
        cursor.execute("""
            INSERT INTO istorija_bolesti (termin_id, zivotinja_id, vreme_pregleda, dijagnoza, terapija)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            termin_id,
            zivotinja_id,
            datetime.now(),
            dijagnoza,
            terapija
        ))
        
        connect.commit()

        cursor.execute("""
            UPDATE termini SET status = 'izvršeno' WHERE termin_id = %s
        """, (termin_id,))

        connect.commit()

        return redirect('/admin')

    cursor.execute("""
        SELECT 
            termini.termin_id,
            CONCAT(korisnici.ime, ' ', korisnici.prezime) AS korisnik,
            CONCAT(veterinari.ime, ' ', veterinari.prezime) AS veterinar,
            termini.datum,
            termini.vreme,
            termini.opis,
            korisnici.korisnik_id
            FROM termini
            JOIN korisnici ON termini.korisnik_id = korisnici.korisnik_id
            JOIN veterinari ON termini.veterinar_id = veterinari.veterinar_id
            WHERE termini.termin_id = %s """, (termin_id,))
    
    termin_info = cursor.fetchone()

    if not termin_info:
        return redirect(url_for('admin.odbij'))

    return render_template("izvrsi.html", termin=termin_info)

@admin_bp.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('login'))

def posalji_email(primalac, subject, poruka):
    email_adresa = "djordjedavidovic00@gmail.com"
    lozinka = "grrh ojix yrdy tfxu"  

    msg = MIMEMultipart()
    msg['From'] = email_adresa
    msg['To'] = primalac
    msg['Subject'] = subject
    msg.attach(MIMEText(poruka, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_adresa, lozinka)
        server.send_message(msg)
        server.quit()
        print("Mejl je poslat")
    except Exception as e:
        print("Greška prilikom slanja mejla:", e)