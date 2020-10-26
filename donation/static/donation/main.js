/*************
 Popup Login
 ************/
document.getElementById('login').addEventListener('click', function(){
    document.querySelector('.bg-model').style.display = 'flex';
});

document.querySelector('.close').addEventListener('click', function(){
    document.querySelector('.bg-model').style.display = 'none';
});