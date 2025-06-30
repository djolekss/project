from flask import Flask, redirect, url_for, render_template, request, session
from db import connect, cursor
from flask import flash
import re
import hashlib

app = Flask(__name__)
app.secret_key = "dodjiPopeLjubimoTiStope"


from admin import admin_bp
app.register_blueprint(admin_bp)

@app.route('/')
def index():
    return render_template('index.html')

def hashLozinke(password):
    return hashlib.md5(password.encode()).hexdigest()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        ime = request.form['ime']
        prezime = request.form['prezime']
        email = request.form['email']
        password = request.form['password']

        if not re.match(r'^(?=.*[A-Z])(?=.*\d).+$', password):
             flash("Lozinka mora imati najmanje jedno veliko slovo i jedan broj.", "danger")
             return redirect('register')

        cursor.execute("SELECT * FROM korisnici WHERE email = %s", (email, ))
        korisnik = cursor.fetchone()
        
        if korisnik:
            flash("Email već postoji u bazi!", "danger")
            return redirect('register')

        hash_lozinka = hashLozinke(password)

        cursor.execute("INSERT INTO korisnici(ime, prezime, email, password) VALUES (%s, %s, %s, %s)", (ime, prezime, email, hash_lozinka))
        connect.commit()

        flash("Uspešno ste se registrovali!", "success")
        return redirect('login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        hash_lozinka = hashLozinke(password)

        cursor.execute("SELECT * FROM korisnici WHERE email = %s", (email,))
        korisnik = cursor.fetchone()

        if korisnik:
            if hash_lozinka == korisnik[4]:
                session['korisnik_id'] = korisnik[0]
                session['ime'] = korisnik[1]
                session['prezime'] = korisnik[2]
                session['is_admin'] = korisnik[5]

                if korisnik[5] == True:
                    return redirect('admin')
                return redirect('/')
            else:
                flash("Lozinka nije ispravna!", "danger")
                return redirect('login')
        else:
            flash("Korisnik nije registrovan!", "danger")
            return redirect('register')
    
    return render_template('login.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        telefon = request.form['telefon']
        poruka = request.form['poruka']

        cursor.execute("""INSERT INTO poruke(email, broj_telefona, poruka)
                            VALUES (%s, %s, %s)""", (email, telefon, poruka))
        connect.commit()
        flash("Uspešno ste poslali poruku!", "success")
        
    return render_template('contact.html')

@app.route('/profile', methods = ['GET','POST'])
def profile():
    if 'korisnik_id' not in session:
        return redirect('login')
    
    id = session['korisnik_id']

    cursor.execute("""SELECT zivotinje.zivotinja_id as 'Redni broj', korisnici.ime as 'Ime vlasnika', korisnici.prezime as 'Prezime vlasnika', 
                             zivotinje.vrsta as 'Vrsta', zivotinje.rasa as 'Rasa', zivotinje.ime as 'Ime životinje', zivotinje.datum_rodjenja as 'Datum rodjenja'
                      FROM zivotinje 
                      JOIN korisnici ON zivotinje.korisnik_id = korisnici.korisnik_id
                      WHERE korisnici.korisnik_id = %s""", (id, ))
    zivotinje = cursor.fetchall()

    cursor.execute("""
                        SELECT 
                            termini.termin_id AS 'ID',
                            CONCAT(korisnici.ime, ' ', korisnici.prezime) AS 'Vlasnik',
                            CONCAT(veterinari.ime, ' ', veterinari.prezime) AS 'Veterinar',
                            termini.datum,
                            termini.vreme,
                            termini.opis,
                            termini.status
                            FROM termini
                            JOIN korisnici ON termini.korisnik_id = korisnici.korisnik_id
                            JOIN veterinari ON termini.veterinar_id = veterinari.veterinar_id
                            WHERE korisnici.korisnik_id = %s
                            ORDER BY termini.datum DESC, termini.vreme DESC;""", (id, ))
    termini = cursor.fetchall()

    cursor.execute("SELECT * FROM korisnici WHERE korisnik_id = %s", (id, ))
    korisnik = cursor.fetchone()

    if request.method == 'POST':
        staraLozinka = request.form['password1']
        novaLozinka = request.form['password2']
        
        hash_lozinka_stara = hashLozinke(staraLozinka)
        hash_lozinka_nova = hashLozinke(novaLozinka)

        if hash_lozinka_stara == hash_lozinka_nova:
            flash("Lozinke ne mogu biti iste!", "danger")
            return redirect('profile')
        
        if hash_lozinka_stara != korisnik[4]:
            flash("Pogrešili ste staru lozinku!", "danger")
            return redirect('profile')
        
        cursor.execute("""UPDATE korisnici
                          SET password = %s
                          WHERE korisnik_id = %s""", (hash_lozinka_nova, id))
        
        connect.commit()

        flash("Uspešno ste promenili lozinku!", "success")
        return redirect('login')
    
    return render_template('profile.html', zivotinje = zivotinje, korisnik = korisnik, termini = termini)

@app.route("/zakazi", methods=["GET", "POST"])
def zakazi():
    if "korisnik_id" not in session:
        return redirect(url_for("login"))

    korisnik_id = session["korisnik_id"]

    cursor.execute("SELECT veterinar_id, CONCAT(ime, ' ', prezime, '-', specijalizacija) FROM veterinari")
    veterinari = cursor.fetchall()

    if request.method == "POST":
        veterinar_id = request.form["veterinar_id"]
        datum = request.form["datum"]
        vreme = request.form["vreme"]
        opis = request.form["opis"]

        cursor.execute("""
            SELECT * FROM termini
            WHERE datum = %s AND vreme = %s AND veterinar_id = %s""", (datum, vreme, veterinar_id))
        
        termin = cursor.fetchone()

        if termin:
            flash("Taj termin je već zauzet! Molimo izaberite drugo vreme.", "danger")
            return redirect(url_for("zakazi"))

        cursor.execute("""
            INSERT INTO termini (korisnik_id, veterinar_id, datum, vreme, opis)
            VALUES (%s, %s, %s, %s, %s)
        """, (korisnik_id, veterinar_id, datum, vreme, opis))

        connect.commit()

        flash("Uspešno ste poslali zahtev za termin!", "success")
        return redirect(url_for("profile"))

    return render_template("schedule.html", veterinari = veterinari)

@app.route('/istorija_bolesti')
def istorija_bolesti():
    if "korisnik_id" not in session:
        return redirect(url_for("login"))
    
    korisnik_id = session['korisnik_id']
    
    cursor.execute("""SELECT 
                        zivotinje.ime AS ime_zivotinje, 
                        istorija_bolesti.vreme_pregleda, 
                        istorija_bolesti.dijagnoza, 
                        istorija_bolesti.terapija
                        FROM istorija_bolesti
                        JOIN zivotinje ON istorija_bolesti.zivotinja_id = zivotinje.zivotinja_id
                        WHERE zivotinje.korisnik_id = %s
                        ORDER BY istorija_bolesti.vreme_pregleda DESC;""", (korisnik_id, ))
    
    istorija = cursor.fetchall()
    
    connect.commit()

    return render_template('istorija_bolesti.html', istorija = istorija)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('login')

if __name__ == '__main__':
    app.run(debug=True)