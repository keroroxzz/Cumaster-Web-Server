//This is a javascript for cookie parsing, which is for global usage.

var cookie = parseCookie();

function parseCookie(){
    var dictionary={};
    var cookies = document.cookie.split(";");
    for(var i=0; i<cookies.length; i++)
    {
        var thisone = cookies[i].split("=");
        if(thisone.length==2)
            dictionary[thisone[0].trim()] = decodeURIComponent(thisone[1].trim());
    }
    return dictionary;
}
function setACookie(item, content)
{
    document.cookie = item + '=' + encodeURIComponent(content) + ';path=/';
}
function setCookieData(name, roomid, psw)
{
    if(name!=null) setACookie('name', name);
    if(roomid!=null) setACookie('rid', roomid);
    if(psw!=null) setACookie('psw', psw);
}