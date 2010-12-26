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
