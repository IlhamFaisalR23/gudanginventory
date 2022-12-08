$('.delete-confirm').on('click', function (event) {
    event.preventDefault();
    const url = $(this).attr('href');
    swal({
        title: 'Anda Yakin?',
        text: 'Data ini akan dihapus secara permanen',
        icon: 'warning',
        confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
        buttons: ["Batal", "Ya!"],
    }).then(function(value) {
        if (value) {
            window.location.href = url;
        }
    });
});

