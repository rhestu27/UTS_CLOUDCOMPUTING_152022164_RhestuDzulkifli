from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# Tentukan folder tempat gambar disimpan
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Anda dapat mengganti path sesuai kebutuhan

# Koneksi ke database MySQL pada RDS
def get_db_connection():
    conn = mysql.connector.connect(
        host='rm-gs5ofd1go25r2c525vo.mysql.singapore.rds.aliyuncs.com',  # Ganti dengan endpoint RDS Anda
        user='rhestu_tugas2',  # Ganti dengan username Anda
        password='restucs27!',  # Ganti dengan password Anda
        database='ecommerce',   # Ganti dengan nama database Anda
        ssl_ca='/path/to/ssl/ApsaraDB-CA-Chain.pem'  # Ganti dengan path ke sertifikat SSL Anda
    )
    return conn

# Route untuk menampilkan produk
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM produk1')  # Ganti dengan nama tabel yang sesuai di database Anda
    produk = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', produk=produk)

# Route untuk menambah produk
@app.route('/tambah_produk', methods=['GET', 'POST'])
def tambah_produk():
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        gambar_url = request.form['gambar_url'] if request.form['gambar_url'] else None  # Mengambil URL gambar jika ada
        stok = request.form['stok']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO produk1 (nama, harga, gambar_url, stok) VALUES (%s, %s, %s, %s)', (nama, harga, gambar_url, stok))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('index'))

    return render_template('tambah_produk.html')


# Route untuk menghapus produk
@app.route('/hapus_produk/<int:id>', methods=['GET'])
def hapus_produk(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Menghapus gambar produk jika ada
    cursor.execute('SELECT gambar_url FROM produk1 WHERE id = %s', (id,))
    gambar_url = cursor.fetchone()
    if gambar_url and gambar_url[0]:
        # Menghapus gambar dari folder
        path = os.path.join(app.config['UPLOAD_FOLDER'], gambar_url[0].split('/')[-1])
        if os.path.exists(path):
            os.remove(path)
    
    # Menghapus produk dari database
    cursor.execute('DELETE FROM produk1 WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
