$(document).ready(function(){
    if(!$('#circle').prop('checked'))
        $('#success_sound').prop('checked', false).prop('disabled', true);
    $('#circle').change(function(){
      if(!this.checked)
        $('#success_sound').prop('checked', false).prop('disabled', true);
      else
        $('#success_sound').prop('disabled', false);
    });
  });
