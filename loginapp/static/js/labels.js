function setPass() {
    document.getElementById('placeholder').style.display = 'none';
    document.getElementById('password').style.display = 'inline';
    document.getElementById('password').focus();

}
function checkPass() {
    if (document.getElementById('password').value.length == 0) {
        document.getElementById('placeholder').style.display = 'inline';
        document.getElementById('password').style.display = 'none';
    }
}

function setUser() {
    document.getElementById('placeholder2').style.display = 'none';
    document.getElementById('username').style.display = 'inline';
    document.getElementById('username').focus();
    
}
function checkUser() {
    if (document.getElementById('username').value.length == 0) {
        document.getElementById('placeholder2').style.display = 'inline';
        document.getElementById('username').style.display = 'none';
    }
}