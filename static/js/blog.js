  $(function () {

  $(".js-create-post").click(function () {
    $.ajax({
      url: '/post/create/',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-post").modal("show");
      },
      success: function (data) {
        $("#modal-post .modal-content").html(data.html_form);
      }
    });
  });

});
