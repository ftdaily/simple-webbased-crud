from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'muhammadfarrellrabbani'

# Configure MySQL database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud'

# Initialize MySQL
mysql = MySQL(app)

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')
        action = request.form.get('action')  

        # if not email or not password:
        #     flash('Email and Password cannot be empty.', 'danger')
        #     return redirect(url_for('login'))

        if action == 'login':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM akun WHERE email = %s AND password = %s', (email, password))
            user = cursor.fetchone()
            cursor.close()
            if user:
                flash('Login successful!', 'success')
                return redirect(url_for('mahasiswa')) 
            else:
                flash('Invalid credentials. Please try again.', 'danger')
                return redirect(url_for('login'))

        elif action == 'signUp':  # Redirect to sign up page
            return redirect(url_for('signUp'))

    return render_template('login.html')

# Sign-up route
@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')

        # if not email or not password:
        #     flash('Email and Password cannot be empty.', 'danger')
        #     return redirect(url_for('signUp'))

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM akun WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user:
            flash('Email already exists. Please log in.', 'danger')
            cursor.close()
            return redirect(url_for('login'))
        else:
            cursor.execute('INSERT INTO akun (email, password) VALUES (%s, %s)', (email, password))
            mysql.connection.commit()
            cursor.close()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        
        if action == 'back':
            return redirect(url_for('login'))

    return render_template('signup.html')



# ================================================================
# Mahasiswa page route
@app.route('/mahasiswa', methods=['POST', 'GET'])
def mahasiswa():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM mahasiswa')
    mahasiswa = cursor.fetchall()
    cursor.close()
    
    if request.method == 'POST':
        if action == 'buttonTambahMahasiswa':
            return redirect(url_for('tambahMahasiswa'))
    
    return render_template('mahasiswa.html', mahasiswa=mahasiswa)

# Mata kuliah page route
@app.route('/mahasiswa/mata_kuliah')
def matakuliah():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM mata_kuliah')
    mata_kuliah = cursor.fetchall()
    cursor.close()
    return render_template('mata_kuliah.html', mata_kuliah=mata_kuliah)

# Add new mata kuliah route
@app.route('/mahasiswa/mata_kuliah/tambah', methods=['GET', 'POST'])
def tambahMataKuliah():
    if request.method == 'POST':
        # Get user input
        kode_matakuliah = request.form['kodematkul']
        nama_matakuliah = request.form['matkul']
        fakultas = request.form['fakultas']
        sks = request.form['sks']
        
        if not kode_matakuliah or not nama_matakuliah or not fakultas or not sks:
            flash('NPM and Name cannot be empty.', 'danger')
            return redirect(url_for('tambahMataKuliah'))

        # Insert data into database
        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO mata_kuliah (kode_matkul, nama_mk, fakultas, sks) VALUES (%s, %s, %s, %s)',
            (kode_matakuliah, nama_matakuliah, fakultas, sks)
        )
        mysql.connection.commit()
        cursor.close()

        return redirect('/mahasiswa/mata_kuliah')
    return render_template('tambah_mata_kuliah.html')

# Edit mata kuliah route
@app.route('/mahasiswa/mata_kuliah/edit/<int:kode_matkul>', methods=['GET', 'POST'])
def editMataKuliah(kode_matkul):
    if request.method == 'POST':
        # Get updated data
        kode_matakuliah = request.form['kodematkul']
        nama_matakuliah = request.form['matkul']
        fakultas = request.form['fakultas']
        sks = request.form['sks']

        # Update data in database
        cursor = mysql.connection.cursor()
        cursor.execute(
            'UPDATE mata_kuliah SET kode_matkul = %s, nama_mk = %s, fakultas = %s, sks = %s WHERE kode_matkul = %s',
            (kode_matakuliah, nama_matakuliah, fakultas, sks, kode_matkul)
        )
        mysql.connection.commit()
        cursor.close()

        return redirect('/mahasiswa/mata_kuliah')
    else:
        # Fetch data to edit
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM mata_kuliah WHERE kode_matkul = %s', (kode_matkul,))
        mata_kuliah = cursor.fetchone()
        cursor.close()

        if mata_kuliah:
            return render_template('edit_mata_kuliah.html', mata_kuliah=mata_kuliah)
        return "Mata kuliah not found."

# Delete mata kuliah route
@app.route('/matakuliah/delete/<int:kode_matkul>', methods=['GET', 'POST'])
def deleteMataKuliah(kode_matkul):
    if request.method == 'POST':
        # Delete data from database
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM mata_kuliah WHERE kode_matkul = %s', (kode_matkul,))
        mysql.connection.commit()
        cursor.close()

        flash('Mata kuliah berhasil dihapus', 'success')
        return redirect(url_for('matakuliah'))
    return render_template('hapus_matkul.html', kode_matkul=kode_matkul)

# ================================================================

@app.route('/mahasiswa/tambah', methods=['GET', 'POST'])
def tambahMahasiswa():
    if request.method == 'POST':
        # Get user input
        namamahasiswa = request.form['namamahasiswa']
        npmmahasiswa = request.form['npmmahasiswa']
        jurusanmahasiswa = request.form['jurusanmahasiswa']

        if not npmmahasiswa or not namamahasiswa:
            flash('NPM and Name cannot be empty.', 'danger')
            return redirect(url_for('tambahMahasiswa'))

        # Check for duplicate NPM
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM mahasiswa WHERE npm = %s', (npmmahasiswa,)) 
        npmDuplikat = cursor.fetchone()
        cursor.close()

        if npmDuplikat:
            # If duplicate NPM exists, flash an error message
            flash('Gunakan NPM yang berbeda!', 'danger')
            return redirect(url_for('tambahMahasiswa'))

        # Insert data into database
        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO mahasiswa (nama, npm, jurusan) VALUES (%s, %s, %s)',
            (namamahasiswa, npmmahasiswa, jurusanmahasiswa)
        )
        mysql.connection.commit()
        cursor.close()

        flash('Mahasiswa berhasil ditambahkan!', 'success')
        return redirect(url_for('mahasiswa'))

    return render_template('tambah_mahasiswa.html')

# Edit data mahasiswa route
@app.route('/mahasiswa/edit/<int:npm>', methods=['GET', 'POST'])
def editMahasiswa(npm):
    if request.method == 'POST':
        # Get updated data
        namamahasiswa = request.form['namamahasiswa']
        npmmahasiswa = request.form['npmmahasiswa']
        jurusanmahasiswa = request.form['jurusanmahasiswa']

        if not jurusanmahasiswa or not namamahasiswa or not npmmahasiswa:
            return redirect('/mahasiswa')

            
        # Update data in database
        cursor = mysql.connection.cursor()
        cursor.execute(
            'UPDATE mahasiswa SET jurusan = %s, nama = %s, npm = %s WHERE npm = %s',
            (jurusanmahasiswa, namamahasiswa, npmmahasiswa, npm)
        )
        mysql.connection.commit()
        cursor.close()
        return redirect('/mahasiswa')
    else:
        # Fetch data to edit
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM mahasiswa WHERE npm = %s', (npm,))
        mata_kuliah = cursor.fetchone()
        cursor.close()

        if mata_kuliah:
            return render_template('edit_mahasiswa.html', npm=npm)
        return "Mahasiswa tidak ditemukan."

# Delete data mahasiswa route
@app.route('/mahasiswa/delete/<int:npm>', methods=['GET', 'POST'])
def deleteMahasiswa(npm):
    if request.method == 'POST':
        # Perform the deletion
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM mahasiswa WHERE npm = %s', (npm,))
        mysql.connection.commit()
        cursor.close()

        flash('Data Mahasiswa berhasil dihapus', 'success')
        return redirect(url_for('mahasiswa'))

    # Render the confirmation page
    return render_template('hapus_mahasiswa.html', npm=npm)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
