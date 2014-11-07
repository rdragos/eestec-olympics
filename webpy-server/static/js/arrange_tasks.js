function makeNote (e) {

    // Check the event object if the .click is on the canvas
        // or a created note
        if (e.eventPhase === 2) {
           
           // Create the new comment at the corsor postition
           var str1 = '<div class="ui-widget-content newbox" style="top:' + e.pageY + 'px; left: ' + e.pageX + 'px;"><span id="close">Delete comment</span><p>Your comment:</p><textarea></textarea></div>';
           node = $(str1).draggable();
           $('#canvas').append(node);
       
       }
       
}

function deleteNote() {
    $(this).parent('#newbox').remove(); 
}

// wait until the dom document is loaded
$(document).ready(function(){

    // listen for a .click() event on the canvas element
    $('#canvas').click(function(e){
        makeNote(e);
    });
    
    // Remove the note
    $("#close").click(function () {
        deleteNote();
    });
    
});

/*
$(document).ready(function() {
  alltasks = JSON.parse(alltasks.replace(/'/g, "\"").replace(/False/g, "false"));
  $('#canvas').click(function(e){
        makeNote(e);
    });
    
    // Remove the note
    $("#close").click(function () {
        deleteNote();
    });
  //styleobject(alltasks);
})*/
