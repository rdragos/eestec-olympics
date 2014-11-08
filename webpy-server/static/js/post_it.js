function submit_task(url) {
    var data = $("#text_data").val();
    var chunks = data.split('\n');
    var query = $.ajax({
        type : "GET",
        url : "/bot",
        data : "question=" + chunks[chunks.length - 1].trim()
    });
    query.done(function(data) {
        console.log(data);
        $("#text_data").val($("#text_data").val() + "\n" + data + "\n");
    });
}

function clear_task(url) {
    $("#text_data").val("");
}

$(function(){
    populateUserDataUi();
});
