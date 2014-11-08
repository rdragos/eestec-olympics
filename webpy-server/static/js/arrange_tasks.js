
var alltasks;

function add_details(node, to_textarea) {
  $(node).text("Another text");
  $(node).append("<textarea>to_textarea</textarea>");
}

function makeNote (e) {

    // Check the event object if the .click is on the canvas
    // or a created note
    if (e.eventPhase === 2) {       
       // Create the new comment at the corsor postition
       var str1 = '<div class="ui-widget-content newbox" style="top:' + e.pageX + 'px; left:' + e.pageY + 'px;">';
       node = $(str1).draggable();
       createNewTask(node);
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
    "id": 0,
    "startDate": "01.01.2009",
    "title": "new title",
    "userId": alltasks[0].userId
  });

  var request = $.ajax({
      type: "POST",
      url: "/tasks",
      data: alltasks[alltasks.length - 1],
      dataType: JSON
  });
  request.success(function (data) {
    alert(data);
    $(this).parent().append("<text>" + "Succesfully created new" + "</text>");
    $('#canvas').append(node);
  });
  request.fail(function (data) {
    console.log(data);
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
      type: "PUT",
      url: "/tasks?id=" + alltasks[idx].id,
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

function getTasks() {

  var userQuery = getUserData();
  userQuery.done(function(data) {


    var userObject = JSON.parse(data);
    console.log(userObject);
    var query = $.ajax({
      type : "GET",
      url : "/tasks",
      data : "userId=" + userObject.id
    });
    query.done(function(data) {
      alltasks = JSON.parse(data);
      $('#canvas').click(function(e){
        makeNote(e);
      });
      console.log(alltasks);
      // Remove the note
      
      var posY = 0;
      var posX = 0;

      for (var idx in alltasks) {

        var task = alltasks[idx];
        posX += 330;
        if (posX > $(document).width()) {
          posX = 0;
          posY += 330;
        }

        var str1 = '<div class=\"ui-widget-content newbox\" style=\"top:' +posY + 'px; left:' + posX + 'px;\"></div>';
        node = $(str1).draggable();
        node = updateTask(node, idx); 
        node.css("position" , "absolute");
        $('#canvas').append(node);
      }
      $("#close").click(function () {
          deleteNote();
      });
    });
  })
}

$(document).ready(function(){
  getTasks();    
});

