function toggleIconBuku(buku) {
        // Toggle list-menu Buku
        const listmenu = document.getElementById('buku_list');
        listmenu.classList.toggle('hidden');

        // Toggle icon menu Buku
        const icon = buku.querySelector('i.fa-angle-right, i.fa-angle-down');
        if (icon) {
            icon.classList.toggle('fa-angle-right');
            icon.classList.toggle('fa-angle-down');
        }
}

function toggleIconAnggota(anggota) {
        // Toggle list-menu Anggota
        const listmenu = document.getElementById('anggota_list');
        listmenu.classList.toggle('hidden');

        // Toggle icon menu Peminjaman
        const icon = anggota.querySelector('i.fa-angle-right, i.fa-angle-down');
        if (icon) {
            icon.classList.toggle('fa-angle-right');
            icon.classList.toggle('fa-angle-down');
        }
}

function toggleIconPeminjaman(peminjaman) {
        // Toggle list-menu Peminjaman
        const listmenu = document.getElementById('peminjaman_list');
        listmenu.classList.toggle('hidden');

        // Toggle icon menu Peminjaman
        const icon = peminjaman.querySelector('i.fa-angle-right, i.fa-angle-down');
        if (icon) {
            icon.classList.toggle('fa-angle-right');
            icon.classList.toggle('fa-angle-down');
        }
}

document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function (e) {
            e.preventDefault();

            const form = this.closest("form");

            Swal.fire({
                title: 'Apakah kamu yakin?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Ya!',
            }).then((result) => {
                if (result.isConfirmed) {
                    form.submit();  // Submit the actual form
                }
            });
        });
    });

    ClassicEditor
    .create(document.querySelector('#alamat_anggota'), {
        licenseKey: 'eyJhbGciOiJFUzI1NiJ9.eyJleHAiOjE3NDg4MjIzOTksImp0aSI6IjBiMDEzZTc5LWYzMTUtNDg2OC1iNGQ5LTU0ZWE0OGY0OTY1OCIsInVzYWdlRW5kcG9pbnQiOiJodHRwczovL3Byb3h5LWV2ZW50LmNrZWRpdG9yLmNvbSIsImRpc3RyaWJ1dGlvbkNoYW5uZWwiOlsiY2xvdWQiLCJkcnVwYWwiLCJzaCJdLCJ3aGl0ZUxhYmVsIjp0cnVlLCJsaWNlbnNlVHlwZSI6InRyaWFsIiwiZmVhdHVyZXMiOlsiKiJdLCJ2YyI6ImZmYmZkZjRiIn0.rk2-D2ph9DesvTite6QsBzPwjr67RgMRdv_vszPeb6AgL58TV8CFTGJSPDx5yM38JObIETq8MLi3sF7wa_wFuA'
    })
    .then(editor => {
        window.editor = editor;
    })
    .catch(error => {
        console.error('Editor init error:', error);
    });

    
    document.getElementById('add-buku-btn').addEventListener('click', function () {
        const container = document.querySelector('.buku-select-group').parentNode;
        const clone = container.cloneNode(true);
        clone.querySelector('select').value = ""; // reset selection
        container.parentNode.appendChild(clone);
});
});