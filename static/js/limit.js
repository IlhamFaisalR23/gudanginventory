var balance = 100; //Fetched from DB

$(document).on('keyup', '#AmountI', function () {
  var $field = $(this);
  var amountI =  parseInt($field.val());

  if( amountI > balance) {
    alert('Jumlah pesanan melebihi stok');
    $field.val("");
  }
});