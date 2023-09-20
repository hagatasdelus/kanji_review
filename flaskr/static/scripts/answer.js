let success_se;
let timer;
let passTimer;
let passTime = 0;
success_se = new Audio('../static/se/success_se.mp3');
if (suc) {
  get_answer();
  if (se)
    success_se.play();
}

function show_second_left(remaining) {
  let old_second_left_elm = document.getElementById('second_left');
  if (old_second_left_elm) 
    old_second_left_elm.remove();
  let old_score_elm = document.getElementById('score');
  if (old_score_elm)
    old_score_elm.remove();
  if (Math.floor((remaining / 1000) - passTime) < 0)
    return
  
  let answer_element = document.getElementById('kanjinfo');
  let score_elm = document.createElement('p');
  score_elm.id = 'score';
  score_elm.textContent = score;
  answer_element.after(score_elm);
  let second_left_elm = document.createElement('p');
  second_left_elm.id = 'second_left';
  second_left_elm.textContent = Math.floor((remaining / 1000) - passTime);
  answer_element.after(second_left_elm);
  passTime++;
}

const play_review_game = () => {
  if (window.location.pathname === '/question') {
    localStorage.setItem('start_time', new Date().getTime());
  }
  let elapsed = new Date().getTime() - localStorage.getItem('start_time');
  let remaining = time - elapsed;
  show_second_left(remaining);
  if (remaining > 0) {
    if (suc) {
      clearTimeout(timer);
    }
    else {
      timer = setTimeout(get_answer, remaining);
      passTimer = setInterval(function(){
        show_second_left(remaining)
      }, 1000);
    }
  }
}

$(function () {
  if (!gamemode) 
    setInterval(get_answer, time);
  else
    play_review_game();

  let idKanji = document.getElementById('kanji');
  let readingBlankEl = document.createElement('div');
  readingBlankEl.id = 'reading_blank';
  idKanji.parentNode.insertBefore(readingBlankEl, idKanji);
});
function get_answer() {
  $.getJSON(
    "answer_ajax", {
      kanji_id: kanji_id,
    },
    function (data) {
      $('#reading_blank').hide();
      $("#kanji").before(data["data"]);
      $('#kanjinfo').hide();
      clearInterval(passTimer);
      passTime = 0;
      setTimeout(function() {
        window.location.href = q_url;
      }, 1500);
    }
  );
}
