
var alltasks;
var userId;

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
    "content": "",
    "endDate": "01.01.2009",
    "id": 0,
    "startDate": "01.01.2009",
    "title": "",
    "userId": userId
  });

  var request = $.ajax({
      type: "POST",
      url: "/tasks",
      data: alltasks[alltasks.length - 1],
      dataType: JSON
  });
  request.success(function (data) {
    alert(data);
    $('#canvas').append(node);
  });
  request.fail(function (data) {
    console.log(data);
  });
}

// wait until the dom document is loaded
function updateTask(node, idx) {
  var titleTextarea = $("<textarea placeholder='Enter title here..' class ='title-holder' rows='1'>" + alltasks[idx].title + "</textarea>"); 
  var contentTextarea = $("<textarea placeholder='Enter some description here..' class ='content-holder'>" + alltasks[idx].content+ "</textarea>");
  var checkbox = $("<input type='checkbox' name='task_completed' " + (alltasks[idx].completed ? " checked " : "") + ">");
  

  var lambdaFunc = function() {
    var idx = $(this).parent().attr("id");
    alltasks[idx].title = $(this).parent().children().eq(0).val();
    alltasks[idx].content = $(this).parent().children().eq(1).val();
    alltasks[idx].completed = ($(this).parent().children().eq(2).attr('checked') == undefined);
    console.log(alltasks[idx]);
    var request = $.ajax({
      type: "PUT",
      url: "/tasks?id=" + alltasks[idx].id,
      data: alltasks[idx],
      dataType: JSON,
    }).done(function(data) {
      console.log("Done this" + alltasks[idx]);
    });
  };  

  titleTextarea.change(lambdaFunc);
  contentTextarea.change(lambdaFunc);
  checkbox.change(lambdaFunc);


  $(node).append(titleTextarea); 
  $(node).append(contentTextarea);
  $(node).append(checkbox);
  $(node).append("  completed");
  $(node).attr("id", idx);

  return $(node);
}

function getTasks() {

  var userQuery = getUserData();
  userQuery.done(function(data) {


    var userObject = JSON.parse(data);
    userId = userObject.id;
    console.log(userObject);
    var query = $.ajax({
      type : "GET",
      url : "/tasks",
      data : "userId=" + userObject.id,
    });
    query.done(function(data) {

      alltasks = JSON.parse(data);
      var posY = 200;
      var posX = 0;

      for (var idx in alltasks) {

        var task = alltasks[idx];
        posX += 430;
        if (posX > $(document).width()) {
          posX = 0;
          posY += 430;
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
  $("#canvas").dblclick(function(event){
     makeNote(event);
  })
  populateUserDataUi();
  getTasks();
});

