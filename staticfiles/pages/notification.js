// the javascript for notification permission requesting and notifying
var notifying=true;
var bell = document.getElementById("notify_bell");

window.addEventListener('load', function () {
    Notification.requestPermission(function (status) {
        if (Notification.permission !== status) 
            Notification.permission = status;
    });
});

function notify(msg, usealert=true){
    if(document.hasFocus())
        if(usealert)
            alert(msg);
    else if(notifying){
        var n = new Notification(msg);
        n.onshow = function(){setTimeout(n.close, 1600);}
    }
}

function call(msg)
{
    alert(msg);
    if(notifying){
        var n = new Notification(msg);
        n.onshow = function(){setTimeout(n.close, 1600);}
    }
}

function setNotification(){
    notifying=!notifying;
    bell.className=notifying?"far fa-bell":"far fa-bell-slash";
}