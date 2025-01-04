from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'muhammadfarrellrabbani'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud'
mysql = MySQL(app)

# Utility function for database queries
def query_db(query, args=(), one=False, commit=False):
    with mysql.connection.cursor() as cursor:
        cursor.execute(query, args)
        if commit:
            mysql.connection.commit()
            return None
        result = cursor.fetchone() if one else cursor.fetchall()
    return result

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')
        action = request.form.get('action')

        if action == 'login':
            user = query_db('SELECT * FROM akun WHERE email = %s AND password = %s', (email, password), one=True)
            if user:
                flash('Login successful!', 'success')
                return redirect(url_for('mahasiswa'))
            flash('Invalid credentials. Please try again.', 'danger')

        elif action == 'signUp':
            return redirect(url_for('signUp'))

    return render_template('login.html')

# Sign-up route
@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')

        if query_db('SELECT * FROM akun WHERE email = %s', (email,), one=True):
            flash('Email already exists. Please log in.', 'danger')
            return redirect(url_for('login'))

        query_db('INSERT INTO akun (email, password) VALUES (%s, %s)', (email, password), commit=True)
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Mahasiswa page route
@app.route('/mahasiswa', methods=['GET', 'POST'])
def mahasiswa():
    mahasiswa_data = query_db('SELECT * FROM mahasiswa')
    return render_template('mahasiswa.html', mahasiswa=mahasiswa_data)

# Mata kuliah routes
@app.route('/mahasiswa/mata_kuliah')
def matakuliah():
    mata_kuliah_data = query_db('SELECT * FROM mata_kuliah')
    return render_template('mata_kuliah.html', mata_kuliah=mata_kuliah_data)

@app.route('/mahasiswa/mata_kuliah/tambah', methods=['GET', 'POST'])
def tambahMataKuliah():
    if request.method == 'POST':
        kode_matkul = request.form['kodematkul']
        nama_matkul = request.form['matkul']
        fakultas = request.form['fakultas']
        sks = request.form['sks']

        if not all([kode_matkul, nama_matkul, fakultas, sks]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('tambahMataKuliah'))

        query_db(
            'INSERT INTO mata_kuliah (kode_matkul, nama_mk, fakultas, sks) VALUES (%s, %s, %s, %s)',
            (kode_matkul, nama_matkul, fakultas, sks),
            commit=True
        )
        flash('Mata kuliah added successfully!', 'success')
        return redirect(url_for('matakuliah'))

    return render_template('tambah_mata_kuliah.html')

@app.route('/mahasiswa/mata_kuliah/edit/<int:kode_matkul>', methods=['GET', 'POST'])
def editMataKuliah(kode_matkul):
    if request.method == 'POST':
        kode_matkul_new = request.form['kodematkul']
        nama_matkul = request.form['matkul']
        fakultas = request.form['fakultas']
        sks = request.form['sks']

        query_db(
            'UPDATE mata_kuliah SET kode_matkul = %s, nama_mk = %s, fakultas = %s, sks = %s WHERE kode_matkul = %s',
            (kode_matkul_new, nama_matkul, fakultas, sks, kode_matkul),
            commit=True
        )
        flash('Mata kuliah updated successfully!', 'success')
        return redirect(url_for('matakuliah'))

    mata_kuliah = query_db('SELECT * FROM mata_kuliah WHERE kode_matkul = %s', (kode_matkul,), one=True)
    if mata_kuliah:
        return render_template('edit_mata_kuliah.html', mata_kuliah=mata_kuliah)
    return "Mata kuliah not found."

@app.route('/matakuliah/delete/<int:kode_matkul>', methods=['POST','GET'])
def deleteMataKuliah(kode_matkul):
    if request.method == 'GET':
        # Handle GET request to show confirmation page
        mahasiswa = query_db('SELECT * FROM mata_kuliah WHERE kode_matkul = %s', (kode_matkul,))
        if not mahasiswa:
            flash('Matakuliah tidak ditemukan!', 'danger')
            return redirect(url_for('matakuliah'))
        return render_template('hapus_matkul.html', kode_matkul=kode_matkul)
    elif request.method == 'POST':
        # Handle POST request to perform deletion
        query_db('DELETE FROM mata_kuliah WHERE kode_matkul = %s', (kode_matkul,), commit=True)
        flash('Mata kuliah dihapus!', 'success')
        return redirect(url_for('matakuliah'))


# Add, edit, delete mahasiswa routes
@app.route('/mahasiswa/tambah', methods=['GET', 'POST'])
def tambahMahasiswa():
    if request.method == 'POST':
        nama = request.form['namamahasiswa']
        npm = request.form['npmmahasiswa']
        jurusan = request.form['jurusanmahasiswa']

        if not all([nama, npm]):
            flash('Name and NPM are required.', 'danger')
            return redirect(url_for('tambahMahasiswa'))

        if query_db('SELECT * FROM mahasiswa WHERE npm = %s', (npm,), one=True):
            flash('NPM already exists!', 'danger')
            return redirect(url_for('tambahMahasiswa'))

        query_db(
            'INSERT INTO mahasiswa (nama, npm, jurusan) VALUES (%s, %s, %s)',
            (nama, npm, jurusan),
            commit=True
        )
        flash('Mahasiswa added successfully!', 'success')
        return redirect(url_for('mahasiswa'))

    return render_template('tambah_mahasiswa.html')

@app.route('/mahasiswa/edit/<int:npm>', methods=['GET', 'POST'])
def editMahasiswa(npm):
    if request.method == 'POST':
        nama = request.form['namamahasiswa']
        npm_new = request.form['npmmahasiswa']
        jurusan = request.form['jurusanmahasiswa']

        query_db(
            'UPDATE mahasiswa SET nama = %s, npm = %s, jurusan = %s WHERE npm = %s',
            (nama, npm_new, jurusan, npm),
            commit=True
        )
        flash('Mahasiswa updated successfully!', 'success')
        return redirect(url_for('mahasiswa'))

    mahasiswa = query_db('SELECT * FROM mahasiswa WHERE npm = %s', (npm,), one=True)
    if mahasiswa:
        return render_template('edit_mahasiswa.html', mahasiswa=mahasiswa)
    return "Mahasiswa not found."

@app.route('/mahasiswa/delete/<int:npm>', methods=['POST', 'GET'])
def deleteMahasiswa(npm):
    if request.method == 'GET':
        # Handle GET request to show confirmation page
        mahasiswa = query_db('SELECT * FROM mahasiswa WHERE npm = %s', (npm,))
        if not mahasiswa:
            flash('Mahasiswa not found!', 'danger')
            return redirect(url_for('mahasiswa'))
        return render_template('hapus_mahasiswa.html', mahasiswa=mahasiswa[0], npm=npm)
    elif request.method == 'POST':
        # Handle POST request to perform deletion
        query_db('DELETE FROM mahasiswa WHERE npm = %s', (npm,), commit=True)
        flash('Mahasiswa deleted successfully!', 'success')
        return redirect(url_for('mahasiswa'))


if __name__ == '__main__':
    app.run(debug=True, port=3000)
