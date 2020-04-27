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

function get_key_info() {
    $.ajax({
        url: "/get_key_info",
        success: function (data) {
            $(".key_info h1").eq(0).text(data.confirm_num);
            $(".key_info h1").eq(1).text(data.suspect_num);
            $(".key_info h1").eq(2).text(data.heal_num);
            $(".key_info h1").eq(3).text(data.dead_num);
        }, error: function () {

        }
    })
}

setInterval(get_time, 1000);
setInterval(get_key_info, 1000)

function get_china_data() {
    $.ajax({
        url: "/get_china_data",
        success: function (data) {
            // alert(data.data)
            ec_china_option.series[0].data = data.data;
            chinaMap.setOption(ec_china_option)
        }, error: function (xhr, type, errorThrow) {
        }
    })
}

get_china_data()