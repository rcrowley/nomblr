// clear form fields

window.onload = function() {
  applyDefaultValue(document.getElementById('id_username'), 'username');
  applyPasswordType(document.getElementById('id_password'), 'password', 'text');
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

function applyPasswordType(elem, val, typ) {
  elem.style.color = '#aeaeae';
	elem.style.fontStyle = 'normal'
  elem.value = val;
  elem.type = typ;
  elem.onfocus = function() {
    if(this.value == val) {
      this.style.color = '#000';
			this.style.fontStyle = 'normal'
      this.type = 'password'; //If in focus, input type will be 'password'
      this.value = '';
    }
  }
  elem.onblur = function() {
    if(this.value == '') {
			this.style.color = '#aeaeae'
			this.style.fontStyle = 'italic'
      this.value = val;
      this.type = 'text'; //On blur, input type will be 'text' in order to show value
    }
  }
}
