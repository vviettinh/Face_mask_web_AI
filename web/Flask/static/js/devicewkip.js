// tạo tên thiết bị a - Kíp b
$(document).ready(function() {
    $(".input-field").change(function() {
        id_cam = $("#device :selected").val();
        shift = $("#shift :selected").val();
        date = $("#start").val();
        face = $(".selected").attr("id");

        console.log(date, id_cam, shift, face)
        data = {}
        data['id_cam'] = id_cam;
        data['shift'] = shift;
        data['time'] = date;
        data['face'] = face;

        $.ajax({
            url: '/info',
            contentType: "application/json;charset=utf-8",
            dataType: 'json',
            type: "POST",
            data: JSON.stringify(data),
            success: function(response) {
                // console.log(response);
                var image = response['image'];
                $("#image").empty();
                for (img in image) {

                    // let src = 'https://image.shutterstock.com/image-photo/close-portrait-smiling-handsome-man-260nw-1011569245.jpg'
                    //let ele = `<div><img src = '${image[img]}' /></div>alt="img"></div>`;
                    let ele = `<div><img src = '${image[img]}' /></div>`;
                    $('#image').append(ele);
                }



                data = [];
                for (var i = 0; i < 2; i++) {
                    if (i.toString() in response)
                        data.push(response[i.toString()]);
                    else
                        data.push(0);
                }
                console.log(data)

                myChart.data.datasets[0].data = data;
                myChart.update();

            },
            error: function(error) {
                $("#wait-load").modal("hide");
                console.log(error);
            }
        });
    });

    // $("#setstt").click(function () {
    //     const template = undefined
    //     $("#informleft").html("Thiết bị - kíp");
    //     $("#informright").html("Thiết bị - kíp");
    // });

    var now = new Date();
    var month = (now.getMonth() + 1);
    var day = now.getDate();
    if (month < 10)
        month = "0" + month;
    if (day < 10)
        day = "0" + day;
    var today = now.getFullYear() + '-' + month + '-' + day;
    $('#start').val(today);

    $('#start').change(function() {
        var date = $(this).val();
        console.log(date, 'change')
    });

    $("#bar .face").click(function() {

        $("#bar .face").each(function() {
            $(this).removeClass("selected");
            $(this).css('border-bottom', 'none')
        });
        $(this).addClass("selected");
        $(this).css('border-bottom', '2px solid #2ecc71')

        id_cam = $("#device :selected").val();
        shift = $("#shift :selected").val();
        date = $("#start").val();
        face = $(".selected").attr("id");

        console.log(date, id_cam, shift, face)
        data = {}
        data['id_cam'] = id_cam;
        data['shift'] = shift;
        data['time'] = date;
        data['face'] = face;

        $.ajax({
            url: '/info',
            contentType: "application/json;charset=utf-8",
            dataType: 'json',
            type: "POST",
            data: JSON.stringify(data),
            success: function(response) {
                console.log(response);
                var image = response['image'];
                $("#image").empty();
                for (img in image) {

                    // let src = 'https://image.shutterstock.com/image-photo/close-portrait-smiling-handsome-man-260nw-1011569245.jpg'
                    //let ele = `<div><img src = '${image[img]}' /></div>alt="img"></div>`;
                    let ele = `<div><img src = '${image[img]}' /></div>`;
                    $('#image').append(ele);
                }
            },
            error: function(error) {
                $("#wait-load").modal("hide");
                console.log(error);
            }
        });
    });

});