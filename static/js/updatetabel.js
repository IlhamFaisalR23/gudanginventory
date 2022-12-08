$('.konfirmasi-acc').on('click', function (event) {
    event.preventDefault();
    const url = $(this).attr('href');
    swal({
        title: "Anda Yakin ?",
        text: "Menyetujui permintaan ini?",
        icon: "warning",
        buttons: true,
        dangerMode: true,
        confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
        buttons: ["Batal", "Ya!"],
      })
      .then((willDelete) => {
        if (willDelete) {
            window.location.href = url;
          swal("Pengajuan barang telah disetujui", {
            icon: "success",
            
          });
        } else {
          swal("Penyetujuan pengajuan dibatalkan");
        }
      });
});

$('.menolak-permintaan').on('click', function (event) {
    event.preventDefault();
    const url = $(this).attr('href');
    swal({
        title: "Anda Yakin ?",
        text: "Menolak permintaan ini?",
        icon: "warning",
        buttons: true,
        dangerMode: true,
        confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
        buttons: ["Batal", "Ya!"],
      })
      .then((willDelete) => {
        if (willDelete) {
            window.location.href = url;
          swal("Pengajuan barang ditolak", {
            icon: "success",
            
          });
        } else {
          swal("Penolakan pengajuan dibatalkan");
        }
      });
});