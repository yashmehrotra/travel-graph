
$(function () {
  
  var ques_id = $('#ques-id').text();
  //alert(ques_id);
  get_answers(ques_id);

  $('#post-ans').on('click', function (){
    var ans_text = objEditor.getData();
    console.log(ans_text);
    add_ans(ques_id, ans_text);
  });

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
  
  $('#answers-grid').empty();

  for (var i = result.answers.length - 1; i >= 0; i--) {
    var answer_html_to_append = '<div class="uk-width-1-5"></div><div class="uk-width-3-5"><hr><p>' + result.answers[i].answer + '</p><img alt="ans-img" class="uk-margin-bottom" src="../../static/images/wbg6.jpg"><br><article class="uk-comment uk-width-3-5"><header class="uk-comment-header"><img class="uk-comment-avatar" src="../../static/images/placeholder_avatar.svg" alt="user-img">Answered by <a href="">' + result.answers[i].user_details.username + '</a><ul class="uk-comment-meta"><li><span>Answered at 9:30pm on 11 Feb 2015</span></li></ul></header></article></div><!-- FOR DISPLAYING TAGS IN ANSWER --><div class="uk-width-1-5 uk-margin-top"><p><button class="uk-button uk-button-small" type="button">tag-1</button><button class="uk-button uk-button-small" type="button">tag-2</button></p></div>';
    
    $('#answers-grid').append(answer_html_to_append);
  }
}