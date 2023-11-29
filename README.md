# EV-Thermal-Runaway-Prediction-ML
 This research was being funded by Indonesian Ministry of Research and Education on Program Kreativitas Mahasiswa Karya Cipta 2022. 

Program Kreativitas Mahasiswa - Karsa Cipta (PKM-KC 2022)
"Prediksi Pelarian Termal pada Battery Pack Mobil Listrik dengan Sistem Akuisisi Data Berbasis Machine Learning sebagai Upaya Peningkatan Keamanan Berkendara"

<img src="Dokumen Resmi/Dokumentasi Alat/foto_prototype.png" alt="Foto Prototype" width=400 />

Gambar 1. Foto Alat

## Our Team

<img src="Dokumen Resmi/Dokumentasi Alat/foto_setelah_pkp2.png" alt="Foto Setelah PKP2" width=400 />
<img src="Dokumen Resmi/Dokumentasi Alat/foto_ruang_pkp2.png" alt="Foto Ruang PKP2" width=400 />

ID Team: KC 2909 (Institut Teknologi Sepuluh Nopember)

Ketua Tim: Muhammad Rayhan Rafy

Pembimbing: Dr. Ir. Purwadi Agus Darwito, M.Sc. (Lab. Instrumentasi, Kontrol, dan Optimisasi - Teknik Fisika ITS)

Anggota:
1. Muhammad Faris Zuhairi
2. Ariel Jonathan
3. Frecia Elrivia Mardianto
4. Novandion Rafly Kurniawan

## Latar Belakang
Dalam sepuluh tahun terakhir, jumlah pengguna kendaraan listrik terus meningkat secara signifikan. Peningkatan penggunaan kendaraan listrik ini dipicu oleh pengembangan baterai lithium-ion (li-ion) yang merupakan jenis baterai yang paling banyak digunakan pada kendaraan listrik saat ini (Iclodean et al., 2017). Namun, penggunaan jenis baterai berenergi tinggi ini memiliki resiko masalah keamanan bagi kendaraan listrik karena potensi kebakaran yang tinggi, salah satunya adalah peristiwa pelarian termal.

Keadaan pelarian termal didefinisikan sebagai adanya defisit evakuasi energi jika dibandingkan dengan akumulasi energi dalam sel baterai. Pelarian termal dipicu oleh perlakuan tidak sesuai pada sistem mekanik, elektrik, atau termal baterai. (Chen et al., 2020). Kerusakan yang diakibatkan oleh pelarian termal baterai dapat membuat umur baterai menjadi singkat (Zhou et al., 2017). Pelarian termal dapat menghancurkan kestabilan struktur baterai. Hancurnya kestabilan struktur dari baterai ini dapat menimbulkan hal-hal berbahaya lain, seperti timbulnya gas beracun, kebakaran, atau bahkan ledakan (Ren et al., 2019). 

Beberapa teknologi telah dikembangkan untuk mencegah dan menanggulangi peristiwa serta akibar dari pelarian termal. Teknologi ini dikembangkan menggunakan metode yang beragam, mulai dari pemantauan menggunakan sensor gas sampai menggabungkan sensor resistance temperature detector (RTD) pada baterai li-ion. Kedua teknologi ini dikembangkan untuk menghindari kecelakaan akibat baterai li-ion yang terlalu panas. Akan tetapi, kedua teknologi ini  masih tergolong tidak efektif dalam mencegah kejadian pelarian termal karena pendeteksian pelarian termal yang cenderung terlambat serta prediksi yang tidak bisa diandalkan. (Liao et al., 2019).

Berdasarkan permasalahan tersebut, dapat disimpulkan bahwa harus dilakukan pemantauan beberapa parameter sel baterai setiap saat. Pemantauan ini dapat dilakukan dengan mengumpulkan data dan membentuk model prediksi karakteristik sistem baterai, yaitu temperatur, arus, dan tegangan sel. Nilai ini dikumpulkan untuk membentuk pola prediktif menggunakan algoritma machine learning. Fungsi prediktif yang dihasilkan dapat membantu mendeteksi potensi pelarian termal serta pengambilan aksi yang dapat dilakukan oleh sistem kendaraan ataupun pengendara.

## Rumusan Masalah
1.	Bagaimana cara merancang dan menciptakan alat yang mampu memprediksi peristiwa pelarian termal pada battery pack mobil listrik dengan sistem akuisisi data berbasis machine learning?
2.	Bagaimana cara meningkatkan keamanan penggunaan battery pack dalam mobil listrik?

## Tujuan
1.	Merancang dan menciptakan alat yang mampu memprediksi peristiwa pelarian termal pada battery pack mobil listrik dengan sistem akuisisi data berbasis machine learning?
2.	Meningkatkan sistem keamanan mobil listrik dengan penerapan alat prediksi peristiwa pelarian termal pada battery pak

## Progress Pengujian
<img src="Dokumen Resmi/Dokumentasi Alat/cara_kerja.png" alt="Diagram Cara Kerja Alat" width=400 />

Gambar 2. Diagram Cara Kerja Alat

Data dikumpulkan dari short circuit untuk data yang tergolong thermal runaway dan discharge baterai untuk non-thermal runaway. Keseluruhan data dibagi menjadi 80% data training dan 20% data testing. Terdapat 2 hidden layer yang dipakai dengan fungsi aktivasinya relu, dan satu output dengan aktivasi linear. Metriks performasi yang ditinjau adalah akurasi dan binary loss entropy. 
<img src="Dokumen Resmi/Dokumentasi Alat/loss_training_per_epoch.png" alt="Grafik loss training setiap epoch" width=400 />

Gambar 3 Grafik loss training setiap epoch

<img src="Dokumen Resmi/Dokumentasi Alat/accuracy_training_per_epoch.png" alt="Grafik akurasi training setiap epoch" width=400 />

Gambar 4 Grafik akurasi training setiap epoch

Hasil yang didapat adalah sangat baik, dimana semakin banyak epoch maka loss semakin kecil, sedangkan akurasi semakin meningkat. Nilainya steady pada sekitar epoch-10 dengan akurasi mampu mencapai 100%. Akurasi yang tinggi tidak mesti merepresentasikan model baik. Pertama, thermal runaway merupakan fenomena kompleks yang membutuhkan data variasi pada baterai yang beragam, sedangkan pada pengujian ini menggunakan satu jenis baterai dan perlakuan yang sama. Akurasi tinggi neural network dapat berarti model klasik dapat diterapkan, namun menjanjikan penggunaan data lebih variasi. Kedua, terjadi overfitting dimana data training yang digunakan merupakan data terbaik, sehingga jika diujikan dengan data lain akan menurunkan akurasi.

## Dokumentasi Video Presentasi
https://www.youtube.com/watch?v=blGbFs8lXC4&ab_channel=DirektoratKemahasiswaanITS
