function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function loadPopup (url) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200) {
      var el = document.getElementById('popup-content');
      el.innerHTML = this.responseText;
    } else if (this.readyState == 4 && this.status == 302) {
        document.location = this.responseText;
    } else if (this.readyState < 4){
      
    } else if (this.readyState != 200) {
      
    }
  }
  xhttp.open('GET', url, true);
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhttp.send();
}

function login_with_cr () {
  var id = document.getElementById('user_id').value;
  var passwd = document.getElementById('password').value;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200) {
      document.body.innerHTML = this.responseText;
      document.location = this.responseURL;
    } else if (this.readyState < 4){
      
    } else if (this.readyState != 200) {
      alert('Cannot login', this.readyState);
    }
  }
  xhttp.open('POST', '/auth/login', true);
  var csrftoken = getCookie('csrftoken');
  xhttp.setRequestHeader("X-CSRFToken", csrftoken);
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhttp.send('id='+id+'&password='+passwd);
}