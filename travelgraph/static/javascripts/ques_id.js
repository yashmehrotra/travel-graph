$(function () {
    
  // retreive id(s) from html
  var ques_id = $('#ques-id').text();
  var asker_user_id = $('#asker-user-id').text();
  var logged_in_user_id = $('#logged-in-user-id').text();
    
  // follow and subscribe buttons should be disabled if the currently logged in user is the same as the question asker
  if (asker_user_id == logged_in_user_id) {
    $('#follow-asker').attr('disabled', true);
    $('#subscribe-question').attr('disabled', true);
  }

  // retreive all answers for the current question
  get_answers(ques_id);

  // post an answer
  $('#post-ans').on('click', function (){
    var ans_text = objEditor.getData();   // get formatted html out of ckeditor 
    // console.log(ans_text);
    add_ans(ques_id, ans_text);
  });
  
  // follow the question asker
  $('#follow-asker').on('click', function(){
    follow_user(asker_user_id, logged_in_user_id);
  });

  // subscribe to a question
  $('#subscribe-question').on('click', function(){
    subscribe_question(logged_in_user_id, ques_id);
  });

  // show/hide the answer text area
  $('#answer-button').on('click', function(){
    if($('#answer-textarea-grid').is(':visible')) {
      $('#answer-tags-select').next().width('100%');  // Used to correct the width of the tags input area when the text editor is shown
      $(this).text("Hide");
    } else {
      $(this).text("Answer");
    }
  });

});

function get_answers(ques_id) {
  $.ajax({
    type: "GET",
    url: "/api/content/get_answers/" + ques_id + "/",
    success: function(result) {
      if(result) {
        console.log(result);
        append_answers(result);    // append all the retreived answers
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
      'answer_tags': 'a,b,c'
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
    var answer_html_to_append = '<div class="uk-width-1-5"></div><div class="uk-width-3-5"><hr><p>' + result.answers[i].answer + '</p><br><article class="uk-comment uk-width-2-5"><header class="uk-comment-header"><img class="uk-comment-avatar" src="../../static/images/placeholder_avatar.svg" alt="user-img" style="height: 40px; width: 40px;">Answered by <a href="">' + result.answers[i].user_details.username + '</a><ul class="uk-comment-meta"><li><span>Answered at 9:30pm on 11 Feb 2015</span></li></ul></header></article></div><!-- FOR DISPLAYING TAGS IN ANSWER --><div class="uk-width-1-5 uk-margin-top"><p><button class="uk-button uk-button-small" type="button">tag-1</button><button class="uk-button uk-button-small" type="button">tag-2</button></p></div>';    

    $('#answers-grid').append(answer_html_to_append);
  }
    $('#answers-count-text').empty().append(result.answers.length + " Answers");
}

function follow_user(user_id, logged_in_user_id) {
  $.ajax({
    type: "POST",
    url: "/api/user/follow_user",
    data: {
      'user_id': user_id,
      'user_id_to_follow': logged_in_user_id,
    },
    success: function(result) {
      if(result) {
	$('#follow-asker').text('Following');
	$('#follow-asker').removeClass('uk-button-primary');
      } else {
	console.log('Problem with ajax');
      }
    }
  });
}

function subscribe_question(user_id, ques_id) {
 $.ajax({
    type: "POST",
    url: "/api/content/.....", // edit here
    data: {
      'question_id': ques_id,
      'user_id': user_id,
    },
    success: function(result) {
      if(result) {
        $('#subscribe-question').text('Subscribed');
	$('#subscribe-question').removeClass('uk-button-success');
      } else {
        console.log('Problem with ajax');
      }
    }
  }); 
}