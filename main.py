# Import library yang diperlukan
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mysqldb import MySQL

# Inisialisasi aplikasi Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'muhammadfarrellrabbani'  # Kunci untuk session dan flash messages

# Konfigurasi koneksi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Kata sandi untuk MySQL
app.config['MYSQL_DB'] = 'crud'  # Nama database yang digunakan
mysql = MySQL(app)  # Inisialisasi koneksi ke MySQL

# Fungsi utilitas untuk menjalankan query ke database
def query_db(query, args=(), one=False, commit=False):
    # Menggunakan cursor untuk eksekusi query
    with mysql.connection.cursor() as cursor:
        cursor.execute(query, args)
        if commit:
            # Jika operasi commit, simpan perubahan ke database
            mysql.connection.commit()
            return None
        result = cursor.fetchone() if one else cursor.fetchall()
    return result

# Rute login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')
        action = request.form.get('action')

        if action == 'login':
            # Memeriksa kecocokan email dan password
            user = query_db('SELECT * FROM akun WHERE email = %s AND password = %s', (email, password), one=True)
            if user:
                flash('Login berhasil!', 'success')
                return redirect(url_for('mahasiswa'))
            flash('Email atau password salah. Silakan coba lagi.', 'danger')

        elif action == 'signUp':
            return redirect(url_for('signUp'))

    return render_template('login.html')

# Rute untuk pendaftaran akun
@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')

        # Memeriksa apakah email sudah terdaftar
        if query_db('SELECT * FROM akun WHERE email = %s', (email,), one=True):
            flash('Email sudah terdaftar. Silakan login.', 'danger')
            return redirect(url_for('login'))

        # Menyimpan data akun baru
        query_db('INSERT INTO akun (email, password) VALUES (%s, %s)', (email, password), commit=True)
        flash('Akun berhasil dibuat! Silakan login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Rute untuk halaman mahasiswa
@app.route('/mahasiswa', methods=['GET', 'POST'])
def mahasiswa():
    mahasiswa_data = query_db('SELECT * FROM mahasiswa')
    return render_template('mahasiswa.html', mahasiswa=mahasiswa_data)

# Rute untuk mata kuliah
@app.route('/mahasiswa/mata_kuliah')
def matakuliah():
    mata_kuliah_data = query_db('SELECT * FROM mata_kuliah')
    return render_template('mata_kuliah.html', mata_kuliah=mata_kuliah_data)

# Rute untuk menambah mata kuliah
@app.route('/mahasiswa/mata_kuliah/tambah', methods=['GET', 'POST'])
def tambahMataKuliah():
    if request.method == 'POST':
        kode_matkul = request.form['kodematkul']
        nama_matkul = request.form['matkul']
        fakultas = request.form['fakultas']
        sks = request.form['sks']

        # Memeriksa apakah semua field sudah diisi
        if not all([kode_matkul, nama_matkul, fakultas, sks]):
            flash('Semua kolom harus diisi.', 'danger')
            return redirect(url_for('tambahMataKuliah'))

        # Menambah mata kuliah ke database
        query_db(
            'INSERT INTO mata_kuliah (kode_matkul, nama_mk, fakultas, sks) VALUES (%s, %s, %s, %s)',
            (kode_matkul, nama_matkul, fakultas, sks),
            commit=True
        )
        flash('Mata kuliah berhasil ditambahkan!', 'success')
        return redirect(url_for('matakuliah'))

    return render_template('tambah_mata_kuliah.html')

# Rute untuk mengedit mata kuliah
@app.route('/mahasiswa/mata_kuliah/edit/<int:kode_matkul>', methods=['GET', 'POST'])
def editMataKuliah(kode_matkul):
    if request.method == 'POST':
        # Mengambil data dari form untuk update mata kuliah
        kode_matkul_new = request.form.get('kodematkul')
        nama_matkul = request.form.get('matkul')
        fakultas = request.form.get('fakultas')
        sks = request.form.get('sks')

        # Persiapkan query untuk update data
        query = 'UPDATE mata_kuliah SET '
        params = []

        # Menambahkan field yang diubah ke query
        if kode_matkul_new:
            query += 'kode_matkul = %s, '
            params.append(kode_matkul_new)
        if nama_matkul:
            query += 'nama_mk = %s, '
            params.append(nama_matkul)
        if fakultas:
            query += 'fakultas = %s, '
            params.append(fakultas)
        if sks:
            query += 'sks = %s, '
            params.append(sks)

        # Menghapus koma terakhir dan menambahkan kondisi WHERE
        query = query.rstrip(', ') + ' WHERE kode_matkul = %s'
        params.append(kode_matkul)

        # Menjalankan query untuk update
        query_db(query, tuple(params), commit=True)

        flash('Mata kuliah berhasil diperbarui!', 'success')
        return redirect(url_for('matakuliah'))

    mata_kuliah = query_db('SELECT * FROM mata_kuliah WHERE kode_matkul = %s', (kode_matkul,), one=True)
    if mata_kuliah:
        return render_template('edit_mata_kuliah.html', mata_kuliah=mata_kuliah)
    return "Mata kuliah tidak ditemukan."

# Rute untuk menghapus mata kuliah
@app.route('/matakuliah/delete/<int:kode_matkul>', methods=['POST','GET'])
def deleteMataKuliah(kode_matkul):
    if request.method == 'GET':
        # Menampilkan halaman konfirmasi sebelum menghapus
        mahasiswa = query_db('SELECT * FROM mata_kuliah WHERE kode_matkul = %s', (kode_matkul,))
        if not mahasiswa:
            flash('Mata kuliah tidak ditemukan!', 'danger')
            return redirect(url_for('matakuliah'))
        return render_template('hapus_matkul.html', kode_matkul=kode_matkul)
    elif request.method == 'POST':
        # Menghapus mata kuliah dari database
        query_db('DELETE FROM mata_kuliah WHERE kode_matkul = %s', (kode_matkul,), commit=True)
        flash('Mata kuliah dihapus!', 'success')
        return redirect(url_for('matakuliah'))

# Rute untuk menambah mahasiswa
@app.route('/mahasiswa/tambah', methods=['GET', 'POST'])
def tambahMahasiswa():
    if request.method == 'POST':
        nama = request.form['namamahasiswa']
        npm = request.form['npmmahasiswa']
        jurusan = request.form['jurusanmahasiswa']

        # Memeriksa kelengkapan data mahasiswa
        if not all([nama, npm]):
            flash('Nama dan NPM harus diisi.', 'danger')
            return redirect(url_for('tambahMahasiswa'))

        if query_db('SELECT * FROM mahasiswa WHERE npm = %s', (npm,), one=True):
            flash('NPM sudah ada!', 'danger')
            return redirect(url_for('tambahMahasiswa'))

        # Menambah mahasiswa baru ke database
        query_db(
            'INSERT INTO mahasiswa (nama, npm, jurusan) VALUES (%s, %s, %s)',
            (nama, npm, jurusan),
            commit=True
        )
        flash('Mahasiswa berhasil ditambahkan!', 'success')
        return redirect(url_for('mahasiswa'))

    return render_template('tambah_mahasiswa.html')

# Rute untuk mengedit data mahasiswa
@app.route('/mahasiswa/edit/<int:npm>', methods=['GET', 'POST'])
def editMahasiswa(npm):
    if request.method == 'POST':
        # Mengambil data form untuk mengupdate mahasiswa
        nama = request.form.get('namamahasiswa')
        npm_new = request.form.get('npmmahasiswa')
        jurusan = request.form.get('jurusanmahasiswa')

        # Update hanya data yang diubah
        if nama:
            query_db(
                'UPDATE mahasiswa SET nama = %s WHERE npm = %s',
                (nama, npm),
                commit=True
            )
        if npm_new:
            query_db(
                'UPDATE mahasiswa SET npm = %s WHERE npm = %s',
                (npm_new, npm),
                commit=True
            )
        if jurusan:
            query_db(
                'UPDATE mahasiswa SET jurusan = %s WHERE npm = %s',
                (jurusan, npm),
                commit=True
            )

        flash('Mahasiswa berhasil diperbarui!', 'success')
        return redirect(url_for('mahasiswa'))

    mahasiswa = query_db('SELECT * FROM mahasiswa WHERE npm = %s', (npm,), one=True)
    if mahasiswa:
        return render_template('edit_mahasiswa.html', mahasiswa=mahasiswa)
    return "Mahasiswa tidak ditemukan."

# Rute untuk menghapus mahasiswa
@app.route('/mahasiswa/delete/<int:npm>', methods=['POST', 'GET'])
def deleteMahasiswa(npm):
    if request.method == 'GET':
        # Menampilkan halaman konfirmasi sebelum menghapus mahasiswa
        mahasiswa = query_db('SELECT * FROM mahasiswa WHERE npm = %s', (npm,))
        if not mahasiswa:
            flash('Mahasiswa tidak ditemukan!', 'danger')
            return redirect(url_for('mahasiswa'))
        return render_template('hapus_mahasiswa.html', mahasiswa=mahasiswa[0], npm=npm)
    elif request.method == 'POST':
        # Menghapus mahasiswa dari database
        query_db('DELETE FROM mahasiswa WHERE npm = %s', (npm,), commit=True)
        flash('Mahasiswa berhasil dihapus!', 'success')
        return redirect(url_for('mahasiswa'))


# Menjalankan aplikasi Flask
if __name__ == '__main__':
    app.run(debug=True, port=3000)
