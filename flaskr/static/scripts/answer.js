let success_se;
let timer;
success_se = new Audio('../static/se/suc.mp3');
if (suc) {
  get_answer();
  if (se)
    success_se.play();
}

const play_review_game = () => {
  if (window.location.pathname === '/question') {
    localStorage.setItem('start_time', new Date().getTime());
  }

  let elapsed = new Date().getTime() - localStorage.getItem('start_time');
  let remaining = time - elapsed;
  if (remaining > 0) {
    if (suc) clearTimeout(timer)
    else timer = setTimeout(get_answer, remaining);
  }
}

$(function () {
  if (!gamemode) {
    setInterval(get_answer, time);
  } else {
    play_review_game();
  }

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
      setTimeout(function() {
        window.location.href = q_url;
      }, 1500);
    }
  );
}
