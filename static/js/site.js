// clear form fields

window.onload = function() {
  applyDefaultValue(document.getElementById('txtSearch'), 'search for noms, tags or people');
}

function applyDefaultValue(elem, val) {
	elem.style.color = '#aeaeae';
	elem.style.fontStyle = 'italic'
  elem.value = val;
  elem.onfocus = function() {
    if(this.value == val) {
			this.style.color = '#000';
			this.style.fontStyle = 'normal'
      this.value = '';
    }
  }
  elem.onblur = function() {
    if(this.value == '') {
			this.style.color = '#aeaeae';
  		this.style.fontStyle = 'italic'
	    this.value = val;
    }
  }
}

// recipe to fullscreen

function fullscreen(id) {
	document.getElementById(id).className += " recfull";
}

function fullscreenOff(id) {
	document.getElementById(id).className = document.getElementById(id).className.replace('recfull','');
}

// show facebook friends

function showFriends(id) {
	document.getElementById(id).style.right = '0';
}