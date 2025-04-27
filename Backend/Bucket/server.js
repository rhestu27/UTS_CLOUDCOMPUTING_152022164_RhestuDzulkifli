// Import package
const express = require('express');
const mysql = require('mysql');

const app = express();
const port = 3000;

// Buat koneksi ke database
const db = mysql.createConnection({
  host: 'rm-gs5ofd1go25r2c525vo.mysql.singapore.rds.aliyuncs.com',
  user: 'rhestu_tugas2',
  password: 'restucs27!',
  database: 'ecommerce'
});

// Connect ke database
db.connect((err) => {
  if (err) {
    console.error('Database connection error:', err.stack);
    process.exit(1); // keluarin program kalau koneksi error
  }
  console.log('Connected to MySQL database!');
});

app.use(express.static(path.join(__dirname, '../frontend')));

// Route sederhana
app.get('/', (req, res) => {
  res.send('Server is running!');
});

// Route untuk contoh query data
app.get('/api/produk  ', (req, res) => {
  db.query('SELECT * FROM produk', (err, results) => {
    if (err) {
      console.error('Database query error:', err);
      res.status(500).send('Database query error');
      return;
    }
    res.json(results);
  });
});


// Jalankan server
app.listen(port, '0.0.0.0', () => {
  console.log(`Server berjalan di http://0.0.0.0:${port}`);
});
