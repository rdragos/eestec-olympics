function submit_task(url) {
    var data = $("#text_data").val();
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: null,
        dataType: null
    });
}

function clear_task(url) {
    var data = "clear";
    $.ajax({
        type: "POST",
        url: url,
        data: "clear",
        success: null,
        dataType: null
    });
}
