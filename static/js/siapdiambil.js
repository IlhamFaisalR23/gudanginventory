$('.barang-siapdiambil').on('click', function (event) {
    event.preventDefault();
    const url = $(this).attr('href');
    swal({
        title: "Anda Yakin ?",
        text: "Mengubah status menjadi Siap Diambil?",
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
          swal("Menunggu pemesan mengambil barang", {
            icon: "success",
            
          });
        } else {
          swal("Pengubahan status dibatalkan");
        }
      });
});