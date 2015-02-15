$(function (){
          
  $('#question-submit-button').on('click',function(){
    var ques_text = $('#question-text').val();
    var ques_desc = objEditor.getData();
    var ques_tags = $('#question-tags').val();
      
    alert(ques_text);
    alert(ques_desc);
    alert(ques_tags);

    submit(ques_text, ques_desc, ques_tags);
  });

});

function submit(ques_text, ques_desc, ques_tags) {
  alert("Submitting");
  $.ajax({
    type: "POST",
    url: "api/content/add_question",
    data: {
      'question_text': ques_text,
      'question_desc': ques_desc,
      'question_tags': ques_tags,
    },
    success: function(result) {
      if(result) {
        console.log(result);
        result = JSON.parse(result);
        console.log(result['status']);
        console.log(result.message);
      } else {
        console.log('Problem with ajax');
        alert('Problem with ajax');
      }
    }
  });
  return false;
}