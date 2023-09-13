let success;
success = new Audio('../static/se/suc.mp3');
if (suc) {
  get_answer();
  if (se)
    success.play();
}
$(function () {
  // setTimeout("get_answer()", time);
  if (!localStorage.getItem('start_time')) {
    localStorage.setItem('start_time', new Date().getTime());
  }

  let elapsed = new Date().getTime() - localStorage.getItem('start_time');
  let remaining = time - elapsed;
  if (remaining > 0) {
    setTimeout(get_answer, remaining);
  } else {
    get_answer();
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
