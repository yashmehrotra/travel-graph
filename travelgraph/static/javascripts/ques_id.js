
$(function () {
  
  var ques_id = $('#ques-id').text();
  //alert(ques_id);
  get_answers(ques_id);

  // $('#post-ans').on('click', function (){
    // var ans_text = objEditor.getData();
    // console.log(ans_text);
    // add_ans(ques_id, ans_text);
  // });

});

function get_answers(ques_id) {
  //alert(ques_id);
  $.ajax({
    type: "GET",
    url: "/api/content/get_answers/" + ques_id + "/",
      // console.log(result);
    success: function(result) {
      if(result) {
        console.log(result);
	// FOR APPENDING THE ANSWERS
        append_answers(result);
      } else {
        console.log('Problem with ajax');
      }
    }
  });
}

function add_ans(ques_id, ans_text) {
  $.ajax({
    type: "POST",
    url: "/api/content/add_answer",
    data: {
      'question_id': ques_id,
      'answer': ans_text,
    },
    success: function(result) {
      if(result) {
        get_answers(ques_id);
      } else {
        console.log('Problem with ajax');
      }
    }
  });
}

function append_answers(result) {
  
  // if ($('.ans-list')) {
    // $('.ans-list').remove();
  // }
  
  $('#answers-grid').empty();

  // console.log(result);

  for (var i = result.answers.length - 1; i >= 0; i--) {
    var answer_html_to_append = '<div class="uk-width-1-5"></div><div class="uk-width-3-5"><hr><p>' + result.answers[i].answer + '</p><img alt="ans-img" class="uk-margin-bottom" src="../../static/images/wbg6.jpg"><br><article class="uk-comment uk-width-3-5"><header class="uk-comment-header"><img class="uk-comment-avatar" src="../../static/images/placeholder_avatar.svg" alt="user-img">Answered by <a href="">Username</a><ul class="uk-comment-meta"><li><span>Answered at 9:30pm on 11 Feb 2015</span></li></ul></header></article></div><!-- FOR DISPLAYING TAGS IN ANSWER --><div class="uk-width-1-5"><!-- <blockquote> --><select id="answer-1-tags-selected" class="answered-tags-selected uk-width-1-1" name="answer-tags-select" multiple><option value="tag-2" selected="selected">tag-2</option><option value="tag-4" selected="selected">tag-4</option><option value="tag-5" selected="selected">tag-5</option></select><!-- </blockquote> --></div>';
    $('#answers-grid').append(answer_html_to_append);
// $('#ans ul').append('<li class="ans-list">' + result.answers[i].answer + '</li>');
  }
  // $('.answers-tags-selected').chosen();
  $('.answered-tags-selected').trigger('chosen:updated');
  // $('#answer-tags-select').trigger('liszt:updated');

}