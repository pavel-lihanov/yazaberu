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
      var el = $('#popup-content');
      el.html(this.responseText);
      el.addClass('is-visible');
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

function add_trip(_from, _to, _date){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200) {
        alert('OK');
    } else if (this.readyState < 4){
      
    } else if (this.readyState != 200) {
      alert('Error!', this.readyState);
    }
  }
  xhttp.open('POST', '/transport/add_trip', true);
  var csrftoken = getCookie('csrftoken');
  xhttp.setRequestHeader("X-CSRFToken", csrftoken);
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhttp.send('from='+encodeURIComponent(_from)+'&to='+encodeURIComponent(_to)+'&date='+encodeURIComponent(_date));
}

function add_parcel(_from, _to, _date, _name, _description, _max_price, _image){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200) {
        alert('OK');
    } else if (this.readyState < 4){
      
    } else if (this.readyState != 200) {
      alert('Error!', this.readyState);
    }
  }
  xhttp.open('POST', '/transport/add_parcel', true);
  var csrftoken = getCookie('csrftoken');
  xhttp.setRequestHeader("X-CSRFToken", csrftoken);
  xhttp.setRequestHeader('Content-type', 'multipart/form-data');
  xhttp.send(
    'from='+encodeURIComponent(_from)
    +'&to='+encodeURIComponent(_to)
    +'&date='+encodeURIComponent(_date)
    +'&name='+encodeURIComponent(_name)
    +'&description='+encodeURIComponent(_description)
    +'&max_price='+encodeURIComponent(_max_price)
    );
}


function find_parcel (origin, destination, due_date) {
    var new_loc = "/transport/parcel_search?origin="+encodeURIComponent(origin)+"&destination="+encodeURIComponent(destination)+"&date="+(due_date?encodeURIComponent(due_date):"any");
    document.location=new_loc;
}

function find_trip (origin, destination,due_date) {
    var new_loc = "/transport/trip_search?origin="+encodeURIComponent(origin)+"&destination="+encodeURIComponent(destination)+"&date="+(due_date?encodeURIComponent(due_date):"any");
    document.location=new_loc;
}


function register () {
  var firstName = document.getElementById('first_name').value;
  var phone = document.getElementById('phone').value;
  var email = document.getElementById('email').value;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200) {
      var el = document.getElementById('popup-content');
      el.innerHTML = this.responseText;
    } else if (this.readyState < 4){
      
    } else if (this.readyState != 200) {
      alert('Cannot register', this.readyState);
    }
  }
  xhttp.open('POST', '/auth/register', true);
  var csrftoken = getCookie('csrftoken');
  xhttp.setRequestHeader("X-CSRFToken", csrftoken);
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhttp.send('first_name='+encodeURIComponent(firstName)+'&phone='+encodeURIComponent(phone)+'&email='+encodeURIComponent(email));
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
  xhttp.send('id='+encodeURIComponent(id)+'&password='+encodeURIComponent(passwd));
}

function offerTrip(parcel_id){
    loadPopup('/transport/parcel/'+parcel_id+'/offer_trip');
}

function offerParcel(trip_id){
    loadPopup('/transport/trip/'+parcel_id+'/offer_parcel');
}


function acceptOffer(offer_id) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200) {
      //document.body.innerHTML = this.responseText;
      //document.location = this.responseURL;
      alert('OK');
    } else if (this.readyState < 4){
      
    } else if (this.readyState != 200) {
      alert('Error', this.readyState);
    }
  }
  xhttp.open('POST', '/transport/offer/'+offer_id+'/accept', true);
  var csrftoken = getCookie('csrftoken');
  xhttp.setRequestHeader("X-CSRFToken", csrftoken);
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhttp.send();    
}

function declineOffer(offer_id) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200) {
      document.location = this.responseURL;
      alert('OK');
    } else if (this.readyState < 4){
      
    } else if (this.readyState != 200) {
      alert('Error', this.readyState);
    }
  }
  xhttp.open('POST', '/transport/offer/'+offer_id+'/decline', true);
  var csrftoken = getCookie('csrftoken');
  xhttp.setRequestHeader("X-CSRFToken", csrftoken);
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhttp.send();    
}
