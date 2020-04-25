function get_time() {
    $.ajax({
        url: "/get_time",
        timeout: 10000,//超时时间设置为10秒
        success: function (data) {
            $('#time').html(data);
        }, error: function (xhr, type, errorThrown) {

        }
    })
}

setInterval(get_time, 1000);