$(function () {
  setTimeout("get_answer()", 8000);
  let idKanji = document.getElementById('kanji');
  let readingBlankEl = document.createElement('div');
  // readingBlankEl.className = 'reading_blank';
  readingBlankEl.id = 'reading_blank';
  idKanji.parentNode.insertBefore(readingBlankEl, idKanji);
});
function get_answer() {
  $.getJSON(
    "answer_ajax",
    {
      kanji_id: kanji_id,
    },
    function (data) {
      $('#reading_blank').hide();
      $("#kanji").before(data["data"]);
    }
  );
}
