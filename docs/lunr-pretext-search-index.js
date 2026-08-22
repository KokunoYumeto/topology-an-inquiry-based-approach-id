var ptx_lunr_search_style = "textbook";
var ptx_lunr_docs = [
{
  "id": "o003-c90-ch07-edition-note",
  "level": "1",
  "url": "o003-c90-ch07-edition-note.html",
  "type": "Preface",
  "number": "",
  "title": "Catatan edisi Bahasa Indonesia",
  "body": " Catatan edisi Bahasa Indonesia  Unit pembaca kumulatif ini memuat tujuh bab pertama edisi Bahasa Indonesia Topology: An Inquiry-Based Approach . Sumber dibekukan pada commit resmi 0c2d8f614ef87aa00de373f3418146c2f1d13bb9 . Terjemahan, deskripsi aksesibilitas, perbaikan sumber yang dicatat, laboratorium epsilon-delta orisinal, dan pendamping belajar mandiri merupakan perubahan pada edisi ini; tidak ada dukungan resmi dari penulis atau Grand Valley State University yang dinyatakan ataupun tersirat.  Karya sumber diperlakukan secara konservatif menurut CC BY-NC-SA 3.0 karena metadata sumber tidak seragam tentang versi lisensi. Laboratorium dan materi pendamping baru merupakan komponen CC BY 4.0 yang terpisah dari turunan GVSU berlisensi CC BY-NC-SA 3.0. Kerjakan kegiatan dan latihan pada bab utama sebelum membuka petunjuk atau pembahasan pendamping.  "
},
{
  "id": "sec_sets_intro",
  "level": "1",
  "url": "sec_sets_intro.html",
  "type": "Bagian",
  "number": "",
  "title": "Pendahuluan",
  "body": " Pendahuluan  Pada tingkat paling mendasar, topologi membahas himpunan dan cara kita dapat mengubah bentuk suatu himpunan menjadi himpunan lain. Jadi, untuk memulai kajian kita tentang topologi, kita mulai dengan himpunan. Sebagian besar materi ini semestinya sudah tidak asing, tetapi beberapa bagian mungkin baru. Hal pertama yang perlu kita tetapkan adalah definisi himpunan yang setepat mungkin.    Andaikan kita mencoba mendefinisikan himpunan sebagai suatu kumpulan anggota. Jadi, menurut definisi tersebut, anggota adalah objek-objek yang terdapat di dalam himpunan. Kita menggunakan simbol untuk menyatakan bahwa suatu objek merupakan anggota suatu himpunan. Dengan demikian, berarti bahwa suatu objek bukan anggota himpunan tersebut jika merupakan anggota suatu himpunan , kita menulis , sedangkan jika bukan anggota himpunan , kita menulis . Kita menuliskan himpunan dengan kurung kurawal. Sebagai contoh, himpunan adalah himpunan yang anggotanya berupa simbol , , dan . Dalam notasi himpunan, kita juga dapat mencantumkan syarat yang harus dipenuhi oleh anggotanya. Sebagai contoh, adalah himpunan bilangan real positif. Biasanya kita menggunakan huruf kapital untuk menyatakan himpunan. Beberapa contoh himpunan yang sudah dikenal adalah , himpunan bilangan real; , himpunan bilangan rasional; dan , himpunan bilangan bulat. Suatu himpunan juga dapat memiliki himpunan sebagai anggotanya. Sebagai contoh, himpunan kuasa suatu himpunan adalah himpunan semua himpunan bagian dari . Jadi, himpunan kuasa dari adalah himpunan . (Kita akan mendefinisikan himpunan bagian dan himpunan kosong nanti dalam aktivitas ini).    Perhatikan himpunan  berikut, yang merupakan suatu kumpulan objek: . Dengan kata lain, adalah kumpulan himpunan yang tidak memuat dirinya sendiri sebagai anggota. Untuk setiap objek , berlaku salah satu dari atau .   Apakah merupakan anggota ? Jelaskan.   Apakah berlaku ? Jelaskan.   Berdasarkan jawaban Anda pada bagian (a) dan (b), jelaskan mengapa gagasan kita saat ini, bahwa himpunan adalah kumpulan anggota, tidak memadai.    Anggaplah kita telah memiliki definisi himpunan yang dapat digunakan. Pada bagian aktivitas ini, kita mendefinisikan himpunan bagian dari suatu himpunan. Notasi yang akan kita gunakan adalah jika merupakan himpunan bagian dari yang tidak sama dengan , dan jika merupakan himpunan bagian dari yang mungkin sama dengan seluruh himpunan . Kita juga akan mengatakan bahwa  termuat dalam jika merupakan himpunan bagian dari , dan menyebut relasi (atau ) sebagai suatu inklusi .   Bagaimana sebaiknya kita mendefinisikan himpunan bagian dari suatu himpunan? Berikan satu contoh konkret suatu himpunan dan dua contoh himpunan bagian dari himpunan tersebut.   Jika adalah suatu himpunan, apakah merupakan himpunan bagian dari ? Jelaskan.   Apa yang dimaksud dengan himpunan kosong ? Jika adalah suatu himpunan, apakah merupakan himpunan bagian dari ? Jelaskan.    "
},
{
  "id": "pa_sets",
  "level": "2",
  "url": "sec_sets_intro.html#pa_sets",
  "type": "Aktivitas Persiapan",
  "number": "1.1",
  "title": "",
  "body": "  Andaikan kita mencoba mendefinisikan himpunan sebagai suatu kumpulan anggota. Jadi, menurut definisi tersebut, anggota adalah objek-objek yang terdapat di dalam himpunan. Kita menggunakan simbol untuk menyatakan bahwa suatu objek merupakan anggota suatu himpunan. Dengan demikian, berarti bahwa suatu objek bukan anggota himpunan tersebut jika merupakan anggota suatu himpunan , kita menulis , sedangkan jika bukan anggota himpunan , kita menulis . Kita menuliskan himpunan dengan kurung kurawal. Sebagai contoh, himpunan adalah himpunan yang anggotanya berupa simbol , , dan . Dalam notasi himpunan, kita juga dapat mencantumkan syarat yang harus dipenuhi oleh anggotanya. Sebagai contoh, adalah himpunan bilangan real positif. Biasanya kita menggunakan huruf kapital untuk menyatakan himpunan. Beberapa contoh himpunan yang sudah dikenal adalah , himpunan bilangan real; , himpunan bilangan rasional; dan , himpunan bilangan bulat. Suatu himpunan juga dapat memiliki himpunan sebagai anggotanya. Sebagai contoh, himpunan kuasa suatu himpunan adalah himpunan semua himpunan bagian dari . Jadi, himpunan kuasa dari adalah himpunan . (Kita akan mendefinisikan himpunan bagian dan himpunan kosong nanti dalam aktivitas ini).    Perhatikan himpunan  berikut, yang merupakan suatu kumpulan objek: . Dengan kata lain, adalah kumpulan himpunan yang tidak memuat dirinya sendiri sebagai anggota. Untuk setiap objek , berlaku salah satu dari atau .   Apakah merupakan anggota ? Jelaskan.   Apakah berlaku ? Jelaskan.   Berdasarkan jawaban Anda pada bagian (a) dan (b), jelaskan mengapa gagasan kita saat ini, bahwa himpunan adalah kumpulan anggota, tidak memadai.    Anggaplah kita telah memiliki definisi himpunan yang dapat digunakan. Pada bagian aktivitas ini, kita mendefinisikan himpunan bagian dari suatu himpunan. Notasi yang akan kita gunakan adalah jika merupakan himpunan bagian dari yang tidak sama dengan , dan jika merupakan himpunan bagian dari yang mungkin sama dengan seluruh himpunan . Kita juga akan mengatakan bahwa  termuat dalam jika merupakan himpunan bagian dari , dan menyebut relasi (atau ) sebagai suatu inklusi .   Bagaimana sebaiknya kita mendefinisikan himpunan bagian dari suatu himpunan? Berikan satu contoh konkret suatu himpunan dan dua contoh himpunan bagian dari himpunan tersebut.   Jika adalah suatu himpunan, apakah merupakan himpunan bagian dari ? Jelaskan.   Apa yang dimaksud dengan himpunan kosong ? Jika adalah suatu himpunan, apakah merupakan himpunan bagian dari ? Jelaskan.   "
},
{
  "id": "sec_basic_top",
  "level": "1",
  "url": "sec_basic_top.html",
  "type": "Bagian",
  "number": "",
  "title": "Gagasan Dasar Topologi",
  "body": " Gagasan Dasar Topologi  Jika Anda menyukai geometri, Anda mungkin juga akan menyukai topologi. Geometri mempelajari objek beserta atribut tertentu (misalnya bentuk dan ukuran), sedangkan topologi lebih umum daripada geometri. Dalam topologi, yang menjadi perhatian bukanlah atribut (bentuk dan ukuran) suatu objek, melainkan ciri-ciri yang tidak berubah ketika objek tersebut kita ubah bentuknya dengan berbagai cara (asalkan objek itu tidak dirobek atau dilubangi). Ada banyak teorema yang sangat menarik dalam topologi sebagai contoh, Teorema Bola Berambut menyatakan bahwa jika seluruh permukaan sebuah bola ditumbuhi rambut (bayangkan tribble dari Star Trek jika acuan itu tidak terlalu lawas), mustahil menyisir rambut-rambut tersebut secara kontinu sehingga semuanya rebah rata. Pasti ada rambut yang mencuat tegak!    Ambillah kawat pembersih pipa, karet gelang, atau seutas tali, lalu bentuklah menjadi persegi. Anda boleh mengubah persegi tersebut dengan menggeser bagian-bagiannya tanpa memutusnya atau mengangkatnya dari permukaan tempatnya berada. Manakah di antara bentuk-bentuk berikut yang dapat diperoleh dengan mengubah persegi tersebut? Jelaskan.   sebuah lingkaran   huruf S    sebuah bintang bersudut lima     huruf D     Sekarang ambillah plastisin (jika tidak memilikinya, gunakan saja imajinasi Anda). Gunakan plastisin tersebut (atau imajinasi Anda) untuk menentukan bentuk-bentuk di bawah ini yang dapat diubah menjadi bentuk lainnya tanpa dirobek atau dilubangi.   sebuah persegi padat   sebuah donat   sebuah mangkuk   sebuah cangkir kopi bergagang    Gagasan untuk mengubah satu himpunan menjadi himpunan lain seperti yang kita kaji dalam secara formal dilakukan dengan fungsi. Seiring kita mendalami pokok bahasan ini, kita akan memerlukan definisi fungsi dan himpunan yang lebih ketat. Kita mulai dengan himpunan dan membahas fungsi dalam .  "
},
{
  "id": "act_rubber_sheet",
  "level": "2",
  "url": "sec_basic_top.html#act_rubber_sheet",
  "type": "Kegiatan",
  "number": "1.2",
  "title": "",
  "body": "  Ambillah kawat pembersih pipa, karet gelang, atau seutas tali, lalu bentuklah menjadi persegi. Anda boleh mengubah persegi tersebut dengan menggeser bagian-bagiannya tanpa memutusnya atau mengangkatnya dari permukaan tempatnya berada. Manakah di antara bentuk-bentuk berikut yang dapat diperoleh dengan mengubah persegi tersebut? Jelaskan.   sebuah lingkaran   huruf S    sebuah bintang bersudut lima     huruf D     Sekarang ambillah plastisin (jika tidak memilikinya, gunakan saja imajinasi Anda). Gunakan plastisin tersebut (atau imajinasi Anda) untuk menentukan bentuk-bentuk di bawah ini yang dapat diubah menjadi bentuk lainnya tanpa dirobek atau dilubangi.   sebuah persegi padat   sebuah donat   sebuah mangkuk   sebuah cangkir kopi bergagang   "
},
{
  "id": "sec_intervals",
  "level": "1",
  "url": "sec_intervals.html",
  "type": "Bagian",
  "number": "",
  "title": "Interval",
  "body": " Interval  Kita akan mulai dengan salah satu jenis himpunan paling dasar yang akan kita jumpai interval. Interval terbuka akan berperan penting karena membentuk suatu basis bagi topologi standar pada . Kita mungkin sudah mengenal interval dari aljabar dan kalkulus, misalnya himpunan seperti dan . Agar benar-benar memahami interval, kita memerlukan definisi yang ketat.   interval   Suatu himpunan bagian dari disebut interval jika untuk setiap , , dan dalam (dalam notasi interval tak berbatas yang diperkenalkan di bawah, atau juga dapat diganti secara formal dengan ) yang memenuhi , apabila dan berada dalam , maka juga berada dalam .    Dengan definisi ini, himpunan semua bilangan real yang memenuhi merupakan interval yang kita nyatakan dengan (penting untuk memperhatikan konteks notasi juga kita gunakan untuk menyatakan pasangan terurut). Notasi umum yang kita gunakan untuk interval adalah sebagai berikut:    ( atau dapat berupa )     ( dapat berupa )     ( dapat berupa )     .     Dalam notasi ini, . Interval berbentuk disebut interval terbuka , interval berbentuk disebut interval tertutup , sedangkan interval berbentuk atau disebut interval setengah terbuka (atau setengah tertutup ). Alasan penggunaan istilah ini akan menjadi lebih jelas ketika nanti kita memperkenalkan himpunan terbuka dan tertutup.  Perhatikan bahwa tidak ada bagian dalam definisi yang mengharuskan pada notasi interval. Hal ini berarti bahwa merupakan interval. Karena tidak ada bilangan real yang sekaligus lebih besar daripada dan lebih kecil daripada , merupakan interval. Kita juga dapat memiliki interval berbentuk , dengan sebarang bilangan real. Artinya, , dan setiap himpunan yang hanya terdiri atas satu titik merupakan interval. Interval dan untuk sebarang bilangan real disebut interval degenerat .  Ada satu catatan terakhir mengenai interval. Sebagian orang mensyaratkan bahwa harus lebih kecil daripada dalam definisi interval, sehingga interval degenerat tidak ada. Hal ini merupakan persoalan konvensi yang tidak akan kita perdebatkan. Dalam hampir seluruh pembahasan kita, kita hanya akan mempertimbangkan interval nondegenerat, sehingga persoalan ini tidak akan menjadi masalah.  "
},
{
  "id": "definition-1",
  "level": "2",
  "url": "sec_intervals.html#definition-1",
  "type": "Definisi",
  "number": "1.1",
  "title": "",
  "body": " interval   Suatu himpunan bagian dari disebut interval jika untuk setiap , , dan dalam (dalam notasi interval tak berbatas yang diperkenalkan di bawah, atau juga dapat diganti secara formal dengan ) yang memenuhi , apabila dan berada dalam , maka juga berada dalam .   "
},
{
  "id": "p-38",
  "level": "2",
  "url": "sec_intervals.html#p-38",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "terbuka tertutup setengah terbuka setengah tertutup "
},
{
  "id": "p-39",
  "level": "2",
  "url": "sec_intervals.html#p-39",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "degenerat "
},
{
  "id": "sec_union_int_comp",
  "level": "1",
  "url": "sec_union_int_comp.html",
  "type": "Bagian",
  "number": "",
  "title": "Gabungan, Irisan, dan Komplemen Himpunan",
  "body": " Gabungan, Irisan, dan Komplemen Himpunan  Dalam matematika, kumpulan titik yang membentuk seutas tali atau segumpal plastisin seperti dalam direpresentasikan sebagai suatu himpunan. Topologi kemudian mempelajari himpunan-himpunan tersebut serta sifat-sifat yang tidak berubah ketika suatu transformasi diterapkan padanya. Untuk mempelajari topologi, kita memerlukan pemahaman yang kuat tentang himpunan dan berbagai operasi pada himpunan.   himpunan Apa yang kita jumpai dalam disebut paradoks . Upaya awal kita untuk mendefinisikan himpunan menghasilkan keadaan yang mustahil, karena baik maupun menimbulkan kontradiksi. Paradoks ini disebut paradoks Russell , mengambil nama Bertrand Russell, meskipun tampaknya paradoks tersebut telah diketahui sebelum Russell. Pelajaran yang dapat kita ambil adalah bahwa kita harus berhati-hati ketika membuat definisi. Himpunan mungkin tampak sebagai objek yang sederhana, dan dalam pengalaman kita biasanya memang demikian, tetapi mendefinisikan himpunan secara formal dapat menimbulkan masalah. Oleh karena itu, kita tidak akan memberikan definisi formal, melainkan menganggap himpunan sebagai kumpulan objek yang tidak menimbulkan paradoks. Objek-objek tersebut disebut anggota himpunan. (Dalam teori himpunan aksiomatik, himpunan dipandang sebagai konsep primitif yang tidak didefinisikan sebagaimana titik tidak didefinisikan dalam geometri Euklides.)  Agar dapat bekerja dengan himpunan secara efektif, kita perlu memahami apa artinya dua himpunan sama.    Apa yang dimaksud dengan dua himpunan yang sama? Jika dan adalah himpunan, bagaimana kita membuktikan bahwa ? (Pertanyaan ini memerlukan pembahasan, berbeda dengan pertanyaan yang hanya meminta perhitungan atau contoh. Aktivitas di sepanjang buku ini akan memuat kedua jenis pertanyaan tersebut.)    Misalkan dan . Apakah ? Jika ya, buktikan jawaban Anda. Jika tidak, buktikan setiap inklusi yang berlaku.    Misalkan dan . Apakah ? Jika ya, buktikan jawaban Anda. Jika tidak, buktikan setiap inklusi yang berlaku.    Misalkan dan . Apakah ? Jika ya, buktikan jawaban Anda. Jika tidak, buktikan setiap inklusi yang berlaku.    Setelah memiliki gagasan tentang himpunan, kita dapat membentuk himpunan baru dari himpunan yang sudah ada. Sebagai contoh, kita mendefinisikan gabungan, irisan, selisih himpunan, dan komplemen sebagai berikut.   himpunan gabungan   Gabungan himpunan dan adalah himpunan yang didefinisikan sebagai .     Irisan  himpunan irisan himpunan dan adalah himpunan yang didefinisikan sebagai .    Misalkan dan adalah himpunan. Selisih himpunan  selisih himpunan  adalah himpunan .    Misalkan merupakan himpunan bagian dari suatu himpunan . Komplemen  himpunan komplemen  di dalam adalah himpunan . Komplemen himpunan di dalam himpunan juga dinyatakan dengan , (jika himpunan sudah dipahami dari konteks), , atau bahkan .     Kita dapat memvisualisasikan himpunan-himpunan ini dengan diagram Venn. Diagram Venn menggambarkan himpunan menggunakan bangun-bangun geometri. Sebagai contoh, jika adalah himpunan yang memuat semua himpunan lain yang sedang diperhatikan (kita menyebut sebagai himpunan semesta ), kita dapat merepresentasikan sebagai wadah besar (misalnya persegi panjang), dengan himpunan bagian dan sebagai wadah yang lebih kecil (misalnya lingkaran), lalu mengarsir anggota-anggota suatu himpunan tertentu. Diagram Venn dalam menggambarkan himpunan , , , , , dan .   Diagram Venn    Sebuah persegi panjang yang mewakili himpunan semesta memuat dua lingkaran beririsan, A di kiri dan B di kanan. Seluruh lingkaran A, termasuk daerah irisannya dengan B, diarsir.  Sebuah persegi panjang yang mewakili himpunan semesta memuat dua lingkaran beririsan, A di kiri dan B di kanan. Seluruh lingkaran B, termasuk daerah irisannya dengan A, diarsir.  Sebuah persegi panjang yang mewakili himpunan semesta memuat dua lingkaran beririsan, A dan B. Kedua lingkaran, termasuk daerah irisannya, diarsir untuk menunjukkan gabungan A dan B.         Sebuah persegi panjang yang mewakili himpunan semesta memuat dua lingkaran beririsan, A dan B. Hanya daerah berbentuk lensa tempat A dan B beririsan yang diarsir.  Sebuah persegi panjang yang mewakili himpunan semesta memuat dua lingkaran beririsan, A dan B. Seluruh daerah di luar lingkaran A diarsir untuk menunjukkan komplemen A.  Sebuah persegi panjang yang mewakili himpunan semesta memuat dua lingkaran beririsan, A dan B. Seluruh daerah di luar lingkaran B diarsir untuk menunjukkan komplemen B.          Seperti yang telah kita bahas, untuk membuktikan bahwa dua himpunan dan sama, kita membuktikan bahwa masing-masing merupakan himpunan bagian dari yang lain. Contoh berikut memberikan ilustrasi lain dari gagasan tersebut.    Misalkan , , dan adalah himpunan. Kita akan membuktikan bahwa .  Untuk membuktikan kesamaan himpunan ini, kita harus membuktikan bahwa dan . Kita mulai dengan .  Untuk membuktikan bahwa , kita perlu menunjukkan bahwa setiap anggota juga merupakan anggota . Untuk itu, kita pilih sembarang anggota dari dan menunjukkan bahwa anggota tersebut berada dalam . Misalkan . Maka dan . Fakta bahwa berarti bahwa , tetapi . Oleh karena itu, dan , tetapi . Ini berarti bahwa dan , sedangkan dan . Jadi, dan , tetapi . Kita menyimpulkan bahwa . Hal ini membuktikan bahwa .  Untuk inklusi sebaliknya, misalkan . Jadi, , tetapi . Karena , kita mengetahui bahwa dan . Fakta bahwa , bersama dengan keanggotaan yang telah disebutkan, berarti bahwa . Jadi, , , dan . Dengan demikian, dan . Kita menyimpulkan bahwa , yang menunjukkan bahwa . Kedua inklusi, dan , menunjukkan bahwa .    Kita akan menggunakan gagasan dalam dan untuk membuktikan kesamaan himpunan di sepanjang buku ini. Aktivitas berikut memberikan latihan tambahan.    Dalam aktivitas ini, kita bekerja dengan gabungan, irisan, dan komplemen himpunan. Misalkan dan adalah himpunan.    Misalkan dan , dengan .   Tentukan anggota dan . Apa saja anggota dan ?   Tentukan anggota dan .    Misalkan dan merupakan sembarang himpunan bagian dari suatu himpunan semesta . Terdapat hubungan antara , , komplemen keduanya, gabungan, dan irisan.   Gunakan diagram Venn untuk menggambar dan .   Gunakan diagram Venn dan hasil pada bagian (a) untuk menemukan serta membuktikan hubungan antara , , dan .   Gunakan diagram Venn dan hasil pada bagian (a) untuk menemukan serta membuktikan hubungan antara , , dan .    Dalam kita bekerja dengan gabungan dan irisan dua himpunan. Tidak ada alasan untuk membatasi definisi ini hanya pada dua himpunan, seperti yang ditunjukkan oleh aktivitas berikut.   keluarga himpunan berindeks   Untuk mendefinisikan kumpulan himpunan tak hingga, kita sering menggunakan apa yang disebut himpunan indeks . Himpunan indeks memungkinkan kita mempertimbangkan kumpulan objek yang berkorespondensi satu-satu dengan himpunan seperti bilangan bulat positif, atau bahkan bilangan real. Ketika menggunakan himpunan indeks, biasanya kita membuat pernyataan seperti “misalkan , untuk , adalah kumpulan himpunan yang diindeks oleh suatu himpunan ”. Kumpulan disebut keluarga himpunan berindeks .    Himpunan dapat berhingga. Sebagai contoh, misalkan untuk dalam himpunan .   Tentukan . Tentukan .   Ada berapa himpunan dalam keluarga berindeks ?    Himpunan indeks juga dapat tak hingga. Sebagai contoh, misalkan untuk dalam himpunan (dengan menyatakan interval yang terdiri atas bilangan real sedemikian sehingga ). Dalam hal ini, tentukan . Tentukan . Tentukan .    Kita telah mendefinisikan gabungan dan irisan dua himpunan. Gagasan yang sama dapat diperluas untuk mendefinisikan gabungan dan irisan suatu kumpulan himpunan berindeks.  himpunan irisan sembarang  Ingat bahwa jika dan adalah himpunan, irisan adalah himpunan . Bagaimana kita dapat memperluas definisi ini dari dua himpunan menjadi sebarang kumpulan himpunan? Dengan kata lain, bagaimana kita mendefinisikan  Dalam contoh pada bagian (b), himpunan apakah itu?  himpunan gabungan sembarang  Ingat bahwa jika dan adalah himpunan, gabungan adalah himpunan . Bagaimana kita dapat memperluas definisi ini dari dua himpunan menjadi sebarang kumpulan himpunan? Dengan kata lain, bagaimana kita mendefinisikan  Dalam contoh pada bagian (b), himpunan apakah itu?    Sifat dan yang kita pelajari dalam disebut Hukum De Morgan. Hukum ini berlaku untuk sebarang gabungan atau irisan himpunan, baik berhingga maupun tak hingga. Pembuktiannya diserahkan kepada .   Hukum De Morgan   Misalkan adalah kumpulan himpunan yang diindeks oleh suatu himpunan di dalam himpunan semesta . Maka                  Verifikasikan Hukum De Morgan untuk kasus khusus di dalam , dengan sebarang anggota himpunan indeks .    Mengapa komplemen suatu gabungan seharusnya berupa irisan, dan mengapa komplemen suatu irisan seharusnya berupa gabungan?   Perhatikan definisi gabungan dan irisan.    "
},
{
  "id": "p-42",
  "level": "2",
  "url": "sec_union_int_comp.html#p-42",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "paradoks paradoks Russell "
},
{
  "id": "act_set_equality",
  "level": "2",
  "url": "sec_union_int_comp.html#act_set_equality",
  "type": "Kegiatan",
  "number": "1.3",
  "title": "",
  "body": "  Apa yang dimaksud dengan dua himpunan yang sama? Jika dan adalah himpunan, bagaimana kita membuktikan bahwa ? (Pertanyaan ini memerlukan pembahasan, berbeda dengan pertanyaan yang hanya meminta perhitungan atau contoh. Aktivitas di sepanjang buku ini akan memuat kedua jenis pertanyaan tersebut.)    Misalkan dan . Apakah ? Jika ya, buktikan jawaban Anda. Jika tidak, buktikan setiap inklusi yang berlaku.    Misalkan dan . Apakah ? Jika ya, buktikan jawaban Anda. Jika tidak, buktikan setiap inklusi yang berlaku.    Misalkan dan . Apakah ? Jika ya, buktikan jawaban Anda. Jika tidak, buktikan setiap inklusi yang berlaku.   "
},
{
  "id": "p-48",
  "level": "2",
  "url": "sec_union_int_comp.html#p-48",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "Gabungan Irisan Selisih himpunan Komplemen "
},
{
  "id": "p-53",
  "level": "2",
  "url": "sec_union_int_comp.html#p-53",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "semesta "
},
{
  "id": "F_Venn",
  "level": "2",
  "url": "sec_union_int_comp.html#F_Venn",
  "type": "Gambar",
  "number": "1.2",
  "title": "",
  "body": " Diagram Venn    Sebuah persegi panjang yang mewakili himpunan semesta memuat dua lingkaran beririsan, A di kiri dan B di kanan. Seluruh lingkaran A, termasuk daerah irisannya dengan B, diarsir.  Sebuah persegi panjang yang mewakili himpunan semesta memuat dua lingkaran beririsan, A di kiri dan B di kanan. Seluruh lingkaran B, termasuk daerah irisannya dengan A, diarsir.  Sebuah persegi panjang yang mewakili himpunan semesta memuat dua lingkaran beririsan, A dan B. Kedua lingkaran, termasuk daerah irisannya, diarsir untuk menunjukkan gabungan A dan B.         Sebuah persegi panjang yang mewakili himpunan semesta memuat dua lingkaran beririsan, A dan B. Hanya daerah berbentuk lensa tempat A dan B beririsan yang diarsir.  Sebuah persegi panjang yang mewakili himpunan semesta memuat dua lingkaran beririsan, A dan B. Seluruh daerah di luar lingkaran A diarsir untuk menunjukkan komplemen A.  Sebuah persegi panjang yang mewakili himpunan semesta memuat dua lingkaran beririsan, A dan B. Seluruh daerah di luar lingkaran B diarsir untuk menunjukkan komplemen B.         "
},
{
  "id": "ex_set_eq",
  "level": "2",
  "url": "sec_union_int_comp.html#ex_set_eq",
  "type": "Contoh",
  "number": "1.3",
  "title": "",
  "body": "  Misalkan , , dan adalah himpunan. Kita akan membuktikan bahwa .  Untuk membuktikan kesamaan himpunan ini, kita harus membuktikan bahwa dan . Kita mulai dengan .  Untuk membuktikan bahwa , kita perlu menunjukkan bahwa setiap anggota juga merupakan anggota . Untuk itu, kita pilih sembarang anggota dari dan menunjukkan bahwa anggota tersebut berada dalam . Misalkan . Maka dan . Fakta bahwa berarti bahwa , tetapi . Oleh karena itu, dan , tetapi . Ini berarti bahwa dan , sedangkan dan . Jadi, dan , tetapi . Kita menyimpulkan bahwa . Hal ini membuktikan bahwa .  Untuk inklusi sebaliknya, misalkan . Jadi, , tetapi . Karena , kita mengetahui bahwa dan . Fakta bahwa , bersama dengan keanggotaan yang telah disebutkan, berarti bahwa . Jadi, , , dan . Dengan demikian, dan . Kita menyimpulkan bahwa , yang menunjukkan bahwa . Kedua inklusi, dan , menunjukkan bahwa .   "
},
{
  "id": "act_sets_1",
  "level": "2",
  "url": "sec_union_int_comp.html#act_sets_1",
  "type": "Kegiatan",
  "number": "1.4",
  "title": "",
  "body": "  Dalam aktivitas ini, kita bekerja dengan gabungan, irisan, dan komplemen himpunan. Misalkan dan adalah himpunan.    Misalkan dan , dengan .   Tentukan anggota dan . Apa saja anggota dan ?   Tentukan anggota dan .    Misalkan dan merupakan sembarang himpunan bagian dari suatu himpunan semesta . Terdapat hubungan antara , , komplemen keduanya, gabungan, dan irisan.   Gunakan diagram Venn untuk menggambar dan .   Gunakan diagram Venn dan hasil pada bagian (a) untuk menemukan serta membuktikan hubungan antara , , dan .   Gunakan diagram Venn dan hasil pada bagian (a) untuk menemukan serta membuktikan hubungan antara , , dan .   "
},
{
  "id": "activity-4",
  "level": "2",
  "url": "sec_union_int_comp.html#activity-4",
  "type": "Kegiatan",
  "number": "1.5",
  "title": "",
  "body": " keluarga himpunan berindeks   Untuk mendefinisikan kumpulan himpunan tak hingga, kita sering menggunakan apa yang disebut himpunan indeks . Himpunan indeks memungkinkan kita mempertimbangkan kumpulan objek yang berkorespondensi satu-satu dengan himpunan seperti bilangan bulat positif, atau bahkan bilangan real. Ketika menggunakan himpunan indeks, biasanya kita membuat pernyataan seperti “misalkan , untuk , adalah kumpulan himpunan yang diindeks oleh suatu himpunan ”. Kumpulan disebut keluarga himpunan berindeks .    Himpunan dapat berhingga. Sebagai contoh, misalkan untuk dalam himpunan .   Tentukan . Tentukan .   Ada berapa himpunan dalam keluarga berindeks ?    Himpunan indeks juga dapat tak hingga. Sebagai contoh, misalkan untuk dalam himpunan (dengan menyatakan interval yang terdiri atas bilangan real sedemikian sehingga ). Dalam hal ini, tentukan . Tentukan . Tentukan .    Kita telah mendefinisikan gabungan dan irisan dua himpunan. Gagasan yang sama dapat diperluas untuk mendefinisikan gabungan dan irisan suatu kumpulan himpunan berindeks.  himpunan irisan sembarang  Ingat bahwa jika dan adalah himpunan, irisan adalah himpunan . Bagaimana kita dapat memperluas definisi ini dari dua himpunan menjadi sebarang kumpulan himpunan? Dengan kata lain, bagaimana kita mendefinisikan  Dalam contoh pada bagian (b), himpunan apakah itu?  himpunan gabungan sembarang  Ingat bahwa jika dan adalah himpunan, gabungan adalah himpunan . Bagaimana kita dapat memperluas definisi ini dari dua himpunan menjadi sebarang kumpulan himpunan? Dengan kata lain, bagaimana kita mendefinisikan  Dalam contoh pada bagian (b), himpunan apakah itu?   "
},
{
  "id": "theorem-1",
  "level": "2",
  "url": "sec_union_int_comp.html#theorem-1",
  "type": "Teorema",
  "number": "1.4",
  "title": "Hukum De Morgan.",
  "body": " Hukum De Morgan   Misalkan adalah kumpulan himpunan yang diindeks oleh suatu himpunan di dalam himpunan semesta . Maka               "
},
{
  "id": "activity-5",
  "level": "2",
  "url": "sec_union_int_comp.html#activity-5",
  "type": "Kegiatan",
  "number": "1.6",
  "title": "",
  "body": "  Verifikasikan Hukum De Morgan untuk kasus khusus di dalam , dengan sebarang anggota himpunan indeks .    Mengapa komplemen suatu gabungan seharusnya berupa irisan, dan mengapa komplemen suatu irisan seharusnya berupa gabungan?   Perhatikan definisi gabungan dan irisan.   "
},
{
  "id": "sec_cart_prod",
  "level": "1",
  "url": "sec_cart_prod.html",
  "type": "Bagian",
  "number": "",
  "title": "Hasil Kali Kartesius Himpunan",
  "body": " Hasil Kali Kartesius Himpunan  Operasi terakhir pada himpunan yang akan kita bahas adalah hasil kali Kartesius (atau hasil kali silang ). Operasi ini sebenarnya sudah pernah kita jumpai. Ketika menggambar grafik garis pada bidang, kita memetakan titik-titik . Titik-titik tersebut merupakan pasangan terurut bilangan real. Gagasan ini dapat kita perluas ke sebarang himpunan.   hasil kali Kartesius   Misalkan dan adalah himpunan. Hasil kali Kartesius dari dan adalah himpunan .    Dengan kata lain, hasil kali Kartesius dan adalah himpunan pasangan terurut , dengan berasal dari dan berasal dari . Perhatikan bahwa urutannya penting.    Tuliskan semua anggota .    Jika memiliki anggota dan memiliki anggota, berapa banyak anggota yang dimiliki himpunan ? Jelaskan.    Tidak ada alasan untuk membatasi diri pada hasil kali Kartesius dua himpunan saja. Gagasan ini juga sudah pernah kita jumpai. Hasil kali Kartesius adalah bidang real standar yang kita nyatakan dengan , sedangkan hasil kali Kartesius adalah ruang real berdimensi tiga yang dinyatakan dengan . Jika kita memiliki suatu kumpulan berindeks yang terdiri atas himpunan-himpunan, dengan menjelajahi himpunan bilangan bulat positif, maka hasil kali Kartesius himpunan-himpunan dapat kita definisikan sebagai himpunan barisan tak hingga , dengan untuk setiap . Kita menyatakan hasil kali Kartesius ini dengan .  Huruf pi kapital ( ) digunakan untuk menyatakan hasil kali, sebagai analog dari sigma kapital ( ) yang digunakan untuk menyatakan jumlah. Kita akan mempelajari barisan secara lebih mendalam nanti.  Sebagai penutup bagian ini, kita merangkum beberapa sifat himpunan. Banyak di antara sifat-sifat ini dapat diperluas ke kumpulan himpunan sembarang. Sebagian besar pembuktiannya langsung. Pembuktian hukum asosiatif dan distributif diserahkan kepada .    Misalkan , , dan merupakan himpunan bagian dari suatu himpunan semesta .   Sifat Himpunan Kosong                            Sifat Himpunan Semesta                            Hukum Idempoten                  Hukum Komutatif                  Hukum Asosiatif                  Hukum Distributif                  Sifat Dasar                  Himpunan Bagian dan Komplemen          "
},
{
  "id": "p-90",
  "level": "2",
  "url": "sec_cart_prod.html#p-90",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "hasil kali Kartesius hasil kali silang "
},
{
  "id": "definition-2",
  "level": "2",
  "url": "sec_cart_prod.html#definition-2",
  "type": "Definisi",
  "number": "1.5",
  "title": "",
  "body": " hasil kali Kartesius   Misalkan dan adalah himpunan. Hasil kali Kartesius dari dan adalah himpunan .   "
},
{
  "id": "activity-6",
  "level": "2",
  "url": "sec_cart_prod.html#activity-6",
  "type": "Kegiatan",
  "number": "1.7",
  "title": "",
  "body": "  Tuliskan semua anggota .    Jika memiliki anggota dan memiliki anggota, berapa banyak anggota yang dimiliki himpunan ? Jelaskan.   "
},
{
  "id": "theorem-2",
  "level": "2",
  "url": "sec_cart_prod.html#theorem-2",
  "type": "Teorema",
  "number": "1.6",
  "title": "",
  "body": "  Misalkan , , dan merupakan himpunan bagian dari suatu himpunan semesta .   Sifat Himpunan Kosong                            Sifat Himpunan Semesta                            Hukum Idempoten                  Hukum Komutatif                  Hukum Asosiatif                  Hukum Distributif                  Sifat Dasar                  Himpunan Bagian dan Komplemen         "
},
{
  "id": "sec_sets_summ",
  "level": "1",
  "url": "sec_sets_summ.html",
  "type": "Bagian",
  "number": "",
  "title": "Ringkasan",
  "body": " Ringkasan  Gagasan penting yang telah kita bahas dalam bagian ini meliputi hal-hal berikut.   Kita dapat memandang himpunan sebagai kumpulan anggota yang terdefinisi dengan baik.    Himpunan bagian dari suatu himpunan adalah sebarang kumpulan anggota yang berasal dari himpunan tersebut. Dengan kata lain, himpunan bagian dari suatu himpunan adalah himpunan dengan sifat bahwa jika , maka .    Jika dan adalah himpunan, maka gabungan adalah himpunan . Gabungan dari suatu keluarga himpunan sembarang , dengan berada dalam suatu himpunan indeks , adalah himpunan .    Jika dan adalah himpunan, maka irisan adalah himpunan . Irisan dari suatu keluarga himpunan sembarang , dengan berada dalam suatu himpunan indeks , adalah himpunan .    Jika adalah himpunan dan merupakan himpunan bagian dari , maka komplemen di dalam adalah himpunan .    Jika adalah kumpulan himpunan dengan berada dalam suatu himpunan indeks , dengan berhingga atau merupakan himpunan bilangan bulat positif, maka hasil kali Kartesius dari himpunan-himpunan adalah himpunan semua tupel terurut berbentuk dengan .     "
},
{
  "id": "sec_sets_exer",
  "level": "1",
  "url": "sec_sets_exer.html",
  "type": "Latihan",
  "number": "",
  "title": "Latihan",
  "body": "  Misalkan , , dan merupakan himpunan bagian dari suatu himpunan . Nyatakan setiap himpunan berikut dalam notasi matematika dengan menggunakan simbol , , dan .   Anggota yang merupakan anggota dan , tetapi bukan anggota .   Anggota yang merupakan anggota dan setidaknya salah satu dari atau .   Anggota yang merupakan anggota , tetapi tidak sekaligus menjadi anggota dan .   Anggota yang bukan merupakan anggota satu pun dari himpunan , , dan .   Anggota yang bukan merupakan anggota setidaknya dua dari himpunan , , dan .   Anggota yang bukan merupakan anggota paling banyak satu dari himpunan , , dan .    Misalkan . Buktikan atau berikan contoh tandingan.    .    .    Misalkan dan merupakan himpunan bagian dari suatu himpunan semesta , dan anggap pula setiap himpunan lain yang muncul di bawah merupakan himpunan bagian dari himpunan semesta yang sama. Buktikan hukum asosiatif dan distributif. Dengan kata lain, buktikan setiap pernyataan berikut.                    Buktikan Hukum De Morgan. Dengan kata lain, misalkan adalah kumpulan himpunan yang diindeks oleh suatu himpunan di dalam himpunan semesta . Buktikan bahwa            Tentukan himpunan yang sama dengan untuk sebarang himpunan . Jelaskan.   himpunan kuasa  Jika adalah suatu himpunan, himpunan kuasa dari , yang dinyatakan dengan , adalah kumpulan semua himpunan bagian dari .   Tuliskan anggota .   Jika adalah himpunan yang memiliki tiga anggota, berapa banyak anggota dalam ?   Jika adalah himpunan yang memiliki anggota, buatlah dugaan mengenai banyaknya anggota dalam . Buktikan dugaan Anda.    Jika adalah suatu himpunan, himpunan kuasa dari , yang dinyatakan dengan , adalah kumpulan semua himpunan bagian dari . (Lihat .) Telaahlah setiap pernyataan berikut. Apakah pernyataan tersebut bermakna atau tidak? Jika tidak, jelaskan alasannya, lalu perbaikilah menjadi pernyataan yang benar (dan tidak sepele).   Jika adalah suatu himpunan, maka .   Jika adalah suatu himpunan, maka .   Jika adalah suatu himpunan, maka .   Jika adalah suatu himpunan, maka .   Jika adalah suatu himpunan, maka .   Jika dan adalah himpunan dan , maka .    Misalkan dan adalah himpunan, yang masing-masing memiliki sekurang-kurangnya dua anggota berbeda. Buktikan bahwa terdapat suatu himpunan bagian yang bukan merupakan hasil kali Kartesius antara suatu himpunan bagian dari dan suatu himpunan bagian dari . [Jadi, tidak setiap himpunan bagian dari suatu hasil kali Kartesius merupakan hasil kali Kartesius dari sepasang himpunan bagian.]    Misalkan adalah himpunan bilangan real yang lebih besar daripada . Untuk setiap , misalkan adalah interval terbuka . Buktikan bahwa , . Untuk setiap , misalkan adalah interval tertutup . Buktikan bahwa , .    Untuk setiap pernyataan berikut, jawablah benar jika pernyataan tersebut selalu benar. Jika pernyataan tersebut hanya kadang-kadang benar atau tidak pernah benar, jawablah salah dan berikan contoh konkret yang menunjukkan bahwa pernyataan itu salah. Jika suatu pernyataan benar, jelaskan alasannya. Sebagai contoh pernyataan yang benar, perhatikan pernyataan berikut.   Misalkan , , dan adalah himpunan sedemikian sehingga dan .   Maka . Kita dapat membenarkan pernyataan ini dengan argumen singkat. Karena , terdapat anggota . Dengan demikian, . Karena , juga harus berlaku , yang berarti bahwa . Jadi, dan . Sebagai contoh pernyataan yang salah, perhatikan pernyataan berikut.   Misalkan , , dan adalah himpunan sedemikian sehingga .  Maka . Kita dapat menunjukkan bahwa pernyataan ini salah dengan memberikan contoh tandingan. Sebagai contoh, misalkan , , dan . Maka , tetapi .   Jika , , dan adalah himpunan serta dan , maka .   Jika , , dan adalah himpunan serta dan , maka .   Jika dan merupakan himpunan bagian dari suatu himpunan serta , maka .   Jika dan merupakan himpunan bagian dari suatu himpunan serta , maka .   Jika dan adalah himpunan, maka .   Jika dan adalah himpunan, maka .   Jika , , dan adalah himpunan, maka .   Jika dan merupakan himpunan bagian dari suatu himpunan , maka .   Himpunan tidak memiliki anggota.   Terdapat dua objek berbeda yang merupakan anggota himpunan .   "
},
{
  "id": "exercise-1",
  "level": "2",
  "url": "sec_sets_exer.html#exercise-1",
  "type": "Latihan",
  "number": "1",
  "title": "",
  "body": " Misalkan , , dan merupakan himpunan bagian dari suatu himpunan . Nyatakan setiap himpunan berikut dalam notasi matematika dengan menggunakan simbol , , dan .   Anggota yang merupakan anggota dan , tetapi bukan anggota .   Anggota yang merupakan anggota dan setidaknya salah satu dari atau .   Anggota yang merupakan anggota , tetapi tidak sekaligus menjadi anggota dan .   Anggota yang bukan merupakan anggota satu pun dari himpunan , , dan .   Anggota yang bukan merupakan anggota setidaknya dua dari himpunan , , dan .   Anggota yang bukan merupakan anggota paling banyak satu dari himpunan , , dan .  "
},
{
  "id": "exercise-2",
  "level": "2",
  "url": "sec_sets_exer.html#exercise-2",
  "type": "Latihan",
  "number": "2",
  "title": "",
  "body": " Misalkan . Buktikan atau berikan contoh tandingan.    .    .  "
},
{
  "id": "ex_set_props",
  "level": "2",
  "url": "sec_sets_exer.html#ex_set_props",
  "type": "Latihan",
  "number": "3",
  "title": "",
  "body": " Misalkan dan merupakan himpunan bagian dari suatu himpunan semesta , dan anggap pula setiap himpunan lain yang muncul di bawah merupakan himpunan bagian dari himpunan semesta yang sama. Buktikan hukum asosiatif dan distributif. Dengan kata lain, buktikan setiap pernyataan berikut.                  "
},
{
  "id": "ex_DeMorgan",
  "level": "2",
  "url": "sec_sets_exer.html#ex_DeMorgan",
  "type": "Latihan",
  "number": "4",
  "title": "",
  "body": " Buktikan Hukum De Morgan. Dengan kata lain, misalkan adalah kumpulan himpunan yang diindeks oleh suatu himpunan di dalam himpunan semesta . Buktikan bahwa          "
},
{
  "id": "exercise-5",
  "level": "2",
  "url": "sec_sets_exer.html#exercise-5",
  "type": "Latihan",
  "number": "5",
  "title": "",
  "body": " Tentukan himpunan yang sama dengan untuk sebarang himpunan . Jelaskan.  "
},
{
  "id": "ex_power_set",
  "level": "2",
  "url": "sec_sets_exer.html#ex_power_set",
  "type": "Latihan",
  "number": "6",
  "title": "",
  "body": "himpunan kuasa  Jika adalah suatu himpunan, himpunan kuasa dari , yang dinyatakan dengan , adalah kumpulan semua himpunan bagian dari .   Tuliskan anggota .   Jika adalah himpunan yang memiliki tiga anggota, berapa banyak anggota dalam ?   Jika adalah himpunan yang memiliki anggota, buatlah dugaan mengenai banyaknya anggota dalam . Buktikan dugaan Anda.  "
},
{
  "id": "exercise-7",
  "level": "2",
  "url": "sec_sets_exer.html#exercise-7",
  "type": "Latihan",
  "number": "7",
  "title": "",
  "body": " Jika adalah suatu himpunan, himpunan kuasa dari , yang dinyatakan dengan , adalah kumpulan semua himpunan bagian dari . (Lihat .) Telaahlah setiap pernyataan berikut. Apakah pernyataan tersebut bermakna atau tidak? Jika tidak, jelaskan alasannya, lalu perbaikilah menjadi pernyataan yang benar (dan tidak sepele).   Jika adalah suatu himpunan, maka .   Jika adalah suatu himpunan, maka .   Jika adalah suatu himpunan, maka .   Jika adalah suatu himpunan, maka .   Jika adalah suatu himpunan, maka .   Jika dan adalah himpunan dan , maka .  "
},
{
  "id": "exercise-8",
  "level": "2",
  "url": "sec_sets_exer.html#exercise-8",
  "type": "Latihan",
  "number": "8",
  "title": "",
  "body": " Misalkan dan adalah himpunan, yang masing-masing memiliki sekurang-kurangnya dua anggota berbeda. Buktikan bahwa terdapat suatu himpunan bagian yang bukan merupakan hasil kali Kartesius antara suatu himpunan bagian dari dan suatu himpunan bagian dari . [Jadi, tidak setiap himpunan bagian dari suatu hasil kali Kartesius merupakan hasil kali Kartesius dari sepasang himpunan bagian.]  "
},
{
  "id": "exercise-9",
  "level": "2",
  "url": "sec_sets_exer.html#exercise-9",
  "type": "Latihan",
  "number": "9",
  "title": "",
  "body": " Misalkan adalah himpunan bilangan real yang lebih besar daripada . Untuk setiap , misalkan adalah interval terbuka . Buktikan bahwa , . Untuk setiap , misalkan adalah interval tertutup . Buktikan bahwa , .  "
},
{
  "id": "exercise-10",
  "level": "2",
  "url": "sec_sets_exer.html#exercise-10",
  "type": "Latihan",
  "number": "10",
  "title": "",
  "body": " Untuk setiap pernyataan berikut, jawablah benar jika pernyataan tersebut selalu benar. Jika pernyataan tersebut hanya kadang-kadang benar atau tidak pernah benar, jawablah salah dan berikan contoh konkret yang menunjukkan bahwa pernyataan itu salah. Jika suatu pernyataan benar, jelaskan alasannya. Sebagai contoh pernyataan yang benar, perhatikan pernyataan berikut.   Misalkan , , dan adalah himpunan sedemikian sehingga dan .   Maka . Kita dapat membenarkan pernyataan ini dengan argumen singkat. Karena , terdapat anggota . Dengan demikian, . Karena , juga harus berlaku , yang berarti bahwa . Jadi, dan . Sebagai contoh pernyataan yang salah, perhatikan pernyataan berikut.   Misalkan , , dan adalah himpunan sedemikian sehingga .  Maka . Kita dapat menunjukkan bahwa pernyataan ini salah dengan memberikan contoh tandingan. Sebagai contoh, misalkan , , dan . Maka , tetapi .   Jika , , dan adalah himpunan serta dan , maka .   Jika , , dan adalah himpunan serta dan , maka .   Jika dan merupakan himpunan bagian dari suatu himpunan serta , maka .   Jika dan merupakan himpunan bagian dari suatu himpunan serta , maka .   Jika dan adalah himpunan, maka .   Jika dan adalah himpunan, maka .   Jika , , dan adalah himpunan, maka .   Jika dan merupakan himpunan bagian dari suatu himpunan , maka .   Himpunan tidak memiliki anggota.   Terdapat dua objek berbeda yang merupakan anggota himpunan .  "
},
{
  "id": "sec_func_intro",
  "level": "1",
  "url": "sec_func_intro.html",
  "type": "Bagian",
  "number": "",
  "title": "Pendahuluan",
  "body": " Pendahuluan  Banyak sifat topologis didefinisikan menggunakan fungsi kontinu. Kontinuitas akan kita pelajari secara khusus nanti untuk saat ini, kita meninjau beberapa konsep penting yang berkaitan dengan fungsi. Sebagian besar konsep ini semestinya sudah tidak asing, tetapi beberapa di antaranya mungkin baru.  Pertama-tama kita sajikan definisi-definisi dasarnya. Sebagian besar pembahasan kita sebelumnya mungkin berkaitan dengan fungsi yang memetakan bilangan real ke bilangan real, tetapi di sini kita akan memandang fungsi dari sudut pandang yang lebih umum. Kita mulai dengan definisi formal suatu fungsi.   fungsi   Suatu fungsi  dari himpunan tak kosong ke himpunan adalah koleksi pasangan terurut sedemikian sehingga   untuk setiap , terdapat pasangan di dalam , dan    jika dan berada di dalam , maka .       Perhatikan bahwa sifat pertama adalah sifat eksistensi jika , maka terdapat unsur di dalam yang dipasangkan dengan . Sifat pertama ini juga menyatakan bahwa setiap unsur di dalam digunakan, atau bahwa setiap unsur di dalam dipasangkan dengan suatu unsur di dalam , dan unsur di dalam tersebut bergantung pada unsur di dalam yang dipilih. Sifat kedua adalah sifat ketunggalan hanya ada satu unsur di dalam yang dipasangkan dengan suatu unsur tertentu di dalam .  Umumnya kita menggunakan notasi lain untuk suatu fungsi. Jika merupakan anggota fungsi , kita menulis , dan dengan cara ini kita memandang sebagai pemetaan dari himpunan ke himpunan . Kita menyatakan bahwa adalah pemetaan dari himpunan ke himpunan dengan notasi .  Jika memetakan unsur ke unsur , kita juga menggunakan notasi .  Ada beberapa istilah dan notasi yang sudah dikenal dan berkaitan dengan fungsi. Misalkan suatu fungsi dari himpunan ke himpunan .   Himpunan disebut domain  fungsi domain dari , dan kita menulis .    Himpunan disebut kodomain  fungsi kodomain dari , dan kita menulis .    Subhimpunan dari disebut daerah hasil  fungsi daerah hasil dari , yang kita nyatakan dengan .    Jika , maka adalah citra  citra suatu unsur dari oleh . Karena setiap di dalam dipasangkan dengan tepat satu , citra oleh hanya ada satu. Karena itu, kita dapat merujuk tanpa ambiguitas pada citra unsur tersebut .    Jika dan untuk suatu , maka disebut suatu prapeta  prapeta suatu unsur dari . Untuk suatu tertentu, mungkin memiliki banyak prapeta yang berbeda, mungkin tidak memiliki prapeta, atau mungkin memiliki tepat satu prapeta. Menyusun contoh untuk setiap keadaan tersebut dapat membantu pemahaman. Karena prapeta suatu unsur belum tentu tunggal, kita menyebutnya suatu prapeta .     Mengetahui domain dan kodomain sangat penting ketika bekerja dengan fungsi, dan kedua himpunan ini akan banyak kita perhatikan.  Dalam pembelajaran matematika sebelumnya, kita mungkin telah menjumpai fungsi satu-ke-satu dan fungsi pada. Fungsi satu-ke-satu (atau injeksi) dan fungsi pada (atau surjeksi) merupakan jenis fungsi khusus; definisinya kita sajikan di sini.   fungsi injeksi  fungsi surjeksi  fungsi bijeksi   Misalkan suatu fungsi dari himpunan ke himpunan .   Fungsi merupakan injeksi jika setiap kali dan berada di dalam , berlaku . Secara ekuivalen, dengan menggunakan notasi fungsi, merupakan injeksi jika mengakibatkan .    Fungsi merupakan surjeksi jika untuk setiap , terdapat sedemikian sehingga berada di dalam . Secara ekuivalen, dengan menggunakan notasi fungsi, merupakan surjeksi jika untuk setiap terdapat sedemikian sehingga .    Fungsi merupakan bijeksi jika sekaligus merupakan injeksi dan surjeksi.        fungsi pembatasan   Misalkan suatu fungsi dari himpunan ke himpunan dan misalkan suatu subhimpunan dari . Pembatasan  pada adalah fungsi yang memenuhi .      Kita sering mendefinisikan fungsi dengan aturan, tetapi fungsi juga dapat didefinisikan melalui tabel atau grafik. Dalam aktivitas ini, kita akan bekerja dengan fungsi yang didefinisikan melalui aturan. Tujuan aktivitas ini adalah menunjukkan bahwa domain, kodomain, dan aturan yang menentukan keluaran sama-sama penting untuk menentukan apakah suatu fungsi merupakan injeksi dan\/atau surjeksi. Sebagai contoh, misalkan . (Perhatikan bahwa adalah fungsinya dan adalah citra oleh .) Perhatikan bahwa .  Pengamatan ini cukup untuk membuktikan bahwa fungsi bukan injeksi karena terdapat dua masukan berbeda yang menghasilkan keluaran yang sama.  Karena , kita mengetahui bahwa untuk setiap . Hal ini menyiratkan bahwa fungsi bukan surjeksi. Sebagai contoh, berada di dalam kodomain , sedangkan untuk setiap di dalam domain .    Kita dapat mengubah domain suatu fungsi sehingga fungsi tersebut didefinisikan pada subhimpunan dari domain semula. Fungsi semacam ini disebut pembatasan.  Pembatasan tersebut juga dinyatakan dengan notasi . Kita juga menyebut sebagai suatu perluasan dari . Misalkan didefinisikan oleh , dan misalkan , dengan menyatakan himpunan bilangan real positif. Jadi, memiliki kodomain yang sama dengan , tetapi domain yang berbeda.   Buktikan bahwa merupakan injeksi.   Apakah merupakan surjeksi? Berikan alasan untuk kesimpulan Anda.    Misalkan , dan misalkan didefinisikan oleh . Perhatikan bahwa fungsi menggunakan rumus yang sama dengan fungsi dan memiliki domain yang sama dengan , tetapi kodomainnya berbeda dari kodomain .   Jelaskan mengapa bukan injeksi.   Apakah merupakan surjeksi? Berikan alasan untuk kesimpulan Anda.    Misalkan . Definisikan dengan .   Buktikan atau berikan contoh tandingan: fungsi merupakan injeksi.   Buktikan atau berikan contoh tandingan: fungsi merupakan surjeksi.    Dalam aktivitas pendahuluan kita, rumus matematika yang sama digunakan untuk menentukan keluaran fungsi-fungsi tersebut. Namun:   Salah satu fungsi bukan injeksi maupun surjeksi.    Salah satu fungsi bukan injeksi, tetapi merupakan surjeksi.    Salah satu fungsi merupakan injeksi, tetapi bukan surjeksi.    Salah satu fungsi sekaligus merupakan injeksi dan surjeksi.     Hal ini menggambarkan fakta penting bahwa sifat injektif atau surjektif suatu fungsi tidak hanya bergantung pada rumus yang menentukan keluaran fungsi tersebut, tetapi juga pada domain dan kodomainnya.  Salah satu fungsi khusus yang penting dan selalu merupakan injeksi sekaligus surjeksi adalah fungsi identitas  fungsi identitas pada suatu himpunan. Jika adalah suatu himpunan, fungsi identitas pada dinyatakan dengan , dan untuk setiap .  "
},
{
  "id": "def_function",
  "level": "2",
  "url": "sec_func_intro.html#def_function",
  "type": "Definisi",
  "number": "2.1",
  "title": "",
  "body": " fungsi   Suatu fungsi  dari himpunan tak kosong ke himpunan adalah koleksi pasangan terurut sedemikian sehingga   untuk setiap , terdapat pasangan di dalam , dan    jika dan berada di dalam , maka .      "
},
{
  "id": "p-195",
  "level": "2",
  "url": "sec_func_intro.html#p-195",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "domain kodomain daerah hasil citra prapeta "
},
{
  "id": "definition-4",
  "level": "2",
  "url": "sec_func_intro.html#definition-4",
  "type": "Definisi",
  "number": "2.2",
  "title": "",
  "body": " fungsi injeksi  fungsi surjeksi  fungsi bijeksi   Misalkan suatu fungsi dari himpunan ke himpunan .   Fungsi merupakan injeksi jika setiap kali dan berada di dalam , berlaku . Secara ekuivalen, dengan menggunakan notasi fungsi, merupakan injeksi jika mengakibatkan .    Fungsi merupakan surjeksi jika untuk setiap , terdapat sedemikian sehingga berada di dalam . Secara ekuivalen, dengan menggunakan notasi fungsi, merupakan surjeksi jika untuk setiap terdapat sedemikian sehingga .    Fungsi merupakan bijeksi jika sekaligus merupakan injeksi dan surjeksi.      "
},
{
  "id": "definition-5",
  "level": "2",
  "url": "sec_func_intro.html#definition-5",
  "type": "Definisi",
  "number": "2.3",
  "title": "",
  "body": " fungsi pembatasan   Misalkan suatu fungsi dari himpunan ke himpunan dan misalkan suatu subhimpunan dari . Pembatasan  pada adalah fungsi yang memenuhi .   "
},
{
  "id": "exploration-2",
  "level": "2",
  "url": "sec_func_intro.html#exploration-2",
  "type": "Aktivitas Persiapan",
  "number": "2.1",
  "title": "",
  "body": "  Kita sering mendefinisikan fungsi dengan aturan, tetapi fungsi juga dapat didefinisikan melalui tabel atau grafik. Dalam aktivitas ini, kita akan bekerja dengan fungsi yang didefinisikan melalui aturan. Tujuan aktivitas ini adalah menunjukkan bahwa domain, kodomain, dan aturan yang menentukan keluaran sama-sama penting untuk menentukan apakah suatu fungsi merupakan injeksi dan\/atau surjeksi. Sebagai contoh, misalkan . (Perhatikan bahwa adalah fungsinya dan adalah citra oleh .) Perhatikan bahwa .  Pengamatan ini cukup untuk membuktikan bahwa fungsi bukan injeksi karena terdapat dua masukan berbeda yang menghasilkan keluaran yang sama.  Karena , kita mengetahui bahwa untuk setiap . Hal ini menyiratkan bahwa fungsi bukan surjeksi. Sebagai contoh, berada di dalam kodomain , sedangkan untuk setiap di dalam domain .    Kita dapat mengubah domain suatu fungsi sehingga fungsi tersebut didefinisikan pada subhimpunan dari domain semula. Fungsi semacam ini disebut pembatasan.  Pembatasan tersebut juga dinyatakan dengan notasi . Kita juga menyebut sebagai suatu perluasan dari . Misalkan didefinisikan oleh , dan misalkan , dengan menyatakan himpunan bilangan real positif. Jadi, memiliki kodomain yang sama dengan , tetapi domain yang berbeda.   Buktikan bahwa merupakan injeksi.   Apakah merupakan surjeksi? Berikan alasan untuk kesimpulan Anda.    Misalkan , dan misalkan didefinisikan oleh . Perhatikan bahwa fungsi menggunakan rumus yang sama dengan fungsi dan memiliki domain yang sama dengan , tetapi kodomainnya berbeda dari kodomain .   Jelaskan mengapa bukan injeksi.   Apakah merupakan surjeksi? Berikan alasan untuk kesimpulan Anda.    Misalkan . Definisikan dengan .   Buktikan atau berikan contoh tandingan: fungsi merupakan injeksi.   Buktikan atau berikan contoh tandingan: fungsi merupakan surjeksi.   "
},
{
  "id": "p-227",
  "level": "2",
  "url": "sec_func_intro.html#p-227",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "identitas "
},
{
  "id": "sec_comp_func",
  "level": "1",
  "url": "sec_comp_func.html",
  "type": "Bagian",
  "number": "",
  "title": "Komposisi Fungsi",
  "body": " Komposisi Fungsi  Dalam pembelajaran matematika sebelumnya, kita sering menjumlahkan dan mengalikan fungsi (misalnya, jika dan memetakan ke , maka dan ). Dalam topologi, pada umumnya kita tidak memperhatikan struktur aljabar apa pun yang mungkin dimiliki suatu himpunan. Karena itu, kita akan beralih dari penjumlahan dan perkalian, lalu memusatkan perhatian pada komposisi fungsi.  Gagasan dasar komposisi fungsi adalah bahwa, jika memungkinkan, keluaran suatu fungsi digunakan sebagai masukan suatu fungsi . Fungsi yang dihasilkan dapat disebut kemudian dan dinamakan komposit dengan . Notasi yang kita gunakan adalah (perhatikan urutannya  diterapkan lebih dahulu). Sebagai contoh, jika , keduanya memetakan ke , maka kita dapat menghitung sebagai berikut: .  Dalam hal ini, , yaitu keluaran fungsi , digunakan sebagai masukan bagi fungsi . Gagasan ini melandasi definisi formal komposisi dua fungsi.   komposisi fungsi   Misalkan , , dan himpunan tak kosong, serta misalkan dan fungsi. Komposit  dan adalah fungsi yang didefinisikan oleh untuk setiap     Fungsi kita sebut fungsi komposit, dan kita baca sebagai komposisi dari .    Misalkan , , dan . Definisikan , , dan dengan ,  .    Tentukan citra unsur-unsur di dalam oleh fungsi .    Tentukan citra unsur-unsur di dalam oleh fungsi .    Apakah di antara , , dan ada yang merupakan injeksi? Apakah di antara , , dan ada yang merupakan surjeksi?    Apakah merupakan injeksi? Apakah merupakan surjeksi? Jelaskan.    Apakah merupakan injeksi? Apakah merupakan surjeksi? Jelaskan.    Dalam , kita menanyakan apakah fungsi-fungsi komposit tertentu merupakan injeksi atau surjeksi, atau keduanya. Dalam matematika, lazim untuk menyelidiki apakah sifat tertentu suatu objek juga dimiliki oleh objek yang berkaitan dengannya. Secara khusus, kita mungkin ingin mengetahui apakah komposit dua fungsi injektif juga merupakan injeksi. (Tentu saja, kita dapat mengajukan pertanyaan serupa untuk surjeksi.) Pertanyaan-pertanyaan ini diselidiki dalam aktivitas berikutnya.    Diberikan himpunan , , , dan berikut: .    Susun suatu fungsi yang merupakan injeksi dan suatu fungsi yang merupakan injeksi. Dalam hal ini, apakah fungsi komposit merupakan injeksi? Jelaskan.    Susun suatu fungsi yang merupakan surjeksi dan suatu fungsi yang merupakan surjeksi. Dalam hal ini, apakah fungsi komposit merupakan surjeksi? Jelaskan.    Susun suatu fungsi yang merupakan bijeksi dan suatu fungsi yang merupakan bijeksi. Dalam hal ini, apakah fungsi komposit merupakan bijeksi? Jelaskan.    Dalam , kita menyelidiki beberapa sifat fungsi komposit yang berkaitan dengan injeksi, surjeksi, dan bijeksi. Teorema berikut merangkum hasil yang hendak diilustrasikan oleh penyelidikan tersebut.    Misalkan , , dan himpunan tak kosong, serta misalkan dan .   Jika dan keduanya merupakan injeksi, maka merupakan injeksi.    Jika dan keduanya merupakan surjeksi, maka merupakan surjeksi.    Jika dan keduanya merupakan bijeksi, maka merupakan bijeksi.         Buktikan bagian (1) dari .    Buktikan bagian (2) dari .    Mengapa bukti bagian (3) dari merupakan akibat langsung dari bagian (1) dan (2)?    "
},
{
  "id": "definition-6",
  "level": "2",
  "url": "sec_comp_func.html#definition-6",
  "type": "Definisi",
  "number": "2.4",
  "title": "",
  "body": " komposisi fungsi   Misalkan , , dan himpunan tak kosong, serta misalkan dan fungsi. Komposit  dan adalah fungsi yang didefinisikan oleh untuk setiap    "
},
{
  "id": "act_functions_1",
  "level": "2",
  "url": "sec_comp_func.html#act_functions_1",
  "type": "Kegiatan",
  "number": "2.2",
  "title": "",
  "body": "  Misalkan , , dan . Definisikan , , dan dengan ,  .    Tentukan citra unsur-unsur di dalam oleh fungsi .    Tentukan citra unsur-unsur di dalam oleh fungsi .    Apakah di antara , , dan ada yang merupakan injeksi? Apakah di antara , , dan ada yang merupakan surjeksi?    Apakah merupakan injeksi? Apakah merupakan surjeksi? Jelaskan.    Apakah merupakan injeksi? Apakah merupakan surjeksi? Jelaskan.   "
},
{
  "id": "act_composition2",
  "level": "2",
  "url": "sec_comp_func.html#act_composition2",
  "type": "Kegiatan",
  "number": "2.3",
  "title": "",
  "body": "  Diberikan himpunan , , , dan berikut: .    Susun suatu fungsi yang merupakan injeksi dan suatu fungsi yang merupakan injeksi. Dalam hal ini, apakah fungsi komposit merupakan injeksi? Jelaskan.    Susun suatu fungsi yang merupakan surjeksi dan suatu fungsi yang merupakan surjeksi. Dalam hal ini, apakah fungsi komposit merupakan surjeksi? Jelaskan.    Susun suatu fungsi yang merupakan bijeksi dan suatu fungsi yang merupakan bijeksi. Dalam hal ini, apakah fungsi komposit merupakan bijeksi? Jelaskan.   "
},
{
  "id": "thm_compositefunctions",
  "level": "2",
  "url": "sec_comp_func.html#thm_compositefunctions",
  "type": "Teorema",
  "number": "2.5",
  "title": "",
  "body": "  Misalkan , , dan himpunan tak kosong, serta misalkan dan .   Jika dan keduanya merupakan injeksi, maka merupakan injeksi.    Jika dan keduanya merupakan surjeksi, maka merupakan surjeksi.    Jika dan keduanya merupakan bijeksi, maka merupakan bijeksi.      "
},
{
  "id": "activity-9",
  "level": "2",
  "url": "sec_comp_func.html#activity-9",
  "type": "Kegiatan",
  "number": "2.4",
  "title": "",
  "body": "  Buktikan bagian (1) dari .    Buktikan bagian (2) dari .    Mengapa bukti bagian (3) dari merupakan akibat langsung dari bagian (1) dan (2)?   "
},
{
  "id": "sec_inv_func",
  "level": "1",
  "url": "sec_inv_func.html",
  "type": "Bagian",
  "number": "",
  "title": "Fungsi Invers",
  "body": " Fungsi Invers  Setelah mempelajari fungsi komposit, kita beralih ke gagasan penting lainnya: invers suatu fungsi. Dalam mata kuliah matematika sebelumnya, Anda mungkin telah mempelajari bahwa fungsi eksponensial (dengan basis ) dan fungsi logaritma natural saling berinvers. Hubungan ini mungkin pernah Anda lihat dinyatakan sebagai berikut: Untuk setiap dengan dan setiap ,   jika dan hanya jika . Perhatikan bahwa merupakan masukan dan merupakan keluaran bagi fungsi logaritma natural jika dan hanya jika merupakan masukan dan merupakan keluaran bagi fungsi eksponensial. Pada dasarnya, fungsi invers (dalam hal ini, fungsi eksponensial) membalik tindakan fungsi semula (dalam hal ini, fungsi logaritma natural). Dalam bentuk pasangan terurut (pasangan masukan-keluaran), hal ini berarti bahwa jika merupakan pasangan terurut dalam suatu fungsi, maka merupakan pasangan terurut dalam invers fungsi tersebut. Gagasan untuk menukar peran koordinat pertama dan kedua mendasari definisi invers suatu fungsi.   fungsi invers   Misalkan suatu fungsi. Invers dari , yang dinyatakan dengan , adalah himpunan pasangan terurut .    Perhatikan bahwa definisi ini tidak menyatakan bahwa merupakan fungsi. Sebaliknya, hanyalah subhimpunan dari . Dalam , kita akan menyelidiki syarat-syarat yang membuat invers suatu fungsi juga merupakan fungsi dari ke .    Misalkan , , dan . Definisikan     Tentukan invers setiap fungsi sebagai suatu himpunan pasangan terurut.    Apakah merupakan fungsi dari ke ? Jelaskan.   Apakah merupakan fungsi dari ke ? Jelaskan.   Apakah merupakan fungsi dari ke ? Jelaskan.    Buatlah konjektur tentang syarat-syarat pada suatu fungsi yang memastikan bahwa inversnya merupakan fungsi dari ke .    Hasil semestinya berupa teorema berikut.    Misalkan dan himpunan tak kosong, serta misalkan . Invers merupakan fungsi dari ke jika dan hanya jika merupakan bijeksi.    Garis besar bukti diberikan dalam aktivitas berikut.     merupakan pernyataan bikondisional, sehingga kita perlu membuktikan kedua arahnya. Misalkan dan himpunan tak kosong, serta misalkan .    Andaikan merupakan bijeksi. Kita akan membuktikan bahwa merupakan fungsi, yakni bahwa memenuhi syarat-syarat dalam .   Misalkan . Sifat apa dari yang memastikan bahwa untuk suatu ? Kesimpulan apa yang dapat kita tarik tentang ?   Sekarang misalkan , , dan andaikan bahwa . Apa yang ditunjukkan hal ini tentang pasangan-pasangan terurut yang harus termuat dalam ? Sifat apa dari yang memastikan bahwa ? Kesimpulan apa yang dapat kita tarik tentang ?    Sekarang andaikan merupakan fungsi dari ke . Kita akan membuktikan bahwa merupakan bijeksi.   Apa yang perlu ditunjukkan untuk membuktikan bahwa merupakan injeksi? Gunakan fakta bahwa merupakan fungsi untuk membuktikan bahwa merupakan injeksi.   Apa yang perlu ditunjukkan untuk membuktikan bahwa merupakan surjeksi? Gunakan fakta bahwa merupakan fungsi untuk membuktikan bahwa merupakan surjeksi.    Dalam keadaan ketika merupakan bijeksi dan merupakan fungsi dari ke , kita dapat menulis . Dalam hal ini, kita sering menyebut sebagai fungsi invertibel , dan biasanya kita tidak menggunakan penyajian pasangan terurut, baik untuk maupun . Alih-alih menulis , kita menulis , dan alih-alih menulis , kita menulis . Dengan menggunakan fakta bahwa jika dan hanya jika , sekarang kita dapat menulis jika dan hanya jika . memformalkan pengamatan ini.    Misalkan dan himpunan tak kosong, serta misalkan suatu bijeksi. Maka merupakan fungsi, dan untuk setiap dan , .    Hasil berikut memberikan informasi yang berguna tentang fungsi invers. Pembuktiannya diserahkan kepada .    Misalkan dan himpunan tak kosong, serta misalkan suatu bijeksi. Maka   Untuk setiap di dalam , .    Untuk setiap di dalam , .       Pertanyaan berikutnya adalah apa yang dapat kita katakan tentang komposisi bijeksi. Secara khusus, jika dan keduanya merupakan bijeksi, maka dan keduanya merupakan fungsi. Apakah pasti invertibel dan, jika demikian, apa bentuk ?    Misalkan dan keduanya merupakan bijeksi.    Mengapa kita mengetahui bahwa invertibel?    Sekarang kita menentukan invers . Kita mungkin tergoda untuk mengira bahwa adalah , tetapi komposit ini tidak didefinisikan karena memetakan ke dan memetakan ke . Namun, didefinisikan. Untuk membuktikan bahwa , kita perlu membuktikan bahwa dua fungsi tersebut sama. Bagaimana kita membuktikan bahwa dua fungsi sama?    Misalkan .   Sifat apa yang memastikan bahwa terdapat sedemikian sehingga ?   Sifat apa yang memastikan bahwa terdapat sedemikian sehingga ?   Unsur apakah ? Mengapa?   Unsur apakah ? Mengapa? Unsur apakah ? Mengapa?   Unsur apakah ? Mengapa? Kesimpulan apa yang dapat kita tarik tentang dan ? Jelaskan.    Hasil tercakup dalam teorema berikut.    Misalkan dan bijeksi. Maka merupakan bijeksi dan .    "
},
{
  "id": "sym_finverse",
  "level": "2",
  "url": "sec_inv_func.html#sym_finverse",
  "type": "Definisi",
  "number": "2.6",
  "title": "",
  "body": " fungsi invers   Misalkan suatu fungsi. Invers dari , yang dinyatakan dengan , adalah himpunan pasangan terurut .   "
},
{
  "id": "prog_exploringinverse",
  "level": "2",
  "url": "sec_inv_func.html#prog_exploringinverse",
  "type": "Kegiatan",
  "number": "2.5",
  "title": "",
  "body": "  Misalkan , , dan . Definisikan     Tentukan invers setiap fungsi sebagai suatu himpunan pasangan terurut.    Apakah merupakan fungsi dari ke ? Jelaskan.   Apakah merupakan fungsi dari ke ? Jelaskan.   Apakah merupakan fungsi dari ke ? Jelaskan.    Buatlah konjektur tentang syarat-syarat pada suatu fungsi yang memastikan bahwa inversnya merupakan fungsi dari ke .   "
},
{
  "id": "T_inverseandbijection",
  "level": "2",
  "url": "sec_inv_func.html#T_inverseandbijection",
  "type": "Teorema",
  "number": "2.7",
  "title": "",
  "body": "  Misalkan dan himpunan tak kosong, serta misalkan . Invers merupakan fungsi dari ke jika dan hanya jika merupakan bijeksi.   "
},
{
  "id": "activity-11",
  "level": "2",
  "url": "sec_inv_func.html#activity-11",
  "type": "Kegiatan",
  "number": "2.6",
  "title": "",
  "body": "   merupakan pernyataan bikondisional, sehingga kita perlu membuktikan kedua arahnya. Misalkan dan himpunan tak kosong, serta misalkan .    Andaikan merupakan bijeksi. Kita akan membuktikan bahwa merupakan fungsi, yakni bahwa memenuhi syarat-syarat dalam .   Misalkan . Sifat apa dari yang memastikan bahwa untuk suatu ? Kesimpulan apa yang dapat kita tarik tentang ?   Sekarang misalkan , , dan andaikan bahwa . Apa yang ditunjukkan hal ini tentang pasangan-pasangan terurut yang harus termuat dalam ? Sifat apa dari yang memastikan bahwa ? Kesimpulan apa yang dapat kita tarik tentang ?    Sekarang andaikan merupakan fungsi dari ke . Kita akan membuktikan bahwa merupakan bijeksi.   Apa yang perlu ditunjukkan untuk membuktikan bahwa merupakan injeksi? Gunakan fakta bahwa merupakan fungsi untuk membuktikan bahwa merupakan injeksi.   Apa yang perlu ditunjukkan untuk membuktikan bahwa merupakan surjeksi? Gunakan fakta bahwa merupakan fungsi untuk membuktikan bahwa merupakan surjeksi.   "
},
{
  "id": "p-272",
  "level": "2",
  "url": "sec_inv_func.html#p-272",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "fungsi invertibel "
},
{
  "id": "T_inversenotation",
  "level": "2",
  "url": "sec_inv_func.html#T_inversenotation",
  "type": "Teorema",
  "number": "2.8",
  "title": "",
  "body": "  Misalkan dan himpunan tak kosong, serta misalkan suatu bijeksi. Maka merupakan fungsi, dan untuk setiap dan , .   "
},
{
  "id": "C_inversecomposition",
  "level": "2",
  "url": "sec_inv_func.html#C_inversecomposition",
  "type": "Corollary",
  "number": "2.9",
  "title": "",
  "body": "  Misalkan dan himpunan tak kosong, serta misalkan suatu bijeksi. Maka   Untuk setiap di dalam , .    Untuk setiap di dalam , .      "
},
{
  "id": "act_comp_inverse",
  "level": "2",
  "url": "sec_inv_func.html#act_comp_inverse",
  "type": "Kegiatan",
  "number": "2.7",
  "title": "",
  "body": "  Misalkan dan keduanya merupakan bijeksi.    Mengapa kita mengetahui bahwa invertibel?    Sekarang kita menentukan invers . Kita mungkin tergoda untuk mengira bahwa adalah , tetapi komposit ini tidak didefinisikan karena memetakan ke dan memetakan ke . Namun, didefinisikan. Untuk membuktikan bahwa , kita perlu membuktikan bahwa dua fungsi tersebut sama. Bagaimana kita membuktikan bahwa dua fungsi sama?    Misalkan .   Sifat apa yang memastikan bahwa terdapat sedemikian sehingga ?   Sifat apa yang memastikan bahwa terdapat sedemikian sehingga ?   Unsur apakah ? Mengapa?   Unsur apakah ? Mengapa? Unsur apakah ? Mengapa?   Unsur apakah ? Mengapa? Kesimpulan apa yang dapat kita tarik tentang dan ? Jelaskan.   "
},
{
  "id": "compositionofbijections",
  "level": "2",
  "url": "sec_inv_func.html#compositionofbijections",
  "type": "Teorema",
  "number": "2.10",
  "title": "",
  "body": "  Misalkan dan bijeksi. Maka merupakan bijeksi dan .   "
},
{
  "id": "sec_fun_set",
  "level": "1",
  "url": "sec_fun_set.html",
  "type": "Bagian",
  "number": "",
  "title": "Fungsi dan Himpunan",
  "body": " Fungsi dan Himpunan  Kita menutup bagian ini dengan menghubungkan subhimpunan dan fungsi. Pertama, kita perkenalkan sedikit notasi. Jika adalah fungsi dari himpunan ke himpunan , dan jika adalah subhimpunan dari serta adalah subhimpunan dari , kita mendefinisikan dan sebagai , dan .  Kita menyebut sebagai citra himpunan di bawah , sedangkan adalah prapeta himpunan di bawah . Perhatikan bahwa didefinisikan untuk setiap fungsi, bukan hanya untuk fungsi yang mempunyai invers. Jadi, penting untuk dipahami bahwa penggunaan notasi tidak berarti bahwa mempunyai invers.  Ketika nanti kita membahas fungsi kontinu, kita perlu memahami perilaku suatu fungsi terhadap subhimpunan. Salah satu hasilnya diberikan dalam lema berikut.    Misalkan suatu fungsi, suatu koleksi subhimpunan dari yang diindeks oleh dalam himpunan indeks , dan suatu koleksi subhimpunan dari yang diindeks oleh dalam himpunan indeks . Maka    , dan     .       Misalkan suatu fungsi dan suatu koleksi subhimpunan dari yang diindeks oleh dalam himpunan indeks . Untuk membuktikan bagian 1, kita tunjukkan inklusi pada kedua arah.  Misalkan . Maka untuk suatu . Akibatnya, untuk suatu . Jadi, . Kita menyimpulkan bahwa .  Sekarang, misalkan . Maka untuk suatu . Karena , diperoleh . Jadi, . Kedua inklusi tersebut membuktikan bagian 1.  Untuk bagian 2, kita kembali menunjukkan inklusi pada kedua arah. Misalkan . Maka . Jadi, terdapat sedemikian sehingga . Ini berarti . Kita menyimpulkan bahwa .  Untuk inklusi sebaliknya, misalkan . Maka untuk suatu . Jadi, . Dengan demikian, . Jadi, . Kedua inklusi tersebut membuktikan bagian 2.    Pada tahap ini, wajar untuk bertanya apakah masih berlaku jika gabungan kita ganti dengan irisan. Pertanyaan itu kita serahkan kepada .  Hasil lainnya dibahas dalam kegiatan berikut.   Misalkan , , dan adalah himpunan, serta dan adalah fungsi. Misalkan suatu subhimpunan dari . Terdapat hubungan antara dan . Temukan dan buktikan hubungan tersebut.   "
},
{
  "id": "lem_functions_subsets",
  "level": "2",
  "url": "sec_fun_set.html#lem_functions_subsets",
  "type": "Lema",
  "number": "2.11",
  "title": "",
  "body": "  Misalkan suatu fungsi, suatu koleksi subhimpunan dari yang diindeks oleh dalam himpunan indeks , dan suatu koleksi subhimpunan dari yang diindeks oleh dalam himpunan indeks . Maka    , dan     .       Misalkan suatu fungsi dan suatu koleksi subhimpunan dari yang diindeks oleh dalam himpunan indeks . Untuk membuktikan bagian 1, kita tunjukkan inklusi pada kedua arah.  Misalkan . Maka untuk suatu . Akibatnya, untuk suatu . Jadi, . Kita menyimpulkan bahwa .  Sekarang, misalkan . Maka untuk suatu . Karena , diperoleh . Jadi, . Kedua inklusi tersebut membuktikan bagian 1.  Untuk bagian 2, kita kembali menunjukkan inklusi pada kedua arah. Misalkan . Maka . Jadi, terdapat sedemikian sehingga . Ini berarti . Kita menyimpulkan bahwa .  Untuk inklusi sebaliknya, misalkan . Maka untuk suatu . Jadi, . Dengan demikian, . Jadi, . Kedua inklusi tersebut membuktikan bagian 2.   "
},
{
  "id": "activity-13",
  "level": "2",
  "url": "sec_fun_set.html#activity-13",
  "type": "Kegiatan",
  "number": "2.8",
  "title": "",
  "body": " Misalkan , , dan adalah himpunan, serta dan adalah fungsi. Misalkan suatu subhimpunan dari . Terdapat hubungan antara dan . Temukan dan buktikan hubungan tersebut.  "
},
{
  "id": "sec_card_set",
  "level": "1",
  "url": "sec_card_set.html",
  "type": "Bagian",
  "number": "",
  "title": "Kardinalitas Himpunan",
  "body": " Kardinalitas Himpunan  Seberapa besar sebuah himpunan? Jika suatu himpunan berhingga, kita dapat menghitung banyaknya unsur dalam himpunan itu dan langsung menjawab pertanyaan tersebut. Jika suatu himpunan tak berhingga, pertanyaannya menjadi sedikit lebih rumit. Sebagai contoh, seberapa besar ? Seberapa besar ? Karena adalah subhimpunan dari , kita mungkin mengira bahwa memuat lebih banyak unsur daripada . Namun, tak berhingga; jadi, mungkinkah suatu himpunan mempunyai lebih banyak unsur daripada himpunan bilangan bulat? Kita tidak akan menjawab pertanyaan itu dalam bagian ini, tetapi pertanyaan tersebut menarik untuk direnungkan.  Jika dua himpunan berhingga memiliki banyak unsur yang sama, wajar jika kita mengatakan bahwa kedua himpunan itu sama besar. Bagaimana gagasan ini dapat kita perluas ke himpunan tak berhingga? Jika dua himpunan berhingga memiliki banyak unsur yang sama, kita dapat memasangkan setiap unsur dalam satu himpunan dengan tepat satu unsur dalam himpunan lainnya. Inilah tepatnya yang dilakukan oleh suatu bijeksi. Jadi, suatu himpunan dengan unsur dapat dipasangkan dengan himpunan , dengan suatu bilangan bulat positif. Dengan cara inilah kita dapat mendefinisikan himpunan berhingga.   himpunan berhingga   Suatu himpunan disebut berhingga jika atau terdapat suatu bijeksi yang memetakan ke himpunan untuk suatu bilangan bulat positif .     kardinalitas himpunan Jika , kita mengatakan bahwa mempunyai kardinalitas  . Jika terdapat suatu bijeksi dari ke himpunan , kita mengatakan bahwa mempunyai kardinalitas . Jika tidak ada bilangan bulat positif sedemikian sehingga terdapat bijeksi dari himpunan ke , kita mengatakan bahwa adalah himpunan tak berhingga dan bahwa mempunyai kardinalitas tak berhingga. Kita menggunakan istilah kardinalitas alih-alih banyaknya unsur karena kita tidak dapat benar-benar menghitung banyaknya unsur dalam suatu himpunan tak berhingga. Kardinalitas himpunan (yakni banyaknya unsur dalam himpunan tersebut) dinotasikan dengan . Sebagai latihan, tunjukkan bahwa jika dan adalah himpunan dengan dan , maka jika dan hanya jika terdapat suatu bijeksi . Hal ini menunjukkan bahwa kardinalitas terdefinisi dengan baik. Karena komposisi dua bijeksi merupakan bijeksi dan invers suatu bijeksi juga merupakan bijeksi, jika terdapat suatu bijeksi dari himpunan ke dan suatu bijeksi dari himpunan ke untuk suatu bilangan bulat positif , maka terdapat suatu bijeksi antara dan . Dengan gagasan ini, kita mengatakan bahwa dua himpunan (baik berhingga maupun tak berhingga) mempunyai kardinalitas yang sama jika terdapat suatu bijeksi antara kedua himpunan tersebut. Kita akan membahas kardinalitas secara lebih terperinci nanti.  "
},
{
  "id": "definition-8",
  "level": "2",
  "url": "sec_card_set.html#definition-8",
  "type": "Definisi",
  "number": "2.12",
  "title": "",
  "body": " himpunan berhingga   Suatu himpunan disebut berhingga jika atau terdapat suatu bijeksi yang memetakan ke himpunan untuk suatu bilangan bulat positif .   "
},
{
  "id": "p-307",
  "level": "2",
  "url": "sec_card_set.html#p-307",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "kardinalitas tak berhingga kardinalitas "
},
{
  "id": "sec_func_summ",
  "level": "1",
  "url": "sec_func_summ.html",
  "type": "Bagian",
  "number": "",
  "title": "Ringkasan",
  "body": " Ringkasan  Gagasan penting yang telah kita bahas dalam bagian ini meliputi hal-hal berikut.   Fungsi dari himpunan tak kosong ke himpunan adalah suatu koleksi pasangan terurut sedemikian sehingga untuk setiap terdapat pasangan dalam , dan jika serta berada dalam , maka . Jika suatu fungsi, kita menggunakan notasi untuk menyatakan bahwa .    Jika adalah fungsi dari ke , himpunan merupakan domain fungsi tersebut.    Jika adalah fungsi dari ke , himpunan merupakan kodomain fungsi tersebut. Himpunan merupakan daerah hasil fungsi tersebut. Jadi, daerah hasil suatu fungsi adalah subhimpunan dari kodomainnya.    Fungsi dari himpunan ke himpunan merupakan injeksi jika kesamaan untuk , selalu mengakibatkan . Fungsi merupakan surjeksi jika, untuk setiap , terdapat sedemikian sehingga .    Jika adalah fungsi dari himpunan ke himpunan dan adalah fungsi dari ke himpunan , komposit merupakan fungsi dari ke yang didefinisikan oleh untuk setiap .    Fungsi dari himpunan ke himpunan merupakan bijeksi jika sekaligus merupakan surjeksi dan injeksi. Jika merupakan bijeksi dari ke , maka mempunyai invers yang didefinisikan oleh ketika .    Jika adalah fungsi dari himpunan ke himpunan , dan jika adalah subhimpunan dari , citra di bawah adalah himpunan , dan jika adalah subhimpunan dari , prapeta adalah himpunan .    Sifat-sifat penting yang menghubungkan citra dan prapeta himpunan dengan gabungan himpunan adalah sebagai berikut. Jika adalah fungsi dari himpunan ke himpunan , jika adalah suatu koleksi subhimpunan dari yang diindeks oleh dalam himpunan indeks , dan adalah suatu koleksi subhimpunan dari yang diindeks oleh dalam himpunan indeks , maka    , dan     .        "
},
{
  "id": "sec_func_exer",
  "level": "1",
  "url": "sec_func_exer.html",
  "type": "Latihan",
  "number": "",
  "title": "Latihan",
  "body": "  Carilah fungsi sedemikian sehingga setiap unsur kodomain memiliki tepat satu prapeta.   Carilah fungsi sedemikian sehingga setiap unsur kodomain memiliki setidaknya dua prapeta.   Carilah fungsi sedemikian sehingga setiap unsur memiliki tepat dua prapeta.   Carilah fungsi sedemikian sehingga terdapat sebuah unsur kodomain yang memiliki tepat tiga prapeta dan sebuah unsur kodomain lain yang memiliki tepat dua prapeta.   Carilah fungsi sedemikian sehingga terdapat sebuah unsur kodomain yang memiliki tak berhingga banyak prapeta.    Untuk setiap fungsi berikut, tentukan apakah fungsi tersebut merupakan injeksi, surjeksi, bijeksi, atau bukan salah satu di antaranya. Ingatlah untuk memperhatikan dengan cermat domain dan kodomain dalam setiap kasus. Berikan alasan untuk semua kesimpulan Anda.    didefinisikan oleh , untuk setiap     didefinisikan oleh , untuk setiap     didefinisikan oleh , untuk setiap     didefinisikan oleh , untuk setiap     didefinisikan oleh untuk setiap , dengan     didefinisikan oleh untuk setiap     Misalkan dan , lalu definisikan sebagaimana diberikan dalam Tabel .   Fungsi dari ke     1  2  3  4  5  6  7  8  9  10                   Apakah merupakan injeksi? Apakah merupakan surjeksi? Jelaskan.   Carilah subhimpunan terbesar dari (terbesar dalam hal banyaknya unsur ) sedemikian sehingga merupakan injeksi.   Carilah subhimpunan dari sedemikian sehingga fungsi dengan aturan yang sama, dipandang sebagai , merupakan surjeksi.   Carilah subhimpunan dari dan dari sedemikian sehingga merupakan bijeksi.    Misalkan dan merupakan himpunan yang masing-masing memiliki setidaknya dua unsur berbeda.   Gambarkan suatu subhimpunan yang merupakan hasil kali Kartesius antara suatu subhimpunan dari dan suatu subhimpunan dari .   Tunjukkan bahwa terdapat suatu subhimpunan yang bukan merupakan hasil kali Kartesius antara suatu subhimpunan dari dan suatu subhimpunan dari . [Dengan demikian, tidak setiap subhimpunan dari suatu hasil kali Kartesius merupakan hasil kali Kartesius dari sepasang subhimpunan.]    Kardinalitas suatu himpunan berhingga didefinisikan sebagai banyaknya unsur himpunan tersebut. Kita menyatakan kardinalitas himpunan dengan . Misalkan dan merupakan himpunan dengan dan untuk bilangan bulat positif dan . Buktikan bahwa terdapat bijeksi jika dan hanya jika .    Misalkan dan merupakan himpunan dan merupakan fungsi.   Misalkan merupakan subhimpunan dari . Tunjukkan bahwa . Buatlah contoh untuk menunjukkan bahwa secara umum, .   Untuk menunjukkan bahwa kedua himpunan tersebut tidak sama, pertimbangkan himpunan dan yang masing-masing memiliki dua unsur.   Misalkan merupakan subhimpunan dari . Tunjukkan bahwa . Buatlah contoh untuk menunjukkan bahwa secara umum, .   Untuk menunjukkan bahwa kedua himpunan tersebut tidak sama, pertimbangkan himpunan dan yang masing-masing memiliki dua unsur.   Buktikan bahwa merupakan surjeksi jika dan hanya jika untuk setiap subhimpunan dari .   Buktikan bahwa merupakan injeksi jika dan hanya jika untuk setiap subhimpunan dari .    Misalkan merupakan fungsi dan merupakan koleksi subhimpunan dari yang diindeks oleh dalam himpunan indeks , serta merupakan koleksi subhimpunan dari yang diindeks oleh dalam himpunan indeks . Buktikan atau sangkal setiap pernyataan berikut. Jika suatu pernyataan tidak benar, apakah salah satu arah inklusi berlaku? Buktikan jawaban Anda.            Misalkan dan merupakan himpunan tak kosong, dan merupakan bijeksi. Buktikan bahwa   Untuk setiap dalam , .   Untuk setiap dalam , .    Misalkan , , dan merupakan himpunan, serta dan merupakan fungsi. Misalkan merupakan subhimpunan dari . Tunjukkan bahwa .    Misalkan dan merupakan himpunan tak kosong, dan misalkan . Definisikan dengan , dengan . Kita menyebut sebagai proyeksi dari ke . Misalkan dan merupakan himpunan tak kosong, dan misalkan . Andaikan bahwa untuk setiap terdapat fungsi . Sebagai contoh, misalkan dan . Kita kemudian dapat mendefinisikan dengan untuk yang bernilai ataupun .   Buktikan bahwa merupakan surjeksi untuk setiap .   Buktikan bahwa terdapat tepat satu fungsi sedemikian sehingga untuk setiap . (Perhatikan bahwa salah satu memetakan ke , sedangkan yang lain memetakan ke .)   Fungsi dari bagian (b) dinyatakan dengan . Misalkan dan merupakan dua himpunan tak kosong, dan misalkan . Andaikan bahwa terdapat fungsi untuk setiap . Tunjukkan bahwa .   Andaikan setiap memiliki invers . Tunjukkan bahwa .    Misalkan merupakan himpunan bilangan bulat positif. Definisikan sebagai berikut: Untuk setiap , tetapkan . Apakah fungsi merupakan injeksi? Apakah fungsi merupakan surjeksi? Berikan alasan untuk kesimpulan Anda.   Mulailah dengan menghitung beberapa keluaran fungsi sebelum mencoba menulis bukti. Saat menyelidiki apakah fungsi tersebut merupakan injeksi, ada baiknya Anda membagi kasus menurut apakah masukannya genap atau ganjil. Saat menyelidiki apakah merupakan surjeksi, pertimbangkan pembagian kasus menurut apakah keluarannya positif atau kurang dari atau sama dengan nol.    Operasi pada himpunan adalah fungsi dari ke yang, untuk pasangan , menetapkan unsur dalam . Sebagai contoh, penjumlahan bilangan bulat dapat didefinisikan sebagai fungsi yang memetakan pasangan ke bilangan bulat .   Apakah fungsi merupakan injeksi? Berikan alasan untuk kesimpulan Anda.   Apakah fungsi merupakan surjeksi? Berikan alasan untuk kesimpulan Anda.    Misalkan , , dan merupakan himpunan dan serta merupakan fungsi.   Benarkah bahwa jika merupakan injeksi, maka dan keduanya merupakan injeksi? Jika jawabannya tidak, adakah syarat yang harus dipenuhi oleh atau jika merupakan injeksi? Buktikan jawaban Anda.   Benarkah bahwa jika merupakan surjeksi, maka dan keduanya merupakan surjeksi? Jika jawabannya tidak, adakah syarat yang harus dipenuhi oleh atau jika merupakan surjeksi? Buktikan jawaban Anda.    Apakah komposisi fungsi merupakan operasi komutatif? Buktikan jawaban Anda.   Apakah komposisi fungsi merupakan operasi asosiatif? Buktikan jawaban Anda.    Definisikan dengan untuk setiap . Tuliskan invers dari sebagai himpunan pasangan terurut, dan jelaskan mengapa bukan fungsi.   Definisikan dengan untuk setiap . Tuliskan invers dari sebagai himpunan pasangan terurut, dan jelaskan mengapa merupakan fungsi.   Mungkinkah kita menuliskan rumus untuk , dengan ? Jawaban atas pertanyaan ini bergantung pada apakah akar pangkat tiga dari unsur-unsur dapat didefinisikan. Ingatlah bahwa untuk bilangan real , kita mendefinisikan akar pangkat tiga dari sebagai bilangan real sedemikian sehingga . Dengan kata lain, jika dan hanya jika . Dengan menggunakan gagasan ini, mungkinkah kita mendefinisikan akar pangkat tiga dari setiap unsur ? Jika ya, tentukan , , , , dan .   Sekarang jawablah pertanyaan yang diajukan pada awal bagian (c). Jika memungkinkan, tentukan rumus untuk dengan .    Misalkan merupakan himpunan semua fungsi yang kontinu pada (gunakan kembali pengetahuan Anda tentang fungsi kontinu dari kalkulus untuk soal ini). Misalkan merupakan subhimpunan dari yang terdiri atas semua fungsi dengan turunan yang kontinu pada . Misalkan merupakan subhimpunan dari yang terdiri atas semua fungsi yang bernilai 0 di .   Berikan contoh fungsi yang berada dalam , tetapi tidak dalam , dengan .   Berikan contoh fungsi yang berada dalam , tetapi tidak dalam , dengan .   Berikan contoh fungsi yang berada dalam dengan .   Misalkan didefinisikan oleh . Apakah fungsi invertibel? Berikan alasan untuk jawaban Anda.   Untuk setiap fungsi , misalkan merupakan fungsi yang didefinisikan oleh untuk .   Tunjukkan bahwa memetakan ke .   Tunjukkan bahwa invertibel dengan mencari fungsi sedemikian sehingga dan merupakan fungsi invers satu sama lain.    Misalkan suatu fungsi. Untuk setiap pernyataan berikut, nyatakan “benar” jika pernyataan tersebut selalu benar. Jika pernyataan tersebut hanya kadang-kadang benar atau tidak pernah benar, nyatakan “salah” dan berikan contoh konkret yang menunjukkan bahwa pernyataan tersebut salah. Jika suatu pernyataan benar, jelaskan alasannya.   Jika merupakan subhimpunan dari , maka .   Jika merupakan subhimpunan dari , maka .   Jika merupakan subhimpunan dari , maka .   Jika merupakan subhimpunan dari , maka .   Jika dan merupakan subhimpunan dari dengan , maka .   Jika dan merupakan subhimpunan dari dengan , maka .   Jika dan merupakan subhimpunan dari dengan , maka .   Jika dan merupakan subhimpunan dari , maka .   Jika dan merupakan subhimpunan dari , maka .   Jika dan merupakan subhimpunan dari , maka .   Jika dan merupakan subhimpunan dari , maka .   Jika dan merupakan subhimpunan dari , maka .   Jika dan merupakan subhimpunan dari , maka .   "
},
{
  "id": "exercise-11",
  "level": "2",
  "url": "sec_func_exer.html#exercise-11",
  "type": "Latihan",
  "number": "1",
  "title": "",
  "body": " Carilah fungsi sedemikian sehingga setiap unsur kodomain memiliki tepat satu prapeta.   Carilah fungsi sedemikian sehingga setiap unsur kodomain memiliki setidaknya dua prapeta.   Carilah fungsi sedemikian sehingga setiap unsur memiliki tepat dua prapeta.   Carilah fungsi sedemikian sehingga terdapat sebuah unsur kodomain yang memiliki tepat tiga prapeta dan sebuah unsur kodomain lain yang memiliki tepat dua prapeta.   Carilah fungsi sedemikian sehingga terdapat sebuah unsur kodomain yang memiliki tak berhingga banyak prapeta.  "
},
{
  "id": "exer_forexample",
  "level": "2",
  "url": "sec_func_exer.html#exer_forexample",
  "type": "Latihan",
  "number": "2",
  "title": "",
  "body": " Untuk setiap fungsi berikut, tentukan apakah fungsi tersebut merupakan injeksi, surjeksi, bijeksi, atau bukan salah satu di antaranya. Ingatlah untuk memperhatikan dengan cermat domain dan kodomain dalam setiap kasus. Berikan alasan untuk semua kesimpulan Anda.    didefinisikan oleh , untuk setiap     didefinisikan oleh , untuk setiap     didefinisikan oleh , untuk setiap     didefinisikan oleh , untuk setiap     didefinisikan oleh untuk setiap , dengan     didefinisikan oleh untuk setiap   "
},
{
  "id": "exercise-13",
  "level": "2",
  "url": "sec_func_exer.html#exercise-13",
  "type": "Latihan",
  "number": "3",
  "title": "",
  "body": " Misalkan dan , lalu definisikan sebagaimana diberikan dalam Tabel .   Fungsi dari ke     1  2  3  4  5  6  7  8  9  10                   Apakah merupakan injeksi? Apakah merupakan surjeksi? Jelaskan.   Carilah subhimpunan terbesar dari (terbesar dalam hal banyaknya unsur ) sedemikian sehingga merupakan injeksi.   Carilah subhimpunan dari sedemikian sehingga fungsi dengan aturan yang sama, dipandang sebagai , merupakan surjeksi.   Carilah subhimpunan dari dan dari sedemikian sehingga merupakan bijeksi.  "
},
{
  "id": "exercise-14",
  "level": "2",
  "url": "sec_func_exer.html#exercise-14",
  "type": "Latihan",
  "number": "4",
  "title": "",
  "body": " Misalkan dan merupakan himpunan yang masing-masing memiliki setidaknya dua unsur berbeda.   Gambarkan suatu subhimpunan yang merupakan hasil kali Kartesius antara suatu subhimpunan dari dan suatu subhimpunan dari .   Tunjukkan bahwa terdapat suatu subhimpunan yang bukan merupakan hasil kali Kartesius antara suatu subhimpunan dari dan suatu subhimpunan dari . [Dengan demikian, tidak setiap subhimpunan dari suatu hasil kali Kartesius merupakan hasil kali Kartesius dari sepasang subhimpunan.]  "
},
{
  "id": "exercise-15",
  "level": "2",
  "url": "sec_func_exer.html#exercise-15",
  "type": "Latihan",
  "number": "5",
  "title": "",
  "body": " Kardinalitas suatu himpunan berhingga didefinisikan sebagai banyaknya unsur himpunan tersebut. Kita menyatakan kardinalitas himpunan dengan . Misalkan dan merupakan himpunan dengan dan untuk bilangan bulat positif dan . Buktikan bahwa terdapat bijeksi jika dan hanya jika .  "
},
{
  "id": "exercise-16",
  "level": "2",
  "url": "sec_func_exer.html#exercise-16",
  "type": "Latihan",
  "number": "6",
  "title": "",
  "body": " Misalkan dan merupakan himpunan dan merupakan fungsi.   Misalkan merupakan subhimpunan dari . Tunjukkan bahwa . Buatlah contoh untuk menunjukkan bahwa secara umum, .   Untuk menunjukkan bahwa kedua himpunan tersebut tidak sama, pertimbangkan himpunan dan yang masing-masing memiliki dua unsur.   Misalkan merupakan subhimpunan dari . Tunjukkan bahwa . Buatlah contoh untuk menunjukkan bahwa secara umum, .   Untuk menunjukkan bahwa kedua himpunan tersebut tidak sama, pertimbangkan himpunan dan yang masing-masing memiliki dua unsur.   Buktikan bahwa merupakan surjeksi jika dan hanya jika untuk setiap subhimpunan dari .   Buktikan bahwa merupakan injeksi jika dan hanya jika untuk setiap subhimpunan dari .  "
},
{
  "id": "ex_intersection_image",
  "level": "2",
  "url": "sec_func_exer.html#ex_intersection_image",
  "type": "Latihan",
  "number": "7",
  "title": "",
  "body": " Misalkan merupakan fungsi dan merupakan koleksi subhimpunan dari yang diindeks oleh dalam himpunan indeks , serta merupakan koleksi subhimpunan dari yang diindeks oleh dalam himpunan indeks . Buktikan atau sangkal setiap pernyataan berikut. Jika suatu pernyataan tidak benar, apakah salah satu arah inklusi berlaku? Buktikan jawaban Anda.          "
},
{
  "id": "ex_inverse_composite",
  "level": "2",
  "url": "sec_func_exer.html#ex_inverse_composite",
  "type": "Latihan",
  "number": "8",
  "title": "",
  "body": " Misalkan dan merupakan himpunan tak kosong, dan merupakan bijeksi. Buktikan bahwa   Untuk setiap dalam , .   Untuk setiap dalam , .  "
},
{
  "id": "ex_inverse_composite_sets",
  "level": "2",
  "url": "sec_func_exer.html#ex_inverse_composite_sets",
  "type": "Latihan",
  "number": "9",
  "title": "",
  "body": " Misalkan , , dan merupakan himpunan, serta dan merupakan fungsi. Misalkan merupakan subhimpunan dari . Tunjukkan bahwa .  "
},
{
  "id": "exercise-20",
  "level": "2",
  "url": "sec_func_exer.html#exercise-20",
  "type": "Latihan",
  "number": "10",
  "title": "",
  "body": " Misalkan dan merupakan himpunan tak kosong, dan misalkan . Definisikan dengan , dengan . Kita menyebut sebagai proyeksi dari ke . Misalkan dan merupakan himpunan tak kosong, dan misalkan . Andaikan bahwa untuk setiap terdapat fungsi . Sebagai contoh, misalkan dan . Kita kemudian dapat mendefinisikan dengan untuk yang bernilai ataupun .   Buktikan bahwa merupakan surjeksi untuk setiap .   Buktikan bahwa terdapat tepat satu fungsi sedemikian sehingga untuk setiap . (Perhatikan bahwa salah satu memetakan ke , sedangkan yang lain memetakan ke .)   Fungsi dari bagian (b) dinyatakan dengan . Misalkan dan merupakan dua himpunan tak kosong, dan misalkan . Andaikan bahwa terdapat fungsi untuk setiap . Tunjukkan bahwa .   Andaikan setiap memiliki invers . Tunjukkan bahwa .  "
},
{
  "id": "exercise-21",
  "level": "2",
  "url": "sec_func_exer.html#exercise-21",
  "type": "Latihan",
  "number": "11",
  "title": "",
  "body": " Misalkan merupakan himpunan bilangan bulat positif. Definisikan sebagai berikut: Untuk setiap , tetapkan . Apakah fungsi merupakan injeksi? Apakah fungsi merupakan surjeksi? Berikan alasan untuk kesimpulan Anda.   Mulailah dengan menghitung beberapa keluaran fungsi sebelum mencoba menulis bukti. Saat menyelidiki apakah fungsi tersebut merupakan injeksi, ada baiknya Anda membagi kasus menurut apakah masukannya genap atau ganjil. Saat menyelidiki apakah merupakan surjeksi, pertimbangkan pembagian kasus menurut apakah keluarannya positif atau kurang dari atau sama dengan nol.  "
},
{
  "id": "exercise-22",
  "level": "2",
  "url": "sec_func_exer.html#exercise-22",
  "type": "Latihan",
  "number": "12",
  "title": "",
  "body": " Operasi pada himpunan adalah fungsi dari ke yang, untuk pasangan , menetapkan unsur dalam . Sebagai contoh, penjumlahan bilangan bulat dapat didefinisikan sebagai fungsi yang memetakan pasangan ke bilangan bulat .   Apakah fungsi merupakan injeksi? Berikan alasan untuk kesimpulan Anda.   Apakah fungsi merupakan surjeksi? Berikan alasan untuk kesimpulan Anda.  "
},
{
  "id": "exercise-23",
  "level": "2",
  "url": "sec_func_exer.html#exercise-23",
  "type": "Latihan",
  "number": "13",
  "title": "",
  "body": " Misalkan , , dan merupakan himpunan dan serta merupakan fungsi.   Benarkah bahwa jika merupakan injeksi, maka dan keduanya merupakan injeksi? Jika jawabannya tidak, adakah syarat yang harus dipenuhi oleh atau jika merupakan injeksi? Buktikan jawaban Anda.   Benarkah bahwa jika merupakan surjeksi, maka dan keduanya merupakan surjeksi? Jika jawabannya tidak, adakah syarat yang harus dipenuhi oleh atau jika merupakan surjeksi? Buktikan jawaban Anda.  "
},
{
  "id": "exercise-24",
  "level": "2",
  "url": "sec_func_exer.html#exercise-24",
  "type": "Latihan",
  "number": "14",
  "title": "",
  "body": " Apakah komposisi fungsi merupakan operasi komutatif? Buktikan jawaban Anda.   Apakah komposisi fungsi merupakan operasi asosiatif? Buktikan jawaban Anda.  "
},
{
  "id": "exercise-25",
  "level": "2",
  "url": "sec_func_exer.html#exercise-25",
  "type": "Latihan",
  "number": "15",
  "title": "",
  "body": " Definisikan dengan untuk setiap . Tuliskan invers dari sebagai himpunan pasangan terurut, dan jelaskan mengapa bukan fungsi.   Definisikan dengan untuk setiap . Tuliskan invers dari sebagai himpunan pasangan terurut, dan jelaskan mengapa merupakan fungsi.   Mungkinkah kita menuliskan rumus untuk , dengan ? Jawaban atas pertanyaan ini bergantung pada apakah akar pangkat tiga dari unsur-unsur dapat didefinisikan. Ingatlah bahwa untuk bilangan real , kita mendefinisikan akar pangkat tiga dari sebagai bilangan real sedemikian sehingga . Dengan kata lain, jika dan hanya jika . Dengan menggunakan gagasan ini, mungkinkah kita mendefinisikan akar pangkat tiga dari setiap unsur ? Jika ya, tentukan , , , , dan .   Sekarang jawablah pertanyaan yang diajukan pada awal bagian (c). Jika memungkinkan, tentukan rumus untuk dengan .  "
},
{
  "id": "exercise-26",
  "level": "2",
  "url": "sec_func_exer.html#exercise-26",
  "type": "Latihan",
  "number": "16",
  "title": "",
  "body": " Misalkan merupakan himpunan semua fungsi yang kontinu pada (gunakan kembali pengetahuan Anda tentang fungsi kontinu dari kalkulus untuk soal ini). Misalkan merupakan subhimpunan dari yang terdiri atas semua fungsi dengan turunan yang kontinu pada . Misalkan merupakan subhimpunan dari yang terdiri atas semua fungsi yang bernilai 0 di .   Berikan contoh fungsi yang berada dalam , tetapi tidak dalam , dengan .   Berikan contoh fungsi yang berada dalam , tetapi tidak dalam , dengan .   Berikan contoh fungsi yang berada dalam dengan .   Misalkan didefinisikan oleh . Apakah fungsi invertibel? Berikan alasan untuk jawaban Anda.   Untuk setiap fungsi , misalkan merupakan fungsi yang didefinisikan oleh untuk .   Tunjukkan bahwa memetakan ke .   Tunjukkan bahwa invertibel dengan mencari fungsi sedemikian sehingga dan merupakan fungsi invers satu sama lain.  "
},
{
  "id": "exercise-27",
  "level": "2",
  "url": "sec_func_exer.html#exercise-27",
  "type": "Latihan",
  "number": "17",
  "title": "",
  "body": " Misalkan suatu fungsi. Untuk setiap pernyataan berikut, nyatakan “benar” jika pernyataan tersebut selalu benar. Jika pernyataan tersebut hanya kadang-kadang benar atau tidak pernah benar, nyatakan “salah” dan berikan contoh konkret yang menunjukkan bahwa pernyataan tersebut salah. Jika suatu pernyataan benar, jelaskan alasannya.   Jika merupakan subhimpunan dari , maka .   Jika merupakan subhimpunan dari , maka .   Jika merupakan subhimpunan dari , maka .   Jika merupakan subhimpunan dari , maka .   Jika dan merupakan subhimpunan dari dengan , maka .   Jika dan merupakan subhimpunan dari dengan , maka .   Jika dan merupakan subhimpunan dari dengan , maka .   Jika dan merupakan subhimpunan dari , maka .   Jika dan merupakan subhimpunan dari , maka .   Jika dan merupakan subhimpunan dari , maka .   Jika dan merupakan subhimpunan dari , maka .   Jika dan merupakan subhimpunan dari , maka .   Jika dan merupakan subhimpunan dari , maka .  "
},
{
  "id": "sec_metric_space_intro",
  "level": "1",
  "url": "sec_metric_space_intro.html",
  "type": "Bagian",
  "number": "",
  "title": "Pendahuluan",
  "body": " Pendahuluan  Ruang metrik merupakan contoh khusus ruang topologis. Ruang metrik adalah ruang yang dilengkapi dengan suatu metrik. Metrik adalah fungsi yang mengukur jarak antara titik-titik dalam ruang metrik.  Kita sudah mengenal satu metrik khusus, yaitu metrik Euklides pada , yang didefinisikan oleh .   Jarak Euklides antara dan , serta lingkaran satuan Euklides pada .  Gambar dua panel. Panel kiri memperlihatkan ruas garis horizontal yang menghubungkan titik berlabel dan . Panel kanan memperlihatkan sumbu koordinat dan sebuah lingkaran yang berpusat di titik asal serta memotong sumbu horizontal pada titik berjarak satu satuan dari pusat.   Dengan metrik ini, jarak antara dua titik dan adalah panjang ruas garis yang menghubungkan kedua titik tersebut, sedangkan lingkaran satuannya (himpunan titik yang berjarak 1 dari titik asal) berbentuk seperti lingkaran yang biasa kita bayangkan, sebagaimana diperlihatkan dalam .  Seperti yang akan kita lihat, ada banyak metrik lain yang dapat didefinisikan pada ataupun pada himpunan-himpunan lain.    Misalkan dan bilangan real. Maka .    Misalkan dan bilangan real. Untuk membuktikan lemma ini, kita meninjau beberapa kasus.   Kasus 1: dan  Dalam kasus ini, tak negatif sehingga , , dan . Dengan demikian, .    Kasus 2: dan  Dalam kasus ini, dan , dengan dan tak negatif. Berdasarkan Kasus 1, .    Kasus 3: Salah satu dari atau positif dan yang lainnya negatif  Tanpa mengurangi keumuman, kita andaikan dan . Sekali lagi, kita meninjau beberapa kasus. Perhatikan bahwa mengakibatkan .   Andaikan . Maka , sehingga . Akibatnya, .    Kasus terakhir terjadi ketika . Dalam kasus ini, , sehingga . Maka . Terakhir, mengakibatkan . Jadi, dan .      Ini membuktikan lemma kita untuk setiap pasangan , .     metrik taksi   Perhatikan fungsi yang memasangkan setiap pasangan titik dalam dengan bilangan real .  Fungsi ini kadang-kadang disebut metrik taksi atau jarak taksi karena jarak antara titik dan dapat dibayangkan sebagai jarak yang ditempuh dengan menyusuri ruas-ruas jalan kota, alih-alih bergerak langsung dari titik ke titik .  Setiap fungsi jarak seharusnya memenuhi sifat-sifat tertentu: jarak antara dua titik tidak boleh negatif; jarak dari titik ke titik harus sama dengan jarak dari titik ke titik ; jarak terpendek antara titik dan tidak boleh melebihi jumlah jarak dari ke suatu titik dan jarak dari ke ; dan jarak antara dua titik hanya boleh bernilai nol jika kedua titik tersebut sama. Dalam aktivitas ini, kita menentukan apakah memiliki sifat-sifat tersebut. Misalkan dan berada di dalam .    Buktikan bahwa .    Buktikan bahwa .    Buktikan bahwa jika dan hanya jika .    Misalkan berada di dalam . Pelajari bukti , kemudian gunakan untuk menunjukkan bahwa .  (Apakah Anda memiliki pertanyaan tentang bukti lemma ini?)    Ilustrasi jarak taksi antara titik dan diperlihatkan dalam . Gambarlah lingkaran satuan (himpunan titik yang berjarak 1 dari titik asal) menurut metrik taksi. Jelaskan alasan Anda.   Jarak taksi antara dan pada .  Bidang koordinat memperlihatkan dua titik berlabel di kiri bawah dan di kanan atas. Keduanya dihubungkan oleh lintasan berbentuk siku-siku: satu ruas horizontal sepanjang diikuti satu ruas vertikal sepanjang .     Metrik taksi dapat diperluas ke untuk setiap sebagai berikut. Jika dan berada di dalam , maka jarak taksi dari ke didefinisikan sebagai .  "
},
{
  "id": "F_Euclidean_metric",
  "level": "2",
  "url": "sec_metric_space_intro.html#F_Euclidean_metric",
  "type": "Gambar",
  "number": "3.1",
  "title": "",
  "body": " Jarak Euklides antara dan , serta lingkaran satuan Euklides pada .  Gambar dua panel. Panel kiri memperlihatkan ruas garis horizontal yang menghubungkan titik berlabel dan . Panel kanan memperlihatkan sumbu koordinat dan sebuah lingkaran yang berpusat di titik asal serta memotong sumbu horizontal pada titik berjarak satu satuan dari pusat.  "
},
{
  "id": "lem_abs_TI",
  "level": "2",
  "url": "sec_metric_space_intro.html#lem_abs_TI",
  "type": "Lema",
  "number": "3.2",
  "title": "",
  "body": "  Misalkan dan bilangan real. Maka .    Misalkan dan bilangan real. Untuk membuktikan lemma ini, kita meninjau beberapa kasus.   Kasus 1: dan  Dalam kasus ini, tak negatif sehingga , , dan . Dengan demikian, .    Kasus 2: dan  Dalam kasus ini, dan , dengan dan tak negatif. Berdasarkan Kasus 1, .    Kasus 3: Salah satu dari atau positif dan yang lainnya negatif  Tanpa mengurangi keumuman, kita andaikan dan . Sekali lagi, kita meninjau beberapa kasus. Perhatikan bahwa mengakibatkan .   Andaikan . Maka , sehingga . Akibatnya, .    Kasus terakhir terjadi ketika . Dalam kasus ini, , sehingga . Maka . Terakhir, mengakibatkan . Jadi, dan .      Ini membuktikan lemma kita untuk setiap pasangan , .   "
},
{
  "id": "exploration-3",
  "level": "2",
  "url": "sec_metric_space_intro.html#exploration-3",
  "type": "Aktivitas Persiapan",
  "number": "3.1",
  "title": "",
  "body": " metrik taksi   Perhatikan fungsi yang memasangkan setiap pasangan titik dalam dengan bilangan real .  Fungsi ini kadang-kadang disebut metrik taksi atau jarak taksi karena jarak antara titik dan dapat dibayangkan sebagai jarak yang ditempuh dengan menyusuri ruas-ruas jalan kota, alih-alih bergerak langsung dari titik ke titik .  Setiap fungsi jarak seharusnya memenuhi sifat-sifat tertentu: jarak antara dua titik tidak boleh negatif; jarak dari titik ke titik harus sama dengan jarak dari titik ke titik ; jarak terpendek antara titik dan tidak boleh melebihi jumlah jarak dari ke suatu titik dan jarak dari ke ; dan jarak antara dua titik hanya boleh bernilai nol jika kedua titik tersebut sama. Dalam aktivitas ini, kita menentukan apakah memiliki sifat-sifat tersebut. Misalkan dan berada di dalam .    Buktikan bahwa .    Buktikan bahwa .    Buktikan bahwa jika dan hanya jika .    Misalkan berada di dalam . Pelajari bukti , kemudian gunakan untuk menunjukkan bahwa .  (Apakah Anda memiliki pertanyaan tentang bukti lemma ini?)    Ilustrasi jarak taksi antara titik dan diperlihatkan dalam . Gambarlah lingkaran satuan (himpunan titik yang berjarak 1 dari titik asal) menurut metrik taksi. Jelaskan alasan Anda.   Jarak taksi antara dan pada .  Bidang koordinat memperlihatkan dua titik berlabel di kiri bawah dan di kanan atas. Keduanya dihubungkan oleh lintasan berbentuk siku-siku: satu ruas horizontal sepanjang diikuti satu ruas vertikal sepanjang .    "
},
{
  "id": "sec_metric_space",
  "level": "1",
  "url": "sec_metric_space.html",
  "type": "Bagian",
  "number": "",
  "title": "Ruang Metrik",
  "body": " Ruang Metrik  Dalam sebagian besar pengalaman kita mempelajari matematika, pembahasan berlangsung di , tempat kita mengukur jarak antara titik dan dengan jarak Euklides standar . Dalam aktivitas pendahuluan, kita melihat bahwa fungsi memenuhi banyak sifat yang sama dengan . Sifat-sifat ini memungkinkan kita menggunakan maupun sebagai fungsi jarak. Setiap fungsi jarak kita sebut metrik , dan setiap ruang tempat suatu metrik didefinisikan disebut ruang metrik .   metrik   Suatu metrik pada ruang adalah fungsi yang memenuhi sifat-sifat berikut:    untuk setiap ,     jika dan hanya jika di dalam ,     untuk setiap , dan     untuk setiap .       Sifat 1 dan 2 suatu metrik menyatakan bahwa metrik tersebut definit positif , sedangkan sifat 3 menyatakan bahwa metrik tersebut simetris . Sifat 4 dalam definisi biasanya merupakan sifat metrik yang paling sulit diverifikasi dan disebut pertidaksamaan segitiga . pertidaksamaan segitiga    ruang metrik   Suatu ruang metrik adalah pasangan , dengan suatu metrik pada ruang .    Apabila metriknya jelas dari konteks, kita cukup menyebut sebagai ruang metrik.    Untuk setiap butir berikut, tentukan apakah merupakan ruang metrik. Jika merupakan ruang metrik, jelaskan alasannya. Jika bukan ruang metrik, tentukan sifat metrik mana yang dipenuhi oleh dan mana yang tidak. Jika merupakan ruang metrik, berikan deskripsi geometris lingkaran satuan (himpunan semua titik di dalam yang berjarak dari unsur nol) di ruang tersebut.     , .     ,      ,      , himpunan semua fungsi kontinu pada interval , .    Perlu diperhatikan bahwa tidak semua ruang metrik bersifat tak berhingga. Pada contoh berikut, kita membahas suatu metrik pada ruang berhingga.    Misalkan dan definisikan dengan nilai-nilai pada Tabel .   Tabel nilai fungsi                             Menurut definisi, kita mempunyai untuk setiap , dengan jika dan hanya jika . Karena tabel tersebut simetris terhadap diagonalnya, kita dapat melihat bahwa untuk setiap . Satu-satunya sifat yang masih perlu diverifikasi adalah pertidaksamaan segitiga. Jika , maka untuk setiap . Jika , maka dan . Jika , maka dan .  Dengan demikian, tersisa tiga kasus yang perlu dipertimbangkan, yaitu ketika , , dan berbeda satu sama lain. Sekarang, .  Jadi, merupakan metrik pada .     menunjukkan bahwa himpunan berhingga pun dapat menjadi ruang metrik. Bahkan, kita dapat membentuk ruang metrik berhingga dengan mengambil sebarang subhimpunan berhingga dari ruang metrik , lalu menggunakan pembatasan pada sebagai metrik. mengilustrasikan hal ini dengan menetapkan , , dan di dalam . Dengan demikian, merupakan pembatasan metrik Euklides pada himpunan . Cara lain untuk membangun ruang metrik berhingga adalah memulai dengan himpunan titik yang berhingga, kemudian membuat graf yang menggunakan titik-titik tersebut sebagai simpul. Buatlah sisi-sisi sedemikian sehingga graf tersebut terhubung (artinya, terdapat lintasan dari setiap simpul ke setiap simpul lainnya), lalu berikan bobot pada sisi-sisinya seperti yang diilustrasikan pada . Selanjutnya, kita mendefinisikan metrik pada dengan menetapkan sebagai panjang lintasan terpendek antara simpul dan di dalam graf. Sebagai contoh, pada graf ini.   Graf untuk mendefinisikan suatu metrik.  Graf berbobot dengan lima simpul a, b, c, d, dan e. Sisi-sisinya berbobot a–b: 3, a–c: 8, a–e: 1, b–d: 7, b–e: 2, c–d: 2, c–e: 7, dan d–e: 5.   Seperti metrik Euklides dan metrik taksi, butir (c) dalam dapat diperluas ke sebagai berikut. Jika dan berada di dalam , maka jarak maksimum dari ke didefinisikan sebagai .   metrik maksimum Metrik disebut metrik maksimum . Pada bagian berikutnya, kita membuktikan bahwa metrik Euklides memang merupakan suatu metrik. Pembuktian bahwa dan merupakan metrik diserahkan kepada dan .  "
},
{
  "id": "p-418",
  "level": "2",
  "url": "sec_metric_space.html#p-418",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "metrik ruang metrik "
},
{
  "id": "definition-9",
  "level": "2",
  "url": "sec_metric_space.html#definition-9",
  "type": "Definisi",
  "number": "3.4",
  "title": "",
  "body": " metrik   Suatu metrik pada ruang adalah fungsi yang memenuhi sifat-sifat berikut:    untuk setiap ,     jika dan hanya jika di dalam ,     untuk setiap , dan     untuk setiap .      "
},
{
  "id": "p-424",
  "level": "2",
  "url": "sec_metric_space.html#p-424",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "definit positif simetris pertidaksamaan segitiga "
},
{
  "id": "definition-10",
  "level": "2",
  "url": "sec_metric_space.html#definition-10",
  "type": "Definisi",
  "number": "3.5",
  "title": "",
  "body": " ruang metrik   Suatu ruang metrik adalah pasangan , dengan suatu metrik pada ruang .   "
},
{
  "id": "act_MS_metrics",
  "level": "2",
  "url": "sec_metric_space.html#act_MS_metrics",
  "type": "Kegiatan",
  "number": "3.2",
  "title": "",
  "body": "  Untuk setiap butir berikut, tentukan apakah merupakan ruang metrik. Jika merupakan ruang metrik, jelaskan alasannya. Jika bukan ruang metrik, tentukan sifat metrik mana yang dipenuhi oleh dan mana yang tidak. Jika merupakan ruang metrik, berikan deskripsi geometris lingkaran satuan (himpunan semua titik di dalam yang berjarak dari unsur nol) di ruang tersebut.     , .     ,      ,      , himpunan semua fungsi kontinu pada interval , .   "
},
{
  "id": "exp_finite_ms",
  "level": "2",
  "url": "sec_metric_space.html#exp_finite_ms",
  "type": "Contoh",
  "number": "3.6",
  "title": "",
  "body": "  Misalkan dan definisikan dengan nilai-nilai pada Tabel .   Tabel nilai fungsi                             Menurut definisi, kita mempunyai untuk setiap , dengan jika dan hanya jika . Karena tabel tersebut simetris terhadap diagonalnya, kita dapat melihat bahwa untuk setiap . Satu-satunya sifat yang masih perlu diverifikasi adalah pertidaksamaan segitiga. Jika , maka untuk setiap . Jika , maka dan . Jika , maka dan .  Dengan demikian, tersisa tiga kasus yang perlu dipertimbangkan, yaitu ketika , , dan berbeda satu sama lain. Sekarang, .  Jadi, merupakan metrik pada .   "
},
{
  "id": "F_Graph_metric",
  "level": "2",
  "url": "sec_metric_space.html#F_Graph_metric",
  "type": "Gambar",
  "number": "3.8",
  "title": "",
  "body": " Graf untuk mendefinisikan suatu metrik.  Graf berbobot dengan lima simpul a, b, c, d, dan e. Sisi-sisinya berbobot a–b: 3, a–c: 8, a–e: 1, b–d: 7, b–e: 2, c–d: 2, c–e: 7, dan d–e: 5.  "
},
{
  "id": "p-439",
  "level": "2",
  "url": "sec_metric_space.html#p-439",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "maksimum "
},
{
  "id": "sec_euclid_rn",
  "level": "1",
  "url": "sec_euclid_rn.html",
  "type": "Bagian",
  "number": "",
  "title": "Metrik Euklides pada <span class=\"process-math\">\\(\\R^n\\)<\/span>",
  "body": " Metrik Euklides pada  Ruang metrik yang paling kita kenal adalah ruang metrik , dengan    metrik Euklides Metrik disebut metrik standar atau metrik Euklides pada .  Metrik Euklides ini dapat kita perumum dari ke ruang real berdimensi berapa pun. Misalkan bilangan bulat positif dan misalkan serta berada di dalam . Kita definisikan dengan .  Dalam aktivitas berikutnya, kita akan menunjukkan bahwa memenuhi tiga sifat pertama suatu metrik.    Misalkan dan berada di dalam .    Tunjukkan bahwa .    Tunjukkan bahwa .    Tunjukkan bahwa jika , maka .    Tunjukkan bahwa jika , maka .    Membuktikan bahwa pertidaksamaan segitiga terpenuhi sering kali merupakan bagian tersulit dalam membuktikan bahwa suatu fungsi adalah metrik. Kita akan menguraikan pembuktian ini dengan bantuan Pertidaksamaan Cauchy-Schwarz.   Pertidaksamaan Cauchy-Schwarz  Pertidaksamaan Cauchy-Schwarz   Misalkan bilangan bulat positif dan , berada di dalam . Maka .      Sebelum membuktikan Pertidaksamaan Cauchy-Schwarz, mari kita telaah pertidaksamaan tersebut dalam dua keadaan khusus.    Misalkan dan berada di dalam . Verifikasikan Pertidaksamaan Cauchy-Schwarz dalam keadaan ini.    Misalkan dan berada di dalam . Verifikasikan Pertidaksamaan Cauchy-Schwarz dalam keadaan ini.    Sekarang kita buktikan Pertidaksamaan Cauchy-Schwarz.   Misalkan bilangan bulat positif dan , berada di dalam . Untuk memverifikasi , cukup ditunjukkan bahwa .  Hal ini sulit dilakukan secara langsung, tetapi ada siasat yang dapat kita gunakan. Perhatikan bentuk .  (Semua penjumlahan kita dipahami berlangsung dari 1 sampai , sehingga batas penjumlahan tidak akan kita tuliskan lagi sepanjang sisa pembuktian.) Sekarang .  Untuk menafsirkan bentuk terakhir ini dengan lebih jelas, misalkan , , dan . Jika , pertidaksamaan yang hendak dibuktikan langsung berlaku. Jadi, dalam argumen berikutnya kita dapat menganggap , sehingga . Pertidaksamaan yang diberikan oleh kemudian dapat ditulis dalam bentuk .  Jadi, kita memiliki polinom kuadrat yang tidak pernah bernilai negatif. Hal ini menyiratkan bahwa polinom kuadrat memiliki paling banyak satu akar real. Rumus kuadrat memberikan akar-akar sebagai .  Jika , maka memiliki dua akar real. Oleh karena itu, agar memiliki paling banyak satu akar real, harus berlaku atau .  Dengan demikian, Pertidaksamaan Cauchy-Schwarz terbukti.   Salah satu akibat Pertidaksamaan Cauchy-Schwarz yang kita perlukan untuk menunjukkan bahwa adalah metrik ialah hasil berikut.    Misalkan bilangan bulat positif dan , berada di dalam . Maka .      Sebelum membuktikan akibat tersebut, mari kita telaah hasil itu dalam dua keadaan khusus.    Misalkan dan berada di dalam . Verifikasikan dalam keadaan ini.    Misalkan dan berada di dalam . Verifikasikan dalam keadaan ini.    Sekarang kita buktikan .   Misalkan bilangan bulat positif dan , berada di dalam . Sekarang .  Mengambil akar kuadrat kedua ruas menghasilkan pertidaksamaan yang diinginkan.   Sekarang kita dapat menyelesaikan pembuktian bahwa adalah metrik.   Misalkan bilangan bulat positif dan , , serta berada di dalam . Gunakan untuk menunjukkan bahwa .   Dengan demikian, pembuktian bahwa metrik Euklides memang merupakan metrik telah selesai.  Kita telah melihat beberapa metrik dalam bagian ini, dan sebagian di antaranya memiliki nama khusus. Misalkan dan .   Metrik Euklides , dengan .    Metrik taksi , dengan .    Metrik maksimum , dengan .     Kita baru menunjukkan bahwa dan merupakan metrik pada , tetapi argumen serupa berlaku di dalam . Pembuktiannya diserahkan kepada dan . Selain itu, metrik diskret  metrik diskret  menjadikan setiap himpunan sebagai ruang metrik. Pembuktiannya diserahkan kepada .  "
},
{
  "id": "p-441",
  "level": "2",
  "url": "sec_euclid_rn.html#p-441",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "standar Euklides "
},
{
  "id": "activity-15",
  "level": "2",
  "url": "sec_euclid_rn.html#activity-15",
  "type": "Kegiatan",
  "number": "3.3",
  "title": "",
  "body": "  Misalkan dan berada di dalam .    Tunjukkan bahwa .    Tunjukkan bahwa .    Tunjukkan bahwa jika , maka .    Tunjukkan bahwa jika , maka .   "
},
{
  "id": "lem_CS_Euclidean",
  "level": "2",
  "url": "sec_euclid_rn.html#lem_CS_Euclidean",
  "type": "Lema",
  "number": "3.9",
  "title": "Pertidaksamaan Cauchy-Schwarz.",
  "body": " Pertidaksamaan Cauchy-Schwarz  Pertidaksamaan Cauchy-Schwarz   Misalkan bilangan bulat positif dan , berada di dalam . Maka .   "
},
{
  "id": "activity-16",
  "level": "2",
  "url": "sec_euclid_rn.html#activity-16",
  "type": "Kegiatan",
  "number": "3.4",
  "title": "",
  "body": "  Sebelum membuktikan Pertidaksamaan Cauchy-Schwarz, mari kita telaah pertidaksamaan tersebut dalam dua keadaan khusus.    Misalkan dan berada di dalam . Verifikasikan Pertidaksamaan Cauchy-Schwarz dalam keadaan ini.    Misalkan dan berada di dalam . Verifikasikan Pertidaksamaan Cauchy-Schwarz dalam keadaan ini.   "
},
{
  "id": "proof-3",
  "level": "2",
  "url": "sec_euclid_rn.html#proof-3",
  "type": "Bukti",
  "number": "1",
  "title": "",
  "body": " Misalkan bilangan bulat positif dan , berada di dalam . Untuk memverifikasi , cukup ditunjukkan bahwa .  Hal ini sulit dilakukan secara langsung, tetapi ada siasat yang dapat kita gunakan. Perhatikan bentuk .  (Semua penjumlahan kita dipahami berlangsung dari 1 sampai , sehingga batas penjumlahan tidak akan kita tuliskan lagi sepanjang sisa pembuktian.) Sekarang .  Untuk menafsirkan bentuk terakhir ini dengan lebih jelas, misalkan , , dan . Jika , pertidaksamaan yang hendak dibuktikan langsung berlaku. Jadi, dalam argumen berikutnya kita dapat menganggap , sehingga . Pertidaksamaan yang diberikan oleh kemudian dapat ditulis dalam bentuk .  Jadi, kita memiliki polinom kuadrat yang tidak pernah bernilai negatif. Hal ini menyiratkan bahwa polinom kuadrat memiliki paling banyak satu akar real. Rumus kuadrat memberikan akar-akar sebagai .  Jika , maka memiliki dua akar real. Oleh karena itu, agar memiliki paling banyak satu akar real, harus berlaku atau .  Dengan demikian, Pertidaksamaan Cauchy-Schwarz terbukti.  "
},
{
  "id": "cor_SL",
  "level": "2",
  "url": "sec_euclid_rn.html#cor_SL",
  "type": "Corollary",
  "number": "3.10",
  "title": "",
  "body": "  Misalkan bilangan bulat positif dan , berada di dalam . Maka .   "
},
{
  "id": "activity-17",
  "level": "2",
  "url": "sec_euclid_rn.html#activity-17",
  "type": "Kegiatan",
  "number": "3.5",
  "title": "",
  "body": "  Sebelum membuktikan akibat tersebut, mari kita telaah hasil itu dalam dua keadaan khusus.    Misalkan dan berada di dalam . Verifikasikan dalam keadaan ini.    Misalkan dan berada di dalam . Verifikasikan dalam keadaan ini.   "
},
{
  "id": "proof-4",
  "level": "2",
  "url": "sec_euclid_rn.html#proof-4",
  "type": "Bukti",
  "number": "2",
  "title": "",
  "body": " Misalkan bilangan bulat positif dan , berada di dalam . Sekarang .  Mengambil akar kuadrat kedua ruas menghasilkan pertidaksamaan yang diinginkan.  "
},
{
  "id": "activity-18",
  "level": "2",
  "url": "sec_euclid_rn.html#activity-18",
  "type": "Kegiatan",
  "number": "3.6",
  "title": "",
  "body": " Misalkan bilangan bulat positif dan , , serta berada di dalam . Gunakan untuk menunjukkan bahwa .  "
},
{
  "id": "p-477",
  "level": "2",
  "url": "sec_euclid_rn.html#p-477",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "metrik diskret "
},
{
  "id": "sec_metric_space_summ",
  "level": "1",
  "url": "sec_metric_space_summ.html",
  "type": "Bagian",
  "number": "",
  "title": "Ringkasan",
  "body": " Ringkasan  Gagasan penting yang telah kita bahas dalam bab ini antara lain sebagai berikut.   Metrik pada suatu ruang adalah fungsi yang mengukur jarak antara unsur-unsur ruang tersebut. Secara lebih formal, metrik pada ruang adalah fungsi sedemikian sehingga    untuk setiap ,     jika dan hanya jika di dalam ,     untuk setiap , dan     untuk setiap .   Ruang metrik adalah suatu ruang beserta metrik yang didefinisikan pada ruang tersebut.    Metrik Euklides, metrik taksi, dan metrik maksimum semuanya merupakan metrik pada , sehingga ketiganya memberikan cara untuk mengukur jarak antara titik-titik di . Ketiga metrik ini berbeda dalam cara mendefinisikan jarak.   Metrik Euklides adalah metrik standar yang telah kita gunakan sepanjang pengalaman kita mempelajari matematika. Untuk unsur dan di , metrik Euklides didefinisikan oleh . Dengan metrik ini, lingkaran satuan di (himpunan titik yang berjarak dari titik asal) adalah lingkaran satuan standar yang kita kenal dari geometri Euklides.    Metrik taksi didefinisikan oleh . Lingkaran satuan di dengan metrik taksi, apabila dilihat dalam geometri Euklides, adalah persegi dengan titik sudut , , , dan .    Metrik maksimum didefinisikan oleh . Dengan metrik maksimum, lingkaran satuan di , apabila dilihat dalam geometri Euklides, adalah persegi dengan titik sudut , , , dan .        "
},
{
  "id": "sec_metric_space_exer",
  "level": "1",
  "url": "sec_metric_space_exer.html",
  "type": "Latihan",
  "number": "",
  "title": "Latihan",
  "body": "   bola terbuka dalam ruang metrik   Misalkan suatu ruang metrik. Untuk setiap bilangan real positif , bola terbuka yang berpusat di dan berjari-jari  dalam adalah himpunan .      Misalkan suatu himpunan. Tunjukkan bahwa fungsi (metrik diskret) yang didefinisikan oleh merupakan metrik.    Misalkan dan definisikan dengan . Artinya, adalah sisa pembagian oleh .   Untuk setiap nilai , tentukan apakah mendefinisikan suatu metrik pada . Buktikan jawaban Anda.    Sebagai motivasi untuk definisi berikut, pada yang dilengkapi suatu metrik (tidak harus fungsi di atas), lingkaran satuan adalah himpunan semua titik di yang berjarak dari titik asal. Jika jaraknya kita syaratkan kurang dari , kita memperoleh apa yang disebut bola terbuka. Definisi tersebut berlaku dalam setiap ruang metrik. Jika merupakan ruang metrik untuk nilai yang diberikan, tentukan semua bola terbuka dalam yang berpusat di . Jika bukan ruang metrik, jelaskan alasannya.               Misalkan himpunan semua bilangan rasional dalam bentuk paling sederhana. Bilangan rasional berada dalam bentuk paling sederhana jika serta dan tidak mempunyai faktor persekutuan yang lebih besar dari . Definisikan dengan .   Buktikan bahwa merupakan metrik.   Suatu metrik memungkinkan kita menentukan unsur-unsur mana dalam ruang metrik yang “berdekatan”. Deskripsikan himpunan unsur di yang berjarak kurang dari terhadap dengan menggunakan metrik ini. Dengan kata lain, deskripsikan bola terbuka berpusat di dengan jari-jari (lihat ).   Jika , , dan merupakan unsur suatu ruang metrik , kita mengatakan bahwa berada di antara dan jika . Dengan metrik Euklides pada , terdapat tak berhingga banyak bilangan rasional yang berbeda di antara dan (yaitu bilangan rasional di antara dan yang terletak pada garis Euklides melalui dan ). Deskripsikan semua titik dalam yang berada di antara dan .    Misalkan ruang metrik dari . Jika , , dan merupakan unsur suatu ruang metrik , kita mengatakan bahwa berada di antara  dan jika . Dengan metrik Euklides pada , terdapat tak berhingga banyak bilangan rasional yang berbeda di antara dan (yaitu bilangan rasional di antara dan yang terletak pada garis Euklides melalui dan ). Dalam latihan ini kita menyelidiki bilangan-bilangan yang berada di antara bilangan lain dalam ruang .   Temukan semua unsur dalam yang berada di antara dan .   Manakah yang lebih dekat ke dalam : atau ?   Sekarang temukan semua unsur dalam yang berada di antara dan .    Buktikan bahwa metrik taksi merupakan metrik pada .    Misalkan dan subhimpunan berhingga tak kosong dari , dan misalkan .   Buktikan bahwa .   Buktikan bahwa metrik maksimum merupakan metrik pada .    Jika , kita tuliskan . Untuk dan , definisikan dengan    Tunjukkan bahwa merupakan metrik (disebut metrik hub ).   Misalkan . Deskripsikan secara eksplisit titik-titik yang termasuk dalam himpunan di . (Lihat untuk definisi bola terbuka.)   Misalkan . Deskripsikan secara eksplisit titik-titik yang termasuk dalam himpunan di .   Sekarang deskripsikan secara eksplisit semua bola terbuka dalam .    Misalkan himpunan bilangan bulat dan suatu bilangan prima. Untuk setiap pasangan bilangan bulat berbeda dan , terdapat bilangan bulat sedemikian sehingga , dengan tidak membagi . Sebagai contoh, jika , , dan , maka . Jadi . Namun, jika dan , maka . Jadi . Definisikan dengan    Tentukan nilai dengan dan dengan .   Buktikan bahwa jika , , dan berada di , maka .   Buktikan bahwa merupakan ruang metrik.   Misalkan . Deskripsikan himpunan semua unsur dalam yang memenuhi .   Tetap gunakan . Deskripsikan himpunan semua unsur dalam yang memenuhi .    Misalkan dan ruang-ruang metrik. Kita dapat menjadikan hasil kali Kartesius suatu ruang metrik dengan mendefinisikan metrik pada sebagai berikut. Jika dan berada di , maka . Anda boleh menganggap tanpa bukti bahwa merupakan metrik pada .   Misalkan dan . Misalkan dan . Berapakah Ingat bahwa dan .   Misalkan dan , dengan metrik diskret. Misalkan di . Misalkan di . Deskripsikan secara geometris bentuk bola terbuka dalam ruang hasil kali . Gambarlah bola terbuka ini.    Misalkan , himpunan bilangan real positif, dan definisikan dengan . Apakah merupakan metrik pada ? Buktikan jawaban Anda.    Misalkan didefinisikan oleh . Tunjukkan bahwa merupakan metrik pada . (Petunjuk: Untuk pertidaksamaan segitiga, perhatikan bahwa , dengan , dan merupakan fungsi naik.)    Misalkan suatu ruang metrik dan suatu konstanta. Definisikan dengan . Dengan syarat apa, jika ada, merupakan metrik pada ? Jelaskan alasan Anda.    Fungsi bernilai real pada suatu interval disebut cekung jika untuk setiap dan setiap serta dalam interval tersebut. Perhatikan bahwa ekspresi linear terhadap , bernilai ketika , dan bernilai ketika . Jadi merupakan parameterisasi ruas garis yang menghubungkan dengan . Seperti diperlihatkan , persamaan menyatakan bahwa grafik fungsi cekung pada setiap interval terletak di atas garis sekan yang menghubungkan titik dan .   Suatu fungsi cekung.  Grafik sebuah fungsi cekung melengkung di atas garis sekan yang menghubungkan dua titik pada grafik.    Misalkan memetakan ke dengan metrik Euklides standar. Tunjukkan bahwa cekung pada interval .   Mulailah dari fakta bahwa .   Tunjukkan bahwa jika merupakan fungsi cekung pada dan . Jika dan berada dalam interval tersebut, maka .   Tinjau dengan . Lalu gunakan fakta bahwa berada di .   Misalkan suatu ruang metrik dan suatu fungsi naik dan cekung sedemikian sehingga jika dan hanya jika . Buktikan bahwa merupakan metrik pada .    Untuk setiap pernyataan berikut, jawablah benar jika pernyataan itu selalu benar. Jika pernyataan itu hanya kadang-kadang benar atau tidak pernah benar, jawablah salah dan berikan contoh konkret yang menunjukkan bahwa pernyataan tersebut salah. Jika suatu pernyataan benar, jelaskan alasannya.   Fungsi yang didefinisikan oleh merupakan metrik pada .   Setiap himpunan tak kosong dapat dijadikan ruang metrik.   Pada setiap himpunan yang memuat sekurang-kurangnya dua unsur, dapat didefinisikan tak berhingga banyak metrik.   Misalkan dan ruang-ruang metrik dengan . Maka fungsi yang didefinisikan oleh merupakan metrik pada .   Misalkan suatu ruang metrik. Jika tak berhingga, maka daerah hasil juga merupakan himpunan tak berhingga.   "
},
{
  "id": "def_ms_open_ball",
  "level": "2",
  "url": "sec_metric_space_exer.html#def_ms_open_ball",
  "type": "Definisi",
  "number": "3.11",
  "title": "",
  "body": " bola terbuka dalam ruang metrik   Misalkan suatu ruang metrik. Untuk setiap bilangan real positif , bola terbuka yang berpusat di dan berjari-jari  dalam adalah himpunan .   "
},
{
  "id": "ex_MS_discrete",
  "level": "2",
  "url": "sec_metric_space_exer.html#ex_MS_discrete",
  "type": "Latihan",
  "number": "1",
  "title": "",
  "body": " Misalkan suatu himpunan. Tunjukkan bahwa fungsi (metrik diskret) yang didefinisikan oleh merupakan metrik.  "
},
{
  "id": "ex_MS_mod_metric",
  "level": "2",
  "url": "sec_metric_space_exer.html#ex_MS_mod_metric",
  "type": "Latihan",
  "number": "2",
  "title": "",
  "body": " Misalkan dan definisikan dengan . Artinya, adalah sisa pembagian oleh .   Untuk setiap nilai , tentukan apakah mendefinisikan suatu metrik pada . Buktikan jawaban Anda.    Sebagai motivasi untuk definisi berikut, pada yang dilengkapi suatu metrik (tidak harus fungsi di atas), lingkaran satuan adalah himpunan semua titik di yang berjarak dari titik asal. Jika jaraknya kita syaratkan kurang dari , kita memperoleh apa yang disebut bola terbuka. Definisi tersebut berlaku dalam setiap ruang metrik. Jika merupakan ruang metrik untuk nilai yang diberikan, tentukan semua bola terbuka dalam yang berpusat di . Jika bukan ruang metrik, jelaskan alasannya.             "
},
{
  "id": "ex_MS_Q_metric",
  "level": "2",
  "url": "sec_metric_space_exer.html#ex_MS_Q_metric",
  "type": "Latihan",
  "number": "3",
  "title": "",
  "body": " Misalkan himpunan semua bilangan rasional dalam bentuk paling sederhana. Bilangan rasional berada dalam bentuk paling sederhana jika serta dan tidak mempunyai faktor persekutuan yang lebih besar dari . Definisikan dengan .   Buktikan bahwa merupakan metrik.   Suatu metrik memungkinkan kita menentukan unsur-unsur mana dalam ruang metrik yang “berdekatan”. Deskripsikan himpunan unsur di yang berjarak kurang dari terhadap dengan menggunakan metrik ini. Dengan kata lain, deskripsikan bola terbuka berpusat di dengan jari-jari (lihat ).   Jika , , dan merupakan unsur suatu ruang metrik , kita mengatakan bahwa berada di antara dan jika . Dengan metrik Euklides pada , terdapat tak berhingga banyak bilangan rasional yang berbeda di antara dan (yaitu bilangan rasional di antara dan yang terletak pada garis Euklides melalui dan ). Deskripsikan semua titik dalam yang berada di antara dan .  "
},
{
  "id": "exercise-31",
  "level": "2",
  "url": "sec_metric_space_exer.html#exercise-31",
  "type": "Latihan",
  "number": "4",
  "title": "",
  "body": " Misalkan ruang metrik dari . Jika , , dan merupakan unsur suatu ruang metrik , kita mengatakan bahwa berada di antara  dan jika . Dengan metrik Euklides pada , terdapat tak berhingga banyak bilangan rasional yang berbeda di antara dan (yaitu bilangan rasional di antara dan yang terletak pada garis Euklides melalui dan ). Dalam latihan ini kita menyelidiki bilangan-bilangan yang berada di antara bilangan lain dalam ruang .   Temukan semua unsur dalam yang berada di antara dan .   Manakah yang lebih dekat ke dalam : atau ?   Sekarang temukan semua unsur dalam yang berada di antara dan .  "
},
{
  "id": "ex_Taxicab",
  "level": "2",
  "url": "sec_metric_space_exer.html#ex_Taxicab",
  "type": "Latihan",
  "number": "5",
  "title": "",
  "body": " Buktikan bahwa metrik taksi merupakan metrik pada .  "
},
{
  "id": "ex_Max",
  "level": "2",
  "url": "sec_metric_space_exer.html#ex_Max",
  "type": "Latihan",
  "number": "6",
  "title": "",
  "body": " Misalkan dan subhimpunan berhingga tak kosong dari , dan misalkan .   Buktikan bahwa .   Buktikan bahwa metrik maksimum merupakan metrik pada .  "
},
{
  "id": "ex_MS_hub",
  "level": "2",
  "url": "sec_metric_space_exer.html#ex_MS_hub",
  "type": "Latihan",
  "number": "7",
  "title": "",
  "body": " Jika , kita tuliskan . Untuk dan , definisikan dengan    Tunjukkan bahwa merupakan metrik (disebut metrik hub ).   Misalkan . Deskripsikan secara eksplisit titik-titik yang termasuk dalam himpunan di . (Lihat untuk definisi bola terbuka.)   Misalkan . Deskripsikan secara eksplisit titik-titik yang termasuk dalam himpunan di .   Sekarang deskripsikan secara eksplisit semua bola terbuka dalam .  "
},
{
  "id": "exercise-35",
  "level": "2",
  "url": "sec_metric_space_exer.html#exercise-35",
  "type": "Latihan",
  "number": "8",
  "title": "",
  "body": " Misalkan himpunan bilangan bulat dan suatu bilangan prima. Untuk setiap pasangan bilangan bulat berbeda dan , terdapat bilangan bulat sedemikian sehingga , dengan tidak membagi . Sebagai contoh, jika , , dan , maka . Jadi . Namun, jika dan , maka . Jadi . Definisikan dengan    Tentukan nilai dengan dan dengan .   Buktikan bahwa jika , , dan berada di , maka .   Buktikan bahwa merupakan ruang metrik.   Misalkan . Deskripsikan himpunan semua unsur dalam yang memenuhi .   Tetap gunakan . Deskripsikan himpunan semua unsur dalam yang memenuhi .  "
},
{
  "id": "exercise-36",
  "level": "2",
  "url": "sec_metric_space_exer.html#exercise-36",
  "type": "Latihan",
  "number": "9",
  "title": "",
  "body": " Misalkan dan ruang-ruang metrik. Kita dapat menjadikan hasil kali Kartesius suatu ruang metrik dengan mendefinisikan metrik pada sebagai berikut. Jika dan berada di , maka . Anda boleh menganggap tanpa bukti bahwa merupakan metrik pada .   Misalkan dan . Misalkan dan . Berapakah Ingat bahwa dan .   Misalkan dan , dengan metrik diskret. Misalkan di . Misalkan di . Deskripsikan secara geometris bentuk bola terbuka dalam ruang hasil kali . Gambarlah bola terbuka ini.  "
},
{
  "id": "exercise-37",
  "level": "2",
  "url": "sec_metric_space_exer.html#exercise-37",
  "type": "Latihan",
  "number": "10",
  "title": "",
  "body": " Misalkan , himpunan bilangan real positif, dan definisikan dengan . Apakah merupakan metrik pada ? Buktikan jawaban Anda.  "
},
{
  "id": "ex_1_over_1_plus_t_metric",
  "level": "2",
  "url": "sec_metric_space_exer.html#ex_1_over_1_plus_t_metric",
  "type": "Latihan",
  "number": "11",
  "title": "",
  "body": " Misalkan didefinisikan oleh . Tunjukkan bahwa merupakan metrik pada . (Petunjuk: Untuk pertidaksamaan segitiga, perhatikan bahwa , dengan , dan merupakan fungsi naik.)  "
},
{
  "id": "exercise-39",
  "level": "2",
  "url": "sec_metric_space_exer.html#exercise-39",
  "type": "Latihan",
  "number": "12",
  "title": "",
  "body": " Misalkan suatu ruang metrik dan suatu konstanta. Definisikan dengan . Dengan syarat apa, jika ada, merupakan metrik pada ? Jelaskan alasan Anda.  "
},
{
  "id": "exercise-40",
  "level": "2",
  "url": "sec_metric_space_exer.html#exercise-40",
  "type": "Latihan",
  "number": "13",
  "title": "",
  "body": " Fungsi bernilai real pada suatu interval disebut cekung jika untuk setiap dan setiap serta dalam interval tersebut. Perhatikan bahwa ekspresi linear terhadap , bernilai ketika , dan bernilai ketika . Jadi merupakan parameterisasi ruas garis yang menghubungkan dengan . Seperti diperlihatkan , persamaan menyatakan bahwa grafik fungsi cekung pada setiap interval terletak di atas garis sekan yang menghubungkan titik dan .   Suatu fungsi cekung.  Grafik sebuah fungsi cekung melengkung di atas garis sekan yang menghubungkan dua titik pada grafik.    Misalkan memetakan ke dengan metrik Euklides standar. Tunjukkan bahwa cekung pada interval .   Mulailah dari fakta bahwa .   Tunjukkan bahwa jika merupakan fungsi cekung pada dan . Jika dan berada dalam interval tersebut, maka .   Tinjau dengan . Lalu gunakan fakta bahwa berada di .   Misalkan suatu ruang metrik dan suatu fungsi naik dan cekung sedemikian sehingga jika dan hanya jika . Buktikan bahwa merupakan metrik pada .  "
},
{
  "id": "exercise-41",
  "level": "2",
  "url": "sec_metric_space_exer.html#exercise-41",
  "type": "Latihan",
  "number": "14",
  "title": "",
  "body": " Untuk setiap pernyataan berikut, jawablah benar jika pernyataan itu selalu benar. Jika pernyataan itu hanya kadang-kadang benar atau tidak pernah benar, jawablah salah dan berikan contoh konkret yang menunjukkan bahwa pernyataan tersebut salah. Jika suatu pernyataan benar, jelaskan alasannya.   Fungsi yang didefinisikan oleh merupakan metrik pada .   Setiap himpunan tak kosong dapat dijadikan ruang metrik.   Pada setiap himpunan yang memuat sekurang-kurangnya dua unsur, dapat didefinisikan tak berhingga banyak metrik.   Misalkan dan ruang-ruang metrik dengan . Maka fungsi yang didefinisikan oleh merupakan metrik pada .   Misalkan suatu ruang metrik. Jika tak berhingga, maka daerah hasil juga merupakan himpunan tak berhingga.  "
},
{
  "id": "sec_met_space_app",
  "level": "1",
  "url": "sec_met_space_app.html",
  "type": "Bagian",
  "number": "",
  "title": "Pendahuluan",
  "body": " Pendahuluan  Pada bagian ini, kita menelaah dua penerapan ruang metrik.  "
},
{
  "id": "sec_hamming",
  "level": "1",
  "url": "sec_hamming.html",
  "type": "Bagian",
  "number": "",
  "title": "Metrik Hamming",
  "body": " Metrik Hamming  Dalam masyarakat kita, banyak sekali informasi dikomunikasikan secara elektronik. Transaksi bank, program televisi, komunikasi militer, panggilan telepon seluler, citra digital, dan hampir setiap pertukaran yang dapat dibayangkan dapat didigitalkan dan dikirimkan secara elektronik, atau memang sudah dilakukan dengan cara tersebut. Dalam banyak situasi, kita perlu membandingkan satu kumpulan data dengan kumpulan lainnya (misalnya, pencarian untai teks atau pencocokan citra di Internet, serta untaian DNA), dan metrik sering digunakan untuk tujuan ini. Komputer bekerja dengan sistem biner, artinya komputer hanya mengenali nol dan satu. Karena itu, pesan teks digital merupakan suatu untai nol dan satu. Dengan kata lain, pesan digital merupakan kumpulan unsur dalam ruang untuk suatu bilangan bulat positif , dengan . Setiap unsur dalam disebut kata —yakni, kata adalah unsur dalam yang dinyatakan dalam bentuk . Seperti halnya dalam bahasa Inggris, yang tidak setiap kombinasi hurufnya membentuk kata yang bermakna, tidak setiap kata dapat dikenali sebagai bagian dari pesan yang dapat dipahami. Sebagai contoh, kita dapat mengodekan huruf-huruf dalam alfabet dengan menetapkan bilangan 1 sampai 26 pada huruf-huruf tersebut, kemudian menjadikannya unsur dalam dengan mengonversinya ke bentuk biner. Himpunan semua kata yang dapat dipahami disebut kode . Jadi, kode hanyalah suatu subhimpunan yang unsur-unsurnya disepakati oleh semua pihak sebagai kata-kata yang bermakna. Kata-kata dalam suatu kode disebut kata kode . Untuk menangani masalah yang terjadi dalam pengiriman pesan digital, seperti mengacak pesan ( pengodean ), memulihkan pesan dari bentuk teracak ( pendekodean ), serta mendeteksi dan memperbaiki galat dalam pesan, kita perlu memiliki cara untuk mengukur jarak antarkata. Salah satu caranya adalah menggunakan metrik Hamming.   metrik Hamming   Misalkan dan merupakan kata-kata dalam . Jarak Hamming  antara dan adalah .    Ingatlah bahwa untuk setiap , baik maupun bernilai 0 atau 1. Oleh karena itu,   Dengan kata lain, menghitung banyaknya komponen tempat dan berbeda.    Jelaskan mengapa merupakan suatu metrik.    Misalkan kita membuat kode dalam , dengan Artinya, kata-kata , , , , , , , dan merupakan satu-satunya kata yang dapat menyusun suatu pesan. Hitung .    Misalkan kita menerima pesan .   Bagaimana kita mengetahui bahwa telah terjadi galat dalam transmisi pesan yang kita terima?   Untuk memperbaiki galat dalam pesan yang diterima ini, kita mengganti kata-kata yang salah dengan kata kode dalam yang paling dekat dengan masing-masing kata tersebut. Perbaikilah pesan ini. (Perhatikan bahwa mungkin terdapat lebih dari satu kemungkinan penggantian. Temukan semua kemungkinannya.)    "
},
{
  "id": "p-537",
  "level": "2",
  "url": "sec_hamming.html#p-537",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "kata kode kata kode pengodean pendekodean "
},
{
  "id": "definition-12",
  "level": "2",
  "url": "sec_hamming.html#definition-12",
  "type": "Definisi",
  "number": "4.1",
  "title": "",
  "body": " metrik Hamming   Misalkan dan merupakan kata-kata dalam . Jarak Hamming  antara dan adalah .   "
},
{
  "id": "activity-19",
  "level": "2",
  "url": "sec_hamming.html#activity-19",
  "type": "Kegiatan",
  "number": "4.1",
  "title": "",
  "body": "  Jelaskan mengapa merupakan suatu metrik.    Misalkan kita membuat kode dalam , dengan Artinya, kata-kata , , , , , , , dan merupakan satu-satunya kata yang dapat menyusun suatu pesan. Hitung .    Misalkan kita menerima pesan .   Bagaimana kita mengetahui bahwa telah terjadi galat dalam transmisi pesan yang kita terima?   Untuk memperbaiki galat dalam pesan yang diterima ini, kita mengganti kata-kata yang salah dengan kata kode dalam yang paling dekat dengan masing-masing kata tersebut. Perbaikilah pesan ini. (Perhatikan bahwa mungkin terdapat lebih dari satu kemungkinan penggantian. Temukan semua kemungkinannya.)   "
},
{
  "id": "sec_levenshtein",
  "level": "1",
  "url": "sec_levenshtein.html",
  "type": "Bagian",
  "number": "",
  "title": "Metrik Levenshtein",
  "body": " Metrik Levenshtein  Metrik Levenshtein merupakan salah satu ukuran jarak yang digunakan para peneliti untuk memahami DNA. DNA tersusun atas dua rantai nukleotida, yang saling berpilin membentuk heliks ganda. Nukleotida terdiri atas empat jenis: adenin (A), sitosin (C), guanin (G), dan timin (T). Nukleotida pada kedua rantai dalam suatu untai DNA saling berpasangan (A dengan T dan C dengan G), sehingga nukleotida pada satu rantai menentukan nukleotida pada rantai lainnya. Karena itu, kita dapat merepresentasikan suatu untai DNA dengan untai huruf dari alfabet . Salah satu persoalan yang dihadapi peneliti DNA adalah cara membandingkan dua untai DNA, dan metrik Levenshtein merupakan salah satu cara untuk mengukur jarak di antara keduanya. Metrik lain dapat digunakan, tetapi metrik Levenshtein sesuai untuk tugas ini karena beberapa alasan. Selama evolusi, perubahan pada urutan DNA terjadi karena substitusi nukleotida, atau karena penyisipan maupun penghapusan nukleotida. Perubahan evolusioner ini dapat dimodelkan lebih baik oleh operasi-operasi yang menentukan jarak Levenshtein daripada oleh metrik lain. Selain itu, metrik Levenshtein dapat digunakan untuk menghitung jarak antara untai-untai yang panjangnya berbeda. Metrik Levenshtein juga diterapkan dalam pemeriksa ejaan, pengenalan wicara, dan deteksi plagiarisme otomatis. Untuk memahami cara menghitung metrik Levenshtein, perhatikan pertanyaan tentang seberapa jauh jarak antara kata green dan grease .  Untuk membandingkan kedua kata ini, kita harus dapat mengubah, menambahkan, atau menghapus huruf. Jika merupakan suatu untai huruf, kita memperbolehkan operasi-operasi berikut:   penghapusan:  ganti dengan untuk suatu ,    penyisipan:  ganti dengan , dengan merupakan huruf yang diperbolehkan dan ,    substitusi:  ganti dengan , dengan merupakan huruf yang diperbolehkan dan .       Dengan menggunakan operasi-operasi yang diperbolehkan, ubahlah kata green menjadi kata grease . Sebutkan secara spesifik setiap operasi yang Anda gunakan. (Catatan: untai-untai huruf antara tidak harus membentuk kata yang dapat dikenali.) Berapa banyak operasi yang Anda gunakan?    Jika diperlukan tiga operasi untuk mengubah green menjadi grease , kita dapat mengatakan bahwa jarak antara green dan grease paling besar 3. Akan tetapi, mungkin saja green dapat diubah menjadi grease dengan kurang dari 3 operasi, sehingga penilaian kita tentang jarak antara kedua kata tersebut dapat berubah. Secara umum, untuk mendefinisikan jarak Levenshtein antara untai dan untai di atas suatu alfabet tetap , misalkan menyatakan banyaknya penghapusan, menyatakan banyaknya penyisipan, dan menyatakan banyaknya substitusi yang digunakan untuk mengubah menjadi . Mungkin terdapat banyak kombinasi berbeda dari , , dan yang mengubah menjadi , sehingga kita menginginkan jumlah terkecil.   metrik Levenshtein    Jarak Levenshtein  antara untai dan adalah .      Buktikan bahwa fungsi jarak Levenshtein benar-benar merupakan metrik pada himpunan semua untai berhingga di atas alfabet tetap (baik yang membentuk kata bermakna maupun tidak).    Sebuah pemeriksa ejaan memperbaiki kata yang salah eja tupotagry . Dengan menggunakan metrik Levenshtein, kata manakah yang akan dipilih pemeriksa ejaan sebagai kata yang paling dekat dengan tupotagry ? Mengapa?     "
},
{
  "id": "activity-20",
  "level": "2",
  "url": "sec_levenshtein.html#activity-20",
  "type": "Kegiatan",
  "number": "4.2",
  "title": "",
  "body": "  Dengan menggunakan operasi-operasi yang diperbolehkan, ubahlah kata green menjadi kata grease . Sebutkan secara spesifik setiap operasi yang Anda gunakan. (Catatan: untai-untai huruf antara tidak harus membentuk kata yang dapat dikenali.) Berapa banyak operasi yang Anda gunakan?   "
},
{
  "id": "definition-13",
  "level": "2",
  "url": "sec_levenshtein.html#definition-13",
  "type": "Definisi",
  "number": "4.2",
  "title": "",
  "body": " metrik Levenshtein    Jarak Levenshtein  antara untai dan adalah .   "
},
{
  "id": "activity-21",
  "level": "2",
  "url": "sec_levenshtein.html#activity-21",
  "type": "Kegiatan",
  "number": "4.3",
  "title": "",
  "body": "  Buktikan bahwa fungsi jarak Levenshtein benar-benar merupakan metrik pada himpunan semua untai berhingga di atas alfabet tetap (baik yang membentuk kata bermakna maupun tidak).    Sebuah pemeriksa ejaan memperbaiki kata yang salah eja tupotagry . Dengan menggunakan metrik Levenshtein, kata manakah yang akan dipilih pemeriksa ejaan sebagai kata yang paling dekat dengan tupotagry ? Mengapa?    "
},
{
  "id": "sec_glb_intro",
  "level": "1",
  "url": "sec_glb_intro.html",
  "type": "Bagian",
  "number": "",
  "title": "Pendahuluan",
  "body": " Pendahuluan  Bilangan real memiliki suatu sifat khusus yang, antara lain, memungkinkan kita mendefinisikan jarak antara suatu titik dan suatu himpunan di ruang metrik. Sifat tersebut juga memungkinkan kita mendefinisikan jarak antarsubhimpunan pada jenis ruang metrik tertentu, sehingga terbentuk suatu ruang metrik yang sama sekali baru, yang unsur-unsurnya adalah subhimpunan dari ruang metrik semula. Dalam aktivitas ini, kita akan menelaah sifat bilangan real tersebut.  Kita mulai dengan meninjau cara mendefinisikan jarak antara suatu bilangan real dan suatu interval di dengan metrik Euklides yang didefinisikan oleh .  Misalkan dan misalkan adalah interval tertutup . Wajar jika kita mengusulkan bahwa jarak antara titik dan himpunan , yang dinotasikan dengan , seharusnya merupakan jarak dari titik ke titik di yang paling dekat dengan . Jadi, dalam kasus ini kita akan mengatakan .  Hal ini mungkin mengarahkan kita untuk mengusulkan bahwa jarak dari suatu titik ke suatu himpunan , yang dinotasikan dengan , adalah jarak minimum dari titik tersebut ke sebarang titik di dalam himpunan itu, yaitu .  Bagaimana jika kita mengubah himpunan menjadi interval terbuka ? Lalu, berapakah seharusnya , atau apakah jarak ini seharusnya ada? Jika kita memandang jarak antara suatu titik dan suatu himpunan sebagai ukuran seberapa jauh kita harus bergerak dari titik tersebut hingga mencapai himpunan itu, maka dalam kasus dan , segera setelah kita menempuh jarak lebih dari 1 dari ke arah , kita mencapai himpunan . Jadi, secara intuitif kita dapat mengatakan bahwa juga. Namun, kita tidak dapat mendefinisikan jarak ini sebagai jarak dari ke suatu titik di karena . Kita memerlukan cara lain untuk merumuskan gagasan jarak dari suatu titik ke suatu himpunan.  Dalam kasus seperti ini, dengan dan , kita dapat menelaah himpunan dan mencermati beberapa fakta tentang himpunan tersebut. Sebagai contoh, himpunan merupakan subhimpunan dari bilangan real tak negatif. Selain itu, dalam contoh ini tidak ada bilangan di yang lebih kecil dari 1. Karena sifat ini, kita akan menyebut bilangan 1 sebagai batas bawah untuk . Secara umum,   batas bawah   Misalkan adalah subhimpunan tak kosong dari . Suatu batas bawah untuk adalah bilangan real sedemikian sehingga untuk setiap .    Jika suatu subhimpunan dari memiliki batas bawah, kita mengatakan bahwa  terbatas di bawah . Jadi, himpunan terbatas di bawah oleh 1. Himpunan juga terbatas di bawah oleh 0.5 dan 0. Bahkan, setiap bilangan yang lebih kecil dari 1 merupakan batas bawah untuk . Namun, gagasan pentingnya adalah bahwa tidak ada bilangan yang lebih besar dari 1 yang merupakan batas bawah untuk . Karena itu, kita menyebut 1 sebagai batas bawah terbesar dari . Secara umum,   batas bawah terbesar   Misalkan adalah subhimpunan tak kosong dari yang terbatas di bawah. Suatu batas bawah terbesar untuk adalah bilangan real sedemikian sehingga memenuhi dua syarat berikut.    merupakan batas bawah untuk ; dan    jika merupakan batas bawah untuk , maka .        infimum Batas bawah terbesar juga disebut infimum . Sekarang kita dapat menggunakan gagasan batas bawah terbesar ini untuk mendefinisikan jarak antara dan sebagai batas bawah terbesar dari himpunan . Namun, ada beberapa pertanyaan yang perlu kita jawab sebelum dapat melakukannya. Salah satunya adalah apakah setiap subhimpunan tak kosong dari yang terbatas di bawah memiliki infimum. Jawaban atas pertanyaan ini adalah ya, dan kita akan menerima hasil ini sebagai suatu aksioma dalam sistem bilangan real (yang sering disebut aksioma kelengkapan ).    Apakah setiap subhimpunan memiliki batas bawah? Jelaskan. (Jika suatu subhimpunan memiliki batas bawah, kita mengatakan bahwa himpunan tersebut terbatas di bawah .)    Manakah dari subhimpunan dari berikut yang terbatas di bawah? Jika himpunannya terbatas di bawah, berapakah infimumnya?                Bagaimana cara mendefinisikan batas atas terkecil dari suatu subhimpunan dari ?    "
},
{
  "id": "p-564",
  "level": "2",
  "url": "sec_glb_intro.html#p-564",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "batas bawah "
},
{
  "id": "definition-14",
  "level": "2",
  "url": "sec_glb_intro.html#definition-14",
  "type": "Definisi",
  "number": "5.1",
  "title": "",
  "body": " batas bawah   Misalkan adalah subhimpunan tak kosong dari . Suatu batas bawah untuk adalah bilangan real sedemikian sehingga untuk setiap .   "
},
{
  "id": "p-566",
  "level": "2",
  "url": "sec_glb_intro.html#p-566",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "terbatas di bawah batas bawah terbesar "
},
{
  "id": "definition-15",
  "level": "2",
  "url": "sec_glb_intro.html#definition-15",
  "type": "Definisi",
  "number": "5.2",
  "title": "",
  "body": " batas bawah terbesar   Misalkan adalah subhimpunan tak kosong dari yang terbatas di bawah. Suatu batas bawah terbesar untuk adalah bilangan real sedemikian sehingga memenuhi dua syarat berikut.    merupakan batas bawah untuk ; dan    jika merupakan batas bawah untuk , maka .      "
},
{
  "id": "p-570",
  "level": "2",
  "url": "sec_glb_intro.html#p-570",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "infimum aksioma kelengkapan "
},
{
  "id": "exploration-4",
  "level": "2",
  "url": "sec_glb_intro.html#exploration-4",
  "type": "Aktivitas Persiapan",
  "number": "5.1",
  "title": "",
  "body": "  Apakah setiap subhimpunan memiliki batas bawah? Jelaskan. (Jika suatu subhimpunan memiliki batas bawah, kita mengatakan bahwa himpunan tersebut terbatas di bawah .)    Manakah dari subhimpunan dari berikut yang terbatas di bawah? Jika himpunannya terbatas di bawah, berapakah infimumnya?                Bagaimana cara mendefinisikan batas atas terkecil dari suatu subhimpunan dari ?   "
},
{
  "id": "sec_dist_point_set",
  "level": "1",
  "url": "sec_dist_point_set.html",
  "type": "Bagian",
  "number": "",
  "title": "Jarak dari Titik ke Himpunan",
  "body": " Jarak dari Titik ke Himpunan  Metrik digunakan untuk menetapkan keterpisahan antarobjek. Ruang topologis dapat dikelompokkan ke dalam berbagai kategori berdasarkan seberapa baik jenis-jenis himpunan tertentu dapat dipisahkan. Kita telah mendefinisikan metrik sebagai fungsi yang mengukur jarak antartitik di suatu ruang metrik, dan dalam aktivitas ini kita memperluas gagasan tersebut untuk mengukur jarak antara sebuah titik dan suatu subhimpunan di ruang metrik. Akan tetapi, sebelum itu kita perlu menjawab dua pertanyaan. Pertanyaan pertama telah kita kemukakan dalam aktivitas pendahuluan. Kita akan mengasumsikan aksioma kelengkapan bagi bilangan real, yakni bahwa setiap subhimpunan tak kosong dari yang terbatas di bawah selalu mempunyai batas bawah terbesar. Pertanyaan kedua adalah apakah batas bawah terbesar itu unik.    Misalkan suatu subhimpunan dari yang terbatas di bawah, dan asumsikan bahwa mempunyai batas bawah terbesar. Dalam aktivitas ini, kita akan menunjukkan bahwa infimum itu unik.    Metode apa yang dapat kita gunakan untuk membuktikan bahwa hanya mempunyai satu batas bawah terbesar?    Misalkan dan keduanya merupakan batas bawah terbesar untuk . Mengapa dan keduanya merupakan batas bawah untuk ?    Dua hal apa yang dinyatakan sifat kedua batas bawah terbesar mengenai hubungan antara dan ?    Mengapa batas bawah terbesar dari harus unik?    Setelah meninjau keberadaan dan keunikan batas bawah terbesar, kini kita dapat mengatakan bahwa setiap subhimpunan tak kosong dari yang terbatas di bawah mempunyai batas bawah terbesar yang unik. Kita menggunakan notasi (atau untuk infimum dari ) bagi batas bawah terbesar dari . Terdapat pula batas atas terkecil  batas atas terkecil ( , atau untuk supremum  supremum ) bagi suatu subhimpunan tak kosong dari yang terbatas di atas.  Sekarang kita dapat mendefinisikan secara formal jarak antara sebuah titik dan suatu subhimpunan di ruang metrik.    Misalkan suatu ruang metrik, misalkan , dan misalkan suatu subhimpunan tak kosong dari . Jarak dari ke adalah .    Kita menotasikan jarak dari ke dengan . Ketika menghitung jarak seperti ini, metrik yang mendasarinya harus dipahami dengan jelas.    Dalam aktivitas ini, kita menelaah beberapa fakta mengenai jarak antara sebuah titik dan suatu himpunan. Misalkan suatu ruang metrik, misalkan , dan misalkan suatu subhimpunan tak kosong dari .    Mengapa pasti ada?    Jika , apakah harus berlaku ?    "
},
{
  "id": "p-577",
  "level": "2",
  "url": "sec_dist_point_set.html#p-577",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "aksioma kelengkapan "
},
{
  "id": "activity-22",
  "level": "2",
  "url": "sec_dist_point_set.html#activity-22",
  "type": "Kegiatan",
  "number": "5.2",
  "title": "",
  "body": "  Misalkan suatu subhimpunan dari yang terbatas di bawah, dan asumsikan bahwa mempunyai batas bawah terbesar. Dalam aktivitas ini, kita akan menunjukkan bahwa infimum itu unik.    Metode apa yang dapat kita gunakan untuk membuktikan bahwa hanya mempunyai satu batas bawah terbesar?    Misalkan dan keduanya merupakan batas bawah terbesar untuk . Mengapa dan keduanya merupakan batas bawah untuk ?    Dua hal apa yang dinyatakan sifat kedua batas bawah terbesar mengenai hubungan antara dan ?    Mengapa batas bawah terbesar dari harus unik?   "
},
{
  "id": "p-583",
  "level": "2",
  "url": "sec_dist_point_set.html#p-583",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "infimum batas atas terkecil supremum "
},
{
  "id": "definition-16",
  "level": "2",
  "url": "sec_dist_point_set.html#definition-16",
  "type": "Definisi",
  "number": "5.3",
  "title": "",
  "body": "  Misalkan suatu ruang metrik, misalkan , dan misalkan suatu subhimpunan tak kosong dari . Jarak dari ke adalah .   "
},
{
  "id": "activity-23",
  "level": "2",
  "url": "sec_dist_point_set.html#activity-23",
  "type": "Kegiatan",
  "number": "5.3",
  "title": "",
  "body": "  Dalam aktivitas ini, kita menelaah beberapa fakta mengenai jarak antara sebuah titik dan suatu himpunan. Misalkan suatu ruang metrik, misalkan , dan misalkan suatu subhimpunan tak kosong dari .    Mengapa pasti ada?    Jika , apakah harus berlaku ?   "
},
{
  "id": "sec_glb_summ",
  "level": "1",
  "url": "sec_glb_summ.html",
  "type": "Bagian",
  "number": "",
  "title": "Ringkasan",
  "body": " Ringkasan  Gagasan penting yang kita bahas dalam bagian ini antara lain sebagai berikut.   Batas bawah untuk subhimpunan tak kosong dari yang terbatas di bawah adalah bilangan real sedemikian sehingga untuk setiap . Batas bawah terbesar (atau infimum) untuk subhimpunan tak kosong dari yang terbatas di bawah adalah bilangan real sedemikian sehingga memenuhi dua syarat berikut.    merupakan batas bawah untuk , dan    jika merupakan batas bawah untuk , maka .       Batas atas untuk subhimpunan tak kosong dari yang terbatas di atas adalah bilangan real sedemikian sehingga untuk setiap . Batas atas terkecil (atau supremum) untuk subhimpunan tak kosong dari yang terbatas di atas adalah bilangan real sedemikian sehingga memenuhi dua syarat berikut.    merupakan batas atas untuk , dan    jika merupakan batas atas untuk , maka .       Jarak dari sebuah titik ke suatu himpunan tak kosong di ruang metrik adalah . Mungkin tidak ada titik yang memenuhi , sehingga infimum diperlukan untuk mendefinisikan jarak ini.     "
},
{
  "id": "sec_glb_exer",
  "level": "1",
  "url": "sec_glb_exer.html",
  "type": "Latihan",
  "number": "",
  "title": "Latihan",
  "body": "  Lima teorema berikut merupakan sasaran pembuktian dalam latihan-latihan di bawah. Bacalah pernyataannya terlebih dahulu, lalu kembangkan setiap pembuktian melalui urutan tugas yang terkait.   Sifat Archimedes  sifat Archimedes   Untuk setiap bilangan real , terdapat bilangan asli sedemikian sehingga .      Untuk setiap bilangan real dan dengan , terdapat bilangan asli sedemikian sehingga .      Jika suatu bilangan real positif, maka terdapat bilangan bulat positif sedemikian sehingga .      Untuk sebarang dua bilangan real yang berbeda dan , terdapat bilangan rasional yang terletak di antaranya.      Untuk sebarang dua bilangan real yang berbeda dan , terdapat bilangan irasional yang terletak di antaranya.      Misalkan suatu subhimpunan tak kosong dari yang terbatas di bawah. Misalkan , dan definisikan sebagai .   Jelaskan mengapa merupakan batas bawah bagi . Jelaskan mengapa memiliki infimum.   Misalkan suatu batas bawah bagi . Tunjukkan bahwa . Lalu jelaskan mengapa .    Misalkan suatu subhimpunan tak kosong dari .   Andaikan terbatas di atas, dan misalkan . Tunjukkan bahwa untuk setiap , terdapat bilangan sedemikian sehingga .   Andaikan terbatas di bawah, dan misalkan . Tunjukkan bahwa untuk setiap , terdapat bilangan sedemikian sehingga .    Misalkan dan merupakan subhimpunan tak kosong dari yang terbatas di atas dan di bawah. Misalkan .   Ikuti langkah-langkah berikut untuk menunjukkan bahwa .   Misalkan dan . Tunjukkan bahwa merupakan batas atas bagi .   Bagian sebelumnya menunjukkan bahwa terbatas di atas sehingga memiliki supremum. Misalkan . Jelaskan mengapa .   Untuk menunjukkan bahwa , kita harus membuktikan bahwa tidak mungkin lebih kecil daripada . Andaikan, demi memperoleh kontradiksi, bahwa . Misalkan . Gunakan hasil untuk memperoleh kontradiksi.   Buktikan bahwa .   Buktikan atau bantah:    Buktikan atau bantah:     Misalkan , dengan , adalah himpunan semua fungsi kontinu dari ke . Definisikan dengan .   Berapakah pada ?   Buktikan bahwa merupakan metrik pada . Deskripsikan secara geometris bagaimana metrik ini mengukur jarak antara fungsi dan . (Metrik ini disebut metrik supremum atau metrik seragam pada .)    Dalam latihan ini, kita membuktikan sifat Archimedes bilangan asli. Perhatikan bahwa himpunan bilangan asli, yang dinotasikan dengan atau , adalah himpunan semua bilangan bulat positif. Misalkan suatu bilangan real.   Andaikan tidak terdapat bilangan bulat positif sedemikian sehingga . Jelaskan bagaimana kita dapat menyimpulkan bahwa terbatas di atas.   Dengan mengandaikan bahwa terbatas di atas, jelaskan mengapa harus memiliki batas atas terkecil .   Jelaskan mengapa tidak mungkin menjadi batas atas terkecil bagi . Jelaskan mengapa hal ini membuktikan sifat Archimedes.    Dalam latihan ini, kita membuktikan dua pernyataan yang ekuivalen dengan sifat Archimedes (lihat ). Kedua pernyataan tersebut dicantumkan dalam pendahuluan kumpulan latihan ini.   Misalkan dan bilangan real dengan .   Tunjukkan bahwa jika sifat Archimedes benar, maka juga benar.   Tunjukkan bahwa jika benar, maka sifat Archimedes juga benar. Simpulkan bahwa ekuivalen dengan sifat Archimedes.   Buktikan bahwa ekuivalen dengan sifat Archimedes.    Kita dapat menggunakan batas bawah terbesar untuk membuktikan teorema tentang kerapatan bilangan rasional yang dicantumkan dalam pendahuluan kumpulan latihan ini. Teorema ini menunjukkan suatu fakta penting bilangan rasional bersifat rapat dalam himpunan bilangan real. Kita membuktikan teorema ini dalam latihan ini. Misalkan dan bilangan real dan andaikan . Berdasarkan sifat Archimedes bilangan asli (lihat Latihan dan ), terdapat bilangan bulat positif sedemikian sehingga . Misalkan . Sifat Archimedes juga menjamin adanya bilangan bulat positif yang memenuhi syarat pembentuk himpunan tersebut; oleh karena itu, himpunan itu tidak kosong.   Tunjukkan bahwa terbatas di bawah dalam .   Jelaskan mengapa memuat suatu bilangan bulat sedemikian sehingga jika dengan , maka . Prinsip Pengurutan Baik berikut mungkin berguna:   Setiap subhimpunan tak kosong dari bilangan bulat yang terbatas di bawah memuat infimumnya.   (Prinsip Pengurutan Baik merupakan salah satu dari banyak aksioma yang ekuivalen dengan Prinsip Induksi Matematika. Prinsip-prinsip ini diterima sebagai aksioma dan dianggap benar.)   Jelaskan mengapa dan . Gunakan pertidaksamaan ini bersama dengan untuk menunjukkan bahwa . Kemudian, temukan suatu bilangan rasional yang terletak di antara dan .    Tunjukkan bahwa setiap bola terbuka dalam memuat suatu titik dengan dan keduanya rasional.    Kita sudah terbiasa menyelesaikan persamaan kuadrat dan memperoleh penyelesaian . Namun, apakah kita benar-benar mengetahui bahwa bilangan ada? Kita membahas pertanyaan tersebut dalam latihan ini dan menunjukkan keberadaan bilangan dengan menggunakan batas bawah terbesar. Di sini, adalah himpunan bilangan real positif.   Sebagai langkah awal, misalkan . Jelaskan mengapa harus memiliki batas bawah terbesar .   Selanjutnya, kita menunjukkan bahwa , sehingga . Kita meninjau kasus dan .   Andaikan . Tunjukkan bahwa terdapat bilangan bulat positif sedemikian sehingga . Jelaskan mengapa hal ini juga tidak mungkin terjadi.   Andaikan . Tunjukkan bahwa terdapat bilangan bulat positif sedemikian sehingga . Jelaskan mengapa hal ini juga tidak mungkin terjadi.   Jelaskan bagaimana kita telah menunjukkan keberadaan .    Serupa dengan , kita dapat membuktikan teorema tentang kerapatan bilangan irasional yang dicantumkan dalam pendahuluan kumpulan latihan ini.   Langkah pertama adalah menunjukkan keberadaan suatu bilangan irasional. Kita akan melakukannya dengan membuktikan bahwa irasional. Gunakan pembuktian dengan kontradiksi dan andaikan bahwa merupakan bilangan rasional. Artinya, untuk suatu bilangan bulat positif dan sedemikian sehingga dan tidak memiliki faktor persekutuan positif selain 1.   Jelaskan mengapa . Karena prima, diperoleh bahwa membagi .   Tunjukkan bahwa membagi . Jelaskan bagaimana hal ini membuktikan bahwa merupakan bilangan irasional.   Misalkan dan dua bilangan real berbeda. Tunjukkan bahwa terdapat bilangan bulat dan bilangan bulat positif sedemikian sehingga merupakan bilangan irasional di antara dan .   Pertimbangkan pendekatan dalam .    Misalkan suatu ruang metrik dan suatu subhimpunan tak kosong dari . Untuk , buktikan bahwa .    Buktikan bahwa jika suatu ruang metrik dan serta subhimpunan tak kosong dari , maka untuk setiap .    Untuk setiap pernyataan berikut, jawab benar jika pernyataan tersebut selalu benar. Jika pernyataan itu hanya kadang-kadang benar atau tidak pernah benar, jawab salah dan berikan contoh konkret yang menunjukkan bahwa pernyataan tersebut salah. Jika suatu pernyataan benar, jelaskan alasannya. Sepanjang latihan ini, misalkan dan subhimpunan tak kosong dan terbatas dari (suatu subhimpunan dari disebut terbatas jika terbatas di atas dan di bawah).   Setiap subhimpunan tak kosong dari terbatas.   Jika , maka .   Jika , maka .   Jika suatu subhimpunan tak kosong dari , maka .   Jika suatu subhimpunan tak kosong dari , maka .   Jika suatu subhimpunan tak kosong dari dan dengan dalam metrik Euklides, maka .   "
},
{
  "id": "theorem-7",
  "level": "2",
  "url": "sec_glb_exer.html#theorem-7",
  "type": "Teorema",
  "number": "5.4",
  "title": "Sifat Archimedes.",
  "body": " Sifat Archimedes  sifat Archimedes   Untuk setiap bilangan real , terdapat bilangan asli sedemikian sehingga .   "
},
{
  "id": "thm_Archimedean_2",
  "level": "2",
  "url": "sec_glb_exer.html#thm_Archimedean_2",
  "type": "Teorema",
  "number": "5.5",
  "title": "",
  "body": "  Untuk setiap bilangan real dan dengan , terdapat bilangan asli sedemikian sehingga .   "
},
{
  "id": "thm_Archimedean_3",
  "level": "2",
  "url": "sec_glb_exer.html#thm_Archimedean_3",
  "type": "Teorema",
  "number": "5.6",
  "title": "",
  "body": "  Jika suatu bilangan real positif, maka terdapat bilangan bulat positif sedemikian sehingga .   "
},
{
  "id": "theorem-10",
  "level": "2",
  "url": "sec_glb_exer.html#theorem-10",
  "type": "Teorema",
  "number": "5.7",
  "title": "",
  "body": "  Untuk sebarang dua bilangan real yang berbeda dan , terdapat bilangan rasional yang terletak di antaranya.   "
},
{
  "id": "theorem-11",
  "level": "2",
  "url": "sec_glb_exer.html#theorem-11",
  "type": "Teorema",
  "number": "5.8",
  "title": "",
  "body": "  Untuk sebarang dua bilangan real yang berbeda dan , terdapat bilangan irasional yang terletak di antaranya.   "
},
{
  "id": "exercise-42",
  "level": "2",
  "url": "sec_glb_exer.html#exercise-42",
  "type": "Latihan",
  "number": "1",
  "title": "",
  "body": " Misalkan suatu subhimpunan tak kosong dari yang terbatas di bawah. Misalkan , dan definisikan sebagai .   Jelaskan mengapa merupakan batas bawah bagi . Jelaskan mengapa memiliki infimum.   Misalkan suatu batas bawah bagi . Tunjukkan bahwa . Lalu jelaskan mengapa .  "
},
{
  "id": "ex_GLB_between",
  "level": "2",
  "url": "sec_glb_exer.html#ex_GLB_between",
  "type": "Latihan",
  "number": "2",
  "title": "",
  "body": " Misalkan suatu subhimpunan tak kosong dari .   Andaikan terbatas di atas, dan misalkan . Tunjukkan bahwa untuk setiap , terdapat bilangan sedemikian sehingga .   Andaikan terbatas di bawah, dan misalkan . Tunjukkan bahwa untuk setiap , terdapat bilangan sedemikian sehingga .  "
},
{
  "id": "exercise-44",
  "level": "2",
  "url": "sec_glb_exer.html#exercise-44",
  "type": "Latihan",
  "number": "3",
  "title": "",
  "body": " Misalkan dan merupakan subhimpunan tak kosong dari yang terbatas di atas dan di bawah. Misalkan .   Ikuti langkah-langkah berikut untuk menunjukkan bahwa .   Misalkan dan . Tunjukkan bahwa merupakan batas atas bagi .   Bagian sebelumnya menunjukkan bahwa terbatas di atas sehingga memiliki supremum. Misalkan . Jelaskan mengapa .   Untuk menunjukkan bahwa , kita harus membuktikan bahwa tidak mungkin lebih kecil daripada . Andaikan, demi memperoleh kontradiksi, bahwa . Misalkan . Gunakan hasil untuk memperoleh kontradiksi.   Buktikan bahwa .   Buktikan atau bantah:    Buktikan atau bantah:   "
},
{
  "id": "ex_GLB_function_sup_metric",
  "level": "2",
  "url": "sec_glb_exer.html#ex_GLB_function_sup_metric",
  "type": "Latihan",
  "number": "4",
  "title": "",
  "body": " Misalkan , dengan , adalah himpunan semua fungsi kontinu dari ke . Definisikan dengan .   Berapakah pada ?   Buktikan bahwa merupakan metrik pada . Deskripsikan secara geometris bagaimana metrik ini mengukur jarak antara fungsi dan . (Metrik ini disebut metrik supremum atau metrik seragam pada .)  "
},
{
  "id": "ex_GLB_Archimedean",
  "level": "2",
  "url": "sec_glb_exer.html#ex_GLB_Archimedean",
  "type": "Latihan",
  "number": "5",
  "title": "",
  "body": " Dalam latihan ini, kita membuktikan sifat Archimedes bilangan asli. Perhatikan bahwa himpunan bilangan asli, yang dinotasikan dengan atau , adalah himpunan semua bilangan bulat positif. Misalkan suatu bilangan real.   Andaikan tidak terdapat bilangan bulat positif sedemikian sehingga . Jelaskan bagaimana kita dapat menyimpulkan bahwa terbatas di atas.   Dengan mengandaikan bahwa terbatas di atas, jelaskan mengapa harus memiliki batas atas terkecil .   Jelaskan mengapa tidak mungkin menjadi batas atas terkecil bagi . Jelaskan mengapa hal ini membuktikan sifat Archimedes.  "
},
{
  "id": "ex_GLB_Archimedean_2",
  "level": "2",
  "url": "sec_glb_exer.html#ex_GLB_Archimedean_2",
  "type": "Latihan",
  "number": "6",
  "title": "",
  "body": " Dalam latihan ini, kita membuktikan dua pernyataan yang ekuivalen dengan sifat Archimedes (lihat ). Kedua pernyataan tersebut dicantumkan dalam pendahuluan kumpulan latihan ini.   Misalkan dan bilangan real dengan .   Tunjukkan bahwa jika sifat Archimedes benar, maka juga benar.   Tunjukkan bahwa jika benar, maka sifat Archimedes juga benar. Simpulkan bahwa ekuivalen dengan sifat Archimedes.   Buktikan bahwa ekuivalen dengan sifat Archimedes.  "
},
{
  "id": "ex_GLB_rational",
  "level": "2",
  "url": "sec_glb_exer.html#ex_GLB_rational",
  "type": "Latihan",
  "number": "7",
  "title": "",
  "body": " Kita dapat menggunakan batas bawah terbesar untuk membuktikan teorema tentang kerapatan bilangan rasional yang dicantumkan dalam pendahuluan kumpulan latihan ini. Teorema ini menunjukkan suatu fakta penting bilangan rasional bersifat rapat dalam himpunan bilangan real. Kita membuktikan teorema ini dalam latihan ini. Misalkan dan bilangan real dan andaikan . Berdasarkan sifat Archimedes bilangan asli (lihat Latihan dan ), terdapat bilangan bulat positif sedemikian sehingga . Misalkan . Sifat Archimedes juga menjamin adanya bilangan bulat positif yang memenuhi syarat pembentuk himpunan tersebut; oleh karena itu, himpunan itu tidak kosong.   Tunjukkan bahwa terbatas di bawah dalam .   Jelaskan mengapa memuat suatu bilangan bulat sedemikian sehingga jika dengan , maka . Prinsip Pengurutan Baik berikut mungkin berguna:   Setiap subhimpunan tak kosong dari bilangan bulat yang terbatas di bawah memuat infimumnya.   (Prinsip Pengurutan Baik merupakan salah satu dari banyak aksioma yang ekuivalen dengan Prinsip Induksi Matematika. Prinsip-prinsip ini diterima sebagai aksioma dan dianggap benar.)   Jelaskan mengapa dan . Gunakan pertidaksamaan ini bersama dengan untuk menunjukkan bahwa . Kemudian, temukan suatu bilangan rasional yang terletak di antara dan .  "
},
{
  "id": "exercise-49",
  "level": "2",
  "url": "sec_glb_exer.html#exercise-49",
  "type": "Latihan",
  "number": "8",
  "title": "",
  "body": " Tunjukkan bahwa setiap bola terbuka dalam memuat suatu titik dengan dan keduanya rasional.  "
},
{
  "id": "exercise-50",
  "level": "2",
  "url": "sec_glb_exer.html#exercise-50",
  "type": "Latihan",
  "number": "9",
  "title": "",
  "body": " Kita sudah terbiasa menyelesaikan persamaan kuadrat dan memperoleh penyelesaian . Namun, apakah kita benar-benar mengetahui bahwa bilangan ada? Kita membahas pertanyaan tersebut dalam latihan ini dan menunjukkan keberadaan bilangan dengan menggunakan batas bawah terbesar. Di sini, adalah himpunan bilangan real positif.   Sebagai langkah awal, misalkan . Jelaskan mengapa harus memiliki batas bawah terbesar .   Selanjutnya, kita menunjukkan bahwa , sehingga . Kita meninjau kasus dan .   Andaikan . Tunjukkan bahwa terdapat bilangan bulat positif sedemikian sehingga . Jelaskan mengapa hal ini juga tidak mungkin terjadi.   Andaikan . Tunjukkan bahwa terdapat bilangan bulat positif sedemikian sehingga . Jelaskan mengapa hal ini juga tidak mungkin terjadi.   Jelaskan bagaimana kita telah menunjukkan keberadaan .  "
},
{
  "id": "ex_GLB_irrational",
  "level": "2",
  "url": "sec_glb_exer.html#ex_GLB_irrational",
  "type": "Latihan",
  "number": "10",
  "title": "",
  "body": " Serupa dengan , kita dapat membuktikan teorema tentang kerapatan bilangan irasional yang dicantumkan dalam pendahuluan kumpulan latihan ini.   Langkah pertama adalah menunjukkan keberadaan suatu bilangan irasional. Kita akan melakukannya dengan membuktikan bahwa irasional. Gunakan pembuktian dengan kontradiksi dan andaikan bahwa merupakan bilangan rasional. Artinya, untuk suatu bilangan bulat positif dan sedemikian sehingga dan tidak memiliki faktor persekutuan positif selain 1.   Jelaskan mengapa . Karena prima, diperoleh bahwa membagi .   Tunjukkan bahwa membagi . Jelaskan bagaimana hal ini membuktikan bahwa merupakan bilangan irasional.   Misalkan dan dua bilangan real berbeda. Tunjukkan bahwa terdapat bilangan bulat dan bilangan bulat positif sedemikian sehingga merupakan bilangan irasional di antara dan .   Pertimbangkan pendekatan dalam .  "
},
{
  "id": "ex_GLB_triangle",
  "level": "2",
  "url": "sec_glb_exer.html#ex_GLB_triangle",
  "type": "Latihan",
  "number": "11",
  "title": "",
  "body": " Misalkan suatu ruang metrik dan suatu subhimpunan tak kosong dari . Untuk , buktikan bahwa .  "
},
{
  "id": "exercise-53",
  "level": "2",
  "url": "sec_glb_exer.html#exercise-53",
  "type": "Latihan",
  "number": "12",
  "title": "",
  "body": " Buktikan bahwa jika suatu ruang metrik dan serta subhimpunan tak kosong dari , maka untuk setiap .  "
},
{
  "id": "exercise-54",
  "level": "2",
  "url": "sec_glb_exer.html#exercise-54",
  "type": "Latihan",
  "number": "13",
  "title": "",
  "body": " Untuk setiap pernyataan berikut, jawab benar jika pernyataan tersebut selalu benar. Jika pernyataan itu hanya kadang-kadang benar atau tidak pernah benar, jawab salah dan berikan contoh konkret yang menunjukkan bahwa pernyataan tersebut salah. Jika suatu pernyataan benar, jelaskan alasannya. Sepanjang latihan ini, misalkan dan subhimpunan tak kosong dan terbatas dari (suatu subhimpunan dari disebut terbatas jika terbatas di atas dan di bawah).   Setiap subhimpunan tak kosong dari terbatas.   Jika , maka .   Jika , maka .   Jika suatu subhimpunan tak kosong dari , maka .   Jika suatu subhimpunan tak kosong dari , maka .   Jika suatu subhimpunan tak kosong dari dan dengan dalam metrik Euklides, maka .  "
},
{
  "id": "sec_cont_func_intro",
  "level": "1",
  "url": "sec_cont_func_intro.html",
  "type": "Bagian",
  "number": "",
  "title": "Pendahuluan",
  "body": " Pendahuluan  Kita mungkin telah menjumpai fungsi kontinu sebelumnya. Kekontinuan merupakan pertimbangan penting dalam masalah optimisasi karena suatu fungsi kontinu mencapai nilai maksimum dan nilai minimum pada setiap interval tertutup dan terbatas. Fungsi kontinu juga memenuhi Teorema Nilai Antara, yakni bahwa suatu fungsi kontinu mengambil semua nilai di antara dan pada interval . Salah satu akibat penting Teorema Nilai Antara adalah bahwa jika merupakan fungsi kontinu pada suatu interval dan serta berlainan tanda, maka pasti mempunyai akar di dalam interval . Dalam bagian ini, kita akan mulai menelaah kekontinuan fungsi antara ruang-ruang metrik. Tujuan akhir kita dalam bagian-bagian mendatang adalah memahami fungsi kontinu dengan cukup baik sehingga kita dapat mendefinisikan kekontinuan hanya dalam kaitannya dengan himpunan terbuka.  Dalam kalkulus, kita membahas gagasan kekontinuan. Suatu fungsi (dengan menggunakan metrik Euklides standar) kontinu di titik jika .  Pernyataan ini mengharuskan kita menjelaskan apa artinya suatu fungsi mempunyai limit di sebuah titik. Secara intuitif, gagasannya adalah bahwa fungsi mempunyai limit ketika jika kita dapat membuat nilai sedekat yang kita inginkan dengan dengan memilih sedekat yang diperlukan dengan (tetapi tidak sama dengan) . Untuk memperluas gagasan limit informal ini menjadi kekontinuan di suatu titik, kita dapat mengatakan bahwa fungsi kontinu di titik jika kita dapat membuat nilai sedekat yang kita inginkan dengan dengan memilih sedekat yang diperlukan dengan (kini boleh sama dengan ).  Untuk mendefinisikan kekontinuan dalam konteks yang lebih umum (di ruang topologis), kita memerlukan definisi kekontinuan yang ketat sebagai landasan. Kita akan mulai dengan membahas fungsi kontinu dari ke , lalu mengembangkannya menjadi fungsi kontinu di ruang metrik. Gagasan-gagasan ini pada akhirnya akan memungkinkan kita mendefinisikan fungsi kontinu di ruang topologis.  Kita mulai dengan mempelajari fungsi kontinu dari ke . Tujuan kita adalah memperketat definisi informal mengenai kekontinuan di suatu titik. Untuk melakukannya, kita perlu mendefinisikan secara formal apa yang dimaksud dengan   membuat nilai  sedekat yang kita inginkan dengan , dan    memilih  sedekat yang kita perlukan dengan .      Ilustrasi definisi kekontinuan di suatu titik.    Grafik biru fungsi kontinu melalui titik di atas x sama dengan a. Dua garis putus-putus magenta pada tinggi f(a) dikurangi epsilon dan f(a) ditambah epsilon membatasi pita horizontal yang diinginkan.    Grafik biru yang sama dengan pita horizontal epsilon, ditambah dua garis putus-putus merah pada x sama dengan a dikurangi delta dan a ditambah delta. Bagian grafik di antara kedua batas delta berada di dalam pita epsilon.     Mari kita bahas pernyataan pertama, yakni membuat nilai  sedekat yang kita inginkan dengan . Artinya, jika kita menetapkan sembarang toleransi, misalnya , kita dapat membuat nilai berjarak kurang dari terhadap . Karena nilai mutlak mengukur kedekatan dengan , kita dapat menuliskan kembali pernyataan bahwa nilai berjarak kurang dari terhadap sebagai . Tentu saja, jarak mungkin belum sedekat yang kita inginkan dengan , sehingga kita memerlukan cara untuk menyatakan bahwa nilai dapat dibuat sedekat apa pun dengan  dalam toleransi sebarang. Untuk itu, kita menjadikan toleransi sebagai parameter . Tugas kita kemudian adalah membuat nilai berjarak kurang dari terhadap , berapa pun besar . Kita menuliskannya sebagai .  Kita dapat menggambarkannya seperti di sisi kiri . Di sini kita ingin membuat nilai berada di dalam pita di sekitar , yakni di atas dan di bawah . Dengan kata lain, kita ingin dapat membuat nilai berada di antara dan .  Sekarang kita harus menjawab pertanyaan tentang cara membuat nilai berjarak kurang dari terhadap . Karena nilai bergantung pada , kita membuat nilai mempunyai sifat yang diinginkan dengan memilih masukan secara tepat. Agar kontinu ketika , kita harus dapat memilih nilai yang cukup dekat dengan sehingga . Secara bergambar, kita dapat melihat bagaimana hal ini terjadi pada gambar di sisi kanan . Kita harus dapat menemukan interval di sekitar sedemikian sehingga graf berada di dalam pita di sekitar untuk nilai-nilai di interval tersebut. Dengan kata lain, kita harus dapat menemukan suatu bilangan positif sedemikian sehingga jika berada dalam interval , maka graf berada dalam pita di sekitar . Secara lebih formal, jika diberikan sembarang toleransi positif , kita harus dapat menemukan bilangan positif sedemikian sehingga jika (yakni, berada dalam interval ), maka (atau berada dalam pita di sekitar ).  Pernyataan ini memberikan definisi yang ketat tentang arti suatu fungsi kontinu di suatu titik.    Suatu fungsi  kontinu di titik jika, untuk setiap , terdapat sedemikian sehingga mengakibatkan .    Perhatikan bahwa nilai boleh bergantung pada nilai dan , tetapi tidak pada nilai .     Laboratorium epsilon-delta O003 memungkinkan kita bereksperimen dengan definisi ini tanpa sambungan jaringan. Gunakan laboratorium interaktif ini untuk dua soal pertama dalam aktivitas ini.    Gunakan fungsi tetap pada laboratorium. Anda dapat mengubah jendela tampilan, titik pangkal , epsilon, dan delta dengan kontrol yang tersedia. Tentukan nilai sedemikian sehingga setiap kali . Jelaskan metode Anda.    Sekarang carilah nilai sedemikian sehingga setiap kali . Jelaskan metode Anda.    Apakah negasi dari definisi kekontinuan di suatu titik? Dengan kata lain, apa yang perlu kita lakukan untuk menunjukkan bahwa suatu fungsi tidak kontinu ketika ?   Gunakan negasi definisi tersebut untuk menjelaskan mengapa fungsi yang didefinisikan oleh tidak kontinu ketika .    "
},
{
  "id": "F_Continuity",
  "level": "2",
  "url": "sec_cont_func_intro.html#F_Continuity",
  "type": "Gambar",
  "number": "6.1",
  "title": "",
  "body": " Ilustrasi definisi kekontinuan di suatu titik.    Grafik biru fungsi kontinu melalui titik di atas x sama dengan a. Dua garis putus-putus magenta pada tinggi f(a) dikurangi epsilon dan f(a) ditambah epsilon membatasi pita horizontal yang diinginkan.    Grafik biru yang sama dengan pita horizontal epsilon, ditambah dua garis putus-putus merah pada x sama dengan a dikurangi delta dan a ditambah delta. Bagian grafik di antara kedua batas delta berada di dalam pita epsilon.    "
},
{
  "id": "def_epsilon_delta_continuity",
  "level": "2",
  "url": "sec_cont_func_intro.html#def_epsilon_delta_continuity",
  "type": "Definisi",
  "number": "6.2",
  "title": "",
  "body": "  Suatu fungsi  kontinu di titik jika, untuk setiap , terdapat sedemikian sehingga mengakibatkan .   "
},
{
  "id": "pa_MS_continuity",
  "level": "2",
  "url": "sec_cont_func_intro.html#pa_MS_continuity",
  "type": "Aktivitas Persiapan",
  "number": "6.1",
  "title": "",
  "body": "   Laboratorium epsilon-delta O003 memungkinkan kita bereksperimen dengan definisi ini tanpa sambungan jaringan. Gunakan laboratorium interaktif ini untuk dua soal pertama dalam aktivitas ini.    Gunakan fungsi tetap pada laboratorium. Anda dapat mengubah jendela tampilan, titik pangkal , epsilon, dan delta dengan kontrol yang tersedia. Tentukan nilai sedemikian sehingga setiap kali . Jelaskan metode Anda.    Sekarang carilah nilai sedemikian sehingga setiap kali . Jelaskan metode Anda.    Apakah negasi dari definisi kekontinuan di suatu titik? Dengan kata lain, apa yang perlu kita lakukan untuk menunjukkan bahwa suatu fungsi tidak kontinu ketika ?   Gunakan negasi definisi tersebut untuk menjelaskan mengapa fungsi yang didefinisikan oleh tidak kontinu ketika .   "
},
{
  "id": "sec_cont_func_btwn",
  "level": "1",
  "url": "sec_cont_func_btwn.html",
  "type": "Bagian",
  "number": "",
  "title": "Fungsi Kontinu antara Ruang-Ruang Metrik",
  "body": " Fungsi Kontinu antara Ruang-Ruang Metrik  Dalam aktivitas pendahuluan, kita telah melihat cara mendefinisikan secara formal arti suatu fungsi kontinu di suatu titik.  Perhatikan bahwa hanya bergantung pada kemampuan untuk mengukur kedekatan antartitik. Karena persis itulah yang dilakukan oleh metrik, kita dapat memperluas gagasan kekontinuan ini untuk mendefinisikan kekontinuan fungsi antara ruang-ruang metrik. Kekontinuan merupakan gagasan penting dalam topologi, dan kita akan banyak menggunakan gagasan ini sepanjang semester.  Jika didefinisikan oleh , maka kita telah melihat bahwa merupakan metrik pada (perhatikan bahwa adalah metrik Euklides pada ). Dengan menggunakan metrik ini, kita dapat merumuskan kembali arti suatu fungsi kontinu di suatu titik.   Definisi Alternatif   Suatu fungsi  kontinu di titik jika, untuk setiap , terdapat sedemikian sehingga mengakibatkan .    Definisi alternatif ini bergantung pada metrik . Kita dapat dengan mudah mengganti metrik dengan metrik lain yang kita pilih. Hal ini memungkinkan kita mendefinisikan kekontinuan di suatu titik bagi fungsi antara ruang-ruang metrik.   kekontinuan di suatu titik dalam ruang metrik   Misalkan dan ruang-ruang metrik. Suatu fungsi  kontinu di jika, untuk setiap , terdapat sedemikian sehingga mengakibatkan .    Setelah mendefinisikan kekontinuan di suatu titik, kita dapat mendefinisikan fungsi kontinu.   fungsi kontinu   Misalkan dan ruang-ruang metrik. Suatu fungsi  kontinu jika kontinu di setiap titik dalam .      Secara umum, untuk membuktikan bahwa fungsi kontinu, dengan dan ruang-ruang metrik, kita mulai dengan memilih unsur sembarang dalam . Kemudian kita ambil suatu bilangan yang lebih besar dari dan menunjukkan bahwa terdapat sedemikian sehingga setiap kali . Nilai yang kita perlukan tidak boleh bergantung pada (karena belum diketahui), tetapi boleh bergantung pada nilai yang kita pilih, dan kemungkinan juga akan bergantung pada . Dengan kata lain, terdapat fungsi yang hanya bergantung pada variabel bebas dan dan menghasilkan , yakni . Sebagai contoh, misalkan dan didefinisikan sebagai .  Pembuktian bahwa merupakan metrik diserahkan kepada . Tinjau yang didefinisikan oleh , dengan . Untuk menunjukkan bahwa kontinu, kita ambil dan .    Pekerjaan pendahuluan. Langkah-langkah berikut bukan bagian dari pembuktian, tetapi menunjukkan cara kita menemukan yang diperlukan. Kita mencari sedemikian sehingga mengakibatkan . Artinya, kita ingin membuat setiap kali . Sekarang . Jika , maka . Jika kita memilih , maka mengakibatkan , sehingga . Sekarang . Akibatnya, . Agar hasil kali ini lebih kecil daripada , kita dapat memilih sedemikian sehingga , atau . Dengan kata lain, pilihan bergantung pada dan ; sebagai contoh, kita dapat mengambil . Sekarang kita kesampingkan paragraf ini dan menyajikan pembuktiannya, yang pada dasarnya membalik langkah-langkah yang baru saja kita lakukan. Jika langkah-langkah itu tidak dapat dibalik, kita harus memikirkan ulang argumen kita. Langkah berikut dalam pembuktian mungkin tampak seperti sulap bagi pembaca yang belum terbiasa, tetapi kita telah melihat apa yang terjadi di balik layar sehingga langkah itu bukan misteri bagi kita.   Misalkan suatu bilangan positif yang lebih kecil daripada . Maka mengakibatkan , sehingga . Selanjutnya, .  Akibatnya, .  Kita menyimpulkan bahwa kontinu di setiap titik dalam , sehingga merupakan fungsi kontinu.    Tidak semua fungsi bersifat kontinu, seperti yang akan kita lihat dalam contoh berikut.    Misalkan dan definisikan dengan . Misalkan metrik Euklides dan metrik diskret. (Ingatlah bahwa setiap kali .) Misalkan dan .  Misalkan , dan ambil . Maka dan . Akan tetapi, .  Jadi, jika , tidak terdapat sedemikian sehingga mengakibatkan . Kita menyimpulkan bahwa tidak kontinu di titik mana pun dalam .    Fungsi-fungsi tertentu selalu kontinu, seperti ditunjukkan oleh aktivitas berikut.    Misalkan dan ruang-ruang metrik, dan misalkan . Definisikan dengan untuk setiap . Tunjukkan bahwa merupakan fungsi kontinu.    Misalkan suatu ruang metrik. Definisikan fungsi dengan untuk setiap . Tunjukkan bahwa merupakan fungsi kontinu. (Fungsi disebut fungsi identitas  fungsi identitas pada .)    Mengapa argumen pada bagian (b) tidak bertentangan dengan ?    Contoh-contoh yang lebih rumit terdapat dalam aktivitas berikut.    Misalkan dan , dengan merupakan metrik taksi dan merupakan metrik maksimum. Definisikan dengan .    Apakah merupakan fungsi kontinu dari ke ? Berikan alasan untuk jawaban Anda.    Apakah merupakan fungsi kontinu dari ke ? Berikan alasan untuk jawaban Anda.    "
},
{
  "id": "definition-18",
  "level": "2",
  "url": "sec_cont_func_btwn.html#definition-18",
  "type": "Definisi",
  "number": "6.3",
  "title": "Definisi Alternatif.",
  "body": " Definisi Alternatif   Suatu fungsi  kontinu di titik jika, untuk setiap , terdapat sedemikian sehingga mengakibatkan .   "
},
{
  "id": "definition-19",
  "level": "2",
  "url": "sec_cont_func_btwn.html#definition-19",
  "type": "Definisi",
  "number": "6.4",
  "title": "",
  "body": " kekontinuan di suatu titik dalam ruang metrik   Misalkan dan ruang-ruang metrik. Suatu fungsi  kontinu di jika, untuk setiap , terdapat sedemikian sehingga mengakibatkan .   "
},
{
  "id": "definition-20",
  "level": "2",
  "url": "sec_cont_func_btwn.html#definition-20",
  "type": "Definisi",
  "number": "6.5",
  "title": "",
  "body": " fungsi kontinu   Misalkan dan ruang-ruang metrik. Suatu fungsi  kontinu jika kontinu di setiap titik dalam .   "
},
{
  "id": "example-3",
  "level": "2",
  "url": "sec_cont_func_btwn.html#example-3",
  "type": "Contoh",
  "number": "6.6",
  "title": "",
  "body": "  Secara umum, untuk membuktikan bahwa fungsi kontinu, dengan dan ruang-ruang metrik, kita mulai dengan memilih unsur sembarang dalam . Kemudian kita ambil suatu bilangan yang lebih besar dari dan menunjukkan bahwa terdapat sedemikian sehingga setiap kali . Nilai yang kita perlukan tidak boleh bergantung pada (karena belum diketahui), tetapi boleh bergantung pada nilai yang kita pilih, dan kemungkinan juga akan bergantung pada . Dengan kata lain, terdapat fungsi yang hanya bergantung pada variabel bebas dan dan menghasilkan , yakni . Sebagai contoh, misalkan dan didefinisikan sebagai .  Pembuktian bahwa merupakan metrik diserahkan kepada . Tinjau yang didefinisikan oleh , dengan . Untuk menunjukkan bahwa kontinu, kita ambil dan .    Pekerjaan pendahuluan. Langkah-langkah berikut bukan bagian dari pembuktian, tetapi menunjukkan cara kita menemukan yang diperlukan. Kita mencari sedemikian sehingga mengakibatkan . Artinya, kita ingin membuat setiap kali . Sekarang . Jika , maka . Jika kita memilih , maka mengakibatkan , sehingga . Sekarang . Akibatnya, . Agar hasil kali ini lebih kecil daripada , kita dapat memilih sedemikian sehingga , atau . Dengan kata lain, pilihan bergantung pada dan ; sebagai contoh, kita dapat mengambil . Sekarang kita kesampingkan paragraf ini dan menyajikan pembuktiannya, yang pada dasarnya membalik langkah-langkah yang baru saja kita lakukan. Jika langkah-langkah itu tidak dapat dibalik, kita harus memikirkan ulang argumen kita. Langkah berikut dalam pembuktian mungkin tampak seperti sulap bagi pembaca yang belum terbiasa, tetapi kita telah melihat apa yang terjadi di balik layar sehingga langkah itu bukan misteri bagi kita.   Misalkan suatu bilangan positif yang lebih kecil daripada . Maka mengakibatkan , sehingga . Selanjutnya, .  Akibatnya, .  Kita menyimpulkan bahwa kontinu di setiap titik dalam , sehingga merupakan fungsi kontinu.   "
},
{
  "id": "exp_not_continuous",
  "level": "2",
  "url": "sec_cont_func_btwn.html#exp_not_continuous",
  "type": "Contoh",
  "number": "6.7",
  "title": "",
  "body": "  Misalkan dan definisikan dengan . Misalkan metrik Euklides dan metrik diskret. (Ingatlah bahwa setiap kali .) Misalkan dan .  Misalkan , dan ambil . Maka dan . Akan tetapi, .  Jadi, jika , tidak terdapat sedemikian sehingga mengakibatkan . Kita menyimpulkan bahwa tidak kontinu di titik mana pun dalam .   "
},
{
  "id": "act_id_constant_continuous",
  "level": "2",
  "url": "sec_cont_func_btwn.html#act_id_constant_continuous",
  "type": "Kegiatan",
  "number": "6.2",
  "title": "",
  "body": "  Misalkan dan ruang-ruang metrik, dan misalkan . Definisikan dengan untuk setiap . Tunjukkan bahwa merupakan fungsi kontinu.    Misalkan suatu ruang metrik. Definisikan fungsi dengan untuk setiap . Tunjukkan bahwa merupakan fungsi kontinu. (Fungsi disebut fungsi identitas  fungsi identitas pada .)    Mengapa argumen pada bagian (b) tidak bertentangan dengan ?   "
},
{
  "id": "activity-25",
  "level": "2",
  "url": "sec_cont_func_btwn.html#activity-25",
  "type": "Kegiatan",
  "number": "6.3",
  "title": "",
  "body": "  Misalkan dan , dengan merupakan metrik taksi dan merupakan metrik maksimum. Definisikan dengan .    Apakah merupakan fungsi kontinu dari ke ? Berikan alasan untuk jawaban Anda.    Apakah merupakan fungsi kontinu dari ke ? Berikan alasan untuk jawaban Anda.   "
},
{
  "id": "sec_comp_cont_func",
  "level": "1",
  "url": "sec_comp_cont_func.html",
  "type": "Bagian",
  "number": "",
  "title": "Komposit Fungsi Kontinu",
  "body": " Komposit Fungsi Kontinu  Misalkan , , dan merupakan ruang-ruang metrik, dan andaikan serta merupakan fungsi kontinu. Wajar jika kita bertanya apakah komposit juga merupakan fungsi kontinu.    Misalkan , , dan merupakan ruang-ruang metrik, dan andaikan serta merupakan fungsi kontinu. Kita akan membuktikan bahwa merupakan fungsi kontinu.    Apa yang harus kita lakukan untuk menunjukkan bahwa merupakan fungsi kontinu? Apa dua langkah pertama dalam pembuktian kita?    Misalkan dan misalkan . Andaikan diberikan . Jelaskan mengapa pasti ada sedemikian sehingga mengakibatkan .    Sekarang jelaskan mengapa ada sedemikian sehingga mengakibatkan .    Buktikan bahwa merupakan fungsi kontinu.    Kekontinuan merupakan konsep penting dalam topologi. Kita telah melihat cara mendefinisikan kekontinuan di ruang metrik, dan tidak lama lagi kita akan memperluas gagasan ini untuk mendefinisikan kekontinuan tanpa merujuk pada metrik sama sekali. Dengan demikian, kelak kita dapat mendefinisikan fungsi kontinu di antara sebarang ruang topologis.  "
},
{
  "id": "activity-26",
  "level": "2",
  "url": "sec_comp_cont_func.html#activity-26",
  "type": "Kegiatan",
  "number": "6.4",
  "title": "",
  "body": "  Misalkan , , dan merupakan ruang-ruang metrik, dan andaikan serta merupakan fungsi kontinu. Kita akan membuktikan bahwa merupakan fungsi kontinu.    Apa yang harus kita lakukan untuk menunjukkan bahwa merupakan fungsi kontinu? Apa dua langkah pertama dalam pembuktian kita?    Misalkan dan misalkan . Andaikan diberikan . Jelaskan mengapa pasti ada sedemikian sehingga mengakibatkan .    Sekarang jelaskan mengapa ada sedemikian sehingga mengakibatkan .    Buktikan bahwa merupakan fungsi kontinu.   "
},
{
  "id": "sec_cont_func_summ",
  "level": "1",
  "url": "sec_cont_func_summ.html",
  "type": "Bagian",
  "number": "",
  "title": "Ringkasan",
  "body": " Ringkasan  Gagasan-gagasan penting yang kita bahas dalam bagian ini mencakup hal-hal berikut.   Misalkan dan merupakan ruang metrik. Suatu fungsi kontinu di jika, untuk setiap , terdapat sedemikian sehingga mengakibatkan .    Misalkan dan merupakan ruang metrik. Suatu fungsi kontinu jika kontinu di setiap titik dalam .     "
},
{
  "id": "sec_cont_func_exer",
  "level": "1",
  "url": "sec_cont_func_exer.html",
  "type": "Latihan",
  "number": "",
  "title": "Latihan",
  "body": "  Misalkan didefinisikan oleh , dengan metrik Euklides pada domain maupun kodomain. Apakah kontinu di ? Buktikan jawaban Anda.    Misalkan didefinisikan oleh Apakah kontinu di ? Buktikan jawaban Anda.    Misalkan , dengan sebagai metrik Euklides.   Misalkan . Buktikan atau berikan contoh tandingan: fungsi yang didefinisikan oleh bersifat kontinu.   Misalkan , dengan sebagai metrik maksimum. Buktikan atau berikan contoh tandingan: fungsi yang didefinisikan oleh bersifat kontinu.    Misalkan sebarang himpunan dan definisikan dengan  meminta kita menunjukkan bahwa merupakan metrik (metrik diskret) pada . Misalkan dan merupakan ruang metrik, dengan sebagai metrik diskret. Tentukan semua fungsi kontinu dari ke .    Misalkan dan merupakan fungsi kontinu dari ke .   Misalkan dengan dan definisikan dengan untuk setiap . Tunjukkan bahwa merupakan fungsi kontinu.   Definisikan dengan untuk setiap . Tunjukkan bahwa merupakan fungsi kontinu.    Misalkan dan merupakan fungsi kontinu dari ke . Dalam soal ini, kita akan membuktikan bahwa merupakan fungsi kontinu dari ke . Misalkan berada di , dan ikuti langkah-langkah berikut untuk menunjukkan bahwa kontinu di . Misalkan suatu bilangan positif.   Mula-mula, kita akan menyatakan dalam bentuk yang lebih berguna. Gunakan fakta bahwa dan untuk menunjukkan bahwa .   Jelaskan mengapa terdapat bilangan-bilangan positif , , , dan sedemikian sehingga .   Gunakan hasil dari (a) dan (b) untuk menunjukkan bahwa kontinu di . (Petunjuk: .)    Misalkan dan merupakan fungsi dari ke .   Benarkah bahwa jika merupakan fungsi kontinu, maka dan juga merupakan fungsi kontinu? Buktikan jawaban Anda.   Benarkah bahwa jika merupakan fungsi kontinu, maka dan juga merupakan fungsi kontinu? Buktikan jawaban Anda.    Misalkan memetakan ke , dengan metrik Euklides pada domain maupun kodomain.   Misalkan . Carilah nilai sedemikian sehingga mengakibatkan . Anda dapat menggunakan Laboratorium epsilon-delta O003 untuk memeriksa nilai Anda secara numerik.   Buktikan bahwa kontinu di .    Definisikan dengan . Buktikan bahwa merupakan metrik.    Misalkan merupakan fungsi kontinu, dengan metrik Euklides pada kedua salinan . Andaikan setiap kali rasional. Buktikan bahwa untuk setiap .   Gunakan .    Misalkan didefinisikan oleh jika irasional dan jika rasional. Gunakan metrik Euklides pada kedua salinan . Tunjukkan bahwa tidak kontinu di titik mana pun dalam .   Gunakan dan .    Misalkan didefinisikan oleh jika irasional dan jika rasional. Gunakan metrik Euklides pada kedua salinan . Tunjukkan bahwa hanya kontinu di .    Misalkan dan himpunan semua fungsi kontinu . Misalkan fungsi jarak pada yang didefinisikan oleh , untuk . Untuk setiap , tetapkan .   Tentukan nilai ketika , , dan .   Tentukan nilai jika dan .   Buktikan bahwa fungsi bersifat kontinu, dengan sebagai metrik Euklides.   Sebelum mencoba membuktikan pernyataan ini, akan membantu jika Anda terlebih dahulu menuliskan secara eksplisit apa artinya kontinu dalam metrik dan .    Untuk setiap pernyataan berikut, jawablah benar jika pernyataan itu selalu benar. Jika pernyataan itu hanya kadang-kadang benar atau tidak pernah benar, jawablah salah dan berikan contoh konkret yang menunjukkan bahwa pernyataan tersebut salah. Jika suatu pernyataan benar, jelaskan alasannya.   Misalkan suatu fungsi, dengan dan sebagai ruang metrik. Jika merupakan metrik diskret dan sebarang metrik, maka kontinu.   Misalkan suatu fungsi, dengan dan sebagai ruang metrik. Jika merupakan metrik diskret dan sebarang metrik, maka kontinu.   Misalkan dan dua metrik pada suatu himpunan . Fungsi identitas yang didefinisikan oleh untuk setiap bersifat kontinu.   Misalkan dan merupakan fungsi kontinu dari (metrik taksi) ke . Maka fungsi dari ke yang didefinisikan oleh untuk setiap merupakan fungsi kontinu.   Jika dan merupakan ruang metrik dengan , maka fungsi konstan yang didefinisikan oleh untuk setiap merupakan fungsi kontinu.   "
},
{
  "id": "exercise-55",
  "level": "2",
  "url": "sec_cont_func_exer.html#exercise-55",
  "type": "Latihan",
  "number": "1",
  "title": "",
  "body": " Misalkan didefinisikan oleh , dengan metrik Euklides pada domain maupun kodomain. Apakah kontinu di ? Buktikan jawaban Anda.  "
},
{
  "id": "exercise-56",
  "level": "2",
  "url": "sec_cont_func_exer.html#exercise-56",
  "type": "Latihan",
  "number": "2",
  "title": "",
  "body": " Misalkan didefinisikan oleh Apakah kontinu di ? Buktikan jawaban Anda.  "
},
{
  "id": "exercise-57",
  "level": "2",
  "url": "sec_cont_func_exer.html#exercise-57",
  "type": "Latihan",
  "number": "3",
  "title": "",
  "body": " Misalkan , dengan sebagai metrik Euklides.   Misalkan . Buktikan atau berikan contoh tandingan: fungsi yang didefinisikan oleh bersifat kontinu.   Misalkan , dengan sebagai metrik maksimum. Buktikan atau berikan contoh tandingan: fungsi yang didefinisikan oleh bersifat kontinu.  "
},
{
  "id": "exercise-58",
  "level": "2",
  "url": "sec_cont_func_exer.html#exercise-58",
  "type": "Latihan",
  "number": "4",
  "title": "",
  "body": " Misalkan sebarang himpunan dan definisikan dengan  meminta kita menunjukkan bahwa merupakan metrik (metrik diskret) pada . Misalkan dan merupakan ruang metrik, dengan sebagai metrik diskret. Tentukan semua fungsi kontinu dari ke .  "
},
{
  "id": "ex_sum_continuous",
  "level": "2",
  "url": "sec_cont_func_exer.html#ex_sum_continuous",
  "type": "Latihan",
  "number": "5",
  "title": "",
  "body": " Misalkan dan merupakan fungsi kontinu dari ke .   Misalkan dengan dan definisikan dengan untuk setiap . Tunjukkan bahwa merupakan fungsi kontinu.   Definisikan dengan untuk setiap . Tunjukkan bahwa merupakan fungsi kontinu.  "
},
{
  "id": "exercise-60",
  "level": "2",
  "url": "sec_cont_func_exer.html#exercise-60",
  "type": "Latihan",
  "number": "6",
  "title": "",
  "body": " Misalkan dan merupakan fungsi kontinu dari ke . Dalam soal ini, kita akan membuktikan bahwa merupakan fungsi kontinu dari ke . Misalkan berada di , dan ikuti langkah-langkah berikut untuk menunjukkan bahwa kontinu di . Misalkan suatu bilangan positif.   Mula-mula, kita akan menyatakan dalam bentuk yang lebih berguna. Gunakan fakta bahwa dan untuk menunjukkan bahwa .   Jelaskan mengapa terdapat bilangan-bilangan positif , , , dan sedemikian sehingga .   Gunakan hasil dari (a) dan (b) untuk menunjukkan bahwa kontinu di . (Petunjuk: .)  "
},
{
  "id": "exercise-61",
  "level": "2",
  "url": "sec_cont_func_exer.html#exercise-61",
  "type": "Latihan",
  "number": "7",
  "title": "",
  "body": " Misalkan dan merupakan fungsi dari ke .   Benarkah bahwa jika merupakan fungsi kontinu, maka dan juga merupakan fungsi kontinu? Buktikan jawaban Anda.   Benarkah bahwa jika merupakan fungsi kontinu, maka dan juga merupakan fungsi kontinu? Buktikan jawaban Anda.  "
},
{
  "id": "exercise-62",
  "level": "2",
  "url": "sec_cont_func_exer.html#exercise-62",
  "type": "Latihan",
  "number": "8",
  "title": "",
  "body": " Misalkan memetakan ke , dengan metrik Euklides pada domain maupun kodomain.   Misalkan . Carilah nilai sedemikian sehingga mengakibatkan . Anda dapat menggunakan Laboratorium epsilon-delta O003 untuk memeriksa nilai Anda secara numerik.   Buktikan bahwa kontinu di .  "
},
{
  "id": "ex_min_1_metric",
  "level": "2",
  "url": "sec_cont_func_exer.html#ex_min_1_metric",
  "type": "Latihan",
  "number": "9",
  "title": "",
  "body": " Definisikan dengan . Buktikan bahwa merupakan metrik.  "
},
{
  "id": "exercise-64",
  "level": "2",
  "url": "sec_cont_func_exer.html#exercise-64",
  "type": "Latihan",
  "number": "10",
  "title": "",
  "body": " Misalkan merupakan fungsi kontinu, dengan metrik Euklides pada kedua salinan . Andaikan setiap kali rasional. Buktikan bahwa untuk setiap .   Gunakan .  "
},
{
  "id": "exercise-65",
  "level": "2",
  "url": "sec_cont_func_exer.html#exercise-65",
  "type": "Latihan",
  "number": "11",
  "title": "",
  "body": " Misalkan didefinisikan oleh jika irasional dan jika rasional. Gunakan metrik Euklides pada kedua salinan . Tunjukkan bahwa tidak kontinu di titik mana pun dalam .   Gunakan dan .  "
},
{
  "id": "exercise-66",
  "level": "2",
  "url": "sec_cont_func_exer.html#exercise-66",
  "type": "Latihan",
  "number": "12",
  "title": "",
  "body": " Misalkan didefinisikan oleh jika irasional dan jika rasional. Gunakan metrik Euklides pada kedua salinan . Tunjukkan bahwa hanya kontinu di .  "
},
{
  "id": "exercise-67",
  "level": "2",
  "url": "sec_cont_func_exer.html#exercise-67",
  "type": "Latihan",
  "number": "13",
  "title": "",
  "body": " Misalkan dan himpunan semua fungsi kontinu . Misalkan fungsi jarak pada yang didefinisikan oleh , untuk . Untuk setiap , tetapkan .   Tentukan nilai ketika , , dan .   Tentukan nilai jika dan .   Buktikan bahwa fungsi bersifat kontinu, dengan sebagai metrik Euklides.   Sebelum mencoba membuktikan pernyataan ini, akan membantu jika Anda terlebih dahulu menuliskan secara eksplisit apa artinya kontinu dalam metrik dan .  "
},
{
  "id": "exercise-68",
  "level": "2",
  "url": "sec_cont_func_exer.html#exercise-68",
  "type": "Latihan",
  "number": "14",
  "title": "",
  "body": " Untuk setiap pernyataan berikut, jawablah benar jika pernyataan itu selalu benar. Jika pernyataan itu hanya kadang-kadang benar atau tidak pernah benar, jawablah salah dan berikan contoh konkret yang menunjukkan bahwa pernyataan tersebut salah. Jika suatu pernyataan benar, jelaskan alasannya.   Misalkan suatu fungsi, dengan dan sebagai ruang metrik. Jika merupakan metrik diskret dan sebarang metrik, maka kontinu.   Misalkan suatu fungsi, dengan dan sebagai ruang metrik. Jika merupakan metrik diskret dan sebarang metrik, maka kontinu.   Misalkan dan dua metrik pada suatu himpunan . Fungsi identitas yang didefinisikan oleh untuk setiap bersifat kontinu.   Misalkan dan merupakan fungsi kontinu dari (metrik taksi) ke . Maka fungsi dari ke yang didefinisikan oleh untuk setiap merupakan fungsi kontinu.   Jika dan merupakan ruang metrik dengan , maka fungsi konstan yang didefinisikan oleh untuk setiap merupakan fungsi kontinu.  "
},
{
  "id": "sec_open_balls_intro",
  "level": "1",
  "url": "sec_open_balls_intro.html",
  "type": "Bagian",
  "number": "",
  "title": "Pendahuluan",
  "body": " Pendahuluan  Himpunan terbuka sangat penting dalam topologi. Nanti kita akan melihat bahwa setiap ruang topologis sepenuhnya ditentukan oleh himpunan-himpunan terbukanya, dan fungsi kontinu dapat didefinisikan hanya dengan menggunakan himpunan terbuka. Pada bagian ini kita memperkenalkan gagasan bola terbuka dan lingkungan dalam ruang metrik serta menemukan beberapa sifatnya. Pembahasan ini akan menjadi landasan untuk memperkenalkan himpunan terbuka pada bagian berikutnya.  Ingat bahwa kekontinuan suatu fungsi dari ruang metrik ke ruang metrik di titik didefinisikan menggunakan himpunan titik yang memenuhi dan titik yang memenuhi , untuk bilangan real positif dan . Dalam dengan metrik Euklides , untuk bilangan real dan , himpunan nilai yang memenuhi adalah himpunan nilai yang memenuhi . Kita sering menuliskan himpunan ini dalam notasi interval sebagai dan menyebut sebagai interval terbuka. Alasan informal mengapa kita menyebut interval tersebut terbuka (berbeda dengan interval , , or ) ialah bahwa interval terbuka tidak memuat satu pun dari kedua titik ujungnya. Alasan yang lebih mendasar untuk menyebut interval tersebut terbuka ialah bahwa jika adalah sembarang unsur dalam , maka kita dapat menemukan interval terbuka lain di sekitar yang seluruhnya termuat dalam interval . Jadi, secara naif, kita dapat membayangkan interval terbuka sebagai interval yang menyediakan cukup ruang bagi setiap titik di dalamnya untuk sedikit bergerak di sekitar posisinya sambil tetap berada di dalam interval tersebut.  Karena interval terbuka dapat dijelaskan sepenuhnya dengan metrik Euklides sebagai himpunan nilai yang memenuhi , tidak ada alasan untuk tidak memperluas gagasan interval terbuka ini ke sembarang ruang metrik. Namun, perlu kita perhatikan bahwa berdimensi satu, sedangkan kebanyakan ruang metrik tidak demikian, sehingga istilah interval tidak lagi sesuai. Kita mengganti konsep interval dengan konsep bola terbuka.   bola terbuka dalam ruang metrik   Misalkan suatu ruang metrik dan . Untuk , bola terbuka berjari-jari dan berpusat di adalah himpunan .    Perlu diperhatikan bahwa notasi kita untuk bola terbuka tidak digunakan secara universal. Sebagai contoh, beberapa buku menggunakan untuk menyatakan dalam notasi kita.    Jelaskan dan buat sketsa bola terbuka yang dinyatakan pada masing-masing ruang metrik berikut.    Bola terbuka dalam ruang metrik dengan metrik Euklides .    Bola terbuka dalam ruang metrik dengan metrik Euklides .    Bola terbuka dalam ruang metrik dengan metrik maksimum .    Bola terbuka dalam ruang metrik dengan metrik taksi .    Bola terbuka dalam ruang metrik dengan metrik diskret . Apa perbedaan antara dan dalam ruang metrik ini jika ? Bagaimana jika ?    "
},
{
  "id": "definition-21",
  "level": "2",
  "url": "sec_open_balls_intro.html#definition-21",
  "type": "Definisi",
  "number": "7.1",
  "title": "",
  "body": " bola terbuka dalam ruang metrik   Misalkan suatu ruang metrik dan . Untuk , bola terbuka berjari-jari dan berpusat di adalah himpunan .   "
},
{
  "id": "exploration-6",
  "level": "2",
  "url": "sec_open_balls_intro.html#exploration-6",
  "type": "Aktivitas Persiapan",
  "number": "7.1",
  "title": "",
  "body": "  Jelaskan dan buat sketsa bola terbuka yang dinyatakan pada masing-masing ruang metrik berikut.    Bola terbuka dalam ruang metrik dengan metrik Euklides .    Bola terbuka dalam ruang metrik dengan metrik Euklides .    Bola terbuka dalam ruang metrik dengan metrik maksimum .    Bola terbuka dalam ruang metrik dengan metrik taksi .    Bola terbuka dalam ruang metrik dengan metrik diskret . Apa perbedaan antara dan dalam ruang metrik ini jika ? Bagaimana jika ?   "
},
{
  "id": "sec_neighborhoods",
  "level": "1",
  "url": "sec_neighborhoods.html",
  "type": "Bagian",
  "number": "",
  "title": "Lingkungan",
  "body": " Lingkungan  -lingkungan suatu titik dalam ruang metrik  Kita telah mengenal gagasan interval terbuka dalam . Selanjutnya, kita memperkenalkan gagasan lingkungan suatu titik dan mencirikan kekontinuan dalam kaitannya dengan lingkungan. Ini merupakan langkah berikutnya dalam mengembangkan gagasan kekontinuan di ruang topologis.  Bola terbuka dalam ruang metrik juga disebut -lingkungan di sekitar . Lingkungan suatu titik dapat dipandang sebagai sebarang himpunan yang mencakup titik tersebut.   lingkungan dalam ruang metrik   Misalkan suatu ruang metrik dan . Suatu subhimpunan dari merupakan lingkungan bagi jika terdapat sedemikian sehingga .         Dalam dengan metrik Euklides, himpunan (bilangan-bilangan riil positif) merupakan lingkungan bagi karena bola terbuka termuat seluruhnya dalam .    Dalam dengan metrik Euklides, himpunan bukan lingkungan bagi karena setiap bola terbuka yang berpusat di memuat sejumlah bilangan bukan bulat.    Dalam dengan metrik diskret, himpunan merupakan lingkungan bagi karena bola terbuka .       Sebagai contoh lain, bola terbuka merupakan lingkungan bagi . Kita bahkan dapat mengatakan lebih banyak mengenai bola terbuka.    Misalkan suatu ruang metrik, , dan . Dalam aktivitas ini, kita mengajukan pertanyaan: apakah merupakan lingkungan bagi setiap titik di dalamnya?    Misalkan . Apa yang harus kita lakukan untuk menunjukkan bahwa merupakan lingkungan bagi ?    Gunakan untuk membantu menunjukkan bahwa merupakan lingkungan bagi .   sebagai lingkungan bagi .   Bola besar berwarna biru dengan garis putus-putus, B(a, delta), berpusat di a. Titik b berada di dalam bola itu dan dihubungkan ke a oleh sebuah ruas garis. Bola lebih kecil berwarna magenta dengan garis putus-putus berpusat di b dan seluruhnya berada di dalam bola besar.      Apakah pernyataan sebaliknya benar? Artinya, jika suatu himpunan merupakan lingkungan bagi setiap titiknya, apakah himpunan tersebut merupakan bola terbuka? Pembuktian tidak diperlukan, tetapi berikan argumen yang meyakinkan.    "
},
{
  "id": "p-765",
  "level": "2",
  "url": "sec_neighborhoods.html#p-765",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "-lingkungan "
},
{
  "id": "definition-22",
  "level": "2",
  "url": "sec_neighborhoods.html#definition-22",
  "type": "Definisi",
  "number": "7.2",
  "title": "",
  "body": " lingkungan dalam ruang metrik   Misalkan suatu ruang metrik dan . Suatu subhimpunan dari merupakan lingkungan bagi jika terdapat sedemikian sehingga .   "
},
{
  "id": "exp_neighborhood_MS",
  "level": "2",
  "url": "sec_neighborhoods.html#exp_neighborhood_MS",
  "type": "Contoh",
  "number": "7.3",
  "title": "",
  "body": "     Dalam dengan metrik Euklides, himpunan (bilangan-bilangan riil positif) merupakan lingkungan bagi karena bola terbuka termuat seluruhnya dalam .    Dalam dengan metrik Euklides, himpunan bukan lingkungan bagi karena setiap bola terbuka yang berpusat di memuat sejumlah bilangan bukan bulat.    Dalam dengan metrik diskret, himpunan merupakan lingkungan bagi karena bola terbuka .      "
},
{
  "id": "activity-27",
  "level": "2",
  "url": "sec_neighborhoods.html#activity-27",
  "type": "Kegiatan",
  "number": "7.2",
  "title": "",
  "body": "  Misalkan suatu ruang metrik, , dan . Dalam aktivitas ini, kita mengajukan pertanyaan: apakah merupakan lingkungan bagi setiap titik di dalamnya?    Misalkan . Apa yang harus kita lakukan untuk menunjukkan bahwa merupakan lingkungan bagi ?    Gunakan untuk membantu menunjukkan bahwa merupakan lingkungan bagi .   sebagai lingkungan bagi .   Bola besar berwarna biru dengan garis putus-putus, B(a, delta), berpusat di a. Titik b berada di dalam bola itu dan dihubungkan ke a oleh sebuah ruas garis. Bola lebih kecil berwarna magenta dengan garis putus-putus berpusat di b dan seluruhnya berada di dalam bola besar.      Apakah pernyataan sebaliknya benar? Artinya, jika suatu himpunan merupakan lingkungan bagi setiap titiknya, apakah himpunan tersebut merupakan bola terbuka? Pembuktian tidak diperlukan, tetapi berikan argumen yang meyakinkan.   "
},
{
  "id": "sec_cont_neighborhoods",
  "level": "1",
  "url": "sec_cont_neighborhoods.html",
  "type": "Bagian",
  "number": "",
  "title": "Kekontinuan dan Lingkungan",
  "body": " Kekontinuan dan Lingkungan  Sekarang kita dapat mendefinisikan kekontinuan dalam kaitannya dengan lingkungan alih-alih menggunakan metrik. Keuntungannya adalah bahwa gagasan ini tidak secara eksplisit bergantung pada keberadaan metrik, sehingga kita akan dapat menggunakan konsep kekontinuan ini untuk ruang topologis sebarang.  Ingatlah bahwa suatu fungsi dari ruang metrik ke ruang metrik kontinu di jika, untuk setiap , terdapat sedemikian sehingga mengakibatkan . Kita dapat menafsirkan definisi kekontinuan ini dengan mengatakan bahwa untuk setiap , di bawah fungsi , prapeta bola terbuka memuat bola terbuka untuk suatu . Wajar jika kita bertanya apakah himpunan itu sendiri merupakan bola terbuka. Kita menyelidiki pertanyaan ini dalam aktivitas berikut.    Misalkan suatu fungsi dari ruang metrik ke ruang metrik yang kontinu di . Dengan menggunakan notasi dari paragraf di atas, dalam aktivitas ini kita menentukan apakah harus sama dengan untuk suatu .  Definisikan dengan , dan gunakan metrik Euklides pada seluruh aktivitas. Asumsikan bahwa merupakan fungsi kontinu. Maka kontinu di .    Tentukan .    Tentukan .    Apakah merupakan bola terbuka yang berpusat di ? Jelaskan.    Kesimpulan yang dapat ditarik dari adalah bahwa jika kontinu, kita hanya dapat menyimpulkan bahwa prapeta  memuat sebuah bola terbuka yang berpusat di . Menurut definisi kekontinuan, jika untuk setiap terdapat sedemikian sehingga memuat bola terbuka , maka kontinu di . Kita merangkum hal ini dalam teorema berikut.    Misalkan suatu fungsi dari ruang metrik ke ruang metrik , dan misalkan . Maka kontinu di jika dan hanya jika, untuk setiap , terdapat sedemikian sehingga .    Kita dapat memperluas gagasan kekontinuan ini untuk mendeskripsikan kekontinuan dalam kaitannya dengan lingkungan. Syarat ini nantinya memungkinkan kita meninjau fungsi kontinu sekalipun ruang kita tidak dilengkapi metrik.    Misalkan dan ruang-ruang metrik, dan misalkan suatu fungsi. Maka kontinu di jika dan hanya jika prapeta setiap lingkungan bagi merupakan lingkungan bagi .    Misalkan dan ruang-ruang metrik, dan misalkan suatu fungsi. Untuk membuktikan pernyataan bikondisional ini, kita harus membuktikan kedua implikasinya. Pertama, asumsikan bahwa kontinu di suatu titik . Kita akan menunjukkan bahwa untuk setiap lingkungan bagi dalam , prapetanya, yaitu dalam , merupakan lingkungan bagi dalam . Misalkan suatu lingkungan bagi dalam . Untuk menunjukkan bahwa merupakan lingkungan bagi dalam , kita perlu menemukan bola terbuka di sekitar yang termuat dalam . Karena merupakan lingkungan bagi , menurut definisi terdapat sedemikian sehingga . Karena kontinu di , terdapat sedemikian sehingga . Jadi, jika , maka . Dengan demikian, , dan merupakan lingkungan bagi dalam .  Pembuktian implikasi sebaliknya diserahkan kepada aktivitas berikut.      Misalkan dan ruang-ruang metrik, dan misalkan suatu fungsi. Misalkan . Dalam aktivitas ini, kita membuktikan bahwa jika prapeta setiap lingkungan bagi merupakan lingkungan bagi , maka kontinu di .    Menurut , apa yang perlu kita lakukan untuk menunjukkan bahwa kontinu di ?    Misalkan lebih besar daripada 0. Mengapa merupakan lingkungan bagi dalam ?    Apa yang dinyatakan oleh hipotesis kita mengenai ?    Apa yang dapat kita simpulkan dari bagian (c)?    Bagaimana bagian (a)-(d) menunjukkan bahwa kontinu di ?    Kita mengakhiri bagian ini dengan beberapa fakta penting mengenai lingkungan. Asumsikan bahwa suatu ruang metrik dan .   Terdapat suatu lingkungan yang memuat .    Jika merupakan lingkungan bagi dan , maka merupakan lingkungan bagi .    Jika dan merupakan lingkungan bagi , maka juga demikian.     Pembuktiannya langsung dan diserahkan kepada .  "
},
{
  "id": "act_OB_1",
  "level": "2",
  "url": "sec_cont_neighborhoods.html#act_OB_1",
  "type": "Kegiatan",
  "number": "7.3",
  "title": "",
  "body": "  Misalkan suatu fungsi dari ruang metrik ke ruang metrik yang kontinu di . Dengan menggunakan notasi dari paragraf di atas, dalam aktivitas ini kita menentukan apakah harus sama dengan untuk suatu .  Definisikan dengan , dan gunakan metrik Euklides pada seluruh aktivitas. Asumsikan bahwa merupakan fungsi kontinu. Maka kontinu di .    Tentukan .    Tentukan .    Apakah merupakan bola terbuka yang berpusat di ? Jelaskan.   "
},
{
  "id": "p-783",
  "level": "2",
  "url": "sec_cont_neighborhoods.html#p-783",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "memuat "
},
{
  "id": "thm_open_ball_continuity",
  "level": "2",
  "url": "sec_cont_neighborhoods.html#thm_open_ball_continuity",
  "type": "Teorema",
  "number": "7.5",
  "title": "",
  "body": "  Misalkan suatu fungsi dari ruang metrik ke ruang metrik , dan misalkan . Maka kontinu di jika dan hanya jika, untuk setiap , terdapat sedemikian sehingga .   "
},
{
  "id": "theorem-13",
  "level": "2",
  "url": "sec_cont_neighborhoods.html#theorem-13",
  "type": "Teorema",
  "number": "7.6",
  "title": "",
  "body": "  Misalkan dan ruang-ruang metrik, dan misalkan suatu fungsi. Maka kontinu di jika dan hanya jika prapeta setiap lingkungan bagi merupakan lingkungan bagi .    Misalkan dan ruang-ruang metrik, dan misalkan suatu fungsi. Untuk membuktikan pernyataan bikondisional ini, kita harus membuktikan kedua implikasinya. Pertama, asumsikan bahwa kontinu di suatu titik . Kita akan menunjukkan bahwa untuk setiap lingkungan bagi dalam , prapetanya, yaitu dalam , merupakan lingkungan bagi dalam . Misalkan suatu lingkungan bagi dalam . Untuk menunjukkan bahwa merupakan lingkungan bagi dalam , kita perlu menemukan bola terbuka di sekitar yang termuat dalam . Karena merupakan lingkungan bagi , menurut definisi terdapat sedemikian sehingga . Karena kontinu di , terdapat sedemikian sehingga . Jadi, jika , maka . Dengan demikian, , dan merupakan lingkungan bagi dalam .  Pembuktian implikasi sebaliknya diserahkan kepada aktivitas berikut.   "
},
{
  "id": "activity-29",
  "level": "2",
  "url": "sec_cont_neighborhoods.html#activity-29",
  "type": "Kegiatan",
  "number": "7.4",
  "title": "",
  "body": "  Misalkan dan ruang-ruang metrik, dan misalkan suatu fungsi. Misalkan . Dalam aktivitas ini, kita membuktikan bahwa jika prapeta setiap lingkungan bagi merupakan lingkungan bagi , maka kontinu di .    Menurut , apa yang perlu kita lakukan untuk menunjukkan bahwa kontinu di ?    Misalkan lebih besar daripada 0. Mengapa merupakan lingkungan bagi dalam ?    Apa yang dinyatakan oleh hipotesis kita mengenai ?    Apa yang dapat kita simpulkan dari bagian (c)?    Bagaimana bagian (a)-(d) menunjukkan bahwa kontinu di ?   "
},
{
  "id": "sec_open_balls_summ",
  "level": "1",
  "url": "sec_open_balls_summ.html",
  "type": "Bagian",
  "number": "",
  "title": "Ringkasan",
  "body": " Ringkasan  Gagasan-gagasan penting yang kita bahas pada bagian ini meliputi hal-hal berikut.   Jika suatu ruang metrik dan , maka bola terbuka yang berpusat di adalah himpunan berbentuk untuk suatu bilangan positif .    Suatu subhimpunan dari ruang metrik merupakan lingkungan titik jika terdapat bilangan real positif sedemikian sehingga .    Salah satu sifat penting bola terbuka ialah bahwa setiap bola terbuka merupakan lingkungan bagi setiap titiknya. Inilah langkah pertama kita menuju definisi konsep himpunan terbuka yang akan menjadi landasan ruang topologis.    Suatu fungsi dari ruang metrik ke ruang metrik kontinu di jika merupakan lingkungan dalam untuk setiap lingkungan dari dalam .     "
},
{
  "id": "sec_open_balls_exer",
  "level": "1",
  "url": "sec_open_balls_exer.html",
  "type": "Latihan",
  "number": "",
  "title": "Latihan",
  "body": "  Tentukan, disertai bukti, manakah di antara himpunan-himpunan berikut yang merupakan lingkungan dari dalam ruang metrik yang diberikan.    dalam dengan     adalah sumbu dalam dengan , dengan sebagai metrik taksi    adalah himpunan bilangan rasional dalam dengan     adalah himpunan bilangan bulat positif dalam dan , dengan sebagai himpunan semua bilangan rasional dalam bentuk paling sederhana dan metrik yang didefinisikan oleh (Fakta bahwa merupakan metrik dibahas dalam .)    Misalkan dan definisikan dengan . Artinya, adalah sisa pembagian oleh . Fakta bahwa merupakan metrik pada dikaji dalam . Misalkan suatu ruang metrik. Mungkinkah kita mendefinisikan suatu fungsi yang tidak kontinu? Jelaskan.    Jika , tetapkan . Untuk dan , definisikan dengan Fakta bahwa merupakan metrik dikaji dalam . Misalkan dan . Definisikan dan dengan . Salah satu dari dan kontinu, sedangkan yang lain tidak. Tentukan yang mana, disertai bukti untuk masing-masing fungsi.    Ingat kembali dari bahwa kita dapat membangun ruang metrik berhingga dengan memulai dari suatu himpunan titik berhingga lalu membuat graf yang titik-titiknya menjadi simpul. Kita membuat sisi-sisi sedemikian sehingga graf tersebut terhubung (artinya, terdapat lintasan dari setiap simpul ke setiap simpul lainnya) dan memberikan bobot pada sisi-sisinya. Selanjutnya, kita mendefinisikan metrik pada dengan menetapkan sebagai panjang lintasan terpendek antara simpul dan pada graf tersebut. Perhatikan ruang metrik yang bersesuaian dengan graf dalam .   Graf untuk mendefinisikan suatu metrik.   Graf berbobot dengan simpul a, b, c, d, dan e. Sisi-sisinya adalah a–b berbobot 3, a–c berbobot 8, a–e berbobot 1, c–e berbobot 7, c–d berbobot 2, d–e berbobot 5, d–b berbobot 7, dan e–b berbobot 2.     Tentukan semua bola terbuka untuk setiap bilangan real positif .   Tentukan semua lingkungan dari .    Misalkan didefinisikan oleh untuk suatu bilangan real dan dengan . Misalkan dan . Tunjukkan bahwa memuat suatu bola terbuka yang berpusat di . Simpulkan bahwa setiap fungsi linear dari ke bersifat kontinu.   Berdasarkan , kita dapat mengasumsikan untuk menyederhanakan soal.   Misalkan didefinisikan oleh untuk suatu bilangan real , , dan dengan . Misalkan dan . Tunjukkan bahwa memuat suatu bola terbuka yang berpusat di . Simpulkan bahwa setiap fungsi kuadrat dari ke bersifat kontinu.   Pertimbangkan beberapa kasus.    Misalkan suatu ruang metrik, dan misalkan suatu subhimpunan tak kosong dari . memberi tahu kita bahwa untuk semua . Definisikan dengan . Misalkan . Diberikan , tunjukkan bahwa terdapat lingkungan dari sedemikian sehingga mengakibatkan . Simpulkan bahwa merupakan fungsi kontinu. (Asumsikan bahwa metrik pada adalah metrik Euklides.)    Misalkan dan merupakan dua titik berbeda dalam suatu ruang metrik . Buktikan bahwa terdapat lingkungan dan , masing-masing dari dan , sedemikian sehingga .    Misalkan suatu ruang metrik dan . Buktikan setiap pernyataan berikut.   Terdapat suatu lingkungan yang memuat .   Jika merupakan lingkungan dari dan , maka merupakan lingkungan dari .   Jika dan merupakan lingkungan dari , maka demikian pula halnya dengan .    Misalkan suatu fungsi kontinu. Tunjukkan bahwa jika untuk suatu , maka terdapat lingkungan dari sedemikian sehingga untuk semua .    Misalkan suatu ruang metrik dengan sebagai metrik diskret. Tunjukkan bahwa setiap subhimpunan dari merupakan lingkungan dari setiap titiknya.    Untuk setiap pernyataan berikut, jawablah benar jika pernyataan itu selalu benar. Jika pernyataan itu hanya kadang-kadang benar atau tidak pernah benar, jawablah salah dan berikan contoh konkret yang menunjukkan bahwa pernyataan tersebut salah. Jika suatu pernyataan benar, jelaskan alasannya.   Jika merupakan lingkungan dari suatu titik dalam ruang metrik , maka setiap bola terbuka yang termuat dalam juga merupakan lingkungan dari .   Jika merupakan lingkungan dari suatu titik dalam ruang metrik , maka merupakan lingkungan dari setiap titiknya.   Jika dan merupakan ruang metrik dan suatu fungsi kontinu, maka merupakan lingkungan dari dalam setiap kali merupakan lingkungan dari dalam .   Jika dan merupakan ruang metrik, kontinu di , dan merupakan lingkungan dari dalam , maka merupakan lingkungan dari dalam .   Jika suatu titik dalam ruang metrik dan suatu bilangan real positif, maka bola terbuka memuat tak berhingga banyak titik dari .   Jika , , , merupakan lingkungan dari suatu titik dalam ruang metrik untuk suatu bilangan bulat positif , maka merupakan lingkungan dari .   Jika merupakan lingkungan dari suatu titik dalam ruang metrik untuk setiap dalam suatu himpunan indeks , maka merupakan lingkungan dari .   "
},
{
  "id": "exercise-69",
  "level": "2",
  "url": "sec_open_balls_exer.html#exercise-69",
  "type": "Latihan",
  "number": "1",
  "title": "",
  "body": " Tentukan, disertai bukti, manakah di antara himpunan-himpunan berikut yang merupakan lingkungan dari dalam ruang metrik yang diberikan.    dalam dengan     adalah sumbu dalam dengan , dengan sebagai metrik taksi    adalah himpunan bilangan rasional dalam dengan     adalah himpunan bilangan bulat positif dalam dan , dengan sebagai himpunan semua bilangan rasional dalam bentuk paling sederhana dan metrik yang didefinisikan oleh (Fakta bahwa merupakan metrik dibahas dalam .)  "
},
{
  "id": "exercise-70",
  "level": "2",
  "url": "sec_open_balls_exer.html#exercise-70",
  "type": "Latihan",
  "number": "2",
  "title": "",
  "body": " Misalkan dan definisikan dengan . Artinya, adalah sisa pembagian oleh . Fakta bahwa merupakan metrik pada dikaji dalam . Misalkan suatu ruang metrik. Mungkinkah kita mendefinisikan suatu fungsi yang tidak kontinu? Jelaskan.  "
},
{
  "id": "exercise-71",
  "level": "2",
  "url": "sec_open_balls_exer.html#exercise-71",
  "type": "Latihan",
  "number": "3",
  "title": "",
  "body": " Jika , tetapkan . Untuk dan , definisikan dengan Fakta bahwa merupakan metrik dikaji dalam . Misalkan dan . Definisikan dan dengan . Salah satu dari dan kontinu, sedangkan yang lain tidak. Tentukan yang mana, disertai bukti untuk masing-masing fungsi.  "
},
{
  "id": "exercise-72",
  "level": "2",
  "url": "sec_open_balls_exer.html#exercise-72",
  "type": "Latihan",
  "number": "4",
  "title": "",
  "body": " Ingat kembali dari bahwa kita dapat membangun ruang metrik berhingga dengan memulai dari suatu himpunan titik berhingga lalu membuat graf yang titik-titiknya menjadi simpul. Kita membuat sisi-sisi sedemikian sehingga graf tersebut terhubung (artinya, terdapat lintasan dari setiap simpul ke setiap simpul lainnya) dan memberikan bobot pada sisi-sisinya. Selanjutnya, kita mendefinisikan metrik pada dengan menetapkan sebagai panjang lintasan terpendek antara simpul dan pada graf tersebut. Perhatikan ruang metrik yang bersesuaian dengan graf dalam .   Graf untuk mendefinisikan suatu metrik.   Graf berbobot dengan simpul a, b, c, d, dan e. Sisi-sisinya adalah a–b berbobot 3, a–c berbobot 8, a–e berbobot 1, c–e berbobot 7, c–d berbobot 2, d–e berbobot 5, d–b berbobot 7, dan e–b berbobot 2.     Tentukan semua bola terbuka untuk setiap bilangan real positif .   Tentukan semua lingkungan dari .  "
},
{
  "id": "ex_linear_continuous1",
  "level": "2",
  "url": "sec_open_balls_exer.html#ex_linear_continuous1",
  "type": "Latihan",
  "number": "5",
  "title": "",
  "body": " Misalkan didefinisikan oleh untuk suatu bilangan real dan dengan . Misalkan dan . Tunjukkan bahwa memuat suatu bola terbuka yang berpusat di . Simpulkan bahwa setiap fungsi linear dari ke bersifat kontinu.   Berdasarkan , kita dapat mengasumsikan untuk menyederhanakan soal.   Misalkan didefinisikan oleh untuk suatu bilangan real , , dan dengan . Misalkan dan . Tunjukkan bahwa memuat suatu bola terbuka yang berpusat di . Simpulkan bahwa setiap fungsi kuadrat dari ke bersifat kontinu.   Pertimbangkan beberapa kasus.  "
},
{
  "id": "ex_metric_continuous",
  "level": "2",
  "url": "sec_open_balls_exer.html#ex_metric_continuous",
  "type": "Latihan",
  "number": "6",
  "title": "",
  "body": " Misalkan suatu ruang metrik, dan misalkan suatu subhimpunan tak kosong dari . memberi tahu kita bahwa untuk semua . Definisikan dengan . Misalkan . Diberikan , tunjukkan bahwa terdapat lingkungan dari sedemikian sehingga mengakibatkan . Simpulkan bahwa merupakan fungsi kontinu. (Asumsikan bahwa metrik pada adalah metrik Euklides.)  "
},
{
  "id": "exercise-75",
  "level": "2",
  "url": "sec_open_balls_exer.html#exercise-75",
  "type": "Latihan",
  "number": "7",
  "title": "",
  "body": " Misalkan dan merupakan dua titik berbeda dalam suatu ruang metrik . Buktikan bahwa terdapat lingkungan dan , masing-masing dari dan , sedemikian sehingga .  "
},
{
  "id": "ex_Nghb_properties",
  "level": "2",
  "url": "sec_open_balls_exer.html#ex_Nghb_properties",
  "type": "Latihan",
  "number": "8",
  "title": "",
  "body": " Misalkan suatu ruang metrik dan . Buktikan setiap pernyataan berikut.   Terdapat suatu lingkungan yang memuat .   Jika merupakan lingkungan dari dan , maka merupakan lingkungan dari .   Jika dan merupakan lingkungan dari , maka demikian pula halnya dengan .  "
},
{
  "id": "exercise-77",
  "level": "2",
  "url": "sec_open_balls_exer.html#exercise-77",
  "type": "Latihan",
  "number": "9",
  "title": "",
  "body": " Misalkan suatu fungsi kontinu. Tunjukkan bahwa jika untuk suatu , maka terdapat lingkungan dari sedemikian sehingga untuk semua .  "
},
{
  "id": "exercise-78",
  "level": "2",
  "url": "sec_open_balls_exer.html#exercise-78",
  "type": "Latihan",
  "number": "10",
  "title": "",
  "body": " Misalkan suatu ruang metrik dengan sebagai metrik diskret. Tunjukkan bahwa setiap subhimpunan dari merupakan lingkungan dari setiap titiknya.  "
},
{
  "id": "exercise-79",
  "level": "2",
  "url": "sec_open_balls_exer.html#exercise-79",
  "type": "Latihan",
  "number": "11",
  "title": "",
  "body": " Untuk setiap pernyataan berikut, jawablah benar jika pernyataan itu selalu benar. Jika pernyataan itu hanya kadang-kadang benar atau tidak pernah benar, jawablah salah dan berikan contoh konkret yang menunjukkan bahwa pernyataan tersebut salah. Jika suatu pernyataan benar, jelaskan alasannya.   Jika merupakan lingkungan dari suatu titik dalam ruang metrik , maka setiap bola terbuka yang termuat dalam juga merupakan lingkungan dari .   Jika merupakan lingkungan dari suatu titik dalam ruang metrik , maka merupakan lingkungan dari setiap titiknya.   Jika dan merupakan ruang metrik dan suatu fungsi kontinu, maka merupakan lingkungan dari dalam setiap kali merupakan lingkungan dari dalam .   Jika dan merupakan ruang metrik, kontinu di , dan merupakan lingkungan dari dalam , maka merupakan lingkungan dari dalam .   Jika suatu titik dalam ruang metrik dan suatu bilangan real positif, maka bola terbuka memuat tak berhingga banyak titik dari .   Jika , , , merupakan lingkungan dari suatu titik dalam ruang metrik untuk suatu bilangan bulat positif , maka merupakan lingkungan dari .   Jika merupakan lingkungan dari suatu titik dalam ruang metrik untuk setiap dalam suatu himpunan indeks , maka merupakan lingkungan dari .  "
},
{
  "id": "o003-c90-ch01-activity-checkpoints",
  "level": "1",
  "url": "o003-c90-ch01-activity-checkpoints.html",
  "type": "Bagian",
  "number": "",
  "title": "Pemeriksaan aktivitas",
  "body": " Pemeriksaan aktivitas  Pemeriksaan 1: himpunan, paradoks, dan subhimpunan  Setelah mengerjakan aktivitas berjangkar pa_sets , periksa apakah alasan Anda menjelaskan kontradiksi pada , lalu merumuskan dan kedudukan dengan kuantor yang tepat.   Petunjuk 1. Ganti dengan dalam syarat pembentuk .  Petunjuk 2. Untuk subhimpunan, mulailah dengan ; untuk himpunan kosong, tanyakan apakah ada contoh yang melanggar implikasi.   Definisi naif menghasilkan . Definisi yang dapat dipakai pada bab ini adalah bila setiap anggota merupakan anggota . Karena implikasi tersebut benar secara vakum untuk , berlaku untuk setiap , dan selalu .   Jika , syarat pembentuknya mengatakan . Jika , syarat yang sama justru menempatkan di dalam . Jadi pemahaman setiap koleksi yang dapat dideskripsikan adalah himpunan tidak aman; inilah paradoks Russell. Untuk bagian subhimpunan, rumusan yang dapat diuji adalah . Rumusan ini langsung memberi refleksivitas dan fakta bahwa himpunan kosong adalah subhimpunan setiap himpunan.   Pemeriksaan 2: deformasi tanpa memotong atau menempel  Bandingkan jawaban Anda pada aktivitas act_rubber_sheet dengan invarian sederhana: apakah objek tetap berupa lengkung tertutup, dan berapa banyak terowongan tembus yang dimilikinya?   Petunjuk 1. Sebuah simpul karet tertutup tidak dapat berubah menjadi lengkung dengan dua ujung tanpa diputus.  Petunjuk 2. Pada benda tiga dimensi, bedakan lekukan biasa dari lubang yang menembus seluruh benda.   Dengan model standar berupa lengkung sederhana tertutup di bidang, persegi dapat dideformasi menjadi lingkaran, garis tepi huruf D , dan bintang berujung lima yang tidak berpotongan sendiri, tetapi bukan huruf S sebagai lengkung terbuka. Dengan model benda padat, persegi padat dan mangkuk tanpa lubang tembus berada dalam kelas tanpa terowongan; donat dan cangkir bergagang masing-masing mempunyai satu terowongan.   Jawaban bergantung pada pemodelan gambar. Pernyataan di atas memakai dua asumsi: S adalah goresan terbuka, sedangkan bintang adalah garis tepi sederhana; mangkuk adalah gumpalan padat dengan cekungan, bukan permukaan tipis. Deformasi kontinu tidak membuat atau menghilangkan ujung maupun terowongan. Karena itu dua kelompok tersebut dapat dibedakan tanpa memakai ukuran atau sudut. Bila guru bermaksud model lain, nyatakan model itu sebelum memberi klasifikasi.   Pemeriksaan 3: kesamaan himpunan  Periksa empat keputusan pada aktivitas act_set_equality dengan uji dua inklusi.   Petunjuk 1. Sederhanakan dan tulis syarat keterbagian sebagai kongruensi modulo .  Petunjuk 2. Bilangan genap mempunyai residu atau modulo ; bilangan ganjil mempunyai residu atau .   Kesamaan berarti dan . Pada contoh riil, kedua himpunan sama-sama . Pada contoh genap, himpunan adalah bilangan yang kongruen modulo , sehingga ; misalnya . Pada contoh ganjil, residu atau modulo tepat mencakup semua bilangan ganjil, jadi .   Bukti yang dapat diperiksa selalu dimulai dengan anggota sembarang. Untuk contoh terakhir, jika ganjil maka algoritma pembagian memberi atau ; arah sebaliknya segera memberi atau . Jadi kedua inklusi terbukti. Satu contoh cukup menggugurkan arah pada contoh genap.   Pemeriksaan 4: operasi himpunan dan hukum De Morgan  Untuk aktivitas act_sets_1 , hitung semua himpunan yang diminta dan cocokkan dua pasangan komplemen dengan hukum De Morgan.   Petunjuk 1. Buat tabel keanggotaan untuk setiap unsur sampai .  Petunjuk 2. Negasi kata atau menjadi dan tidak , sedangkan negasi kata dan menjadi atau tidak .    dan . Relatif terhadap , , sedangkan .   Di sini dan . Mengambil irisan dan gabungannya menghasilkan dua himpunan pada jawaban. Untuk bukti umum, misalnya, ekuivalen dengan dan , yang ekuivalen dengan . Argumen serupa membuktikan hukum kedua.   Pemeriksaan 5: keluarga terindeks  Periksa contoh hingga dan tak hingga pada aktivitas keluarga terindeks tanpa ID sumber, lalu tulis definisi gabungan dan irisan dengan kuantor.   Petunjuk 1. Untuk , indeks menentukan irisan.  Petunjuk 2. Untuk gabungan, setelah memilih , pilih indeks dengan .   Pada keluarga hingga, , , dan terdapat sepuluh himpunan. Pada keluarga berindeks riil, , , serta . Selanjutnya dan .   Definisi umumnya adalah bila dan hanya bila , sedangkan bila dan hanya bila . Karena , irisannya kosong. Setiap anggota setiap tidak negatif; sebaliknya, untuk pilih , sehingga . Ini membuktikan hasil gabungan.   Pemeriksaan 6: hukum De Morgan untuk keluarga tak hingga  Untuk aktivitas tanpa ID sesudah teorema De Morgan, verifikasi kedua hukum pada , , dengan semesta .   Petunjuk 1. Tentukan dahulu dan .  Petunjuk 2. Keluarga membesar, sehingga keluarga komplemennya mengecil.    dan . Maka , serta .   Setiap bilangan bulat positif muncul dalam setelah cukup besar, sementara hanya yang terdapat dalam semua . Selain itu, karena komplemennya mengecil. Secara logika, tidak berada di sedikitnya satu gabungan berarti tidak berada di setiap komponennya ; perubahan kuantor inilah yang menukar gabungan dengan irisan.   Pemeriksaan 7: produk Kartesius  Periksa daftar pasangan dan argumen pencacahan pada aktivitas produk Kartesius tanpa ID sumber.   Petunjuk 1. Koordinat pertama mempunyai dua pilihan dan koordinat kedua tiga pilihan.  Petunjuk 2. Untuk tiap satu dari pilihan pertama, ada pilihan kedua.   Hasilnya ialah . Jika dan , maka .   Kelompokkan pasangan menurut koordinat pertamanya. Ada kelompok yang saling lepas, dan masing-masing berisi tepat pasangan. Karena urutan koordinat bermakna, tidak boleh diam-diam diperlakukan sama dengan .   "
},
{
  "id": "o003-c90-ch01-checkpoint-pa-sets",
  "level": "2",
  "url": "o003-c90-ch01-activity-checkpoints.html#o003-c90-ch01-checkpoint-pa-sets",
  "type": "Pemeriksaan",
  "number": "A.1",
  "title": "Pemeriksaan 1: himpunan, paradoks, dan subhimpunan.",
  "body": "Pemeriksaan 1: himpunan, paradoks, dan subhimpunan  Setelah mengerjakan aktivitas berjangkar pa_sets , periksa apakah alasan Anda menjelaskan kontradiksi pada , lalu merumuskan dan kedudukan dengan kuantor yang tepat.   Petunjuk 1. Ganti dengan dalam syarat pembentuk .  Petunjuk 2. Untuk subhimpunan, mulailah dengan ; untuk himpunan kosong, tanyakan apakah ada contoh yang melanggar implikasi.   Definisi naif menghasilkan . Definisi yang dapat dipakai pada bab ini adalah bila setiap anggota merupakan anggota . Karena implikasi tersebut benar secara vakum untuk , berlaku untuk setiap , dan selalu .   Jika , syarat pembentuknya mengatakan . Jika , syarat yang sama justru menempatkan di dalam . Jadi pemahaman setiap koleksi yang dapat dideskripsikan adalah himpunan tidak aman; inilah paradoks Russell. Untuk bagian subhimpunan, rumusan yang dapat diuji adalah . Rumusan ini langsung memberi refleksivitas dan fakta bahwa himpunan kosong adalah subhimpunan setiap himpunan.  "
},
{
  "id": "o003-c90-ch01-checkpoint-rubber-sheet",
  "level": "2",
  "url": "o003-c90-ch01-activity-checkpoints.html#o003-c90-ch01-checkpoint-rubber-sheet",
  "type": "Pemeriksaan",
  "number": "A.2",
  "title": "Pemeriksaan 2: deformasi tanpa memotong atau menempel.",
  "body": "Pemeriksaan 2: deformasi tanpa memotong atau menempel  Bandingkan jawaban Anda pada aktivitas act_rubber_sheet dengan invarian sederhana: apakah objek tetap berupa lengkung tertutup, dan berapa banyak terowongan tembus yang dimilikinya?   Petunjuk 1. Sebuah simpul karet tertutup tidak dapat berubah menjadi lengkung dengan dua ujung tanpa diputus.  Petunjuk 2. Pada benda tiga dimensi, bedakan lekukan biasa dari lubang yang menembus seluruh benda.   Dengan model standar berupa lengkung sederhana tertutup di bidang, persegi dapat dideformasi menjadi lingkaran, garis tepi huruf D , dan bintang berujung lima yang tidak berpotongan sendiri, tetapi bukan huruf S sebagai lengkung terbuka. Dengan model benda padat, persegi padat dan mangkuk tanpa lubang tembus berada dalam kelas tanpa terowongan; donat dan cangkir bergagang masing-masing mempunyai satu terowongan.   Jawaban bergantung pada pemodelan gambar. Pernyataan di atas memakai dua asumsi: S adalah goresan terbuka, sedangkan bintang adalah garis tepi sederhana; mangkuk adalah gumpalan padat dengan cekungan, bukan permukaan tipis. Deformasi kontinu tidak membuat atau menghilangkan ujung maupun terowongan. Karena itu dua kelompok tersebut dapat dibedakan tanpa memakai ukuran atau sudut. Bila guru bermaksud model lain, nyatakan model itu sebelum memberi klasifikasi.  "
},
{
  "id": "o003-c90-ch01-checkpoint-set-equality",
  "level": "2",
  "url": "o003-c90-ch01-activity-checkpoints.html#o003-c90-ch01-checkpoint-set-equality",
  "type": "Pemeriksaan",
  "number": "A.3",
  "title": "Pemeriksaan 3: kesamaan himpunan.",
  "body": "Pemeriksaan 3: kesamaan himpunan  Periksa empat keputusan pada aktivitas act_set_equality dengan uji dua inklusi.   Petunjuk 1. Sederhanakan dan tulis syarat keterbagian sebagai kongruensi modulo .  Petunjuk 2. Bilangan genap mempunyai residu atau modulo ; bilangan ganjil mempunyai residu atau .   Kesamaan berarti dan . Pada contoh riil, kedua himpunan sama-sama . Pada contoh genap, himpunan adalah bilangan yang kongruen modulo , sehingga ; misalnya . Pada contoh ganjil, residu atau modulo tepat mencakup semua bilangan ganjil, jadi .   Bukti yang dapat diperiksa selalu dimulai dengan anggota sembarang. Untuk contoh terakhir, jika ganjil maka algoritma pembagian memberi atau ; arah sebaliknya segera memberi atau . Jadi kedua inklusi terbukti. Satu contoh cukup menggugurkan arah pada contoh genap.  "
},
{
  "id": "o003-c90-ch01-checkpoint-set-operations",
  "level": "2",
  "url": "o003-c90-ch01-activity-checkpoints.html#o003-c90-ch01-checkpoint-set-operations",
  "type": "Pemeriksaan",
  "number": "A.4",
  "title": "Pemeriksaan 4: operasi himpunan dan hukum De Morgan.",
  "body": "Pemeriksaan 4: operasi himpunan dan hukum De Morgan  Untuk aktivitas act_sets_1 , hitung semua himpunan yang diminta dan cocokkan dua pasangan komplemen dengan hukum De Morgan.   Petunjuk 1. Buat tabel keanggotaan untuk setiap unsur sampai .  Petunjuk 2. Negasi kata atau menjadi dan tidak , sedangkan negasi kata dan menjadi atau tidak .    dan . Relatif terhadap , , sedangkan .   Di sini dan . Mengambil irisan dan gabungannya menghasilkan dua himpunan pada jawaban. Untuk bukti umum, misalnya, ekuivalen dengan dan , yang ekuivalen dengan . Argumen serupa membuktikan hukum kedua.  "
},
{
  "id": "o003-c90-ch01-checkpoint-indexed-family",
  "level": "2",
  "url": "o003-c90-ch01-activity-checkpoints.html#o003-c90-ch01-checkpoint-indexed-family",
  "type": "Pemeriksaan",
  "number": "A.5",
  "title": "Pemeriksaan 5: keluarga terindeks.",
  "body": "Pemeriksaan 5: keluarga terindeks  Periksa contoh hingga dan tak hingga pada aktivitas keluarga terindeks tanpa ID sumber, lalu tulis definisi gabungan dan irisan dengan kuantor.   Petunjuk 1. Untuk , indeks menentukan irisan.  Petunjuk 2. Untuk gabungan, setelah memilih , pilih indeks dengan .   Pada keluarga hingga, , , dan terdapat sepuluh himpunan. Pada keluarga berindeks riil, , , serta . Selanjutnya dan .   Definisi umumnya adalah bila dan hanya bila , sedangkan bila dan hanya bila . Karena , irisannya kosong. Setiap anggota setiap tidak negatif; sebaliknya, untuk pilih , sehingga . Ini membuktikan hasil gabungan.  "
},
{
  "id": "o003-c90-ch01-checkpoint-demorgan",
  "level": "2",
  "url": "o003-c90-ch01-activity-checkpoints.html#o003-c90-ch01-checkpoint-demorgan",
  "type": "Pemeriksaan",
  "number": "A.6",
  "title": "Pemeriksaan 6: hukum De Morgan untuk keluarga tak hingga.",
  "body": "Pemeriksaan 6: hukum De Morgan untuk keluarga tak hingga  Untuk aktivitas tanpa ID sesudah teorema De Morgan, verifikasi kedua hukum pada , , dengan semesta .   Petunjuk 1. Tentukan dahulu dan .  Petunjuk 2. Keluarga membesar, sehingga keluarga komplemennya mengecil.    dan . Maka , serta .   Setiap bilangan bulat positif muncul dalam setelah cukup besar, sementara hanya yang terdapat dalam semua . Selain itu, karena komplemennya mengecil. Secara logika, tidak berada di sedikitnya satu gabungan berarti tidak berada di setiap komponennya ; perubahan kuantor inilah yang menukar gabungan dengan irisan.  "
},
{
  "id": "o003-c90-ch01-checkpoint-cartesian-product",
  "level": "2",
  "url": "o003-c90-ch01-activity-checkpoints.html#o003-c90-ch01-checkpoint-cartesian-product",
  "type": "Pemeriksaan",
  "number": "A.7",
  "title": "Pemeriksaan 7: produk Kartesius.",
  "body": "Pemeriksaan 7: produk Kartesius  Periksa daftar pasangan dan argumen pencacahan pada aktivitas produk Kartesius tanpa ID sumber.   Petunjuk 1. Koordinat pertama mempunyai dua pilihan dan koordinat kedua tiga pilihan.  Petunjuk 2. Untuk tiap satu dari pilihan pertama, ada pilihan kedua.   Hasilnya ialah . Jika dan , maka .   Kelompokkan pasangan menurut koordinat pertamanya. Ada kelompok yang saling lepas, dan masing-masing berisi tepat pasangan. Karena urutan koordinat bermakna, tidak boleh diam-diam diperlakukan sama dengan .  "
},
{
  "id": "o003-c90-ch01-exercise-guides",
  "level": "1",
  "url": "o003-c90-ch01-exercise-guides.html",
  "type": "Bagian",
  "number": "",
  "title": "Jawaban dan panduan sepuluh latihan",
  "body": " Jawaban dan panduan sepuluh latihan  Latihan 1: menerjemahkan kalimat menjadi notasi Bandingkan keenam ekspresi Anda dengan syarat keanggotaan pada latihan pertama.  Petunjuk 1. Terjemahkan setidaknya dua dan paling banyak satu dengan menghitung banyaknya himpunan yang memuat sebuah unsur.  Petunjuk 2. Gunakan komplemen relatif terhadap ; gabungkan tiga kemungkinan pasangan.   Berturut-turut: ; ; ; ; ; dan .   Pada butir ketiga, berada di tetapi tidak sekaligus di dan berarti meniadakan , bukan meniadakan kedua himpunan secara terpisah. Pada butir kelima, gagal berada di sedikitnya dua himpunan berarti sedikitnya satu dari tiga pasangan komplemen berlaku. Pada butir keenam, gagal berada di paling banyak satu himpunan berarti berada di sedikitnya dua himpunan. Uji tabel delapan pola keanggotaan memberi pemeriksaan langsung.   Latihan 2: komplemen pada semesta bersarang Untuk , periksa kedua klaim dengan argumen unsur.  Petunjuk 1. Tulis dan .  Petunjuk 2. Pisahkan anggota menurut apakah ia berada di .   Keduanya benar: dan . Jika simbol pada sumber dimaksudkan ketat dan kedua inklusi awal ketat, inklusi pertama juga ketat karena tidak kosong.   Jika , maka dan , jadi . Untuk identitas kedua, anggota ruas kiri berada di tetapi tidak di . Jika ia tidak di , ia berada di ; jika ia di , kegagalan berada di memaksanya berada di . Arah sebaliknya diperiksa langsung dari dua kasus itu.   Latihan 3: hukum asosiatif dan distributif Buktikan semua empat identitas yang tercantum pada latihan berjangkar ex_set_props .  Petunjuk 1. Ambil unsur sembarang dan terjemahkan irisan sebagai dan , gabungan sebagai atau .  Petunjuk 2. Gunakan asosiativitas serta distributivitas logika proposisional, lalu terjemahkan kembali.   Keempat identitas benar: , , , dan .   Sebagai pola, ekuivalen dengan dan ( atau ). Distribusikan kata dan untuk memperoleh ( ) atau ( ), tepat syarat ruas kanan. Tiga identitas lain dibuktikan dengan rantai ekuivalensi yang sama. Sumber menempatkan dua hukum distributif dalam satu task melalui token \\item ; keduanya tetap harus dibuktikan.   Latihan 4: hukum De Morgan untuk keluarga terindeks Lengkapi dua bukti pada latihan berjangkar ex_DeMorgan .  Petunjuk 1. Mulai dari keanggotaan sebuah unsur pada komplemen ruas kiri.  Petunjuk 2. Gunakan negasi kuantor: menjadi , dan menjadi .    dan .   Untuk hukum pertama, jika dan hanya jika tidak ada dengan ; ini jika dan hanya jika untuk setiap , ; dan ini jika dan hanya jika . Untuk hukum kedua, jika dan hanya jika ada dengan ; ini jika dan hanya jika . Dengan konvensi gabungan kosong dan irisan kosong , bukti juga mencakup .   Latihan 5: produk dengan himpunan kosong Tentukan dan jelaskan dari definisi pasangan berurutan.  Petunjuk 1. Anda memerlukan koordinat pertama yang merupakan anggota .  Petunjuk 2. Apakah pasangan seperti itu dapat ada?  .  Andaikan . Definisi produk mengharuskan , yang mustahil. Jadi produk itu tidak mempunyai anggota.   Latihan 6: himpunan kuasa Periksa daftar, pencacahan, dan bukti umum pada latihan berjangkar ex_power_set .  Petunjuk 1. Untuk setiap unsur, ada dua pilihan independen: dimasukkan atau tidak dimasukkan ke subhimpunan.  Petunjuk 2. Untuk bukti induksi, tambahkan satu unsur baru dan pasangkan subhimpunan yang memuatnya dengan yang tidak.    . Himpunan beranggota tiga mempunyai subhimpunan; secara umum, jika , maka .   Kodekan setiap subhimpunan dengan deret biner sepanjang : digit ke- bernilai bila unsur ke- dipilih. Korespondensi ini bijektif dengan semua deret biner. Secara induktif, menambahkan satu unsur menggandakan jumlah subhimpunan, sebab setiap subhimpunan lama menghasilkan satu versi tanpa dan satu versi dengan unsur baru.   Latihan 7: membedakan keanggotaan dan inklusi Nilai keenam pernyataan tentang dan berikan koreksi bila perlu.  Petunjuk 1.  tepat ketika .  Petunjuk 2. Uji klaim inklusi ketat pada kasus tepi .   (a) benar; (b) tidak benar secara umum; (c) inklusi tak-ketat selalu benar, tetapi inklusi ketat gagal saat ; (d) benar; (e) benar sebagai inklusi ketat karena tidak pernah kosong; (f) benar.   (a) Karena , maka . (b) Anggota tidak harus berupa subhimpunan ; misalnya . Koreksi universalnya adalah . (c) Selalu ; inklusi itu ketat bila , tetapi sama saat . (d) Karena , berlaku . (e) Himpunan kosong merupakan subhimpunan ketat dari sebab memuat sedikitnya . (f) Jika , maka , sehingga .   Latihan 8: subhimpunan produk yang bukan persegi panjang Bangun yang tidak berbentuk .  Petunjuk 1. Pilih dan .  Petunjuk 2. Ambil dua sudut diagonal; sebuah produk yang memuat keduanya harus memuat dua sudut silang.   adalah contoh yang diminta.   Andaikan . Karena dua pasangan diagonal berada di , kita harus mempunyai dan . Maka dan juga harus berada di , bertentangan dengan definisi . Karena dan masing-masing mempunyai sedikitnya dua anggota, pilihan tersebut selalu tersedia.   Latihan 9: gabungan dan irisan interval terindeks Buktikan keempat identitas untuk dan , .  Petunjuk 1. Untuk menyingkirkan dari irisan, pilih .  Petunjuk 2. Untuk memasukkan ke gabungan, pilih ; periksa secara terpisah.    , , , dan .   Tidak ada dalam semua : jika , ia tidak berada dalam interval mana pun; jika , pilih . Sebaliknya, setiap berada dalam , sehingga gabungannya tepat . Untuk interval tertutup, berada dalam semuanya. Argumen menyingkirkan setiap dari irisan dan bilangan negatif tidak pernah masuk; jadi irisannya . Setiap berada dalam , yang membuktikan hasil gabungan.   Latihan 10: benar, salah, bukti, dan contoh tandingan Periksa sepuluh keputusan Anda dan pastikan setiap klaim salah mempunyai contoh tandingan konkret.  Petunjuk 1. Inklusi berbalik saat mengambil komplemen.  Petunjuk 2. Untuk identitas selisih, ubah menjadi ; bedakan dari .   Urutannya adalah: benar, benar, salah, benar, salah, salah, benar, benar, salah, benar.   (a) Anggota berada di dan , jadi di irisannya. (b) Anggota berasal dari salah satu subhimpunan . (c) Salah: ambil , , dan ; arah yang benar adalah . (d) Benar oleh pembalikan komplemen. (e) Salah: , ; ruas kiri . Identitas yang benar ialah . (f) Salah: , ; ruas kiri , bukan . Identitas umumnya . (g) Benar, karena kedua ruas berarti dan . (h) Benar relatif terhadap . (i) Salah: mempunyai tepat satu anggota, yaitu . (j) Benar: dan adalah dua objek berbeda.   "
},
{
  "id": "o003-c90-ch01-exercise-01",
  "level": "2",
  "url": "o003-c90-ch01-exercise-guides.html#o003-c90-ch01-exercise-01",
  "type": "Pemeriksaan",
  "number": "A.8",
  "title": "Latihan 1: menerjemahkan kalimat menjadi notasi.",
  "body": "Latihan 1: menerjemahkan kalimat menjadi notasi Bandingkan keenam ekspresi Anda dengan syarat keanggotaan pada latihan pertama.  Petunjuk 1. Terjemahkan setidaknya dua dan paling banyak satu dengan menghitung banyaknya himpunan yang memuat sebuah unsur.  Petunjuk 2. Gunakan komplemen relatif terhadap ; gabungkan tiga kemungkinan pasangan.   Berturut-turut: ; ; ; ; ; dan .   Pada butir ketiga, berada di tetapi tidak sekaligus di dan berarti meniadakan , bukan meniadakan kedua himpunan secara terpisah. Pada butir kelima, gagal berada di sedikitnya dua himpunan berarti sedikitnya satu dari tiga pasangan komplemen berlaku. Pada butir keenam, gagal berada di paling banyak satu himpunan berarti berada di sedikitnya dua himpunan. Uji tabel delapan pola keanggotaan memberi pemeriksaan langsung.  "
},
{
  "id": "o003-c90-ch01-exercise-02",
  "level": "2",
  "url": "o003-c90-ch01-exercise-guides.html#o003-c90-ch01-exercise-02",
  "type": "Pemeriksaan",
  "number": "A.9",
  "title": "Latihan 2: komplemen pada semesta bersarang.",
  "body": "Latihan 2: komplemen pada semesta bersarang Untuk , periksa kedua klaim dengan argumen unsur.  Petunjuk 1. Tulis dan .  Petunjuk 2. Pisahkan anggota menurut apakah ia berada di .   Keduanya benar: dan . Jika simbol pada sumber dimaksudkan ketat dan kedua inklusi awal ketat, inklusi pertama juga ketat karena tidak kosong.   Jika , maka dan , jadi . Untuk identitas kedua, anggota ruas kiri berada di tetapi tidak di . Jika ia tidak di , ia berada di ; jika ia di , kegagalan berada di memaksanya berada di . Arah sebaliknya diperiksa langsung dari dua kasus itu.  "
},
{
  "id": "o003-c90-ch01-exercise-03",
  "level": "2",
  "url": "o003-c90-ch01-exercise-guides.html#o003-c90-ch01-exercise-03",
  "type": "Pemeriksaan",
  "number": "A.10",
  "title": "Latihan 3: hukum asosiatif dan distributif.",
  "body": "Latihan 3: hukum asosiatif dan distributif Buktikan semua empat identitas yang tercantum pada latihan berjangkar ex_set_props .  Petunjuk 1. Ambil unsur sembarang dan terjemahkan irisan sebagai dan , gabungan sebagai atau .  Petunjuk 2. Gunakan asosiativitas serta distributivitas logika proposisional, lalu terjemahkan kembali.   Keempat identitas benar: , , , dan .   Sebagai pola, ekuivalen dengan dan ( atau ). Distribusikan kata dan untuk memperoleh ( ) atau ( ), tepat syarat ruas kanan. Tiga identitas lain dibuktikan dengan rantai ekuivalensi yang sama. Sumber menempatkan dua hukum distributif dalam satu task melalui token \\item ; keduanya tetap harus dibuktikan.  "
},
{
  "id": "o003-c90-ch01-exercise-04",
  "level": "2",
  "url": "o003-c90-ch01-exercise-guides.html#o003-c90-ch01-exercise-04",
  "type": "Pemeriksaan",
  "number": "A.11",
  "title": "Latihan 4: hukum De Morgan untuk keluarga terindeks.",
  "body": "Latihan 4: hukum De Morgan untuk keluarga terindeks Lengkapi dua bukti pada latihan berjangkar ex_DeMorgan .  Petunjuk 1. Mulai dari keanggotaan sebuah unsur pada komplemen ruas kiri.  Petunjuk 2. Gunakan negasi kuantor: menjadi , dan menjadi .    dan .   Untuk hukum pertama, jika dan hanya jika tidak ada dengan ; ini jika dan hanya jika untuk setiap , ; dan ini jika dan hanya jika . Untuk hukum kedua, jika dan hanya jika ada dengan ; ini jika dan hanya jika . Dengan konvensi gabungan kosong dan irisan kosong , bukti juga mencakup .  "
},
{
  "id": "o003-c90-ch01-exercise-05",
  "level": "2",
  "url": "o003-c90-ch01-exercise-guides.html#o003-c90-ch01-exercise-05",
  "type": "Pemeriksaan",
  "number": "A.12",
  "title": "Latihan 5: produk dengan himpunan kosong.",
  "body": "Latihan 5: produk dengan himpunan kosong Tentukan dan jelaskan dari definisi pasangan berurutan.  Petunjuk 1. Anda memerlukan koordinat pertama yang merupakan anggota .  Petunjuk 2. Apakah pasangan seperti itu dapat ada?  .  Andaikan . Definisi produk mengharuskan , yang mustahil. Jadi produk itu tidak mempunyai anggota.  "
},
{
  "id": "o003-c90-ch01-exercise-06",
  "level": "2",
  "url": "o003-c90-ch01-exercise-guides.html#o003-c90-ch01-exercise-06",
  "type": "Pemeriksaan",
  "number": "A.13",
  "title": "Latihan 6: himpunan kuasa.",
  "body": "Latihan 6: himpunan kuasa Periksa daftar, pencacahan, dan bukti umum pada latihan berjangkar ex_power_set .  Petunjuk 1. Untuk setiap unsur, ada dua pilihan independen: dimasukkan atau tidak dimasukkan ke subhimpunan.  Petunjuk 2. Untuk bukti induksi, tambahkan satu unsur baru dan pasangkan subhimpunan yang memuatnya dengan yang tidak.    . Himpunan beranggota tiga mempunyai subhimpunan; secara umum, jika , maka .   Kodekan setiap subhimpunan dengan deret biner sepanjang : digit ke- bernilai bila unsur ke- dipilih. Korespondensi ini bijektif dengan semua deret biner. Secara induktif, menambahkan satu unsur menggandakan jumlah subhimpunan, sebab setiap subhimpunan lama menghasilkan satu versi tanpa dan satu versi dengan unsur baru.  "
},
{
  "id": "o003-c90-ch01-exercise-07",
  "level": "2",
  "url": "o003-c90-ch01-exercise-guides.html#o003-c90-ch01-exercise-07",
  "type": "Pemeriksaan",
  "number": "A.14",
  "title": "Latihan 7: membedakan keanggotaan dan inklusi.",
  "body": "Latihan 7: membedakan keanggotaan dan inklusi Nilai keenam pernyataan tentang dan berikan koreksi bila perlu.  Petunjuk 1.  tepat ketika .  Petunjuk 2. Uji klaim inklusi ketat pada kasus tepi .   (a) benar; (b) tidak benar secara umum; (c) inklusi tak-ketat selalu benar, tetapi inklusi ketat gagal saat ; (d) benar; (e) benar sebagai inklusi ketat karena tidak pernah kosong; (f) benar.   (a) Karena , maka . (b) Anggota tidak harus berupa subhimpunan ; misalnya . Koreksi universalnya adalah . (c) Selalu ; inklusi itu ketat bila , tetapi sama saat . (d) Karena , berlaku . (e) Himpunan kosong merupakan subhimpunan ketat dari sebab memuat sedikitnya . (f) Jika , maka , sehingga .  "
},
{
  "id": "o003-c90-ch01-exercise-08",
  "level": "2",
  "url": "o003-c90-ch01-exercise-guides.html#o003-c90-ch01-exercise-08",
  "type": "Pemeriksaan",
  "number": "A.15",
  "title": "Latihan 8: subhimpunan produk yang bukan persegi panjang.",
  "body": "Latihan 8: subhimpunan produk yang bukan persegi panjang Bangun yang tidak berbentuk .  Petunjuk 1. Pilih dan .  Petunjuk 2. Ambil dua sudut diagonal; sebuah produk yang memuat keduanya harus memuat dua sudut silang.   adalah contoh yang diminta.   Andaikan . Karena dua pasangan diagonal berada di , kita harus mempunyai dan . Maka dan juga harus berada di , bertentangan dengan definisi . Karena dan masing-masing mempunyai sedikitnya dua anggota, pilihan tersebut selalu tersedia.  "
},
{
  "id": "o003-c90-ch01-exercise-09",
  "level": "2",
  "url": "o003-c90-ch01-exercise-guides.html#o003-c90-ch01-exercise-09",
  "type": "Pemeriksaan",
  "number": "A.16",
  "title": "Latihan 9: gabungan dan irisan interval terindeks.",
  "body": "Latihan 9: gabungan dan irisan interval terindeks Buktikan keempat identitas untuk dan , .  Petunjuk 1. Untuk menyingkirkan dari irisan, pilih .  Petunjuk 2. Untuk memasukkan ke gabungan, pilih ; periksa secara terpisah.    , , , dan .   Tidak ada dalam semua : jika , ia tidak berada dalam interval mana pun; jika , pilih . Sebaliknya, setiap berada dalam , sehingga gabungannya tepat . Untuk interval tertutup, berada dalam semuanya. Argumen menyingkirkan setiap dari irisan dan bilangan negatif tidak pernah masuk; jadi irisannya . Setiap berada dalam , yang membuktikan hasil gabungan.  "
},
{
  "id": "o003-c90-ch01-exercise-10",
  "level": "2",
  "url": "o003-c90-ch01-exercise-guides.html#o003-c90-ch01-exercise-10",
  "type": "Pemeriksaan",
  "number": "A.17",
  "title": "Latihan 10: benar, salah, bukti, dan contoh tandingan.",
  "body": "Latihan 10: benar, salah, bukti, dan contoh tandingan Periksa sepuluh keputusan Anda dan pastikan setiap klaim salah mempunyai contoh tandingan konkret.  Petunjuk 1. Inklusi berbalik saat mengambil komplemen.  Petunjuk 2. Untuk identitas selisih, ubah menjadi ; bedakan dari .   Urutannya adalah: benar, benar, salah, benar, salah, salah, benar, benar, salah, benar.   (a) Anggota berada di dan , jadi di irisannya. (b) Anggota berasal dari salah satu subhimpunan . (c) Salah: ambil , , dan ; arah yang benar adalah . (d) Benar oleh pembalikan komplemen. (e) Salah: , ; ruas kiri . Identitas yang benar ialah . (f) Salah: , ; ruas kiri , bukan . Identitas umumnya . (g) Benar, karena kedua ruas berarti dan . (h) Benar relatif terhadap . (i) Salah: mempunyai tepat satu anggota, yaitu . (j) Benar: dan adalah dua objek berbeda.  "
},
{
  "id": "o003-c90-ch01-mastery",
  "level": "1",
  "url": "o003-c90-ch01-mastery.html",
  "type": "Bagian",
  "number": "",
  "title": "Uji penguasaan",
  "body": " Uji penguasaan  Kerjakan tanpa melihat bab atau pembahasan. Buka petunjuk hanya setelah menulis percobaan pertama.  Untuk , tentukan benar atau salah: , , , dan . Bandingkan anggota yang tertulis dengan subhimpunan yang seluruh anggotanya berada di . Keempatnya benar. Dua objek yang tercantum adalah dan . Satu-satunya anggota ialah , sehingga . Akhirnya , jadi .  Buktikan . Ikuti satu unsur dan negasikan syarat di atau di . Identitas benar. berada di ruas kiri jika dan hanya jika , , dan ; ini setara dengan dan , tepat syarat ruas kanan.  Untuk , , tentukan gabungan dan irisannya. Keluarga ini mengecil; interval terbesar terjadi saat . Untuk , pilih . dan . Karena dan sendiri ikut dalam keluarga, gabungannya . Nol berada di semua interval. Jika , ambil ; maka , sehingga .  Dalam semesta , sederhanakan . Terapkan De Morgan dua kali dan ingat . . .  Jika dan , hitung dan jelaskan. Hitung dahulu banyaknya subhimpunan , lalu gunakan aturan produk. . Ada pilihan untuk koordinat pertama dan, untuk masing-masing, pilihan koordinat kedua.  Nilai klaim: jika dan semua empat himpunan tidak kosong, maka dan . Untuk membuktikan , ambil dan gunakan satu anggota tetap . Klaim benar dengan asumsi ketakosongan; tanpa asumsi itu klaim salah. Pilih . Untuk setiap , pasangan berada di , sehingga . Jadi ; simetri memberi . Argumen yang sama pada koordinat kedua memberi . Ketakosongan perlu karena untuk sembarang .  "
},
{
  "id": "o003-c90-ch01-mastery-01",
  "level": "2",
  "url": "o003-c90-ch01-mastery.html#o003-c90-ch01-mastery-01",
  "type": "Pemeriksaan",
  "number": "A.18",
  "title": "",
  "body": "Untuk , tentukan benar atau salah: , , , dan . Bandingkan anggota yang tertulis dengan subhimpunan yang seluruh anggotanya berada di . Keempatnya benar. Dua objek yang tercantum adalah dan . Satu-satunya anggota ialah , sehingga . Akhirnya , jadi . "
},
{
  "id": "o003-c90-ch01-mastery-02",
  "level": "2",
  "url": "o003-c90-ch01-mastery.html#o003-c90-ch01-mastery-02",
  "type": "Pemeriksaan",
  "number": "A.19",
  "title": "",
  "body": "Buktikan . Ikuti satu unsur dan negasikan syarat di atau di . Identitas benar. berada di ruas kiri jika dan hanya jika , , dan ; ini setara dengan dan , tepat syarat ruas kanan. "
},
{
  "id": "o003-c90-ch01-mastery-03",
  "level": "2",
  "url": "o003-c90-ch01-mastery.html#o003-c90-ch01-mastery-03",
  "type": "Pemeriksaan",
  "number": "A.20",
  "title": "",
  "body": "Untuk , , tentukan gabungan dan irisannya. Keluarga ini mengecil; interval terbesar terjadi saat . Untuk , pilih . dan . Karena dan sendiri ikut dalam keluarga, gabungannya . Nol berada di semua interval. Jika , ambil ; maka , sehingga . "
},
{
  "id": "o003-c90-ch01-mastery-04",
  "level": "2",
  "url": "o003-c90-ch01-mastery.html#o003-c90-ch01-mastery-04",
  "type": "Pemeriksaan",
  "number": "A.21",
  "title": "",
  "body": "Dalam semesta , sederhanakan . Terapkan De Morgan dua kali dan ingat . . . "
},
{
  "id": "o003-c90-ch01-mastery-05",
  "level": "2",
  "url": "o003-c90-ch01-mastery.html#o003-c90-ch01-mastery-05",
  "type": "Pemeriksaan",
  "number": "A.22",
  "title": "",
  "body": "Jika dan , hitung dan jelaskan. Hitung dahulu banyaknya subhimpunan , lalu gunakan aturan produk. . Ada pilihan untuk koordinat pertama dan, untuk masing-masing, pilihan koordinat kedua. "
},
{
  "id": "o003-c90-ch01-mastery-06",
  "level": "2",
  "url": "o003-c90-ch01-mastery.html#o003-c90-ch01-mastery-06",
  "type": "Pemeriksaan",
  "number": "A.23",
  "title": "",
  "body": "Nilai klaim: jika dan semua empat himpunan tidak kosong, maka dan . Untuk membuktikan , ambil dan gunakan satu anggota tetap . Klaim benar dengan asumsi ketakosongan; tanpa asumsi itu klaim salah. Pilih . Untuk setiap , pasangan berada di , sehingga . Jadi ; simetri memberi . Argumen yang sama pada koordinat kedua memberi . Ketakosongan perlu karena untuk sembarang . "
},
{
  "id": "o003-c90-ch01-error-diagnostics",
  "level": "1",
  "url": "o003-c90-ch01-error-diagnostics.html",
  "type": "Bagian",
  "number": "",
  "title": "Diagnostik kesalahan ringkas",
  "body": " Diagnostik kesalahan ringkas   Menukar dan Ucapkan jenis objeknya: ruas kiri adalah satu anggota; ruas kiri adalah sebuah himpunan yang semua anggotanya harus diuji.  Membuktikan kesamaan hanya satu arah Tulis dua sasaran terpisah, dan , sebelum memulai bukti.  Komplemen tanpa semesta Catat semesta ; nilai berubah ketika berubah.  Menukar untuk semua dan ada Irisan memakai ; gabungan memakai . Negasi menukar keduanya.  Contoh tandingan tidak memenuhi hipotesis Periksa semua asumsi terlebih dahulu, baru tunjukkan bahwa kesimpulannya gagal.  Menganggap semua subhimpunan produk berbentuk produk Produk harus memuat seluruh kombinasi silang, bukan hanya pasangan yang dipilih.  Mengabaikan kasus kosong Uji , keluarga indeks kosong, atau faktor produk kosong sebelum menyatakan inklusi ketat atau pembatalan.   "
},
{
  "id": "o003-c90-ch02-activity-checkpoints",
  "level": "1",
  "url": "o003-c90-ch02-activity-checkpoints.html",
  "type": "Bagian",
  "number": "",
  "title": "Pemeriksaan eksplorasi dan aktivitas",
  "body": " Pemeriksaan eksplorasi dan aktivitas  Pemeriksaan 1: aturan yang sama, fungsi yang berbeda  Setelah menyelesaikan eksplorasi pembuka pada bagian Pendahuluan, klasifikasikan keempat fungsi yang memakai aturan . Nyatakan pula fungsi mana yang merupakan pembatasan dan fungsi mana yang merupakan perluasannya. Rubrik lengkap: domain dan kodomain harus disebutkan; kegagalan injektivitas harus disertai dua masukan; kegagalan surjektivitas harus disertai satu unsur kodomain tanpa prapeta; setiap klaim positif harus dibuktikan.   Petunjuk 1. Bandingkan dan , lalu selesaikan .  Petunjuk 2. Periksa secara terpisah apakah termasuk domain dan apakah termasuk daerah hasil.    bukan injeksi maupun surjeksi; injektif tetapi bukan surjektif; surjektif tetapi bukan injektif; dan bijektif. Fungsi adalah pembatasan pada , dan merupakan perluasan . Selain itu, , sehingga merupakan pembatasan dan merupakan perluasan .   Karena , fungsi pertama dan tidak injektif. Daerah hasil aturan tersebut pada ialah , sehingga tidak mencapai, misalnya, , sedangkan mencapai setiap melalui . Pada domain positif ketat, naik tegas dan daerah hasilnya ; karena itu injektif tetapi tidak mencapai ataupun unsur kodomain di bawahnya. Pada domain tak negatif, akar ada dan tunggal untuk setiap , sehingga bijektif. Menurut definisi, kesamaan aturan pada subdomain memberi , sehingga pembatasan dan perluasan . Demikian pula, aturan dan sama pada subdomain , jadi : adalah pembatasan dan adalah perluasan . Klasifikasi berubah karena domain dan kodomain merupakan bagian dari data fungsi, bukan hiasan pada rumus.   Pemeriksaan 2: komposisi pada himpunan berhingga  Periksa seluruh lima tugas pada aktivitas . Rubrik: tulis tabel nilai kedua komposit, lalu dukung setiap klasifikasi dengan tabrakan masukan, unsur kodomain yang hilang, atau pemeriksaan menyeluruh.   Petunjuk 1. Terapkan atau dahulu, baru .  Petunjuk 2. Pada himpunan berhingga, bandingkan daftar keluaran dengan seluruh kodomain.    memetakan berturut-turut ke ; memetakannya ke . Fungsi injektif tetapi tidak surjektif, bukan keduanya, dan surjektif tetapi tidak injektif. Komposit pertama bijektif; komposit kedua bukan injektif maupun surjektif.   Dari tabel sumber, , , dan . Ketiga keluaran berbeda dan memenuhi . Sebaliknya, , , dan ; masukan dan bertabrakan dan tidak tercapai. Keluaran ialah , keluaran ialah , dan keluaran ialah seluruh , dengan . Fakta-fakta ini memberi semua klasifikasi pada jawaban.   Pemeriksaan 3: membangun komposit  Untuk aktivitas , berikan fungsi konkret pada ketiga bagian dan jelaskan sifat kompositnya. Rubrik: setiap unsur domain harus mempunyai tepat satu citra, kodomain harus benar, dan alasan tidak boleh hanya mengandalkan gambar.   Petunjuk 1. Gunakan korespondensi , , sebagai fungsi pertama.  Petunjuk 2. Untuk surjeksi ke , salah satu nilai boleh dipakai dua kali.   Contoh yang sah: gunakan . Untuk kasus injektif, ambil . Untuk kasus surjektif ke , ambil . Untuk kasus bijektif ke , ambil . Kompositnya berturut-turut injektif, surjektif, dan bijektif.   Fungsi yang dipilih adalah bijeksi , jadi khususnya injektif dan surjektif. Pada pilihan pertama, keluaran komposit adalah , semuanya berbeda, maka komposit injektif. Pada pilihan kedua, keluaran komposit memuat dan , yaitu seluruh , maka komposit surjektif. Pada pilihan terakhir, komposit memetakan masing-masing ke dirinya sendiri; fungsi identitas ini bijektif.   Pemeriksaan 4: teorema komposisi  Lengkapi aktivitas pembuktian sesudah . Rubrik: bukti injektivitas dimulai dari kesamaan keluaran, bukti surjektivitas dimulai dari unsur sembarang kodomain, dan bagian bijektif menyebut kedua hasil.   Petunjuk 1. Dari , gunakan injektivitas dalam urutan terbalik.  Petunjuk 2. Untuk , pilih dahulu prapeta di , lalu prapetanya di .   Komposit dua injeksi adalah injeksi; komposit dua surjeksi adalah surjeksi; karena bijeksi berarti kedua sifat tersebut, komposit dua bijeksi adalah bijeksi.   Andaikan . Injektivitas memberi , lalu injektivitas memberi . Untuk surjektivitas, ambil . Karena surjektif, ada dengan ; karena surjektif, ada dengan . Maka . Jika kedua fungsi bijektif, kedua argumen berlaku, sehingga komposit sekaligus injektif dan surjektif.   Pemeriksaan 5: kapan relasi invers menjadi fungsi  Periksa aktivitas . Rubrik: tulis setiap relasi invers sebagai pasangan terurut; uji syarat eksistensi bagi setiap unsur domain baru dan syarat ketunggalan keluarannya; simpulkan syarat umum.   Petunjuk 1. Balik urutan setiap pasangan pada tabel fungsi.  Petunjuk 2. Surjektivitas fungsi asal memberi eksistensi pada invers; injektivitas memberi ketunggalan.    merupakan fungsi . dan bukan fungsi dengan domain . Secara umum, invers merupakan fungsi tepat ketika bijektif.   Pada , setiap unsur muncul sekali sebagai koordinat pertama, sehingga eksistensi dan ketunggalan terpenuhi. Pada , mempunyai dua keluaran dan tidak mempunyai keluaran. Pada , mempunyai dua keluaran. Untuk relasi invers umum, setiap muncul sebagai koordinat pertama sedikitnya sekali tepat ketika surjektif, dan paling banyak sekali tepat ketika injektif. Kedua syarat fungsi berlaku tepat ketika bijektif.   Pemeriksaan 6: bukti bikondisional invers  Lengkapi aktivitas pembuktian sesudah . Rubrik: kedua arah bikondisional harus dibuktikan; pada tiap arah, pisahkan eksistensi dan ketunggalan, atau surjektivitas dan injektivitas.   Petunjuk 1. Jika bijektif, gunakan surjektivitas untuk menemukan dan injektivitas untuk membuktikan bahwa tunggal.  Petunjuk 2. Jika fungsi, setiap harus mempunyai tepat satu pasangan balik.   merupakan fungsi jika dan hanya jika bijektif.   Jika bijektif dan , surjektivitas memberi suatu dengan , sehingga . Jika juga , maka ; injektivitas memberi . Jadi invers adalah fungsi. Sebaliknya, andaikan invers adalah fungsi pada seluruh . Untuk setiap , adanya nilai memberi , jadi surjektif. Jika , relasi invers memuat dan ; ketunggalan nilai fungsi invers memberi . Jadi injektif dan karenanya bijektif.   Pemeriksaan 7: invers komposit  Selesaikan aktivitas . Rubrik: periksa tipe setiap komposit, gunakan unsur sembarang , dan buktikan kesamaan fungsi pada seluruh domain, bukan pada satu contoh.   Petunjuk 1. Untuk membatalkan , tindakan terakhir harus dibalik lebih dahulu.  Petunjuk 2. Tuliskan dan , lalu evaluasi kedua ruas pada .    bijektif dan .   Komposit bijeksi adalah bijeksi, jadi inversnya ada. Ambil . Karena dan bijektif, terdapat unsur tunggal dan dengan dan . Maka , sehingga . Di sisi lain, dan , sehingga . Kesamaan berlaku untuk setiap , jadi kedua fungsi sama. Urutan sebaliknya umumnya bahkan tidak bertipe benar.   Pemeriksaan 8: prapeta komposit  Untuk aktivitas terakhir pada bagian Fungsi dan Himpunan, tentukan hubungan antara dua prapeta yang diberikan dan buktikan dengan argumen unsur. Rubrik: semua ekuivalensi harus menyebut keanggotaan pada ; jangan berasumsi bahwa atau invertibel.   Petunjuk 1. Mulai dengan .  Petunjuk 2. Buka definisi prapeta dua kali.   .   Untuk , jika dan hanya jika . Ini setara dengan , yang setara dengan . Rantai ekuivalensi berlaku bagi setiap , sehingga kedua himpunan sama. Simbol invers di sini menyatakan prapeta himpunan dan tidak memerlukan bijektivitas.   "
},
{
  "id": "o003-c90-ch02-checkpoint-01",
  "level": "2",
  "url": "o003-c90-ch02-activity-checkpoints.html#o003-c90-ch02-checkpoint-01",
  "type": "Pemeriksaan",
  "number": "B.1",
  "title": "Pemeriksaan 1: aturan yang sama, fungsi yang berbeda.",
  "body": "Pemeriksaan 1: aturan yang sama, fungsi yang berbeda  Setelah menyelesaikan eksplorasi pembuka pada bagian Pendahuluan, klasifikasikan keempat fungsi yang memakai aturan . Nyatakan pula fungsi mana yang merupakan pembatasan dan fungsi mana yang merupakan perluasannya. Rubrik lengkap: domain dan kodomain harus disebutkan; kegagalan injektivitas harus disertai dua masukan; kegagalan surjektivitas harus disertai satu unsur kodomain tanpa prapeta; setiap klaim positif harus dibuktikan.   Petunjuk 1. Bandingkan dan , lalu selesaikan .  Petunjuk 2. Periksa secara terpisah apakah termasuk domain dan apakah termasuk daerah hasil.    bukan injeksi maupun surjeksi; injektif tetapi bukan surjektif; surjektif tetapi bukan injektif; dan bijektif. Fungsi adalah pembatasan pada , dan merupakan perluasan . Selain itu, , sehingga merupakan pembatasan dan merupakan perluasan .   Karena , fungsi pertama dan tidak injektif. Daerah hasil aturan tersebut pada ialah , sehingga tidak mencapai, misalnya, , sedangkan mencapai setiap melalui . Pada domain positif ketat, naik tegas dan daerah hasilnya ; karena itu injektif tetapi tidak mencapai ataupun unsur kodomain di bawahnya. Pada domain tak negatif, akar ada dan tunggal untuk setiap , sehingga bijektif. Menurut definisi, kesamaan aturan pada subdomain memberi , sehingga pembatasan dan perluasan . Demikian pula, aturan dan sama pada subdomain , jadi : adalah pembatasan dan adalah perluasan . Klasifikasi berubah karena domain dan kodomain merupakan bagian dari data fungsi, bukan hiasan pada rumus.  "
},
{
  "id": "o003-c90-ch02-checkpoint-02",
  "level": "2",
  "url": "o003-c90-ch02-activity-checkpoints.html#o003-c90-ch02-checkpoint-02",
  "type": "Pemeriksaan",
  "number": "B.2",
  "title": "Pemeriksaan 2: komposisi pada himpunan berhingga.",
  "body": "Pemeriksaan 2: komposisi pada himpunan berhingga  Periksa seluruh lima tugas pada aktivitas . Rubrik: tulis tabel nilai kedua komposit, lalu dukung setiap klasifikasi dengan tabrakan masukan, unsur kodomain yang hilang, atau pemeriksaan menyeluruh.   Petunjuk 1. Terapkan atau dahulu, baru .  Petunjuk 2. Pada himpunan berhingga, bandingkan daftar keluaran dengan seluruh kodomain.    memetakan berturut-turut ke ; memetakannya ke . Fungsi injektif tetapi tidak surjektif, bukan keduanya, dan surjektif tetapi tidak injektif. Komposit pertama bijektif; komposit kedua bukan injektif maupun surjektif.   Dari tabel sumber, , , dan . Ketiga keluaran berbeda dan memenuhi . Sebaliknya, , , dan ; masukan dan bertabrakan dan tidak tercapai. Keluaran ialah , keluaran ialah , dan keluaran ialah seluruh , dengan . Fakta-fakta ini memberi semua klasifikasi pada jawaban.  "
},
{
  "id": "o003-c90-ch02-checkpoint-03",
  "level": "2",
  "url": "o003-c90-ch02-activity-checkpoints.html#o003-c90-ch02-checkpoint-03",
  "type": "Pemeriksaan",
  "number": "B.3",
  "title": "Pemeriksaan 3: membangun komposit.",
  "body": "Pemeriksaan 3: membangun komposit  Untuk aktivitas , berikan fungsi konkret pada ketiga bagian dan jelaskan sifat kompositnya. Rubrik: setiap unsur domain harus mempunyai tepat satu citra, kodomain harus benar, dan alasan tidak boleh hanya mengandalkan gambar.   Petunjuk 1. Gunakan korespondensi , , sebagai fungsi pertama.  Petunjuk 2. Untuk surjeksi ke , salah satu nilai boleh dipakai dua kali.   Contoh yang sah: gunakan . Untuk kasus injektif, ambil . Untuk kasus surjektif ke , ambil . Untuk kasus bijektif ke , ambil . Kompositnya berturut-turut injektif, surjektif, dan bijektif.   Fungsi yang dipilih adalah bijeksi , jadi khususnya injektif dan surjektif. Pada pilihan pertama, keluaran komposit adalah , semuanya berbeda, maka komposit injektif. Pada pilihan kedua, keluaran komposit memuat dan , yaitu seluruh , maka komposit surjektif. Pada pilihan terakhir, komposit memetakan masing-masing ke dirinya sendiri; fungsi identitas ini bijektif.  "
},
{
  "id": "o003-c90-ch02-checkpoint-04",
  "level": "2",
  "url": "o003-c90-ch02-activity-checkpoints.html#o003-c90-ch02-checkpoint-04",
  "type": "Pemeriksaan",
  "number": "B.4",
  "title": "Pemeriksaan 4: teorema komposisi.",
  "body": "Pemeriksaan 4: teorema komposisi  Lengkapi aktivitas pembuktian sesudah . Rubrik: bukti injektivitas dimulai dari kesamaan keluaran, bukti surjektivitas dimulai dari unsur sembarang kodomain, dan bagian bijektif menyebut kedua hasil.   Petunjuk 1. Dari , gunakan injektivitas dalam urutan terbalik.  Petunjuk 2. Untuk , pilih dahulu prapeta di , lalu prapetanya di .   Komposit dua injeksi adalah injeksi; komposit dua surjeksi adalah surjeksi; karena bijeksi berarti kedua sifat tersebut, komposit dua bijeksi adalah bijeksi.   Andaikan . Injektivitas memberi , lalu injektivitas memberi . Untuk surjektivitas, ambil . Karena surjektif, ada dengan ; karena surjektif, ada dengan . Maka . Jika kedua fungsi bijektif, kedua argumen berlaku, sehingga komposit sekaligus injektif dan surjektif.  "
},
{
  "id": "o003-c90-ch02-checkpoint-05",
  "level": "2",
  "url": "o003-c90-ch02-activity-checkpoints.html#o003-c90-ch02-checkpoint-05",
  "type": "Pemeriksaan",
  "number": "B.5",
  "title": "Pemeriksaan 5: kapan relasi invers menjadi fungsi.",
  "body": "Pemeriksaan 5: kapan relasi invers menjadi fungsi  Periksa aktivitas . Rubrik: tulis setiap relasi invers sebagai pasangan terurut; uji syarat eksistensi bagi setiap unsur domain baru dan syarat ketunggalan keluarannya; simpulkan syarat umum.   Petunjuk 1. Balik urutan setiap pasangan pada tabel fungsi.  Petunjuk 2. Surjektivitas fungsi asal memberi eksistensi pada invers; injektivitas memberi ketunggalan.    merupakan fungsi . dan bukan fungsi dengan domain . Secara umum, invers merupakan fungsi tepat ketika bijektif.   Pada , setiap unsur muncul sekali sebagai koordinat pertama, sehingga eksistensi dan ketunggalan terpenuhi. Pada , mempunyai dua keluaran dan tidak mempunyai keluaran. Pada , mempunyai dua keluaran. Untuk relasi invers umum, setiap muncul sebagai koordinat pertama sedikitnya sekali tepat ketika surjektif, dan paling banyak sekali tepat ketika injektif. Kedua syarat fungsi berlaku tepat ketika bijektif.  "
},
{
  "id": "o003-c90-ch02-checkpoint-06",
  "level": "2",
  "url": "o003-c90-ch02-activity-checkpoints.html#o003-c90-ch02-checkpoint-06",
  "type": "Pemeriksaan",
  "number": "B.6",
  "title": "Pemeriksaan 6: bukti bikondisional invers.",
  "body": "Pemeriksaan 6: bukti bikondisional invers  Lengkapi aktivitas pembuktian sesudah . Rubrik: kedua arah bikondisional harus dibuktikan; pada tiap arah, pisahkan eksistensi dan ketunggalan, atau surjektivitas dan injektivitas.   Petunjuk 1. Jika bijektif, gunakan surjektivitas untuk menemukan dan injektivitas untuk membuktikan bahwa tunggal.  Petunjuk 2. Jika fungsi, setiap harus mempunyai tepat satu pasangan balik.   merupakan fungsi jika dan hanya jika bijektif.   Jika bijektif dan , surjektivitas memberi suatu dengan , sehingga . Jika juga , maka ; injektivitas memberi . Jadi invers adalah fungsi. Sebaliknya, andaikan invers adalah fungsi pada seluruh . Untuk setiap , adanya nilai memberi , jadi surjektif. Jika , relasi invers memuat dan ; ketunggalan nilai fungsi invers memberi . Jadi injektif dan karenanya bijektif.  "
},
{
  "id": "o003-c90-ch02-checkpoint-07",
  "level": "2",
  "url": "o003-c90-ch02-activity-checkpoints.html#o003-c90-ch02-checkpoint-07",
  "type": "Pemeriksaan",
  "number": "B.7",
  "title": "Pemeriksaan 7: invers komposit.",
  "body": "Pemeriksaan 7: invers komposit  Selesaikan aktivitas . Rubrik: periksa tipe setiap komposit, gunakan unsur sembarang , dan buktikan kesamaan fungsi pada seluruh domain, bukan pada satu contoh.   Petunjuk 1. Untuk membatalkan , tindakan terakhir harus dibalik lebih dahulu.  Petunjuk 2. Tuliskan dan , lalu evaluasi kedua ruas pada .    bijektif dan .   Komposit bijeksi adalah bijeksi, jadi inversnya ada. Ambil . Karena dan bijektif, terdapat unsur tunggal dan dengan dan . Maka , sehingga . Di sisi lain, dan , sehingga . Kesamaan berlaku untuk setiap , jadi kedua fungsi sama. Urutan sebaliknya umumnya bahkan tidak bertipe benar.  "
},
{
  "id": "o003-c90-ch02-checkpoint-08",
  "level": "2",
  "url": "o003-c90-ch02-activity-checkpoints.html#o003-c90-ch02-checkpoint-08",
  "type": "Pemeriksaan",
  "number": "B.8",
  "title": "Pemeriksaan 8: prapeta komposit.",
  "body": "Pemeriksaan 8: prapeta komposit  Untuk aktivitas terakhir pada bagian Fungsi dan Himpunan, tentukan hubungan antara dua prapeta yang diberikan dan buktikan dengan argumen unsur. Rubrik: semua ekuivalensi harus menyebut keanggotaan pada ; jangan berasumsi bahwa atau invertibel.   Petunjuk 1. Mulai dengan .  Petunjuk 2. Buka definisi prapeta dua kali.   .   Untuk , jika dan hanya jika . Ini setara dengan , yang setara dengan . Rantai ekuivalensi berlaku bagi setiap , sehingga kedua himpunan sama. Simbol invers di sini menyatakan prapeta himpunan dan tidak memerlukan bijektivitas.  "
},
{
  "id": "o003-c90-ch02-mastery",
  "level": "1",
  "url": "o003-c90-ch02-mastery.html",
  "type": "Bagian",
  "number": "",
  "title": "Uji penguasaan",
  "body": " Uji penguasaan  Kerjakan tanpa melihat bab atau pembahasan. Buka petunjuk hanya setelah Anda menuliskan domain, kodomain, dan argumen pertama.  Penguasaan 1: data fungsi  Untuk , , tentukan domain, kodomain, daerah hasil, citra , semua prapeta , dan klasifikasinya.   Bedakan himpunan yang dinyatakan setelah tanda panah dari himpunan nilai yang benar-benar tercapai.   Domain dan kodomain sama-sama ; daerah hasilnya ; ; tidak mempunyai prapeta; fungsi injektif tetapi tidak surjektif.   Dari penulisan , domain dan kodomainnya sama-sama . Substitusi langsung memberi . Daerah hasil terdiri tepat atas bilangan genap. Jika , maka dan , jadi fungsi injektif. Persamaan tidak mempunyai solusi bilangan bulat, sehingga adalah unsur kodomain yang tidak tercapai dan fungsi tidak surjektif.   Penguasaan 2: mengubah kodomain  Pandang aturan yang sama sebagai , . Buktikan klasifikasinya dan tulis inversnya.   Setiap unsur kodomain kini berbentuk untuk suatu .   bijektif dan .   Bukti injektivitas sama seperti pada soal sebelumnya. Untuk setiap , berlaku , sehingga surjektif ke kodomain barunya. Jadi bijektif. Persamaan menunjukkan langsung bahwa fungsi invers memetakan ke .   Penguasaan 3: tipe dan urutan komposisi  Misalkan , , dan , . Tentukan tipe dan rumus kedua urutan komposisi, lalu nilai injektivitas dan surjektivitas masing-masing.   Cocokkan kodomain fungsi yang diterapkan pertama dengan domain fungsi kedua.    selalu terdefinisi dan bernilai ; fungsi ini bukan injektif dan bukan surjektif. bernilai ; fungsi ini injektif tetapi tidak surjektif.   Karena keluaran berada dalam domain , . Nilai dan bertabrakan untuk , dan keluaran di bawah tidak tercapai, jadi fungsi bukan injektif maupun surjektif ke . Karena kodomain sama dengan domain , juga terdefinisi dan bernilai . Pada fungsi ini naik tegas, maka injektif; daerah hasilnya , sehingga dalam kodomain tidak tercapai dan fungsi tidak surjektif. Kedua urutan sah di sini, tetapi tipenya tetap harus diperiksa sebelum rumus dievaluasi.   Penguasaan 4: relasi invers dan fungsi invers  Definisikan dengan . Tuliskan relasi , putuskan apakah ia fungsi, lalu temukan pembatasan domain terbesar yang membuat aturan kuadrat bijektif ke kodomain yang sama.   Pilih tepat satu unsur dari setiap pasangan dan , serta pertahankan .    bukan fungsi. Salah satu pembatasan terbesar ialah , yang bijektif.   Pada relasi balik, masukan mempunyai keluaran dan , sedangkan masukan mempunyai keluaran dan ; syarat ketunggalan fungsi gagal. Suatu pembatasan bijektif harus memilih satu prapeta bagi masing-masing . Pilihan melakukan tepat itu, sehingga pembatasannya injektif dan surjektif. Ukuran maksimal karena kodomain hanya mempunyai tiga unsur.   Penguasaan 5: menghitung citra dan prapeta  Misalkan memenuhi . Untuk dan , hitung , , , dan .   Prapeta menghimpun semua masukan yang nilainya berada di himpunan sasaran, termasuk masukan yang tidak berada di .    , , , dan .   Citra dan ialah dan , jadi sama dengan seluruh kodomain. Karena dan tepat merupakan masukan yang bernilai , prapeta ialah . Prapeta seluruh kodomain adalah seluruh domain. Menerapkan pada menghasilkan hanya .   Penguasaan 6: prapeta dan selisih  Untuk dan , buktikan . Nyatakan kasus komplemen sebagai akibatnya.   Buka syarat menjadi satu keanggotaan dan satu ketidakanggotaan.   Identitas berlaku untuk setiap fungsi. Dengan , diperoleh .   Untuk , setara dengan dan . Ini setara dengan dan , yaitu . Jika , maka , sehingga rumus komplemen mengikuti.   Penguasaan 7: sama banyak dengan subhimpunan ketat  Buktikan bahwa dan himpunan bilangan bulat genap mempunyai kardinalitas sama, walaupun .   Bangun bijeksi dengan mengalikan dua dan tulis inversnya pada kodomain .   Bijeksi , , membuktikan kedua himpunan ekuinumeros.   Jika , maka , jadi injektif. Setiap unsur secara definisi berbentuk dan merupakan , jadi surjektif. Inversnya . Inklusi bersifat ketat karena, misalnya, tetapi . Fenomena ini dapat terjadi pada himpunan tak berhingga.   Penguasaan 8: injeksi versus surjeksi pada himpunan berhingga  Misalkan dan berhingga dengan , dan . Buktikan bahwa injektif jika dan hanya jika surjektif.   Pada himpunan berukuran sama, satu tabrakan memaksa satu unsur kodomain hilang, dan satu unsur hilang memaksa satu tabrakan.   Pada domain dan kodomain berhingga yang sama besar, injektivitas dan surjektivitas ekuivalen.   Tuliskan . Jika injektif, unsur domain mempunyai citra berbeda di dalam kodomain yang hanya berisi unsur; semua unsur kodomain tercapai, jadi surjektif. Jika surjektif, pilih sedikitnya satu prapeta bagi setiap satu dari unsur kodomain. Pilihan ini sudah memakai seluruh unsur domain, sehingga tidak ada unsur kodomain yang dapat mempunyai prapeta kedua; jadi injektif. Argumen gagal tanpa keberhinggaan atau tanpa kesamaan ukuran.   "
},
{
  "id": "o003-c90-ch02-mastery-01",
  "level": "2",
  "url": "o003-c90-ch02-mastery.html#o003-c90-ch02-mastery-01",
  "type": "Pemeriksaan",
  "number": "B.9",
  "title": "Penguasaan 1: data fungsi.",
  "body": "Penguasaan 1: data fungsi  Untuk , , tentukan domain, kodomain, daerah hasil, citra , semua prapeta , dan klasifikasinya.   Bedakan himpunan yang dinyatakan setelah tanda panah dari himpunan nilai yang benar-benar tercapai.   Domain dan kodomain sama-sama ; daerah hasilnya ; ; tidak mempunyai prapeta; fungsi injektif tetapi tidak surjektif.   Dari penulisan , domain dan kodomainnya sama-sama . Substitusi langsung memberi . Daerah hasil terdiri tepat atas bilangan genap. Jika , maka dan , jadi fungsi injektif. Persamaan tidak mempunyai solusi bilangan bulat, sehingga adalah unsur kodomain yang tidak tercapai dan fungsi tidak surjektif.  "
},
{
  "id": "o003-c90-ch02-mastery-02",
  "level": "2",
  "url": "o003-c90-ch02-mastery.html#o003-c90-ch02-mastery-02",
  "type": "Pemeriksaan",
  "number": "B.10",
  "title": "Penguasaan 2: mengubah kodomain.",
  "body": "Penguasaan 2: mengubah kodomain  Pandang aturan yang sama sebagai , . Buktikan klasifikasinya dan tulis inversnya.   Setiap unsur kodomain kini berbentuk untuk suatu .   bijektif dan .   Bukti injektivitas sama seperti pada soal sebelumnya. Untuk setiap , berlaku , sehingga surjektif ke kodomain barunya. Jadi bijektif. Persamaan menunjukkan langsung bahwa fungsi invers memetakan ke .  "
},
{
  "id": "o003-c90-ch02-mastery-03",
  "level": "2",
  "url": "o003-c90-ch02-mastery.html#o003-c90-ch02-mastery-03",
  "type": "Pemeriksaan",
  "number": "B.11",
  "title": "Penguasaan 3: tipe dan urutan komposisi.",
  "body": "Penguasaan 3: tipe dan urutan komposisi  Misalkan , , dan , . Tentukan tipe dan rumus kedua urutan komposisi, lalu nilai injektivitas dan surjektivitas masing-masing.   Cocokkan kodomain fungsi yang diterapkan pertama dengan domain fungsi kedua.    selalu terdefinisi dan bernilai ; fungsi ini bukan injektif dan bukan surjektif. bernilai ; fungsi ini injektif tetapi tidak surjektif.   Karena keluaran berada dalam domain , . Nilai dan bertabrakan untuk , dan keluaran di bawah tidak tercapai, jadi fungsi bukan injektif maupun surjektif ke . Karena kodomain sama dengan domain , juga terdefinisi dan bernilai . Pada fungsi ini naik tegas, maka injektif; daerah hasilnya , sehingga dalam kodomain tidak tercapai dan fungsi tidak surjektif. Kedua urutan sah di sini, tetapi tipenya tetap harus diperiksa sebelum rumus dievaluasi.  "
},
{
  "id": "o003-c90-ch02-mastery-04",
  "level": "2",
  "url": "o003-c90-ch02-mastery.html#o003-c90-ch02-mastery-04",
  "type": "Pemeriksaan",
  "number": "B.12",
  "title": "Penguasaan 4: relasi invers dan fungsi invers.",
  "body": "Penguasaan 4: relasi invers dan fungsi invers  Definisikan dengan . Tuliskan relasi , putuskan apakah ia fungsi, lalu temukan pembatasan domain terbesar yang membuat aturan kuadrat bijektif ke kodomain yang sama.   Pilih tepat satu unsur dari setiap pasangan dan , serta pertahankan .    bukan fungsi. Salah satu pembatasan terbesar ialah , yang bijektif.   Pada relasi balik, masukan mempunyai keluaran dan , sedangkan masukan mempunyai keluaran dan ; syarat ketunggalan fungsi gagal. Suatu pembatasan bijektif harus memilih satu prapeta bagi masing-masing . Pilihan melakukan tepat itu, sehingga pembatasannya injektif dan surjektif. Ukuran maksimal karena kodomain hanya mempunyai tiga unsur.  "
},
{
  "id": "o003-c90-ch02-mastery-05",
  "level": "2",
  "url": "o003-c90-ch02-mastery.html#o003-c90-ch02-mastery-05",
  "type": "Pemeriksaan",
  "number": "B.13",
  "title": "Penguasaan 5: menghitung citra dan prapeta.",
  "body": "Penguasaan 5: menghitung citra dan prapeta  Misalkan memenuhi . Untuk dan , hitung , , , dan .   Prapeta menghimpun semua masukan yang nilainya berada di himpunan sasaran, termasuk masukan yang tidak berada di .    , , , dan .   Citra dan ialah dan , jadi sama dengan seluruh kodomain. Karena dan tepat merupakan masukan yang bernilai , prapeta ialah . Prapeta seluruh kodomain adalah seluruh domain. Menerapkan pada menghasilkan hanya .  "
},
{
  "id": "o003-c90-ch02-mastery-06",
  "level": "2",
  "url": "o003-c90-ch02-mastery.html#o003-c90-ch02-mastery-06",
  "type": "Pemeriksaan",
  "number": "B.14",
  "title": "Penguasaan 6: prapeta dan selisih.",
  "body": "Penguasaan 6: prapeta dan selisih  Untuk dan , buktikan . Nyatakan kasus komplemen sebagai akibatnya.   Buka syarat menjadi satu keanggotaan dan satu ketidakanggotaan.   Identitas berlaku untuk setiap fungsi. Dengan , diperoleh .   Untuk , setara dengan dan . Ini setara dengan dan , yaitu . Jika , maka , sehingga rumus komplemen mengikuti.  "
},
{
  "id": "o003-c90-ch02-mastery-07",
  "level": "2",
  "url": "o003-c90-ch02-mastery.html#o003-c90-ch02-mastery-07",
  "type": "Pemeriksaan",
  "number": "B.15",
  "title": "Penguasaan 7: sama banyak dengan subhimpunan ketat.",
  "body": "Penguasaan 7: sama banyak dengan subhimpunan ketat  Buktikan bahwa dan himpunan bilangan bulat genap mempunyai kardinalitas sama, walaupun .   Bangun bijeksi dengan mengalikan dua dan tulis inversnya pada kodomain .   Bijeksi , , membuktikan kedua himpunan ekuinumeros.   Jika , maka , jadi injektif. Setiap unsur secara definisi berbentuk dan merupakan , jadi surjektif. Inversnya . Inklusi bersifat ketat karena, misalnya, tetapi . Fenomena ini dapat terjadi pada himpunan tak berhingga.  "
},
{
  "id": "o003-c90-ch02-mastery-08",
  "level": "2",
  "url": "o003-c90-ch02-mastery.html#o003-c90-ch02-mastery-08",
  "type": "Pemeriksaan",
  "number": "B.16",
  "title": "Penguasaan 8: injeksi versus surjeksi pada himpunan berhingga.",
  "body": "Penguasaan 8: injeksi versus surjeksi pada himpunan berhingga  Misalkan dan berhingga dengan , dan . Buktikan bahwa injektif jika dan hanya jika surjektif.   Pada himpunan berukuran sama, satu tabrakan memaksa satu unsur kodomain hilang, dan satu unsur hilang memaksa satu tabrakan.   Pada domain dan kodomain berhingga yang sama besar, injektivitas dan surjektivitas ekuivalen.   Tuliskan . Jika injektif, unsur domain mempunyai citra berbeda di dalam kodomain yang hanya berisi unsur; semua unsur kodomain tercapai, jadi surjektif. Jika surjektif, pilih sedikitnya satu prapeta bagi setiap satu dari unsur kodomain. Pilihan ini sudah memakai seluruh unsur domain, sehingga tidak ada unsur kodomain yang dapat mempunyai prapeta kedua; jadi injektif. Argumen gagal tanpa keberhinggaan atau tanpa kesamaan ukuran.  "
},
{
  "id": "o003-c90-ch02-error-diagnostics",
  "level": "1",
  "url": "o003-c90-ch02-error-diagnostics.html",
  "type": "Bagian",
  "number": "",
  "title": "Diagnostik kesalahan ringkas",
  "body": " Diagnostik kesalahan ringkas   Mengabaikan kodomain Dua aturan yang sama dapat mempunyai sifat surjektif berbeda. Tulis tipe lengkap sebelum menguji.  Menukar daerah hasil dan kodomain Daerah hasil adalah nilai yang benar-benar tercapai dan selalu merupakan subhimpunan kodomain.  Membaca komposisi dari kiri Pada , terapkan lebih dahulu; periksa bahwa keluarannya dapat menjadi masukan .  Menganggap simbol selalu fungsi Relasi balik menjadi fungsi hanya untuk bijeksi; prapeta himpunan tetap terdefinisi tanpa bijektivitas.  Citra dan irisan Citra mempertahankan gabungan, tetapi untuk irisan hanya satu inklusi yang selalu benar; prapeta mempertahankan keduanya.  Membuktikan surjektivitas dengan satu contoh Mulai dari unsur sembarang kodomain dan bangun prapetanya.  Mengabaikan kasus kosong atau faktor tak kosong Periksa asumsi ketakosongan ketika memakai proyeksi, membatalkan produk, atau menafsirkan irisan keluarga kosong.   "
},
{
  "id": "o003-c90-ch02-exercise-guides",
  "level": "1",
  "url": "o003-c90-ch02-exercise-guides.html",
  "type": "Bagian",
  "number": "",
  "title": "Panduan dan pembahasan tujuh belas latihan",
  "body": " Panduan dan pembahasan tujuh belas latihan  Nomor di bawah mengikuti urutan latihan pada bagian Latihan Bab 2. Jika sebuah latihan sumber mempunyai beberapa tugas, satu panduan di sini menutup semuanya.  Latihan 1: merancang banyaknya prapeta  Periksa kelima contoh Anda pada latihan pertama. Sebuah contoh lengkap harus merupakan fungsi pada seluruh , mencapai setiap keluaran yang diklaim, dan mempunyai tepat banyak prapeta yang diminta.   Petunjuk 1. Identitas menyelesaikan kasus satu prapeta. Untuk dua prapeta, lipat setiap pasangan interval satuan berurutan ke satu interval satuan.  Petunjuk 2. Grafik mempunyai keluaran dengan tiga prapeta dan keluaran pada titik ekstrem dengan dua prapeta.   Contoh berturut-turut dapat diambil sebagai fungsi identitas; fungsi lipatan interval yang mempunyai tepat dua prapeta bagi setiap keluaran (juga memenuhi setidaknya dua ); fungsi lipatan yang sama; ; dan fungsi konstan .   Untuk kasus pertama, memberi satu prapeta bagi setiap . Untuk kasus kedua dan ketiga, bagi setiap definisikan pada dan pada . Interval-interval domain saling lepas dan menutupi . Jika , dua dan hanya dua prapetanya ialah dan . Jadi fungsi ini mempunyai tepat dua prapeta untuk setiap , dan khususnya sedikitnya dua.  Untuk kasus keempat, ambil . Keluaran mempunyai tepat tiga prapeta . Keluaran mempunyai dua prapeta berbeda: akar ganda dan akar ; faktorisasi setelah memindahkan keluaran ke ruas kiri memverifikasi bahwa tidak ada akar lain. Untuk kasus terakhir, fungsi konstan memberi tak berhingga banyak prapeta bagi unsur kodomain .   Latihan 2: enam klasifikasi fungsi  Klasifikasikan keenam fungsi pada latihan berjangkar dan dukung setiap keputusan dengan persamaan, tabrakan, atau unsur yang hilang.   Petunjuk 1. Untuk fungsi pecahan, selesaikan terhadap dan periksa nilai .  Petunjuk 2. Aturan kuadrat menjadi injektif setelah domain dibatasi ke bilangan tak negatif.   Berturut-turut: bijektif; injektif tetapi tidak surjektif; injektif tetapi tidak surjektif; bijektif; surjektif tetapi tidak injektif; dan bijektif.   Persamaan mempunyai solusi tunggal di , jadi bijektif. Pada , kesamaan keluaran masih memaksa kesamaan masukan, tetapi semua keluaran kongruen dengan modulo ; misalnya tidak tercapai, sehingga hanya injektif.  Jika , maka untuk satu-satunya kandidat ialah , yang tidak pernah sama dengan . Nilai mustahil karena akan memberi . Karena itu aturan pecahan injektif dengan daerah hasil : fungsi ke tidak surjektif, sedangkan fungsi ke bijektif. Akhirnya, dari ke bilangan tak negatif surjektif tetapi dan bertabrakan bila . Pada domain tak negatif, akar kuadrat memberi prapeta tunggal bagi setiap keluaran, jadi bijektif.   Latihan 3: membatasi tabel fungsi  Gunakan tabel pada latihan ketiga untuk menilai fungsi, menemukan pembatasan injektif terbesar, menyesuaikan kodomain agar surjektif, dan menghasilkan bijeksi.   Petunjuk 1. Kelompokkan unsur domain menurut nilai .  Petunjuk 2. Pembatasan injektif boleh memilih paling banyak satu wakil dari setiap serat.   Fungsi asal bukan injeksi dan bukan surjeksi. Salah satu pembatasan injektif terbesar memakai . Kodomain surjektif yang tepat ialah . Dengan dan , pembatasan merupakan bijeksi.   Serat-serat tak kosongnya adalah , , , , dan . Jadi terdapat tabrakan, sedangkan tidak tercapai. Suatu pembatasan injektif memilih paling banyak satu unsur dari masing-masing lima serat; pilihan pada jawaban memilih tepat satu dari setiap serat, sehingga ukurannya maksimal, yaitu . Daerah hasil fungsi adalah ; memandang aturan yang sama sebagai fungsi membuatnya surjektif. Membatasi sekaligus domain ke membuat setiap unsur mempunyai tepat satu prapeta, sehingga diperoleh bijeksi.   Latihan 4: subhimpunan produk dan persegi panjang  Berikan satu subhimpunan berbentuk produk dan satu subhimpunan yang tidak dapat ditulis sebagai produk, dengan memakai dua unsur berbeda dari masing-masing faktor.   Petunjuk 1. Produk satu unsur dengan dua unsur memberi contoh positif.  Petunjuk 2. Dua sudut diagonal memaksa dua sudut silang jika himpunannya benar-benar produk.   Untuk dan , ambil . Sebagai contoh negatif, ambil .   Bentuk sudah secara eksplisit merupakan produk dua subhimpunan. Andaikan . Dari dua pasangan di dalam diperoleh dan . Definisi produk lalu memaksa dan berada di , padahal keduanya tidak tercantum. Kontradiksi ini membuktikan bahwa bukan produk.   Latihan 5: kardinalitas berhingga dan bijeksi  Buktikan kedua arah hubungan antara dan keberadaan bijeksi untuk himpunan berhingga.   Petunjuk 1. Gunakan bijeksi pencacahan dan .  Petunjuk 2. Komposisi dengan bijeksi yang diasumsikan menghasilkan bijeksi antara dua himpunan bilangan bulat awal.   Terdapat bijeksi jika dan hanya jika .   Pilih bijeksi pencacahan dan . Jika , maka adalah bijeksi. Sebaliknya, jika bijektif, maka adalah bijeksi dari ke . Jika , fungsi itu tidak mungkin surjektif; jika , fungsi itu tidak mungkin injektif, menurut prinsip rumah merpati. Jadi satu-satunya kemungkinan ialah .   Latihan 6: citra sesudah prapeta dan sebaliknya  Lengkapi empat bagian latihan tentang dan , termasuk contoh ketat dan dua karakterisasi.   Petunjuk 1. Untuk kegagalan kesamaan pertama gunakan fungsi konstan pada domain dua unsur; untuk kegagalan kedua tambahkan unsur kodomain yang tidak tercapai.  Petunjuk 2. Pada arah balik karakterisasi injeksi, uji himpunan satu unsur.   Selalu dan , dan keduanya dapat ketat. Kesamaan kedua berlaku untuk setiap tepat ketika surjektif; kesamaan pertama berlaku untuk setiap tepat ketika injektif.   Jika , maka , sehingga . Kesamaan dapat gagal: untuk fungsi konstan dan , prapeta citranya adalah seluruh . Jika , ada dengan dan , jadi . Kesamaan dapat gagal untuk , , dan .  Jika surjektif dan , pilih dengan ; maka dan , sehingga kesamaan berlaku. Jika kesamaan berlaku untuk semua , ambil untuk memperoleh . Jika injektif dan , ada dengan , maka . Sebaliknya, andaikan kesamaan berlaku untuk semua . Jika , ambil ; maka , sehingga dan injektif.   Latihan 7: fungsi dan irisan terindeks  Putuskan kedua identitas pada latihan . Jika suatu kesamaan gagal, nyatakan dan buktikan inklusi yang selalu benar serta berikan contoh tandingan terkecil yang jelas.   Petunjuk 1. Fungsi konstan pada dua unsur dapat membuat citra dua himpunan saling beririsan walaupun himpunan asalnya tidak.  Petunjuk 2. Untuk prapeta, buka kuantor untuk setiap indeks ; tidak diperlukan injektivitas.   Selalu , tetapi kesamaan dapat gagal. Sebaliknya, prapeta mempertahankan irisan secara tepat: .   Jika , ada yang berada di setiap dan memenuhi . Maka berada di setiap , sehingga inklusi berlaku. Kesamaan gagal untuk fungsi konstan dengan dan : citra irisannya kosong, sedangkan irisan citranya . Untuk prapeta, setara dengan bagi setiap , yang setara dengan bagi setiap . Dengan konvensi irisan keluarga kosong sebagai seluruh himpunan semesta yang sesuai, argumen dan inklusi pertama juga mencakup himpunan indeks kosong.   Latihan 8: membatalkan bijeksi dengan inversnya  Buktikan kedua identitas pada latihan langsung dari definisi invers, dengan memperhatikan domain masing-masing identitas.   Petunjuk 1. Tetapkan dan gunakan ekuivalensi .  Petunjuk 2. Untuk arah lain, tetapkan .   dan .   Untuk , ambil . Definisi fungsi invers memberi , sehingga . Untuk , bijektivitas memberi unsur tunggal dengan . Karena itu . Identitas pertama adalah fungsi pada , sedangkan identitas kedua fungsi pada .   Latihan 9: prapeta himpunan oleh komposit  Buktikan identitas pada latihan dengan rantai ekuivalensi keanggotaan; jangan menganggap atau bijektif.   Untuk , terjemahkan berturut-turut , , dan .   .   Bagi setiap , jika dan hanya jika . Hal terakhir berlaku jika dan hanya jika , yang menurut definisi setara dengan . Karena unsur pada kedua ruas sama, himpunannya sama. Ini adalah identitas prapeta, bukan rumus invers fungsi.   Latihan 10: proyeksi dan hasil kali fungsi  Selesaikan keempat tugas tentang proyeksi, fungsi hasil kali, komposisinya, dan inversnya. Rubrik: rumus kandidat harus ditulis, keberadaan dan ketunggalan harus dipisahkan, dan semua kesamaan fungsi dibuktikan per unsur.   Petunjuk 1. Faktor lain yang tak kosong menyediakan koordinat pendamping untuk membuktikan proyeksi surjektif.  Petunjuk 2. Satu-satunya kandidat ialah .   Setiap surjektif. Fungsi tunggal yang diminta adalah . Hasil kali mempertahankan komposisi secara koordinat, dan jika invers ada, maka .   Untuk , pilih satu ; maka . Argumen simetris berlaku bagi . Definisikan . Proyeksi ke koordinat memberi , jadi diagram yang diminta komutatif. Sebaliknya, jika memenuhi kedua persamaan proyeksi, kedua koordinat harus sama dengan koordinat ; maka , membuktikan ketunggalan.  Pada , ruas kiri identitas komposisi bernilai , sama dengan ruas kanan. Jika adalah invers , maka komposisi mengirim ke dirinya sendiri, dan komposisi dalam urutan sebaliknya juga identitas pada . Jadi memang fungsi inversnya. Ketakosongan kedua faktor diperlukan pada bukti surjektivitas proyeksi.   Latihan 11: pencacahan bilangan bulat  Tentukan apakah rumus yang diberikan mendefinisikan injeksi dan surjeksi , lalu beri prapeta eksplisit untuk setiap bilangan bulat.   Petunjuk 1. Tulis atau .  Petunjuk 2. Keluaran cabang genap positif, sedangkan cabang ganjil tidak positif.   Fungsi tersebut bijektif. Secara khusus, dan untuk .   Substitusi memberi dan . Cabang genap memuat setiap bilangan bulat positif tepat sekali; cabang ganjil memuat tepat sekali. Kedua daerah hasil cabang saling lepas, jadi fungsi injektif. Untuk , prapetanya ; untuk , prapetanya . Maka setiap tercapai dan fungsi surjektif.   Latihan 12: penjumlahan sebagai fungsi dua peubah  Nilai injektivitas dan surjektivitas fungsi , , dengan saksi konkret.   Bandingkan dengan ; untuk mencapai , gunakan pasangan .   Fungsi penjumlahan tidak injektif, tetapi surjektif.   Pasangan berbeda dan keduanya dipetakan ke , sehingga fungsi tidak injektif. Untuk setiap , pasangan berada dalam domain dan memenuhi ; karena itu fungsi surjektif.   Latihan 13: sifat yang dipaksa oleh komposit  Tentukan bagian mana dari injektivitas atau surjektivitas yang harus diwarisi oleh faktor-faktornya, dan sangkal klaim yang terlalu kuat dengan fungsi berhingga yang bertipe benar.   Petunjuk 1. Jika , terapkan pada kedua ruas.  Petunjuk 2. Jika setiap berbentuk , maka setiap tentu berada dalam daerah hasil .   Jika injektif, maka harus injektif, tetapi tidak harus injektif. Jika surjektif, maka harus surjektif, tetapi tidak harus surjektif.   Jika , maka ; injektivitas komposit memberi , jadi injektif. Namun ambil , , , , dan . Komposit dari satu unsur ke satu unsur injektif, sedangkan tidak.  Jika komposit surjektif dan , ada dengan . Jadi mempunyai prapeta oleh , sehingga surjektif. Untuk menunjukkan bahwa tidak harus surjektif, gunakan himpunan dan fungsi yang sama: tidak mencapai , tetapi komposit mencapai satu-satunya unsur .   Latihan 14: komutativitas dan asosiativitas komposisi  Putuskan apakah komposisi komutatif dan asosiatif. Untuk klaim positif, buktikan secara titik demi titik; untuk klaim negatif, pastikan kedua urutan komposisi pada contoh Anda sama-sama terdefinisi.   Petunjuk 1. Coba endofungsi dan pada .  Petunjuk 2. Evaluasi kedua pengelompokan tiga fungsi pada unsur .   Komposisi tidak komutatif secara umum, tetapi asosiatif ketika semua komposit yang ditulis bertipe benar.   Untuk dengan dan , diperoleh , sedangkan . Jadi komposisi tidak komutatif; pada fungsi dengan domain dan kodomain berbeda, salah satu urutan bahkan mungkin tidak terdefinisi. Jika , , dan , maka bagi setiap , . Kedua fungsi mempunyai domain , kodomain , dan nilai yang sama pada setiap unsur, sehingga komposisi asosiatif.   Latihan 15: invers fungsi pada  Buat tabel lengkap bagi kedua fungsi pada , balik semua pasangan, tentukan apakah relasi inversnya fungsi, lalu rumuskan akar pangkat tiga dan invers secara eksplisit.   Petunjuk 1. Hitung pangkat perwakilan modulo .  Petunjuk 2. Pada , pemetaan pangkat tiga adalah invers bagi dirinya sendiri.   Relasi invers ialah dan bukan fungsi. Relasi invers ialah dan merupakan fungsi. Akar pangkat tiga dari berturut-turut ialah , serta .   Nilai untuk berturut-turut adalah . Membalik tabel memberi relasi pada jawaban; masukan dan pada relasi invers masing-masing mempunyai dua keluaran, sedangkan dan tidak mempunyai keluaran. Jadi relasi itu bukan fungsi .  Nilai berturut-turut ialah , suatu permutasi seluruh . Pembalikan tabel memberi relasi invers pada jawaban dan menunjukkan bahwa ia fungsi. Kubus dari ialah ; menerapkan kubus sekali lagi mengembalikan unsur semula, jadi akar pangkat tiga adalah . Dari diperoleh , sehingga , rumus yang dinyatakan.   Latihan 16: diferensiasi dan integrasi sebagai fungsi  Lengkapi seluruh bagian latihan ruang fungsi: berikan tiga contoh pada , nilai invertibilitas operator turunan, lalu buktikan bahwa operator integral yang diberikan mempunyai invers.   Petunjuk 1. Gunakan , fungsi konstan, dan fungsi linear untuk tiga contoh pertama.  Petunjuk 2. Teorema Dasar Kalkulus memberi dan .   Pada , contoh berturut-turut ialah , fungsi konstan , dan . Operator turunan surjektif tetapi tidak injektif, jadi tidak invertibel. Operator , , bijektif dengan invers , .   Fungsi kontinu tetapi tidak terdiferensialkan di , jadi berada di . Fungsi konstan mempunyai turunan kontinu tetapi nilainya di bukan nol, jadi berada di . Fungsi mempunyai turunan kontinu dan bernilai nol di , jadi berada di . Setiap fungsi kontinu adalah turunan fungsi dalam , maka surjektif. Namun dua fungsi yang berbeda sebesar konstanta mempunyai turunan sama; misalnya turunan fungsi konstan dan sama-sama nol. Jadi tidak injektif dan tidak invertibel.  Untuk , Teorema Dasar Kalkulus menyatakan bahwa mempunyai turunan kontinu , dan ; maka . Definisikan . Bagi , . Bagi , , karena . Jadi kedua komposisi adalah identitas dan .   Latihan 17: tiga belas klaim tentang citra dan prapeta  Periksa ketiga belas klaim terakhir dalam urutan sumber. Setiap klaim salah memerlukan contoh fungsi dan himpunan konkret; setiap klaim benar memerlukan sedikitnya satu rantai keanggotaan.   Petunjuk 1. Fungsi konstan pada domain dua unsur menguji klaim citra yang memerlukan injektivitas.  Petunjuk 2. Fungsi identitas pada dua unsur dan satu unsur kodomain yang tidak tercapai menguji arah inklusi prapeta dan citra.   Urutannya adalah: benar, salah, salah, benar, benar, benar, salah, benar, benar, salah, benar, salah, benar.   (a) Benar karena memberi . (b) Salah: untuk fungsi konstan dan , prapeta citra adalah seluruh domain. (c) Salah: untuk , , dan , ruas kanan kosong. (d) Benar: setiap unsur citra prapeta menurut definisi berada di . (e) Benar: citra anggota juga citra anggota . (f) Benar: memberi inklusi prapeta.  (g) Salah: untuk fungsi identitas pada , ambil dan ; prapeta tidak termuat dalam prapeta . (h) Benar: sebuah nilai berasal dari gabungan tepat ketika berasal dari sedikitnya satu bagian. (i) Benar karena, untuk setiap , jika dan hanya jika , jika dan hanya jika atau , jika dan hanya jika . (j) Salah: pada fungsi konstan , ambil dan ; citra irisan kosong, tetapi irisan citra tidak kosong. (k) Benar: syarat dan setara dengan .  (l) Salah: pada fungsi konstan yang sama, ambil dan . Ruas kiri , sedangkan . (m) Benar: berada pada prapeta tepat ketika dan , yaitu tepat ketika .   "
},
{
  "id": "o003-c90-ch02-exercise-01",
  "level": "2",
  "url": "o003-c90-ch02-exercise-guides.html#o003-c90-ch02-exercise-01",
  "type": "Pemeriksaan",
  "number": "B.17",
  "title": "Latihan 1: merancang banyaknya prapeta.",
  "body": "Latihan 1: merancang banyaknya prapeta  Periksa kelima contoh Anda pada latihan pertama. Sebuah contoh lengkap harus merupakan fungsi pada seluruh , mencapai setiap keluaran yang diklaim, dan mempunyai tepat banyak prapeta yang diminta.   Petunjuk 1. Identitas menyelesaikan kasus satu prapeta. Untuk dua prapeta, lipat setiap pasangan interval satuan berurutan ke satu interval satuan.  Petunjuk 2. Grafik mempunyai keluaran dengan tiga prapeta dan keluaran pada titik ekstrem dengan dua prapeta.   Contoh berturut-turut dapat diambil sebagai fungsi identitas; fungsi lipatan interval yang mempunyai tepat dua prapeta bagi setiap keluaran (juga memenuhi setidaknya dua ); fungsi lipatan yang sama; ; dan fungsi konstan .   Untuk kasus pertama, memberi satu prapeta bagi setiap . Untuk kasus kedua dan ketiga, bagi setiap definisikan pada dan pada . Interval-interval domain saling lepas dan menutupi . Jika , dua dan hanya dua prapetanya ialah dan . Jadi fungsi ini mempunyai tepat dua prapeta untuk setiap , dan khususnya sedikitnya dua.  Untuk kasus keempat, ambil . Keluaran mempunyai tepat tiga prapeta . Keluaran mempunyai dua prapeta berbeda: akar ganda dan akar ; faktorisasi setelah memindahkan keluaran ke ruas kiri memverifikasi bahwa tidak ada akar lain. Untuk kasus terakhir, fungsi konstan memberi tak berhingga banyak prapeta bagi unsur kodomain .  "
},
{
  "id": "o003-c90-ch02-exercise-02",
  "level": "2",
  "url": "o003-c90-ch02-exercise-guides.html#o003-c90-ch02-exercise-02",
  "type": "Pemeriksaan",
  "number": "B.18",
  "title": "Latihan 2: enam klasifikasi fungsi.",
  "body": "Latihan 2: enam klasifikasi fungsi  Klasifikasikan keenam fungsi pada latihan berjangkar dan dukung setiap keputusan dengan persamaan, tabrakan, atau unsur yang hilang.   Petunjuk 1. Untuk fungsi pecahan, selesaikan terhadap dan periksa nilai .  Petunjuk 2. Aturan kuadrat menjadi injektif setelah domain dibatasi ke bilangan tak negatif.   Berturut-turut: bijektif; injektif tetapi tidak surjektif; injektif tetapi tidak surjektif; bijektif; surjektif tetapi tidak injektif; dan bijektif.   Persamaan mempunyai solusi tunggal di , jadi bijektif. Pada , kesamaan keluaran masih memaksa kesamaan masukan, tetapi semua keluaran kongruen dengan modulo ; misalnya tidak tercapai, sehingga hanya injektif.  Jika , maka untuk satu-satunya kandidat ialah , yang tidak pernah sama dengan . Nilai mustahil karena akan memberi . Karena itu aturan pecahan injektif dengan daerah hasil : fungsi ke tidak surjektif, sedangkan fungsi ke bijektif. Akhirnya, dari ke bilangan tak negatif surjektif tetapi dan bertabrakan bila . Pada domain tak negatif, akar kuadrat memberi prapeta tunggal bagi setiap keluaran, jadi bijektif.  "
},
{
  "id": "o003-c90-ch02-exercise-03",
  "level": "2",
  "url": "o003-c90-ch02-exercise-guides.html#o003-c90-ch02-exercise-03",
  "type": "Pemeriksaan",
  "number": "B.19",
  "title": "Latihan 3: membatasi tabel fungsi.",
  "body": "Latihan 3: membatasi tabel fungsi  Gunakan tabel pada latihan ketiga untuk menilai fungsi, menemukan pembatasan injektif terbesar, menyesuaikan kodomain agar surjektif, dan menghasilkan bijeksi.   Petunjuk 1. Kelompokkan unsur domain menurut nilai .  Petunjuk 2. Pembatasan injektif boleh memilih paling banyak satu wakil dari setiap serat.   Fungsi asal bukan injeksi dan bukan surjeksi. Salah satu pembatasan injektif terbesar memakai . Kodomain surjektif yang tepat ialah . Dengan dan , pembatasan merupakan bijeksi.   Serat-serat tak kosongnya adalah , , , , dan . Jadi terdapat tabrakan, sedangkan tidak tercapai. Suatu pembatasan injektif memilih paling banyak satu unsur dari masing-masing lima serat; pilihan pada jawaban memilih tepat satu dari setiap serat, sehingga ukurannya maksimal, yaitu . Daerah hasil fungsi adalah ; memandang aturan yang sama sebagai fungsi membuatnya surjektif. Membatasi sekaligus domain ke membuat setiap unsur mempunyai tepat satu prapeta, sehingga diperoleh bijeksi.  "
},
{
  "id": "o003-c90-ch02-exercise-04",
  "level": "2",
  "url": "o003-c90-ch02-exercise-guides.html#o003-c90-ch02-exercise-04",
  "type": "Pemeriksaan",
  "number": "B.20",
  "title": "Latihan 4: subhimpunan produk dan persegi panjang.",
  "body": "Latihan 4: subhimpunan produk dan persegi panjang  Berikan satu subhimpunan berbentuk produk dan satu subhimpunan yang tidak dapat ditulis sebagai produk, dengan memakai dua unsur berbeda dari masing-masing faktor.   Petunjuk 1. Produk satu unsur dengan dua unsur memberi contoh positif.  Petunjuk 2. Dua sudut diagonal memaksa dua sudut silang jika himpunannya benar-benar produk.   Untuk dan , ambil . Sebagai contoh negatif, ambil .   Bentuk sudah secara eksplisit merupakan produk dua subhimpunan. Andaikan . Dari dua pasangan di dalam diperoleh dan . Definisi produk lalu memaksa dan berada di , padahal keduanya tidak tercantum. Kontradiksi ini membuktikan bahwa bukan produk.  "
},
{
  "id": "o003-c90-ch02-exercise-05",
  "level": "2",
  "url": "o003-c90-ch02-exercise-guides.html#o003-c90-ch02-exercise-05",
  "type": "Pemeriksaan",
  "number": "B.21",
  "title": "Latihan 5: kardinalitas berhingga dan bijeksi.",
  "body": "Latihan 5: kardinalitas berhingga dan bijeksi  Buktikan kedua arah hubungan antara dan keberadaan bijeksi untuk himpunan berhingga.   Petunjuk 1. Gunakan bijeksi pencacahan dan .  Petunjuk 2. Komposisi dengan bijeksi yang diasumsikan menghasilkan bijeksi antara dua himpunan bilangan bulat awal.   Terdapat bijeksi jika dan hanya jika .   Pilih bijeksi pencacahan dan . Jika , maka adalah bijeksi. Sebaliknya, jika bijektif, maka adalah bijeksi dari ke . Jika , fungsi itu tidak mungkin surjektif; jika , fungsi itu tidak mungkin injektif, menurut prinsip rumah merpati. Jadi satu-satunya kemungkinan ialah .  "
},
{
  "id": "o003-c90-ch02-exercise-06",
  "level": "2",
  "url": "o003-c90-ch02-exercise-guides.html#o003-c90-ch02-exercise-06",
  "type": "Pemeriksaan",
  "number": "B.22",
  "title": "Latihan 6: citra sesudah prapeta dan sebaliknya.",
  "body": "Latihan 6: citra sesudah prapeta dan sebaliknya  Lengkapi empat bagian latihan tentang dan , termasuk contoh ketat dan dua karakterisasi.   Petunjuk 1. Untuk kegagalan kesamaan pertama gunakan fungsi konstan pada domain dua unsur; untuk kegagalan kedua tambahkan unsur kodomain yang tidak tercapai.  Petunjuk 2. Pada arah balik karakterisasi injeksi, uji himpunan satu unsur.   Selalu dan , dan keduanya dapat ketat. Kesamaan kedua berlaku untuk setiap tepat ketika surjektif; kesamaan pertama berlaku untuk setiap tepat ketika injektif.   Jika , maka , sehingga . Kesamaan dapat gagal: untuk fungsi konstan dan , prapeta citranya adalah seluruh . Jika , ada dengan dan , jadi . Kesamaan dapat gagal untuk , , dan .  Jika surjektif dan , pilih dengan ; maka dan , sehingga kesamaan berlaku. Jika kesamaan berlaku untuk semua , ambil untuk memperoleh . Jika injektif dan , ada dengan , maka . Sebaliknya, andaikan kesamaan berlaku untuk semua . Jika , ambil ; maka , sehingga dan injektif.  "
},
{
  "id": "o003-c90-ch02-exercise-07",
  "level": "2",
  "url": "o003-c90-ch02-exercise-guides.html#o003-c90-ch02-exercise-07",
  "type": "Pemeriksaan",
  "number": "B.23",
  "title": "Latihan 7: fungsi dan irisan terindeks.",
  "body": "Latihan 7: fungsi dan irisan terindeks  Putuskan kedua identitas pada latihan . Jika suatu kesamaan gagal, nyatakan dan buktikan inklusi yang selalu benar serta berikan contoh tandingan terkecil yang jelas.   Petunjuk 1. Fungsi konstan pada dua unsur dapat membuat citra dua himpunan saling beririsan walaupun himpunan asalnya tidak.  Petunjuk 2. Untuk prapeta, buka kuantor untuk setiap indeks ; tidak diperlukan injektivitas.   Selalu , tetapi kesamaan dapat gagal. Sebaliknya, prapeta mempertahankan irisan secara tepat: .   Jika , ada yang berada di setiap dan memenuhi . Maka berada di setiap , sehingga inklusi berlaku. Kesamaan gagal untuk fungsi konstan dengan dan : citra irisannya kosong, sedangkan irisan citranya . Untuk prapeta, setara dengan bagi setiap , yang setara dengan bagi setiap . Dengan konvensi irisan keluarga kosong sebagai seluruh himpunan semesta yang sesuai, argumen dan inklusi pertama juga mencakup himpunan indeks kosong.  "
},
{
  "id": "o003-c90-ch02-exercise-08",
  "level": "2",
  "url": "o003-c90-ch02-exercise-guides.html#o003-c90-ch02-exercise-08",
  "type": "Pemeriksaan",
  "number": "B.24",
  "title": "Latihan 8: membatalkan bijeksi dengan inversnya.",
  "body": "Latihan 8: membatalkan bijeksi dengan inversnya  Buktikan kedua identitas pada latihan langsung dari definisi invers, dengan memperhatikan domain masing-masing identitas.   Petunjuk 1. Tetapkan dan gunakan ekuivalensi .  Petunjuk 2. Untuk arah lain, tetapkan .   dan .   Untuk , ambil . Definisi fungsi invers memberi , sehingga . Untuk , bijektivitas memberi unsur tunggal dengan . Karena itu . Identitas pertama adalah fungsi pada , sedangkan identitas kedua fungsi pada .  "
},
{
  "id": "o003-c90-ch02-exercise-09",
  "level": "2",
  "url": "o003-c90-ch02-exercise-guides.html#o003-c90-ch02-exercise-09",
  "type": "Pemeriksaan",
  "number": "B.25",
  "title": "Latihan 9: prapeta himpunan oleh komposit.",
  "body": "Latihan 9: prapeta himpunan oleh komposit  Buktikan identitas pada latihan dengan rantai ekuivalensi keanggotaan; jangan menganggap atau bijektif.   Untuk , terjemahkan berturut-turut , , dan .   .   Bagi setiap , jika dan hanya jika . Hal terakhir berlaku jika dan hanya jika , yang menurut definisi setara dengan . Karena unsur pada kedua ruas sama, himpunannya sama. Ini adalah identitas prapeta, bukan rumus invers fungsi.  "
},
{
  "id": "o003-c90-ch02-exercise-10",
  "level": "2",
  "url": "o003-c90-ch02-exercise-guides.html#o003-c90-ch02-exercise-10",
  "type": "Pemeriksaan",
  "number": "B.26",
  "title": "Latihan 10: proyeksi dan hasil kali fungsi.",
  "body": "Latihan 10: proyeksi dan hasil kali fungsi  Selesaikan keempat tugas tentang proyeksi, fungsi hasil kali, komposisinya, dan inversnya. Rubrik: rumus kandidat harus ditulis, keberadaan dan ketunggalan harus dipisahkan, dan semua kesamaan fungsi dibuktikan per unsur.   Petunjuk 1. Faktor lain yang tak kosong menyediakan koordinat pendamping untuk membuktikan proyeksi surjektif.  Petunjuk 2. Satu-satunya kandidat ialah .   Setiap surjektif. Fungsi tunggal yang diminta adalah . Hasil kali mempertahankan komposisi secara koordinat, dan jika invers ada, maka .   Untuk , pilih satu ; maka . Argumen simetris berlaku bagi . Definisikan . Proyeksi ke koordinat memberi , jadi diagram yang diminta komutatif. Sebaliknya, jika memenuhi kedua persamaan proyeksi, kedua koordinat harus sama dengan koordinat ; maka , membuktikan ketunggalan.  Pada , ruas kiri identitas komposisi bernilai , sama dengan ruas kanan. Jika adalah invers , maka komposisi mengirim ke dirinya sendiri, dan komposisi dalam urutan sebaliknya juga identitas pada . Jadi memang fungsi inversnya. Ketakosongan kedua faktor diperlukan pada bukti surjektivitas proyeksi.  "
},
{
  "id": "o003-c90-ch02-exercise-11",
  "level": "2",
  "url": "o003-c90-ch02-exercise-guides.html#o003-c90-ch02-exercise-11",
  "type": "Pemeriksaan",
  "number": "B.27",
  "title": "Latihan 11: pencacahan bilangan bulat.",
  "body": "Latihan 11: pencacahan bilangan bulat  Tentukan apakah rumus yang diberikan mendefinisikan injeksi dan surjeksi , lalu beri prapeta eksplisit untuk setiap bilangan bulat.   Petunjuk 1. Tulis atau .  Petunjuk 2. Keluaran cabang genap positif, sedangkan cabang ganjil tidak positif.   Fungsi tersebut bijektif. Secara khusus, dan untuk .   Substitusi memberi dan . Cabang genap memuat setiap bilangan bulat positif tepat sekali; cabang ganjil memuat tepat sekali. Kedua daerah hasil cabang saling lepas, jadi fungsi injektif. Untuk , prapetanya ; untuk , prapetanya . Maka setiap tercapai dan fungsi surjektif.  "
},
{
  "id": "o003-c90-ch02-exercise-12",
  "level": "2",
  "url": "o003-c90-ch02-exercise-guides.html#o003-c90-ch02-exercise-12",
  "type": "Pemeriksaan",
  "number": "B.28",
  "title": "Latihan 12: penjumlahan sebagai fungsi dua peubah.",
  "body": "Latihan 12: penjumlahan sebagai fungsi dua peubah  Nilai injektivitas dan surjektivitas fungsi , , dengan saksi konkret.   Bandingkan dengan ; untuk mencapai , gunakan pasangan .   Fungsi penjumlahan tidak injektif, tetapi surjektif.   Pasangan berbeda dan keduanya dipetakan ke , sehingga fungsi tidak injektif. Untuk setiap , pasangan berada dalam domain dan memenuhi ; karena itu fungsi surjektif.  "
},
{
  "id": "o003-c90-ch02-exercise-13",
  "level": "2",
  "url": "o003-c90-ch02-exercise-guides.html#o003-c90-ch02-exercise-13",
  "type": "Pemeriksaan",
  "number": "B.29",
  "title": "Latihan 13: sifat yang dipaksa oleh komposit.",
  "body": "Latihan 13: sifat yang dipaksa oleh komposit  Tentukan bagian mana dari injektivitas atau surjektivitas yang harus diwarisi oleh faktor-faktornya, dan sangkal klaim yang terlalu kuat dengan fungsi berhingga yang bertipe benar.   Petunjuk 1. Jika , terapkan pada kedua ruas.  Petunjuk 2. Jika setiap berbentuk , maka setiap tentu berada dalam daerah hasil .   Jika injektif, maka harus injektif, tetapi tidak harus injektif. Jika surjektif, maka harus surjektif, tetapi tidak harus surjektif.   Jika , maka ; injektivitas komposit memberi , jadi injektif. Namun ambil , , , , dan . Komposit dari satu unsur ke satu unsur injektif, sedangkan tidak.  Jika komposit surjektif dan , ada dengan . Jadi mempunyai prapeta oleh , sehingga surjektif. Untuk menunjukkan bahwa tidak harus surjektif, gunakan himpunan dan fungsi yang sama: tidak mencapai , tetapi komposit mencapai satu-satunya unsur .  "
},
{
  "id": "o003-c90-ch02-exercise-14",
  "level": "2",
  "url": "o003-c90-ch02-exercise-guides.html#o003-c90-ch02-exercise-14",
  "type": "Pemeriksaan",
  "number": "B.30",
  "title": "Latihan 14: komutativitas dan asosiativitas komposisi.",
  "body": "Latihan 14: komutativitas dan asosiativitas komposisi  Putuskan apakah komposisi komutatif dan asosiatif. Untuk klaim positif, buktikan secara titik demi titik; untuk klaim negatif, pastikan kedua urutan komposisi pada contoh Anda sama-sama terdefinisi.   Petunjuk 1. Coba endofungsi dan pada .  Petunjuk 2. Evaluasi kedua pengelompokan tiga fungsi pada unsur .   Komposisi tidak komutatif secara umum, tetapi asosiatif ketika semua komposit yang ditulis bertipe benar.   Untuk dengan dan , diperoleh , sedangkan . Jadi komposisi tidak komutatif; pada fungsi dengan domain dan kodomain berbeda, salah satu urutan bahkan mungkin tidak terdefinisi. Jika , , dan , maka bagi setiap , . Kedua fungsi mempunyai domain , kodomain , dan nilai yang sama pada setiap unsur, sehingga komposisi asosiatif.  "
},
{
  "id": "o003-c90-ch02-exercise-15",
  "level": "2",
  "url": "o003-c90-ch02-exercise-guides.html#o003-c90-ch02-exercise-15",
  "type": "Pemeriksaan",
  "number": "B.31",
  "title": "Latihan 15: invers fungsi pada <span class=\"process-math\">\\(\\Z_5\\)<\/span>.",
  "body": "Latihan 15: invers fungsi pada  Buat tabel lengkap bagi kedua fungsi pada , balik semua pasangan, tentukan apakah relasi inversnya fungsi, lalu rumuskan akar pangkat tiga dan invers secara eksplisit.   Petunjuk 1. Hitung pangkat perwakilan modulo .  Petunjuk 2. Pada , pemetaan pangkat tiga adalah invers bagi dirinya sendiri.   Relasi invers ialah dan bukan fungsi. Relasi invers ialah dan merupakan fungsi. Akar pangkat tiga dari berturut-turut ialah , serta .   Nilai untuk berturut-turut adalah . Membalik tabel memberi relasi pada jawaban; masukan dan pada relasi invers masing-masing mempunyai dua keluaran, sedangkan dan tidak mempunyai keluaran. Jadi relasi itu bukan fungsi .  Nilai berturut-turut ialah , suatu permutasi seluruh . Pembalikan tabel memberi relasi invers pada jawaban dan menunjukkan bahwa ia fungsi. Kubus dari ialah ; menerapkan kubus sekali lagi mengembalikan unsur semula, jadi akar pangkat tiga adalah . Dari diperoleh , sehingga , rumus yang dinyatakan.  "
},
{
  "id": "o003-c90-ch02-exercise-16",
  "level": "2",
  "url": "o003-c90-ch02-exercise-guides.html#o003-c90-ch02-exercise-16",
  "type": "Pemeriksaan",
  "number": "B.32",
  "title": "Latihan 16: diferensiasi dan integrasi sebagai fungsi.",
  "body": "Latihan 16: diferensiasi dan integrasi sebagai fungsi  Lengkapi seluruh bagian latihan ruang fungsi: berikan tiga contoh pada , nilai invertibilitas operator turunan, lalu buktikan bahwa operator integral yang diberikan mempunyai invers.   Petunjuk 1. Gunakan , fungsi konstan, dan fungsi linear untuk tiga contoh pertama.  Petunjuk 2. Teorema Dasar Kalkulus memberi dan .   Pada , contoh berturut-turut ialah , fungsi konstan , dan . Operator turunan surjektif tetapi tidak injektif, jadi tidak invertibel. Operator , , bijektif dengan invers , .   Fungsi kontinu tetapi tidak terdiferensialkan di , jadi berada di . Fungsi konstan mempunyai turunan kontinu tetapi nilainya di bukan nol, jadi berada di . Fungsi mempunyai turunan kontinu dan bernilai nol di , jadi berada di . Setiap fungsi kontinu adalah turunan fungsi dalam , maka surjektif. Namun dua fungsi yang berbeda sebesar konstanta mempunyai turunan sama; misalnya turunan fungsi konstan dan sama-sama nol. Jadi tidak injektif dan tidak invertibel.  Untuk , Teorema Dasar Kalkulus menyatakan bahwa mempunyai turunan kontinu , dan ; maka . Definisikan . Bagi , . Bagi , , karena . Jadi kedua komposisi adalah identitas dan .  "
},
{
  "id": "o003-c90-ch02-exercise-17",
  "level": "2",
  "url": "o003-c90-ch02-exercise-guides.html#o003-c90-ch02-exercise-17",
  "type": "Pemeriksaan",
  "number": "B.33",
  "title": "Latihan 17: tiga belas klaim tentang citra dan prapeta.",
  "body": "Latihan 17: tiga belas klaim tentang citra dan prapeta  Periksa ketiga belas klaim terakhir dalam urutan sumber. Setiap klaim salah memerlukan contoh fungsi dan himpunan konkret; setiap klaim benar memerlukan sedikitnya satu rantai keanggotaan.   Petunjuk 1. Fungsi konstan pada domain dua unsur menguji klaim citra yang memerlukan injektivitas.  Petunjuk 2. Fungsi identitas pada dua unsur dan satu unsur kodomain yang tidak tercapai menguji arah inklusi prapeta dan citra.   Urutannya adalah: benar, salah, salah, benar, benar, benar, salah, benar, benar, salah, benar, salah, benar.   (a) Benar karena memberi . (b) Salah: untuk fungsi konstan dan , prapeta citra adalah seluruh domain. (c) Salah: untuk , , dan , ruas kanan kosong. (d) Benar: setiap unsur citra prapeta menurut definisi berada di . (e) Benar: citra anggota juga citra anggota . (f) Benar: memberi inklusi prapeta.  (g) Salah: untuk fungsi identitas pada , ambil dan ; prapeta tidak termuat dalam prapeta . (h) Benar: sebuah nilai berasal dari gabungan tepat ketika berasal dari sedikitnya satu bagian. (i) Benar karena, untuk setiap , jika dan hanya jika , jika dan hanya jika atau , jika dan hanya jika . (j) Salah: pada fungsi konstan , ambil dan ; citra irisan kosong, tetapi irisan citra tidak kosong. (k) Benar: syarat dan setara dengan .  (l) Salah: pada fungsi konstan yang sama, ambil dan . Ruas kiri , sedangkan . (m) Benar: berada pada prapeta tepat ketika dan , yaitu tepat ketika .  "
},
{
  "id": "o003-c90-ch03-activity-checkpoints",
  "level": "1",
  "url": "o003-c90-ch03-activity-checkpoints.html",
  "type": "Bagian",
  "number": "",
  "title": "Pemeriksaan eksplorasi dan aktivitas",
  "body": " Pemeriksaan eksplorasi dan aktivitas  Pemeriksaan 1: metrik taksi  Audit kelima tugas eksplorasi pembuka: buktikan empat aksioma untuk pada , lalu tentukan lingkaran satuannya dalam koordinat Euklides. Rubrik lengkap: setiap aksioma harus dinyatakan; bukti pertidaksamaan segitiga harus berlaku koordinat demi koordinat; gambar lingkaran harus disertai persamaan atau pertidaksamaan yang menjelaskan keempat sisinya.   Petunjuk 1. Gunakan pada masing-masing selisih koordinat.  Petunjuk 2. Lingkaran satuan memenuhi .   Fungsi merupakan metrik. Lingkaran satuannya adalah , yakni persegi yang tampak sebagai belah ketupat dengan titik sudut , , , dan dalam gambar Euklides.   Nilai mutlak tak negatif, jadi . Jumlah dua nilai mutlak bernilai nol tepat ketika kedua selisih koordinat nol, yaitu tepat ketika . Karena , fungsi ini simetris. Untuk titik ketiga , tulis . Ketaksamaan nilai mutlak memberi untuk . Menjumlahkan kedua pertidaksamaan menghasilkan .  Jarak titik dari asal ialah . Pada setiap kuadran, persamaan menjadi sebuah ruas garis; keempat ruas bertemu pada empat titik sudut yang dinyatakan pada jawaban.   Pemeriksaan 2: empat calon ruang metrik  Periksa seluruh butir pada aktivitas . Rubrik: untuk calon yang gagal, berikan aksioma dan titik konkret yang gagal; untuk calon yang berhasil, buktikan semua aksioma yang belum langsung; deskripsikan lingkaran satuan relatif terhadap unsur nol.   Petunjuk 1. Uji pada calon pertama.  Petunjuk 2. Untuk integral, gunakan pertidaksamaan segitiga titik demi titik dan kekontinuan .   Calon (a) bukan metrik karena . Calon (b) adalah metrik diskret dan lingkaran satuan berpusat di ialah . Calon (c) adalah metrik maksimum; lingkaran satuannya ialah batas persegi . Calon (d) adalah metrik pada ; lingkaran satuannya terdiri atas fungsi kontinu dengan .   Pada (a), aksioma identitas titik sudah gagal: jarak suatu titik dari dirinya seharusnya nol. Pada (b), nilai hanya atau ; identitas dan simetri langsung, dan jika , sedikitnya satu dari dan bernilai , sehingga pertidaksamaan segitiga berlaku. Jarak dari nol sama dengan satu tepat bagi semua titik bukan nol.  Pada (c), tak-negatif, identitas, dan simetri mengikuti nilai mutlak. Untuk tiap koordinat, ; mengambil maksimum atas membuktikan aksioma keempat. Pada (d), integral tak negatif dan simetris. Jika integral nol, fungsi kontinu tak negatif tidak dapat positif di satu titik tanpa positif pada suatu interval; jadi . Ketaksamaan yang diintegralkan memberi pertidaksamaan segitiga. Deskripsi lingkaran mengikuti dengan mengambil jarak dari fungsi nol.   Pemeriksaan 3: tiga aksioma pertama metrik Euklides  Lengkapi empat tugas aktivitas pertama pada bagian metrik Euklides di . Rubrik: jelaskan mengapa akar kuadrat terdefinisi, buktikan kedua arah dari syarat jarak nol, dan jangan memakai gambar sebagai bukti.   Petunjuk. Jumlah kuadrat tak negatif, dan jumlah bilangan tak negatif bernilai nol tepat ketika setiap sukunya nol.   Untuk semua , berlaku , , dan tepat ketika .   Setiap tak negatif, sehingga jumlahnya dan akar kuadratnya tak negatif. Karena untuk setiap , menukar dan tidak mengubah jarak. Jika , semua selisih nol dan jaraknya nol. Sebaliknya, jika jaraknya nol, maka . Semua suku tak negatif, jadi setiap suku nol; maka untuk seluruh , yakni .   Pemeriksaan 4: dua uji numerik Cauchy–Schwarz  Hitung kedua ruas Pertidaksamaan Cauchy–Schwarz pada dua pasangan vektor dalam aktivitas. Rubrik: tampilkan hasil kali titik, kedua norma, dan perbandingan numeriknya.   Petunjuk. Ruas kiri adalah ; ruas kanan adalah .   Untuk dan , diperoleh . Untuk dan , diperoleh .   Pada pasangan pertama, hasil kali titiknya . Kuadrat normanya masing-masing dan , sehingga ruas kanan ; karena , perbandingan berlaku. Pada pasangan kedua, hasil kali titiknya , sedangkan kuadrat normanya dan . Jadi ruas kanan positif dan jelas lebih besar daripada . Bentuk standar dengan nilai mutlak juga terpenuhi karena .   Pemeriksaan 5: dua uji numerik pertidaksamaan jumlah  Verifikasikan akibat Cauchy–Schwarz pada dua pasangan vektor yang diberikan. Rubrik: hitung norma jumlah serta jumlah kedua norma tanpa membulatkan akar.   Petunjuk. Hitung terlebih dahulu, lalu kuadratkan kedua ruas jika perlu.   Pasangan pertama memberi . Pasangan kedua memberi .   Untuk dan , jumlahnya , sehingga normanya ; norma masing-masing vektor adalah dan . Setelah mengurangi , cukup memeriksa . Untuk pasangan kedua, jumlahnya dengan norma , sedangkan jumlah norma awal ialah . Menguadratkan ruas kanan menghasilkan , jadi pertidaksamaan berlaku.   Pemeriksaan 6: pertidaksamaan segitiga Euklides  Lengkapi aktivitas terakhir pada bagian Euklides dengan menurunkan langsung dari . Rubrik: vektor yang dimasukkan ke akibat harus disebutkan dan jumlahnya harus disederhanakan menjadi .   Petunjuk. Ambil dan .   Terapkan pada dan ; karena , hasilnya tepat pertidaksamaan segitiga bagi .   Notasi norma Euklides memberi . Dengan dan , akibat Cauchy–Schwarz menyatakan . Karena , ruas kiri ialah , sedangkan dua suku ruas kanan ialah dan . Jadi aksioma keempat terbukti untuk semua .   "
},
{
  "id": "o003-c90-ch03-checkpoint-01",
  "level": "2",
  "url": "o003-c90-ch03-activity-checkpoints.html#o003-c90-ch03-checkpoint-01",
  "type": "Pemeriksaan",
  "number": "C.1",
  "title": "Pemeriksaan 1: metrik taksi.",
  "body": "Pemeriksaan 1: metrik taksi  Audit kelima tugas eksplorasi pembuka: buktikan empat aksioma untuk pada , lalu tentukan lingkaran satuannya dalam koordinat Euklides. Rubrik lengkap: setiap aksioma harus dinyatakan; bukti pertidaksamaan segitiga harus berlaku koordinat demi koordinat; gambar lingkaran harus disertai persamaan atau pertidaksamaan yang menjelaskan keempat sisinya.   Petunjuk 1. Gunakan pada masing-masing selisih koordinat.  Petunjuk 2. Lingkaran satuan memenuhi .   Fungsi merupakan metrik. Lingkaran satuannya adalah , yakni persegi yang tampak sebagai belah ketupat dengan titik sudut , , , dan dalam gambar Euklides.   Nilai mutlak tak negatif, jadi . Jumlah dua nilai mutlak bernilai nol tepat ketika kedua selisih koordinat nol, yaitu tepat ketika . Karena , fungsi ini simetris. Untuk titik ketiga , tulis . Ketaksamaan nilai mutlak memberi untuk . Menjumlahkan kedua pertidaksamaan menghasilkan .  Jarak titik dari asal ialah . Pada setiap kuadran, persamaan menjadi sebuah ruas garis; keempat ruas bertemu pada empat titik sudut yang dinyatakan pada jawaban.  "
},
{
  "id": "o003-c90-ch03-checkpoint-02",
  "level": "2",
  "url": "o003-c90-ch03-activity-checkpoints.html#o003-c90-ch03-checkpoint-02",
  "type": "Pemeriksaan",
  "number": "C.2",
  "title": "Pemeriksaan 2: empat calon ruang metrik.",
  "body": "Pemeriksaan 2: empat calon ruang metrik  Periksa seluruh butir pada aktivitas . Rubrik: untuk calon yang gagal, berikan aksioma dan titik konkret yang gagal; untuk calon yang berhasil, buktikan semua aksioma yang belum langsung; deskripsikan lingkaran satuan relatif terhadap unsur nol.   Petunjuk 1. Uji pada calon pertama.  Petunjuk 2. Untuk integral, gunakan pertidaksamaan segitiga titik demi titik dan kekontinuan .   Calon (a) bukan metrik karena . Calon (b) adalah metrik diskret dan lingkaran satuan berpusat di ialah . Calon (c) adalah metrik maksimum; lingkaran satuannya ialah batas persegi . Calon (d) adalah metrik pada ; lingkaran satuannya terdiri atas fungsi kontinu dengan .   Pada (a), aksioma identitas titik sudah gagal: jarak suatu titik dari dirinya seharusnya nol. Pada (b), nilai hanya atau ; identitas dan simetri langsung, dan jika , sedikitnya satu dari dan bernilai , sehingga pertidaksamaan segitiga berlaku. Jarak dari nol sama dengan satu tepat bagi semua titik bukan nol.  Pada (c), tak-negatif, identitas, dan simetri mengikuti nilai mutlak. Untuk tiap koordinat, ; mengambil maksimum atas membuktikan aksioma keempat. Pada (d), integral tak negatif dan simetris. Jika integral nol, fungsi kontinu tak negatif tidak dapat positif di satu titik tanpa positif pada suatu interval; jadi . Ketaksamaan yang diintegralkan memberi pertidaksamaan segitiga. Deskripsi lingkaran mengikuti dengan mengambil jarak dari fungsi nol.  "
},
{
  "id": "o003-c90-ch03-checkpoint-03",
  "level": "2",
  "url": "o003-c90-ch03-activity-checkpoints.html#o003-c90-ch03-checkpoint-03",
  "type": "Pemeriksaan",
  "number": "C.3",
  "title": "Pemeriksaan 3: tiga aksioma pertama metrik Euklides.",
  "body": "Pemeriksaan 3: tiga aksioma pertama metrik Euklides  Lengkapi empat tugas aktivitas pertama pada bagian metrik Euklides di . Rubrik: jelaskan mengapa akar kuadrat terdefinisi, buktikan kedua arah dari syarat jarak nol, dan jangan memakai gambar sebagai bukti.   Petunjuk. Jumlah kuadrat tak negatif, dan jumlah bilangan tak negatif bernilai nol tepat ketika setiap sukunya nol.   Untuk semua , berlaku , , dan tepat ketika .   Setiap tak negatif, sehingga jumlahnya dan akar kuadratnya tak negatif. Karena untuk setiap , menukar dan tidak mengubah jarak. Jika , semua selisih nol dan jaraknya nol. Sebaliknya, jika jaraknya nol, maka . Semua suku tak negatif, jadi setiap suku nol; maka untuk seluruh , yakni .  "
},
{
  "id": "o003-c90-ch03-checkpoint-04",
  "level": "2",
  "url": "o003-c90-ch03-activity-checkpoints.html#o003-c90-ch03-checkpoint-04",
  "type": "Pemeriksaan",
  "number": "C.4",
  "title": "Pemeriksaan 4: dua uji numerik Cauchy–Schwarz.",
  "body": "Pemeriksaan 4: dua uji numerik Cauchy–Schwarz  Hitung kedua ruas Pertidaksamaan Cauchy–Schwarz pada dua pasangan vektor dalam aktivitas. Rubrik: tampilkan hasil kali titik, kedua norma, dan perbandingan numeriknya.   Petunjuk. Ruas kiri adalah ; ruas kanan adalah .   Untuk dan , diperoleh . Untuk dan , diperoleh .   Pada pasangan pertama, hasil kali titiknya . Kuadrat normanya masing-masing dan , sehingga ruas kanan ; karena , perbandingan berlaku. Pada pasangan kedua, hasil kali titiknya , sedangkan kuadrat normanya dan . Jadi ruas kanan positif dan jelas lebih besar daripada . Bentuk standar dengan nilai mutlak juga terpenuhi karena .  "
},
{
  "id": "o003-c90-ch03-checkpoint-05",
  "level": "2",
  "url": "o003-c90-ch03-activity-checkpoints.html#o003-c90-ch03-checkpoint-05",
  "type": "Pemeriksaan",
  "number": "C.5",
  "title": "Pemeriksaan 5: dua uji numerik pertidaksamaan jumlah.",
  "body": "Pemeriksaan 5: dua uji numerik pertidaksamaan jumlah  Verifikasikan akibat Cauchy–Schwarz pada dua pasangan vektor yang diberikan. Rubrik: hitung norma jumlah serta jumlah kedua norma tanpa membulatkan akar.   Petunjuk. Hitung terlebih dahulu, lalu kuadratkan kedua ruas jika perlu.   Pasangan pertama memberi . Pasangan kedua memberi .   Untuk dan , jumlahnya , sehingga normanya ; norma masing-masing vektor adalah dan . Setelah mengurangi , cukup memeriksa . Untuk pasangan kedua, jumlahnya dengan norma , sedangkan jumlah norma awal ialah . Menguadratkan ruas kanan menghasilkan , jadi pertidaksamaan berlaku.  "
},
{
  "id": "o003-c90-ch03-checkpoint-06",
  "level": "2",
  "url": "o003-c90-ch03-activity-checkpoints.html#o003-c90-ch03-checkpoint-06",
  "type": "Pemeriksaan",
  "number": "C.6",
  "title": "Pemeriksaan 6: pertidaksamaan segitiga Euklides.",
  "body": "Pemeriksaan 6: pertidaksamaan segitiga Euklides  Lengkapi aktivitas terakhir pada bagian Euklides dengan menurunkan langsung dari . Rubrik: vektor yang dimasukkan ke akibat harus disebutkan dan jumlahnya harus disederhanakan menjadi .   Petunjuk. Ambil dan .   Terapkan pada dan ; karena , hasilnya tepat pertidaksamaan segitiga bagi .   Notasi norma Euklides memberi . Dengan dan , akibat Cauchy–Schwarz menyatakan . Karena , ruas kiri ialah , sedangkan dua suku ruas kanan ialah dan . Jadi aksioma keempat terbukti untuk semua .  "
},
{
  "id": "o003-c90-ch03-mastery",
  "level": "1",
  "url": "o003-c90-ch03-mastery.html",
  "type": "Bagian",
  "number": "",
  "title": "Uji penguasaan",
  "body": " Uji penguasaan  Delapan butir berikut merupakan materi asli pendamping. Kerjakan tanpa membuka petunjuk terlebih dahulu; gunakan pembahasan untuk mengaudit setiap langkah, bukan hanya hasil akhir.  Penguasaan 1: jarak yang dikuadratkan  Pada , tentukan apakah merupakan metrik. Jika tidak, identifikasi aksioma yang gagal dengan contoh terkecil yang wajar.   Petunjuk. Bandingkan jarak dari ke dengan lintasan melalui .   Bukan metrik; pertidaksamaan segitiga gagal pada titik .   Fungsi ini tak negatif, simetris, dan bernilai nol tepat pada diagonal. Namun , sedangkan . Karena , aksioma pertidaksamaan segitiga gagal. Contoh ini juga menunjukkan mengapa memeriksa tiga aksioma pertama saja tidak cukup.   Penguasaan 2: membandingkan tiga metrik pada  Buktikan bahwa untuk setiap , . Nyatakan akibatnya bagi bola terbuka yang berpusat sama dan berjari-jari .   Petunjuk 1. Setiap suku maksimum tidak melebihi akar jumlah kuadrat.  Petunjuk 2. Terapkan Cauchy–Schwarz pada vektor dan .   Rantai pertidaksamaan berlaku. Karena jarak yang lebih besar menghasilkan bola berjari-jari sama yang lebih kecil, , dan .   Tuliskan . Karena , diperoleh . Karena , diperoleh . Cauchy–Schwarz memberi .  Jika , maka , lalu ; ini memberi tiga inklusi pertama. Jika , maka , memberi inklusi terakhir.   Penguasaan 3: semua bola pada metrik diskret  Misalkan himpunan tak kosong dengan metrik diskret dan . Tentukan untuk setiap .   Petunjuk. Satu-satunya nilai jarak adalah dan ; perhatikan ketegasan tanda .   untuk , dan untuk .   Titik pusat selalu masuk karena . Setiap mempunyai jarak dari . Jika , syarat gagal, termasuk pada ; jadi hanya pusat yang masuk. Jika , kedua nilai jarak lebih kecil dari , sehingga seluruh masuk.   Penguasaan 4: metrik lintasan terpendek  Pada graf berbobot , hitung dan . Berikan satu verifikasi eksplisit pertidaksamaan segitiga yang melibatkan , , dan .   Petunjuk. Daftarkan lintasan pendek melalui dan bandingkan dengan sisi atau lintasan lain.   dan ; misalnya .   Lintasan berbobot . Semua alternatif yang tampak lebih pendek gagal: sisi melalui memberi sedikitnya , dan melalui memberi ; jadi . Dari ke , lintasan dan masing-masing berbobot dan ; lintasan melalui berbobot , jadi jarak terpendeknya . Untuk ketiga titik yang diminta, dan , sehingga .   Penguasaan 5: menarik kembali metrik melalui injeksi  Misalkan ruang metrik dan injektif. Buktikan bahwa mendefinisikan metrik pada . Jelaskan tepat di mana injektivitas dipakai.   Petunjuk. Tiga aksioma diwarisi langsung; untuk jarak nol, ubah kesamaan citra menjadi kesamaan masukan.   Fungsi merupakan metrik. Injektivitas diperlukan pada arah .   Tak-negatif dan simetri mengikuti sifat . Jika , jelas . Sebaliknya, jarak nol memberi menurut identitas titik di ; injektivitas lalu memberi . Untuk , , yang tepat merupakan pertidaksamaan segitiga bagi . Tanpa injektivitas, dua masukan berbeda yang mempunyai citra sama akan berjarak nol.   Penguasaan 6: maksimum dua metrik  Jika dan adalah metrik pada himpunan yang sama , buktikan bahwa juga metrik.   Petunjuk. Untuk setiap , batasi dengan jumlah yang suku-sukunya masing-masing tidak melebihi .   merupakan metrik pada .   Maksimum dua bilangan tak negatif tak negatif dan simetris. Nilai nol tepat ketika kedua nol, dan karena keduanya metrik, hal itu tepat ketika . Untuk , . Kedua calon di dalam maksimum dibatasi oleh ruas kanan yang sama; mengambil maksimumnya memberi .   Penguasaan 7: penskalaan tidak mengubah bola secara hakiki  Misalkan metrik dan . Buktikan bahwa . Simpulkan bahwa kedua metrik menentukan keluarga himpunan terbuka yang sama ketika konsep itu diperkenalkan nanti.   Petunjuk. Bagi pertidaksamaan dengan bilangan positif .   Kedua bola sama karena tepat ketika . Jadi penskalaan positif hanya mengganti label jari-jari.   Untuk titik sembarang , jika dan hanya jika . Karena , pembagian tidak membalik tanda, sehingga syarat ini setara dengan , yakni . Setiap bola bagi satu metrik dengan demikian merupakan bola bagi metrik lain; gabungan bola yang kelak mendefinisikan himpunan terbuka juga sama.   Penguasaan 8: membangun tak berhingga banyak metrik  Misalkan mempunyai sedikitnya dua unsur. Bangun tak berhingga banyak metrik yang berbeda pada , dan buktikan bahwa metrik-metrik tersebut memang berbeda sebagai fungsi.   Petunjuk. Kalikan metrik diskret dengan konstanta positif yang berbeda.   Untuk setiap , fungsi jika dan jika merupakan metrik; nilai yang berbeda menghasilkan fungsi yang berbeda.   Tak-negatif, identitas, dan simetri langsung. Jika , pertidaksamaan segitiga seketika. Jika , tidak mungkin sekaligus dan ; sedikitnya satu jarak pada ruas kanan bernilai , sehingga . Pilih dua unsur berbeda . Untuk , , jadi metriknya berbeda. Karena ada tak berhingga banyak bilangan real positif, diperoleh tak berhingga banyak metrik.   "
},
{
  "id": "o003-c90-ch03-mastery-01",
  "level": "2",
  "url": "o003-c90-ch03-mastery.html#o003-c90-ch03-mastery-01",
  "type": "Pemeriksaan",
  "number": "C.7",
  "title": "Penguasaan 1: jarak yang dikuadratkan.",
  "body": "Penguasaan 1: jarak yang dikuadratkan  Pada , tentukan apakah merupakan metrik. Jika tidak, identifikasi aksioma yang gagal dengan contoh terkecil yang wajar.   Petunjuk. Bandingkan jarak dari ke dengan lintasan melalui .   Bukan metrik; pertidaksamaan segitiga gagal pada titik .   Fungsi ini tak negatif, simetris, dan bernilai nol tepat pada diagonal. Namun , sedangkan . Karena , aksioma pertidaksamaan segitiga gagal. Contoh ini juga menunjukkan mengapa memeriksa tiga aksioma pertama saja tidak cukup.  "
},
{
  "id": "o003-c90-ch03-mastery-02",
  "level": "2",
  "url": "o003-c90-ch03-mastery.html#o003-c90-ch03-mastery-02",
  "type": "Pemeriksaan",
  "number": "C.8",
  "title": "Penguasaan 2: membandingkan tiga metrik pada <span class=\"process-math\">\\(\\R^n\\)<\/span>.",
  "body": "Penguasaan 2: membandingkan tiga metrik pada  Buktikan bahwa untuk setiap , . Nyatakan akibatnya bagi bola terbuka yang berpusat sama dan berjari-jari .   Petunjuk 1. Setiap suku maksimum tidak melebihi akar jumlah kuadrat.  Petunjuk 2. Terapkan Cauchy–Schwarz pada vektor dan .   Rantai pertidaksamaan berlaku. Karena jarak yang lebih besar menghasilkan bola berjari-jari sama yang lebih kecil, , dan .   Tuliskan . Karena , diperoleh . Karena , diperoleh . Cauchy–Schwarz memberi .  Jika , maka , lalu ; ini memberi tiga inklusi pertama. Jika , maka , memberi inklusi terakhir.  "
},
{
  "id": "o003-c90-ch03-mastery-03",
  "level": "2",
  "url": "o003-c90-ch03-mastery.html#o003-c90-ch03-mastery-03",
  "type": "Pemeriksaan",
  "number": "C.9",
  "title": "Penguasaan 3: semua bola pada metrik diskret.",
  "body": "Penguasaan 3: semua bola pada metrik diskret  Misalkan himpunan tak kosong dengan metrik diskret dan . Tentukan untuk setiap .   Petunjuk. Satu-satunya nilai jarak adalah dan ; perhatikan ketegasan tanda .   untuk , dan untuk .   Titik pusat selalu masuk karena . Setiap mempunyai jarak dari . Jika , syarat gagal, termasuk pada ; jadi hanya pusat yang masuk. Jika , kedua nilai jarak lebih kecil dari , sehingga seluruh masuk.  "
},
{
  "id": "o003-c90-ch03-mastery-04",
  "level": "2",
  "url": "o003-c90-ch03-mastery.html#o003-c90-ch03-mastery-04",
  "type": "Pemeriksaan",
  "number": "C.10",
  "title": "Penguasaan 4: metrik lintasan terpendek.",
  "body": "Penguasaan 4: metrik lintasan terpendek  Pada graf berbobot , hitung dan . Berikan satu verifikasi eksplisit pertidaksamaan segitiga yang melibatkan , , dan .   Petunjuk. Daftarkan lintasan pendek melalui dan bandingkan dengan sisi atau lintasan lain.   dan ; misalnya .   Lintasan berbobot . Semua alternatif yang tampak lebih pendek gagal: sisi melalui memberi sedikitnya , dan melalui memberi ; jadi . Dari ke , lintasan dan masing-masing berbobot dan ; lintasan melalui berbobot , jadi jarak terpendeknya . Untuk ketiga titik yang diminta, dan , sehingga .  "
},
{
  "id": "o003-c90-ch03-mastery-05",
  "level": "2",
  "url": "o003-c90-ch03-mastery.html#o003-c90-ch03-mastery-05",
  "type": "Pemeriksaan",
  "number": "C.11",
  "title": "Penguasaan 5: menarik kembali metrik melalui injeksi.",
  "body": "Penguasaan 5: menarik kembali metrik melalui injeksi  Misalkan ruang metrik dan injektif. Buktikan bahwa mendefinisikan metrik pada . Jelaskan tepat di mana injektivitas dipakai.   Petunjuk. Tiga aksioma diwarisi langsung; untuk jarak nol, ubah kesamaan citra menjadi kesamaan masukan.   Fungsi merupakan metrik. Injektivitas diperlukan pada arah .   Tak-negatif dan simetri mengikuti sifat . Jika , jelas . Sebaliknya, jarak nol memberi menurut identitas titik di ; injektivitas lalu memberi . Untuk , , yang tepat merupakan pertidaksamaan segitiga bagi . Tanpa injektivitas, dua masukan berbeda yang mempunyai citra sama akan berjarak nol.  "
},
{
  "id": "o003-c90-ch03-mastery-06",
  "level": "2",
  "url": "o003-c90-ch03-mastery.html#o003-c90-ch03-mastery-06",
  "type": "Pemeriksaan",
  "number": "C.12",
  "title": "Penguasaan 6: maksimum dua metrik.",
  "body": "Penguasaan 6: maksimum dua metrik  Jika dan adalah metrik pada himpunan yang sama , buktikan bahwa juga metrik.   Petunjuk. Untuk setiap , batasi dengan jumlah yang suku-sukunya masing-masing tidak melebihi .   merupakan metrik pada .   Maksimum dua bilangan tak negatif tak negatif dan simetris. Nilai nol tepat ketika kedua nol, dan karena keduanya metrik, hal itu tepat ketika . Untuk , . Kedua calon di dalam maksimum dibatasi oleh ruas kanan yang sama; mengambil maksimumnya memberi .  "
},
{
  "id": "o003-c90-ch03-mastery-07",
  "level": "2",
  "url": "o003-c90-ch03-mastery.html#o003-c90-ch03-mastery-07",
  "type": "Pemeriksaan",
  "number": "C.13",
  "title": "Penguasaan 7: penskalaan tidak mengubah bola secara hakiki.",
  "body": "Penguasaan 7: penskalaan tidak mengubah bola secara hakiki  Misalkan metrik dan . Buktikan bahwa . Simpulkan bahwa kedua metrik menentukan keluarga himpunan terbuka yang sama ketika konsep itu diperkenalkan nanti.   Petunjuk. Bagi pertidaksamaan dengan bilangan positif .   Kedua bola sama karena tepat ketika . Jadi penskalaan positif hanya mengganti label jari-jari.   Untuk titik sembarang , jika dan hanya jika . Karena , pembagian tidak membalik tanda, sehingga syarat ini setara dengan , yakni . Setiap bola bagi satu metrik dengan demikian merupakan bola bagi metrik lain; gabungan bola yang kelak mendefinisikan himpunan terbuka juga sama.  "
},
{
  "id": "o003-c90-ch03-mastery-08",
  "level": "2",
  "url": "o003-c90-ch03-mastery.html#o003-c90-ch03-mastery-08",
  "type": "Pemeriksaan",
  "number": "C.14",
  "title": "Penguasaan 8: membangun tak berhingga banyak metrik.",
  "body": "Penguasaan 8: membangun tak berhingga banyak metrik  Misalkan mempunyai sedikitnya dua unsur. Bangun tak berhingga banyak metrik yang berbeda pada , dan buktikan bahwa metrik-metrik tersebut memang berbeda sebagai fungsi.   Petunjuk. Kalikan metrik diskret dengan konstanta positif yang berbeda.   Untuk setiap , fungsi jika dan jika merupakan metrik; nilai yang berbeda menghasilkan fungsi yang berbeda.   Tak-negatif, identitas, dan simetri langsung. Jika , pertidaksamaan segitiga seketika. Jika , tidak mungkin sekaligus dan ; sedikitnya satu jarak pada ruas kanan bernilai , sehingga . Pilih dua unsur berbeda . Untuk , , jadi metriknya berbeda. Karena ada tak berhingga banyak bilangan real positif, diperoleh tak berhingga banyak metrik.  "
},
{
  "id": "o003-c90-ch03-diagnostics",
  "level": "1",
  "url": "o003-c90-ch03-diagnostics.html",
  "type": "Bagian",
  "number": "",
  "title": "Diagnostik kesalahan ringkas",
  "body": " Diagnostik kesalahan ringkas    Memeriksa hanya tiga aksioma Calon jarak yang tak negatif, simetris, dan nol pada diagonal masih dapat gagal pada pertidaksamaan segitiga.  Mengabaikan domain Rumus yang sama dapat menjadi metrik pada satu himpunan dan gagal atau bahkan tidak terdefinisi pada himpunan lain.  Menggambar bola dengan geometri yang salah Bola selalu ditentukan oleh metrik yang sedang dipakai; bentuk Euklidesnya dapat berupa lingkaran, belah ketupat, persegi, ruas, atau himpunan lain.  Mengganti “kurang dari” dengan “kurang dari atau sama dengan” Bola terbuka memakai syarat tegas ; titik pada batas tidak termasuk.  Menganggap representasi rasional tidak penting Pada metrik pembilang-penyebut, gunakan bentuk paling sederhana dengan penyebut positif sebelum menghitung jarak.  Membagi dengan koefisien yang mungkin nol Dalam bukti Cauchy–Schwarz, pisahkan kasus vektor nol sebelum memakai rumus kuadrat dengan koefisien utama .  Membuktikan hasil kali jarak dengan gambar Untuk metrik maksimum pada produk, buktikan pertidaksamaan koordinat demi koordinat lalu ambil maksimum.  Menggunakan petunjuk pecahan pada kasus nol Jika petunjuk memakai , tangani lebih dahulu.    "
},
{
  "id": "o003-c90-ch03-exercise-guides",
  "level": "1",
  "url": "o003-c90-ch03-exercise-guides.html",
  "type": "Bagian",
  "number": "",
  "title": "Panduan dan pembahasan empat belas latihan",
  "body": " Panduan dan pembahasan empat belas latihan  Nomor panduan mengikuti urutan empat belas latihan pada bagian akhir Bab 3. Setiap panduan mempertahankan persoalan sumber, tetapi penyelesaiannya merupakan uraian asli pendamping ini.  Latihan 1: metrik diskret  Buktikan latihan dengan memeriksa keempat aksioma.   Petunjuk. Dalam pertidaksamaan segitiga, pisahkan kasus dan .   Fungsi nol-satu yang diberikan merupakan metrik pada setiap himpunan .   Nilainya atau , jadi tak negatif. Menurut definisi, tepat ketika , dan kondisi kesamaan tidak berubah ketika urutan titik dibalik, sehingga simetri berlaku. Jika , ruas kiri pertidaksamaan segitiga nol. Jika , sedikitnya satu dari atau harus berlaku; maka sedikitnya satu suku ruas kanan bernilai . Jadi .   Latihan 2: metrik modular pada tiga titik  Selesaikan kedua nilai pada . Untuk nilai yang menghasilkan metrik, klasifikasikan semua bola terbuka berpusat di menurut jari-jarinya.   Petunjuk 1. Buat tabel simetris untuk pasangan .  Petunjuk 2. Pada , tiga jarak antartitik adalah .   Untuk , fungsi bukan metrik karena . Untuk , fungsi merupakan metrik. Dalam kasus ini, untuk , untuk , dan untuk .   Modulo , nilai diagonal semuanya nol, tetapi juga bersisa nol; identitas titik gagal. Modulo , tabel jaraknya ialah , , , nilai diagonal nol, dan tabel simetris. Ketiga pertidaksamaan tak trivial adalah , , dan ; semuanya benar, jadi fungsi merupakan metrik.  Jarak dari pusat ke berturut-turut . Karena bola terbuka memakai tanda tegas, titik baru masuk ketika dan titik baru masuk ketika , yang menghasilkan tiga kasus pada jawaban.   Latihan 3: metrik pembilang–penyebut pada  Selesaikan ketiga tugas pada : buktikan metriknya, tentukan bola terbuka berpusat di berjari-jari , dan tentukan titik yang berada di antara dan .   Petunjuk 1. Petakan pecahan paling sederhana ke pasangan dan gunakan metrik maksimum.  Petunjuk 2. Semua jarak yang muncul adalah bilangan bulat tak negatif.   Fungsi merupakan metrik. Bola hanya memuat . Titik-titik yang berada di antara dan hanyalah kedua titik ujung tersebut.   Representasi paling sederhana dengan penyebut positif bersifat tunggal, sehingga peta injektif. Rumus adalah pembatasan metrik maksimum pada ke citra ; karena itu keempat aksioma diwarisi. Secara langsung, pertidaksamaan segitiga mengikuti dari dan ketaksamaan yang sama bagi penyebut, lalu mengambil maksimum.  Jarak antardua representasi merupakan maksimum dua bilangan bulat. Syarat jarak kurang dari memaksa kedua selisih nol, jadi bola hanya memuat pusat. Selanjutnya . Jika berada di antara keduanya, dua jarak bilangan bulat tak negatif harus berjumlah ; salah satunya nol. Maka sama dengan salah satu titik ujung. Kedua ujung memang memenuhi definisi betweenness.   Latihan 4: betweenness yang berbeda pada  Pada latihan keempat dalam urutan sumber, tentukan semua titik di antara dan , bandingkan jarak dan dari , lalu tentukan semua titik di antara dan .   Petunjuk. Untuk kasus terakhir, jarak total ialah ; periksa kemungkinan , , dan .   Di antara dan hanya ada dan . Titik lebih dekat ke daripada . Di antara dan terdapat tepat .   Bagian pertama sama dengan akhir panduan sebelumnya. Karena representasi dan , jaraknya . Sementara itu ; jadi lebih dekat.  Misalkan dalam bentuk paling sederhana dan berada di antara dan . Jumlah kedua jaraknya harus . Kasus dan memberi titik ujung. Pada kasus , syarat pertama memberi dan ; syarat kedua memberi dan . Dengan , irisan syarat memaksa dan . Pecahan bukan bentuk paling sederhana, sedangkan sah dan berjarak dari kedua ujung. Jadi daftar pada jawaban lengkap.   Latihan 5: metrik taksi pada  Buktikan untuk dimensi sembarang dengan memeriksa keempat aksioma metrik, termasuk pertidaksamaan segitiga sebagai jumlah pertidaksamaan koordinat.   Petunjuk. Jumlahkan ketaksamaan dari sampai .   merupakan metrik pada .   Setiap suku tak negatif, jadi jumlahnya tak negatif. Jumlah itu nol tepat ketika setiap , yakni ketika . Simetri mengikuti . Untuk titik ketiga , ketaksamaan nilai mutlak pada setiap koordinat memberi . Menjumlahkan atas semua menghasilkan .   Latihan 6: metrik maksimum pada  Selesaikan kedua tugas : buktikan ketaksamaan maksimum bagi dua himpunan berhingga tak kosong di , lalu gunakan hasilnya atau argumen koordinat untuk membuktikan bahwa merupakan metrik.   Petunjuk. Setiap memenuhi .   Berlaku , dan merupakan metrik pada .   Karena berhingga dan tak kosong, semua maksimum ada. Untuk setiap dan , dan , jadi . Mengambil maksimum atas semua jumlah membuktikan ketaksamaan pertama.  Tak-negatif, identitas, dan simetri bagi mengikuti nilai mutlak. Untuk setiap koordinat, . Karena semua dibatasi ruas kanan yang sama, maksimum mereka juga dibatasi ruas kanan tersebut. Inilah pertidaksamaan segitiga.   Latihan 7: metrik hub dan bola-bolanya  Selesaikan seluruh tugas : buktikan bahwa metrik, tentukan dua bola yang diminta, lalu deskripsikan untuk pusat dan jari-jari sembarang.   Petunjuk 1. Jika tiga titik berbeda, ruas kanan pertidaksamaan segitiga memuat tambahan.  Petunjuk 2. Untuk , syarat bola ialah .   Fungsi merupakan metrik. Untuk , . Untuk , . Secara umum, jika , bolanya ; jika , bolanya .   Tak-negatif, identitas, dan simetri langsung dari definisi kasus. Untuk pertidaksamaan segitiga, jika ruas kiri nol. Jika dan atau , diperoleh kesamaan. Jika berbeda dari keduanya, ruas kiri , sedangkan ruas kanan , yang tidak lebih kecil.  Pusat selalu masuk karena jaraknya nol. Untuk , tepat ketika . Jika , tidak ada titik tambahan. Jika , titik tambahannya membentuk bola Euklides berpusat di asal dengan jari-jari . Substitusi dan memberi dua kasus khusus.   Latihan 8: metrik -adik pada bilangan bulat  Selesaikan lima tugas latihan kedelapan: dua perhitungan, lema tentang eksponen keterbagian, bukti metrik, dan dua deskripsi himpunan untuk .   Petunjuk 1. Faktorkan dan .  Petunjuk 2. Jika dua selisih habis dibagi , jumlahnya juga habis dibagi .    untuk dan untuk . Berlaku , sehingga merupakan metrik, bahkan memenuhi pertidaksamaan ultrametrik. Untuk , syarat berarti , sedangkan berarti , dengan turut termasuk pada himpunan kedua.   Selisih pertama , jadi eksponennya dan jaraknya . Selisih kedua , jadi jaraknya .  Misalkan . Bilangan membagi dan , maka membagi jumlahnya ; karena itu . Setelah membalik pangkat positif, diperoleh . Tak-negatif, identitas, dan simetri mengikuti definisi serta ; jadi metrik.  Untuk dan , jarak satu berarti eksponen keterbagian , yakni tidak membagi . Nilai positif yang kurang dari mulai dari , jadi diperlukan , tepat ketika . Titik mempunyai jarak nol dan karena itu juga memenuhi syarat kedua.   Latihan 9: metrik maksimum pada ruang hasil kali  Hitung jarak pasangan pada tugas pertama latihan kesembilan, lalu deskripsikan dan gambarkan bola pada produk metrik Euklides dan diskret.   Petunjuk 1. Hitung jarak pada faktor dan secara terpisah, kemudian ambil maksimum.  Petunjuk 2. Syarat maksimum kurang dari memaksa kedua jarak faktor kurang dari .   Pada tugas pertama, . Pada tugas kedua, , sebuah ruas horizontal terbuka pada tinggi dalam gambar koordinat biasa.   Pada faktor pertama, . Pada faktor kedua, . Maka jarak produk ialah .  Untuk titik , syarat berada dalam bola kedua ialah . Jarak diskret hanya atau ; karena pertidaksamaannya tegas, harus . Syarat yang tersisa ialah . Jadi kedua titik ujung tidak masuk dan tidak ada titik pada tinggi lain.   Latihan 10: metrik logaritmik  Tentukan apakah merupakan metrik pada bilangan real positif dan buktikan jawaban Anda.   Petunjuk. Tulis dan gunakan bahwa injektif pada .   Ya. Metrik tersebut adalah tarikan balik metrik Euklides pada melalui bijeksi .   Karena , logaritma terdefinisi, dan . Nilai ini tak negatif dan simetris. Nilainya nol tepat ketika , yang oleh injektivitas logaritma setara dengan . Untuk , , yaitu tepat . Jadi semua aksioma terpenuhi.   Latihan 11: transformasi terbatas suatu metrik  Buktikan . Selain monotonitas, buktikan secara eksplisit bahwa subaditif pada bilangan tak negatif.   Petunjuk. Sederhanakan menjadi pecahan dengan penyebut positif.   Fungsi merupakan metrik pada .   Fungsi pada tak negatif, naik, dan bernilai nol tepat ketika . Selain itu, untuk , perhitungan langsung memberi Jadi .  Tak-negatif, identitas, dan simetri bagi kini langsung. Untuk pertidaksamaan segitiga, . Monotonitas lalu subaditivitas memberi , yang merupakan aksioma keempat.   Latihan 12: mengalikan metrik dengan konstanta  Tentukan semua syarat pada konstanta agar merupakan metrik. Nyatakan secara terpisah kasus ruang yang mempunyai sedikitnya dua titik dan kasus ruang satu titik.   Petunjuk. Untuk dua titik berbeda, uji tanda dan kemungkinan jarak nol; untuk ruang satu titik, semua nilai sudah nol.   Jika mempunyai sedikitnya dua titik, syarat perlu dan cukup adalah . Jika hanya mempunyai satu titik, setiap konstanta real menghasilkan fungsi nol yang sama dan tetap metrik.   Untuk , mengalikan setiap aksioma metrik dengan mempertahankan tak-negatif, himpunan nol, simetri, dan arah pertidaksamaan segitiga. Jika ada , maka . Untuk , jarak kedua titik menjadi nol dan identitas gagal; untuk , jaraknya negatif. Jadi perlu pada ruang dengan sedikitnya dua titik.  Pada ruang satu titik, satu-satunya pasangan adalah dan . Maka adalah fungsi nol untuk setiap ; semua aksioma tetap terpenuhi. Kasus kosong, jika diizinkan oleh konvensi, juga bersifat vakum.   Latihan 13: fungsi cekung dan transformasi metrik  Selesaikan ketiga tugas latihan fungsi cekung: verifikasi cekungnya , buktikan subaditivitas fungsi cekung pada yang nilainya di nol tak negatif, lalu buktikan bahwa adalah metrik di bawah hipotesis sumber.   Petunjuk 1. Selisih yang relevan untuk adalah .  Petunjuk 2. Jika , gunakan bobot dan ; tangani lebih dahulu.   Fungsi cekung pada , bahkan pada seluruh . Setiap fungsi cekung dengan memenuhi . Dengan tambahan bahwa naik dan nol tepat di nol, komposit merupakan metrik.   Untuk , pertidaksamaan cekung ekuivalen dengan . Selisih ruas kanan dan kiri ialah , jadi klaim berlaku.  Jika , maka . Jika , letakkan . Kekonkavan dengan titik dan memberi . Dengan bobot pelengkap diperoleh . Menjumlahkan memberi subaditivitas.  Untuk , tak-negatif jelas; nilai nol setara dengan , lalu dengan . Simetri diwarisi dari . Akhirnya, monotonitas dan subaditivitas memberi . Jadi semua aksioma metrik terpenuhi.   Latihan 14: lima klaim benar–salah  Putuskan lima klaim pada latihan terakhir dalam urutan sumber. Setiap jawaban salah harus disertai contoh konkret; setiap jawaban benar harus disertai argumen yang berlaku umum.   Petunjuk 1. Titik menguji jarak kuadrat; metrik diskret menguji klaim tentang himpunan dan daerah hasil.  Petunjuk 2. Pada hasil kali jarak, pilih dua titik yang berbeda hanya pada satu koordinat.   Urutannya adalah: salah, benar, benar, salah, salah.   (a) Salah: , tetapi . (b) Benar: pada setiap himpunan tak kosong, metrik diskret merupakan metrik. (c) Benar: jika himpunan mempunyai dua titik berbeda, metrik yang memberi jarak pada setiap pasangan berbeda adalah metrik; nilai yang berbeda memberi tak berhingga banyak fungsi berbeda.  (d) Salah. Ambil dengan metrik diskret. Titik dan berbeda, tetapi hasil kali jaraknya , sehingga identitas titik gagal. (e) Salah: himpunan tak berhingga apa pun dengan metrik diskret mempunyai daerah hasil jarak hanya , suatu himpunan berhingga.   "
},
{
  "id": "o003-c90-ch03-exercise-01",
  "level": "2",
  "url": "o003-c90-ch03-exercise-guides.html#o003-c90-ch03-exercise-01",
  "type": "Pemeriksaan",
  "number": "C.15",
  "title": "Latihan 1: metrik diskret.",
  "body": "Latihan 1: metrik diskret  Buktikan latihan dengan memeriksa keempat aksioma.   Petunjuk. Dalam pertidaksamaan segitiga, pisahkan kasus dan .   Fungsi nol-satu yang diberikan merupakan metrik pada setiap himpunan .   Nilainya atau , jadi tak negatif. Menurut definisi, tepat ketika , dan kondisi kesamaan tidak berubah ketika urutan titik dibalik, sehingga simetri berlaku. Jika , ruas kiri pertidaksamaan segitiga nol. Jika , sedikitnya satu dari atau harus berlaku; maka sedikitnya satu suku ruas kanan bernilai . Jadi .  "
},
{
  "id": "o003-c90-ch03-exercise-02",
  "level": "2",
  "url": "o003-c90-ch03-exercise-guides.html#o003-c90-ch03-exercise-02",
  "type": "Pemeriksaan",
  "number": "C.16",
  "title": "Latihan 2: metrik modular pada tiga titik.",
  "body": "Latihan 2: metrik modular pada tiga titik  Selesaikan kedua nilai pada . Untuk nilai yang menghasilkan metrik, klasifikasikan semua bola terbuka berpusat di menurut jari-jarinya.   Petunjuk 1. Buat tabel simetris untuk pasangan .  Petunjuk 2. Pada , tiga jarak antartitik adalah .   Untuk , fungsi bukan metrik karena . Untuk , fungsi merupakan metrik. Dalam kasus ini, untuk , untuk , dan untuk .   Modulo , nilai diagonal semuanya nol, tetapi juga bersisa nol; identitas titik gagal. Modulo , tabel jaraknya ialah , , , nilai diagonal nol, dan tabel simetris. Ketiga pertidaksamaan tak trivial adalah , , dan ; semuanya benar, jadi fungsi merupakan metrik.  Jarak dari pusat ke berturut-turut . Karena bola terbuka memakai tanda tegas, titik baru masuk ketika dan titik baru masuk ketika , yang menghasilkan tiga kasus pada jawaban.  "
},
{
  "id": "o003-c90-ch03-exercise-03",
  "level": "2",
  "url": "o003-c90-ch03-exercise-guides.html#o003-c90-ch03-exercise-03",
  "type": "Pemeriksaan",
  "number": "C.17",
  "title": "Latihan 3: metrik pembilang–penyebut pada <span class=\"process-math\">\\(\\Q\\)<\/span>.",
  "body": "Latihan 3: metrik pembilang–penyebut pada  Selesaikan ketiga tugas pada : buktikan metriknya, tentukan bola terbuka berpusat di berjari-jari , dan tentukan titik yang berada di antara dan .   Petunjuk 1. Petakan pecahan paling sederhana ke pasangan dan gunakan metrik maksimum.  Petunjuk 2. Semua jarak yang muncul adalah bilangan bulat tak negatif.   Fungsi merupakan metrik. Bola hanya memuat . Titik-titik yang berada di antara dan hanyalah kedua titik ujung tersebut.   Representasi paling sederhana dengan penyebut positif bersifat tunggal, sehingga peta injektif. Rumus adalah pembatasan metrik maksimum pada ke citra ; karena itu keempat aksioma diwarisi. Secara langsung, pertidaksamaan segitiga mengikuti dari dan ketaksamaan yang sama bagi penyebut, lalu mengambil maksimum.  Jarak antardua representasi merupakan maksimum dua bilangan bulat. Syarat jarak kurang dari memaksa kedua selisih nol, jadi bola hanya memuat pusat. Selanjutnya . Jika berada di antara keduanya, dua jarak bilangan bulat tak negatif harus berjumlah ; salah satunya nol. Maka sama dengan salah satu titik ujung. Kedua ujung memang memenuhi definisi betweenness.  "
},
{
  "id": "o003-c90-ch03-exercise-04",
  "level": "2",
  "url": "o003-c90-ch03-exercise-guides.html#o003-c90-ch03-exercise-04",
  "type": "Pemeriksaan",
  "number": "C.18",
  "title": "Latihan 4: betweenness yang berbeda pada <span class=\"process-math\">\\(\\Q\\)<\/span>.",
  "body": "Latihan 4: betweenness yang berbeda pada  Pada latihan keempat dalam urutan sumber, tentukan semua titik di antara dan , bandingkan jarak dan dari , lalu tentukan semua titik di antara dan .   Petunjuk. Untuk kasus terakhir, jarak total ialah ; periksa kemungkinan , , dan .   Di antara dan hanya ada dan . Titik lebih dekat ke daripada . Di antara dan terdapat tepat .   Bagian pertama sama dengan akhir panduan sebelumnya. Karena representasi dan , jaraknya . Sementara itu ; jadi lebih dekat.  Misalkan dalam bentuk paling sederhana dan berada di antara dan . Jumlah kedua jaraknya harus . Kasus dan memberi titik ujung. Pada kasus , syarat pertama memberi dan ; syarat kedua memberi dan . Dengan , irisan syarat memaksa dan . Pecahan bukan bentuk paling sederhana, sedangkan sah dan berjarak dari kedua ujung. Jadi daftar pada jawaban lengkap.  "
},
{
  "id": "o003-c90-ch03-exercise-05",
  "level": "2",
  "url": "o003-c90-ch03-exercise-guides.html#o003-c90-ch03-exercise-05",
  "type": "Pemeriksaan",
  "number": "C.19",
  "title": "Latihan 5: metrik taksi pada <span class=\"process-math\">\\(\\R^n\\)<\/span>.",
  "body": "Latihan 5: metrik taksi pada  Buktikan untuk dimensi sembarang dengan memeriksa keempat aksioma metrik, termasuk pertidaksamaan segitiga sebagai jumlah pertidaksamaan koordinat.   Petunjuk. Jumlahkan ketaksamaan dari sampai .   merupakan metrik pada .   Setiap suku tak negatif, jadi jumlahnya tak negatif. Jumlah itu nol tepat ketika setiap , yakni ketika . Simetri mengikuti . Untuk titik ketiga , ketaksamaan nilai mutlak pada setiap koordinat memberi . Menjumlahkan atas semua menghasilkan .  "
},
{
  "id": "o003-c90-ch03-exercise-06",
  "level": "2",
  "url": "o003-c90-ch03-exercise-guides.html#o003-c90-ch03-exercise-06",
  "type": "Pemeriksaan",
  "number": "C.20",
  "title": "Latihan 6: metrik maksimum pada <span class=\"process-math\">\\(\\R^n\\)<\/span>.",
  "body": "Latihan 6: metrik maksimum pada  Selesaikan kedua tugas : buktikan ketaksamaan maksimum bagi dua himpunan berhingga tak kosong di , lalu gunakan hasilnya atau argumen koordinat untuk membuktikan bahwa merupakan metrik.   Petunjuk. Setiap memenuhi .   Berlaku , dan merupakan metrik pada .   Karena berhingga dan tak kosong, semua maksimum ada. Untuk setiap dan , dan , jadi . Mengambil maksimum atas semua jumlah membuktikan ketaksamaan pertama.  Tak-negatif, identitas, dan simetri bagi mengikuti nilai mutlak. Untuk setiap koordinat, . Karena semua dibatasi ruas kanan yang sama, maksimum mereka juga dibatasi ruas kanan tersebut. Inilah pertidaksamaan segitiga.  "
},
{
  "id": "o003-c90-ch03-exercise-07",
  "level": "2",
  "url": "o003-c90-ch03-exercise-guides.html#o003-c90-ch03-exercise-07",
  "type": "Pemeriksaan",
  "number": "C.21",
  "title": "Latihan 7: metrik hub dan bola-bolanya.",
  "body": "Latihan 7: metrik hub dan bola-bolanya  Selesaikan seluruh tugas : buktikan bahwa metrik, tentukan dua bola yang diminta, lalu deskripsikan untuk pusat dan jari-jari sembarang.   Petunjuk 1. Jika tiga titik berbeda, ruas kanan pertidaksamaan segitiga memuat tambahan.  Petunjuk 2. Untuk , syarat bola ialah .   Fungsi merupakan metrik. Untuk , . Untuk , . Secara umum, jika , bolanya ; jika , bolanya .   Tak-negatif, identitas, dan simetri langsung dari definisi kasus. Untuk pertidaksamaan segitiga, jika ruas kiri nol. Jika dan atau , diperoleh kesamaan. Jika berbeda dari keduanya, ruas kiri , sedangkan ruas kanan , yang tidak lebih kecil.  Pusat selalu masuk karena jaraknya nol. Untuk , tepat ketika . Jika , tidak ada titik tambahan. Jika , titik tambahannya membentuk bola Euklides berpusat di asal dengan jari-jari . Substitusi dan memberi dua kasus khusus.  "
},
{
  "id": "o003-c90-ch03-exercise-08",
  "level": "2",
  "url": "o003-c90-ch03-exercise-guides.html#o003-c90-ch03-exercise-08",
  "type": "Pemeriksaan",
  "number": "C.22",
  "title": "Latihan 8: metrik <span class=\"process-math\">\\(p\\)<\/span>-adik pada bilangan bulat.",
  "body": "Latihan 8: metrik -adik pada bilangan bulat  Selesaikan lima tugas latihan kedelapan: dua perhitungan, lema tentang eksponen keterbagian, bukti metrik, dan dua deskripsi himpunan untuk .   Petunjuk 1. Faktorkan dan .  Petunjuk 2. Jika dua selisih habis dibagi , jumlahnya juga habis dibagi .    untuk dan untuk . Berlaku , sehingga merupakan metrik, bahkan memenuhi pertidaksamaan ultrametrik. Untuk , syarat berarti , sedangkan berarti , dengan turut termasuk pada himpunan kedua.   Selisih pertama , jadi eksponennya dan jaraknya . Selisih kedua , jadi jaraknya .  Misalkan . Bilangan membagi dan , maka membagi jumlahnya ; karena itu . Setelah membalik pangkat positif, diperoleh . Tak-negatif, identitas, dan simetri mengikuti definisi serta ; jadi metrik.  Untuk dan , jarak satu berarti eksponen keterbagian , yakni tidak membagi . Nilai positif yang kurang dari mulai dari , jadi diperlukan , tepat ketika . Titik mempunyai jarak nol dan karena itu juga memenuhi syarat kedua.  "
},
{
  "id": "o003-c90-ch03-exercise-09",
  "level": "2",
  "url": "o003-c90-ch03-exercise-guides.html#o003-c90-ch03-exercise-09",
  "type": "Pemeriksaan",
  "number": "C.23",
  "title": "Latihan 9: metrik maksimum pada ruang hasil kali.",
  "body": "Latihan 9: metrik maksimum pada ruang hasil kali  Hitung jarak pasangan pada tugas pertama latihan kesembilan, lalu deskripsikan dan gambarkan bola pada produk metrik Euklides dan diskret.   Petunjuk 1. Hitung jarak pada faktor dan secara terpisah, kemudian ambil maksimum.  Petunjuk 2. Syarat maksimum kurang dari memaksa kedua jarak faktor kurang dari .   Pada tugas pertama, . Pada tugas kedua, , sebuah ruas horizontal terbuka pada tinggi dalam gambar koordinat biasa.   Pada faktor pertama, . Pada faktor kedua, . Maka jarak produk ialah .  Untuk titik , syarat berada dalam bola kedua ialah . Jarak diskret hanya atau ; karena pertidaksamaannya tegas, harus . Syarat yang tersisa ialah . Jadi kedua titik ujung tidak masuk dan tidak ada titik pada tinggi lain.  "
},
{
  "id": "o003-c90-ch03-exercise-10",
  "level": "2",
  "url": "o003-c90-ch03-exercise-guides.html#o003-c90-ch03-exercise-10",
  "type": "Pemeriksaan",
  "number": "C.24",
  "title": "Latihan 10: metrik logaritmik.",
  "body": "Latihan 10: metrik logaritmik  Tentukan apakah merupakan metrik pada bilangan real positif dan buktikan jawaban Anda.   Petunjuk. Tulis dan gunakan bahwa injektif pada .   Ya. Metrik tersebut adalah tarikan balik metrik Euklides pada melalui bijeksi .   Karena , logaritma terdefinisi, dan . Nilai ini tak negatif dan simetris. Nilainya nol tepat ketika , yang oleh injektivitas logaritma setara dengan . Untuk , , yaitu tepat . Jadi semua aksioma terpenuhi.  "
},
{
  "id": "o003-c90-ch03-exercise-11",
  "level": "2",
  "url": "o003-c90-ch03-exercise-guides.html#o003-c90-ch03-exercise-11",
  "type": "Pemeriksaan",
  "number": "C.25",
  "title": "Latihan 11: transformasi terbatas suatu metrik.",
  "body": "Latihan 11: transformasi terbatas suatu metrik  Buktikan . Selain monotonitas, buktikan secara eksplisit bahwa subaditif pada bilangan tak negatif.   Petunjuk. Sederhanakan menjadi pecahan dengan penyebut positif.   Fungsi merupakan metrik pada .   Fungsi pada tak negatif, naik, dan bernilai nol tepat ketika . Selain itu, untuk , perhitungan langsung memberi Jadi .  Tak-negatif, identitas, dan simetri bagi kini langsung. Untuk pertidaksamaan segitiga, . Monotonitas lalu subaditivitas memberi , yang merupakan aksioma keempat.  "
},
{
  "id": "o003-c90-ch03-exercise-12",
  "level": "2",
  "url": "o003-c90-ch03-exercise-guides.html#o003-c90-ch03-exercise-12",
  "type": "Pemeriksaan",
  "number": "C.26",
  "title": "Latihan 12: mengalikan metrik dengan konstanta.",
  "body": "Latihan 12: mengalikan metrik dengan konstanta  Tentukan semua syarat pada konstanta agar merupakan metrik. Nyatakan secara terpisah kasus ruang yang mempunyai sedikitnya dua titik dan kasus ruang satu titik.   Petunjuk. Untuk dua titik berbeda, uji tanda dan kemungkinan jarak nol; untuk ruang satu titik, semua nilai sudah nol.   Jika mempunyai sedikitnya dua titik, syarat perlu dan cukup adalah . Jika hanya mempunyai satu titik, setiap konstanta real menghasilkan fungsi nol yang sama dan tetap metrik.   Untuk , mengalikan setiap aksioma metrik dengan mempertahankan tak-negatif, himpunan nol, simetri, dan arah pertidaksamaan segitiga. Jika ada , maka . Untuk , jarak kedua titik menjadi nol dan identitas gagal; untuk , jaraknya negatif. Jadi perlu pada ruang dengan sedikitnya dua titik.  Pada ruang satu titik, satu-satunya pasangan adalah dan . Maka adalah fungsi nol untuk setiap ; semua aksioma tetap terpenuhi. Kasus kosong, jika diizinkan oleh konvensi, juga bersifat vakum.  "
},
{
  "id": "o003-c90-ch03-exercise-13",
  "level": "2",
  "url": "o003-c90-ch03-exercise-guides.html#o003-c90-ch03-exercise-13",
  "type": "Pemeriksaan",
  "number": "C.27",
  "title": "Latihan 13: fungsi cekung dan transformasi metrik.",
  "body": "Latihan 13: fungsi cekung dan transformasi metrik  Selesaikan ketiga tugas latihan fungsi cekung: verifikasi cekungnya , buktikan subaditivitas fungsi cekung pada yang nilainya di nol tak negatif, lalu buktikan bahwa adalah metrik di bawah hipotesis sumber.   Petunjuk 1. Selisih yang relevan untuk adalah .  Petunjuk 2. Jika , gunakan bobot dan ; tangani lebih dahulu.   Fungsi cekung pada , bahkan pada seluruh . Setiap fungsi cekung dengan memenuhi . Dengan tambahan bahwa naik dan nol tepat di nol, komposit merupakan metrik.   Untuk , pertidaksamaan cekung ekuivalen dengan . Selisih ruas kanan dan kiri ialah , jadi klaim berlaku.  Jika , maka . Jika , letakkan . Kekonkavan dengan titik dan memberi . Dengan bobot pelengkap diperoleh . Menjumlahkan memberi subaditivitas.  Untuk , tak-negatif jelas; nilai nol setara dengan , lalu dengan . Simetri diwarisi dari . Akhirnya, monotonitas dan subaditivitas memberi . Jadi semua aksioma metrik terpenuhi.  "
},
{
  "id": "o003-c90-ch03-exercise-14",
  "level": "2",
  "url": "o003-c90-ch03-exercise-guides.html#o003-c90-ch03-exercise-14",
  "type": "Pemeriksaan",
  "number": "C.28",
  "title": "Latihan 14: lima klaim benar–salah.",
  "body": "Latihan 14: lima klaim benar–salah  Putuskan lima klaim pada latihan terakhir dalam urutan sumber. Setiap jawaban salah harus disertai contoh konkret; setiap jawaban benar harus disertai argumen yang berlaku umum.   Petunjuk 1. Titik menguji jarak kuadrat; metrik diskret menguji klaim tentang himpunan dan daerah hasil.  Petunjuk 2. Pada hasil kali jarak, pilih dua titik yang berbeda hanya pada satu koordinat.   Urutannya adalah: salah, benar, benar, salah, salah.   (a) Salah: , tetapi . (b) Benar: pada setiap himpunan tak kosong, metrik diskret merupakan metrik. (c) Benar: jika himpunan mempunyai dua titik berbeda, metrik yang memberi jarak pada setiap pasangan berbeda adalah metrik; nilai yang berbeda memberi tak berhingga banyak fungsi berbeda.  (d) Salah. Ambil dengan metrik diskret. Titik dan berbeda, tetapi hasil kali jaraknya , sehingga identitas titik gagal. (e) Salah: himpunan tak berhingga apa pun dengan metrik diskret mempunyai daerah hasil jarak hanya , suatu himpunan berhingga.  "
},
{
  "id": "o003-c90-ch04-source-task-guides",
  "level": "1",
  "url": "o003-c90-ch04-source-task-guides.html",
  "type": "Bagian",
  "number": "",
  "title": "Panduan untuk tugas sumber",
  "body": " Panduan untuk tugas sumber  Delapan pemeriksaan berikut berkorespondensi, secara berurutan, dengan lima tugas yang diratakan dari bagian dan tiga tugas dari bagian .  Tugas Hamming 1: membuktikan aksioma metrik  Buktikan bahwa fungsi pada , dengan , benar-benar merupakan metrik. Rubrik: tangani tak-negatif, identitas titik, simetri, dan pertidaksamaan segitiga; jangan mengganti bukti umum dengan satu contoh numerik.   Petunjuk 1. Setiap suku bernilai nol atau satu.  Petunjuk 2. Terapkan pertidaksamaan segitiga nilai mutlak pada setiap koordinat, lalu jumlahkan.   Ya. Keempat aksioma metrik mengikuti sifat nilai mutlak pada setiap koordinat dan fakta bahwa jumlahnya nol tepat ketika semua koordinat sama.   Karena setiap , jumlah tak negatif. Jumlah ini nol tepat ketika setiap sukunya nol, yakni tepat ketika untuk semua ; keadaan itu setara dengan . Kesamaan pada setiap koordinat memberi simetri.  Untuk , pertidaksamaan nilai mutlak memberi untuk setiap . Menjumlahkan dari sampai menghasilkan . Jadi memenuhi seluruh aksioma metrik.   Tugas Hamming 2: jarak dua kata kode  Untuk kode pada bab utama, hitung dan tunjukkan koordinat mana yang menyumbang pada jarak tersebut.   Petunjuk. Bandingkan dan dari kiri ke kanan.   ; kedua kata berbeda tepat pada koordinat ketiga dan keempat.   Kita mempunyai dan . Selisih pada koordinat pertama, kedua, kelima, dan keenam adalah nol, sedangkan selisih pada koordinat ketiga dan keempat bernilai satu. Karena itu, .   Tugas Hamming 3: menyiapkan pesan untuk pendekodean  Namai kelima blok pada pesan yang diterima sebagai , lalu tentukan blok mana yang sudah merupakan kata kode dalam . Rubrik: pertahankan urutan blok dan cocokkan blok yang sah dengan indeks kata kodenya.   Petunjuk. Bandingkan setiap blok enam bit dengan daftar , bukan hanya dengan panjangnya.   Bloknya adalah , , , , dan . Jadi sudah berada dalam , sedangkan tidak.   Memisahkan pesan pada setiap spasi menghasilkan, dalam urutan yang diterima, Pencocokan langsung dengan delapan anggota memberi , , dan . Tidak ada anggota daftar yang sama dengan atau . Audit ini menyiapkan dua sub-tugas pendekodean berikutnya tanpa menebak kata pengganti terlebih dahulu.   Tugas Hamming 4: mendeteksi galat transmisi  Jelaskan bagaimana pesan yang diterima membuktikan bahwa sedikitnya satu galat transmisi telah terjadi, dengan asumsi setiap blok yang dikirim harus merupakan kata kode dalam .   Petunjuk. Keanggotaan dalam kode adalah uji validitas blok yang diterima.   Blok pertama dan blok ketiga bukan anggota ; karena blok yang sah harus berada dalam , pesan tersebut tidak mungkin diterima tanpa galat.   Menurut definisi kode yang dipakai, pengirim hanya mengirim anggota . Pemeriksaan keanggotaan pada tugas sebelumnya menunjukkan dan . Maka kedua blok yang diterima itu tidak mungkin identik dengan blok sah yang dikirim. Sedikitnya satu bit berubah pada masing-masing blok tersebut. Sebaliknya, fakta bahwa tidak membuktikan bahwa bit-bitnya pasti tidak berubah; galat berganda secara prinsip dapat mengubah satu kata kode menjadi kata kode lain. Yang pasti dari data ini ialah adanya galat pada blok pertama dan ketiga.   Tugas Hamming 5: semua hasil pendekodean terdekat  Ganti setiap blok yang diterima dengan setiap kata kode yang berjarak paling dekat. Temukan seluruh pesan hasil, bukan hanya satu pilihan. Rubrik: hitung jarak terhadap kedelapan kata kode untuk setiap blok dan nyatakan semua keadaan seri.   Petunjuk 1. Susun satu baris delapan jarak untuk setiap .  Petunjuk 2. Empat kata kode sama-sama berjarak satu dari blok pertama.   Blok terdekatnya adalah , , , , dan . Jadi terdapat tepat empat pesan hasil.   Dengan kolom dalam urutan , seluruh vektor jarak adalah Minimum baris pertama ialah satu dan dicapai pada kolom . Minimum baris ketiga ialah satu dan hanya dicapai pada kolom pertama. Tiga blok yang memang sudah berupa kata kode mempunyai minimum nol yang unik pada kolomnya sendiri.  Oleh sebab itu, seluruh kemungkinan pesan terkoreksi, dalam urutan blok, ialah Dekode tetangga terdekat tidak menyediakan informasi untuk memilih satu di antara empat kemungkinan ini bagi blok pertama.   Tugas Levenshtein 1: dari green ke grease  Ubah green menjadi grease dengan operasi penyisipan, penghapusan, dan substitusi yang diizinkan. Berikan urutan terpendek, identifikasi setiap operasi, dan buktikan bahwa lebih sedikit operasi tidak mungkin.   Petunjuk 1. Pertahankan awalan gre , lalu ubah dua huruf dan tambahkan satu huruf.  Petunjuk 2. Karena panjang sasaran lebih besar satu, lintasan dengan paling banyak dua operasi harus memakai tepat satu penyisipan dan paling banyak satu substitusi.   Salah satu urutan terpendek adalah green → grean → greas → grease . Jadi .   Substitusikan huruf keempat e dengan a untuk memperoleh grean . Substitusikan n dengan s untuk memperoleh greas , lalu sisipkan e di ujung. Ini memberi batas atas tiga operasi.  Untuk batas bawah, perubahan panjang dari lima menjadi enam memerlukan sedikitnya satu penyisipan. Jika seluruh perubahan memakai paling banyak dua operasi, hitungan panjang memaksa tepat satu penyisipan, tanpa penghapusan, dan paling banyak satu substitusi. Menghapus calon huruf yang disisipkan dari grease menghasilkan salah satu dari rease , gease , grase , grese , greae , atau greas . Jarak Hamming masing-masing dari green adalah . Tidak satu pun dapat diperoleh dari green dengan paling banyak satu substitusi. Jadi dua operasi mustahil, sedangkan tiga operasi sudah dicapai; jaraknya tepat tiga.   Tugas Levenshtein 2: membuktikan metrik pada  Misalkan adalah himpunan semua untai berhingga atas alfabet . Buktikan bahwa banyak minimum operasi penyisipan, penghapusan, dan substitusi mendefinisikan metrik pada . Rubrik: jelaskan bahwa minimum ada, lalu buktikan keempat aksioma.   Petunjuk 1. Semua huruf dapat dihapus, kemudian semua huruf disisipkan.  Petunjuk 2. Balik urutan operasi untuk simetri dan sambungkan dua urutan terpendek untuk pertidaksamaan segitiga.   Fungsi merupakan metrik pada . Urutan kosong memberi identitas, pembalikan operasi memberi simetri, dan penyambungan urutan edit memberi pertidaksamaan segitiga.   Untuk sembarang untai , ada urutan edit berhingga: hapus seluruh huruf , lalu sisipkan seluruh huruf . Jadi himpunan panjang urutan edit dari ke adalah subhimpunan tak kosong dari bilangan bulat tak negatif; menurut prinsip pengurutan baik, himpunan itu mempunyai minimum. Karena panjang urutan edit tak negatif, .  Jika , urutan kosong mempunyai panjang nol, sehingga . Sebaliknya, jarak nol berarti minimum dicapai oleh urutan tanpa operasi; urutan demikian tidak mengubah untai, jadi . Setiap substitusi dapat dibalik dengan substitusi, setiap penyisipan dengan penghapusan, dan setiap penghapusan dengan penyisipan. Membalik urutan terpendek dari ke menghasilkan urutan sama panjang dari ke . Maka ; menukar peran memberi pertidaksamaan sebaliknya, sehingga jaraknya simetris.  Akhirnya, sambungkan urutan terpendek dari ke dengan urutan terpendek dari ke . Hasilnya adalah suatu urutan dari ke sepanjang . Karena adalah panjang minimum, . Keempat aksioma terpenuhi.   Tugas Levenshtein 3: memilih koreksi ejaan terdekat  Hitung secara tepat jarak Levenshtein dari tupotagry ke topography , topology , dan tautology . Tentukan pilihan pemeriksa ejaan dan buktikan bahwa setiap jarak yang dilaporkan memang minimum.   Petunjuk 1. Isi tabel jarak untuk semua pasangan awalan, bukan hanya mencocokkan huruf pada posisi yang sama.  Petunjuk 2. Rekurensi mengambil minimum dari penghapusan, penyisipan, dan substitusi atau pencocokan terakhir.   Jaraknya berturut-turut adalah , , dan . Karena itu, pilihan terdekat yang unik adalah topology .   Untuk awalan sepanjang dan , definisikan sebagai jarak keduanya. Nilai batasnya dan . Jika huruf terakhir sama, letakkan ; jika berbeda, letakkan . Meninjau operasi terakhir memberi rekurensi Argumen berdasarkan operasi terakhir menunjukkan bahwa setiap urutan edit masuk ke salah satu dari tiga kasus ini; karena itu, tabel tersebut memberi batas bawah sekaligus batas atas.  Untuk sumber tupotagry , baris terakhir tabel, mulai dari awalan sasaran kosong, adalah Unsur terakhir memberi jarak . Batas atas itu juga tampak pada urutan edit berikut; setiap anak panah adalah satu operasi:   tupotagry → topotagry → topogtagry → topogragry → topograpry → topography ;   tupotagry → topotagry → topolagry → topologry → topology ;   tupotagry → taupotagry → tautotagry → tautolagry → tautologry → tautology . Karena nilai minimum terkecil adalah empat dan hanya dimiliki topology , itulah koreksi menurut aturan tetangga terdekat.   "
},
{
  "id": "o003-c90-ch04-hamming-task-01",
  "level": "2",
  "url": "o003-c90-ch04-source-task-guides.html#o003-c90-ch04-hamming-task-01",
  "type": "Pemeriksaan",
  "number": "D.1",
  "title": "Tugas Hamming 1: membuktikan aksioma metrik.",
  "body": "Tugas Hamming 1: membuktikan aksioma metrik  Buktikan bahwa fungsi pada , dengan , benar-benar merupakan metrik. Rubrik: tangani tak-negatif, identitas titik, simetri, dan pertidaksamaan segitiga; jangan mengganti bukti umum dengan satu contoh numerik.   Petunjuk 1. Setiap suku bernilai nol atau satu.  Petunjuk 2. Terapkan pertidaksamaan segitiga nilai mutlak pada setiap koordinat, lalu jumlahkan.   Ya. Keempat aksioma metrik mengikuti sifat nilai mutlak pada setiap koordinat dan fakta bahwa jumlahnya nol tepat ketika semua koordinat sama.   Karena setiap , jumlah tak negatif. Jumlah ini nol tepat ketika setiap sukunya nol, yakni tepat ketika untuk semua ; keadaan itu setara dengan . Kesamaan pada setiap koordinat memberi simetri.  Untuk , pertidaksamaan nilai mutlak memberi untuk setiap . Menjumlahkan dari sampai menghasilkan . Jadi memenuhi seluruh aksioma metrik.  "
},
{
  "id": "o003-c90-ch04-hamming-task-02",
  "level": "2",
  "url": "o003-c90-ch04-source-task-guides.html#o003-c90-ch04-hamming-task-02",
  "type": "Pemeriksaan",
  "number": "D.2",
  "title": "Tugas Hamming 2: jarak dua kata kode.",
  "body": "Tugas Hamming 2: jarak dua kata kode  Untuk kode pada bab utama, hitung dan tunjukkan koordinat mana yang menyumbang pada jarak tersebut.   Petunjuk. Bandingkan dan dari kiri ke kanan.   ; kedua kata berbeda tepat pada koordinat ketiga dan keempat.   Kita mempunyai dan . Selisih pada koordinat pertama, kedua, kelima, dan keenam adalah nol, sedangkan selisih pada koordinat ketiga dan keempat bernilai satu. Karena itu, .  "
},
{
  "id": "o003-c90-ch04-hamming-task-03",
  "level": "2",
  "url": "o003-c90-ch04-source-task-guides.html#o003-c90-ch04-hamming-task-03",
  "type": "Pemeriksaan",
  "number": "D.3",
  "title": "Tugas Hamming 3: menyiapkan pesan untuk pendekodean.",
  "body": "Tugas Hamming 3: menyiapkan pesan untuk pendekodean  Namai kelima blok pada pesan yang diterima sebagai , lalu tentukan blok mana yang sudah merupakan kata kode dalam . Rubrik: pertahankan urutan blok dan cocokkan blok yang sah dengan indeks kata kodenya.   Petunjuk. Bandingkan setiap blok enam bit dengan daftar , bukan hanya dengan panjangnya.   Bloknya adalah , , , , dan . Jadi sudah berada dalam , sedangkan tidak.   Memisahkan pesan pada setiap spasi menghasilkan, dalam urutan yang diterima, Pencocokan langsung dengan delapan anggota memberi , , dan . Tidak ada anggota daftar yang sama dengan atau . Audit ini menyiapkan dua sub-tugas pendekodean berikutnya tanpa menebak kata pengganti terlebih dahulu.  "
},
{
  "id": "o003-c90-ch04-hamming-task-04",
  "level": "2",
  "url": "o003-c90-ch04-source-task-guides.html#o003-c90-ch04-hamming-task-04",
  "type": "Pemeriksaan",
  "number": "D.4",
  "title": "Tugas Hamming 4: mendeteksi galat transmisi.",
  "body": "Tugas Hamming 4: mendeteksi galat transmisi  Jelaskan bagaimana pesan yang diterima membuktikan bahwa sedikitnya satu galat transmisi telah terjadi, dengan asumsi setiap blok yang dikirim harus merupakan kata kode dalam .   Petunjuk. Keanggotaan dalam kode adalah uji validitas blok yang diterima.   Blok pertama dan blok ketiga bukan anggota ; karena blok yang sah harus berada dalam , pesan tersebut tidak mungkin diterima tanpa galat.   Menurut definisi kode yang dipakai, pengirim hanya mengirim anggota . Pemeriksaan keanggotaan pada tugas sebelumnya menunjukkan dan . Maka kedua blok yang diterima itu tidak mungkin identik dengan blok sah yang dikirim. Sedikitnya satu bit berubah pada masing-masing blok tersebut. Sebaliknya, fakta bahwa tidak membuktikan bahwa bit-bitnya pasti tidak berubah; galat berganda secara prinsip dapat mengubah satu kata kode menjadi kata kode lain. Yang pasti dari data ini ialah adanya galat pada blok pertama dan ketiga.  "
},
{
  "id": "o003-c90-ch04-hamming-task-05",
  "level": "2",
  "url": "o003-c90-ch04-source-task-guides.html#o003-c90-ch04-hamming-task-05",
  "type": "Pemeriksaan",
  "number": "D.5",
  "title": "Tugas Hamming 5: semua hasil pendekodean terdekat.",
  "body": "Tugas Hamming 5: semua hasil pendekodean terdekat  Ganti setiap blok yang diterima dengan setiap kata kode yang berjarak paling dekat. Temukan seluruh pesan hasil, bukan hanya satu pilihan. Rubrik: hitung jarak terhadap kedelapan kata kode untuk setiap blok dan nyatakan semua keadaan seri.   Petunjuk 1. Susun satu baris delapan jarak untuk setiap .  Petunjuk 2. Empat kata kode sama-sama berjarak satu dari blok pertama.   Blok terdekatnya adalah , , , , dan . Jadi terdapat tepat empat pesan hasil.   Dengan kolom dalam urutan , seluruh vektor jarak adalah Minimum baris pertama ialah satu dan dicapai pada kolom . Minimum baris ketiga ialah satu dan hanya dicapai pada kolom pertama. Tiga blok yang memang sudah berupa kata kode mempunyai minimum nol yang unik pada kolomnya sendiri.  Oleh sebab itu, seluruh kemungkinan pesan terkoreksi, dalam urutan blok, ialah Dekode tetangga terdekat tidak menyediakan informasi untuk memilih satu di antara empat kemungkinan ini bagi blok pertama.  "
},
{
  "id": "o003-c90-ch04-levenshtein-task-01",
  "level": "2",
  "url": "o003-c90-ch04-source-task-guides.html#o003-c90-ch04-levenshtein-task-01",
  "type": "Pemeriksaan",
  "number": "D.6",
  "title": "Tugas Levenshtein 1: dari “green” ke “grease”.",
  "body": "Tugas Levenshtein 1: dari green ke grease  Ubah green menjadi grease dengan operasi penyisipan, penghapusan, dan substitusi yang diizinkan. Berikan urutan terpendek, identifikasi setiap operasi, dan buktikan bahwa lebih sedikit operasi tidak mungkin.   Petunjuk 1. Pertahankan awalan gre , lalu ubah dua huruf dan tambahkan satu huruf.  Petunjuk 2. Karena panjang sasaran lebih besar satu, lintasan dengan paling banyak dua operasi harus memakai tepat satu penyisipan dan paling banyak satu substitusi.   Salah satu urutan terpendek adalah green → grean → greas → grease . Jadi .   Substitusikan huruf keempat e dengan a untuk memperoleh grean . Substitusikan n dengan s untuk memperoleh greas , lalu sisipkan e di ujung. Ini memberi batas atas tiga operasi.  Untuk batas bawah, perubahan panjang dari lima menjadi enam memerlukan sedikitnya satu penyisipan. Jika seluruh perubahan memakai paling banyak dua operasi, hitungan panjang memaksa tepat satu penyisipan, tanpa penghapusan, dan paling banyak satu substitusi. Menghapus calon huruf yang disisipkan dari grease menghasilkan salah satu dari rease , gease , grase , grese , greae , atau greas . Jarak Hamming masing-masing dari green adalah . Tidak satu pun dapat diperoleh dari green dengan paling banyak satu substitusi. Jadi dua operasi mustahil, sedangkan tiga operasi sudah dicapai; jaraknya tepat tiga.  "
},
{
  "id": "o003-c90-ch04-levenshtein-task-02",
  "level": "2",
  "url": "o003-c90-ch04-source-task-guides.html#o003-c90-ch04-levenshtein-task-02",
  "type": "Pemeriksaan",
  "number": "D.7",
  "title": "Tugas Levenshtein 2: membuktikan metrik pada <span class=\"process-math\">\\(\\Sigma^\\ast\\)<\/span>.",
  "body": "Tugas Levenshtein 2: membuktikan metrik pada  Misalkan adalah himpunan semua untai berhingga atas alfabet . Buktikan bahwa banyak minimum operasi penyisipan, penghapusan, dan substitusi mendefinisikan metrik pada . Rubrik: jelaskan bahwa minimum ada, lalu buktikan keempat aksioma.   Petunjuk 1. Semua huruf dapat dihapus, kemudian semua huruf disisipkan.  Petunjuk 2. Balik urutan operasi untuk simetri dan sambungkan dua urutan terpendek untuk pertidaksamaan segitiga.   Fungsi merupakan metrik pada . Urutan kosong memberi identitas, pembalikan operasi memberi simetri, dan penyambungan urutan edit memberi pertidaksamaan segitiga.   Untuk sembarang untai , ada urutan edit berhingga: hapus seluruh huruf , lalu sisipkan seluruh huruf . Jadi himpunan panjang urutan edit dari ke adalah subhimpunan tak kosong dari bilangan bulat tak negatif; menurut prinsip pengurutan baik, himpunan itu mempunyai minimum. Karena panjang urutan edit tak negatif, .  Jika , urutan kosong mempunyai panjang nol, sehingga . Sebaliknya, jarak nol berarti minimum dicapai oleh urutan tanpa operasi; urutan demikian tidak mengubah untai, jadi . Setiap substitusi dapat dibalik dengan substitusi, setiap penyisipan dengan penghapusan, dan setiap penghapusan dengan penyisipan. Membalik urutan terpendek dari ke menghasilkan urutan sama panjang dari ke . Maka ; menukar peran memberi pertidaksamaan sebaliknya, sehingga jaraknya simetris.  Akhirnya, sambungkan urutan terpendek dari ke dengan urutan terpendek dari ke . Hasilnya adalah suatu urutan dari ke sepanjang . Karena adalah panjang minimum, . Keempat aksioma terpenuhi.  "
},
{
  "id": "o003-c90-ch04-levenshtein-task-03",
  "level": "2",
  "url": "o003-c90-ch04-source-task-guides.html#o003-c90-ch04-levenshtein-task-03",
  "type": "Pemeriksaan",
  "number": "D.8",
  "title": "Tugas Levenshtein 3: memilih koreksi ejaan terdekat.",
  "body": "Tugas Levenshtein 3: memilih koreksi ejaan terdekat  Hitung secara tepat jarak Levenshtein dari tupotagry ke topography , topology , dan tautology . Tentukan pilihan pemeriksa ejaan dan buktikan bahwa setiap jarak yang dilaporkan memang minimum.   Petunjuk 1. Isi tabel jarak untuk semua pasangan awalan, bukan hanya mencocokkan huruf pada posisi yang sama.  Petunjuk 2. Rekurensi mengambil minimum dari penghapusan, penyisipan, dan substitusi atau pencocokan terakhir.   Jaraknya berturut-turut adalah , , dan . Karena itu, pilihan terdekat yang unik adalah topology .   Untuk awalan sepanjang dan , definisikan sebagai jarak keduanya. Nilai batasnya dan . Jika huruf terakhir sama, letakkan ; jika berbeda, letakkan . Meninjau operasi terakhir memberi rekurensi Argumen berdasarkan operasi terakhir menunjukkan bahwa setiap urutan edit masuk ke salah satu dari tiga kasus ini; karena itu, tabel tersebut memberi batas bawah sekaligus batas atas.  Untuk sumber tupotagry , baris terakhir tabel, mulai dari awalan sasaran kosong, adalah Unsur terakhir memberi jarak . Batas atas itu juga tampak pada urutan edit berikut; setiap anak panah adalah satu operasi:   tupotagry → topotagry → topogtagry → topogragry → topograpry → topography ;   tupotagry → topotagry → topolagry → topologry → topology ;   tupotagry → taupotagry → tautotagry → tautolagry → tautologry → tautology . Karena nilai minimum terkecil adalah empat dan hanya dimiliki topology , itulah koreksi menurut aturan tetangga terdekat.  "
},
{
  "id": "o003-c90-ch04-mastery",
  "level": "1",
  "url": "o003-c90-ch04-mastery.html",
  "type": "Bagian",
  "number": "",
  "title": "Uji penguasaan",
  "body": " Uji penguasaan  Empat butir berikut merupakan materi asli pendamping. Kerjakan tanpa membuka petunjuk terlebih dahulu, lalu gunakan pembahasan untuk mengaudit perhitungan dan argumen batas bawah Anda.  Penguasaan 1: lintasan geodesik Hamming  Dalam , ambil , , dan . Hitung ketiga jarak pasangan dan tentukan apakah pertidaksamaan segitiga menjadi kesamaan melalui .   Petunjuk. Tandai koordinat yang berbeda untuk setiap pasangan secara terpisah.   , , dan ; jadi kesamaan segitiga berlaku.   Kata berbeda pada koordinat , sehingga . Kata berbeda pada koordinat , sehingga jaraknya . Kata hanya berbeda pada koordinat kelima, sehingga jaraknya . Maka ; berada pada suatu lintasan terpendek dari ke dalam kubus Hamming.   Penguasaan 2: kapan dekode terdekat bersifat unik  Misalkan jarak minimum antara dua kata kode berbeda dalam adalah . Buktikan: jika kata diterima memenuhi untuk suatu , maka adalah satu-satunya kata kode terdekat dengan .   Petunjuk. Andaikan ada dengan , lalu gunakan pertidaksamaan segitiga pada .   Benar. Kata kode lain yang setidaknya sama dekat akan memaksa , bertentangan dengan definisi jarak minimum kode.   Andaikan , , dan . Pertidaksamaan segitiga memberi Namun dua kata kode berbeda harus berjarak sedikitnya . Kontradiksi ini menunjukkan bahwa tidak ada yang sama dekat atau lebih dekat daripada . Jadi dekode terdekatnya unik.   Penguasaan 3: jarak kitten dan sitting  Hitung jarak Levenshtein antara kitten dan sitting . Berikan urutan edit yang mencapai nilai tersebut dan sertakan alasan bahwa dua operasi tidak cukup.   Petunjuk. Dua substitusi dan satu penyisipan memberi batas atas; gunakan rekurensi awalan untuk batas bawah.   .   Urutan kitten → sitten → sittin → sitting memakai substitusi k menjadi s , substitusi e menjadi i , lalu penyisipan g . Jadi jaraknya paling besar tiga.  Rekurensi awalan dari pembahasan tugas Levenshtein 3, dengan kolom berlabel awalan sitting , menghasilkan baris terakhir untuk kitten  . Unsur terakhir adalah tiga. Karena rekurensi itu menguji ketiga kemungkinan operasi terakhir dan dimulai dari nilai batas yang tepat, tidak ada urutan sepanjang dua. Maka jaraknya tepat tiga.   Penguasaan 4: membandingkan Hamming dan Levenshtein  Untuk dua untai biner dengan panjang sama, buktikan . Tunjukkan bahwa pertidaksamaan dapat ketat dengan menghitung kedua jarak bagi dan .   Petunjuk 1. Substitusikan tepat koordinat yang berbeda untuk memperoleh batas umum.  Petunjuk 2. Pada contoh, satu penghapusan dan satu penyisipan memindahkan pola bergantian.   Selalu berlaku . Pada contoh, , sedangkan .   Jika berbeda pada koordinat, substitusikan huruf pada masing-masing koordinat tersebut dengan huruf . Urutan ini mengubah menjadi dalam operasi, sehingga minimum Levenshtein memenuhi .  Keempat koordinat dan berbeda, jadi jarak Hamming-nya empat. Untuk Levenshtein, hapus nol pertama dari 0101 sehingga diperoleh 101 , lalu sisipkan nol di ujung sehingga diperoleh 1010 ; jadi . Jaraknya bukan nol karena untainya berbeda. Jaraknya juga bukan satu: satu penyisipan atau penghapusan akan mengubah panjang, sedangkan satu substitusi hanya dapat mengubah satu dari empat koordinat yang berbeda. Jadi .   "
},
{
  "id": "o003-c90-ch04-mastery-01",
  "level": "2",
  "url": "o003-c90-ch04-mastery.html#o003-c90-ch04-mastery-01",
  "type": "Pemeriksaan",
  "number": "D.9",
  "title": "Penguasaan 1: lintasan geodesik Hamming.",
  "body": "Penguasaan 1: lintasan geodesik Hamming  Dalam , ambil , , dan . Hitung ketiga jarak pasangan dan tentukan apakah pertidaksamaan segitiga menjadi kesamaan melalui .   Petunjuk. Tandai koordinat yang berbeda untuk setiap pasangan secara terpisah.   , , dan ; jadi kesamaan segitiga berlaku.   Kata berbeda pada koordinat , sehingga . Kata berbeda pada koordinat , sehingga jaraknya . Kata hanya berbeda pada koordinat kelima, sehingga jaraknya . Maka ; berada pada suatu lintasan terpendek dari ke dalam kubus Hamming.  "
},
{
  "id": "o003-c90-ch04-mastery-02",
  "level": "2",
  "url": "o003-c90-ch04-mastery.html#o003-c90-ch04-mastery-02",
  "type": "Pemeriksaan",
  "number": "D.10",
  "title": "Penguasaan 2: kapan dekode terdekat bersifat unik.",
  "body": "Penguasaan 2: kapan dekode terdekat bersifat unik  Misalkan jarak minimum antara dua kata kode berbeda dalam adalah . Buktikan: jika kata diterima memenuhi untuk suatu , maka adalah satu-satunya kata kode terdekat dengan .   Petunjuk. Andaikan ada dengan , lalu gunakan pertidaksamaan segitiga pada .   Benar. Kata kode lain yang setidaknya sama dekat akan memaksa , bertentangan dengan definisi jarak minimum kode.   Andaikan , , dan . Pertidaksamaan segitiga memberi Namun dua kata kode berbeda harus berjarak sedikitnya . Kontradiksi ini menunjukkan bahwa tidak ada yang sama dekat atau lebih dekat daripada . Jadi dekode terdekatnya unik.  "
},
{
  "id": "o003-c90-ch04-mastery-03",
  "level": "2",
  "url": "o003-c90-ch04-mastery.html#o003-c90-ch04-mastery-03",
  "type": "Pemeriksaan",
  "number": "D.11",
  "title": "Penguasaan 3: jarak “kitten” dan “sitting”.",
  "body": "Penguasaan 3: jarak kitten dan sitting  Hitung jarak Levenshtein antara kitten dan sitting . Berikan urutan edit yang mencapai nilai tersebut dan sertakan alasan bahwa dua operasi tidak cukup.   Petunjuk. Dua substitusi dan satu penyisipan memberi batas atas; gunakan rekurensi awalan untuk batas bawah.   .   Urutan kitten → sitten → sittin → sitting memakai substitusi k menjadi s , substitusi e menjadi i , lalu penyisipan g . Jadi jaraknya paling besar tiga.  Rekurensi awalan dari pembahasan tugas Levenshtein 3, dengan kolom berlabel awalan sitting , menghasilkan baris terakhir untuk kitten  . Unsur terakhir adalah tiga. Karena rekurensi itu menguji ketiga kemungkinan operasi terakhir dan dimulai dari nilai batas yang tepat, tidak ada urutan sepanjang dua. Maka jaraknya tepat tiga.  "
},
{
  "id": "o003-c90-ch04-mastery-04",
  "level": "2",
  "url": "o003-c90-ch04-mastery.html#o003-c90-ch04-mastery-04",
  "type": "Pemeriksaan",
  "number": "D.12",
  "title": "Penguasaan 4: membandingkan Hamming dan Levenshtein.",
  "body": "Penguasaan 4: membandingkan Hamming dan Levenshtein  Untuk dua untai biner dengan panjang sama, buktikan . Tunjukkan bahwa pertidaksamaan dapat ketat dengan menghitung kedua jarak bagi dan .   Petunjuk 1. Substitusikan tepat koordinat yang berbeda untuk memperoleh batas umum.  Petunjuk 2. Pada contoh, satu penghapusan dan satu penyisipan memindahkan pola bergantian.   Selalu berlaku . Pada contoh, , sedangkan .   Jika berbeda pada koordinat, substitusikan huruf pada masing-masing koordinat tersebut dengan huruf . Urutan ini mengubah menjadi dalam operasi, sehingga minimum Levenshtein memenuhi .  Keempat koordinat dan berbeda, jadi jarak Hamming-nya empat. Untuk Levenshtein, hapus nol pertama dari 0101 sehingga diperoleh 101 , lalu sisipkan nol di ujung sehingga diperoleh 1010 ; jadi . Jaraknya bukan nol karena untainya berbeda. Jaraknya juga bukan satu: satu penyisipan atau penghapusan akan mengubah panjang, sedangkan satu substitusi hanya dapat mengubah satu dari empat koordinat yang berbeda. Jadi .  "
},
{
  "id": "o003-c90-ch05-intro-guides",
  "level": "1",
  "url": "o003-c90-ch05-intro-guides.html",
  "type": "Bagian",
  "number": "",
  "title": "Panduan untuk kegiatan pendahuluan",
  "body": " Panduan untuk kegiatan pendahuluan  Tugas 1: keberadaan batas bawah  Tentukan apakah setiap himpunan bagian dari mempunyai batas bawah, lalu benarkan jawaban dengan contoh atau argumen umum. Rubrik: gunakan definisi batas bawah dan, jika jawabannya negatif, berikan satu himpunan bagian yang tidak terbatas di bawah.   Carilah himpunan yang, untuk setiap calon batas bawah , masih memuat suatu bilangan yang lebih kecil daripada .   Tidak. Sebagai contoh, sendiri tidak mempunyai batas bawah.   Andaikan merupakan batas bawah untuk . Menurut definisi, harus berlaku untuk setiap . Akan tetapi, bilangan juga anggota dan memenuhi . Hal ini bertentangan dengan syarat bahwa adalah batas bawah. Jadi tidak mempunyai batas bawah, sehingga tidak setiap himpunan bagian dari terbatas di bawah.   Tugas 2: pertidaksamaan kuadrat  Untuk , tentukan apakah terbatas di bawah dan, jika demikian, tentukan infimumnya. Rubrik: selesaikan pertidaksamaan, nyatakan himpunannya sebagai interval, dan jelaskan mengapa titik ujung bawah adalah batas bawah terbesarnya.    Langkah 1. Bagilah pertidaksamaan dengan dan tentukan akar-akar .   Langkah 2. Karena koefisien positif, polinom bernilai negatif tepat di antara kedua akarnya.    ; himpunan ini terbatas di bawah dan .   Karena , pertidaksamaan semula setara dengan . Akar-akarnya adalah Parabola membuka ke atas, sehingga nilainya negatif tepat untuk . Jadi .  Setiap anggota lebih besar daripada , maka adalah batas bawah. Jika , pilih di antara dan ; maka tetapi , sehingga bukan batas bawah. Dengan demikian , meskipun titik itu tidak termasuk dalam karena pertidaksamaannya ketat.   Tugas 3: citra fungsi kubik  Untuk , tentukan apakah terbatas di bawah dan apakah mempunyai infimum di . Rubrik: tentukan citra fungsi kubik tersebut, bukan hanya beberapa nilainya.   Untuk sembarang , coba selesaikan persamaan terhadap .    . Karena itu tidak terbatas di bawah dan tidak mempunyai infimum yang merupakan bilangan real.   Ambil sembarang dan tetapkan . Bilangan ini real dan memenuhi . Jadi setiap bilangan real merupakan anggota , sedangkan berdasarkan definisinya ; maka . Untuk setiap calon batas bawah , bilangan lebih kecil daripada . Jadi tidak terbatas di bawah dan tidak mempunyai infimum di .   Tugas 4: jumlah dua perpangkatan  Dengan konvensi , tentukan apakah terbatas di bawah dan tentukan infimumnya. Rubrik: buktikan satu batas bawah berlaku untuk semua pasangan eksponen dan periksa apakah batas itu dicapai.   Karena eksponen positif terkecil adalah , bandingkan dengan dan dengan .   Himpunan terbatas di bawah dan ; bahkan adalah nilai minimumnya.   Untuk menurut konvensi yang dinyatakan, berlaku dan . Karena perpangkatan dengan basis lebih besar daripada satu meningkat terhadap eksponennya, dan . Akibatnya untuk setiap anggota , sehingga adalah batas bawah.  Dengan memilih , kita memperoleh . Tidak ada batas bawah yang lebih besar daripada suatu anggota himpunan, khususnya daripada . Oleh sebab itu adalah batas bawah terbesar, minimum, dan infimum .   Tugas 5: batas atas terkecil  Rumuskan definisi batas atas terkecil untuk suatu himpunan bagian dari . Rubrik: nyatakan baik syarat menjadi batas atas maupun syarat bahwa batas atas tersebut tidak melebihi batas atas lain mana pun.   Balik arah pertidaksamaan dalam dua butir definisi batas bawah terbesar: anggota berada di bawah calon batas, dan calon itu berada di bawah setiap batas atas lainnya.   Untuk yang terbatas di atas, bilangan adalah batas atas terkecil jika untuk setiap dan untuk setiap batas atas dari . Bilangan ini disebut supremum dan ditulis .   Misalkan adalah himpunan bagian tak kosong dari yang terbatas di atas. Bilangan disebut batas atas terkecil dari apabila memenuhi dua syarat berikut.   untuk setiap , sehingga adalah batas atas ;    jika adalah batas atas , maka .   Syarat kedua menyatakan bahwa tidak ada batas atas yang lebih kecil daripada . Bilangan tersebut juga disebut supremum, dan dinotasikan dengan . Aksioma kelengkapan bilangan real menjamin keberadaannya bagi setiap himpunan bagian tak kosong dari yang terbatas di atas.   "
},
{
  "id": "o003-c90-ch05-intro-task-01",
  "level": "2",
  "url": "o003-c90-ch05-intro-guides.html#o003-c90-ch05-intro-task-01",
  "type": "Pemeriksaan",
  "number": "E.1",
  "title": "Tugas 1: keberadaan batas bawah.",
  "body": "Tugas 1: keberadaan batas bawah  Tentukan apakah setiap himpunan bagian dari mempunyai batas bawah, lalu benarkan jawaban dengan contoh atau argumen umum. Rubrik: gunakan definisi batas bawah dan, jika jawabannya negatif, berikan satu himpunan bagian yang tidak terbatas di bawah.   Carilah himpunan yang, untuk setiap calon batas bawah , masih memuat suatu bilangan yang lebih kecil daripada .   Tidak. Sebagai contoh, sendiri tidak mempunyai batas bawah.   Andaikan merupakan batas bawah untuk . Menurut definisi, harus berlaku untuk setiap . Akan tetapi, bilangan juga anggota dan memenuhi . Hal ini bertentangan dengan syarat bahwa adalah batas bawah. Jadi tidak mempunyai batas bawah, sehingga tidak setiap himpunan bagian dari terbatas di bawah.  "
},
{
  "id": "o003-c90-ch05-intro-task-02",
  "level": "2",
  "url": "o003-c90-ch05-intro-guides.html#o003-c90-ch05-intro-task-02",
  "type": "Pemeriksaan",
  "number": "E.2",
  "title": "Tugas 2: pertidaksamaan kuadrat.",
  "body": "Tugas 2: pertidaksamaan kuadrat  Untuk , tentukan apakah terbatas di bawah dan, jika demikian, tentukan infimumnya. Rubrik: selesaikan pertidaksamaan, nyatakan himpunannya sebagai interval, dan jelaskan mengapa titik ujung bawah adalah batas bawah terbesarnya.    Langkah 1. Bagilah pertidaksamaan dengan dan tentukan akar-akar .   Langkah 2. Karena koefisien positif, polinom bernilai negatif tepat di antara kedua akarnya.    ; himpunan ini terbatas di bawah dan .   Karena , pertidaksamaan semula setara dengan . Akar-akarnya adalah Parabola membuka ke atas, sehingga nilainya negatif tepat untuk . Jadi .  Setiap anggota lebih besar daripada , maka adalah batas bawah. Jika , pilih di antara dan ; maka tetapi , sehingga bukan batas bawah. Dengan demikian , meskipun titik itu tidak termasuk dalam karena pertidaksamaannya ketat.  "
},
{
  "id": "o003-c90-ch05-intro-task-03",
  "level": "2",
  "url": "o003-c90-ch05-intro-guides.html#o003-c90-ch05-intro-task-03",
  "type": "Pemeriksaan",
  "number": "E.3",
  "title": "Tugas 3: citra fungsi kubik.",
  "body": "Tugas 3: citra fungsi kubik  Untuk , tentukan apakah terbatas di bawah dan apakah mempunyai infimum di . Rubrik: tentukan citra fungsi kubik tersebut, bukan hanya beberapa nilainya.   Untuk sembarang , coba selesaikan persamaan terhadap .    . Karena itu tidak terbatas di bawah dan tidak mempunyai infimum yang merupakan bilangan real.   Ambil sembarang dan tetapkan . Bilangan ini real dan memenuhi . Jadi setiap bilangan real merupakan anggota , sedangkan berdasarkan definisinya ; maka . Untuk setiap calon batas bawah , bilangan lebih kecil daripada . Jadi tidak terbatas di bawah dan tidak mempunyai infimum di .  "
},
{
  "id": "o003-c90-ch05-intro-task-04",
  "level": "2",
  "url": "o003-c90-ch05-intro-guides.html#o003-c90-ch05-intro-task-04",
  "type": "Pemeriksaan",
  "number": "E.4",
  "title": "Tugas 4: jumlah dua perpangkatan.",
  "body": "Tugas 4: jumlah dua perpangkatan  Dengan konvensi , tentukan apakah terbatas di bawah dan tentukan infimumnya. Rubrik: buktikan satu batas bawah berlaku untuk semua pasangan eksponen dan periksa apakah batas itu dicapai.   Karena eksponen positif terkecil adalah , bandingkan dengan dan dengan .   Himpunan terbatas di bawah dan ; bahkan adalah nilai minimumnya.   Untuk menurut konvensi yang dinyatakan, berlaku dan . Karena perpangkatan dengan basis lebih besar daripada satu meningkat terhadap eksponennya, dan . Akibatnya untuk setiap anggota , sehingga adalah batas bawah.  Dengan memilih , kita memperoleh . Tidak ada batas bawah yang lebih besar daripada suatu anggota himpunan, khususnya daripada . Oleh sebab itu adalah batas bawah terbesar, minimum, dan infimum .  "
},
{
  "id": "o003-c90-ch05-intro-task-05",
  "level": "2",
  "url": "o003-c90-ch05-intro-guides.html#o003-c90-ch05-intro-task-05",
  "type": "Pemeriksaan",
  "number": "E.5",
  "title": "Tugas 5: batas atas terkecil.",
  "body": "Tugas 5: batas atas terkecil  Rumuskan definisi batas atas terkecil untuk suatu himpunan bagian dari . Rubrik: nyatakan baik syarat menjadi batas atas maupun syarat bahwa batas atas tersebut tidak melebihi batas atas lain mana pun.   Balik arah pertidaksamaan dalam dua butir definisi batas bawah terbesar: anggota berada di bawah calon batas, dan calon itu berada di bawah setiap batas atas lainnya.   Untuk yang terbatas di atas, bilangan adalah batas atas terkecil jika untuk setiap dan untuk setiap batas atas dari . Bilangan ini disebut supremum dan ditulis .   Misalkan adalah himpunan bagian tak kosong dari yang terbatas di atas. Bilangan disebut batas atas terkecil dari apabila memenuhi dua syarat berikut.   untuk setiap , sehingga adalah batas atas ;    jika adalah batas atas , maka .   Syarat kedua menyatakan bahwa tidak ada batas atas yang lebih kecil daripada . Bilangan tersebut juga disebut supremum, dan dinotasikan dengan . Aksioma kelengkapan bilangan real menjamin keberadaannya bagi setiap himpunan bagian tak kosong dari yang terbatas di atas.  "
},
{
  "id": "o003-c90-ch05-point-set-guides",
  "level": "1",
  "url": "o003-c90-ch05-point-set-guides.html",
  "type": "Bagian",
  "number": "",
  "title": "Panduan untuk jarak titik ke himpunan",
  "body": " Panduan untuk jarak titik ke himpunan  Enam panduan berikut mengikuti urutan tugas pada bagian tentang jarak dari titik ke himpunan. Empat tugas pertama menyusun bukti bahwa batas bawah terbesar itu tunggal; dua tugas terakhir memeriksa keberadaan dan makna . Bukalah petunjuk, jawaban, dan pembahasan hanya setelah mencoba tiap tugas secara mandiri.  Tugas 1: memilih bentuk bukti ketunggalan  Tentukan metode untuk membuktikan bahwa himpunan mempunyai paling banyak satu batas bawah terbesar. Rubrik: nyatakan dua calon batas bawah terbesar dan jelaskan hubungan apa yang cukup dibuktikan di antara keduanya.    Langkah 1. Misalkan dan sama-sama memenuhi definisi batas bawah terbesar untuk .   Langkah 2. Carilah dua pertidaksamaan yang, jika digabungkan, memaksa .   Gunakan bukti langsung: ambil dua calon dan , lalu buktikan dan . Antisimetri urutan pada kemudian memberi .   Pernyataan ketunggalan berbentuk: jika dan keduanya merupakan batas bawah terbesar , maka keduanya sama. Karena objek-objek ini berada dalam himpunan terurut , cukup memperoleh kedua arah perbandingan, yaitu dan . Sifat antisimetri urutan real menyimpulkan . Langkah-langkah berikut menunjukkan bagaimana definisi batas bawah terbesar menghasilkan kedua pertidaksamaan itu.   Tugas 2: mengenali kedua batas bawah  Andaikan dan sama-sama merupakan batas bawah terbesar untuk . Mengapa masing-masing merupakan batas bawah ? Rubrik: gunakan bagian yang tepat dari definisi dan tuliskan pertidaksamaannya untuk setiap .    Langkah 1. Kata terbesar menambahkan suatu sifat pada sebuah objek yang lebih dahulu harus menjadi batas bawah.   Langkah 2. Terapkan syarat batas bawah sekali untuk dan sekali lagi untuk .   Itu merupakan syarat pertama dalam definisi batas bawah terbesar: untuk setiap , berlaku dan .   Sebuah batas bawah terbesar harus, pertama-tama, merupakan batas bawah. Karena adalah batas bawah terbesar , definisi memberi untuk setiap . Alasan yang sama untuk memberi untuk setiap . Jadi kedua bilangan itu berada di antara batas-batas bawah yang dapat dibandingkan oleh sifat terbesar pada langkah berikutnya.   Tugas 3: memperoleh dua pertidaksamaan  Dengan dan seperti pada tugas sebelumnya, tentukan dua kesimpulan yang diberikan oleh sifat bahwa masing-masing adalah batas bawah terbesar . Rubrik: terapkan kemaksimalan kepada , lalu kemaksimalan kepada .    Langkah 1. Setiap batas bawah bagi memenuhi apabila adalah batas bawah terbesar.   Langkah 2. Pada penerapan pertama pilih ; pada penerapan kedua tukarkan peran keduanya.   Karena adalah batas bawah dan yang terbesar, . Sebaliknya, karena adalah batas bawah dan yang terbesar, .   Sifat kedua batas bawah terbesar menyatakan bahwa setiap batas bawah dari memenuhi . Tugas sebelumnya membuktikan bahwa merupakan batas bawah, sehingga memilih menghasilkan . Dengan menukar peran keduanya, sifat terbesar dari diterapkan kepada batas bawah dan menghasilkan . Kedua arah perbandingan telah diperoleh tanpa mengasumsikan kesimpulan ketunggalan.   Tugas 4: menutup bukti ketunggalan  Selesaikan bukti bahwa batas bawah terbesar itu tunggal. Rubrik: sebutkan sifat urutan yang dipakai dan nyatakan dengan jelas bahwa setiap dua calon harus sama.    Langkah 1. Dari tugas sebelumnya diketahui sekaligus dan .   Langkah 2. Gunakan antisimetri relasi pada bilangan real.   Antisimetri memberi . Karena dua calon batas bawah terbesar mana pun harus sama, batas bawah terbesar itu tunggal.   Misalkan dan merupakan dua batas bawah terbesar bagi . Karena masing-masing merupakan batas bawah, sifat terbesar dari memberi , sedangkan sifat terbesar dari memberi . Relasi pada bersifat antisimetris, sehingga dua pertidaksamaan tersebut memaksa . Jadi tidak mungkin ada dua batas bawah terbesar yang berbeda; jika batas bawah terbesar itu ada, nilainya tunggal.   Tugas 5: keberadaan jarak titik ke himpunan  Untuk ruang metrik , titik , dan himpunan tak kosong , buktikan bahwa ada. Rubrik: buktikan bahwa himpunan nilai jarak itu tak kosong dan terbatas di bawah sebelum memakai sifat kelengkapan .    Langkah 1. Pilih satu untuk menunjukkan bahwa bukan himpunan kosong.   Langkah 2. Aksioma metrik memberi satu batas bawah yang sama bagi semua anggota .   Himpunan tak kosong karena , dan adalah batas bawahnya karena jarak selalu tak negatif. Kelengkapan bilangan real menjamin bahwa , yaitu , ada dan tunggal.   Karena tak kosong, ada . Maka bilangan real merupakan anggota , sehingga . Untuk setiap , aksioma tak-negatif metrik memberi . Jadi adalah batas bawah .  Aksioma kelengkapan menyatakan bahwa setiap himpunan real tak kosong yang terbatas di bawah mempunyai infimum. Karena kedua hipotesis itu berlaku untuk , bilangan ada. Ketunggalan batas bawah terbesar, yang dibuktikan pada empat tugas pertama, memastikan nilainya tunggal. Berdasarkan definisi, .   Tugas 6: apakah jarak nol berarti keanggotaan?  Putuskan apakah selalu mengakibatkan . Rubrik: jika pernyataan salah, berikan ruang metrik, titik, dan himpunan tak kosong yang konkret; hitung infimumnya dan jelaskan hubungan yang benar dengan penutupan .    Langkah 1. Di dengan metrik Euklides, periksa dan .   Langkah 2. Anggota dapat mendekati sedekat apa pun tanpa pernah sama dengan .   Tidak. Dalam dengan metrik Euklides, ambil dan . Maka , tetapi . Yang selalu benar dalam ruang metrik ialah jika dan hanya jika .   Gunakan ruang metrik dengan . Untuk dan , himpunan jaraknya ialah . Infimum himpunan ini adalah , sehingga . Akan tetapi, interval tidak memuat titik ujung ; jadi . Ini merupakan contoh tandingan bagi implikasi yang ditanyakan.  Makna yang tepat adalah keanggotaan dalam penutupan. Jika , maka untuk setiap terdapat dengan ; jika tidak, suatu akan menjadi batas bawah positif bagi semua jarak dan infimumnya tidak mungkin nol. Jadi setiap bola terbuka di sekitar bertemu , sehingga . Sebaliknya, jika , untuk setiap ada dengan . Karena dan untuk setiap , haruslah . Maka setara dengan , bukan dengan kecuali, misalnya, tertutup.   "
},
{
  "id": "o003-c90-ch05-pointset-task-01",
  "level": "2",
  "url": "o003-c90-ch05-point-set-guides.html#o003-c90-ch05-pointset-task-01",
  "type": "Pemeriksaan",
  "number": "E.6",
  "title": "Tugas 1: memilih bentuk bukti ketunggalan.",
  "body": "Tugas 1: memilih bentuk bukti ketunggalan  Tentukan metode untuk membuktikan bahwa himpunan mempunyai paling banyak satu batas bawah terbesar. Rubrik: nyatakan dua calon batas bawah terbesar dan jelaskan hubungan apa yang cukup dibuktikan di antara keduanya.    Langkah 1. Misalkan dan sama-sama memenuhi definisi batas bawah terbesar untuk .   Langkah 2. Carilah dua pertidaksamaan yang, jika digabungkan, memaksa .   Gunakan bukti langsung: ambil dua calon dan , lalu buktikan dan . Antisimetri urutan pada kemudian memberi .   Pernyataan ketunggalan berbentuk: jika dan keduanya merupakan batas bawah terbesar , maka keduanya sama. Karena objek-objek ini berada dalam himpunan terurut , cukup memperoleh kedua arah perbandingan, yaitu dan . Sifat antisimetri urutan real menyimpulkan . Langkah-langkah berikut menunjukkan bagaimana definisi batas bawah terbesar menghasilkan kedua pertidaksamaan itu.  "
},
{
  "id": "o003-c90-ch05-pointset-task-02",
  "level": "2",
  "url": "o003-c90-ch05-point-set-guides.html#o003-c90-ch05-pointset-task-02",
  "type": "Pemeriksaan",
  "number": "E.7",
  "title": "Tugas 2: mengenali kedua batas bawah.",
  "body": "Tugas 2: mengenali kedua batas bawah  Andaikan dan sama-sama merupakan batas bawah terbesar untuk . Mengapa masing-masing merupakan batas bawah ? Rubrik: gunakan bagian yang tepat dari definisi dan tuliskan pertidaksamaannya untuk setiap .    Langkah 1. Kata terbesar menambahkan suatu sifat pada sebuah objek yang lebih dahulu harus menjadi batas bawah.   Langkah 2. Terapkan syarat batas bawah sekali untuk dan sekali lagi untuk .   Itu merupakan syarat pertama dalam definisi batas bawah terbesar: untuk setiap , berlaku dan .   Sebuah batas bawah terbesar harus, pertama-tama, merupakan batas bawah. Karena adalah batas bawah terbesar , definisi memberi untuk setiap . Alasan yang sama untuk memberi untuk setiap . Jadi kedua bilangan itu berada di antara batas-batas bawah yang dapat dibandingkan oleh sifat terbesar pada langkah berikutnya.  "
},
{
  "id": "o003-c90-ch05-pointset-task-03",
  "level": "2",
  "url": "o003-c90-ch05-point-set-guides.html#o003-c90-ch05-pointset-task-03",
  "type": "Pemeriksaan",
  "number": "E.8",
  "title": "Tugas 3: memperoleh dua pertidaksamaan.",
  "body": "Tugas 3: memperoleh dua pertidaksamaan  Dengan dan seperti pada tugas sebelumnya, tentukan dua kesimpulan yang diberikan oleh sifat bahwa masing-masing adalah batas bawah terbesar . Rubrik: terapkan kemaksimalan kepada , lalu kemaksimalan kepada .    Langkah 1. Setiap batas bawah bagi memenuhi apabila adalah batas bawah terbesar.   Langkah 2. Pada penerapan pertama pilih ; pada penerapan kedua tukarkan peran keduanya.   Karena adalah batas bawah dan yang terbesar, . Sebaliknya, karena adalah batas bawah dan yang terbesar, .   Sifat kedua batas bawah terbesar menyatakan bahwa setiap batas bawah dari memenuhi . Tugas sebelumnya membuktikan bahwa merupakan batas bawah, sehingga memilih menghasilkan . Dengan menukar peran keduanya, sifat terbesar dari diterapkan kepada batas bawah dan menghasilkan . Kedua arah perbandingan telah diperoleh tanpa mengasumsikan kesimpulan ketunggalan.  "
},
{
  "id": "o003-c90-ch05-pointset-task-04",
  "level": "2",
  "url": "o003-c90-ch05-point-set-guides.html#o003-c90-ch05-pointset-task-04",
  "type": "Pemeriksaan",
  "number": "E.9",
  "title": "Tugas 4: menutup bukti ketunggalan.",
  "body": "Tugas 4: menutup bukti ketunggalan  Selesaikan bukti bahwa batas bawah terbesar itu tunggal. Rubrik: sebutkan sifat urutan yang dipakai dan nyatakan dengan jelas bahwa setiap dua calon harus sama.    Langkah 1. Dari tugas sebelumnya diketahui sekaligus dan .   Langkah 2. Gunakan antisimetri relasi pada bilangan real.   Antisimetri memberi . Karena dua calon batas bawah terbesar mana pun harus sama, batas bawah terbesar itu tunggal.   Misalkan dan merupakan dua batas bawah terbesar bagi . Karena masing-masing merupakan batas bawah, sifat terbesar dari memberi , sedangkan sifat terbesar dari memberi . Relasi pada bersifat antisimetris, sehingga dua pertidaksamaan tersebut memaksa . Jadi tidak mungkin ada dua batas bawah terbesar yang berbeda; jika batas bawah terbesar itu ada, nilainya tunggal.  "
},
{
  "id": "o003-c90-ch05-pointset-task-05",
  "level": "2",
  "url": "o003-c90-ch05-point-set-guides.html#o003-c90-ch05-pointset-task-05",
  "type": "Pemeriksaan",
  "number": "E.10",
  "title": "Tugas 5: keberadaan jarak titik ke himpunan.",
  "body": "Tugas 5: keberadaan jarak titik ke himpunan  Untuk ruang metrik , titik , dan himpunan tak kosong , buktikan bahwa ada. Rubrik: buktikan bahwa himpunan nilai jarak itu tak kosong dan terbatas di bawah sebelum memakai sifat kelengkapan .    Langkah 1. Pilih satu untuk menunjukkan bahwa bukan himpunan kosong.   Langkah 2. Aksioma metrik memberi satu batas bawah yang sama bagi semua anggota .   Himpunan tak kosong karena , dan adalah batas bawahnya karena jarak selalu tak negatif. Kelengkapan bilangan real menjamin bahwa , yaitu , ada dan tunggal.   Karena tak kosong, ada . Maka bilangan real merupakan anggota , sehingga . Untuk setiap , aksioma tak-negatif metrik memberi . Jadi adalah batas bawah .  Aksioma kelengkapan menyatakan bahwa setiap himpunan real tak kosong yang terbatas di bawah mempunyai infimum. Karena kedua hipotesis itu berlaku untuk , bilangan ada. Ketunggalan batas bawah terbesar, yang dibuktikan pada empat tugas pertama, memastikan nilainya tunggal. Berdasarkan definisi, .  "
},
{
  "id": "o003-c90-ch05-pointset-task-06",
  "level": "2",
  "url": "o003-c90-ch05-point-set-guides.html#o003-c90-ch05-pointset-task-06",
  "type": "Pemeriksaan",
  "number": "E.11",
  "title": "Tugas 6: apakah jarak nol berarti keanggotaan?",
  "body": "Tugas 6: apakah jarak nol berarti keanggotaan?  Putuskan apakah selalu mengakibatkan . Rubrik: jika pernyataan salah, berikan ruang metrik, titik, dan himpunan tak kosong yang konkret; hitung infimumnya dan jelaskan hubungan yang benar dengan penutupan .    Langkah 1. Di dengan metrik Euklides, periksa dan .   Langkah 2. Anggota dapat mendekati sedekat apa pun tanpa pernah sama dengan .   Tidak. Dalam dengan metrik Euklides, ambil dan . Maka , tetapi . Yang selalu benar dalam ruang metrik ialah jika dan hanya jika .   Gunakan ruang metrik dengan . Untuk dan , himpunan jaraknya ialah . Infimum himpunan ini adalah , sehingga . Akan tetapi, interval tidak memuat titik ujung ; jadi . Ini merupakan contoh tandingan bagi implikasi yang ditanyakan.  Makna yang tepat adalah keanggotaan dalam penutupan. Jika , maka untuk setiap terdapat dengan ; jika tidak, suatu akan menjadi batas bawah positif bagi semua jarak dan infimumnya tidak mungkin nol. Jadi setiap bola terbuka di sekitar bertemu , sehingga . Sebaliknya, jika , untuk setiap ada dengan . Karena dan untuk setiap , haruslah . Maka setara dengan , bukan dengan kecuali, misalnya, tertutup.  "
},
{
  "id": "o003-c90-ch05-exercise-guides-a",
  "level": "1",
  "url": "o003-c90-ch05-exercise-guides-a.html",
  "type": "Bagian",
  "number": "",
  "title": "Panduan latihan sumber, bagian pertama",
  "body": " Panduan latihan sumber, bagian pertama  Delapan belas panduan berikut berkorespondensi, dalam urutan sumber, dengan semua tugas yang memuat pernyataan pada enam latihan pertama bagian latihan Bab 5. Buka petunjuk secara bertahap; jawaban menyatakan kesimpulan langsung, sedangkan pembahasan memberikan pembuktian lengkap. Rubrik pada setiap butir menunjukkan unsur yang harus tampak dalam pekerjaan mandiri.  Translasi himpunan dan batas bawah  Misalkan tidak kosong dan terbatas di bawah, serta . Jelaskan mengapa merupakan batas bawah bagi dan mengapa mempunyai infimum. Rubrik: buktikan sifat batas bawah, ketak-kosongan, dan syarat untuk memakai aksioma kelengkapan.   Mulailah dari untuk setiap , lalu tambahkan pada kedua ruas.   Setiap memenuhi . Himpunan tidak kosong dan terbatas di bawah, sehingga aksioma kelengkapan menjamin adanya .   Karena adalah batas bawah bagi , untuk setiap berlaku . Penjumlahan dengan bilangan real mempertahankan urutan, sehingga . Setiap unsur berbentuk ; jadi memang batas bawah bagi .  Pilih , yang ada karena tidak kosong. Maka , sehingga tidak kosong. Bersama dengan batas bawah yang baru ditemukan, aksioma kelengkapan untuk menyatakan bahwa mempunyai batas bawah terbesar, yakni .   Infimum translasi himpunan  Dengan asumsi yang sama, misalkan suatu batas bawah bagi . Buktikan bahwa , lalu simpulkan . Rubrik: ubah menjadi batas bawah bagi dan gunakan sifat terbesar dari infimum.   Dari untuk semua , kurangi kedua ruas dengan .   Bilangan adalah batas bawah bagi , jadi dan . Karena sendiri merupakan batas bawah bagi , bilangan itu adalah infimumnya.   Karena batas bawah bagi , untuk setiap berlaku . Mengurangi kedua ruas dengan memberi untuk setiap . Jadi merupakan batas bawah bagi . Infimum adalah batas bawah terbesar, sehingga , atau ekuivalen dengan .  Butir sebelumnya telah membuktikan bahwa adalah batas bawah bagi . Argumen di atas membuktikan bahwa setiap batas bawah bagi tidak melebihi bilangan tersebut. Maka adalah batas bawah terbesar bagi , sehingga .   Mendekati supremum dari bawah  Misalkan tidak kosong dan terbatas di atas, serta . Buktikan bahwa untuk setiap terdapat dengan . Rubrik: gunakan kontraposisi dari sifat batas atas, bukan asumsi bahwa supremum harus berada di dalam .   Jika tidak ada yang lebih besar daripada , apakah peran bagi ?   Jika tidak ada dengan , maka adalah batas atas bagi , yang bertentangan dengan . Karena batas atas, unsur yang diperoleh juga memenuhi .   Ambil sebarang . Andaikan tidak terdapat dengan . Maka setiap memenuhi , sehingga adalah batas atas bagi . Namun, karena adalah batas atas terkecil, setiap batas atas bagi harus memenuhi . Hal ini bertentangan dengan . Jadi ada dengan . Selain itu, adalah batas atas bagi , maka . Dengan demikian .   Mendekati infimum dari atas  Misalkan tidak kosong dan terbatas di bawah, serta . Buktikan bahwa untuk setiap terdapat dengan . Rubrik: tunjukkan secara eksplisit kontradiksi yang timbul jika menjadi batas bawah.   Andaikan tidak ada dengan ; bandingkan dengan batas bawah terbesar .   Jika semua memenuhi , maka adalah batas bawah bagi , sehingga ; ini bertentangan dengan . Unsur yang diperoleh memenuhi karena batas bawah.   Ambil sebarang . Jika tidak ada dengan , maka untuk setiap . Dengan demikian merupakan batas bawah bagi . Karena adalah batas bawah terbesar, setiap batas bawah harus memenuhi , bertentangan dengan . Jadi terdapat dengan . Karena sendiri batas bawah bagi , berlaku pula . Maka .   Batas atas jumlah dua himpunan  Misalkan tidak kosong serta terbatas di atas dan di bawah. Tetapkan , , dan . Buktikan bahwa merupakan batas atas bagi . Rubrik: mulai dari dua pertidaksamaan batas atas dan kuantifikasikan atas setiap unsur .   Untuk dan , jumlahkan dan .   Setiap memenuhi ; jadi adalah batas atas bagi .   Supremum adalah batas atas bagi , sehingga untuk setiap . Demikian pula, untuk setiap . Ambil sebarang unsur . Berdasarkan definisi jumlah himpunan, terdapat dan dengan . Menjumlahkan kedua pertidaksamaan menghasilkan . Karena hal ini berlaku bagi setiap , adalah batas atas bagi .   Membandingkan dua supremum  Dengan notasi pada butir sebelumnya, misalkan . Jelaskan mengapa . Rubrik: sebutkan sifat supremum yang dipakai dan alasan ada.   Supremum tidak lebih besar daripada batas atas mana pun bagi himpunan yang sama.   Himpunan tidak kosong dan, menurut butir sebelumnya, terbatas di atas oleh . Jadi ada dan, sebagai batas atas terkecil, memenuhi .   Karena dan tidak kosong, terdapat dan , sehingga ; jadi tidak kosong. Butir sebelumnya menunjukkan bahwa merupakan batas atas bagi . Aksioma kelengkapan kemudian menjamin adanya . Supremum adalah batas atas terkecil, sehingga ia tidak dapat melebihi batas atas . Oleh karena itu .   Kesamaan supremum jumlah himpunan  Dengan , , dan , buktikan bahwa melalui kontradiksi. Jika , tetapkan dan gunakan sifat pendekatan supremum. Rubrik: pilih unsur dari kedua himpunan dengan galat yang jumlahnya kurang dari .   Pilih dan sehingga dan .   Pilihan tersebut memberi , padahal dan adalah batas atas. Maka ; bersama , diperoleh .   Kita sudah mengetahui . Andaikan dan definisikan . Karena , sifat pendekatan supremum menjamin adanya dengan . Dengan alasan yang sama, ada dengan .  Menjumlahkan dua pertidaksamaan ketat itu menghasilkan Akan tetapi, , sedangkan adalah batas atas bagi ; seharusnya . Kontradiksi ini menolak . Karena sebelumnya telah dibuktikan , satu-satunya kemungkinan ialah . Jadi .   Infimum jumlah himpunan  Buktikan bahwa . Rubrik: buktikan terlebih dahulu satu batas bawah, lalu gunakan pendekatan infimum dengan pembagian galat yang eksplisit untuk membuktikan arah sebaliknya.   Jika , , dan , gunakan untuk memilih serta .   Bilangan adalah batas bawah bagi , jadi . Jika ketat, unsur dan dapat dipilih dengan , bertentangan dengan sifat sebagai batas bawah. Jadi .   Tetapkan dan . Untuk setiap dan , berlaku dan , sehingga . Jadi adalah batas bawah bagi . Himpunan tidak kosong, maka infimumnya ada, dan sifat terbesar infimum memberi .  Andaikan dan tetapkan . Karena , sifat pendekatan infimum memberi dengan . Demikian pula, ada dengan . Maka Ini mustahil karena dan adalah batas bawah bagi , yang mengharuskan . Jadi . Bersama , diperoleh .   Supremum suatu gabungan  Buktikan atau bantah pernyataan berikut. Rubrik: putuskan nilai kebenarannya dan verifikasi dua syarat batas atas terkecil.   Setiap unsur gabungan berasal dari atau ; setiap batas atas bagi gabungan juga membatasi keduanya.   Pernyataan benar. Bilangan membatasi dari atas, dan setiap batas atas bagi sedikitnya sebesar .   Tetapkan . Jika , maka atau . Dalam kasus pertama, ; dalam kasus kedua, . Jadi adalah batas atas bagi .  Sekarang misalkan sebarang batas atas bagi . Karena dan , adalah batas atas bagi dan bagi . Maka dan , sehingga . Jadi adalah batas atas terkecil, yang membuktikan kesamaan tersebut.   Infimum suatu gabungan  Buktikan atau bantah pernyataan berikut. Rubrik: putuskan nilai kebenarannya dan verifikasi dua syarat batas bawah terbesar.   Gunakan bahwa setiap unsur gabungan berada dalam salah satu himpunan dan setiap batas bawah bagi gabungan membatasi keduanya.   Pernyataan benar. Bilangan membatasi dari bawah, dan setiap batas bawah bagi gabungan tidak melebihi .   Tetapkan . Jika , maka atau . Jika , maka ; jika , maka . Jadi adalah batas bawah bagi .  Misalkan sebarang batas bawah bagi . Karena , adalah batas bawah bagi dan bagi . Maka dan , sehingga . Jadi adalah batas bawah terbesar dan kesamaan yang diminta berlaku.   Menghitung metrik supremum  Pada dengan , hitung . Rubrik: tentukan supremum nilai mutlak pada seluruh interval dan tunjukkan bahwa nilainya dicapai.   Fungsi meningkat pada ; bandingkan nilai mutlak pada kedua ujung rentangnya.   , dan jarak maksimum itu dicapai pada .   Selisih kedua fungsi adalah . Untuk , sehingga meningkat pada . Karena dan , setiap berada dalam . Maka untuk semua . Pada , , sehingga batas atas ini dicapai dan . Jadi .   Membuktikan metrik seragam pada ruang fungsi  Misalkan , dengan , dan definisikan . Buktikan bahwa merupakan metrik dan jelaskan makna geometrisnya. Rubrik: buktikan nilai supremum berhingga serta keempat aksioma metrik, lalu identifikasi jarak vertikal maksimum antara dua graf.   Gunakan kekompakan untuk keberadaan maksimum dan terapkan pertidaksamaan segitiga nilai mutlak secara titik-demi-titik sebelum mengambil supremum.   Fungsi kontinu pada interval kompak, sehingga supremumnya berhingga dan dicapai. Fungsi tak negatif, nol tepat untuk , simetris, dan memenuhi pertidaksamaan segitiga. Secara geometris, adalah pemisahan vertikal terbesar antara graf dan pada interval tersebut.   Untuk , fungsi kontinu. Teorema nilai ekstrem pada interval kompak menjamin bahwa fungsi ini mencapai suatu maksimum berhingga. Jadi terdefinisi sebagai bilangan real tak negatif.  Jelas . Jika , maka seluruh selisih bernilai nol, sehingga . Sebaliknya, jika , maka untuk setiap , . Jadi untuk setiap , yakni . Selanjutnya, pada setiap , maka .  Untuk dan setiap , Ruas kanan adalah batas atas yang tidak bergantung pada . Mengambil supremum atas pada ruas kiri memberi . Jadi keempat aksioma metrik terpenuhi. Nilai adalah jarak vertikal kedua graf di absis ; supremum, yang di sini merupakan maksimum, adalah jarak vertikal terbesar pada seluruh interval. Itulah alasan nama metrik supremum atau metrik seragam .   Asumsi negasi sifat Archimedes  Misalkan . Andaikan tidak ada bilangan bulat positif dengan . Jelaskan mengapa terbatas di atas. Rubrik: terjemahkan negasi kuantor dengan tepat dan berikan batas atas yang eksplisit.   Negasi “ada dengan ” adalah “untuk setiap , .”   Asumsi tersebut menyatakan bagi setiap . Jadi adalah batas atas bagi , dan terbatas di atas.   Pernyataan yang diandaikan salah adalah . Negasinya ialah . Dengan demikian setiap unsur tidak melebihi bilangan real . Menurut definisi, adalah batas atas bagi ; karena itu terbatas di atas.   Supremum bilangan bulat positif  Dengan mengandaikan terbatas di atas, jelaskan mengapa terdapat batas atas terkecil bagi . Rubrik: verifikasi ketak-kosongan dan terapkan aksioma kelengkapan dengan tepat.   Himpunan memuat dan, menurut asumsi, mempunyai suatu batas atas real.   Karena , himpunan itu tidak kosong; menurut asumsi, himpunan itu terbatas di atas. Aksioma kelengkapan menjamin adanya , yaitu batas atas terkecilnya.   Aksioma kelengkapan menyatakan bahwa setiap subhimpunan tak kosong dari yang terbatas di atas mempunyai supremum. Himpunan merupakan subhimpunan dan tidak kosong karena memuat . Dalam argumen kontradiksi ini, keterbatasannya di atas sedang diandaikan. Karena semua hipotesis aksioma kelengkapan terpenuhi, terdapat . Berdasarkan definisi supremum, adalah batas atas terkecil bagi .   Kontradiksi yang membuktikan sifat Archimedes  Andaikan . Buktikan bahwa tidak mungkin menjadi batas atas terkecil, lalu simpulkan sifat Archimedes. Rubrik: gunakan untuk memperoleh bilangan bulat positif yang menghasilkan unsur baru di atas .   Karena lebih kecil daripada supremum, ia bukan batas atas; pilih dengan dan perhatikan .   Ada dengan , sehingga dan . Ini bertentangan dengan sebagai batas atas. Jadi tidak terbatas di atas, yang persis menyatakan bahwa untuk setiap ada dengan .   Karena , bilangan tidak dapat menjadi batas atas bagi ; jika ia batas atas, sifat terkecil supremum akan memberi . Jadi terdapat dengan . Penambahan satu memberi . Akan tetapi, juga bilangan bulat positif, sehingga . Ini bertentangan dengan asumsi bahwa adalah batas atas bagi .  Kontradiksi tersebut berasal dari asumsi awal bahwa, untuk suatu , tidak ada bilangan bulat positif yang lebih besar daripada . Maka asumsi itu salah untuk setiap : bagi setiap terdapat dengan . Inilah sifat Archimedes.   Dari sifat Archimedes menuju bentuk berskala  Misalkan dengan . Dengan mengandaikan sifat Archimedes, buktikan bahwa ada sedemikian sehingga . Rubrik: terapkan sifat Archimedes pada hasil bagi yang tepat dan perhatikan arah pertidaksamaan ketika mengalikan.   Terapkan sifat Archimedes pada bilangan real .   Pilih dengan . Karena , perkalian dengan memberi .   Karena , hasil bagi adalah bilangan real. Sifat Archimedes memberi bilangan bulat positif dengan . Mengalikan kedua ruas dengan tidak membalik arah pertidaksamaan, sehingga . Argumen ini juga mencakup ; tidak diperlukan asumsi tambahan pada tanda .   Dari bentuk berskala kembali ke sifat Archimedes  Andaikan bahwa untuk setiap dengan ada yang memenuhi . Buktikan sifat Archimedes dan simpulkan ekuivalensi kedua pernyataan. Rubrik: buat satu substitusi yang berlaku bagi sebarang batas real.   Dalam bentuk berskala, tetapkan faktor positif sama dengan .   Untuk sebarang , gunakan pernyataan berskala dengan dan . Diperoleh dengan , yaitu sifat Archimedes. Bersama butir sebelumnya, kedua pernyataan ekuivalen.   Ambil sebarang bilangan real . Hipotesis bentuk berskala dapat diterapkan pada dan . Maka terdapat bilangan bulat positif sehingga , yakni . Karena dipilih sebarang, ini membuktikan sifat Archimedes. Butir sebelumnya membuktikan implikasi dari sifat Archimedes ke bentuk berskala, sedangkan argumen ini membuktikan implikasi balik. Oleh sebab itu kedua pernyataan ekuivalen.   Ekuivalensi bentuk kebalikan sifat Archimedes  Buktikan bahwa pernyataan “untuk setiap terdapat dengan ” ekuivalen dengan sifat Archimedes. Rubrik: buktikan kedua arah, pisahkan kasus batas real tak positif dalam arah balik, dan jaga tanda ketika mengambil kebalikan.   Untuk arah maju gunakan . Untuk arah balik, jika batas positif, terapkan pernyataan kebalikan pada .   Sifat Archimedes pada memberi , sehingga . Sebaliknya, untuk , penerapan pernyataan pada memberi , sehingga ; untuk , ambil . Jadi sifat Archimedes berlaku.   Pertama, andaikan sifat Archimedes dan ambil sebarang . Karena , terdapat dengan . Semua bilangan ini positif. Mengalikan dengan memberi . Jadi bentuk kebalikan mengikuti dari sifat Archimedes.  Sebaliknya, andaikan untuk setiap terdapat dengan . Ambil sebarang . Jika , bilangan memenuhi . Jika , terapkan hipotesis pada . Terdapat dengan . Mengalikan dengan menghasilkan . Dalam kedua kasus ada bilangan bulat positif . Karena sebarang, sifat Archimedes berlaku. Kedua implikasi telah dibuktikan, maka kedua pernyataan ekuivalen.   "
},
{
  "id": "o003-c90-ch05-exercise-task-01",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-01",
  "type": "Pemeriksaan",
  "number": "E.12",
  "title": "Translasi himpunan dan batas bawah.",
  "body": "Translasi himpunan dan batas bawah  Misalkan tidak kosong dan terbatas di bawah, serta . Jelaskan mengapa merupakan batas bawah bagi dan mengapa mempunyai infimum. Rubrik: buktikan sifat batas bawah, ketak-kosongan, dan syarat untuk memakai aksioma kelengkapan.   Mulailah dari untuk setiap , lalu tambahkan pada kedua ruas.   Setiap memenuhi . Himpunan tidak kosong dan terbatas di bawah, sehingga aksioma kelengkapan menjamin adanya .   Karena adalah batas bawah bagi , untuk setiap berlaku . Penjumlahan dengan bilangan real mempertahankan urutan, sehingga . Setiap unsur berbentuk ; jadi memang batas bawah bagi .  Pilih , yang ada karena tidak kosong. Maka , sehingga tidak kosong. Bersama dengan batas bawah yang baru ditemukan, aksioma kelengkapan untuk menyatakan bahwa mempunyai batas bawah terbesar, yakni .  "
},
{
  "id": "o003-c90-ch05-exercise-task-02",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-02",
  "type": "Pemeriksaan",
  "number": "E.13",
  "title": "Infimum translasi himpunan.",
  "body": "Infimum translasi himpunan  Dengan asumsi yang sama, misalkan suatu batas bawah bagi . Buktikan bahwa , lalu simpulkan . Rubrik: ubah menjadi batas bawah bagi dan gunakan sifat terbesar dari infimum.   Dari untuk semua , kurangi kedua ruas dengan .   Bilangan adalah batas bawah bagi , jadi dan . Karena sendiri merupakan batas bawah bagi , bilangan itu adalah infimumnya.   Karena batas bawah bagi , untuk setiap berlaku . Mengurangi kedua ruas dengan memberi untuk setiap . Jadi merupakan batas bawah bagi . Infimum adalah batas bawah terbesar, sehingga , atau ekuivalen dengan .  Butir sebelumnya telah membuktikan bahwa adalah batas bawah bagi . Argumen di atas membuktikan bahwa setiap batas bawah bagi tidak melebihi bilangan tersebut. Maka adalah batas bawah terbesar bagi , sehingga .  "
},
{
  "id": "o003-c90-ch05-exercise-task-03",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-03",
  "type": "Pemeriksaan",
  "number": "E.14",
  "title": "Mendekati supremum dari bawah.",
  "body": "Mendekati supremum dari bawah  Misalkan tidak kosong dan terbatas di atas, serta . Buktikan bahwa untuk setiap terdapat dengan . Rubrik: gunakan kontraposisi dari sifat batas atas, bukan asumsi bahwa supremum harus berada di dalam .   Jika tidak ada yang lebih besar daripada , apakah peran bagi ?   Jika tidak ada dengan , maka adalah batas atas bagi , yang bertentangan dengan . Karena batas atas, unsur yang diperoleh juga memenuhi .   Ambil sebarang . Andaikan tidak terdapat dengan . Maka setiap memenuhi , sehingga adalah batas atas bagi . Namun, karena adalah batas atas terkecil, setiap batas atas bagi harus memenuhi . Hal ini bertentangan dengan . Jadi ada dengan . Selain itu, adalah batas atas bagi , maka . Dengan demikian .  "
},
{
  "id": "o003-c90-ch05-exercise-task-04",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-04",
  "type": "Pemeriksaan",
  "number": "E.15",
  "title": "Mendekati infimum dari atas.",
  "body": "Mendekati infimum dari atas  Misalkan tidak kosong dan terbatas di bawah, serta . Buktikan bahwa untuk setiap terdapat dengan . Rubrik: tunjukkan secara eksplisit kontradiksi yang timbul jika menjadi batas bawah.   Andaikan tidak ada dengan ; bandingkan dengan batas bawah terbesar .   Jika semua memenuhi , maka adalah batas bawah bagi , sehingga ; ini bertentangan dengan . Unsur yang diperoleh memenuhi karena batas bawah.   Ambil sebarang . Jika tidak ada dengan , maka untuk setiap . Dengan demikian merupakan batas bawah bagi . Karena adalah batas bawah terbesar, setiap batas bawah harus memenuhi , bertentangan dengan . Jadi terdapat dengan . Karena sendiri batas bawah bagi , berlaku pula . Maka .  "
},
{
  "id": "o003-c90-ch05-exercise-task-05",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-05",
  "type": "Pemeriksaan",
  "number": "E.16",
  "title": "Batas atas jumlah dua himpunan.",
  "body": "Batas atas jumlah dua himpunan  Misalkan tidak kosong serta terbatas di atas dan di bawah. Tetapkan , , dan . Buktikan bahwa merupakan batas atas bagi . Rubrik: mulai dari dua pertidaksamaan batas atas dan kuantifikasikan atas setiap unsur .   Untuk dan , jumlahkan dan .   Setiap memenuhi ; jadi adalah batas atas bagi .   Supremum adalah batas atas bagi , sehingga untuk setiap . Demikian pula, untuk setiap . Ambil sebarang unsur . Berdasarkan definisi jumlah himpunan, terdapat dan dengan . Menjumlahkan kedua pertidaksamaan menghasilkan . Karena hal ini berlaku bagi setiap , adalah batas atas bagi .  "
},
{
  "id": "o003-c90-ch05-exercise-task-06",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-06",
  "type": "Pemeriksaan",
  "number": "E.17",
  "title": "Membandingkan dua supremum.",
  "body": "Membandingkan dua supremum  Dengan notasi pada butir sebelumnya, misalkan . Jelaskan mengapa . Rubrik: sebutkan sifat supremum yang dipakai dan alasan ada.   Supremum tidak lebih besar daripada batas atas mana pun bagi himpunan yang sama.   Himpunan tidak kosong dan, menurut butir sebelumnya, terbatas di atas oleh . Jadi ada dan, sebagai batas atas terkecil, memenuhi .   Karena dan tidak kosong, terdapat dan , sehingga ; jadi tidak kosong. Butir sebelumnya menunjukkan bahwa merupakan batas atas bagi . Aksioma kelengkapan kemudian menjamin adanya . Supremum adalah batas atas terkecil, sehingga ia tidak dapat melebihi batas atas . Oleh karena itu .  "
},
{
  "id": "o003-c90-ch05-exercise-task-07",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-07",
  "type": "Pemeriksaan",
  "number": "E.18",
  "title": "Kesamaan supremum jumlah himpunan.",
  "body": "Kesamaan supremum jumlah himpunan  Dengan , , dan , buktikan bahwa melalui kontradiksi. Jika , tetapkan dan gunakan sifat pendekatan supremum. Rubrik: pilih unsur dari kedua himpunan dengan galat yang jumlahnya kurang dari .   Pilih dan sehingga dan .   Pilihan tersebut memberi , padahal dan adalah batas atas. Maka ; bersama , diperoleh .   Kita sudah mengetahui . Andaikan dan definisikan . Karena , sifat pendekatan supremum menjamin adanya dengan . Dengan alasan yang sama, ada dengan .  Menjumlahkan dua pertidaksamaan ketat itu menghasilkan Akan tetapi, , sedangkan adalah batas atas bagi ; seharusnya . Kontradiksi ini menolak . Karena sebelumnya telah dibuktikan , satu-satunya kemungkinan ialah . Jadi .  "
},
{
  "id": "o003-c90-ch05-exercise-task-08",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-08",
  "type": "Pemeriksaan",
  "number": "E.19",
  "title": "Infimum jumlah himpunan.",
  "body": "Infimum jumlah himpunan  Buktikan bahwa . Rubrik: buktikan terlebih dahulu satu batas bawah, lalu gunakan pendekatan infimum dengan pembagian galat yang eksplisit untuk membuktikan arah sebaliknya.   Jika , , dan , gunakan untuk memilih serta .   Bilangan adalah batas bawah bagi , jadi . Jika ketat, unsur dan dapat dipilih dengan , bertentangan dengan sifat sebagai batas bawah. Jadi .   Tetapkan dan . Untuk setiap dan , berlaku dan , sehingga . Jadi adalah batas bawah bagi . Himpunan tidak kosong, maka infimumnya ada, dan sifat terbesar infimum memberi .  Andaikan dan tetapkan . Karena , sifat pendekatan infimum memberi dengan . Demikian pula, ada dengan . Maka Ini mustahil karena dan adalah batas bawah bagi , yang mengharuskan . Jadi . Bersama , diperoleh .  "
},
{
  "id": "o003-c90-ch05-exercise-task-09",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-09",
  "type": "Pemeriksaan",
  "number": "E.20",
  "title": "Supremum suatu gabungan.",
  "body": "Supremum suatu gabungan  Buktikan atau bantah pernyataan berikut. Rubrik: putuskan nilai kebenarannya dan verifikasi dua syarat batas atas terkecil.   Setiap unsur gabungan berasal dari atau ; setiap batas atas bagi gabungan juga membatasi keduanya.   Pernyataan benar. Bilangan membatasi dari atas, dan setiap batas atas bagi sedikitnya sebesar .   Tetapkan . Jika , maka atau . Dalam kasus pertama, ; dalam kasus kedua, . Jadi adalah batas atas bagi .  Sekarang misalkan sebarang batas atas bagi . Karena dan , adalah batas atas bagi dan bagi . Maka dan , sehingga . Jadi adalah batas atas terkecil, yang membuktikan kesamaan tersebut.  "
},
{
  "id": "o003-c90-ch05-exercise-task-10",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-10",
  "type": "Pemeriksaan",
  "number": "E.21",
  "title": "Infimum suatu gabungan.",
  "body": "Infimum suatu gabungan  Buktikan atau bantah pernyataan berikut. Rubrik: putuskan nilai kebenarannya dan verifikasi dua syarat batas bawah terbesar.   Gunakan bahwa setiap unsur gabungan berada dalam salah satu himpunan dan setiap batas bawah bagi gabungan membatasi keduanya.   Pernyataan benar. Bilangan membatasi dari bawah, dan setiap batas bawah bagi gabungan tidak melebihi .   Tetapkan . Jika , maka atau . Jika , maka ; jika , maka . Jadi adalah batas bawah bagi .  Misalkan sebarang batas bawah bagi . Karena , adalah batas bawah bagi dan bagi . Maka dan , sehingga . Jadi adalah batas bawah terbesar dan kesamaan yang diminta berlaku.  "
},
{
  "id": "o003-c90-ch05-exercise-task-11",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-11",
  "type": "Pemeriksaan",
  "number": "E.22",
  "title": "Menghitung metrik supremum.",
  "body": "Menghitung metrik supremum  Pada dengan , hitung . Rubrik: tentukan supremum nilai mutlak pada seluruh interval dan tunjukkan bahwa nilainya dicapai.   Fungsi meningkat pada ; bandingkan nilai mutlak pada kedua ujung rentangnya.   , dan jarak maksimum itu dicapai pada .   Selisih kedua fungsi adalah . Untuk , sehingga meningkat pada . Karena dan , setiap berada dalam . Maka untuk semua . Pada , , sehingga batas atas ini dicapai dan . Jadi .  "
},
{
  "id": "o003-c90-ch05-exercise-task-12",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-12",
  "type": "Pemeriksaan",
  "number": "E.23",
  "title": "Membuktikan metrik seragam pada ruang fungsi.",
  "body": "Membuktikan metrik seragam pada ruang fungsi  Misalkan , dengan , dan definisikan . Buktikan bahwa merupakan metrik dan jelaskan makna geometrisnya. Rubrik: buktikan nilai supremum berhingga serta keempat aksioma metrik, lalu identifikasi jarak vertikal maksimum antara dua graf.   Gunakan kekompakan untuk keberadaan maksimum dan terapkan pertidaksamaan segitiga nilai mutlak secara titik-demi-titik sebelum mengambil supremum.   Fungsi kontinu pada interval kompak, sehingga supremumnya berhingga dan dicapai. Fungsi tak negatif, nol tepat untuk , simetris, dan memenuhi pertidaksamaan segitiga. Secara geometris, adalah pemisahan vertikal terbesar antara graf dan pada interval tersebut.   Untuk , fungsi kontinu. Teorema nilai ekstrem pada interval kompak menjamin bahwa fungsi ini mencapai suatu maksimum berhingga. Jadi terdefinisi sebagai bilangan real tak negatif.  Jelas . Jika , maka seluruh selisih bernilai nol, sehingga . Sebaliknya, jika , maka untuk setiap , . Jadi untuk setiap , yakni . Selanjutnya, pada setiap , maka .  Untuk dan setiap , Ruas kanan adalah batas atas yang tidak bergantung pada . Mengambil supremum atas pada ruas kiri memberi . Jadi keempat aksioma metrik terpenuhi. Nilai adalah jarak vertikal kedua graf di absis ; supremum, yang di sini merupakan maksimum, adalah jarak vertikal terbesar pada seluruh interval. Itulah alasan nama metrik supremum atau metrik seragam .  "
},
{
  "id": "o003-c90-ch05-exercise-task-13",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-13",
  "type": "Pemeriksaan",
  "number": "E.24",
  "title": "Asumsi negasi sifat Archimedes.",
  "body": "Asumsi negasi sifat Archimedes  Misalkan . Andaikan tidak ada bilangan bulat positif dengan . Jelaskan mengapa terbatas di atas. Rubrik: terjemahkan negasi kuantor dengan tepat dan berikan batas atas yang eksplisit.   Negasi “ada dengan ” adalah “untuk setiap , .”   Asumsi tersebut menyatakan bagi setiap . Jadi adalah batas atas bagi , dan terbatas di atas.   Pernyataan yang diandaikan salah adalah . Negasinya ialah . Dengan demikian setiap unsur tidak melebihi bilangan real . Menurut definisi, adalah batas atas bagi ; karena itu terbatas di atas.  "
},
{
  "id": "o003-c90-ch05-exercise-task-14",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-14",
  "type": "Pemeriksaan",
  "number": "E.25",
  "title": "Supremum bilangan bulat positif.",
  "body": "Supremum bilangan bulat positif  Dengan mengandaikan terbatas di atas, jelaskan mengapa terdapat batas atas terkecil bagi . Rubrik: verifikasi ketak-kosongan dan terapkan aksioma kelengkapan dengan tepat.   Himpunan memuat dan, menurut asumsi, mempunyai suatu batas atas real.   Karena , himpunan itu tidak kosong; menurut asumsi, himpunan itu terbatas di atas. Aksioma kelengkapan menjamin adanya , yaitu batas atas terkecilnya.   Aksioma kelengkapan menyatakan bahwa setiap subhimpunan tak kosong dari yang terbatas di atas mempunyai supremum. Himpunan merupakan subhimpunan dan tidak kosong karena memuat . Dalam argumen kontradiksi ini, keterbatasannya di atas sedang diandaikan. Karena semua hipotesis aksioma kelengkapan terpenuhi, terdapat . Berdasarkan definisi supremum, adalah batas atas terkecil bagi .  "
},
{
  "id": "o003-c90-ch05-exercise-task-15",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-15",
  "type": "Pemeriksaan",
  "number": "E.26",
  "title": "Kontradiksi yang membuktikan sifat Archimedes.",
  "body": "Kontradiksi yang membuktikan sifat Archimedes  Andaikan . Buktikan bahwa tidak mungkin menjadi batas atas terkecil, lalu simpulkan sifat Archimedes. Rubrik: gunakan untuk memperoleh bilangan bulat positif yang menghasilkan unsur baru di atas .   Karena lebih kecil daripada supremum, ia bukan batas atas; pilih dengan dan perhatikan .   Ada dengan , sehingga dan . Ini bertentangan dengan sebagai batas atas. Jadi tidak terbatas di atas, yang persis menyatakan bahwa untuk setiap ada dengan .   Karena , bilangan tidak dapat menjadi batas atas bagi ; jika ia batas atas, sifat terkecil supremum akan memberi . Jadi terdapat dengan . Penambahan satu memberi . Akan tetapi, juga bilangan bulat positif, sehingga . Ini bertentangan dengan asumsi bahwa adalah batas atas bagi .  Kontradiksi tersebut berasal dari asumsi awal bahwa, untuk suatu , tidak ada bilangan bulat positif yang lebih besar daripada . Maka asumsi itu salah untuk setiap : bagi setiap terdapat dengan . Inilah sifat Archimedes.  "
},
{
  "id": "o003-c90-ch05-exercise-task-16",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-16",
  "type": "Pemeriksaan",
  "number": "E.27",
  "title": "Dari sifat Archimedes menuju bentuk berskala.",
  "body": "Dari sifat Archimedes menuju bentuk berskala  Misalkan dengan . Dengan mengandaikan sifat Archimedes, buktikan bahwa ada sedemikian sehingga . Rubrik: terapkan sifat Archimedes pada hasil bagi yang tepat dan perhatikan arah pertidaksamaan ketika mengalikan.   Terapkan sifat Archimedes pada bilangan real .   Pilih dengan . Karena , perkalian dengan memberi .   Karena , hasil bagi adalah bilangan real. Sifat Archimedes memberi bilangan bulat positif dengan . Mengalikan kedua ruas dengan tidak membalik arah pertidaksamaan, sehingga . Argumen ini juga mencakup ; tidak diperlukan asumsi tambahan pada tanda .  "
},
{
  "id": "o003-c90-ch05-exercise-task-17",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-17",
  "type": "Pemeriksaan",
  "number": "E.28",
  "title": "Dari bentuk berskala kembali ke sifat Archimedes.",
  "body": "Dari bentuk berskala kembali ke sifat Archimedes  Andaikan bahwa untuk setiap dengan ada yang memenuhi . Buktikan sifat Archimedes dan simpulkan ekuivalensi kedua pernyataan. Rubrik: buat satu substitusi yang berlaku bagi sebarang batas real.   Dalam bentuk berskala, tetapkan faktor positif sama dengan .   Untuk sebarang , gunakan pernyataan berskala dengan dan . Diperoleh dengan , yaitu sifat Archimedes. Bersama butir sebelumnya, kedua pernyataan ekuivalen.   Ambil sebarang bilangan real . Hipotesis bentuk berskala dapat diterapkan pada dan . Maka terdapat bilangan bulat positif sehingga , yakni . Karena dipilih sebarang, ini membuktikan sifat Archimedes. Butir sebelumnya membuktikan implikasi dari sifat Archimedes ke bentuk berskala, sedangkan argumen ini membuktikan implikasi balik. Oleh sebab itu kedua pernyataan ekuivalen.  "
},
{
  "id": "o003-c90-ch05-exercise-task-18",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-a.html#o003-c90-ch05-exercise-task-18",
  "type": "Pemeriksaan",
  "number": "E.29",
  "title": "Ekuivalensi bentuk kebalikan sifat Archimedes.",
  "body": "Ekuivalensi bentuk kebalikan sifat Archimedes  Buktikan bahwa pernyataan “untuk setiap terdapat dengan ” ekuivalen dengan sifat Archimedes. Rubrik: buktikan kedua arah, pisahkan kasus batas real tak positif dalam arah balik, dan jaga tanda ketika mengambil kebalikan.   Untuk arah maju gunakan . Untuk arah balik, jika batas positif, terapkan pernyataan kebalikan pada .   Sifat Archimedes pada memberi , sehingga . Sebaliknya, untuk , penerapan pernyataan pada memberi , sehingga ; untuk , ambil . Jadi sifat Archimedes berlaku.   Pertama, andaikan sifat Archimedes dan ambil sebarang . Karena , terdapat dengan . Semua bilangan ini positif. Mengalikan dengan memberi . Jadi bentuk kebalikan mengikuti dari sifat Archimedes.  Sebaliknya, andaikan untuk setiap terdapat dengan . Ambil sebarang . Jika , bilangan memenuhi . Jika , terapkan hipotesis pada . Terdapat dengan . Mengalikan dengan menghasilkan . Dalam kedua kasus ada bilangan bulat positif . Karena sebarang, sifat Archimedes berlaku. Kedua implikasi telah dibuktikan, maka kedua pernyataan ekuivalen.  "
},
{
  "id": "o003-c90-ch05-exercise-guides-b",
  "level": "1",
  "url": "o003-c90-ch05-exercise-guides-b.html",
  "type": "Bagian",
  "number": "",
  "title": "Panduan latihan sumber, bagian kedua",
  "body": " Panduan latihan sumber, bagian kedua  Panduan ini mengikuti sembilan belas tugas pada Latihan 7–13 secara berurutan. Setiap pembahasan mempertahankan tujuan pembuktian pada sumber; bukalah petunjuk, jawaban, dan solusi secara bertahap setelah mencoba tugas secara mandiri.  Tugas 19: batas bawah bagi himpunan bilangan bulat  Untuk , buktikan bahwa terbatas di bawah. Rubrik: berikan satu batas bawah real yang berlaku untuk setiap dan hubungkan langsung dengan syarat pembentuk .    Langkah 1. Tidak perlu mencari suatu bilangan bulat sebagai batas bawah; batas bawah boleh berupa sebarang bilangan real.   Langkah 2. Setiap memenuhi .   Bilangan adalah batas bawah bagi , sebab untuk setiap .   Berdasarkan definisi , jika , maka . Dengan demikian untuk setiap anggota . Ini tepat merupakan definisi bahwa adalah batas bawah bagi . Karena , himpunan terbatas di bawah dalam .   Tugas 20: anggota bulat terkecil  Tunjukkan bahwa memuat suatu bilangan bulat sedemikian sehingga setiap dengan memenuhi . Rubrik: terapkan Prinsip Pengurutan Baik kepada , lalu gunakan keminimalan anggota yang diperoleh.    Langkah 1. Himpunan tak kosong dan, menurut tugas sebelumnya, terbatas di bawah; semua anggotanya bilangan bulat.   Langkah 2. Jika tetapi , di manakah letak terhadap anggota terkecil dari ?   Prinsip Pengurutan Baik memberi anggota terkecil . Jika dan , maka tidak mungkin memenuhi ; jadi .   Sifat Archimedes menjamin bahwa tak kosong, sedangkan Tugas 19 menunjukkan bahwa terbatas di bawah. Karena , Prinsip Pengurutan Baik yang dinyatakan pada latihan sumber memastikan bahwa memuat infimumnya. Tuliskan anggota terkecil ini sebagai ; khususnya .  Ambil dengan . Andaikan . Syarat ini dan fakta bahwa bilangan bulat akan memberi , bertentangan dengan keminimalan karena . Jadi pengandaian tersebut salah dan harus berlaku .   Tugas 21: bilangan rasional di antara dua bilangan real  Gunakan anggota terkecil untuk membuktikan , lalu temukan bilangan rasional di antara dan . Rubrik: terapkan hasil tugas sebelumnya kepada dan gunakan .    Langkah 1. Karena , langsung diperoleh satu dari dua pertidaksamaan. Untuk yang lain, masukkan ke hasil Tugas 20.   Langkah 2. Ubah menjadi , kemudian bagi rantai pertidaksamaan dengan .   Berlaku . Karena itu , dan adalah bilangan rasional yang dicari.   Karena , definisi memberi . Bilangan adalah bilangan bulat dan memenuhi . Maka Tugas 20, dengan , memberi , atau setara dengan .  Dari diperoleh , sehingga . Menggabungkan semuanya menghasilkan Karena bilangan bulat positif, pembagian dengan mempertahankan arah pertidaksamaan dan memberi . Dengan dan , bilangan rasional. Jadi setiap interval terbuka tak kosong di memuat suatu bilangan rasional.   Tugas 22: titik rasional dalam bola Euklides  Buktikan bahwa setiap bola terbuka dalam memuat titik yang kedua koordinatnya rasional. Rubrik: mulai dari pusat dan jari-jari bola, pilih satu bilangan rasional dekat dengan tiap koordinat pusat, lalu perkirakan jarak Euklidesnya.    Langkah 1. Untuk bola berpusat berjari-jari , gunakan kerapatan untuk memilih .   Langkah 2. Gunakan .   Pilih dengan . Untuk , berlaku ; jadi berada dalam bola dan kedua koordinatnya rasional.   Misalkan suatu bola terbuka dengan dan . Berdasarkan kerapatan bilangan rasional dalam bilangan real, terdapat sedemikian sehingga dan . Tetapkan .  Untuk bilangan real , kedua ruas tak negatif dan , sehingga . Karena itu Maka , dan kedua koordinat rasional sebagaimana diminta.   Tugas 23: membentuk calon akar kuadrat  Untuk , buktikan bahwa mempunyai batas bawah terbesar . Rubrik: tunjukkan bahwa tak kosong dan berikan satu batas bawahnya sebelum memakai kelengkapan .    Langkah 1. Periksa bahwa .   Langkah 2. Jika , maka ; jadi setiap anggota lebih besar daripada .   Himpunan tak kosong karena , dan adalah batas bawahnya. Kelengkapan memberi ; selain itu .   Bilangan positif dan , sehingga dan tak kosong. Jika , maka dan . Seandainya , akan berlaku , suatu kontradiksi. Jadi untuk setiap , dan adalah batas bawah .  Aksioma kelengkapan bilangan real menjamin bahwa himpunan real tak kosong yang terbatas di bawah mempunyai infimum. Maka ada. Karena adalah batas bawah, ; karena dan infimum tidak melebihi setiap anggota himpunan, .   Tugas 24: menyingkirkan kasus  Andaikan . Pilih sehingga , lalu jelaskan kontradiksinya. Rubrik: buat pilihan kuantitatif untuk dan buktikan bahwa menjadi batas bawah yang lebih besar daripada .    Langkah 1. Tetapkan dan gunakan sifat Archimedes untuk memilih .   Langkah 2. Untuk , berlaku . Jika kuadrat suatu bilangan positif kurang daripada , bandingkan dengan semua anggota .   Dengan , pilih . Maka . Bilangan lalu merupakan batas bawah yang lebih besar daripada , suatu kontradiksi.   Andaikan dan tetapkan . Sifat Archimedes memberi bilangan bulat positif dengan . Karena , diperoleh   Tuliskan . Bilangan positif dan . Untuk setiap , berlaku dan . Karena keduanya positif, . Jadi adalah batas bawah bagi . Akan tetapi, , bertentangan dengan fakta bahwa adalah batas bawah terbesar. Maka kasus mustahil.   Tugas 25: menyingkirkan kasus  Andaikan . Pilih sehingga , lalu jelaskan kontradiksinya. Rubrik: pastikan serta buktikan bahwa bilangan tersebut menjadi anggota yang lebih kecil daripada batas bawah .    Langkah 1. Tetapkan dan pilih sedemikian besar sehingga sekaligus dan .   Langkah 2. Gunakan .   Pilih . Maka dan . Jadi , bertentangan dengan sebagai batas bawah .   Andaikan dan tetapkan . Sifat Archimedes memungkinkan kita memilih dengan . Maka , sehingga . Selain itu,   Karena dan , definisi memberi . Namun , sedangkan sebagai batas bawah harus memenuhi untuk setiap . Kontradiksi ini menunjukkan bahwa kasus juga mustahil.   Tugas 26: keberadaan  Simpulkan dari dua kasus yang telah disingkirkan bahwa bilangan real positif ada. Rubrik: gunakan trikotomi pada dan, untuk ketepatan notasi, jelaskan ketunggalan akar positif tersebut.    Langkah 1. Tepat satu dari , , atau berlaku.   Langkah 2. Jika dan , faktorkan .   Karena kedua pertidaksamaan ketat mustahil, . Dari , positif; ia adalah akar kuadrat positif yang tunggal dan karenanya .   Trikotomi urutan bilangan real menyatakan bahwa tepat satu dari , , dan berlaku. Tugas 24 menyingkirkan kemungkinan pertama dan Tugas 25 menyingkirkan kemungkinan ketiga. Oleh sebab itu . Tugas 23 memberi , sehingga .  Untuk memeriksa ketunggalan, andaikan dan . Maka . Karena , harus berlaku , jadi . Dengan demikian ada tepat satu bilangan real positif yang kuadratnya ; bilangan itu dinotasikan dengan , dan konstruksi di atas membuktikan bahwa benar-benar ada.   Tugas 27: paritas pembilang  Andaikan demi kontradiksi bahwa , dengan relatif prima. Buktikan dan simpulkan bahwa membagi . Rubrik: kuadratkan persamaan dan gunakan bahwa jika bilangan prima membagi suatu kuadrat, bilangan itu membagi dasarnya.    Langkah 1. Gunakan dan kalikan dengan .   Langkah 2. Persamaan yang diperoleh menunjukkan ; terapkan sifat bilangan prima .   Menguadratkan memberi , sehingga . Jadi ; karena prima, .   Dari , dengan , kita memperoleh Mengalikan kedua ruas dengan menghasilkan . Maka genap, atau . Berdasarkan lema Euklides, jika bilangan prima membagi suatu hasil kali, ia membagi sekurang-kurangnya satu faktornya. Karena kedua faktor di sini sama-sama , diperoleh . Jadi ada dengan .   Tugas 28: kontradiksi faktor persekutuan  Dengan hasil , buktikan bahwa dan selesaikan pembuktian bahwa irasional. Rubrik: tuliskan , substitusikan ke , dan bandingkan dengan asumsi bahwa pecahan telah disederhanakan.    Langkah 1. Substitusi memberi .   Langkah 2. Setelah membagi dengan , gunakan kembali sifat prima yang dipakai pada tugas sebelumnya.   Dari diperoleh , sehingga . Maka membagi baik maupun , bertentangan dengan keduanya relatif prima. Jadi .   Karena , tuliskan untuk suatu . Substitusi ke persamaan memberi Jadi . Karena prima, lema Euklides memberi .  Dengan demikian adalah faktor persekutuan positif dari dan . Ini bertentangan dengan pilihan dalam bentuk paling sederhana, yakni bahwa dan tidak mempunyai faktor persekutuan positif selain . Pengandaian bahwa rasional harus salah; maka irasional.   Tugas 29: bilangan irasional di antara dua bilangan real  Untuk dua bilangan real berbeda dan , temukan dan sehingga irasional dan terletak ketat di antara dan . Rubrik: buat langkah cukup kecil, pilih kelipatan bulat yang tepat, pastikan , lalu buktikan irasionalitasnya.    Langkah 1. Setelah menamai ujung interval sebagai , pilih sehingga . Jika interval tidak melintasi , ambil bilangan bulat terkecil .   Langkah 2. Jika , buat juga dan ambil . Jika dan rasional, selesaikan persamaan itu terhadap .   Tulis dan . Pilih sehingga . Jika interval tidak melintasi , bilangan bulat terkecil memenuhi dan . Jika , pilih juga dan ambil . Dalam kedua kasus irasional.   Tukarkan nama kedua bilangan jika perlu dan tetapkan serta , sehingga . Bilangan dapat dibuat sekecil yang diinginkan: menurut induksi , dan sifat Archimedes memungkinkan melampaui sebarang batas real yang ditentukan. Jadi pilih sehingga .  Mula-mula andaikan interval tidak melintasi nol, yaitu atau . Ambil bilangan bulat terkecil yang memenuhi . Keminimalannya memberi , sehingga Jika , maka , sehingga . Jika , rantai di atas memberi , sehingga . Jadi dalam kedua subkasus .  Jika , pilih lebih besar lagi bila perlu agar juga , dan ambil . Maka , sehingga kembali diperoleh kelipatan di dalam interval dengan .  Akhirnya, dalam kedua kasus . Seandainya rasional, karena kita akan memperoleh , bertentangan dengan Tugas 28. Jadi irasional dan terletak ketat di antara dan .   Tugas 30: pertidaksamaan jarak titik ke himpunan  Dalam ruang metrik , untuk himpunan tak kosong dan , buktikan . Rubrik: gunakan sifat infimum untuk memilih titik yang hampir meminimumkan jarak dari , terapkan pertidaksamaan segitiga, lalu hilangkan galat positifnya.    Langkah 1. Untuk setiap , ada dengan .   Langkah 2. Bandingkan dengan , lalu gunakan pertidaksamaan segitiga.   Untuk setiap , pilih dengan . Maka . Karena ini berlaku untuk setiap , diperoleh pertidaksamaan yang diminta.   Ambil sebarang . Karena , terdapat dengan . Jika tidak ada titik seperti itu, akan menjadi batas bawah yang lebih besar daripada infimum, suatu kontradiksi.  Berdasarkan definisi infimum dan pertidaksamaan segitiga, Misalkan, sebaliknya, . Memilih lebih kecil daripada selisih positif kedua ruas akan bertentangan dengan pertidaksamaan terakhir. Jadi .   Tugas 31: jarak ke gabungan  Untuk subhimpunan tak kosong dari ruang metrik dan , buktikan . Rubrik: buktikan kedua arah pertidaksamaan dengan membandingkan himpunan kandidat jarak.    Langkah 1. Karena dan , mengambil infimum atas gabungan tidak dapat menghasilkan nilai yang lebih besar daripada salah satu infimum.   Langkah 2. Jika , tunjukkan bahwa adalah batas bawah bagi semua dengan .   Jarak ke gabungan tidak melebihi jarak ke masing-masing himpunan, sehingga tidak melebihi minimum keduanya. Sebaliknya, minimum itu adalah batas bawah bagi setiap jarak ke titik dalam . Kedua pertidaksamaan memberi kesamaan.   Tetapkan , , dan . Karena , himpunan jarak yang dipakai untuk mendefinisikan memuat semua jarak ke . Maka . Dengan alasan yang sama, . Jadi .  Sebaliknya, ambil . Jika , definisi infimum memberi . Jika , diperoleh . Jadi adalah batas bawah bagi semua jarak . Karena infimum adalah batas bawah terbesar, . Menggabungkan kedua arah memberi .   Tugas 32: keterbatasan diwarisi subhimpunan  Putuskan benar atau salah: setiap subhimpunan tak kosong dari himpunan terbatas juga terbatas. Rubrik: jika benar, gunakan batas bawah dan batas atas yang sama untuk semua anggota subhimpunan.    Langkah 1. Karena terbatas, ada dengan untuk setiap .   Langkah 2. Apa yang berubah jika kuantifikasi dibatasi pada anggota suatu ?   Benar. Setiap batas bawah dan batas atas bagi juga menjadi batas bawah dan batas atas bagi setiap .   Karena terbatas, terdapat sedemikian sehingga untuk setiap . Jika dan , maka juga , sehingga . Jadi adalah batas bawah dan adalah batas atas bagi . Dengan demikian setiap subhimpunan tak kosong dari terbatas. Syarat tak kosong diperlukan agar pembahasan infimum dan supremum biasa dapat dilanjutkan, tetapi pewarisan kedua batas itu sendiri tetap berlaku bagi himpunan kosong.   Tugas 33: supremum jumlah himpunan  Putuskan benar atau salah: . Rubrik: uji dengan himpunan tunggal yang konkret dan bandingkan kedua ruas.    Langkah 1. Ambil .   Langkah 2. Hitung sebelum mengambil supremumnya.   Salah. Untuk , diperoleh , sedangkan .   Pilih himpunan tak kosong dan terbatas . Maka , sehingga . Di sisi lain, , jadi . Karena , pernyataan tersebut salah. Rumus yang benar di bawah hipotesis latihan ialah , bukan maksimum kedua supremum.   Tugas 34: infimum jumlah himpunan  Putuskan benar atau salah: . Rubrik: berikan contoh konkret yang memenuhi semua hipotesis dan hitung kedua ruas.    Langkah 1. Himpunan tunggal juga cukup di sini.   Langkah 2. Bandingkan infimum dengan minimum dari dua salinan bilangan .   Salah. Untuk , diperoleh , sedangkan .   Ambil , yang keduanya tak kosong dan terbatas. Karena , diperoleh . Namun , sehingga . Kedua nilai itu berbeda, jadi pernyataan salah. Rumus yang benar adalah di bawah hipotesis yang diberikan.   Tugas 35: supremum subhimpunan  Putuskan benar atau salah: jika subhimpunan tak kosong dari , maka . Rubrik: tunjukkan bahwa adalah batas atas bagi , lalu gunakan sifat terkecil dari supremum.    Langkah 1. Untuk setiap , berlaku .   Langkah 2. Supremum tidak melebihi batas atas mana pun bagi .   Benar. Bilangan adalah batas atas bagi , sehingga batas atas terkecil memenuhi .   Ambil sebarang . Karena , berlaku . Berdasarkan definisi supremum, . Jadi adalah batas atas bagi . Himpunan tak kosong dan terbatas karena merupakan subhimpunan dari , sehingga ada. Sebagai batas atas terkecil, tidak melebihi setiap batas atas bagi , khususnya tidak melebihi . Maka , dan pernyataannya benar.   Tugas 36: infimum subhimpunan  Putuskan benar atau salah: jika subhimpunan tak kosong dari , maka . Rubrik: tunjukkan bahwa adalah batas bawah bagi , lalu gunakan sifat terbesar dari infimum.    Langkah 1. Untuk setiap , berlaku .   Langkah 2. Infimum tidak lebih kecil daripada batas bawah mana pun bagi .   Benar. Bilangan adalah batas bawah bagi , sehingga batas bawah terbesar memenuhi .   Untuk setiap , inklusi memberi . Karena adalah batas bawah bagi , berlaku . Jadi juga merupakan batas bawah bagi . Himpunan tak kosong dan terbatas, sehingga ada. Karena adalah batas bawah terbesar bagi , ia sekurang-kurangnya sebesar setiap batas bawah bagi , khususnya . Dengan demikian , dan pernyataannya benar.   Tugas 37: jarak nol dan penutupan  Putuskan benar atau salah: jika tak kosong dan , maka . Rubrik: jika salah, berikan contoh konkret dalam metrik Euklides dan nyatakan hubungan yang tepat antara jarak nol, penutupan , dan keanggotaan dalam .    Langkah 1. Ambil dan . Titik-titik berada dalam untuk dan mendekati .   Langkah 2. Dalam ruang metrik, mencirikan , bukan selalu .   Salah. Untuk dan , berlaku , tetapi . Yang benar ialah jika dan hanya jika ; keanggotaan dalam penutupan tidak sama dengan keanggotaan dalam kecuali, misalnya, tertutup.   Gunakan metrik Euklides pada . Ambil dan . Semua jarak dengan positif, tetapi untuk setiap terdapat dengan . Oleh karena itu . Meskipun demikian, . Ini membantah pernyataan.  Secara umum dalam ruang metrik, berarti bahwa untuk setiap terdapat dengan ; pernyataan ini setara dengan setiap bola terbuka di sekitar bertemu , yakni . Sebaliknya, sifat penutupan tersebut membuat infimum semua jarak ke sama dengan nol. Jadi kesetaraan yang tepat adalah . Dari sini hanya dapat disimpulkan apabila diketahui tambahan bahwa , misalnya bila tertutup.   "
},
{
  "id": "o003-c90-ch05-exercise-task-19",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-19",
  "type": "Pemeriksaan",
  "number": "E.30",
  "title": "Tugas 19: batas bawah bagi himpunan bilangan bulat.",
  "body": "Tugas 19: batas bawah bagi himpunan bilangan bulat  Untuk , buktikan bahwa terbatas di bawah. Rubrik: berikan satu batas bawah real yang berlaku untuk setiap dan hubungkan langsung dengan syarat pembentuk .    Langkah 1. Tidak perlu mencari suatu bilangan bulat sebagai batas bawah; batas bawah boleh berupa sebarang bilangan real.   Langkah 2. Setiap memenuhi .   Bilangan adalah batas bawah bagi , sebab untuk setiap .   Berdasarkan definisi , jika , maka . Dengan demikian untuk setiap anggota . Ini tepat merupakan definisi bahwa adalah batas bawah bagi . Karena , himpunan terbatas di bawah dalam .  "
},
{
  "id": "o003-c90-ch05-exercise-task-20",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-20",
  "type": "Pemeriksaan",
  "number": "E.31",
  "title": "Tugas 20: anggota bulat terkecil.",
  "body": "Tugas 20: anggota bulat terkecil  Tunjukkan bahwa memuat suatu bilangan bulat sedemikian sehingga setiap dengan memenuhi . Rubrik: terapkan Prinsip Pengurutan Baik kepada , lalu gunakan keminimalan anggota yang diperoleh.    Langkah 1. Himpunan tak kosong dan, menurut tugas sebelumnya, terbatas di bawah; semua anggotanya bilangan bulat.   Langkah 2. Jika tetapi , di manakah letak terhadap anggota terkecil dari ?   Prinsip Pengurutan Baik memberi anggota terkecil . Jika dan , maka tidak mungkin memenuhi ; jadi .   Sifat Archimedes menjamin bahwa tak kosong, sedangkan Tugas 19 menunjukkan bahwa terbatas di bawah. Karena , Prinsip Pengurutan Baik yang dinyatakan pada latihan sumber memastikan bahwa memuat infimumnya. Tuliskan anggota terkecil ini sebagai ; khususnya .  Ambil dengan . Andaikan . Syarat ini dan fakta bahwa bilangan bulat akan memberi , bertentangan dengan keminimalan karena . Jadi pengandaian tersebut salah dan harus berlaku .  "
},
{
  "id": "o003-c90-ch05-exercise-task-21",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-21",
  "type": "Pemeriksaan",
  "number": "E.32",
  "title": "Tugas 21: bilangan rasional di antara dua bilangan real.",
  "body": "Tugas 21: bilangan rasional di antara dua bilangan real  Gunakan anggota terkecil untuk membuktikan , lalu temukan bilangan rasional di antara dan . Rubrik: terapkan hasil tugas sebelumnya kepada dan gunakan .    Langkah 1. Karena , langsung diperoleh satu dari dua pertidaksamaan. Untuk yang lain, masukkan ke hasil Tugas 20.   Langkah 2. Ubah menjadi , kemudian bagi rantai pertidaksamaan dengan .   Berlaku . Karena itu , dan adalah bilangan rasional yang dicari.   Karena , definisi memberi . Bilangan adalah bilangan bulat dan memenuhi . Maka Tugas 20, dengan , memberi , atau setara dengan .  Dari diperoleh , sehingga . Menggabungkan semuanya menghasilkan Karena bilangan bulat positif, pembagian dengan mempertahankan arah pertidaksamaan dan memberi . Dengan dan , bilangan rasional. Jadi setiap interval terbuka tak kosong di memuat suatu bilangan rasional.  "
},
{
  "id": "o003-c90-ch05-exercise-task-22",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-22",
  "type": "Pemeriksaan",
  "number": "E.33",
  "title": "Tugas 22: titik rasional dalam bola Euklides.",
  "body": "Tugas 22: titik rasional dalam bola Euklides  Buktikan bahwa setiap bola terbuka dalam memuat titik yang kedua koordinatnya rasional. Rubrik: mulai dari pusat dan jari-jari bola, pilih satu bilangan rasional dekat dengan tiap koordinat pusat, lalu perkirakan jarak Euklidesnya.    Langkah 1. Untuk bola berpusat berjari-jari , gunakan kerapatan untuk memilih .   Langkah 2. Gunakan .   Pilih dengan . Untuk , berlaku ; jadi berada dalam bola dan kedua koordinatnya rasional.   Misalkan suatu bola terbuka dengan dan . Berdasarkan kerapatan bilangan rasional dalam bilangan real, terdapat sedemikian sehingga dan . Tetapkan .  Untuk bilangan real , kedua ruas tak negatif dan , sehingga . Karena itu Maka , dan kedua koordinat rasional sebagaimana diminta.  "
},
{
  "id": "o003-c90-ch05-exercise-task-23",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-23",
  "type": "Pemeriksaan",
  "number": "E.34",
  "title": "Tugas 23: membentuk calon akar kuadrat.",
  "body": "Tugas 23: membentuk calon akar kuadrat  Untuk , buktikan bahwa mempunyai batas bawah terbesar . Rubrik: tunjukkan bahwa tak kosong dan berikan satu batas bawahnya sebelum memakai kelengkapan .    Langkah 1. Periksa bahwa .   Langkah 2. Jika , maka ; jadi setiap anggota lebih besar daripada .   Himpunan tak kosong karena , dan adalah batas bawahnya. Kelengkapan memberi ; selain itu .   Bilangan positif dan , sehingga dan tak kosong. Jika , maka dan . Seandainya , akan berlaku , suatu kontradiksi. Jadi untuk setiap , dan adalah batas bawah .  Aksioma kelengkapan bilangan real menjamin bahwa himpunan real tak kosong yang terbatas di bawah mempunyai infimum. Maka ada. Karena adalah batas bawah, ; karena dan infimum tidak melebihi setiap anggota himpunan, .  "
},
{
  "id": "o003-c90-ch05-exercise-task-24",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-24",
  "type": "Pemeriksaan",
  "number": "E.35",
  "title": "Tugas 24: menyingkirkan kasus <span class=\"process-math\">\\(m^2<2\\)<\/span>.",
  "body": "Tugas 24: menyingkirkan kasus  Andaikan . Pilih sehingga , lalu jelaskan kontradiksinya. Rubrik: buat pilihan kuantitatif untuk dan buktikan bahwa menjadi batas bawah yang lebih besar daripada .    Langkah 1. Tetapkan dan gunakan sifat Archimedes untuk memilih .   Langkah 2. Untuk , berlaku . Jika kuadrat suatu bilangan positif kurang daripada , bandingkan dengan semua anggota .   Dengan , pilih . Maka . Bilangan lalu merupakan batas bawah yang lebih besar daripada , suatu kontradiksi.   Andaikan dan tetapkan . Sifat Archimedes memberi bilangan bulat positif dengan . Karena , diperoleh   Tuliskan . Bilangan positif dan . Untuk setiap , berlaku dan . Karena keduanya positif, . Jadi adalah batas bawah bagi . Akan tetapi, , bertentangan dengan fakta bahwa adalah batas bawah terbesar. Maka kasus mustahil.  "
},
{
  "id": "o003-c90-ch05-exercise-task-25",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-25",
  "type": "Pemeriksaan",
  "number": "E.36",
  "title": "Tugas 25: menyingkirkan kasus <span class=\"process-math\">\\(m^2>2\\)<\/span>.",
  "body": "Tugas 25: menyingkirkan kasus  Andaikan . Pilih sehingga , lalu jelaskan kontradiksinya. Rubrik: pastikan serta buktikan bahwa bilangan tersebut menjadi anggota yang lebih kecil daripada batas bawah .    Langkah 1. Tetapkan dan pilih sedemikian besar sehingga sekaligus dan .   Langkah 2. Gunakan .   Pilih . Maka dan . Jadi , bertentangan dengan sebagai batas bawah .   Andaikan dan tetapkan . Sifat Archimedes memungkinkan kita memilih dengan . Maka , sehingga . Selain itu,   Karena dan , definisi memberi . Namun , sedangkan sebagai batas bawah harus memenuhi untuk setiap . Kontradiksi ini menunjukkan bahwa kasus juga mustahil.  "
},
{
  "id": "o003-c90-ch05-exercise-task-26",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-26",
  "type": "Pemeriksaan",
  "number": "E.37",
  "title": "Tugas 26: keberadaan <span class=\"process-math\">\\(\\sqrt{2}\\)<\/span>.",
  "body": "Tugas 26: keberadaan  Simpulkan dari dua kasus yang telah disingkirkan bahwa bilangan real positif ada. Rubrik: gunakan trikotomi pada dan, untuk ketepatan notasi, jelaskan ketunggalan akar positif tersebut.    Langkah 1. Tepat satu dari , , atau berlaku.   Langkah 2. Jika dan , faktorkan .   Karena kedua pertidaksamaan ketat mustahil, . Dari , positif; ia adalah akar kuadrat positif yang tunggal dan karenanya .   Trikotomi urutan bilangan real menyatakan bahwa tepat satu dari , , dan berlaku. Tugas 24 menyingkirkan kemungkinan pertama dan Tugas 25 menyingkirkan kemungkinan ketiga. Oleh sebab itu . Tugas 23 memberi , sehingga .  Untuk memeriksa ketunggalan, andaikan dan . Maka . Karena , harus berlaku , jadi . Dengan demikian ada tepat satu bilangan real positif yang kuadratnya ; bilangan itu dinotasikan dengan , dan konstruksi di atas membuktikan bahwa benar-benar ada.  "
},
{
  "id": "o003-c90-ch05-exercise-task-27",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-27",
  "type": "Pemeriksaan",
  "number": "E.38",
  "title": "Tugas 27: paritas pembilang.",
  "body": "Tugas 27: paritas pembilang  Andaikan demi kontradiksi bahwa , dengan relatif prima. Buktikan dan simpulkan bahwa membagi . Rubrik: kuadratkan persamaan dan gunakan bahwa jika bilangan prima membagi suatu kuadrat, bilangan itu membagi dasarnya.    Langkah 1. Gunakan dan kalikan dengan .   Langkah 2. Persamaan yang diperoleh menunjukkan ; terapkan sifat bilangan prima .   Menguadratkan memberi , sehingga . Jadi ; karena prima, .   Dari , dengan , kita memperoleh Mengalikan kedua ruas dengan menghasilkan . Maka genap, atau . Berdasarkan lema Euklides, jika bilangan prima membagi suatu hasil kali, ia membagi sekurang-kurangnya satu faktornya. Karena kedua faktor di sini sama-sama , diperoleh . Jadi ada dengan .  "
},
{
  "id": "o003-c90-ch05-exercise-task-28",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-28",
  "type": "Pemeriksaan",
  "number": "E.39",
  "title": "Tugas 28: kontradiksi faktor persekutuan.",
  "body": "Tugas 28: kontradiksi faktor persekutuan  Dengan hasil , buktikan bahwa dan selesaikan pembuktian bahwa irasional. Rubrik: tuliskan , substitusikan ke , dan bandingkan dengan asumsi bahwa pecahan telah disederhanakan.    Langkah 1. Substitusi memberi .   Langkah 2. Setelah membagi dengan , gunakan kembali sifat prima yang dipakai pada tugas sebelumnya.   Dari diperoleh , sehingga . Maka membagi baik maupun , bertentangan dengan keduanya relatif prima. Jadi .   Karena , tuliskan untuk suatu . Substitusi ke persamaan memberi Jadi . Karena prima, lema Euklides memberi .  Dengan demikian adalah faktor persekutuan positif dari dan . Ini bertentangan dengan pilihan dalam bentuk paling sederhana, yakni bahwa dan tidak mempunyai faktor persekutuan positif selain . Pengandaian bahwa rasional harus salah; maka irasional.  "
},
{
  "id": "o003-c90-ch05-exercise-task-29",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-29",
  "type": "Pemeriksaan",
  "number": "E.40",
  "title": "Tugas 29: bilangan irasional di antara dua bilangan real.",
  "body": "Tugas 29: bilangan irasional di antara dua bilangan real  Untuk dua bilangan real berbeda dan , temukan dan sehingga irasional dan terletak ketat di antara dan . Rubrik: buat langkah cukup kecil, pilih kelipatan bulat yang tepat, pastikan , lalu buktikan irasionalitasnya.    Langkah 1. Setelah menamai ujung interval sebagai , pilih sehingga . Jika interval tidak melintasi , ambil bilangan bulat terkecil .   Langkah 2. Jika , buat juga dan ambil . Jika dan rasional, selesaikan persamaan itu terhadap .   Tulis dan . Pilih sehingga . Jika interval tidak melintasi , bilangan bulat terkecil memenuhi dan . Jika , pilih juga dan ambil . Dalam kedua kasus irasional.   Tukarkan nama kedua bilangan jika perlu dan tetapkan serta , sehingga . Bilangan dapat dibuat sekecil yang diinginkan: menurut induksi , dan sifat Archimedes memungkinkan melampaui sebarang batas real yang ditentukan. Jadi pilih sehingga .  Mula-mula andaikan interval tidak melintasi nol, yaitu atau . Ambil bilangan bulat terkecil yang memenuhi . Keminimalannya memberi , sehingga Jika , maka , sehingga . Jika , rantai di atas memberi , sehingga . Jadi dalam kedua subkasus .  Jika , pilih lebih besar lagi bila perlu agar juga , dan ambil . Maka , sehingga kembali diperoleh kelipatan di dalam interval dengan .  Akhirnya, dalam kedua kasus . Seandainya rasional, karena kita akan memperoleh , bertentangan dengan Tugas 28. Jadi irasional dan terletak ketat di antara dan .  "
},
{
  "id": "o003-c90-ch05-exercise-task-30",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-30",
  "type": "Pemeriksaan",
  "number": "E.41",
  "title": "Tugas 30: pertidaksamaan jarak titik ke himpunan.",
  "body": "Tugas 30: pertidaksamaan jarak titik ke himpunan  Dalam ruang metrik , untuk himpunan tak kosong dan , buktikan . Rubrik: gunakan sifat infimum untuk memilih titik yang hampir meminimumkan jarak dari , terapkan pertidaksamaan segitiga, lalu hilangkan galat positifnya.    Langkah 1. Untuk setiap , ada dengan .   Langkah 2. Bandingkan dengan , lalu gunakan pertidaksamaan segitiga.   Untuk setiap , pilih dengan . Maka . Karena ini berlaku untuk setiap , diperoleh pertidaksamaan yang diminta.   Ambil sebarang . Karena , terdapat dengan . Jika tidak ada titik seperti itu, akan menjadi batas bawah yang lebih besar daripada infimum, suatu kontradiksi.  Berdasarkan definisi infimum dan pertidaksamaan segitiga, Misalkan, sebaliknya, . Memilih lebih kecil daripada selisih positif kedua ruas akan bertentangan dengan pertidaksamaan terakhir. Jadi .  "
},
{
  "id": "o003-c90-ch05-exercise-task-31",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-31",
  "type": "Pemeriksaan",
  "number": "E.42",
  "title": "Tugas 31: jarak ke gabungan.",
  "body": "Tugas 31: jarak ke gabungan  Untuk subhimpunan tak kosong dari ruang metrik dan , buktikan . Rubrik: buktikan kedua arah pertidaksamaan dengan membandingkan himpunan kandidat jarak.    Langkah 1. Karena dan , mengambil infimum atas gabungan tidak dapat menghasilkan nilai yang lebih besar daripada salah satu infimum.   Langkah 2. Jika , tunjukkan bahwa adalah batas bawah bagi semua dengan .   Jarak ke gabungan tidak melebihi jarak ke masing-masing himpunan, sehingga tidak melebihi minimum keduanya. Sebaliknya, minimum itu adalah batas bawah bagi setiap jarak ke titik dalam . Kedua pertidaksamaan memberi kesamaan.   Tetapkan , , dan . Karena , himpunan jarak yang dipakai untuk mendefinisikan memuat semua jarak ke . Maka . Dengan alasan yang sama, . Jadi .  Sebaliknya, ambil . Jika , definisi infimum memberi . Jika , diperoleh . Jadi adalah batas bawah bagi semua jarak . Karena infimum adalah batas bawah terbesar, . Menggabungkan kedua arah memberi .  "
},
{
  "id": "o003-c90-ch05-exercise-task-32",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-32",
  "type": "Pemeriksaan",
  "number": "E.43",
  "title": "Tugas 32: keterbatasan diwarisi subhimpunan.",
  "body": "Tugas 32: keterbatasan diwarisi subhimpunan  Putuskan benar atau salah: setiap subhimpunan tak kosong dari himpunan terbatas juga terbatas. Rubrik: jika benar, gunakan batas bawah dan batas atas yang sama untuk semua anggota subhimpunan.    Langkah 1. Karena terbatas, ada dengan untuk setiap .   Langkah 2. Apa yang berubah jika kuantifikasi dibatasi pada anggota suatu ?   Benar. Setiap batas bawah dan batas atas bagi juga menjadi batas bawah dan batas atas bagi setiap .   Karena terbatas, terdapat sedemikian sehingga untuk setiap . Jika dan , maka juga , sehingga . Jadi adalah batas bawah dan adalah batas atas bagi . Dengan demikian setiap subhimpunan tak kosong dari terbatas. Syarat tak kosong diperlukan agar pembahasan infimum dan supremum biasa dapat dilanjutkan, tetapi pewarisan kedua batas itu sendiri tetap berlaku bagi himpunan kosong.  "
},
{
  "id": "o003-c90-ch05-exercise-task-33",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-33",
  "type": "Pemeriksaan",
  "number": "E.44",
  "title": "Tugas 33: supremum jumlah himpunan.",
  "body": "Tugas 33: supremum jumlah himpunan  Putuskan benar atau salah: . Rubrik: uji dengan himpunan tunggal yang konkret dan bandingkan kedua ruas.    Langkah 1. Ambil .   Langkah 2. Hitung sebelum mengambil supremumnya.   Salah. Untuk , diperoleh , sedangkan .   Pilih himpunan tak kosong dan terbatas . Maka , sehingga . Di sisi lain, , jadi . Karena , pernyataan tersebut salah. Rumus yang benar di bawah hipotesis latihan ialah , bukan maksimum kedua supremum.  "
},
{
  "id": "o003-c90-ch05-exercise-task-34",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-34",
  "type": "Pemeriksaan",
  "number": "E.45",
  "title": "Tugas 34: infimum jumlah himpunan.",
  "body": "Tugas 34: infimum jumlah himpunan  Putuskan benar atau salah: . Rubrik: berikan contoh konkret yang memenuhi semua hipotesis dan hitung kedua ruas.    Langkah 1. Himpunan tunggal juga cukup di sini.   Langkah 2. Bandingkan infimum dengan minimum dari dua salinan bilangan .   Salah. Untuk , diperoleh , sedangkan .   Ambil , yang keduanya tak kosong dan terbatas. Karena , diperoleh . Namun , sehingga . Kedua nilai itu berbeda, jadi pernyataan salah. Rumus yang benar adalah di bawah hipotesis yang diberikan.  "
},
{
  "id": "o003-c90-ch05-exercise-task-35",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-35",
  "type": "Pemeriksaan",
  "number": "E.46",
  "title": "Tugas 35: supremum subhimpunan.",
  "body": "Tugas 35: supremum subhimpunan  Putuskan benar atau salah: jika subhimpunan tak kosong dari , maka . Rubrik: tunjukkan bahwa adalah batas atas bagi , lalu gunakan sifat terkecil dari supremum.    Langkah 1. Untuk setiap , berlaku .   Langkah 2. Supremum tidak melebihi batas atas mana pun bagi .   Benar. Bilangan adalah batas atas bagi , sehingga batas atas terkecil memenuhi .   Ambil sebarang . Karena , berlaku . Berdasarkan definisi supremum, . Jadi adalah batas atas bagi . Himpunan tak kosong dan terbatas karena merupakan subhimpunan dari , sehingga ada. Sebagai batas atas terkecil, tidak melebihi setiap batas atas bagi , khususnya tidak melebihi . Maka , dan pernyataannya benar.  "
},
{
  "id": "o003-c90-ch05-exercise-task-36",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-36",
  "type": "Pemeriksaan",
  "number": "E.47",
  "title": "Tugas 36: infimum subhimpunan.",
  "body": "Tugas 36: infimum subhimpunan  Putuskan benar atau salah: jika subhimpunan tak kosong dari , maka . Rubrik: tunjukkan bahwa adalah batas bawah bagi , lalu gunakan sifat terbesar dari infimum.    Langkah 1. Untuk setiap , berlaku .   Langkah 2. Infimum tidak lebih kecil daripada batas bawah mana pun bagi .   Benar. Bilangan adalah batas bawah bagi , sehingga batas bawah terbesar memenuhi .   Untuk setiap , inklusi memberi . Karena adalah batas bawah bagi , berlaku . Jadi juga merupakan batas bawah bagi . Himpunan tak kosong dan terbatas, sehingga ada. Karena adalah batas bawah terbesar bagi , ia sekurang-kurangnya sebesar setiap batas bawah bagi , khususnya . Dengan demikian , dan pernyataannya benar.  "
},
{
  "id": "o003-c90-ch05-exercise-task-37",
  "level": "2",
  "url": "o003-c90-ch05-exercise-guides-b.html#o003-c90-ch05-exercise-task-37",
  "type": "Pemeriksaan",
  "number": "E.48",
  "title": "Tugas 37: jarak nol dan penutupan.",
  "body": "Tugas 37: jarak nol dan penutupan  Putuskan benar atau salah: jika tak kosong dan , maka . Rubrik: jika salah, berikan contoh konkret dalam metrik Euklides dan nyatakan hubungan yang tepat antara jarak nol, penutupan , dan keanggotaan dalam .    Langkah 1. Ambil dan . Titik-titik berada dalam untuk dan mendekati .   Langkah 2. Dalam ruang metrik, mencirikan , bukan selalu .   Salah. Untuk dan , berlaku , tetapi . Yang benar ialah jika dan hanya jika ; keanggotaan dalam penutupan tidak sama dengan keanggotaan dalam kecuali, misalnya, tertutup.   Gunakan metrik Euklides pada . Ambil dan . Semua jarak dengan positif, tetapi untuk setiap terdapat dengan . Oleh karena itu . Meskipun demikian, . Ini membantah pernyataan.  Secara umum dalam ruang metrik, berarti bahwa untuk setiap terdapat dengan ; pernyataan ini setara dengan setiap bola terbuka di sekitar bertemu , yakni . Sebaliknya, sifat penutupan tersebut membuat infimum semua jarak ke sama dengan nol. Jadi kesetaraan yang tepat adalah . Dari sini hanya dapat disimpulkan apabila diketahui tambahan bahwa , misalnya bila tertutup.  "
},
{
  "id": "o003-c90-ch05-mastery",
  "level": "1",
  "url": "o003-c90-ch05-mastery.html",
  "type": "Bagian",
  "number": "",
  "title": "Pemeriksaan penguasaan dan transfer",
  "body": " Pemeriksaan penguasaan dan transfer  Enam latihan asli berikut menguji apakah gagasan Bab 5 dapat dipakai pada situasi baru. Kerjakan pernyataannya terlebih dahulu, nilai pekerjaan Anda dengan rubrik yang diberikan, lalu buka petunjuk secara bertahap sebelum membandingkan jawaban dan pembahasan lengkap.  Infimum, supremum, minimum, dan maksimum  Untuk parameter , definisikan dengan . Tentukan dan , lalu putuskan apakah mempunyai minimum atau maksimum.   Rubrik. Buktikan bahwa setiap nilai yang Anda usulkan memang merupakan batas yang sesuai dan bahwa tidak ada batas bawah yang lebih besar atau batas atas yang lebih kecil. Bedakan dengan tegas antara infimum atau supremum dan anggota himpunan yang menjadi minimum atau maksimum.    Langkah 1. Titik-titik pada interval terbuka dapat mendekati dari kanan sedekat apa pun.   Langkah 2. Barisan meningkat menuju , tetapi tidak pernah mencapainya.   Langkah 3. Untuk menguji minimum atau maksimum, periksa apakah infimum atau supremum tersebut merupakan anggota .    dan . Karena kedua nilai itu tidak berada dalam , himpunan tersebut tidak mempunyai minimum dan tidak mempunyai maksimum.   Setiap anggota interval lebih besar daripada . Selain itu, untuk berlaku . Jadi adalah batas bawah . Jika , pilih . Kita mempunyai , sehingga , dan sekaligus . Maka bukan batas bawah. Jadi .  Setiap anggota lebih kecil daripada , dan untuk setiap . Dengan demikian adalah batas atas. Jika , sifat Archimedes memberi dengan . Akibatnya , sehingga bukan batas atas. Oleh karena itu .  Interval tidak memuat , sedangkan setiap unsur barisan sedikitnya ; jadi . Demikian pula, tidak satu pun dari kedua bagian pembentuk memuat . Karena minimum harus sama dengan infimum dan maksimum harus sama dengan supremum, tidak mempunyai minimum maupun maksimum.   Jarak nol dan penutupan  Misalkan ruang metrik, tak kosong, dan . Buktikan bahwa    Rubrik. Buktikan kedua implikasi dengan definisi penutupan melalui bola terbuka; nyatakan secara eksplisit bagaimana sifat infimum menghasilkan titik pada jarak kurang dari .    Langkah 1. Jika , maka untuk setiap .   Langkah 2. Jika infimum himpunan jarak adalah nol tetapi tidak ada jarak yang lebih kecil daripada suatu , maka akan menjadi batas bawah positif.   Kesetaraan itu benar: tepat ketika setiap bola terbuka berpusat di bertemu , dan kondisi terakhir adalah definisi .   Andaikan . Untuk setiap , ada dengan . Karena infimum tidak melebihi setiap anggota himpunan yang diinfimumkan, . Tidak ada bilangan real positif yang lebih kecil daripada setiap ; maka .  Sebaliknya, andaikan . Ambil sembarang . Jika semua memenuhi , maka merupakan batas bawah himpunan , bertentangan dengan fakta bahwa batas bawah terbesarnya adalah nol. Jadi terdapat dengan . Artinya untuk setiap radius positif, sehingga .   Fungsi jarak bersifat 1-Lipschitz  Dalam keadaan latihan sebelumnya, definisikan dengan . Buktikan bahwa untuk semua ,    Rubrik. Gunakan pertidaksamaan segitiga sebelum mengambil infimum, peroleh dua pertidaksamaan satu arah dengan menukar dan , lalu gabungkan keduanya. Jangan mengandaikan bahwa infimum dicapai oleh suatu anggota .    Langkah 1. Untuk setiap , berlaku .   Langkah 2. Ambil infimum terhadap , lalu ulangi dengan menukar dan .   Fungsi bersifat 1-Lipschitz: untuk setiap .   Tetapkan . Untuk setiap , pertidaksamaan segitiga memberi . Karena adalah infimum nilai-nilai di ruas kiri, kita mempunyai untuk setiap . Mengambil infimum ruas kanan terhadap menghasilkan sehingga .  Dengan menukar dan serta memakai simetri metrik, diperoleh . Jadi baik selisih maupun kebalikannya tidak melebihi . Kedua pertidaksamaan itu setara dengan . Bukti ini tidak memerlukan titik terdekat dalam , yang memang belum tentu ada.   Geometri metrik supremum  Pada , gunakan metrik supremum . Ambil , , dan . Hitung , deskripsikan sebagai hasil kali interval, dan tentukan apakah berada pada lintasan yang membuat pertidaksamaan segitiga dari ke menjadi kesamaan.   Rubrik. Tampilkan semua selisih koordinat, bedakan bola terbuka dari bola tertutup, dan periksa kedua jarak melalui sebelum menyimpulkan kesamaan segitiga.    Langkah 1. Untuk berada dalam bola terbuka berjari-jari dua, ketiga selisih koordinat harus bernilai mutlak kurang dari dua.   Langkah 2. Hitung maksimum dari , lalu maksimum selisih koordinat untuk pasangan dan .    dan . Selain itu, , sehingga .   Selisih mutlak koordinat dan adalah . Jadi nilai maksimumnya empat dan .  Suatu titik berada dalam tepat ketika , , dan . Oleh karena itu Titik pada muka kotak, tempat salah satu selisih bernilai tepat dua, tidak termasuk karena bolanya terbuka.  Selisih mutlak bagi dan adalah , sedangkan bagi dan juga . Maka kedua jarak tersebut sama dengan dua. Akhirnya, , sehingga pertidaksamaan segitiga menjadi kesamaan melalui . Perhatikan bahwa terletak pada batas, bukan di dalam, bola terbuka .   Batas resiprokal yang sekecil apa pun  Gunakan sifat Archimedes—untuk setiap terdapat dengan —untuk membuktikan pernyataan yang lebih terarah berikut: bagi setiap dan setiap , terdapat dengan dan    Rubrik. Berikan satu pilihan ambang Archimedes yang sekaligus menjamin dan pertidaksamaan resiprokal; jelaskan mengapa membalik pertidaksamaan sah.    Langkah 1. Terapkan sifat Archimedes pada .   Langkah 2. Semua bilangan yang dibalik bersifat positif, jadi setara dengan .   Pilih yang memenuhi . Maka dan .   Tetapkan dan , lalu definisikan . Sifat Archimedes memberi dengan . Karena , kita langsung memperoleh .  Selanjutnya, . Membalik dua bilangan positif membalik arah pertidaksamaan, sehingga . Karena dapat dipilih sebesar apa pun, bukan hanya ada satu resiprokal kecil: terdapat resiprokal dengan indeks yang melampaui setiap ambang yang ditentukan.   Aproksimasi rasional pada ketelitian yang ditentukan  Untuk sembarang dan , berikan konstruksi eksplisit bilangan rasional yang memenuhi . Gunakan hasil latihan sebelumnya dan fungsi lantai. Kemudian jalankan konstruksi tersebut untuk dan dengan memilih .   Rubrik. Nyatakan pilihan dan , turunkan batas galat tanpa mengandalkan desimal, hitung pecahan pada contoh, dan jelaskan mengapa konstruksi membuktikan bahwa rapat dalam .    Langkah 1. Pilih dengan , lalu gunakan .   Langkah 2. Setelah membagi dengan , jarak dari ke kurang dari .   Langkah 3. Untuk contoh, gunakan .   Pilih dengan , tetapkan , dan ambil . Maka . Untuk contoh, dan .   Menurut latihan sebelumnya, pilih sehingga . Ambil bilangan bulat . Definisi fungsi lantai memberi Karena , pembagian dengan mempertahankan arah pertidaksamaan dan menghasilkan Dengan , kita memperoleh , sehingga .  Untuk , , dan , berlaku . Pertidaksamaan dapat diperiksa dengan menguadratkan semua suku positif: . Jadi dan   Konstruksi ini berlaku untuk setiap pusat real dan setiap radius . Karena itu setiap bola terbuka memuat suatu , yang tepat menyatakan bahwa rapat dalam .   "
},
{
  "id": "o003-c90-ch05-mastery-01",
  "level": "2",
  "url": "o003-c90-ch05-mastery.html#o003-c90-ch05-mastery-01",
  "type": "Pemeriksaan",
  "number": "E.49",
  "title": "Infimum, supremum, minimum, dan maksimum.",
  "body": "Infimum, supremum, minimum, dan maksimum  Untuk parameter , definisikan dengan . Tentukan dan , lalu putuskan apakah mempunyai minimum atau maksimum.   Rubrik. Buktikan bahwa setiap nilai yang Anda usulkan memang merupakan batas yang sesuai dan bahwa tidak ada batas bawah yang lebih besar atau batas atas yang lebih kecil. Bedakan dengan tegas antara infimum atau supremum dan anggota himpunan yang menjadi minimum atau maksimum.    Langkah 1. Titik-titik pada interval terbuka dapat mendekati dari kanan sedekat apa pun.   Langkah 2. Barisan meningkat menuju , tetapi tidak pernah mencapainya.   Langkah 3. Untuk menguji minimum atau maksimum, periksa apakah infimum atau supremum tersebut merupakan anggota .    dan . Karena kedua nilai itu tidak berada dalam , himpunan tersebut tidak mempunyai minimum dan tidak mempunyai maksimum.   Setiap anggota interval lebih besar daripada . Selain itu, untuk berlaku . Jadi adalah batas bawah . Jika , pilih . Kita mempunyai , sehingga , dan sekaligus . Maka bukan batas bawah. Jadi .  Setiap anggota lebih kecil daripada , dan untuk setiap . Dengan demikian adalah batas atas. Jika , sifat Archimedes memberi dengan . Akibatnya , sehingga bukan batas atas. Oleh karena itu .  Interval tidak memuat , sedangkan setiap unsur barisan sedikitnya ; jadi . Demikian pula, tidak satu pun dari kedua bagian pembentuk memuat . Karena minimum harus sama dengan infimum dan maksimum harus sama dengan supremum, tidak mempunyai minimum maupun maksimum.  "
},
{
  "id": "o003-c90-ch05-mastery-02",
  "level": "2",
  "url": "o003-c90-ch05-mastery.html#o003-c90-ch05-mastery-02",
  "type": "Pemeriksaan",
  "number": "E.50",
  "title": "Jarak nol dan penutupan.",
  "body": "Jarak nol dan penutupan  Misalkan ruang metrik, tak kosong, dan . Buktikan bahwa    Rubrik. Buktikan kedua implikasi dengan definisi penutupan melalui bola terbuka; nyatakan secara eksplisit bagaimana sifat infimum menghasilkan titik pada jarak kurang dari .    Langkah 1. Jika , maka untuk setiap .   Langkah 2. Jika infimum himpunan jarak adalah nol tetapi tidak ada jarak yang lebih kecil daripada suatu , maka akan menjadi batas bawah positif.   Kesetaraan itu benar: tepat ketika setiap bola terbuka berpusat di bertemu , dan kondisi terakhir adalah definisi .   Andaikan . Untuk setiap , ada dengan . Karena infimum tidak melebihi setiap anggota himpunan yang diinfimumkan, . Tidak ada bilangan real positif yang lebih kecil daripada setiap ; maka .  Sebaliknya, andaikan . Ambil sembarang . Jika semua memenuhi , maka merupakan batas bawah himpunan , bertentangan dengan fakta bahwa batas bawah terbesarnya adalah nol. Jadi terdapat dengan . Artinya untuk setiap radius positif, sehingga .  "
},
{
  "id": "o003-c90-ch05-mastery-03",
  "level": "2",
  "url": "o003-c90-ch05-mastery.html#o003-c90-ch05-mastery-03",
  "type": "Pemeriksaan",
  "number": "E.51",
  "title": "Fungsi jarak bersifat 1-Lipschitz.",
  "body": "Fungsi jarak bersifat 1-Lipschitz  Dalam keadaan latihan sebelumnya, definisikan dengan . Buktikan bahwa untuk semua ,    Rubrik. Gunakan pertidaksamaan segitiga sebelum mengambil infimum, peroleh dua pertidaksamaan satu arah dengan menukar dan , lalu gabungkan keduanya. Jangan mengandaikan bahwa infimum dicapai oleh suatu anggota .    Langkah 1. Untuk setiap , berlaku .   Langkah 2. Ambil infimum terhadap , lalu ulangi dengan menukar dan .   Fungsi bersifat 1-Lipschitz: untuk setiap .   Tetapkan . Untuk setiap , pertidaksamaan segitiga memberi . Karena adalah infimum nilai-nilai di ruas kiri, kita mempunyai untuk setiap . Mengambil infimum ruas kanan terhadap menghasilkan sehingga .  Dengan menukar dan serta memakai simetri metrik, diperoleh . Jadi baik selisih maupun kebalikannya tidak melebihi . Kedua pertidaksamaan itu setara dengan . Bukti ini tidak memerlukan titik terdekat dalam , yang memang belum tentu ada.  "
},
{
  "id": "o003-c90-ch05-mastery-04",
  "level": "2",
  "url": "o003-c90-ch05-mastery.html#o003-c90-ch05-mastery-04",
  "type": "Pemeriksaan",
  "number": "E.52",
  "title": "Geometri metrik supremum.",
  "body": "Geometri metrik supremum  Pada , gunakan metrik supremum . Ambil , , dan . Hitung , deskripsikan sebagai hasil kali interval, dan tentukan apakah berada pada lintasan yang membuat pertidaksamaan segitiga dari ke menjadi kesamaan.   Rubrik. Tampilkan semua selisih koordinat, bedakan bola terbuka dari bola tertutup, dan periksa kedua jarak melalui sebelum menyimpulkan kesamaan segitiga.    Langkah 1. Untuk berada dalam bola terbuka berjari-jari dua, ketiga selisih koordinat harus bernilai mutlak kurang dari dua.   Langkah 2. Hitung maksimum dari , lalu maksimum selisih koordinat untuk pasangan dan .    dan . Selain itu, , sehingga .   Selisih mutlak koordinat dan adalah . Jadi nilai maksimumnya empat dan .  Suatu titik berada dalam tepat ketika , , dan . Oleh karena itu Titik pada muka kotak, tempat salah satu selisih bernilai tepat dua, tidak termasuk karena bolanya terbuka.  Selisih mutlak bagi dan adalah , sedangkan bagi dan juga . Maka kedua jarak tersebut sama dengan dua. Akhirnya, , sehingga pertidaksamaan segitiga menjadi kesamaan melalui . Perhatikan bahwa terletak pada batas, bukan di dalam, bola terbuka .  "
},
{
  "id": "o003-c90-ch05-mastery-05",
  "level": "2",
  "url": "o003-c90-ch05-mastery.html#o003-c90-ch05-mastery-05",
  "type": "Pemeriksaan",
  "number": "E.53",
  "title": "Batas resiprokal yang sekecil apa pun.",
  "body": "Batas resiprokal yang sekecil apa pun  Gunakan sifat Archimedes—untuk setiap terdapat dengan —untuk membuktikan pernyataan yang lebih terarah berikut: bagi setiap dan setiap , terdapat dengan dan    Rubrik. Berikan satu pilihan ambang Archimedes yang sekaligus menjamin dan pertidaksamaan resiprokal; jelaskan mengapa membalik pertidaksamaan sah.    Langkah 1. Terapkan sifat Archimedes pada .   Langkah 2. Semua bilangan yang dibalik bersifat positif, jadi setara dengan .   Pilih yang memenuhi . Maka dan .   Tetapkan dan , lalu definisikan . Sifat Archimedes memberi dengan . Karena , kita langsung memperoleh .  Selanjutnya, . Membalik dua bilangan positif membalik arah pertidaksamaan, sehingga . Karena dapat dipilih sebesar apa pun, bukan hanya ada satu resiprokal kecil: terdapat resiprokal dengan indeks yang melampaui setiap ambang yang ditentukan.  "
},
{
  "id": "o003-c90-ch05-mastery-06",
  "level": "2",
  "url": "o003-c90-ch05-mastery.html#o003-c90-ch05-mastery-06",
  "type": "Pemeriksaan",
  "number": "E.54",
  "title": "Aproksimasi rasional pada ketelitian yang ditentukan.",
  "body": "Aproksimasi rasional pada ketelitian yang ditentukan  Untuk sembarang dan , berikan konstruksi eksplisit bilangan rasional yang memenuhi . Gunakan hasil latihan sebelumnya dan fungsi lantai. Kemudian jalankan konstruksi tersebut untuk dan dengan memilih .   Rubrik. Nyatakan pilihan dan , turunkan batas galat tanpa mengandalkan desimal, hitung pecahan pada contoh, dan jelaskan mengapa konstruksi membuktikan bahwa rapat dalam .    Langkah 1. Pilih dengan , lalu gunakan .   Langkah 2. Setelah membagi dengan , jarak dari ke kurang dari .   Langkah 3. Untuk contoh, gunakan .   Pilih dengan , tetapkan , dan ambil . Maka . Untuk contoh, dan .   Menurut latihan sebelumnya, pilih sehingga . Ambil bilangan bulat . Definisi fungsi lantai memberi Karena , pembagian dengan mempertahankan arah pertidaksamaan dan menghasilkan Dengan , kita memperoleh , sehingga .  Untuk , , dan , berlaku . Pertidaksamaan dapat diperiksa dengan menguadratkan semua suku positif: . Jadi dan   Konstruksi ini berlaku untuk setiap pusat real dan setiap radius . Karena itu setiap bola terbuka memuat suatu , yang tepat menyatakan bahwa rapat dalam .  "
},
{
  "id": "o003-c90-ch06-source-guides",
  "level": "1",
  "url": "o003-c90-ch06-source-guides.html",
  "type": "Bagian",
  "number": "",
  "title": "Panduan kegiatan sumber",
  "body": " Panduan kegiatan sumber  Tiga belas panduan berikut mengikuti semua tugas yang benar-benar meminta jawaban dalam kegiatan Bab 6: empat tugas pendahuluan, lima tugas tentang fungsi antara ruang metrik, dan empat tugas tentang komposisi. Kerjakan pernyataan pada bab utama sebelum membuka petunjuk, jawaban, dan pembahasan.  Toleransi di titik  Untuk , tentukan sedemikian sehingga setiap kali . Jelaskan metode Anda. Rubrik: berikan satu nilai yang sah dan buktikan implikasinya; pembacaan graf saja belum merupakan pembuktian.   Tulis selisih sebagai , lalu gunakan dan .   Salah satu pilihan yang sah adalah .   Karena , pertidaksamaan segitiga dan Teorema Nilai Rata-Rata, yang memberi sebab , menghasilkan Jika , maka . Jadi nilai tersebut memenuhi syarat.   Toleransi di titik  Untuk , tentukan sedemikian sehingga setiap kali . Jelaskan metode Anda. Rubrik: hubungkan batas jarak masukan dengan batas jarak keluaran secara eksplisit.   Tambahkan dan kurangkan . Batas yang dihasilkan adalah .   Salah satu pilihan yang sah adalah .   Dengan , kita mempunyai Di sini digunakan dan, melalui Teorema Nilai Rata-Rata serta , . Jika , maka . Jadi memenuhi syarat.   Negasi kekontinuan di suatu titik  Nyatakan negasi definisi bahwa kontinu di . Rubrik: balikkan seluruh urutan kuantor dan negasikan pertidaksamaan keluaran dengan tepat.   Negasi pernyataan untuk setiap terdapat sehingga untuk setiap berlaku implikasi dimulai dengan terdapat sehingga untuk setiap terdapat .   Fungsi tidak kontinu di jika terdapat sedemikian sehingga, untuk setiap , terdapat dengan tetapi .   Kekontinuan di menyatakan Ketika menegasikan, kuantor universal dan eksistensial saling bertukar. Negasi suatu implikasi adalah , dan negasi adalah . Karena itu negasinya persis pernyataan pada jawaban. Satu toleransi keluaran tetap harus gagal pada setiap skala masukan.   Diskontinuitas fungsi loncatan  Misalkan untuk dan untuk . Gunakan negasi definisi untuk membuktikan bahwa tidak kontinu di . Rubrik: pilih satu dan, untuk sebarang , berikan saksi yang bergantung pada .   Ambil titik sedikit di sebelah kiri , misalnya , dan bandingkan dengan .   Ambil . Untuk setiap , titik memenuhi , tetapi .   Nilai fungsi di titik pangkal adalah . Tetapkan dan ambil sebarang . Untuk , berlaku , sehingga , serta . Akan tetapi, Jadi toleransi keluaran gagal untuk setiap pilihan . Ini tepat negasi kekontinuan di .   Fungsi konstan selalu kontinu  Misalkan dan ruang metrik, , dan didefinisikan oleh . Buktikan bahwa kontinu. Rubrik: periksa definisi di titik sebarang dan berikan pilihan yang tidak bergantung pada .   Berapa nilai untuk dua titik masukan mana pun?   Fungsi kontinu; di setiap titik dapat dipilih, misalnya, untuk setiap .   Ambil sebarang dan . Pilih . Jika , maka karena fungsi tersebut konstan, Jadi kontinu di setiap , dan karenanya kontinu pada . Jika kosong, pernyataan itu berlaku secara hampa.   Kekontinuan fungsi identitas  Untuk ruang metrik , buktikan bahwa fungsi identitas , dengan , kontinu. Rubrik: nyatakan pilihan sebagai fungsi dari dan hitung jarak keluaran.   Domain dan kodomain memakai metrik yang sama, sehingga .   Fungsi identitas kontinu; untuk setiap dan , pilih .   Ambil sebarang dan , lalu tetapkan . Jika , maka Jadi kontinu di . Karena sebarang, kontinu pada seluruh .   Dua metrik pada fungsi identitas  Jelaskan mengapa kekontinuan fungsi identitas pada butir sebelumnya tidak bertentangan dengan contoh fungsi identitas dari bermetrik Euklides ke bermetrik diskret yang tidak kontinu. Rubrik: bedakan fungsi sebagai aturan dari ruang bermetrik yang menjadi domain dan kodomainnya.   Tanyakan apakah jarak pada domain dan kodomain sama dalam kedua pernyataan tersebut.   Tidak ada pertentangan: butir sebelumnya memakai metrik yang sama pada domain dan kodomain, sedangkan contoh tersebut memakai metrik Euklides pada domain dan metrik diskret pada kodomain.   Rumus kedua fungsi memang sama, yaitu , tetapi kekontinuan bergantung pada metrik. Untuk , jarak keluaran sama persis dengan jarak masukan. Pada contoh , titik berbeda dapat sedekat apa pun menurut , tetapi jarak keluarannya selalu menurut . Jadi untuk, misalnya, , tidak ada yang bekerja. Perbedaan metrik menjelaskan perbedaan kesimpulan.   Dari metrik taksi ke metrik maksimum  Pada , misalkan adalah metrik taksi dan metrik maksimum. Untuk , buktikan atau sangkal bahwa kontinu. Rubrik: turunkan satu batas global yang membandingkan jarak keluaran dengan jarak masukan.   Untuk dan , batasi dengan pertidaksamaan segitiga.   Fungsi tersebut kontinu, bahkan . Pilihan berlaku di setiap titik.   Ambil dan . Maka Sekarang ambil sebarang titik dan , serta pilih . Jika , pertidaksamaan di atas memberi . Jadi kontinu.   Dari metrik maksimum ke metrik taksi  Dengan fungsi yang sama, buktikan atau sangkal bahwa kontinu. Rubrik: batasi jumlah dua jarak koordinat keluaran dengan kelipatan jarak maksimum masukan.   Setelah memakai pertidaksamaan segitiga pada koordinat pertama, masing-masing dan tidak melebihi .   Fungsi tersebut kontinu, karena . Pilihan berlaku di setiap titik.   Untuk dan , berlaku Untuk sebarang titik dan , pilih . Jika , maka . Jadi kontinu.   Memulai bukti kekontinuan komposisi  Misalkan dan kontinu. Nyatakan apa yang harus dibuktikan agar kontinu dan sebutkan dua langkah pertama bukti. Rubrik: mulai di titik domain sebarang dan dengan toleransi keluaran sebarang.   Buka definisi kekontinuan pada seluruh ruang: pertama pilih , kemudian pilih .   Ambil sebarang dan . Harus ditemukan sehingga mengakibatkan .   Kekontinuan berarti kekontinuan di setiap titik . Karena itu dua langkah pertama adalah menetapkan sebarang dan kemudian sebarang . Setelah itu kita harus membangun , yang boleh bergantung pada dan tetapi tidak pada , agar Butir berikutnya membangun melalui ruang antara .   Toleransi di ruang antara  Dengan , , dan , jelaskan mengapa terdapat sehingga mengakibatkan . Rubrik: sebutkan hipotesis dan titik tempat definisi diterapkan.   Terapkan kekontinuan di titik dengan toleransi keluaran .   Keberadaan adalah persis konsekuensi kekontinuan di .   Karena , titik berada dalam . Hipotesis menyatakan bahwa kontinu pada , khususnya di . Dengan menerapkan definisi kekontinuan di pada bilangan yang telah dipilih, kita memperoleh sedemikian sehingga untuk setiap ,    Mengangkut toleransi ke domain  Jelaskan mengapa terdapat sehingga mengakibatkan . Rubrik: gunakan sebagai toleransi keluaran untuk fungsi yang tepat.   Terapkan kekontinuan di dengan pada definisi diganti oleh .   Keberadaan adalah persis konsekuensi kekontinuan di dengan toleransi keluaran .   Hipotesis menyatakan bahwa kontinu pada , khususnya di titik . Bilangan yang diperoleh pada butir sebelumnya positif, sehingga sah dipakai sebagai toleransi keluaran dalam definisi kekontinuan . Oleh karena itu ada sedemikian sehingga    Komposisi fungsi kontinu  Lengkapi pembuktian bahwa kontinu. Rubrik: rangkai dua implikasi metrik, identifikasi , lalu tutup semua kuantor.   Pilih . Kedekatan di mula-mula memberi kedekatan dengan di , lalu memberi kedekatan setelah menerapkan .   Dengan , berlaku mengakibatkan . Jadi kontinu.   Ambil sebarang dan , lalu tetapkan . Kekontinuan di menghasilkan sehingga mengakibatkan . Kekontinuan di , dengan toleransi keluaran , menghasilkan sehingga mengakibatkan .  Pilih . Jika , maka , dan karenanya . Karena , ini adalah . Jadi komposisi kontinu di ; karena sebarang, komposisi kontinu pada .   "
},
{
  "id": "o003-c90-ch06-intro-task-01",
  "level": "2",
  "url": "o003-c90-ch06-source-guides.html#o003-c90-ch06-intro-task-01",
  "type": "Pemeriksaan",
  "number": "F.1",
  "title": "Toleransi di titik <span class=\"process-math\">\\(x=1\\)<\/span>.",
  "body": "Toleransi di titik  Untuk , tentukan sedemikian sehingga setiap kali . Jelaskan metode Anda. Rubrik: berikan satu nilai yang sah dan buktikan implikasinya; pembacaan graf saja belum merupakan pembuktian.   Tulis selisih sebagai , lalu gunakan dan .   Salah satu pilihan yang sah adalah .   Karena , pertidaksamaan segitiga dan Teorema Nilai Rata-Rata, yang memberi sebab , menghasilkan Jika , maka . Jadi nilai tersebut memenuhi syarat.  "
},
{
  "id": "o003-c90-ch06-intro-task-02",
  "level": "2",
  "url": "o003-c90-ch06-source-guides.html#o003-c90-ch06-intro-task-02",
  "type": "Pemeriksaan",
  "number": "F.2",
  "title": "Toleransi di titik <span class=\"process-math\">\\(x=2.5\\)<\/span>.",
  "body": "Toleransi di titik  Untuk , tentukan sedemikian sehingga setiap kali . Jelaskan metode Anda. Rubrik: hubungkan batas jarak masukan dengan batas jarak keluaran secara eksplisit.   Tambahkan dan kurangkan . Batas yang dihasilkan adalah .   Salah satu pilihan yang sah adalah .   Dengan , kita mempunyai Di sini digunakan dan, melalui Teorema Nilai Rata-Rata serta , . Jika , maka . Jadi memenuhi syarat.  "
},
{
  "id": "o003-c90-ch06-intro-task-03",
  "level": "2",
  "url": "o003-c90-ch06-source-guides.html#o003-c90-ch06-intro-task-03",
  "type": "Pemeriksaan",
  "number": "F.3",
  "title": "Negasi kekontinuan di suatu titik.",
  "body": "Negasi kekontinuan di suatu titik  Nyatakan negasi definisi bahwa kontinu di . Rubrik: balikkan seluruh urutan kuantor dan negasikan pertidaksamaan keluaran dengan tepat.   Negasi pernyataan untuk setiap terdapat sehingga untuk setiap berlaku implikasi dimulai dengan terdapat sehingga untuk setiap terdapat .   Fungsi tidak kontinu di jika terdapat sedemikian sehingga, untuk setiap , terdapat dengan tetapi .   Kekontinuan di menyatakan Ketika menegasikan, kuantor universal dan eksistensial saling bertukar. Negasi suatu implikasi adalah , dan negasi adalah . Karena itu negasinya persis pernyataan pada jawaban. Satu toleransi keluaran tetap harus gagal pada setiap skala masukan.  "
},
{
  "id": "o003-c90-ch06-intro-task-04",
  "level": "2",
  "url": "o003-c90-ch06-source-guides.html#o003-c90-ch06-intro-task-04",
  "type": "Pemeriksaan",
  "number": "F.4",
  "title": "Diskontinuitas fungsi loncatan.",
  "body": "Diskontinuitas fungsi loncatan  Misalkan untuk dan untuk . Gunakan negasi definisi untuk membuktikan bahwa tidak kontinu di . Rubrik: pilih satu dan, untuk sebarang , berikan saksi yang bergantung pada .   Ambil titik sedikit di sebelah kiri , misalnya , dan bandingkan dengan .   Ambil . Untuk setiap , titik memenuhi , tetapi .   Nilai fungsi di titik pangkal adalah . Tetapkan dan ambil sebarang . Untuk , berlaku , sehingga , serta . Akan tetapi, Jadi toleransi keluaran gagal untuk setiap pilihan . Ini tepat negasi kekontinuan di .  "
},
{
  "id": "o003-c90-ch06-between-task-01",
  "level": "2",
  "url": "o003-c90-ch06-source-guides.html#o003-c90-ch06-between-task-01",
  "type": "Pemeriksaan",
  "number": "F.5",
  "title": "Fungsi konstan selalu kontinu.",
  "body": "Fungsi konstan selalu kontinu  Misalkan dan ruang metrik, , dan didefinisikan oleh . Buktikan bahwa kontinu. Rubrik: periksa definisi di titik sebarang dan berikan pilihan yang tidak bergantung pada .   Berapa nilai untuk dua titik masukan mana pun?   Fungsi kontinu; di setiap titik dapat dipilih, misalnya, untuk setiap .   Ambil sebarang dan . Pilih . Jika , maka karena fungsi tersebut konstan, Jadi kontinu di setiap , dan karenanya kontinu pada . Jika kosong, pernyataan itu berlaku secara hampa.  "
},
{
  "id": "o003-c90-ch06-between-task-02",
  "level": "2",
  "url": "o003-c90-ch06-source-guides.html#o003-c90-ch06-between-task-02",
  "type": "Pemeriksaan",
  "number": "F.6",
  "title": "Kekontinuan fungsi identitas.",
  "body": "Kekontinuan fungsi identitas  Untuk ruang metrik , buktikan bahwa fungsi identitas , dengan , kontinu. Rubrik: nyatakan pilihan sebagai fungsi dari dan hitung jarak keluaran.   Domain dan kodomain memakai metrik yang sama, sehingga .   Fungsi identitas kontinu; untuk setiap dan , pilih .   Ambil sebarang dan , lalu tetapkan . Jika , maka Jadi kontinu di . Karena sebarang, kontinu pada seluruh .  "
},
{
  "id": "o003-c90-ch06-between-task-03",
  "level": "2",
  "url": "o003-c90-ch06-source-guides.html#o003-c90-ch06-between-task-03",
  "type": "Pemeriksaan",
  "number": "F.7",
  "title": "Dua metrik pada fungsi identitas.",
  "body": "Dua metrik pada fungsi identitas  Jelaskan mengapa kekontinuan fungsi identitas pada butir sebelumnya tidak bertentangan dengan contoh fungsi identitas dari bermetrik Euklides ke bermetrik diskret yang tidak kontinu. Rubrik: bedakan fungsi sebagai aturan dari ruang bermetrik yang menjadi domain dan kodomainnya.   Tanyakan apakah jarak pada domain dan kodomain sama dalam kedua pernyataan tersebut.   Tidak ada pertentangan: butir sebelumnya memakai metrik yang sama pada domain dan kodomain, sedangkan contoh tersebut memakai metrik Euklides pada domain dan metrik diskret pada kodomain.   Rumus kedua fungsi memang sama, yaitu , tetapi kekontinuan bergantung pada metrik. Untuk , jarak keluaran sama persis dengan jarak masukan. Pada contoh , titik berbeda dapat sedekat apa pun menurut , tetapi jarak keluarannya selalu menurut . Jadi untuk, misalnya, , tidak ada yang bekerja. Perbedaan metrik menjelaskan perbedaan kesimpulan.  "
},
{
  "id": "o003-c90-ch06-between-task-04",
  "level": "2",
  "url": "o003-c90-ch06-source-guides.html#o003-c90-ch06-between-task-04",
  "type": "Pemeriksaan",
  "number": "F.8",
  "title": "Dari metrik taksi ke metrik maksimum.",
  "body": "Dari metrik taksi ke metrik maksimum  Pada , misalkan adalah metrik taksi dan metrik maksimum. Untuk , buktikan atau sangkal bahwa kontinu. Rubrik: turunkan satu batas global yang membandingkan jarak keluaran dengan jarak masukan.   Untuk dan , batasi dengan pertidaksamaan segitiga.   Fungsi tersebut kontinu, bahkan . Pilihan berlaku di setiap titik.   Ambil dan . Maka Sekarang ambil sebarang titik dan , serta pilih . Jika , pertidaksamaan di atas memberi . Jadi kontinu.  "
},
{
  "id": "o003-c90-ch06-between-task-05",
  "level": "2",
  "url": "o003-c90-ch06-source-guides.html#o003-c90-ch06-between-task-05",
  "type": "Pemeriksaan",
  "number": "F.9",
  "title": "Dari metrik maksimum ke metrik taksi.",
  "body": "Dari metrik maksimum ke metrik taksi  Dengan fungsi yang sama, buktikan atau sangkal bahwa kontinu. Rubrik: batasi jumlah dua jarak koordinat keluaran dengan kelipatan jarak maksimum masukan.   Setelah memakai pertidaksamaan segitiga pada koordinat pertama, masing-masing dan tidak melebihi .   Fungsi tersebut kontinu, karena . Pilihan berlaku di setiap titik.   Untuk dan , berlaku Untuk sebarang titik dan , pilih . Jika , maka . Jadi kontinu.  "
},
{
  "id": "o003-c90-ch06-composition-task-01",
  "level": "2",
  "url": "o003-c90-ch06-source-guides.html#o003-c90-ch06-composition-task-01",
  "type": "Pemeriksaan",
  "number": "F.10",
  "title": "Memulai bukti kekontinuan komposisi.",
  "body": "Memulai bukti kekontinuan komposisi  Misalkan dan kontinu. Nyatakan apa yang harus dibuktikan agar kontinu dan sebutkan dua langkah pertama bukti. Rubrik: mulai di titik domain sebarang dan dengan toleransi keluaran sebarang.   Buka definisi kekontinuan pada seluruh ruang: pertama pilih , kemudian pilih .   Ambil sebarang dan . Harus ditemukan sehingga mengakibatkan .   Kekontinuan berarti kekontinuan di setiap titik . Karena itu dua langkah pertama adalah menetapkan sebarang dan kemudian sebarang . Setelah itu kita harus membangun , yang boleh bergantung pada dan tetapi tidak pada , agar Butir berikutnya membangun melalui ruang antara .  "
},
{
  "id": "o003-c90-ch06-composition-task-02",
  "level": "2",
  "url": "o003-c90-ch06-source-guides.html#o003-c90-ch06-composition-task-02",
  "type": "Pemeriksaan",
  "number": "F.11",
  "title": "Toleransi di ruang antara.",
  "body": "Toleransi di ruang antara  Dengan , , dan , jelaskan mengapa terdapat sehingga mengakibatkan . Rubrik: sebutkan hipotesis dan titik tempat definisi diterapkan.   Terapkan kekontinuan di titik dengan toleransi keluaran .   Keberadaan adalah persis konsekuensi kekontinuan di .   Karena , titik berada dalam . Hipotesis menyatakan bahwa kontinu pada , khususnya di . Dengan menerapkan definisi kekontinuan di pada bilangan yang telah dipilih, kita memperoleh sedemikian sehingga untuk setiap ,   "
},
{
  "id": "o003-c90-ch06-composition-task-03",
  "level": "2",
  "url": "o003-c90-ch06-source-guides.html#o003-c90-ch06-composition-task-03",
  "type": "Pemeriksaan",
  "number": "F.12",
  "title": "Mengangkut toleransi ke domain.",
  "body": "Mengangkut toleransi ke domain  Jelaskan mengapa terdapat sehingga mengakibatkan . Rubrik: gunakan sebagai toleransi keluaran untuk fungsi yang tepat.   Terapkan kekontinuan di dengan pada definisi diganti oleh .   Keberadaan adalah persis konsekuensi kekontinuan di dengan toleransi keluaran .   Hipotesis menyatakan bahwa kontinu pada , khususnya di titik . Bilangan yang diperoleh pada butir sebelumnya positif, sehingga sah dipakai sebagai toleransi keluaran dalam definisi kekontinuan . Oleh karena itu ada sedemikian sehingga   "
},
{
  "id": "o003-c90-ch06-composition-task-04",
  "level": "2",
  "url": "o003-c90-ch06-source-guides.html#o003-c90-ch06-composition-task-04",
  "type": "Pemeriksaan",
  "number": "F.13",
  "title": "Komposisi fungsi kontinu.",
  "body": "Komposisi fungsi kontinu  Lengkapi pembuktian bahwa kontinu. Rubrik: rangkai dua implikasi metrik, identifikasi , lalu tutup semua kuantor.   Pilih . Kedekatan di mula-mula memberi kedekatan dengan di , lalu memberi kedekatan setelah menerapkan .   Dengan , berlaku mengakibatkan . Jadi kontinu.   Ambil sebarang dan , lalu tetapkan . Kekontinuan di menghasilkan sehingga mengakibatkan . Kekontinuan di , dengan toleransi keluaran , menghasilkan sehingga mengakibatkan .  Pilih . Jika , maka , dan karenanya . Karena , ini adalah . Jadi komposisi kontinu di ; karena sebarang, komposisi kontinu pada .  "
},
{
  "id": "o003-c90-ch06-exercise-guides-a",
  "level": "1",
  "url": "o003-c90-ch06-exercise-guides-a.html",
  "type": "Bagian",
  "number": "",
  "title": "Panduan latihan sumber, bagian pertama",
  "body": " Panduan latihan sumber, bagian pertama  Tiga belas panduan berikut berkorespondensi dengan tiga belas perintah pertama pada bagian latihan Bab 6 menurut urutan kedalaman sumber. Latihan yang hanya mempunyai pernyataan dihitung sekali; pada latihan bertingkat, hanya tugas daun yang meminta jawaban yang dihitung.  Kekontinuan fungsi nilai mutlak di nol  Misalkan didefinisikan oleh , dengan metrik Euklides pada domain dan kodomain. Tentukan apakah kontinu di dan buktikan jawaban Anda. Rubrik: mulai dari sebarang , nyatakan , dan periksa implikasi definisi.   Karena , sederhanakan sebelum memilih .   Ya. Untuk setiap , pilihan memenuhi definisi kekontinuan di .   Ambil sebarang dan pilih . Jika , maka Jadi syarat epsilon-delta terpenuhi dan kontinu di .   Diskontinuitas fungsi tanda di nol  Misalkan untuk dan , dengan metrik Euklides. Tentukan apakah kontinu di dan buktikan jawaban Anda. Rubrik: jika jawabannya negatif, nyatakan negasi definisi beserta satu saksi untuk setiap .   Ambil titik negatif yang berjarak kurang daripada dari , misalnya .   Tidak. Dengan , untuk setiap titik memenuhi , tetapi .   Tetapkan dan ambil sebarang . Pilih . Maka , sedangkan sehingga . Karena , Satu toleransi keluaran gagal pada setiap skala masukan. Menurut negasi definisi, tidak kontinu di .   Penjumlahan koordinat dengan metrik Euklides  Dengan metrik Euklides pada dan , buktikan atau sangkal bahwa kontinu. Rubrik: bandingkan nilai mutlak selisih keluaran dengan jarak Euklides dua titik masukan.   Gunakan pertidaksamaan Cauchy pada vektor dan .   Fungsi tersebut kontinu, bahkan . Pilih .   Untuk dan , pertidaksamaan Cauchy memberikan Ambil sebarang dan , lalu pilih . Jika , batas di atas memberi . Jadi kontinu.   Penjumlahan koordinat dengan metrik maksimum  Dengan metrik maksimum pada domain dan metrik Euklides pada kodomain , buktikan atau sangkal bahwa kontinu. Rubrik: turunkan batas yang berlaku bagi semua pasangan titik dan berikan pilihan .   Masing-masing selisih koordinat tidak melebihi jarak maksimum.   Fungsi tersebut kontinu, karena . Pilih .   Untuk dan , Ambil sebarang dan , serta pilih . Jika , maka . Jadi kontinu.   Semua fungsi dari ruang diskret  Misalkan memakai metrik diskret dan sebarang ruang metrik. Tentukan semua fungsi kontinu . Rubrik: buktikan klasifikasi Anda langsung dari definisi; jangan mengasumsikan sifat khusus kodomain.   Jika , apa yang dapat disimpulkan tentang dan ?   Setiap fungsi kontinu ketika domain memakai metrik diskret.   Ambil fungsi sebarang , titik sebarang , dan . Pilih . Jika , definisi metrik diskret memaksa . Karena itu Jadi setiap fungsi kontinu di setiap titik domain. Tidak ada syarat tambahan pada atau pada metrik .   Kelipatan skalar fungsi kontinu  Misalkan kontinu dan . Buktikan bahwa fungsi , yang didefinisikan oleh , kontinu. Rubrik: gunakan kekontinuan dengan toleransi keluaran yang disesuaikan oleh .   Karena , mintalah .   Fungsi kontinu. Untuk toleransi , pakai dalam definisi kekontinuan .   Ambil sebarang dan . Karena , bilangan positif. Kekontinuan di memberikan sedemikian sehingga mengakibatkan . Maka Jadi kontinu di setiap , sehingga kontinu pada .   Jumlah dua fungsi kontinu  Misalkan kontinu. Buktikan bahwa , yang didefinisikan oleh , kontinu. Rubrik: alokasikan toleransi keluaran di antara dua suku dan gabungkan dua skala masukan.   Gunakan toleransi untuk masing-masing fungsi dan pilih nilai minimum dari dua yang dihasilkan.   Fungsi kontinu; jika dan bekerja untuk toleransi , pilih .   Ambil sebarang dan . Kekontinuan dan di memberikan sehingga, berturut-turut, mengakibatkan dan mengakibatkan .  Pilih . Jika , kedua batas berlaku dan Jadi kontinu.   Menguraikan selisih hasil kali  Untuk fungsi dan serta titik , buktikan identitas Rubrik: perluas kedua faktor setelah menambahkan dan mengurangkan nilai di , lalu sederhanakan seluruh suku.   Substitusikan dan ke dalam .   Identitas tersebut benar; ia diperoleh dengan memperluas hasil kali dua jumlah dan membatalkan suku .   Tuliskan dan . Maka Mengembalikan definisi dan menghasilkan tepat identitas yang diminta. Bentuk ini memisahkan dua suku linear dan satu suku hasil kali yang masing-masing dapat dikendalikan oleh kekontinuan dan .   Empat skala untuk bukti hasil kali  Misalkan dan kontinu di dan . Jelaskan mengapa ada yang masing-masing menjamin Rubrik: pasangkan setiap toleransi positif dengan fungsi yang sesuai.   Keempat ruas kanan positif. Terapkan definisi kekontinuan dua kali dan definisi kekontinuan dua kali.   Kekontinuan menghasilkan dan ; kekontinuan menghasilkan dan , dengan toleransi keluaran sesuai urutan yang ditampilkan.   Karena , semua bilangan , , dan positif. Kekontinuan di , berturut-turut dengan toleransi dan , memberikan dan . Kekontinuan di , berturut-turut dengan toleransi dan , memberikan dan . Masing-masing definisi tepat menghasilkan implikasi yang diminta ketika lebih kecil daripada terkait.   Hasil kali dua fungsi kontinu  Gunakan penguraian selisih dan empat skala pada dua butir sebelumnya untuk membuktikan bahwa kontinu di . Rubrik: pilih satu yang mengaktifkan keempat batas dan tunjukkan bahwa masing-masing dari tiga suku bernilai kurang daripada .   Pilih . Gunakan dan analoginya untuk .   Dengan sebagai minimum keempat skala, tiga suku dalam batas segitiga masing-masing kurang daripada ; karena itu .   Pilih . Jika , penguraian pada butir pertama dan pertidaksamaan segitiga memberikan Batas dari menjadikan suku pertama kurang daripada . Batas dari menjadikan suku kedua kurang daripada . Batas dari dan menjadikan suku ketiga kurang daripada . Jadi seluruh jumlah kurang daripada , sehingga kontinu di .   Kebalikan pernyataan tentang jumlah  Tentukan apakah kekontinuan memaksa dan masing-masing kontinu. Buktikan jawaban Anda. Rubrik: jika pernyataan salah, berikan fungsi konkret, periksa jumlahnya, dan buktikan diskontinuitas kedua suku yang diperlukan.   Ambil suatu fungsi tak kontinu , lalu pertimbangkan dan .   Tidak. Jika untuk dan untuk , maka dan tidak kontinu di , tetapi kontinu.   Definisikan dengan jika dan jika . Fungsi tidak kontinu di : untuk dan setiap , titik memenuhi , tetapi . Fungsi juga tidak kontinu di dengan argumen yang sama.  Ambil dan . Untuk setiap , , sehingga adalah fungsi konstan dan kontinu. Jadi kekontinuan jumlah tidak memaksa kekontinuan kedua sukunya.   Kebalikan pernyataan tentang hasil kali  Tentukan apakah kekontinuan memaksa dan masing-masing kontinu. Buktikan jawaban Anda. Rubrik: berikan contoh tandingan konkret dan verifikasi baik hasil kali maupun diskontinuitas faktor-faktornya.   Carilah fungsi tak kontinu yang hanya bernilai dan , lalu kalikan fungsi itu dengan dirinya sendiri.   Tidak. Jika untuk dan untuk , maka tidak kontinu di , tetapi kontinu.   Definisikan dengan untuk dan untuk . Fungsi ini tidak kontinu di : tetapkan ; untuk setiap , titik memenuhi , tetapi .  Ambil . Kedua faktor tidak kontinu di , sedangkan untuk setiap , . Hasil kali tersebut adalah fungsi konstan, sehingga kontinu. Jadi pernyataannya salah.   Skala eksplisit untuk fungsi kuadrat  Misalkan . Untuk , carilah sedemikian sehingga mengakibatkan . Rubrik: berikan satu nilai sah dan buktikan batasnya secara aljabar.   Faktorkan . Jika , maka .   Salah satu pilihan yang sah adalah .   Pilih ; khususnya . Jika , maka . Oleh karena itu Jadi memenuhi implikasi yang diminta.   "
},
{
  "id": "o003-c90-ch06-exercise-task-01",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-a.html#o003-c90-ch06-exercise-task-01",
  "type": "Pemeriksaan",
  "number": "F.14",
  "title": "Kekontinuan fungsi nilai mutlak di nol.",
  "body": "Kekontinuan fungsi nilai mutlak di nol  Misalkan didefinisikan oleh , dengan metrik Euklides pada domain dan kodomain. Tentukan apakah kontinu di dan buktikan jawaban Anda. Rubrik: mulai dari sebarang , nyatakan , dan periksa implikasi definisi.   Karena , sederhanakan sebelum memilih .   Ya. Untuk setiap , pilihan memenuhi definisi kekontinuan di .   Ambil sebarang dan pilih . Jika , maka Jadi syarat epsilon-delta terpenuhi dan kontinu di .  "
},
{
  "id": "o003-c90-ch06-exercise-task-02",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-a.html#o003-c90-ch06-exercise-task-02",
  "type": "Pemeriksaan",
  "number": "F.15",
  "title": "Diskontinuitas fungsi tanda di nol.",
  "body": "Diskontinuitas fungsi tanda di nol  Misalkan untuk dan , dengan metrik Euklides. Tentukan apakah kontinu di dan buktikan jawaban Anda. Rubrik: jika jawabannya negatif, nyatakan negasi definisi beserta satu saksi untuk setiap .   Ambil titik negatif yang berjarak kurang daripada dari , misalnya .   Tidak. Dengan , untuk setiap titik memenuhi , tetapi .   Tetapkan dan ambil sebarang . Pilih . Maka , sedangkan sehingga . Karena , Satu toleransi keluaran gagal pada setiap skala masukan. Menurut negasi definisi, tidak kontinu di .  "
},
{
  "id": "o003-c90-ch06-exercise-task-03",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-a.html#o003-c90-ch06-exercise-task-03",
  "type": "Pemeriksaan",
  "number": "F.16",
  "title": "Penjumlahan koordinat dengan metrik Euklides.",
  "body": "Penjumlahan koordinat dengan metrik Euklides  Dengan metrik Euklides pada dan , buktikan atau sangkal bahwa kontinu. Rubrik: bandingkan nilai mutlak selisih keluaran dengan jarak Euklides dua titik masukan.   Gunakan pertidaksamaan Cauchy pada vektor dan .   Fungsi tersebut kontinu, bahkan . Pilih .   Untuk dan , pertidaksamaan Cauchy memberikan Ambil sebarang dan , lalu pilih . Jika , batas di atas memberi . Jadi kontinu.  "
},
{
  "id": "o003-c90-ch06-exercise-task-04",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-a.html#o003-c90-ch06-exercise-task-04",
  "type": "Pemeriksaan",
  "number": "F.17",
  "title": "Penjumlahan koordinat dengan metrik maksimum.",
  "body": "Penjumlahan koordinat dengan metrik maksimum  Dengan metrik maksimum pada domain dan metrik Euklides pada kodomain , buktikan atau sangkal bahwa kontinu. Rubrik: turunkan batas yang berlaku bagi semua pasangan titik dan berikan pilihan .   Masing-masing selisih koordinat tidak melebihi jarak maksimum.   Fungsi tersebut kontinu, karena . Pilih .   Untuk dan , Ambil sebarang dan , serta pilih . Jika , maka . Jadi kontinu.  "
},
{
  "id": "o003-c90-ch06-exercise-task-05",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-a.html#o003-c90-ch06-exercise-task-05",
  "type": "Pemeriksaan",
  "number": "F.18",
  "title": "Semua fungsi dari ruang diskret.",
  "body": "Semua fungsi dari ruang diskret  Misalkan memakai metrik diskret dan sebarang ruang metrik. Tentukan semua fungsi kontinu . Rubrik: buktikan klasifikasi Anda langsung dari definisi; jangan mengasumsikan sifat khusus kodomain.   Jika , apa yang dapat disimpulkan tentang dan ?   Setiap fungsi kontinu ketika domain memakai metrik diskret.   Ambil fungsi sebarang , titik sebarang , dan . Pilih . Jika , definisi metrik diskret memaksa . Karena itu Jadi setiap fungsi kontinu di setiap titik domain. Tidak ada syarat tambahan pada atau pada metrik .  "
},
{
  "id": "o003-c90-ch06-exercise-task-06",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-a.html#o003-c90-ch06-exercise-task-06",
  "type": "Pemeriksaan",
  "number": "F.19",
  "title": "Kelipatan skalar fungsi kontinu.",
  "body": "Kelipatan skalar fungsi kontinu  Misalkan kontinu dan . Buktikan bahwa fungsi , yang didefinisikan oleh , kontinu. Rubrik: gunakan kekontinuan dengan toleransi keluaran yang disesuaikan oleh .   Karena , mintalah .   Fungsi kontinu. Untuk toleransi , pakai dalam definisi kekontinuan .   Ambil sebarang dan . Karena , bilangan positif. Kekontinuan di memberikan sedemikian sehingga mengakibatkan . Maka Jadi kontinu di setiap , sehingga kontinu pada .  "
},
{
  "id": "o003-c90-ch06-exercise-task-07",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-a.html#o003-c90-ch06-exercise-task-07",
  "type": "Pemeriksaan",
  "number": "F.20",
  "title": "Jumlah dua fungsi kontinu.",
  "body": "Jumlah dua fungsi kontinu  Misalkan kontinu. Buktikan bahwa , yang didefinisikan oleh , kontinu. Rubrik: alokasikan toleransi keluaran di antara dua suku dan gabungkan dua skala masukan.   Gunakan toleransi untuk masing-masing fungsi dan pilih nilai minimum dari dua yang dihasilkan.   Fungsi kontinu; jika dan bekerja untuk toleransi , pilih .   Ambil sebarang dan . Kekontinuan dan di memberikan sehingga, berturut-turut, mengakibatkan dan mengakibatkan .  Pilih . Jika , kedua batas berlaku dan Jadi kontinu.  "
},
{
  "id": "o003-c90-ch06-exercise-task-08",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-a.html#o003-c90-ch06-exercise-task-08",
  "type": "Pemeriksaan",
  "number": "F.21",
  "title": "Menguraikan selisih hasil kali.",
  "body": "Menguraikan selisih hasil kali  Untuk fungsi dan serta titik , buktikan identitas Rubrik: perluas kedua faktor setelah menambahkan dan mengurangkan nilai di , lalu sederhanakan seluruh suku.   Substitusikan dan ke dalam .   Identitas tersebut benar; ia diperoleh dengan memperluas hasil kali dua jumlah dan membatalkan suku .   Tuliskan dan . Maka Mengembalikan definisi dan menghasilkan tepat identitas yang diminta. Bentuk ini memisahkan dua suku linear dan satu suku hasil kali yang masing-masing dapat dikendalikan oleh kekontinuan dan .  "
},
{
  "id": "o003-c90-ch06-exercise-task-09",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-a.html#o003-c90-ch06-exercise-task-09",
  "type": "Pemeriksaan",
  "number": "F.22",
  "title": "Empat skala untuk bukti hasil kali.",
  "body": "Empat skala untuk bukti hasil kali  Misalkan dan kontinu di dan . Jelaskan mengapa ada yang masing-masing menjamin Rubrik: pasangkan setiap toleransi positif dengan fungsi yang sesuai.   Keempat ruas kanan positif. Terapkan definisi kekontinuan dua kali dan definisi kekontinuan dua kali.   Kekontinuan menghasilkan dan ; kekontinuan menghasilkan dan , dengan toleransi keluaran sesuai urutan yang ditampilkan.   Karena , semua bilangan , , dan positif. Kekontinuan di , berturut-turut dengan toleransi dan , memberikan dan . Kekontinuan di , berturut-turut dengan toleransi dan , memberikan dan . Masing-masing definisi tepat menghasilkan implikasi yang diminta ketika lebih kecil daripada terkait.  "
},
{
  "id": "o003-c90-ch06-exercise-task-10",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-a.html#o003-c90-ch06-exercise-task-10",
  "type": "Pemeriksaan",
  "number": "F.23",
  "title": "Hasil kali dua fungsi kontinu.",
  "body": "Hasil kali dua fungsi kontinu  Gunakan penguraian selisih dan empat skala pada dua butir sebelumnya untuk membuktikan bahwa kontinu di . Rubrik: pilih satu yang mengaktifkan keempat batas dan tunjukkan bahwa masing-masing dari tiga suku bernilai kurang daripada .   Pilih . Gunakan dan analoginya untuk .   Dengan sebagai minimum keempat skala, tiga suku dalam batas segitiga masing-masing kurang daripada ; karena itu .   Pilih . Jika , penguraian pada butir pertama dan pertidaksamaan segitiga memberikan Batas dari menjadikan suku pertama kurang daripada . Batas dari menjadikan suku kedua kurang daripada . Batas dari dan menjadikan suku ketiga kurang daripada . Jadi seluruh jumlah kurang daripada , sehingga kontinu di .  "
},
{
  "id": "o003-c90-ch06-exercise-task-11",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-a.html#o003-c90-ch06-exercise-task-11",
  "type": "Pemeriksaan",
  "number": "F.24",
  "title": "Kebalikan pernyataan tentang jumlah.",
  "body": "Kebalikan pernyataan tentang jumlah  Tentukan apakah kekontinuan memaksa dan masing-masing kontinu. Buktikan jawaban Anda. Rubrik: jika pernyataan salah, berikan fungsi konkret, periksa jumlahnya, dan buktikan diskontinuitas kedua suku yang diperlukan.   Ambil suatu fungsi tak kontinu , lalu pertimbangkan dan .   Tidak. Jika untuk dan untuk , maka dan tidak kontinu di , tetapi kontinu.   Definisikan dengan jika dan jika . Fungsi tidak kontinu di : untuk dan setiap , titik memenuhi , tetapi . Fungsi juga tidak kontinu di dengan argumen yang sama.  Ambil dan . Untuk setiap , , sehingga adalah fungsi konstan dan kontinu. Jadi kekontinuan jumlah tidak memaksa kekontinuan kedua sukunya.  "
},
{
  "id": "o003-c90-ch06-exercise-task-12",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-a.html#o003-c90-ch06-exercise-task-12",
  "type": "Pemeriksaan",
  "number": "F.25",
  "title": "Kebalikan pernyataan tentang hasil kali.",
  "body": "Kebalikan pernyataan tentang hasil kali  Tentukan apakah kekontinuan memaksa dan masing-masing kontinu. Buktikan jawaban Anda. Rubrik: berikan contoh tandingan konkret dan verifikasi baik hasil kali maupun diskontinuitas faktor-faktornya.   Carilah fungsi tak kontinu yang hanya bernilai dan , lalu kalikan fungsi itu dengan dirinya sendiri.   Tidak. Jika untuk dan untuk , maka tidak kontinu di , tetapi kontinu.   Definisikan dengan untuk dan untuk . Fungsi ini tidak kontinu di : tetapkan ; untuk setiap , titik memenuhi , tetapi .  Ambil . Kedua faktor tidak kontinu di , sedangkan untuk setiap , . Hasil kali tersebut adalah fungsi konstan, sehingga kontinu. Jadi pernyataannya salah.  "
},
{
  "id": "o003-c90-ch06-exercise-task-13",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-a.html#o003-c90-ch06-exercise-task-13",
  "type": "Pemeriksaan",
  "number": "F.26",
  "title": "Skala eksplisit untuk fungsi kuadrat.",
  "body": "Skala eksplisit untuk fungsi kuadrat  Misalkan . Untuk , carilah sedemikian sehingga mengakibatkan . Rubrik: berikan satu nilai sah dan buktikan batasnya secara aljabar.   Faktorkan . Jika , maka .   Salah satu pilihan yang sah adalah .   Pilih ; khususnya . Jika , maka . Oleh karena itu Jadi memenuhi implikasi yang diminta.  "
},
{
  "id": "o003-c90-ch06-exercise-guides-b",
  "level": "1",
  "url": "o003-c90-ch06-exercise-guides-b.html",
  "type": "Bagian",
  "number": "",
  "title": "Panduan latihan sumber, bagian kedua",
  "body": " Panduan latihan sumber, bagian kedua  Panduan ini mengikuti Tugas 14–26 pada latihan sumber secara berurutan. Kerjakan pernyataannya terlebih dahulu, lalu gunakan rubrik untuk menilai kelengkapan argumen Anda. Bukalah petunjuk, jawaban, dan solusi secara bertahap hanya setelah Anda mencoba tugas secara mandiri.  Tugas 14: kekontinuan fungsi kuadrat di titik  Misalkan didefinisikan oleh , dengan metrik Euklides pada domain dan kodomain. Buktikan bahwa kontinu di . Rubrik. Mulailah dengan sembarang , berikan pilihan yang hanya bergantung pada , dan turunkan pertidaksamaan yang diperlukan tanpa mengandaikan kesimpulan.    Langkah 1. Faktorkan .   Langkah 2. Jika , maka . Pilih yang sekaligus menjamin syarat ini dan membuat .   Fungsi kontinu di . Untuk , pilihan memenuhi definisi kekontinuan.   Ambil sembarang dan tetapkan . Andaikan . Karena , berlaku . Pertidaksamaan segitiga kemudian memberi .  Oleh karena itu, Jadi, untuk setiap toleransi positif telah ditemukan radius positif yang memenuhi implikasi definisi. Maka kontinu di .   Tugas 15: metrik yang dipangkas pada  Definisikan dengan . Buktikan bahwa merupakan metrik. Rubrik. Verifikasi keempat aksioma metrik. Untuk pertidaksamaan segitiga, jelaskan mengapa pemangkasan pada mempertahankan pertidaksamaan, bukan sekadar menyatakan bahwa hasilnya jelas.    Langkah 1. Ketaknegatifan, simetri, dan pemisahan titik diwarisi dari nilai mutlak.   Langkah 2. Untuk , buktikan dengan memisahkan kasus ketika salah satu dari sedikitnya dan ketika keduanya kurang dari .   Benar, merupakan metrik. Aksioma pertama hingga ketiga mengikuti sifat nilai mutlak, sedangkan pertidaksamaan segitiga mengikuti untuk .   Untuk setiap , kedua bilangan dan tak negatif, sehingga . Selanjutnya, tepat ketika , yakni tepat ketika . Simetri nilai mutlak juga memberi .  Tinggal membuktikan pertidaksamaan segitiga. Untuk bilangan tak negatif , berlaku Memang, jika atau , ruas kanan sedikitnya , sedangkan ruas kiri paling besar . Jika dan , ruas kanan sama dengan , yang tidak lebih kecil daripada ruas kiri.  Sekarang tetapkan dan . Dari dan sifat naik fungsi , diperoleh Keempat aksioma terpenuhi, jadi merupakan metrik pada .   Tugas 16: nilai pada himpunan rapat menentukan fungsi kontinu  Misalkan kontinu dalam metrik Euklides dan untuk setiap . Buktikan bahwa untuk setiap . Rubrik. Gunakan kerapatan secara kuantitatif di dalam lingkungan ; jangan mengandaikan hasil tentang limit barisan yang belum diperlukan.    Langkah 1. Tetapkan . Kekontinuan di menyediakan untuk setiap .   Langkah 2. Pilih dengan . Kemudian bandingkan dengan .   Untuk setiap dan setiap , kekontinuan dan kerapatan memberi . Karena ini berlaku untuk setiap toleransi positif, . Jadi identik nol.   Ambil sembarang . Untuk membuktikan , tetapkan sembarang . Karena kontinu di , ada sedemikian sehingga mengakibatkan .  Kerapatan bilangan rasional dalam bilangan real memberi dengan . Oleh hipotesis, , sehingga Jika positif, kita dapat memilih dan memperoleh kontradiksi. Jadi . Karena dipilih sembarang, kesimpulan ini berlaku pada seluruh .   Tugas 17: fungsi Dirichlet tidak kontinu di mana pun  Definisikan dengan untuk irasional dan untuk rasional. Dengan metrik Euklides pada domain dan kodomain, tunjukkan bahwa tidak kontinu di titik mana pun. Rubrik. Untuk setiap titik pusat, berikan satu toleransi tetap yang menggagalkan setiap pilihan , dan gunakan kerapatan bilangan rasional serta irasional dengan urutan kuantor yang benar.    Langkah 1. Tetapkan dan pilih .   Langkah 2. Di setiap interval terbuka di sekitar terdapat titik yang jenisnya—rasional atau irasional—berlawanan dengan jenis .   Fungsi tidak kontinu di setiap . Untuk dan setiap , ada dengan tetapi .   Tetapkan sembarang dan ambil . Misalkan diberikan. Jika rasional, kerapatan bilangan irasional memberi titik irasional dengan . Maka , , dan .  Jika irasional, kerapatan bilangan rasional memberi titik rasional dengan . Kini , , dan kembali . Jadi, pada kedua kasus, toleransi menggagalkan setiap radius positif. Ini tepat merupakan negasi definisi kekontinuan di . Karena sembarang, tidak kontinu di mana pun.   Tugas 18: fungsi yang kontinu hanya di titik asal  Definisikan dengan jika irasional dan jika rasional. Dengan metrik Euklides pada domain dan kodomain, buktikan bahwa kontinu tepat di . Rubrik. Berikan pembuktian langsung epsilon-delta di , lalu gunakan negasi definisi dan kerapatan untuk setiap titik tak nol.    Langkah 1. Untuk semua , berlaku .   Langkah 2. Jika , ambil . Pilih titik yang jenis rasionalitasnya berlawanan dengan dan juga cukup dekat agar nilai mutlaknya lebih besar daripada bila diperlukan.   Di , pilihan bekerja karena . Pada setiap , toleransi digagalkan oleh titik-titik rasional atau irasional yang sedekat apa pun dengan . Jadi himpunan titik kekontinuan adalah .   Karena rasional, . Ambil dan pilih . Jika , maka untuk irasional berlaku , sedangkan untuk rasional berlaku . Jadi kontinu di .  Sekarang tetapkan dan ambil . Jika rasional, maka . Untuk setiap , pilih titik irasional dengan . Karena , diperoleh .  Jika irasional, maka . Untuk radius , kerapatan bilangan rasional memungkinkan kita memilih dengan . Pertidaksamaan segitiga terbalik memberi . Jadi . Dalam kedua kasus, negasi kekontinuan terpenuhi di . Dengan demikian hanya merupakan titik kekontinuan .   Tugas 19: menghitung jarak integral  Pada , gunakan . Hitung untuk dan . Rubrik. Temukan semua titik tempat selisih berubah tanda, pecah integral mutlak pada titik-titik tersebut, dan berikan nilai eksak.    Langkah 1. Faktorkan .   Langkah 2. Ekspresi itu tidak positif pada dan tidak negatif pada .   Nilainya adalah .   Selisih kedua fungsi adalah . Pada interval , berlaku , sedangkan pada , berlaku . Dengan antiturunan , kita peroleh   Nilai-nilainya adalah , , dan . Jadi setiap integral bertanda positif bernilai , dan    Tugas 20: nilai fungsional integral  Untuk , hitung ketika dan . Rubrik. Tampilkan antiturunan dan evaluasi pada kedua ujung interval.   Suatu antiturunan adalah .    .   Berdasarkan Teorema Dasar Kalkulus,    Tugas 21: kekontinuan fungsional integral  Misalkan , , , dan . Buktikan bahwa kontinu. Rubrik. Tuliskan definisi kekontinuan dalam kedua metrik, gunakan pertidaksamaan nilai mutlak integral, dan berikan pilihan yang eksplisit.    Langkah 1. Untuk , tuliskan .   Langkah 2. Gunakan ; fungsi bahkan memenuhi pertidaksamaan Lipschitz dengan konstanta .   Untuk semua , berlaku . Karena itu pilihan membuktikan bahwa kontinu di setiap .   Tetapkan sembarang dan . Ambil . Jika memenuhi , maka sifat linear integral dan pertidaksamaan nilai mutlak memberi Jadi kontinu di . Karena sembarang, kontinu pada seluruh . Pertidaksamaan yang sama juga menunjukkan bahwa bersifat 1-Lipschitz.   Tugas 22: domain bermetrik diskret  Putuskan benar atau salah: jika suatu fungsi, metrik diskret, dan sebarang metrik, maka kontinu. Rubrik. Jika benar, berikan pembuktian epsilon-delta yang berlaku untuk sebarang fungsi dan sebarang titik tanpa memakai sifat khusus kodomain.   Pada metrik diskret, memaksa .   Benar. Untuk setiap titik dan setiap , pilih . Syarat memaksa , sehingga jarak keluarannya nol.   Tetapkan dan . Ambil . Karena diskret, nilainya hanya atau . Maka mengakibatkan , sehingga . Akibatnya . Jadi kontinu di setiap , apa pun fungsi dan metrik .   Tugas 23: kodomain bermetrik diskret  Putuskan benar atau salah: jika suatu fungsi, metrik diskret, dan sebarang metrik, maka kontinu. Rubrik. Jika salah, tentukan domain, kodomain, fungsi, titik, dan satu toleransi yang menggagalkan setiap radius positif.   Gunakan fungsi identitas dari bermetrik Euklides menuju bermetrik diskret dan ambil .   Salah. Fungsi identitas tidak kontinu di titik mana pun, dengan metrik diskret.   Ambil , gunakan metrik Euklides pada domain dan metrik diskret pada kodomain, lalu definisikan . Tetapkan sembarang dan ambil . Untuk setiap , pilih . Maka , tetapi , sehingga . Jadi tidak kontinu di . Contoh ini membantah pernyataan universal.   Tugas 24: identitas di antara dua metrik  Putuskan benar atau salah: untuk sebarang dua metrik dan pada himpunan , fungsi identitas selalu kontinu. Rubrik. Jika salah, berikan dua metrik konkret pada himpunan yang sama dan tunjukkan kegagalan definisi kekontinuan.   Pilih , , dan , dengan metrik diskret.   Salah. Identitas tidak kontinu, sebab titik-titik yang berbeda dapat sedekat apa pun dalam tetapi selalu berjarak dalam .   Pada , ambil dan metrik diskret . Tetapkan dan . Apa pun , titik memenuhi . Namun , sehingga . Jadi identitas ini tidak kontinu. Kekontinuan identitas bergantung pada hubungan antara kedua metrik, bukan hanya pada fakta bahwa keduanya didefinisikan pada himpunan yang sama.   Tugas 25: jumlah fungsi pada domain bermetrik taksi  Misalkan kontinu. Buktikan bahwa fungsi , yang didefinisikan oleh , juga kontinu. Rubrik. Buktikan kekontinuan di titik sembarang, bagikan toleransi keluaran di antara kedua fungsi, dan gabungkan radius dengan minimum.    Langkah 1. Untuk toleransi , terapkan kekontinuan dan masing-masing dengan toleransi .   Langkah 2. Ambil dan gunakan pertidaksamaan segitiga dalam .   Benar. Kekontinuan kedua fungsi dengan toleransi menghasilkan radius ; radius minimumnya membuat selisih nilai kurang dari .   Tetapkan dan . Karena kontinu di , terdapat sedemikian sehingga mengakibatkan . Demikian pula, terdapat sedemikian sehingga mengakibatkan .  Ambil . Jika , kedua taksiran di atas berlaku, sehingga Jadi kontinu di , dan karena sembarang, fungsi itu kontinu pada seluruh .   Tugas 26: fungsi konstan di antara ruang metrik  Misalkan dan ruang-ruang metrik serta . Buktikan bahwa fungsi konstan yang didefinisikan oleh untuk setiap kontinu. Rubrik. Berikan pembuktian epsilon-delta yang berlaku sekalipun domain kosong atau tidak terbatas dan jangan memberlakukan syarat yang tidak diperlukan pada metrik.   Jarak antara dua keluaran fungsi konstan selalu nol. Bila perlu pilih radius tetap, misalnya .   Fungsi konstan selalu kontinu. Untuk setiap titik domain dan setiap , pilihan bekerja karena .   Jika kosong, pernyataan bahwa kontinu di setiap titik domain benar secara hampa. Jika tidak kosong, tetapkan sembarang dan . Pilih . Untuk setiap yang memenuhi , kita mempunyai Dengan demikian kontinu di setiap titik , sehingga kontinu.   "
},
{
  "id": "o003-c90-ch06-exercise-task-14",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-b.html#o003-c90-ch06-exercise-task-14",
  "type": "Pemeriksaan",
  "number": "F.27",
  "title": "Tugas 14: kekontinuan fungsi kuadrat di titik <span class=\"process-math\">\\(1\\)<\/span>.",
  "body": "Tugas 14: kekontinuan fungsi kuadrat di titik  Misalkan didefinisikan oleh , dengan metrik Euklides pada domain dan kodomain. Buktikan bahwa kontinu di . Rubrik. Mulailah dengan sembarang , berikan pilihan yang hanya bergantung pada , dan turunkan pertidaksamaan yang diperlukan tanpa mengandaikan kesimpulan.    Langkah 1. Faktorkan .   Langkah 2. Jika , maka . Pilih yang sekaligus menjamin syarat ini dan membuat .   Fungsi kontinu di . Untuk , pilihan memenuhi definisi kekontinuan.   Ambil sembarang dan tetapkan . Andaikan . Karena , berlaku . Pertidaksamaan segitiga kemudian memberi .  Oleh karena itu, Jadi, untuk setiap toleransi positif telah ditemukan radius positif yang memenuhi implikasi definisi. Maka kontinu di .  "
},
{
  "id": "o003-c90-ch06-exercise-task-15",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-b.html#o003-c90-ch06-exercise-task-15",
  "type": "Pemeriksaan",
  "number": "F.28",
  "title": "Tugas 15: metrik yang dipangkas pada <span class=\"process-math\">\\(1\\)<\/span>.",
  "body": "Tugas 15: metrik yang dipangkas pada  Definisikan dengan . Buktikan bahwa merupakan metrik. Rubrik. Verifikasi keempat aksioma metrik. Untuk pertidaksamaan segitiga, jelaskan mengapa pemangkasan pada mempertahankan pertidaksamaan, bukan sekadar menyatakan bahwa hasilnya jelas.    Langkah 1. Ketaknegatifan, simetri, dan pemisahan titik diwarisi dari nilai mutlak.   Langkah 2. Untuk , buktikan dengan memisahkan kasus ketika salah satu dari sedikitnya dan ketika keduanya kurang dari .   Benar, merupakan metrik. Aksioma pertama hingga ketiga mengikuti sifat nilai mutlak, sedangkan pertidaksamaan segitiga mengikuti untuk .   Untuk setiap , kedua bilangan dan tak negatif, sehingga . Selanjutnya, tepat ketika , yakni tepat ketika . Simetri nilai mutlak juga memberi .  Tinggal membuktikan pertidaksamaan segitiga. Untuk bilangan tak negatif , berlaku Memang, jika atau , ruas kanan sedikitnya , sedangkan ruas kiri paling besar . Jika dan , ruas kanan sama dengan , yang tidak lebih kecil daripada ruas kiri.  Sekarang tetapkan dan . Dari dan sifat naik fungsi , diperoleh Keempat aksioma terpenuhi, jadi merupakan metrik pada .  "
},
{
  "id": "o003-c90-ch06-exercise-task-16",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-b.html#o003-c90-ch06-exercise-task-16",
  "type": "Pemeriksaan",
  "number": "F.29",
  "title": "Tugas 16: nilai pada himpunan rapat menentukan fungsi kontinu.",
  "body": "Tugas 16: nilai pada himpunan rapat menentukan fungsi kontinu  Misalkan kontinu dalam metrik Euklides dan untuk setiap . Buktikan bahwa untuk setiap . Rubrik. Gunakan kerapatan secara kuantitatif di dalam lingkungan ; jangan mengandaikan hasil tentang limit barisan yang belum diperlukan.    Langkah 1. Tetapkan . Kekontinuan di menyediakan untuk setiap .   Langkah 2. Pilih dengan . Kemudian bandingkan dengan .   Untuk setiap dan setiap , kekontinuan dan kerapatan memberi . Karena ini berlaku untuk setiap toleransi positif, . Jadi identik nol.   Ambil sembarang . Untuk membuktikan , tetapkan sembarang . Karena kontinu di , ada sedemikian sehingga mengakibatkan .  Kerapatan bilangan rasional dalam bilangan real memberi dengan . Oleh hipotesis, , sehingga Jika positif, kita dapat memilih dan memperoleh kontradiksi. Jadi . Karena dipilih sembarang, kesimpulan ini berlaku pada seluruh .  "
},
{
  "id": "o003-c90-ch06-exercise-task-17",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-b.html#o003-c90-ch06-exercise-task-17",
  "type": "Pemeriksaan",
  "number": "F.30",
  "title": "Tugas 17: fungsi Dirichlet tidak kontinu di mana pun.",
  "body": "Tugas 17: fungsi Dirichlet tidak kontinu di mana pun  Definisikan dengan untuk irasional dan untuk rasional. Dengan metrik Euklides pada domain dan kodomain, tunjukkan bahwa tidak kontinu di titik mana pun. Rubrik. Untuk setiap titik pusat, berikan satu toleransi tetap yang menggagalkan setiap pilihan , dan gunakan kerapatan bilangan rasional serta irasional dengan urutan kuantor yang benar.    Langkah 1. Tetapkan dan pilih .   Langkah 2. Di setiap interval terbuka di sekitar terdapat titik yang jenisnya—rasional atau irasional—berlawanan dengan jenis .   Fungsi tidak kontinu di setiap . Untuk dan setiap , ada dengan tetapi .   Tetapkan sembarang dan ambil . Misalkan diberikan. Jika rasional, kerapatan bilangan irasional memberi titik irasional dengan . Maka , , dan .  Jika irasional, kerapatan bilangan rasional memberi titik rasional dengan . Kini , , dan kembali . Jadi, pada kedua kasus, toleransi menggagalkan setiap radius positif. Ini tepat merupakan negasi definisi kekontinuan di . Karena sembarang, tidak kontinu di mana pun.  "
},
{
  "id": "o003-c90-ch06-exercise-task-18",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-b.html#o003-c90-ch06-exercise-task-18",
  "type": "Pemeriksaan",
  "number": "F.31",
  "title": "Tugas 18: fungsi yang kontinu hanya di titik asal.",
  "body": "Tugas 18: fungsi yang kontinu hanya di titik asal  Definisikan dengan jika irasional dan jika rasional. Dengan metrik Euklides pada domain dan kodomain, buktikan bahwa kontinu tepat di . Rubrik. Berikan pembuktian langsung epsilon-delta di , lalu gunakan negasi definisi dan kerapatan untuk setiap titik tak nol.    Langkah 1. Untuk semua , berlaku .   Langkah 2. Jika , ambil . Pilih titik yang jenis rasionalitasnya berlawanan dengan dan juga cukup dekat agar nilai mutlaknya lebih besar daripada bila diperlukan.   Di , pilihan bekerja karena . Pada setiap , toleransi digagalkan oleh titik-titik rasional atau irasional yang sedekat apa pun dengan . Jadi himpunan titik kekontinuan adalah .   Karena rasional, . Ambil dan pilih . Jika , maka untuk irasional berlaku , sedangkan untuk rasional berlaku . Jadi kontinu di .  Sekarang tetapkan dan ambil . Jika rasional, maka . Untuk setiap , pilih titik irasional dengan . Karena , diperoleh .  Jika irasional, maka . Untuk radius , kerapatan bilangan rasional memungkinkan kita memilih dengan . Pertidaksamaan segitiga terbalik memberi . Jadi . Dalam kedua kasus, negasi kekontinuan terpenuhi di . Dengan demikian hanya merupakan titik kekontinuan .  "
},
{
  "id": "o003-c90-ch06-exercise-task-19",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-b.html#o003-c90-ch06-exercise-task-19",
  "type": "Pemeriksaan",
  "number": "F.32",
  "title": "Tugas 19: menghitung jarak integral.",
  "body": "Tugas 19: menghitung jarak integral  Pada , gunakan . Hitung untuk dan . Rubrik. Temukan semua titik tempat selisih berubah tanda, pecah integral mutlak pada titik-titik tersebut, dan berikan nilai eksak.    Langkah 1. Faktorkan .   Langkah 2. Ekspresi itu tidak positif pada dan tidak negatif pada .   Nilainya adalah .   Selisih kedua fungsi adalah . Pada interval , berlaku , sedangkan pada , berlaku . Dengan antiturunan , kita peroleh   Nilai-nilainya adalah , , dan . Jadi setiap integral bertanda positif bernilai , dan   "
},
{
  "id": "o003-c90-ch06-exercise-task-20",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-b.html#o003-c90-ch06-exercise-task-20",
  "type": "Pemeriksaan",
  "number": "F.33",
  "title": "Tugas 20: nilai fungsional integral.",
  "body": "Tugas 20: nilai fungsional integral  Untuk , hitung ketika dan . Rubrik. Tampilkan antiturunan dan evaluasi pada kedua ujung interval.   Suatu antiturunan adalah .    .   Berdasarkan Teorema Dasar Kalkulus,   "
},
{
  "id": "o003-c90-ch06-exercise-task-21",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-b.html#o003-c90-ch06-exercise-task-21",
  "type": "Pemeriksaan",
  "number": "F.34",
  "title": "Tugas 21: kekontinuan fungsional integral.",
  "body": "Tugas 21: kekontinuan fungsional integral  Misalkan , , , dan . Buktikan bahwa kontinu. Rubrik. Tuliskan definisi kekontinuan dalam kedua metrik, gunakan pertidaksamaan nilai mutlak integral, dan berikan pilihan yang eksplisit.    Langkah 1. Untuk , tuliskan .   Langkah 2. Gunakan ; fungsi bahkan memenuhi pertidaksamaan Lipschitz dengan konstanta .   Untuk semua , berlaku . Karena itu pilihan membuktikan bahwa kontinu di setiap .   Tetapkan sembarang dan . Ambil . Jika memenuhi , maka sifat linear integral dan pertidaksamaan nilai mutlak memberi Jadi kontinu di . Karena sembarang, kontinu pada seluruh . Pertidaksamaan yang sama juga menunjukkan bahwa bersifat 1-Lipschitz.  "
},
{
  "id": "o003-c90-ch06-exercise-task-22",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-b.html#o003-c90-ch06-exercise-task-22",
  "type": "Pemeriksaan",
  "number": "F.35",
  "title": "Tugas 22: domain bermetrik diskret.",
  "body": "Tugas 22: domain bermetrik diskret  Putuskan benar atau salah: jika suatu fungsi, metrik diskret, dan sebarang metrik, maka kontinu. Rubrik. Jika benar, berikan pembuktian epsilon-delta yang berlaku untuk sebarang fungsi dan sebarang titik tanpa memakai sifat khusus kodomain.   Pada metrik diskret, memaksa .   Benar. Untuk setiap titik dan setiap , pilih . Syarat memaksa , sehingga jarak keluarannya nol.   Tetapkan dan . Ambil . Karena diskret, nilainya hanya atau . Maka mengakibatkan , sehingga . Akibatnya . Jadi kontinu di setiap , apa pun fungsi dan metrik .  "
},
{
  "id": "o003-c90-ch06-exercise-task-23",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-b.html#o003-c90-ch06-exercise-task-23",
  "type": "Pemeriksaan",
  "number": "F.36",
  "title": "Tugas 23: kodomain bermetrik diskret.",
  "body": "Tugas 23: kodomain bermetrik diskret  Putuskan benar atau salah: jika suatu fungsi, metrik diskret, dan sebarang metrik, maka kontinu. Rubrik. Jika salah, tentukan domain, kodomain, fungsi, titik, dan satu toleransi yang menggagalkan setiap radius positif.   Gunakan fungsi identitas dari bermetrik Euklides menuju bermetrik diskret dan ambil .   Salah. Fungsi identitas tidak kontinu di titik mana pun, dengan metrik diskret.   Ambil , gunakan metrik Euklides pada domain dan metrik diskret pada kodomain, lalu definisikan . Tetapkan sembarang dan ambil . Untuk setiap , pilih . Maka , tetapi , sehingga . Jadi tidak kontinu di . Contoh ini membantah pernyataan universal.  "
},
{
  "id": "o003-c90-ch06-exercise-task-24",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-b.html#o003-c90-ch06-exercise-task-24",
  "type": "Pemeriksaan",
  "number": "F.37",
  "title": "Tugas 24: identitas di antara dua metrik.",
  "body": "Tugas 24: identitas di antara dua metrik  Putuskan benar atau salah: untuk sebarang dua metrik dan pada himpunan , fungsi identitas selalu kontinu. Rubrik. Jika salah, berikan dua metrik konkret pada himpunan yang sama dan tunjukkan kegagalan definisi kekontinuan.   Pilih , , dan , dengan metrik diskret.   Salah. Identitas tidak kontinu, sebab titik-titik yang berbeda dapat sedekat apa pun dalam tetapi selalu berjarak dalam .   Pada , ambil dan metrik diskret . Tetapkan dan . Apa pun , titik memenuhi . Namun , sehingga . Jadi identitas ini tidak kontinu. Kekontinuan identitas bergantung pada hubungan antara kedua metrik, bukan hanya pada fakta bahwa keduanya didefinisikan pada himpunan yang sama.  "
},
{
  "id": "o003-c90-ch06-exercise-task-25",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-b.html#o003-c90-ch06-exercise-task-25",
  "type": "Pemeriksaan",
  "number": "F.38",
  "title": "Tugas 25: jumlah fungsi pada domain bermetrik taksi.",
  "body": "Tugas 25: jumlah fungsi pada domain bermetrik taksi  Misalkan kontinu. Buktikan bahwa fungsi , yang didefinisikan oleh , juga kontinu. Rubrik. Buktikan kekontinuan di titik sembarang, bagikan toleransi keluaran di antara kedua fungsi, dan gabungkan radius dengan minimum.    Langkah 1. Untuk toleransi , terapkan kekontinuan dan masing-masing dengan toleransi .   Langkah 2. Ambil dan gunakan pertidaksamaan segitiga dalam .   Benar. Kekontinuan kedua fungsi dengan toleransi menghasilkan radius ; radius minimumnya membuat selisih nilai kurang dari .   Tetapkan dan . Karena kontinu di , terdapat sedemikian sehingga mengakibatkan . Demikian pula, terdapat sedemikian sehingga mengakibatkan .  Ambil . Jika , kedua taksiran di atas berlaku, sehingga Jadi kontinu di , dan karena sembarang, fungsi itu kontinu pada seluruh .  "
},
{
  "id": "o003-c90-ch06-exercise-task-26",
  "level": "2",
  "url": "o003-c90-ch06-exercise-guides-b.html#o003-c90-ch06-exercise-task-26",
  "type": "Pemeriksaan",
  "number": "F.39",
  "title": "Tugas 26: fungsi konstan di antara ruang metrik.",
  "body": "Tugas 26: fungsi konstan di antara ruang metrik  Misalkan dan ruang-ruang metrik serta . Buktikan bahwa fungsi konstan yang didefinisikan oleh untuk setiap kontinu. Rubrik. Berikan pembuktian epsilon-delta yang berlaku sekalipun domain kosong atau tidak terbatas dan jangan memberlakukan syarat yang tidak diperlukan pada metrik.   Jarak antara dua keluaran fungsi konstan selalu nol. Bila perlu pilih radius tetap, misalnya .   Fungsi konstan selalu kontinu. Untuk setiap titik domain dan setiap , pilihan bekerja karena .   Jika kosong, pernyataan bahwa kontinu di setiap titik domain benar secara hampa. Jika tidak kosong, tetapkan sembarang dan . Pilih . Untuk setiap yang memenuhi , kita mempunyai Dengan demikian kontinu di setiap titik , sehingga kontinu.  "
},
{
  "id": "o003-c90-ch06-mastery",
  "level": "1",
  "url": "o003-c90-ch06-mastery.html",
  "type": "Bagian",
  "number": "",
  "title": "Pemeriksaan penguasaan dan transfer",
  "body": " Pemeriksaan penguasaan dan transfer  Enam latihan asli berikut menguji penguasaan definisi epsilon-delta, kekontinuan di antara ruang metrik, serta operasi pada fungsi kontinu. Kerjakan setiap pernyataan sebelum membuka petunjuk. Gunakan rubrik untuk memeriksa urutan kuantor, ketepatan pilihan radius, dan kelengkapan contoh tandingan Anda.  Definisi kekontinuan dan negasinya  Misalkan dan ruang-ruang metrik, , dan .   Tuliskan definisi lengkap bahwa kontinu di dengan semua kuantornya.    Negasikan definisi tersebut untuk memperoleh pernyataan lengkap bahwa tidak kontinu di .      Rubrik. Urutan , , dan harus tepat; pada negasi, balik setiap kuantor dan negasikan implikasi menjadi dua syarat serentak. Nyatakan dengan tegas variabel mana yang boleh bergantung pada variabel sebelumnya.    Langkah 1. Kekontinuan dimulai dengan “untuk setiap ” dan baru sesudah itu memilih .   Langkah 2. Negasi pernyataan adalah dan bukan .   Langkah 3. Negasi adalah .   Kekontinuan di berarti Ketidakkontinuan di berarti    Fungsi kontinu di jika Dengan urutan ini, boleh bergantung pada dan titik tetap , tetapi tidak boleh dipilih sesudah melihat . Titik harus memenuhi implikasi yang sama untuk semua titik di dalam bola .  Untuk menegasikan pernyataan tersebut, kuantor universal menjadi eksistensial dan sebaliknya. Selain itu, gagal tepat ketika benar dan salah. Jadi tidak kontinu di tepat ketika Di sini satu toleransi keluaran dipilih lebih dahulu dan harus menggagalkan setiap radius masukan, meskipun titik saksi boleh bergantung pada radius tersebut.   Pemetaan Lipschitz bersifat kontinu  Misalkan dan ruang-ruang metrik. Andaikan dan terdapat konstanta sedemikian sehingga untuk semua . Buktikan langsung dari definisi bahwa kontinu.   Rubrik. Tetapkan titik dan toleransi sembarang, berikan pilihan yang eksplisit, dan tunjukkan rantai pertidaksamaan lengkap. Jangan hanya menyebut teorema tentang fungsi Lipschitz.    Langkah 1. Untuk membuat , cukup minta .   Langkah 2. Pilihan radius yang sama bekerja di setiap titik .   Untuk setiap dan , ambil . Jika , maka . Jadi kontinu.   Tetapkan sembarang dan . Karena , bilangan positif. Jika memenuhi , hipotesis Lipschitz memberi Maka kontinu di . Karena dipilih sembarang, kontinu pada . Bahkan radius tersebut tidak bergantung pada titik pusat; hipotesis memberi kendali yang lebih kuat daripada kekontinuan biasa.   Metrik Euklides, metrik pangkas, dan metrik diskret  Pada , definisikan , , dan metrik diskret jika serta jika . Selidiki kekontinuan keempat fungsi identitas berikut:   ;    ;    ;    .      Rubrik. Untuk setiap fungsi yang kontinu, berikan pilihan radius. Untuk fungsi yang tidak kontinu, berikan satu toleransi dan saksi untuk setiap radius. Jelaskan apa yang ditunjukkan dua arah pertama tentang pengaruh pemangkasan jarak besar.    Langkah 1. Selalu berlaku . Sebaliknya, jika , maka .   Langkah 2. Bola diskret berjari-jari hanya memuat pusatnya.   Langkah 3. Untuk menggagalkan , pilih pada kodomain diskret dan titik berbeda yang sedekat apa pun dalam .   Fungsi , , dan kontinu, sedangkan tidak kontinu di titik mana pun. Jadi metrik Euklides dan metrik pangkas mempunyai perilaku kekontinuan lokal yang sama, tetapi metrik diskret pada kodomain menuntut pemisahan yang lebih kuat.   Untuk , tetapkan dan , lalu pilih . Jika , maka . Jadi kontinu.  Untuk , pilih . Jika , nilai minimum tidak mungkin berasal dari cabang . Maka . Jadi juga kontinu. Kedua hasil ini menunjukkan bahwa pemangkasan semua jarak besar pada tidak mengubah perilaku lokal yang dideteksi oleh kekontinuan.  Untuk , ambil untuk setiap toleransi positif. Syarat memaksa , sehingga jarak keluarannya nol. Jadi kontinu.  Sebaliknya, tetapkan dan untuk . Untuk setiap , ambil dan . Maka , tetapi , sehingga . Dengan demikian tidak kontinu di , dan sembarang.   Jumlah dua fungsi kontinu pada ruang metrik  Misalkan ruang metrik, , dan kontinu di , dengan metrik Euklides pada . Buktikan langsung bahwa kontinu di .   Rubrik. Jangan mengandaikan radius yang sama tersedia untuk kedua fungsi. Bagikan toleransi, peroleh dua radius, ambil minimumnya, dan gunakan pertidaksamaan segitiga.    Langkah 1. Terapkan kekontinuan dan masing-masing dengan toleransi .   Langkah 2. Gunakan .   Jika dan bekerja untuk toleransi , maka bekerja untuk dan toleransi .   Ambil sembarang . Kekontinuan di memberi sedemikian sehingga mengakibatkan . Kekontinuan memberi dengan implikasi serupa untuk .  Pilih . Jika , kedua taksiran berlaku dan Ini membuktikan bahwa kontinu di .   Komposisi fungsi kontinu  Misalkan , , dan ruang-ruang metrik. Jika kontinu di dan kontinu di , buktikan bahwa kontinu di .   Rubrik. Mulailah dari toleransi di . Radius yang dihasilkan oleh kekontinuan harus dipakai sebagai toleransi keluaran ketika menerapkan kekontinuan .    Langkah 1. Untuk , kekontinuan di memberi suatu pada ruang .   Langkah 2. Terapkan kekontinuan di dengan toleransi untuk memperoleh pada ruang .   Pilih dari kekontinuan untuk toleransi , lalu pilih dari kekontinuan untuk toleransi . Rantai kedua implikasi membuktikan kekontinuan di .   Tetapkan . Karena kontinu di , ada sedemikian sehingga Karena kontinu di , untuk toleransi ini ada sedemikian sehingga   Jadi, jika , implikasi kedua menempatkan di dalam bola berjari-jari di sekitar . Dengan mengambil pada implikasi pertama, diperoleh Maka kontinu di .   Contoh tandingan bagi kebalikan aturan jumlah  Bangun dua fungsi yang masing-masing tidak kontinu di titik mana pun, tetapi jumlah kontinu di setiap titik. Buktikan kedua klaim menggunakan metrik Euklides.   Rubrik. Berikan rumus eksplisit bagi kedua fungsi. Untuk ketidakkontinuan, gunakan satu toleransi tetap dan kerapatan bilangan rasional serta irasional. Untuk kekontinuan jumlah, hitung jumlahnya tepat, bukan hanya menyatakan bahwa diskontinuitas “saling meniadakan.”    Langkah 1. Definisikan pada bilangan rasional dan pada bilangan irasional.   Langkah 2. Ambil dan . Gunakan untuk membuktikan ketidakkontinuan masing-masing.   Ambil dan , dengan . Fungsi dan tidak kontinu di titik mana pun, tetapi untuk semua , sehingga jumlahnya kontinu.   Definisikan Ambil dan . Tetapkan sembarang dan . Jika rasional, setiap lingkungan di sekitar memuat titik irasional , dan . Jika irasional, setiap lingkungan memuat titik rasional , dan kembali . Jadi tidak kontinu di . Karena , argumen yang sama membuktikan bahwa juga tidak kontinu di . Titik sembarang, sehingga keduanya tidak kontinu di mana pun.  Namun, untuk setiap , Jadi adalah fungsi konstan nol dan kontinu di setiap titik. Contoh ini menunjukkan bahwa kekontinuan jumlah tidak memaksa kekontinuan masing-masing suku.   "
},
{
  "id": "o003-c90-ch06-mastery-01",
  "level": "2",
  "url": "o003-c90-ch06-mastery.html#o003-c90-ch06-mastery-01",
  "type": "Pemeriksaan",
  "number": "F.40",
  "title": "Definisi kekontinuan dan negasinya.",
  "body": "Definisi kekontinuan dan negasinya  Misalkan dan ruang-ruang metrik, , dan .   Tuliskan definisi lengkap bahwa kontinu di dengan semua kuantornya.    Negasikan definisi tersebut untuk memperoleh pernyataan lengkap bahwa tidak kontinu di .      Rubrik. Urutan , , dan harus tepat; pada negasi, balik setiap kuantor dan negasikan implikasi menjadi dua syarat serentak. Nyatakan dengan tegas variabel mana yang boleh bergantung pada variabel sebelumnya.    Langkah 1. Kekontinuan dimulai dengan “untuk setiap ” dan baru sesudah itu memilih .   Langkah 2. Negasi pernyataan adalah dan bukan .   Langkah 3. Negasi adalah .   Kekontinuan di berarti Ketidakkontinuan di berarti    Fungsi kontinu di jika Dengan urutan ini, boleh bergantung pada dan titik tetap , tetapi tidak boleh dipilih sesudah melihat . Titik harus memenuhi implikasi yang sama untuk semua titik di dalam bola .  Untuk menegasikan pernyataan tersebut, kuantor universal menjadi eksistensial dan sebaliknya. Selain itu, gagal tepat ketika benar dan salah. Jadi tidak kontinu di tepat ketika Di sini satu toleransi keluaran dipilih lebih dahulu dan harus menggagalkan setiap radius masukan, meskipun titik saksi boleh bergantung pada radius tersebut.  "
},
{
  "id": "o003-c90-ch06-mastery-02",
  "level": "2",
  "url": "o003-c90-ch06-mastery.html#o003-c90-ch06-mastery-02",
  "type": "Pemeriksaan",
  "number": "F.41",
  "title": "Pemetaan Lipschitz bersifat kontinu.",
  "body": "Pemetaan Lipschitz bersifat kontinu  Misalkan dan ruang-ruang metrik. Andaikan dan terdapat konstanta sedemikian sehingga untuk semua . Buktikan langsung dari definisi bahwa kontinu.   Rubrik. Tetapkan titik dan toleransi sembarang, berikan pilihan yang eksplisit, dan tunjukkan rantai pertidaksamaan lengkap. Jangan hanya menyebut teorema tentang fungsi Lipschitz.    Langkah 1. Untuk membuat , cukup minta .   Langkah 2. Pilihan radius yang sama bekerja di setiap titik .   Untuk setiap dan , ambil . Jika , maka . Jadi kontinu.   Tetapkan sembarang dan . Karena , bilangan positif. Jika memenuhi , hipotesis Lipschitz memberi Maka kontinu di . Karena dipilih sembarang, kontinu pada . Bahkan radius tersebut tidak bergantung pada titik pusat; hipotesis memberi kendali yang lebih kuat daripada kekontinuan biasa.  "
},
{
  "id": "o003-c90-ch06-mastery-03",
  "level": "2",
  "url": "o003-c90-ch06-mastery.html#o003-c90-ch06-mastery-03",
  "type": "Pemeriksaan",
  "number": "F.42",
  "title": "Metrik Euklides, metrik pangkas, dan metrik diskret.",
  "body": "Metrik Euklides, metrik pangkas, dan metrik diskret  Pada , definisikan , , dan metrik diskret jika serta jika . Selidiki kekontinuan keempat fungsi identitas berikut:   ;    ;    ;    .      Rubrik. Untuk setiap fungsi yang kontinu, berikan pilihan radius. Untuk fungsi yang tidak kontinu, berikan satu toleransi dan saksi untuk setiap radius. Jelaskan apa yang ditunjukkan dua arah pertama tentang pengaruh pemangkasan jarak besar.    Langkah 1. Selalu berlaku . Sebaliknya, jika , maka .   Langkah 2. Bola diskret berjari-jari hanya memuat pusatnya.   Langkah 3. Untuk menggagalkan , pilih pada kodomain diskret dan titik berbeda yang sedekat apa pun dalam .   Fungsi , , dan kontinu, sedangkan tidak kontinu di titik mana pun. Jadi metrik Euklides dan metrik pangkas mempunyai perilaku kekontinuan lokal yang sama, tetapi metrik diskret pada kodomain menuntut pemisahan yang lebih kuat.   Untuk , tetapkan dan , lalu pilih . Jika , maka . Jadi kontinu.  Untuk , pilih . Jika , nilai minimum tidak mungkin berasal dari cabang . Maka . Jadi juga kontinu. Kedua hasil ini menunjukkan bahwa pemangkasan semua jarak besar pada tidak mengubah perilaku lokal yang dideteksi oleh kekontinuan.  Untuk , ambil untuk setiap toleransi positif. Syarat memaksa , sehingga jarak keluarannya nol. Jadi kontinu.  Sebaliknya, tetapkan dan untuk . Untuk setiap , ambil dan . Maka , tetapi , sehingga . Dengan demikian tidak kontinu di , dan sembarang.  "
},
{
  "id": "o003-c90-ch06-mastery-04",
  "level": "2",
  "url": "o003-c90-ch06-mastery.html#o003-c90-ch06-mastery-04",
  "type": "Pemeriksaan",
  "number": "F.43",
  "title": "Jumlah dua fungsi kontinu pada ruang metrik.",
  "body": "Jumlah dua fungsi kontinu pada ruang metrik  Misalkan ruang metrik, , dan kontinu di , dengan metrik Euklides pada . Buktikan langsung bahwa kontinu di .   Rubrik. Jangan mengandaikan radius yang sama tersedia untuk kedua fungsi. Bagikan toleransi, peroleh dua radius, ambil minimumnya, dan gunakan pertidaksamaan segitiga.    Langkah 1. Terapkan kekontinuan dan masing-masing dengan toleransi .   Langkah 2. Gunakan .   Jika dan bekerja untuk toleransi , maka bekerja untuk dan toleransi .   Ambil sembarang . Kekontinuan di memberi sedemikian sehingga mengakibatkan . Kekontinuan memberi dengan implikasi serupa untuk .  Pilih . Jika , kedua taksiran berlaku dan Ini membuktikan bahwa kontinu di .  "
},
{
  "id": "o003-c90-ch06-mastery-05",
  "level": "2",
  "url": "o003-c90-ch06-mastery.html#o003-c90-ch06-mastery-05",
  "type": "Pemeriksaan",
  "number": "F.44",
  "title": "Komposisi fungsi kontinu.",
  "body": "Komposisi fungsi kontinu  Misalkan , , dan ruang-ruang metrik. Jika kontinu di dan kontinu di , buktikan bahwa kontinu di .   Rubrik. Mulailah dari toleransi di . Radius yang dihasilkan oleh kekontinuan harus dipakai sebagai toleransi keluaran ketika menerapkan kekontinuan .    Langkah 1. Untuk , kekontinuan di memberi suatu pada ruang .   Langkah 2. Terapkan kekontinuan di dengan toleransi untuk memperoleh pada ruang .   Pilih dari kekontinuan untuk toleransi , lalu pilih dari kekontinuan untuk toleransi . Rantai kedua implikasi membuktikan kekontinuan di .   Tetapkan . Karena kontinu di , ada sedemikian sehingga Karena kontinu di , untuk toleransi ini ada sedemikian sehingga   Jadi, jika , implikasi kedua menempatkan di dalam bola berjari-jari di sekitar . Dengan mengambil pada implikasi pertama, diperoleh Maka kontinu di .  "
},
{
  "id": "o003-c90-ch06-mastery-06",
  "level": "2",
  "url": "o003-c90-ch06-mastery.html#o003-c90-ch06-mastery-06",
  "type": "Pemeriksaan",
  "number": "F.45",
  "title": "Contoh tandingan bagi kebalikan aturan jumlah.",
  "body": "Contoh tandingan bagi kebalikan aturan jumlah  Bangun dua fungsi yang masing-masing tidak kontinu di titik mana pun, tetapi jumlah kontinu di setiap titik. Buktikan kedua klaim menggunakan metrik Euklides.   Rubrik. Berikan rumus eksplisit bagi kedua fungsi. Untuk ketidakkontinuan, gunakan satu toleransi tetap dan kerapatan bilangan rasional serta irasional. Untuk kekontinuan jumlah, hitung jumlahnya tepat, bukan hanya menyatakan bahwa diskontinuitas “saling meniadakan.”    Langkah 1. Definisikan pada bilangan rasional dan pada bilangan irasional.   Langkah 2. Ambil dan . Gunakan untuk membuktikan ketidakkontinuan masing-masing.   Ambil dan , dengan . Fungsi dan tidak kontinu di titik mana pun, tetapi untuk semua , sehingga jumlahnya kontinu.   Definisikan Ambil dan . Tetapkan sembarang dan . Jika rasional, setiap lingkungan di sekitar memuat titik irasional , dan . Jika irasional, setiap lingkungan memuat titik rasional , dan kembali . Jadi tidak kontinu di . Karena , argumen yang sama membuktikan bahwa juga tidak kontinu di . Titik sembarang, sehingga keduanya tidak kontinu di mana pun.  Namun, untuk setiap , Jadi adalah fungsi konstan nol dan kontinu di setiap titik. Contoh ini menunjukkan bahwa kekontinuan jumlah tidak memaksa kekontinuan masing-masing suku.  "
},
{
  "id": "o003-c90-ch07-source-guides",
  "level": "1",
  "url": "o003-c90-ch07-source-guides.html",
  "type": "Bagian",
  "number": "",
  "title": "Panduan kegiatan sumber",
  "body": " Panduan kegiatan sumber  Enam belas panduan berikut mendampingi seluruh tugas kegiatan dalam Bab 7: lima tugas tentang bentuk bola terbuka, tiga tugas tentang lingkungan, tiga tugas tentang prapeta bola terbuka, dan lima langkah pembuktian kekontinuan melalui lingkungan. Kerjakan lebih dahulu tugas pada bab utama. Sesudah itu, buka petunjuk, jawaban, dan solusi secara bertahap. Rubrik pada setiap pernyataan menjelaskan bukti yang diperlukan tanpa menggantikan proses penyelidikan.  Bola terbuka pada garis bilangan  Jelaskan dan buat sketsa bola terbuka dalam , dengan . Rubrik: ubah syarat jarak menjadi pertidaksamaan rangkap, tuliskan himpunannya, dan tunjukkan apakah titik batas termasuk.   Mulailah dari , lalu hilangkan nilai mutlak.   Bola tersebut adalah interval terbuka .   Menurut definisi, Pertidaksamaan ekuivalen dengan , atau . Jadi . Sketsanya adalah ruas garis di antara dan dengan lingkaran kosong pada kedua ujung karena pertidaksamaannya ketat.   Bola untuk metrik Euklides pada bidang  Jelaskan dan buat sketsa dalam . Rubrik: berikan deskripsi koordinat yang tepat, identifikasi pusat dan jari-jari, serta bedakan bola dari lingkaran batasnya.   Kuadratkan pertidaksamaan jarak; kedua ruasnya tidak negatif.   Hasilnya adalah cakram Euklides terbuka berpusat di dan berjari-jari .   Titik berada dalam bola tepat ketika yang ekuivalen dengan . Jadi Sketsanya memuat seluruh bagian dalam lingkaran berpusat di dan berjari-jari , tetapi tidak memuat lingkaran batas karena jaraknya di sana sama dengan .   Bola untuk metrik maksimum  Jelaskan dan buat sketsa dalam , dengan . Rubrik: uraikan pertidaksamaan maksimum menjadi dua syarat koordinat dan nyatakan status batasnya.   Nilai maksimum dua bilangan lebih kecil daripada tepat ketika keduanya lebih kecil daripada .   Bola tersebut adalah persegi terbuka dengan sisi-sisi sejajar sumbu koordinat.   Syarat keanggotaan adalah Ini ekuivalen dengan dua syarat dan , yakni dan . Oleh karena itu . Sketsanya berupa bagian dalam persegi dengan sudut batas , , , dan ; seluruh sisi dan sudut tidak termasuk.   Bola untuk metrik taksi  Jelaskan dan buat sketsa dalam , dengan . Rubrik: tuliskan pertidaksamaan yang menentukan bola, berikan bentuk geometrisnya, dan identifikasi titik-titik sudut pada batas.   Periksa perpotongan batas dengan garis horizontal dan vertikal melalui pusat.   Bola tersebut adalah bagian dalam belah ketupat , dengan batas melalui , , , dan .   Dari definisi metrik taksi, Himpunan batas diperoleh dengan mengganti oleh . Pada garis , batasnya berada di dan ; pada garis , batasnya berada di dan . Keempat ruas batas membentuk belah ketupat. Karena bola memakai pertidaksamaan ketat, hanya bagian dalam belah ketupat yang termasuk.   Bola untuk metrik diskret  Tentukan dalam dengan metrik diskret. Bandingkan hasilnya dengan ketika dan ketika . Rubrik: gunakan semua kemungkinan nilai jarak diskret dan ingat bahwa definisi bola memakai pertidaksamaan ketat.   Dalam metrik diskret, jarak dari pusat hanya dapat bernilai atau . Bandingkan kedua nilai itu dengan jari-jari.   Untuk , bolanya hanya ; untuk , bolanya adalah seluruh .   Pusat mempunyai , sedangkan setiap titik mempunyai . Untuk jari-jari , hanya pusat yang memenuhi , sehingga . Argumen yang sama berlaku jika : jarak masih lebih kecil daripada , tetapi jarak tidak. Jika , baik jarak maupun lebih kecil daripada . Karena itu setiap titik termasuk dan .   Target pembuktian lingkungan  Misalkan . Nyatakan dengan tepat apa yang harus ditemukan untuk membuktikan bahwa merupakan lingkungan bagi . Rubrik: buka definisi lingkungan pada titik dan nyatakan baik kepositifan jari-jari maupun inklusi himpunannya.   Ganti oleh dan titik pangkal oleh dalam definisi lingkungan.   Kita harus menemukan sedemikian sehingga .   Sebuah himpunan merupakan lingkungan bagi tepat ketika ada bola terbuka berpusat di yang termuat dalam . Di sini . Jadi target lengkapnya adalah membangun suatu bilangan dan membuktikan Syarat akan menjamin adanya ruang positif antara dan batas berjari-jari ; butir berikutnya menghitung ruang itu.   Bola kecil di dalam bola besar  Buktikan bahwa jika , maka merupakan lingkungan bagi . Gunakan . Rubrik: buktikan bahwa positif, ambil titik sebarang dalam , lalu gunakan pertidaksamaan segitiga untuk memperoleh inklusi.   Untuk , bandingkan dengan , kemudian substitusikan definisi .   Nilai positif dan memenuhi .   Karena , berlaku . Maka . Ambil sebarang . Pertidaksamaan segitiga dan kesimetrian metrik memberikan Jadi . Karena sebarang, . Jadi memuat bola terbuka berpusat di dan merupakan lingkungan bagi .   Lingkungan setiap titik tidak harus sebuah bola  Tentukan apakah setiap himpunan yang merupakan lingkungan bagi semua titiknya harus berupa satu bola terbuka. Berikan contoh tandingan terbuka dan alasan yang meyakinkan. Rubrik: verifikasi sifat lingkungan pada setiap titik dan buktikan bahwa himpunan contoh bukan satu bola.   Dalam bermetrik Euklides, pertimbangkan gabungan dua interval terbuka yang saling terpisah.   Tidak. Sebagai contoh, merupakan lingkungan bagi setiap titiknya, tetapi bukan sebuah bola terbuka dalam bermetrik Euklides.   Ambil . Jika , pilih ; maka . Jika , pilih ; lagi-lagi . Jadi merupakan lingkungan bagi setiap titiknya.  Setiap bola terbuka dalam bermetrik Euklides adalah satu interval , sehingga memuat setiap titik di antara dua titik anggotanya. Himpunan memuat, misalnya, dan , tetapi tidak memuat yang berada di antaranya. Karena itu bukan satu bola terbuka. Pernyataan sebaliknya salah.   Bola di sekitar nilai fungsi  Untuk , , dengan metrik Euklides, tentukan . Rubrik: hitung dahulu nilai pusatnya, lalu ubah syarat jarak menjadi interval terbuka.   Nilai adalah ; selesaikan .    .   Karena , definisi bola Euklides memberi Pertidaksamaan tersebut ekuivalen dengan . Maka bolanya adalah interval terbuka .   Prapeta bola di bawah fungsi kuadrat  Dengan fungsi dan metrik yang sama, tentukan . Rubrik: tuliskan pertidaksamaan ganda untuk , selesaikan pada bagian negatif dan positif, dan perhatikan bahwa semua titik batas dikecualikan.   Dari butir sebelumnya, syaratnya adalah . Gunakan .    .   Suatu bilangan berada dalam prapeta tepat ketika , yaitu ketika . Syarat ini ekuivalen dengan . Pada sumbu negatif, diperoleh ; pada sumbu positif, diperoleh . Oleh karena itu Keempat titik batas tidak termasuk karena bola asal memakai pertidaksamaan ketat.   Prapeta bukan bola berpusat di titik pangkal  Tentukan apakah merupakan bola terbuka yang berpusat di , dan jelaskan. Rubrik: bandingkan bentuk prapeta dengan bentuk setiap bola Euklides berpusat di ; satu pengamatan struktural yang menentukan harus dinyatakan.   Bola selalu satu interval . Berapa banyak komponen interval yang dimiliki prapeta pada butir sebelumnya?   Tidak. Prapeta itu adalah gabungan dua interval terpisah, sedangkan setiap bola Euklides berpusat di merupakan satu interval yang simetris terhadap .   Dari butir sebelumnya, Himpunan ini mempunyai dua bagian yang terpisah. Sebaliknya, untuk setiap , bola Euklides berpusat di adalah , yaitu satu interval. Bahkan prapeta memuat titik-titik dekat tetapi tidak memuat , meskipun lebih dekat ke daripada titik-titik tersebut. Ini mustahil bagi bola berpusat di . Jadi prapeta itu bukan bola terbuka berpusat di .   Target inklusi untuk kekontinuan  Misalkan prapeta setiap lingkungan bagi merupakan lingkungan bagi . Nyatakan target yang, menurut pencirian bola terbuka, cukup untuk membuktikan bahwa kontinu di . Rubrik: mulai dengan sebarang dan nyatakan kuantor untuk beserta inklusi yang tepat.   Pencirian itu membandingkan dengan prapeta .   Untuk setiap , kita harus menemukan sedemikian sehingga .   Pencirian kekontinuan melalui bola terbuka menyatakan bahwa kontinu di jika dan hanya jika Jadi setelah memilih sebarang, seluruh pekerjaan yang tersisa adalah menghasilkan dengan inklusi tersebut. Empat butir berikut membangunnya dari hipotesis lingkungan.   Bola sebagai lingkungan titik pusatnya  Untuk , jelaskan mengapa merupakan lingkungan bagi . Rubrik: tunjukkan secara eksplisit sebuah bola terbuka berpusat di yang termuat dalam himpunan tersebut.   Himpunan yang hendak diuji sudah merupakan bola terbuka. Ia dapat memuat dirinya sendiri.   Pilih jari-jari ; berlaku , sehingga himpunan itu merupakan lingkungan bagi .   Menurut definisi, suatu himpunan merupakan lingkungan bagi jika terdapat dengan . Ambil dan . Jari-jari ini positif dan Jadi bola tersebut memang merupakan lingkungan bagi titik pusatnya.   Menerapkan hipotesis prapeta  Gunakan hipotesis bahwa prapeta setiap lingkungan bagi merupakan lingkungan bagi untuk menentukan sifat . Rubrik: identifikasi himpunan yang memainkan peran sebagai lingkungan dalam kodomain dan terapkan hipotesis tepat satu kali.   Butir sebelumnya telah memverifikasi bahwa memenuhi premis hipotesis.   Himpunan merupakan lingkungan bagi .   Tetapkan . Dari butir sebelumnya, merupakan lingkungan bagi . Hipotesis mengatakan bahwa untuk setiap lingkungan bagi , prapetanya merupakan lingkungan bagi . Dengan mensubstitusikan pilihan , kita memperoleh bahwa merupakan lingkungan bagi .   Membuka definisi lingkungan prapeta  Uraikan kesimpulan bahwa merupakan lingkungan bagi . Rubrik: tuliskan jari-jari positif yang dijamin ada dan inklusi bola yang dihasilkan; jangan berhenti pada kata lingkungan .   Terapkan definisi lingkungan dengan .   Terdapat sedemikian sehingga .   Definisi lingkungan menyatakan bahwa merupakan lingkungan bagi tepat ketika ada dengan . Butir sebelumnya memberi . Oleh karena itu terdapat sedemikian sehingga Inilah inklusi yang ditetapkan sebagai target pada butir pertama.   Menutup pembuktian kekontinuan  Rangkai bagian (a)-(d) untuk membuktikan bahwa kontinu di . Rubrik: mulai dengan sebarang, jelaskan rantai lingkungan dan prapeta, hasilkan inklusi untuk suatu , lalu sebutkan pencirian kekontinuan yang menutup bukti.   Rantainya adalah: bola di kodomain merupakan lingkungan; hipotesis membawa lingkungan itu melalui prapeta; definisi lingkungan memberi bola di domain; pencirian bola memberi kekontinuan.   Untuk setiap , hipotesis menghasilkan dengan . Menurut pencirian bola terbuka, kontinu di .   Ambil sebarang . Bola merupakan lingkungan bagi karena ia memuat bola itu sendiri. Berdasarkan hipotesis, prapetanya merupakan lingkungan bagi . Dengan membuka definisi lingkungan, terdapat sedemikian sehingga Karena konstruksi ini berlaku untuk setiap , pencirian kekontinuan melalui bola terbuka menyatakan bahwa kontinu di . Semua kuantor yang diperlukan untuk arah pembuktian ini telah tertutup.   "
},
{
  "id": "o003-c90-ch07-intro-task-01",
  "level": "2",
  "url": "o003-c90-ch07-source-guides.html#o003-c90-ch07-intro-task-01",
  "type": "Pemeriksaan",
  "number": "G.1",
  "title": "Bola terbuka pada garis bilangan.",
  "body": "Bola terbuka pada garis bilangan  Jelaskan dan buat sketsa bola terbuka dalam , dengan . Rubrik: ubah syarat jarak menjadi pertidaksamaan rangkap, tuliskan himpunannya, dan tunjukkan apakah titik batas termasuk.   Mulailah dari , lalu hilangkan nilai mutlak.   Bola tersebut adalah interval terbuka .   Menurut definisi, Pertidaksamaan ekuivalen dengan , atau . Jadi . Sketsanya adalah ruas garis di antara dan dengan lingkaran kosong pada kedua ujung karena pertidaksamaannya ketat.  "
},
{
  "id": "o003-c90-ch07-intro-task-02",
  "level": "2",
  "url": "o003-c90-ch07-source-guides.html#o003-c90-ch07-intro-task-02",
  "type": "Pemeriksaan",
  "number": "G.2",
  "title": "Bola untuk metrik Euklides pada bidang.",
  "body": "Bola untuk metrik Euklides pada bidang  Jelaskan dan buat sketsa dalam . Rubrik: berikan deskripsi koordinat yang tepat, identifikasi pusat dan jari-jari, serta bedakan bola dari lingkaran batasnya.   Kuadratkan pertidaksamaan jarak; kedua ruasnya tidak negatif.   Hasilnya adalah cakram Euklides terbuka berpusat di dan berjari-jari .   Titik berada dalam bola tepat ketika yang ekuivalen dengan . Jadi Sketsanya memuat seluruh bagian dalam lingkaran berpusat di dan berjari-jari , tetapi tidak memuat lingkaran batas karena jaraknya di sana sama dengan .  "
},
{
  "id": "o003-c90-ch07-intro-task-03",
  "level": "2",
  "url": "o003-c90-ch07-source-guides.html#o003-c90-ch07-intro-task-03",
  "type": "Pemeriksaan",
  "number": "G.3",
  "title": "Bola untuk metrik maksimum.",
  "body": "Bola untuk metrik maksimum  Jelaskan dan buat sketsa dalam , dengan . Rubrik: uraikan pertidaksamaan maksimum menjadi dua syarat koordinat dan nyatakan status batasnya.   Nilai maksimum dua bilangan lebih kecil daripada tepat ketika keduanya lebih kecil daripada .   Bola tersebut adalah persegi terbuka dengan sisi-sisi sejajar sumbu koordinat.   Syarat keanggotaan adalah Ini ekuivalen dengan dua syarat dan , yakni dan . Oleh karena itu . Sketsanya berupa bagian dalam persegi dengan sudut batas , , , dan ; seluruh sisi dan sudut tidak termasuk.  "
},
{
  "id": "o003-c90-ch07-intro-task-04",
  "level": "2",
  "url": "o003-c90-ch07-source-guides.html#o003-c90-ch07-intro-task-04",
  "type": "Pemeriksaan",
  "number": "G.4",
  "title": "Bola untuk metrik taksi.",
  "body": "Bola untuk metrik taksi  Jelaskan dan buat sketsa dalam , dengan . Rubrik: tuliskan pertidaksamaan yang menentukan bola, berikan bentuk geometrisnya, dan identifikasi titik-titik sudut pada batas.   Periksa perpotongan batas dengan garis horizontal dan vertikal melalui pusat.   Bola tersebut adalah bagian dalam belah ketupat , dengan batas melalui , , , dan .   Dari definisi metrik taksi, Himpunan batas diperoleh dengan mengganti oleh . Pada garis , batasnya berada di dan ; pada garis , batasnya berada di dan . Keempat ruas batas membentuk belah ketupat. Karena bola memakai pertidaksamaan ketat, hanya bagian dalam belah ketupat yang termasuk.  "
},
{
  "id": "o003-c90-ch07-intro-task-05",
  "level": "2",
  "url": "o003-c90-ch07-source-guides.html#o003-c90-ch07-intro-task-05",
  "type": "Pemeriksaan",
  "number": "G.5",
  "title": "Bola untuk metrik diskret.",
  "body": "Bola untuk metrik diskret  Tentukan dalam dengan metrik diskret. Bandingkan hasilnya dengan ketika dan ketika . Rubrik: gunakan semua kemungkinan nilai jarak diskret dan ingat bahwa definisi bola memakai pertidaksamaan ketat.   Dalam metrik diskret, jarak dari pusat hanya dapat bernilai atau . Bandingkan kedua nilai itu dengan jari-jari.   Untuk , bolanya hanya ; untuk , bolanya adalah seluruh .   Pusat mempunyai , sedangkan setiap titik mempunyai . Untuk jari-jari , hanya pusat yang memenuhi , sehingga . Argumen yang sama berlaku jika : jarak masih lebih kecil daripada , tetapi jarak tidak. Jika , baik jarak maupun lebih kecil daripada . Karena itu setiap titik termasuk dan .  "
},
{
  "id": "o003-c90-ch07-neighborhood-task-01",
  "level": "2",
  "url": "o003-c90-ch07-source-guides.html#o003-c90-ch07-neighborhood-task-01",
  "type": "Pemeriksaan",
  "number": "G.6",
  "title": "Target pembuktian lingkungan.",
  "body": "Target pembuktian lingkungan  Misalkan . Nyatakan dengan tepat apa yang harus ditemukan untuk membuktikan bahwa merupakan lingkungan bagi . Rubrik: buka definisi lingkungan pada titik dan nyatakan baik kepositifan jari-jari maupun inklusi himpunannya.   Ganti oleh dan titik pangkal oleh dalam definisi lingkungan.   Kita harus menemukan sedemikian sehingga .   Sebuah himpunan merupakan lingkungan bagi tepat ketika ada bola terbuka berpusat di yang termuat dalam . Di sini . Jadi target lengkapnya adalah membangun suatu bilangan dan membuktikan Syarat akan menjamin adanya ruang positif antara dan batas berjari-jari ; butir berikutnya menghitung ruang itu.  "
},
{
  "id": "o003-c90-ch07-neighborhood-task-02",
  "level": "2",
  "url": "o003-c90-ch07-source-guides.html#o003-c90-ch07-neighborhood-task-02",
  "type": "Pemeriksaan",
  "number": "G.7",
  "title": "Bola kecil di dalam bola besar.",
  "body": "Bola kecil di dalam bola besar  Buktikan bahwa jika , maka merupakan lingkungan bagi . Gunakan . Rubrik: buktikan bahwa positif, ambil titik sebarang dalam , lalu gunakan pertidaksamaan segitiga untuk memperoleh inklusi.   Untuk , bandingkan dengan , kemudian substitusikan definisi .   Nilai positif dan memenuhi .   Karena , berlaku . Maka . Ambil sebarang . Pertidaksamaan segitiga dan kesimetrian metrik memberikan Jadi . Karena sebarang, . Jadi memuat bola terbuka berpusat di dan merupakan lingkungan bagi .  "
},
{
  "id": "o003-c90-ch07-neighborhood-task-03",
  "level": "2",
  "url": "o003-c90-ch07-source-guides.html#o003-c90-ch07-neighborhood-task-03",
  "type": "Pemeriksaan",
  "number": "G.8",
  "title": "Lingkungan setiap titik tidak harus sebuah bola.",
  "body": "Lingkungan setiap titik tidak harus sebuah bola  Tentukan apakah setiap himpunan yang merupakan lingkungan bagi semua titiknya harus berupa satu bola terbuka. Berikan contoh tandingan terbuka dan alasan yang meyakinkan. Rubrik: verifikasi sifat lingkungan pada setiap titik dan buktikan bahwa himpunan contoh bukan satu bola.   Dalam bermetrik Euklides, pertimbangkan gabungan dua interval terbuka yang saling terpisah.   Tidak. Sebagai contoh, merupakan lingkungan bagi setiap titiknya, tetapi bukan sebuah bola terbuka dalam bermetrik Euklides.   Ambil . Jika , pilih ; maka . Jika , pilih ; lagi-lagi . Jadi merupakan lingkungan bagi setiap titiknya.  Setiap bola terbuka dalam bermetrik Euklides adalah satu interval , sehingga memuat setiap titik di antara dua titik anggotanya. Himpunan memuat, misalnya, dan , tetapi tidak memuat yang berada di antaranya. Karena itu bukan satu bola terbuka. Pernyataan sebaliknya salah.  "
},
{
  "id": "o003-c90-ch07-continuity-ball-task-01",
  "level": "2",
  "url": "o003-c90-ch07-source-guides.html#o003-c90-ch07-continuity-ball-task-01",
  "type": "Pemeriksaan",
  "number": "G.9",
  "title": "Bola di sekitar nilai fungsi.",
  "body": "Bola di sekitar nilai fungsi  Untuk , , dengan metrik Euklides, tentukan . Rubrik: hitung dahulu nilai pusatnya, lalu ubah syarat jarak menjadi interval terbuka.   Nilai adalah ; selesaikan .    .   Karena , definisi bola Euklides memberi Pertidaksamaan tersebut ekuivalen dengan . Maka bolanya adalah interval terbuka .  "
},
{
  "id": "o003-c90-ch07-continuity-ball-task-02",
  "level": "2",
  "url": "o003-c90-ch07-source-guides.html#o003-c90-ch07-continuity-ball-task-02",
  "type": "Pemeriksaan",
  "number": "G.10",
  "title": "Prapeta bola di bawah fungsi kuadrat.",
  "body": "Prapeta bola di bawah fungsi kuadrat  Dengan fungsi dan metrik yang sama, tentukan . Rubrik: tuliskan pertidaksamaan ganda untuk , selesaikan pada bagian negatif dan positif, dan perhatikan bahwa semua titik batas dikecualikan.   Dari butir sebelumnya, syaratnya adalah . Gunakan .    .   Suatu bilangan berada dalam prapeta tepat ketika , yaitu ketika . Syarat ini ekuivalen dengan . Pada sumbu negatif, diperoleh ; pada sumbu positif, diperoleh . Oleh karena itu Keempat titik batas tidak termasuk karena bola asal memakai pertidaksamaan ketat.  "
},
{
  "id": "o003-c90-ch07-continuity-ball-task-03",
  "level": "2",
  "url": "o003-c90-ch07-source-guides.html#o003-c90-ch07-continuity-ball-task-03",
  "type": "Pemeriksaan",
  "number": "G.11",
  "title": "Prapeta bukan bola berpusat di titik pangkal.",
  "body": "Prapeta bukan bola berpusat di titik pangkal  Tentukan apakah merupakan bola terbuka yang berpusat di , dan jelaskan. Rubrik: bandingkan bentuk prapeta dengan bentuk setiap bola Euklides berpusat di ; satu pengamatan struktural yang menentukan harus dinyatakan.   Bola selalu satu interval . Berapa banyak komponen interval yang dimiliki prapeta pada butir sebelumnya?   Tidak. Prapeta itu adalah gabungan dua interval terpisah, sedangkan setiap bola Euklides berpusat di merupakan satu interval yang simetris terhadap .   Dari butir sebelumnya, Himpunan ini mempunyai dua bagian yang terpisah. Sebaliknya, untuk setiap , bola Euklides berpusat di adalah , yaitu satu interval. Bahkan prapeta memuat titik-titik dekat tetapi tidak memuat , meskipun lebih dekat ke daripada titik-titik tersebut. Ini mustahil bagi bola berpusat di . Jadi prapeta itu bukan bola terbuka berpusat di .  "
},
{
  "id": "o003-c90-ch07-continuity-neighborhood-task-01",
  "level": "2",
  "url": "o003-c90-ch07-source-guides.html#o003-c90-ch07-continuity-neighborhood-task-01",
  "type": "Pemeriksaan",
  "number": "G.12",
  "title": "Target inklusi untuk kekontinuan.",
  "body": "Target inklusi untuk kekontinuan  Misalkan prapeta setiap lingkungan bagi merupakan lingkungan bagi . Nyatakan target yang, menurut pencirian bola terbuka, cukup untuk membuktikan bahwa kontinu di . Rubrik: mulai dengan sebarang dan nyatakan kuantor untuk beserta inklusi yang tepat.   Pencirian itu membandingkan dengan prapeta .   Untuk setiap , kita harus menemukan sedemikian sehingga .   Pencirian kekontinuan melalui bola terbuka menyatakan bahwa kontinu di jika dan hanya jika Jadi setelah memilih sebarang, seluruh pekerjaan yang tersisa adalah menghasilkan dengan inklusi tersebut. Empat butir berikut membangunnya dari hipotesis lingkungan.  "
},
{
  "id": "o003-c90-ch07-continuity-neighborhood-task-02",
  "level": "2",
  "url": "o003-c90-ch07-source-guides.html#o003-c90-ch07-continuity-neighborhood-task-02",
  "type": "Pemeriksaan",
  "number": "G.13",
  "title": "Bola sebagai lingkungan titik pusatnya.",
  "body": "Bola sebagai lingkungan titik pusatnya  Untuk , jelaskan mengapa merupakan lingkungan bagi . Rubrik: tunjukkan secara eksplisit sebuah bola terbuka berpusat di yang termuat dalam himpunan tersebut.   Himpunan yang hendak diuji sudah merupakan bola terbuka. Ia dapat memuat dirinya sendiri.   Pilih jari-jari ; berlaku , sehingga himpunan itu merupakan lingkungan bagi .   Menurut definisi, suatu himpunan merupakan lingkungan bagi jika terdapat dengan . Ambil dan . Jari-jari ini positif dan Jadi bola tersebut memang merupakan lingkungan bagi titik pusatnya.  "
},
{
  "id": "o003-c90-ch07-continuity-neighborhood-task-03",
  "level": "2",
  "url": "o003-c90-ch07-source-guides.html#o003-c90-ch07-continuity-neighborhood-task-03",
  "type": "Pemeriksaan",
  "number": "G.14",
  "title": "Menerapkan hipotesis prapeta.",
  "body": "Menerapkan hipotesis prapeta  Gunakan hipotesis bahwa prapeta setiap lingkungan bagi merupakan lingkungan bagi untuk menentukan sifat . Rubrik: identifikasi himpunan yang memainkan peran sebagai lingkungan dalam kodomain dan terapkan hipotesis tepat satu kali.   Butir sebelumnya telah memverifikasi bahwa memenuhi premis hipotesis.   Himpunan merupakan lingkungan bagi .   Tetapkan . Dari butir sebelumnya, merupakan lingkungan bagi . Hipotesis mengatakan bahwa untuk setiap lingkungan bagi , prapetanya merupakan lingkungan bagi . Dengan mensubstitusikan pilihan , kita memperoleh bahwa merupakan lingkungan bagi .  "
},
{
  "id": "o003-c90-ch07-continuity-neighborhood-task-04",
  "level": "2",
  "url": "o003-c90-ch07-source-guides.html#o003-c90-ch07-continuity-neighborhood-task-04",
  "type": "Pemeriksaan",
  "number": "G.15",
  "title": "Membuka definisi lingkungan prapeta.",
  "body": "Membuka definisi lingkungan prapeta  Uraikan kesimpulan bahwa merupakan lingkungan bagi . Rubrik: tuliskan jari-jari positif yang dijamin ada dan inklusi bola yang dihasilkan; jangan berhenti pada kata lingkungan .   Terapkan definisi lingkungan dengan .   Terdapat sedemikian sehingga .   Definisi lingkungan menyatakan bahwa merupakan lingkungan bagi tepat ketika ada dengan . Butir sebelumnya memberi . Oleh karena itu terdapat sedemikian sehingga Inilah inklusi yang ditetapkan sebagai target pada butir pertama.  "
},
{
  "id": "o003-c90-ch07-continuity-neighborhood-task-05",
  "level": "2",
  "url": "o003-c90-ch07-source-guides.html#o003-c90-ch07-continuity-neighborhood-task-05",
  "type": "Pemeriksaan",
  "number": "G.16",
  "title": "Menutup pembuktian kekontinuan.",
  "body": "Menutup pembuktian kekontinuan  Rangkai bagian (a)-(d) untuk membuktikan bahwa kontinu di . Rubrik: mulai dengan sebarang, jelaskan rantai lingkungan dan prapeta, hasilkan inklusi untuk suatu , lalu sebutkan pencirian kekontinuan yang menutup bukti.   Rantainya adalah: bola di kodomain merupakan lingkungan; hipotesis membawa lingkungan itu melalui prapeta; definisi lingkungan memberi bola di domain; pencirian bola memberi kekontinuan.   Untuk setiap , hipotesis menghasilkan dengan . Menurut pencirian bola terbuka, kontinu di .   Ambil sebarang . Bola merupakan lingkungan bagi karena ia memuat bola itu sendiri. Berdasarkan hipotesis, prapetanya merupakan lingkungan bagi . Dengan membuka definisi lingkungan, terdapat sedemikian sehingga Karena konstruksi ini berlaku untuk setiap , pencirian kekontinuan melalui bola terbuka menyatakan bahwa kontinu di . Semua kuantor yang diperlukan untuk arah pembuktian ini telah tertutup.  "
},
{
  "id": "o003-c90-ch07-exercise-guides-a",
  "level": "1",
  "url": "o003-c90-ch07-exercise-guides-a.html",
  "type": "Bagian",
  "number": "",
  "title": "Panduan latihan sumber, bagian pertama",
  "body": " Panduan latihan sumber, bagian pertama  Dua belas panduan berikut berkorespondensi dengan dua belas perintah pertama pada bagian latihan Bab 7 menurut urutan kedalaman sumber. Materi pendamping ini merupakan uraian asli untuk pembelajaran mandiri, bukan jawaban yang disediakan oleh penulis karya sumber.  Cakram satuan sebagai lingkungan  Dalam , misalkan dan . Tentukan, disertai bukti, apakah merupakan lingkungan dari . Rubrik. Nyatakan sebuah radius positif dan buktikan bahwa seluruh bola terbuka dengan pusat dan radius tersebut termuat dalam .    Langkah 1. Jarak Euklides dari titik asal adalah .   Langkah 2. Gunakan pertidaksamaan segitiga untuk titik .   Ya. Radius positif dan memenuhi .   Tuliskan untuk norma Euklides titik . Karena bilangan positif. Jika , maka pertidaksamaan segitiga memberi Jadi jumlah kuadrat koordinat kurang daripada , sehingga . Dengan demikian , dan menurut definisi merupakan lingkungan dari .   Sumbu horizontal dalam metrik taksi  Dalam , misalkan adalah sumbu dan . Tentukan, disertai bukti, apakah merupakan lingkungan dari . Rubrik. Jika jawabannya negatif, untuk setiap radius positif berikan titik di dalam bola yang tidak berada pada sumbu .   Untuk , periksa titik dan hitung .   Tidak. Setiap bola memuat titik , yang tidak berada pada sumbu .   Ambil sebarang dan tetapkan . Jarak taksi dari ke adalah Maka . Akan tetapi, koordinat kedua tidak nol, sehingga . Jadi tidak ada dengan . Oleh karena itu, bukan lingkungan dari .   Bilangan rasional bukan lingkungan di garis real  Dalam , misalkan dan . Tentukan, disertai bukti, apakah merupakan lingkungan dari . Rubrik. Gunakan urutan kuantor dalam definisi lingkungan dan sifat kerapatan bilangan irasional.   Setiap interval terbuka memuat bilangan irasional.   Tidak. Untuk setiap , bola memuat suatu bilangan irasional dan karenanya tidak termuat dalam .   Misalkan diberikan. Kerapatan bilangan irasional dalam menjamin adanya dengan . Dengan demikian , sehingga , tetapi . Argumen ini berlaku untuk setiap radius positif, sehingga tidak ada bola terbuka berpusat di yang termuat dalam . Jadi bukan lingkungan dari dalam metrik Euklides.   Bilangan bulat positif dalam metrik pecahan tereduksi  Misalkan adalah himpunan bilangan rasional dalam bentuk paling sederhana dan . Dalam , tentukan apakah himpunan semua bilangan bulat positif merupakan lingkungan dari . Rubrik. Tentukan bola terbuka berjari-jari di sekitar dan jelaskan peran koordinat pembilang serta penyebut yang bulat.   Jika dua pecahan tereduksi berbeda, setidaknya salah satu dari selisih pembilang dan selisih penyebutnya adalah bilangan bulat tak nol.   Ya. Bola hanya berisi , sehingga bola itu termuat dalam himpunan bilangan bulat positif.   Ambil dalam bentuk paling sederhana. Jika , pasangan bilangan bulat berbeda dari . Maka paling sedikit satu dari dan merupakan bilangan bulat positif, sehingga Akibatnya, syarat hanya dipenuhi oleh . Jadi . Karena memuat bola terbuka berpusat di , merupakan lingkungan dari .   Semua fungsi dari ruang metrik berhingga ini kontinu  Misalkan dan , yakni sisa pembagian oleh . Untuk sebarang ruang metrik , tentukan apakah mungkin mendefinisikan fungsi yang tidak kontinu. Rubrik. Hitung jarak antar-titik berbeda dan berikan satu radius yang mengisolasi setiap titik domain.   Jarak antartitik berbeda adalah , , dan . Apa isi untuk ?   Tidak mungkin. Setiap fungsi kontinu; radius mengisolasi setiap titik .   Perhitungan modulo memberikan , , dan . Jadi untuk setiap , tidak ada titik lain yang berjarak kurang daripada dari ; dengan kata lain, .  Sekarang ambil fungsi sebarang , titik , dan . Pilih . Jika , maka , sehingga Jadi kontinu di setiap titik dalam . Tidak ada fungsi tak kontinu dari domain ini ke ruang metrik mana pun.   Dua fungsi pada ruang bermetrik pusat  Pada , dengan jika dan jika , definisikan oleh , untuk , serta jika dan selain itu. Tentukan fungsi mana yang kontinu dan buktikan kedua klaim. Rubrik. Periksa titik asal secara terpisah; untuk titik tak nol, tunjukkan bahwa terdapat bola terbuka yang hanya memuat pusatnya.    Langkah 1. Untuk setiap , berlaku .   Langkah 2. Di titik asal, bandingkan perilaku dan pada titik-titik tak nol yang normanya menuju nol.   Fungsi tidak kontinu di , sedangkan kontinu pada seluruh . Untuk di , radius bekerja; semua titik tak nol terisolasi.   Untuk menunjukkan bahwa tidak kontinu di , tetapkan . Diberikan sebarang , pilih . Maka dan Ini adalah negasi definisi kekontinuan, sehingga tidak kontinu.  Untuk di titik asal, pilih bagi sebarang . Jika , maka , sehingga dan jarak keluarannya nol. Jadi kontinu di .  Terakhir, jika , maka untuk setiap berlaku . Karena itu . Untuk setiap , pilihan memaksa dan karenanya . Maka kontinu di setiap titik tak nol juga, sehingga kontinu pada seluruh .   Semua bola terbuka pada graf berbobot  Pada ruang metrik graf berbobot dengan sisi , , , , , , , dan , tentukan untuk setiap . Rubrik. Hitung dahulu jarak lintasan terpendek dari ke kelima simpul, lalu pisahkan semua rentang radius pada nilai jarak kritis.   Jarak dari ke , berturut-turut, adalah . Ingat bahwa bola terbuka memakai pertidaksamaan ketat .   Bola-bolanya adalah untuk ; untuk ; untuk ; untuk ; dan untuk .   Jalankan langkah jarak terpendek dari . Mula-mula diperoleh jarak tentatif , , dan dari sisi-sisi yang bersisian dengan . Melalui , jarak ke tetap , jarak ke menjadi , dan jarak ke tetap . Melalui , kandidat jarak ke adalah , sehingga tidak memperbaiki . Melalui , kandidat jarak ke adalah , sama dengan jarak yang sudah diperoleh. Karena semua bobot sisi positif, langkah-langkah ini menyelesaikan pemeriksaan lintasan terpendek. Jadi jarak dari ke , berturut-turut, adalah .  Sebuah simpul masuk ke tepat ketika jaraknya kurang daripada . Karena ketaksamaan ini ketat, simpul pada jarak baru masuk setelah radius melewati nilai tersebut. Dengan demikian    Semua lingkungan dari simpul a  Untuk ruang metrik graf berbobot pada tugas sebelumnya, tentukan semua lingkungan dari . Rubrik. Gunakan bola terbuka terkecil yang ditemukan dan buktikan kedua arah klasifikasi.   Karena , setiap subhimpunan yang memuat otomatis memuat sebuah bola terbuka berpusat di .   Lingkungan dari tepat merupakan semua subhimpunan yang memuat .   Jika merupakan lingkungan dari , maka ada dengan . Setiap bola berpusat di memuat pusatnya, sehingga .  Sebaliknya, andaikan . Dari perhitungan tugas sebelumnya, . Maka , sehingga menurut definisi merupakan lingkungan dari . Kedua arah ini membuktikan klasifikasi tersebut.   Prapeta bola di bawah fungsi linear  Misalkan didefinisikan oleh , dengan . Untuk dan , tunjukkan bahwa memuat bola terbuka berpusat di , lalu simpulkan kekontinuan fungsi linear. Rubrik. Hitung selisih dan berikan radius eksplisit dalam dan .   Gunakan dan pilih .   Berlaku . Maka pilihan membuktikan kekontinuan di setiap .   Untuk setiap , Karena , radius positif. Kita mempunyai rangkaian kesetaraan Jadi prapeta tersebut bukan hanya memuat, melainkan sama dengan bola yang dinyatakan. Karena konstruksi ini berlaku bagi setiap dan , kontinu. Jika istilah fungsi linear juga mencakup kasus , kasus itu adalah fungsi konstan dan juga kontinu.   Prapeta bola di bawah fungsi kuadrat  Misalkan didefinisikan oleh , dengan . Untuk dan , tunjukkan bahwa memuat bola terbuka berpusat di , lalu simpulkan bahwa setiap fungsi kuadrat kontinu. Rubrik. Faktorkan selisih nilai fungsi, batasi di sekitar , dan berikan radius eksplisit.    Langkah 1. Gunakan .   Langkah 2. Tetapkan dan pilih .   Dengan , radius memenuhi . Jadi kontinu di setiap .   Karena , bilangan positif. Tetapkan . Jika , maka , sehingga dan . Oleh karena itu, Jadi setiap kali . Ini membuktikan . Karena dan dipilih sembarang, kontinu pada .   Fungsi jarak ke suatu himpunan  Misalkan ruang metrik dan tak kosong. Definisikan dengan . Gunakan untuk menunjukkan bahwa, bagi setiap dan , terdapat lingkungan dari dengan . Simpulkan bahwa kontinu. Rubrik. Turunkan batas simetris untuk selisih mutlak dua jarak ke , lalu pilih lingkungan secara eksplisit.   Tukarkan dan dalam pertidaksamaan yang diberikan, lalu gabungkan kedua hasil untuk memperoleh pertidaksamaan 1-Lipschitz.   Berlaku . Karena itu memenuhi syarat, dan bahkan 1-Lipschitz.   Pertidaksamaan yang diberikan menyatakan . Setelah dan ditukar, simetri metrik memberi . Kedua pertidaksamaan itu setara dengan   Tetapkan dan , lalu ambil . Jika , maka Dengan demikian . Karena ini berlaku untuk setiap dan , fungsi kontinu; batas pertama juga menunjukkan bahwa konstanta Lipschitz-nya paling besar .   Lingkungan terpisah bagi dua titik berbeda  Misalkan dan dua titik berbeda dalam ruang metrik . Buktikan bahwa terdapat lingkungan dan , masing-masing dari dan , dengan . Rubrik. Pilih radius berdasarkan dan gunakan pertidaksamaan segitiga untuk membuktikan ketakteririsan.   Karena , bilangan positif. Cobalah dan .   Ambil , , dan . Kedua bola terbuka itu merupakan lingkungan dan tidak beririsan.   Karena , sifat definit positif metrik memberi . Tetapkan dan ambil serta . Masing-masing jelas merupakan lingkungan dari pusatnya.  Andaikan, untuk memperoleh kontradiksi, ada . Maka dan . Pertidaksamaan segitiga memberikan suatu kontradiksi. Jadi , sebagaimana diminta.   "
},
{
  "id": "o003-c90-ch07-exercise-task-01",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-a.html#o003-c90-ch07-exercise-task-01",
  "type": "Pemeriksaan",
  "number": "G.17",
  "title": "Cakram satuan sebagai lingkungan.",
  "body": "Cakram satuan sebagai lingkungan  Dalam , misalkan dan . Tentukan, disertai bukti, apakah merupakan lingkungan dari . Rubrik. Nyatakan sebuah radius positif dan buktikan bahwa seluruh bola terbuka dengan pusat dan radius tersebut termuat dalam .    Langkah 1. Jarak Euklides dari titik asal adalah .   Langkah 2. Gunakan pertidaksamaan segitiga untuk titik .   Ya. Radius positif dan memenuhi .   Tuliskan untuk norma Euklides titik . Karena bilangan positif. Jika , maka pertidaksamaan segitiga memberi Jadi jumlah kuadrat koordinat kurang daripada , sehingga . Dengan demikian , dan menurut definisi merupakan lingkungan dari .  "
},
{
  "id": "o003-c90-ch07-exercise-task-02",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-a.html#o003-c90-ch07-exercise-task-02",
  "type": "Pemeriksaan",
  "number": "G.18",
  "title": "Sumbu horizontal dalam metrik taksi.",
  "body": "Sumbu horizontal dalam metrik taksi  Dalam , misalkan adalah sumbu dan . Tentukan, disertai bukti, apakah merupakan lingkungan dari . Rubrik. Jika jawabannya negatif, untuk setiap radius positif berikan titik di dalam bola yang tidak berada pada sumbu .   Untuk , periksa titik dan hitung .   Tidak. Setiap bola memuat titik , yang tidak berada pada sumbu .   Ambil sebarang dan tetapkan . Jarak taksi dari ke adalah Maka . Akan tetapi, koordinat kedua tidak nol, sehingga . Jadi tidak ada dengan . Oleh karena itu, bukan lingkungan dari .  "
},
{
  "id": "o003-c90-ch07-exercise-task-03",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-a.html#o003-c90-ch07-exercise-task-03",
  "type": "Pemeriksaan",
  "number": "G.19",
  "title": "Bilangan rasional bukan lingkungan di garis real.",
  "body": "Bilangan rasional bukan lingkungan di garis real  Dalam , misalkan dan . Tentukan, disertai bukti, apakah merupakan lingkungan dari . Rubrik. Gunakan urutan kuantor dalam definisi lingkungan dan sifat kerapatan bilangan irasional.   Setiap interval terbuka memuat bilangan irasional.   Tidak. Untuk setiap , bola memuat suatu bilangan irasional dan karenanya tidak termuat dalam .   Misalkan diberikan. Kerapatan bilangan irasional dalam menjamin adanya dengan . Dengan demikian , sehingga , tetapi . Argumen ini berlaku untuk setiap radius positif, sehingga tidak ada bola terbuka berpusat di yang termuat dalam . Jadi bukan lingkungan dari dalam metrik Euklides.  "
},
{
  "id": "o003-c90-ch07-exercise-task-04",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-a.html#o003-c90-ch07-exercise-task-04",
  "type": "Pemeriksaan",
  "number": "G.20",
  "title": "Bilangan bulat positif dalam metrik pecahan tereduksi.",
  "body": "Bilangan bulat positif dalam metrik pecahan tereduksi  Misalkan adalah himpunan bilangan rasional dalam bentuk paling sederhana dan . Dalam , tentukan apakah himpunan semua bilangan bulat positif merupakan lingkungan dari . Rubrik. Tentukan bola terbuka berjari-jari di sekitar dan jelaskan peran koordinat pembilang serta penyebut yang bulat.   Jika dua pecahan tereduksi berbeda, setidaknya salah satu dari selisih pembilang dan selisih penyebutnya adalah bilangan bulat tak nol.   Ya. Bola hanya berisi , sehingga bola itu termuat dalam himpunan bilangan bulat positif.   Ambil dalam bentuk paling sederhana. Jika , pasangan bilangan bulat berbeda dari . Maka paling sedikit satu dari dan merupakan bilangan bulat positif, sehingga Akibatnya, syarat hanya dipenuhi oleh . Jadi . Karena memuat bola terbuka berpusat di , merupakan lingkungan dari .  "
},
{
  "id": "o003-c90-ch07-exercise-task-05",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-a.html#o003-c90-ch07-exercise-task-05",
  "type": "Pemeriksaan",
  "number": "G.21",
  "title": "Semua fungsi dari ruang metrik berhingga ini kontinu.",
  "body": "Semua fungsi dari ruang metrik berhingga ini kontinu  Misalkan dan , yakni sisa pembagian oleh . Untuk sebarang ruang metrik , tentukan apakah mungkin mendefinisikan fungsi yang tidak kontinu. Rubrik. Hitung jarak antar-titik berbeda dan berikan satu radius yang mengisolasi setiap titik domain.   Jarak antartitik berbeda adalah , , dan . Apa isi untuk ?   Tidak mungkin. Setiap fungsi kontinu; radius mengisolasi setiap titik .   Perhitungan modulo memberikan , , dan . Jadi untuk setiap , tidak ada titik lain yang berjarak kurang daripada dari ; dengan kata lain, .  Sekarang ambil fungsi sebarang , titik , dan . Pilih . Jika , maka , sehingga Jadi kontinu di setiap titik dalam . Tidak ada fungsi tak kontinu dari domain ini ke ruang metrik mana pun.  "
},
{
  "id": "o003-c90-ch07-exercise-task-06",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-a.html#o003-c90-ch07-exercise-task-06",
  "type": "Pemeriksaan",
  "number": "G.22",
  "title": "Dua fungsi pada ruang bermetrik pusat.",
  "body": "Dua fungsi pada ruang bermetrik pusat  Pada , dengan jika dan jika , definisikan oleh , untuk , serta jika dan selain itu. Tentukan fungsi mana yang kontinu dan buktikan kedua klaim. Rubrik. Periksa titik asal secara terpisah; untuk titik tak nol, tunjukkan bahwa terdapat bola terbuka yang hanya memuat pusatnya.    Langkah 1. Untuk setiap , berlaku .   Langkah 2. Di titik asal, bandingkan perilaku dan pada titik-titik tak nol yang normanya menuju nol.   Fungsi tidak kontinu di , sedangkan kontinu pada seluruh . Untuk di , radius bekerja; semua titik tak nol terisolasi.   Untuk menunjukkan bahwa tidak kontinu di , tetapkan . Diberikan sebarang , pilih . Maka dan Ini adalah negasi definisi kekontinuan, sehingga tidak kontinu.  Untuk di titik asal, pilih bagi sebarang . Jika , maka , sehingga dan jarak keluarannya nol. Jadi kontinu di .  Terakhir, jika , maka untuk setiap berlaku . Karena itu . Untuk setiap , pilihan memaksa dan karenanya . Maka kontinu di setiap titik tak nol juga, sehingga kontinu pada seluruh .  "
},
{
  "id": "o003-c90-ch07-exercise-task-07",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-a.html#o003-c90-ch07-exercise-task-07",
  "type": "Pemeriksaan",
  "number": "G.23",
  "title": "Semua bola terbuka pada graf berbobot.",
  "body": "Semua bola terbuka pada graf berbobot  Pada ruang metrik graf berbobot dengan sisi , , , , , , , dan , tentukan untuk setiap . Rubrik. Hitung dahulu jarak lintasan terpendek dari ke kelima simpul, lalu pisahkan semua rentang radius pada nilai jarak kritis.   Jarak dari ke , berturut-turut, adalah . Ingat bahwa bola terbuka memakai pertidaksamaan ketat .   Bola-bolanya adalah untuk ; untuk ; untuk ; untuk ; dan untuk .   Jalankan langkah jarak terpendek dari . Mula-mula diperoleh jarak tentatif , , dan dari sisi-sisi yang bersisian dengan . Melalui , jarak ke tetap , jarak ke menjadi , dan jarak ke tetap . Melalui , kandidat jarak ke adalah , sehingga tidak memperbaiki . Melalui , kandidat jarak ke adalah , sama dengan jarak yang sudah diperoleh. Karena semua bobot sisi positif, langkah-langkah ini menyelesaikan pemeriksaan lintasan terpendek. Jadi jarak dari ke , berturut-turut, adalah .  Sebuah simpul masuk ke tepat ketika jaraknya kurang daripada . Karena ketaksamaan ini ketat, simpul pada jarak baru masuk setelah radius melewati nilai tersebut. Dengan demikian   "
},
{
  "id": "o003-c90-ch07-exercise-task-08",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-a.html#o003-c90-ch07-exercise-task-08",
  "type": "Pemeriksaan",
  "number": "G.24",
  "title": "Semua lingkungan dari simpul a.",
  "body": "Semua lingkungan dari simpul a  Untuk ruang metrik graf berbobot pada tugas sebelumnya, tentukan semua lingkungan dari . Rubrik. Gunakan bola terbuka terkecil yang ditemukan dan buktikan kedua arah klasifikasi.   Karena , setiap subhimpunan yang memuat otomatis memuat sebuah bola terbuka berpusat di .   Lingkungan dari tepat merupakan semua subhimpunan yang memuat .   Jika merupakan lingkungan dari , maka ada dengan . Setiap bola berpusat di memuat pusatnya, sehingga .  Sebaliknya, andaikan . Dari perhitungan tugas sebelumnya, . Maka , sehingga menurut definisi merupakan lingkungan dari . Kedua arah ini membuktikan klasifikasi tersebut.  "
},
{
  "id": "o003-c90-ch07-exercise-task-09",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-a.html#o003-c90-ch07-exercise-task-09",
  "type": "Pemeriksaan",
  "number": "G.25",
  "title": "Prapeta bola di bawah fungsi linear.",
  "body": "Prapeta bola di bawah fungsi linear  Misalkan didefinisikan oleh , dengan . Untuk dan , tunjukkan bahwa memuat bola terbuka berpusat di , lalu simpulkan kekontinuan fungsi linear. Rubrik. Hitung selisih dan berikan radius eksplisit dalam dan .   Gunakan dan pilih .   Berlaku . Maka pilihan membuktikan kekontinuan di setiap .   Untuk setiap , Karena , radius positif. Kita mempunyai rangkaian kesetaraan Jadi prapeta tersebut bukan hanya memuat, melainkan sama dengan bola yang dinyatakan. Karena konstruksi ini berlaku bagi setiap dan , kontinu. Jika istilah fungsi linear juga mencakup kasus , kasus itu adalah fungsi konstan dan juga kontinu.  "
},
{
  "id": "o003-c90-ch07-exercise-task-10",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-a.html#o003-c90-ch07-exercise-task-10",
  "type": "Pemeriksaan",
  "number": "G.26",
  "title": "Prapeta bola di bawah fungsi kuadrat.",
  "body": "Prapeta bola di bawah fungsi kuadrat  Misalkan didefinisikan oleh , dengan . Untuk dan , tunjukkan bahwa memuat bola terbuka berpusat di , lalu simpulkan bahwa setiap fungsi kuadrat kontinu. Rubrik. Faktorkan selisih nilai fungsi, batasi di sekitar , dan berikan radius eksplisit.    Langkah 1. Gunakan .   Langkah 2. Tetapkan dan pilih .   Dengan , radius memenuhi . Jadi kontinu di setiap .   Karena , bilangan positif. Tetapkan . Jika , maka , sehingga dan . Oleh karena itu, Jadi setiap kali . Ini membuktikan . Karena dan dipilih sembarang, kontinu pada .  "
},
{
  "id": "o003-c90-ch07-exercise-task-11",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-a.html#o003-c90-ch07-exercise-task-11",
  "type": "Pemeriksaan",
  "number": "G.27",
  "title": "Fungsi jarak ke suatu himpunan.",
  "body": "Fungsi jarak ke suatu himpunan  Misalkan ruang metrik dan tak kosong. Definisikan dengan . Gunakan untuk menunjukkan bahwa, bagi setiap dan , terdapat lingkungan dari dengan . Simpulkan bahwa kontinu. Rubrik. Turunkan batas simetris untuk selisih mutlak dua jarak ke , lalu pilih lingkungan secara eksplisit.   Tukarkan dan dalam pertidaksamaan yang diberikan, lalu gabungkan kedua hasil untuk memperoleh pertidaksamaan 1-Lipschitz.   Berlaku . Karena itu memenuhi syarat, dan bahkan 1-Lipschitz.   Pertidaksamaan yang diberikan menyatakan . Setelah dan ditukar, simetri metrik memberi . Kedua pertidaksamaan itu setara dengan   Tetapkan dan , lalu ambil . Jika , maka Dengan demikian . Karena ini berlaku untuk setiap dan , fungsi kontinu; batas pertama juga menunjukkan bahwa konstanta Lipschitz-nya paling besar .  "
},
{
  "id": "o003-c90-ch07-exercise-task-12",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-a.html#o003-c90-ch07-exercise-task-12",
  "type": "Pemeriksaan",
  "number": "G.28",
  "title": "Lingkungan terpisah bagi dua titik berbeda.",
  "body": "Lingkungan terpisah bagi dua titik berbeda  Misalkan dan dua titik berbeda dalam ruang metrik . Buktikan bahwa terdapat lingkungan dan , masing-masing dari dan , dengan . Rubrik. Pilih radius berdasarkan dan gunakan pertidaksamaan segitiga untuk membuktikan ketakteririsan.   Karena , bilangan positif. Cobalah dan .   Ambil , , dan . Kedua bola terbuka itu merupakan lingkungan dan tidak beririsan.   Karena , sifat definit positif metrik memberi . Tetapkan dan ambil serta . Masing-masing jelas merupakan lingkungan dari pusatnya.  Andaikan, untuk memperoleh kontradiksi, ada . Maka dan . Pertidaksamaan segitiga memberikan suatu kontradiksi. Jadi , sebagaimana diminta.  "
},
{
  "id": "o003-c90-ch07-exercise-guides-b",
  "level": "1",
  "url": "o003-c90-ch07-exercise-guides-b.html",
  "type": "Bagian",
  "number": "",
  "title": "Panduan latihan sumber, bagian kedua",
  "body": " Panduan latihan sumber, bagian kedua  Dua belas panduan berikut berkorespondensi dengan perintah ke-13 sampai ke-24 pada bagian latihan Bab 7 menurut urutan kedalaman sumber. Materi pendamping ini merupakan uraian asli untuk pembelajaran mandiri, bukan jawaban yang disediakan oleh penulis karya sumber.  Keberadaan lingkungan yang memuat pusatnya  Misalkan ruang metrik dan . Buktikan bahwa terdapat suatu lingkungan yang memuat . Rubrik. Berikan satu himpunan konkret, tunjukkan bahwa himpunan itu memuat bola terbuka berpusat di , dan periksa bahwa sendiri berada di dalamnya.   Bola terbuka memuat dirinya sendiri dan selalu memuat pusat .   Himpunan adalah lingkungan dari yang memuat .   Ambil . Karena , definisi lingkungan langsung menunjukkan bahwa merupakan lingkungan dari . Selain itu, , sehingga . Jadi lingkungan yang diminta selalu ada.   Himpunan yang lebih besar tetap merupakan lingkungan  Misalkan merupakan lingkungan dari dan . Buktikan bahwa juga merupakan lingkungan dari . Rubrik. Mulailah dari bola yang dijamin oleh definisi lingkungan bagi , lalu gunakan transitivitas inklusi.   Ada dengan . Gabungkan inklusi ini dengan .   Benar. Bola yang membuktikan bahwa merupakan lingkungan juga termuat dalam .   Karena merupakan lingkungan dari , terdapat sedemikian sehingga . Hipotesis kemudian memberi Jadi memuat sebuah bola terbuka berpusat di . Menurut definisi, merupakan lingkungan dari .   Irisan dua lingkungan  Misalkan dan merupakan lingkungan dari . Buktikan bahwa juga merupakan lingkungan dari . Rubrik. Nyatakan radius yang disediakan oleh masing-masing lingkungan dan gabungkan keduanya dengan operasi minimum.   Jika dan , pilih .   Benar. Bola termuat dalam .   Karena dan merupakan lingkungan dari , terdapat dengan dan . Tetapkan , yang tetap positif. Jika , maka dan . Jadi dan , sehingga . Maka irisan tersebut merupakan lingkungan dari .   Kepositifan bertahan di sekitar suatu titik  Misalkan kontinu dan untuk suatu . Buktikan bahwa terdapat lingkungan dari sedemikian sehingga untuk semua . Rubrik. Pilih toleransi keluaran sebagai fraksi eksplisit dari dan turunkan batas bawah positif bagi .   Terapkan kekontinuan di dengan .   Ambil . Radius kekontinuan yang sesuai menghasilkan lingkungan dengan bagi semua .   Karena , bilangan positif. Kekontinuan di memberikan sedemikian sehingga mengakibatkan . Tetapkan , yang merupakan lingkungan dari . Untuk setiap , Jadi tetap positif di seluruh lingkungan .   Subhimpunan ruang diskret  Misalkan ruang metrik dengan sebagai metrik diskret. Buktikan bahwa setiap subhimpunan merupakan lingkungan dari setiap titiknya. Rubrik. Tetapkan titik sebarang , tentukan sebuah bola yang hanya memuat , dan bahas kasus .   Dalam metrik diskret, .   Benar. Untuk setiap , berlaku . Jika kosong, pernyataannya benar secara hampa.   Jika , tidak ada titik yang perlu diperiksa. Jika tidak kosong, tetapkan sebarang . Pada metrik diskret, bernilai ketika dan ketika . Karena bola terbuka memakai pertidaksamaan ketat, . Maka , sehingga merupakan lingkungan dari . Karena sebarang, klaim berlaku bagi setiap titik dalam .   Bola di dalam lingkungan belum tentu berpusat tepat  Putuskan benar atau salah: jika merupakan lingkungan dari dalam ruang metrik , maka setiap bola terbuka yang termuat dalam juga merupakan lingkungan dari . Rubrik. Jika salah, berikan ruang, titik, lingkungan, dan bola terbuka konkret; verifikasi inklusi serta kegagalan sifat lingkungan.   Dalam , sebuah lingkungan dari dapat memuat bola kecil yang berpusat jauh dari dan bahkan tidak memuat .   Salah. Dalam , ambil , , dan bola . Bola itu termuat dalam , tetapi bukan lingkungan dari .   Dalam , himpunan merupakan lingkungan dari , misalnya karena . Bola terbuka memenuhi .  Akan tetapi, . Setiap lingkungan dari harus memuat , sebab setiap bola terbuka berpusat di memuat pusatnya. Jadi bukan lingkungan dari . Contoh ini membantah pernyataan universal tersebut.   Lingkungan dari satu titik belum tentu terbuka  Putuskan benar atau salah: jika merupakan lingkungan dari dalam ruang metrik , maka merupakan lingkungan dari setiap titiknya. Rubrik. Jika salah, buat himpunan yang memuat satu interval terbuka di sekitar dan satu titik tambahan yang tidak mempunyai ruang terbuka di dalam himpunan itu.   Pertimbangkan dalam , dengan .   Salah. Himpunan merupakan lingkungan dari , tetapi bukan lingkungan dari titiknya .   Dalam , ambil . Karena , himpunan merupakan lingkungan dari . Selain itu, .  Untuk sebarang , tetapkan dan . Maka , tetapi dan , sehingga . Jadi tidak ada bola terbuka berpusat di yang termuat dalam . Dengan demikian bukan lingkungan dari .   Citra lingkungan di bawah fungsi kontinu  Putuskan benar atau salah: jika ruang-ruang metrik, kontinu, dan merupakan lingkungan dari , maka merupakan lingkungan dari dalam . Rubrik. Jika salah, pilih fungsi kontinu yang meruntuhkan seluruh lingkungan menjadi sebuah himpunan yang terlalu kecil.   Gunakan fungsi konstan dan sebuah interval terbuka sebagai .   Salah. Untuk fungsi konstan dan , berlaku , yang bukan lingkungan dari dalam garis real bermetrik Euklides.   Ambil dengan metrik Euklides, definisikan fungsi konstan , dan pilih serta . Fungsi konstan kontinu, dan merupakan lingkungan dari .  Namun . Untuk setiap , bola memuat titik , sehingga tidak termuat dalam . Jadi bukan lingkungan dari . Kekontinuan tidak menjamin bahwa citra lingkungan merupakan lingkungan.   Prapeta lingkungan di bawah fungsi yang kontinu di titik  Putuskan benar atau salah: jika ruang-ruang metrik, kontinu di , dan merupakan lingkungan dari , maka merupakan lingkungan dari . Rubrik. Mulailah dari bola yang termuat dalam dan terapkan definisi kekontinuan dengan radius bola tersebut sebagai toleransi keluaran.   Pilih dengan , lalu gunakan kekontinuan untuk memperoleh .   Benar. Kekontinuan menghasilkan .   Karena merupakan lingkungan dari , ada dengan . Kekontinuan di memberikan sedemikian sehingga mengakibatkan .  Jadi, jika , maka , sehingga . Dengan demikian . Prapeta tersebut memuat bola terbuka berpusat di , sehingga merupakan lingkungan dari .   Bola terbuka belum tentu memuat tak berhingga banyak titik  Putuskan benar atau salah: jika suatu titik dalam ruang metrik dan , maka bola terbuka memuat tak berhingga banyak titik dari . Rubrik. Jika salah, berikan ruang metrik eksplisit, pusat, dan radius positif, lalu hitung bolanya.   Gunakan himpunan berhingga dengan metrik diskret dan radius .   Salah. Dalam dengan metrik diskret, , yang hanya memuat satu titik.   Ambil dan metrik diskret jika , serta jika . Untuk dan , titik berada dalam tepat ketika . Hanya yang memenuhi syarat ini; tidak kurang dari . Jadi , suatu himpunan berhingga. Contoh ini membantah pernyataan tersebut.   Irisan berhingga lingkungan  Putuskan benar atau salah: jika merupakan lingkungan dari dalam ruang metrik untuk suatu bilangan bulat positif , maka merupakan lingkungan dari . Rubrik. Pilih satu radius positif untuk setiap lingkungan, lalu gunakan minimum dari himpunan radius yang berhingga.   Jika untuk , tetapkan .   Benar. Radius minimum memenuhi .   Untuk setiap , karena merupakan lingkungan dari , pilih sehingga . Himpunan berhingga dan tak kosong, sehingga ada dan positif.  Jika , maka untuk setiap berlaku . Jadi bagi semua . Karena itu , yang membuktikan bahwa irisan tersebut merupakan lingkungan dari .   Irisan sebarang keluarga lingkungan  Putuskan benar atau salah: jika merupakan lingkungan dari dalam ruang metrik untuk setiap dalam suatu himpunan indeks , maka merupakan lingkungan dari . Rubrik. Jika salah, gunakan keluarga terhitung lingkungan yang radiusnya menuju nol, hitung irisannya, dan buktikan bahwa irisan itu tidak memuat bola terbuka beradius positif.   Dalam , ambil untuk setiap bilangan bulat positif .   Salah. Setiap merupakan lingkungan dari , tetapi , yang bukan lingkungan dari dalam metrik Euklides.   Dalam , untuk setiap bilangan bulat positif , himpunan merupakan lingkungan dari . Titik berada dalam semua . Sebaliknya, jika , sifat Archimedes memberi bilangan bulat positif dengan . Maka , sehingga . Jadi   Himpunan bukan lingkungan dari : untuk setiap , titik berada dalam tetapi tidak berada dalam . Jadi irisan tak berhingga dari lingkungan-lingkungan tidak harus merupakan lingkungan.   "
},
{
  "id": "o003-c90-ch07-exercise-task-13",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-b.html#o003-c90-ch07-exercise-task-13",
  "type": "Pemeriksaan",
  "number": "G.29",
  "title": "Keberadaan lingkungan yang memuat pusatnya.",
  "body": "Keberadaan lingkungan yang memuat pusatnya  Misalkan ruang metrik dan . Buktikan bahwa terdapat suatu lingkungan yang memuat . Rubrik. Berikan satu himpunan konkret, tunjukkan bahwa himpunan itu memuat bola terbuka berpusat di , dan periksa bahwa sendiri berada di dalamnya.   Bola terbuka memuat dirinya sendiri dan selalu memuat pusat .   Himpunan adalah lingkungan dari yang memuat .   Ambil . Karena , definisi lingkungan langsung menunjukkan bahwa merupakan lingkungan dari . Selain itu, , sehingga . Jadi lingkungan yang diminta selalu ada.  "
},
{
  "id": "o003-c90-ch07-exercise-task-14",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-b.html#o003-c90-ch07-exercise-task-14",
  "type": "Pemeriksaan",
  "number": "G.30",
  "title": "Himpunan yang lebih besar tetap merupakan lingkungan.",
  "body": "Himpunan yang lebih besar tetap merupakan lingkungan  Misalkan merupakan lingkungan dari dan . Buktikan bahwa juga merupakan lingkungan dari . Rubrik. Mulailah dari bola yang dijamin oleh definisi lingkungan bagi , lalu gunakan transitivitas inklusi.   Ada dengan . Gabungkan inklusi ini dengan .   Benar. Bola yang membuktikan bahwa merupakan lingkungan juga termuat dalam .   Karena merupakan lingkungan dari , terdapat sedemikian sehingga . Hipotesis kemudian memberi Jadi memuat sebuah bola terbuka berpusat di . Menurut definisi, merupakan lingkungan dari .  "
},
{
  "id": "o003-c90-ch07-exercise-task-15",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-b.html#o003-c90-ch07-exercise-task-15",
  "type": "Pemeriksaan",
  "number": "G.31",
  "title": "Irisan dua lingkungan.",
  "body": "Irisan dua lingkungan  Misalkan dan merupakan lingkungan dari . Buktikan bahwa juga merupakan lingkungan dari . Rubrik. Nyatakan radius yang disediakan oleh masing-masing lingkungan dan gabungkan keduanya dengan operasi minimum.   Jika dan , pilih .   Benar. Bola termuat dalam .   Karena dan merupakan lingkungan dari , terdapat dengan dan . Tetapkan , yang tetap positif. Jika , maka dan . Jadi dan , sehingga . Maka irisan tersebut merupakan lingkungan dari .  "
},
{
  "id": "o003-c90-ch07-exercise-task-16",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-b.html#o003-c90-ch07-exercise-task-16",
  "type": "Pemeriksaan",
  "number": "G.32",
  "title": "Kepositifan bertahan di sekitar suatu titik.",
  "body": "Kepositifan bertahan di sekitar suatu titik  Misalkan kontinu dan untuk suatu . Buktikan bahwa terdapat lingkungan dari sedemikian sehingga untuk semua . Rubrik. Pilih toleransi keluaran sebagai fraksi eksplisit dari dan turunkan batas bawah positif bagi .   Terapkan kekontinuan di dengan .   Ambil . Radius kekontinuan yang sesuai menghasilkan lingkungan dengan bagi semua .   Karena , bilangan positif. Kekontinuan di memberikan sedemikian sehingga mengakibatkan . Tetapkan , yang merupakan lingkungan dari . Untuk setiap , Jadi tetap positif di seluruh lingkungan .  "
},
{
  "id": "o003-c90-ch07-exercise-task-17",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-b.html#o003-c90-ch07-exercise-task-17",
  "type": "Pemeriksaan",
  "number": "G.33",
  "title": "Subhimpunan ruang diskret.",
  "body": "Subhimpunan ruang diskret  Misalkan ruang metrik dengan sebagai metrik diskret. Buktikan bahwa setiap subhimpunan merupakan lingkungan dari setiap titiknya. Rubrik. Tetapkan titik sebarang , tentukan sebuah bola yang hanya memuat , dan bahas kasus .   Dalam metrik diskret, .   Benar. Untuk setiap , berlaku . Jika kosong, pernyataannya benar secara hampa.   Jika , tidak ada titik yang perlu diperiksa. Jika tidak kosong, tetapkan sebarang . Pada metrik diskret, bernilai ketika dan ketika . Karena bola terbuka memakai pertidaksamaan ketat, . Maka , sehingga merupakan lingkungan dari . Karena sebarang, klaim berlaku bagi setiap titik dalam .  "
},
{
  "id": "o003-c90-ch07-exercise-task-18",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-b.html#o003-c90-ch07-exercise-task-18",
  "type": "Pemeriksaan",
  "number": "G.34",
  "title": "Bola di dalam lingkungan belum tentu berpusat tepat.",
  "body": "Bola di dalam lingkungan belum tentu berpusat tepat  Putuskan benar atau salah: jika merupakan lingkungan dari dalam ruang metrik , maka setiap bola terbuka yang termuat dalam juga merupakan lingkungan dari . Rubrik. Jika salah, berikan ruang, titik, lingkungan, dan bola terbuka konkret; verifikasi inklusi serta kegagalan sifat lingkungan.   Dalam , sebuah lingkungan dari dapat memuat bola kecil yang berpusat jauh dari dan bahkan tidak memuat .   Salah. Dalam , ambil , , dan bola . Bola itu termuat dalam , tetapi bukan lingkungan dari .   Dalam , himpunan merupakan lingkungan dari , misalnya karena . Bola terbuka memenuhi .  Akan tetapi, . Setiap lingkungan dari harus memuat , sebab setiap bola terbuka berpusat di memuat pusatnya. Jadi bukan lingkungan dari . Contoh ini membantah pernyataan universal tersebut.  "
},
{
  "id": "o003-c90-ch07-exercise-task-19",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-b.html#o003-c90-ch07-exercise-task-19",
  "type": "Pemeriksaan",
  "number": "G.35",
  "title": "Lingkungan dari satu titik belum tentu terbuka.",
  "body": "Lingkungan dari satu titik belum tentu terbuka  Putuskan benar atau salah: jika merupakan lingkungan dari dalam ruang metrik , maka merupakan lingkungan dari setiap titiknya. Rubrik. Jika salah, buat himpunan yang memuat satu interval terbuka di sekitar dan satu titik tambahan yang tidak mempunyai ruang terbuka di dalam himpunan itu.   Pertimbangkan dalam , dengan .   Salah. Himpunan merupakan lingkungan dari , tetapi bukan lingkungan dari titiknya .   Dalam , ambil . Karena , himpunan merupakan lingkungan dari . Selain itu, .  Untuk sebarang , tetapkan dan . Maka , tetapi dan , sehingga . Jadi tidak ada bola terbuka berpusat di yang termuat dalam . Dengan demikian bukan lingkungan dari .  "
},
{
  "id": "o003-c90-ch07-exercise-task-20",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-b.html#o003-c90-ch07-exercise-task-20",
  "type": "Pemeriksaan",
  "number": "G.36",
  "title": "Citra lingkungan di bawah fungsi kontinu.",
  "body": "Citra lingkungan di bawah fungsi kontinu  Putuskan benar atau salah: jika ruang-ruang metrik, kontinu, dan merupakan lingkungan dari , maka merupakan lingkungan dari dalam . Rubrik. Jika salah, pilih fungsi kontinu yang meruntuhkan seluruh lingkungan menjadi sebuah himpunan yang terlalu kecil.   Gunakan fungsi konstan dan sebuah interval terbuka sebagai .   Salah. Untuk fungsi konstan dan , berlaku , yang bukan lingkungan dari dalam garis real bermetrik Euklides.   Ambil dengan metrik Euklides, definisikan fungsi konstan , dan pilih serta . Fungsi konstan kontinu, dan merupakan lingkungan dari .  Namun . Untuk setiap , bola memuat titik , sehingga tidak termuat dalam . Jadi bukan lingkungan dari . Kekontinuan tidak menjamin bahwa citra lingkungan merupakan lingkungan.  "
},
{
  "id": "o003-c90-ch07-exercise-task-21",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-b.html#o003-c90-ch07-exercise-task-21",
  "type": "Pemeriksaan",
  "number": "G.37",
  "title": "Prapeta lingkungan di bawah fungsi yang kontinu di titik.",
  "body": "Prapeta lingkungan di bawah fungsi yang kontinu di titik  Putuskan benar atau salah: jika ruang-ruang metrik, kontinu di , dan merupakan lingkungan dari , maka merupakan lingkungan dari . Rubrik. Mulailah dari bola yang termuat dalam dan terapkan definisi kekontinuan dengan radius bola tersebut sebagai toleransi keluaran.   Pilih dengan , lalu gunakan kekontinuan untuk memperoleh .   Benar. Kekontinuan menghasilkan .   Karena merupakan lingkungan dari , ada dengan . Kekontinuan di memberikan sedemikian sehingga mengakibatkan .  Jadi, jika , maka , sehingga . Dengan demikian . Prapeta tersebut memuat bola terbuka berpusat di , sehingga merupakan lingkungan dari .  "
},
{
  "id": "o003-c90-ch07-exercise-task-22",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-b.html#o003-c90-ch07-exercise-task-22",
  "type": "Pemeriksaan",
  "number": "G.38",
  "title": "Bola terbuka belum tentu memuat tak berhingga banyak titik.",
  "body": "Bola terbuka belum tentu memuat tak berhingga banyak titik  Putuskan benar atau salah: jika suatu titik dalam ruang metrik dan , maka bola terbuka memuat tak berhingga banyak titik dari . Rubrik. Jika salah, berikan ruang metrik eksplisit, pusat, dan radius positif, lalu hitung bolanya.   Gunakan himpunan berhingga dengan metrik diskret dan radius .   Salah. Dalam dengan metrik diskret, , yang hanya memuat satu titik.   Ambil dan metrik diskret jika , serta jika . Untuk dan , titik berada dalam tepat ketika . Hanya yang memenuhi syarat ini; tidak kurang dari . Jadi , suatu himpunan berhingga. Contoh ini membantah pernyataan tersebut.  "
},
{
  "id": "o003-c90-ch07-exercise-task-23",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-b.html#o003-c90-ch07-exercise-task-23",
  "type": "Pemeriksaan",
  "number": "G.39",
  "title": "Irisan berhingga lingkungan.",
  "body": "Irisan berhingga lingkungan  Putuskan benar atau salah: jika merupakan lingkungan dari dalam ruang metrik untuk suatu bilangan bulat positif , maka merupakan lingkungan dari . Rubrik. Pilih satu radius positif untuk setiap lingkungan, lalu gunakan minimum dari himpunan radius yang berhingga.   Jika untuk , tetapkan .   Benar. Radius minimum memenuhi .   Untuk setiap , karena merupakan lingkungan dari , pilih sehingga . Himpunan berhingga dan tak kosong, sehingga ada dan positif.  Jika , maka untuk setiap berlaku . Jadi bagi semua . Karena itu , yang membuktikan bahwa irisan tersebut merupakan lingkungan dari .  "
},
{
  "id": "o003-c90-ch07-exercise-task-24",
  "level": "2",
  "url": "o003-c90-ch07-exercise-guides-b.html#o003-c90-ch07-exercise-task-24",
  "type": "Pemeriksaan",
  "number": "G.40",
  "title": "Irisan sebarang keluarga lingkungan.",
  "body": "Irisan sebarang keluarga lingkungan  Putuskan benar atau salah: jika merupakan lingkungan dari dalam ruang metrik untuk setiap dalam suatu himpunan indeks , maka merupakan lingkungan dari . Rubrik. Jika salah, gunakan keluarga terhitung lingkungan yang radiusnya menuju nol, hitung irisannya, dan buktikan bahwa irisan itu tidak memuat bola terbuka beradius positif.   Dalam , ambil untuk setiap bilangan bulat positif .   Salah. Setiap merupakan lingkungan dari , tetapi , yang bukan lingkungan dari dalam metrik Euklides.   Dalam , untuk setiap bilangan bulat positif , himpunan merupakan lingkungan dari . Titik berada dalam semua . Sebaliknya, jika , sifat Archimedes memberi bilangan bulat positif dengan . Maka , sehingga . Jadi   Himpunan bukan lingkungan dari : untuk setiap , titik berada dalam tetapi tidak berada dalam . Jadi irisan tak berhingga dari lingkungan-lingkungan tidak harus merupakan lingkungan.  "
},
{
  "id": "o003-c90-ch07-mastery",
  "level": "1",
  "url": "o003-c90-ch07-mastery.html",
  "type": "Bagian",
  "number": "",
  "title": "Pemeriksaan penguasaan Bab 7",
  "body": " Pemeriksaan penguasaan Bab 7  Enam soal berikut menggabungkan geometri bola, lingkungan, kekontinuan, dan contoh penyangkal. Setiap soal merupakan materi asli pendamping. Cobalah menyusun bukti lengkap sebelum membuka bantuan bertahap.  Empat metrik dan empat bentuk bola  Pada , gambarkan dan nyatakan dengan pertidaksamaan bola berjari-jari yang berpusat di untuk metrik Euklides , metrik maksimum , metrik taksi , dan metrik diskret . Buktikan bahwa    Tuliskan syarat jarak kurang dari untuk setiap metrik. Untuk inklusi, gunakan . Untuk ketatnya inklusi, uji titik pada sumbu, lalu titik dan .   Untuk bolanya ialah cakram ; untuk , persegi terbuka ; untuk , belah ketupat ; dan untuk , singleton . Semua inklusi yang ditampilkan bersifat ketat.   Dari definisi masing-masing metrik diperoleh Untuk setiap , berlaku . Karena itu, syarat norma satu kurang dari mengakibatkan syarat norma dua, dan syarat norma dua mengakibatkan syarat norma maksimum. Bola diskret jelas termuat dalam semuanya.  Inklusinya ketat: berada dalam bola taksi tetapi bukan dalam bola diskret; berada dalam bola Euklides karena , tetapi tidak dalam bola taksi karena ; dan berada dalam bola maksimum, tetapi tidak dalam bola Euklides karena .   Ruang yang tersisa di dalam bola terbuka  Misalkan suatu ruang metrik, , dan . Nyatakan jari-jari residu alami yang berpusat di , buktikan bahwa jari-jari tersebut positif, lalu buktikan bahwa bola yang dihasilkannya termuat dalam .   Ukur bagian jari-jari yang belum dipakai oleh jarak . Untuk titik dalam bola baru, terapkan pertidaksamaan segitiga pada dan pertahankan pertidaksamaan ketatnya.   Ambil . Karena , berlaku , dan .   Keanggotaan berarti , sehingga . Jika , maka Jadi . Karena dipilih sebarang, . Inilah alasan setiap bola terbuka merupakan lingkungan bagi setiap titiknya.   Tiga bentuk yang setara untuk kekontinuan  Untuk fungsi dan , buktikan kesetaraan ketiga syarat berikut: definisi epsilon-delta; untuk setiap terdapat dengan ; dan prapeta setiap lingkungan bagi merupakan lingkungan bagi . Kemudian gunakan di untuk menjelaskan mengapa prapeta bola tidak harus menjadi bola yang berpusat di .   Kesetaraan dua syarat pertama hanyalah penerjemahan keanggotaan bola. Untuk lingkungan umum, sisipkan sebuah bola di dalam lingkungan. Untuk arah sebaliknya, gunakan fakta bahwa merupakan lingkungan bagi pusatnya. Pada contoh konkret, selesaikan .   Ketiga syarat setara. Untuk , , yang bukan satu interval dan karena itu bukan bola Euklides yang berpusat di .   Untuk , keanggotaan tepat berarti , sedangkan tepat berarti . Jadi implikasi epsilon-delta untuk semua setara tepat dengan inklusi kedua bola tersebut.  Andaikan syarat inklusi bola berlaku dan suatu lingkungan bagi . Ada dengan . Pilih dari syarat inklusi. Maka sehingga merupakan lingkungan bagi .  Sebaliknya, andaikan sifat prapeta lingkungan berlaku. Untuk , bola merupakan lingkungan bagi . Prapetanya karena itu merupakan lingkungan bagi , sehingga memuat untuk suatu . Ini menghasilkan syarat inklusi bola dan menutup siklus kesetaraan.  Pada contoh , bola sasaran ialah . Menyelesaikan memberi dua interval terpisah . Prapeta ini memuat bola kecil di sekitar , tetapi bukan dirinya sendiri sebuah bola yang berpusat di .   Metrik graf berhingga yang lengkap  Ambil lintasan berbobot dengan bobot sisi berturut-turut , dan definisikan jarak sebagai panjang lintasan terpendek. Daftarkan semua bola berbeda untuk , cirikan semua lingkungan bagi , lalu buktikan bahwa setiap fungsi dari ruang ini ke sembarang ruang metrik bersifat kontinu.   Hitung dahulu dan ingat bahwa syarat bola adalah jarak kurang dari jari-jari. Untuk kekontinuan, cari bola singleton di setiap simpul.   Jarak dari ialah . Bola-bolanya adalah untuk , untuk , untuk , dan seluruh ruang untuk . Semua subhimpunan yang memuat merupakan lingkungan bagi , dan setiap fungsi dari ruang tersebut kontinu.   Karena graf adalah lintasan, satu-satunya lintasan sederhana dari ke setiap simpul memberi , , , dan . Membandingkan angka-angka ini dengan syarat menghasilkan tepat empat rezim bola yang dinyatakan pada jawaban.  Karena , setiap himpunan yang memuat juga memuat bola tersebut dan merupakan lingkungan bagi . Sebaliknya, setiap lingkungan bagi harus memuat pusatnya, jadi pencirian itu tepat.  Di setiap simpul , jarak minimum dari ke simpul lain bernilai positif. Pilih jari-jari sebesar jarak minimum tersebut; karena pertidaksamaan bola ketat, bola yang dihasilkan adalah . Untuk fungsi sebarang dan toleransi keluaran sebarang, gunakan bola singleton ini sebagai lingkungan masukan. Setiap di dalamnya sama dengan , sehingga jarak keluarannya nol. Jadi setiap fungsi kontinu di setiap simpul.   Irisan berhingga dan irisan tak berhingga  Buktikan bahwa irisan setiap keluarga berhingga yang tak kosong dari lingkungan bagi titik kembali merupakan lingkungan bagi . Kemudian berikan contoh yang menunjukkan bahwa pernyataan tersebut dapat gagal untuk keluarga tak berhingga.   Untuk banyak lingkungan berhingga, ambil minimum dari jari-jari saksi. Untuk menyangkal versi tak berhingga, gunakan interval terbuka yang menyusut ke dalam .   Jika untuk , maka jari-jari menyaksikan bahwa merupakan lingkungan. Untuk keluarga tak berhingga, setiap merupakan lingkungan bagi , tetapi irisannya adalah , yang bukan lingkungan bagi dalam metrik Euklides.   Misalkan dan lingkungan bagi . Untuk setiap , pilih dengan . Karena hanya ada berhingga banyak jari-jari positif, tetap positif. Maka untuk setiap , sehingga .  Dalam , tetapkan . Setiap adalah bola terbuka dan karena itu lingkungan bagi . Namun, satu-satunya bilangan real yang berada dalam semua interval tersebut ialah , jadi . Setiap bola Euklides berjari-jari positif di sekitar memuat titik selain , sehingga tidak ada bola demikian yang termuat dalam . Irisan itu bukan lingkungan.   Arah prapeta dan citra lingkungan  Misalkan kontinu di . Buktikan bahwa prapeta setiap lingkungan bagi merupakan lingkungan bagi . Sangkal pernyataan serupa bahwa citra setiap lingkungan bagi harus merupakan lingkungan bagi . Terakhir, nyatakan satu hipotesis tambahan yang cukup agar pernyataan tentang citra menjadi benar.   Gunakan pencirian kekontinuan dengan lingkungan untuk prapeta. Untuk citra, uji fungsi konstan dari ke . Hipotesis tambahan yang berguna ialah bahwa merupakan pemetaan terbuka: citra setiap himpunan terbuka harus terbuka.   Pernyataan prapeta benar menurut pencirian kekontinuan. Pernyataan citra salah: fungsi konstan , , memetakan setiap lingkungan ke singleton , yang bukan lingkungan bagi dalam metrik Euklides. Jika kontinu dan juga merupakan pemetaan terbuka, maka citra setiap lingkungan bagi merupakan lingkungan bagi .   Karena kontinu di , teorema lingkungan menyatakan langsung bahwa untuk setiap lingkungan bagi , himpunan merupakan lingkungan bagi . Arah prapeta ini sesuai dengan urutan kuantor dalam definisi kekontinuan.  Untuk arah citra, ambil fungsi konstan dengan . Fungsi ini kontinu. Jika , maka merupakan lingkungan bagi , tetapi . Singleton tersebut tidak memuat bola Euklides berjari-jari positif di sekitar , jadi bukan lingkungan.  Sekarang andaikan, sebagai tambahan, bahwa merupakan pemetaan terbuka. Jika lingkungan bagi , pilih dengan . Himpunan terbuka, sehingga terbuka karena pemetaan terbuka. Himpunan itu memuat dan termuat dalam . Jadi memuat suatu lingkungan terbuka bagi dan karenanya merupakan lingkungan bagi .   "
},
{
  "id": "o003-c90-ch07-mastery-01",
  "level": "2",
  "url": "o003-c90-ch07-mastery.html#o003-c90-ch07-mastery-01",
  "type": "Pemeriksaan",
  "number": "G.41",
  "title": "Empat metrik dan empat bentuk bola.",
  "body": "Empat metrik dan empat bentuk bola  Pada , gambarkan dan nyatakan dengan pertidaksamaan bola berjari-jari yang berpusat di untuk metrik Euklides , metrik maksimum , metrik taksi , dan metrik diskret . Buktikan bahwa    Tuliskan syarat jarak kurang dari untuk setiap metrik. Untuk inklusi, gunakan . Untuk ketatnya inklusi, uji titik pada sumbu, lalu titik dan .   Untuk bolanya ialah cakram ; untuk , persegi terbuka ; untuk , belah ketupat ; dan untuk , singleton . Semua inklusi yang ditampilkan bersifat ketat.   Dari definisi masing-masing metrik diperoleh Untuk setiap , berlaku . Karena itu, syarat norma satu kurang dari mengakibatkan syarat norma dua, dan syarat norma dua mengakibatkan syarat norma maksimum. Bola diskret jelas termuat dalam semuanya.  Inklusinya ketat: berada dalam bola taksi tetapi bukan dalam bola diskret; berada dalam bola Euklides karena , tetapi tidak dalam bola taksi karena ; dan berada dalam bola maksimum, tetapi tidak dalam bola Euklides karena .  "
},
{
  "id": "o003-c90-ch07-mastery-02",
  "level": "2",
  "url": "o003-c90-ch07-mastery.html#o003-c90-ch07-mastery-02",
  "type": "Pemeriksaan",
  "number": "G.42",
  "title": "Ruang yang tersisa di dalam bola terbuka.",
  "body": "Ruang yang tersisa di dalam bola terbuka  Misalkan suatu ruang metrik, , dan . Nyatakan jari-jari residu alami yang berpusat di , buktikan bahwa jari-jari tersebut positif, lalu buktikan bahwa bola yang dihasilkannya termuat dalam .   Ukur bagian jari-jari yang belum dipakai oleh jarak . Untuk titik dalam bola baru, terapkan pertidaksamaan segitiga pada dan pertahankan pertidaksamaan ketatnya.   Ambil . Karena , berlaku , dan .   Keanggotaan berarti , sehingga . Jika , maka Jadi . Karena dipilih sebarang, . Inilah alasan setiap bola terbuka merupakan lingkungan bagi setiap titiknya.  "
},
{
  "id": "o003-c90-ch07-mastery-03",
  "level": "2",
  "url": "o003-c90-ch07-mastery.html#o003-c90-ch07-mastery-03",
  "type": "Pemeriksaan",
  "number": "G.43",
  "title": "Tiga bentuk yang setara untuk kekontinuan.",
  "body": "Tiga bentuk yang setara untuk kekontinuan  Untuk fungsi dan , buktikan kesetaraan ketiga syarat berikut: definisi epsilon-delta; untuk setiap terdapat dengan ; dan prapeta setiap lingkungan bagi merupakan lingkungan bagi . Kemudian gunakan di untuk menjelaskan mengapa prapeta bola tidak harus menjadi bola yang berpusat di .   Kesetaraan dua syarat pertama hanyalah penerjemahan keanggotaan bola. Untuk lingkungan umum, sisipkan sebuah bola di dalam lingkungan. Untuk arah sebaliknya, gunakan fakta bahwa merupakan lingkungan bagi pusatnya. Pada contoh konkret, selesaikan .   Ketiga syarat setara. Untuk , , yang bukan satu interval dan karena itu bukan bola Euklides yang berpusat di .   Untuk , keanggotaan tepat berarti , sedangkan tepat berarti . Jadi implikasi epsilon-delta untuk semua setara tepat dengan inklusi kedua bola tersebut.  Andaikan syarat inklusi bola berlaku dan suatu lingkungan bagi . Ada dengan . Pilih dari syarat inklusi. Maka sehingga merupakan lingkungan bagi .  Sebaliknya, andaikan sifat prapeta lingkungan berlaku. Untuk , bola merupakan lingkungan bagi . Prapetanya karena itu merupakan lingkungan bagi , sehingga memuat untuk suatu . Ini menghasilkan syarat inklusi bola dan menutup siklus kesetaraan.  Pada contoh , bola sasaran ialah . Menyelesaikan memberi dua interval terpisah . Prapeta ini memuat bola kecil di sekitar , tetapi bukan dirinya sendiri sebuah bola yang berpusat di .  "
},
{
  "id": "o003-c90-ch07-mastery-04",
  "level": "2",
  "url": "o003-c90-ch07-mastery.html#o003-c90-ch07-mastery-04",
  "type": "Pemeriksaan",
  "number": "G.44",
  "title": "Metrik graf berhingga yang lengkap.",
  "body": "Metrik graf berhingga yang lengkap  Ambil lintasan berbobot dengan bobot sisi berturut-turut , dan definisikan jarak sebagai panjang lintasan terpendek. Daftarkan semua bola berbeda untuk , cirikan semua lingkungan bagi , lalu buktikan bahwa setiap fungsi dari ruang ini ke sembarang ruang metrik bersifat kontinu.   Hitung dahulu dan ingat bahwa syarat bola adalah jarak kurang dari jari-jari. Untuk kekontinuan, cari bola singleton di setiap simpul.   Jarak dari ialah . Bola-bolanya adalah untuk , untuk , untuk , dan seluruh ruang untuk . Semua subhimpunan yang memuat merupakan lingkungan bagi , dan setiap fungsi dari ruang tersebut kontinu.   Karena graf adalah lintasan, satu-satunya lintasan sederhana dari ke setiap simpul memberi , , , dan . Membandingkan angka-angka ini dengan syarat menghasilkan tepat empat rezim bola yang dinyatakan pada jawaban.  Karena , setiap himpunan yang memuat juga memuat bola tersebut dan merupakan lingkungan bagi . Sebaliknya, setiap lingkungan bagi harus memuat pusatnya, jadi pencirian itu tepat.  Di setiap simpul , jarak minimum dari ke simpul lain bernilai positif. Pilih jari-jari sebesar jarak minimum tersebut; karena pertidaksamaan bola ketat, bola yang dihasilkan adalah . Untuk fungsi sebarang dan toleransi keluaran sebarang, gunakan bola singleton ini sebagai lingkungan masukan. Setiap di dalamnya sama dengan , sehingga jarak keluarannya nol. Jadi setiap fungsi kontinu di setiap simpul.  "
},
{
  "id": "o003-c90-ch07-mastery-05",
  "level": "2",
  "url": "o003-c90-ch07-mastery.html#o003-c90-ch07-mastery-05",
  "type": "Pemeriksaan",
  "number": "G.45",
  "title": "Irisan berhingga dan irisan tak berhingga.",
  "body": "Irisan berhingga dan irisan tak berhingga  Buktikan bahwa irisan setiap keluarga berhingga yang tak kosong dari lingkungan bagi titik kembali merupakan lingkungan bagi . Kemudian berikan contoh yang menunjukkan bahwa pernyataan tersebut dapat gagal untuk keluarga tak berhingga.   Untuk banyak lingkungan berhingga, ambil minimum dari jari-jari saksi. Untuk menyangkal versi tak berhingga, gunakan interval terbuka yang menyusut ke dalam .   Jika untuk , maka jari-jari menyaksikan bahwa merupakan lingkungan. Untuk keluarga tak berhingga, setiap merupakan lingkungan bagi , tetapi irisannya adalah , yang bukan lingkungan bagi dalam metrik Euklides.   Misalkan dan lingkungan bagi . Untuk setiap , pilih dengan . Karena hanya ada berhingga banyak jari-jari positif, tetap positif. Maka untuk setiap , sehingga .  Dalam , tetapkan . Setiap adalah bola terbuka dan karena itu lingkungan bagi . Namun, satu-satunya bilangan real yang berada dalam semua interval tersebut ialah , jadi . Setiap bola Euklides berjari-jari positif di sekitar memuat titik selain , sehingga tidak ada bola demikian yang termuat dalam . Irisan itu bukan lingkungan.  "
},
{
  "id": "o003-c90-ch07-mastery-06",
  "level": "2",
  "url": "o003-c90-ch07-mastery.html#o003-c90-ch07-mastery-06",
  "type": "Pemeriksaan",
  "number": "G.46",
  "title": "Arah prapeta dan citra lingkungan.",
  "body": "Arah prapeta dan citra lingkungan  Misalkan kontinu di . Buktikan bahwa prapeta setiap lingkungan bagi merupakan lingkungan bagi . Sangkal pernyataan serupa bahwa citra setiap lingkungan bagi harus merupakan lingkungan bagi . Terakhir, nyatakan satu hipotesis tambahan yang cukup agar pernyataan tentang citra menjadi benar.   Gunakan pencirian kekontinuan dengan lingkungan untuk prapeta. Untuk citra, uji fungsi konstan dari ke . Hipotesis tambahan yang berguna ialah bahwa merupakan pemetaan terbuka: citra setiap himpunan terbuka harus terbuka.   Pernyataan prapeta benar menurut pencirian kekontinuan. Pernyataan citra salah: fungsi konstan , , memetakan setiap lingkungan ke singleton , yang bukan lingkungan bagi dalam metrik Euklides. Jika kontinu dan juga merupakan pemetaan terbuka, maka citra setiap lingkungan bagi merupakan lingkungan bagi .   Karena kontinu di , teorema lingkungan menyatakan langsung bahwa untuk setiap lingkungan bagi , himpunan merupakan lingkungan bagi . Arah prapeta ini sesuai dengan urutan kuantor dalam definisi kekontinuan.  Untuk arah citra, ambil fungsi konstan dengan . Fungsi ini kontinu. Jika , maka merupakan lingkungan bagi , tetapi . Singleton tersebut tidak memuat bola Euklides berjari-jari positif di sekitar , jadi bukan lingkungan.  Sekarang andaikan, sebagai tambahan, bahwa merupakan pemetaan terbuka. Jika lingkungan bagi , pilih dengan . Himpunan terbuka, sehingga terbuka karena pemetaan terbuka. Himpunan itu memuat dan termuat dalam . Jadi memuat suatu lingkungan terbuka bagi dan karenanya merupakan lingkungan bagi .  "
},
{
  "id": "index-1",
  "level": "1",
  "url": "index-1.html",
  "type": "Indeks",
  "number": "",
  "title": "Indeks",
  "body": " Indeks   "
}
]

var ptx_lunr_idx = lunr(function () {
  this.ref('id')
  this.field('title')
  this.field('body')

  ptx_lunr_docs.forEach(function (doc) {
    this.add(doc)
  }, this)
})
