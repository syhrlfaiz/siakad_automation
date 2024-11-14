// Buat dan tambahkan tombol ke halaman
function createCopyButton() {
   // Buat tombol
   const button = document.createElement('button');
   button.innerHTML = 'Salin MSO Text';
   button.style.cssText = `
       position: fixed;
       top: 10px;
       right: 10px;
       z-index: 9999;
       padding: 10px;
       background: #007bff;
       color: white;
       border: none;
       border-radius: 5px;
       cursor: pointer;
   `;

   // Tambahkan fungsi untuk menyalin saat diklik
   button.onclick = function() {
       // Tambahkan "jwb" di awal
       const headerText = "jwb";
       
       // Ambil elemen dari kedua kelas
       const msoListElements = document.getElementsByClassName('MsoListParagraph');
       const msoNormalElements = document.getElementsByClassName('MsoNormal');
       
       // Gabungkan hasil dari kedua kelas
       const textsArray = [
           headerText, // Tambahkan "jwb" sebagai elemen pertama array
           ...Array.from(msoListElements).map(el => el.textContent),
           ...Array.from(msoNormalElements).map(el => el.textContent)
       ];
       
       const combinedText = textsArray.join('\n');
       
       navigator.clipboard.writeText(combinedText)
           .then(() => {
               // Feedback visual bahwa copy berhasil
               button.innerHTML = 'Tersalin!';
               button.style.background = '#28a745';
               console.log('Isi yang disalin:', combinedText); // untuk melihat hasilnya di console
               setTimeout(() => {
                   button.innerHTML = 'Salin MSO Text';
                   button.style.background = '#007bff';
               }, 2000);
           })
           .catch(err => {
               console.error('Gagal menyalin:', err);
               button.innerHTML = 'Gagal!';
               button.style.background = '#dc3545';
               setTimeout(() => {
                   button.innerHTML = 'Salin MSO Text';
                   button.style.background = '#007bff';
               }, 2000);
           });
   };

   // Tambahkan tombol ke halaman
   document.body.appendChild(button);
}

// Jalankan fungsi
createCopyButton();
