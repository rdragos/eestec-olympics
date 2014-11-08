

var task_cnt = 0;
function add_details(node, to_textarea) {
  $(node).text("Another text");
  $(node).append("<textarea>to_textarea</textarea>");
}
function makeNote (e) {

    // Check the event object if the .click is on the canvas
    // or a created note
    if (e.eventPhase === 2) {
       
       // Create the new comment at the corsor postition
       var str1 = '<div class="ui-widget-content newbox" style="top:' + e.pageY + 'px; left:' + e.pageX + 'px;">';
       node = $(str1).draggable();
       createNewTask(node);
       task_cnt += 1;
       $('#canvas').append(node);
   
   }
       
}

function deleteNote() {
    $(this).parent('#newbox').remove(); 
}
function createNewTask(node) {

  alltasks.push({
    "completed": false,
    "content": "Nothing here",
    "endDate": "01.01.2009",
    "id": task_cnt + 1,
    "startDate": "01.01.2009",
    "title": "new title",
    "userId": alltasks[0].id
  });

  $.ajax({
      type: "POST",
      url: "/create_new_task",
      data: alltasks[alltasks.length - 1],
      success: function(data) {
        $(this).parent().append("<text>" + "Succesfully created new" + "</text>");
      },
      dataType: JSON
    });
}
// wait until the dom document is loaded
function updateTask(node, idx) {
  $(node).append("<text>" + alltasks[idx].title + "</text>"); 
  $(node).append("<textarea id=1>" + alltasks[idx].content+ "</textarea>");
  $(node).append("<text>" + alltasks[idx].completed + "</text>");
  $(node).attr("id", idx);

  var submitButton = $("<button>Send it!</button>");

  $(submitButton).click(function() {
    var idx = $(this).parent().attr("id");
    alltasks[idx].content = $(this).parent().children(0).eq(1).val();
    alert(alltasks[idx].content);
    $.ajax({
      type: "POST",
      url: "/alter_task",
      data: alltasks[idx],
      success: function(data) {
        $(this).parent().append("<text>" + "Succesfully updated" + "</text>");
      },
      dataType: JSON
    });
  })
  $(node).append(submitButton);
  return $(node);
}
$(document).ready(function(){

    alltasks = JSON.parse(alltasks.replace(/'/g, "\"").replace(/False/g, "false"));
    $('#canvas').click(function(e){
        makeNote(e);
    });
    // Remove the note
    
    var posY = 0;
    var posX = 0;

    for (var idx in alltasks) {
      task_cnt += 1;
      var task = alltasks[idx];
      var str1 = '<div class="ui-widget-content newbox" style="top:' + posY + 'px;';

      posY += 10;
      posX += 10;

      var str1 = '<div class="ui-widget-content newbox" style="top:' +posX + 'px; left:' + posY + 'px;">';
      node = $(str1).draggable();
      node = updateTask(node, idx); 
      $('#canvas').append(node);
    }
    $("#close").click(function () {
        deleteNote();
    });
    
});

