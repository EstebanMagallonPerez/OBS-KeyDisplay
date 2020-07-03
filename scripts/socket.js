document.addEventListener('DOMContentLoaded', function(){ 
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};
    updater.start();
}, false);

var updater = {
    socket: null,

    start: function() {
        var url = "ws://" + location.host + "/keyboardSocket";
        updater.socket = new WebSocket(url);
        updater.socket.onmessage = function(event) {
            updater.showMessage(JSON.parse(event.data));
        }
    },

    showMessage: function(message) {
        if (message.type == "press"){
            press(message)
        }else if (message.type == "release"){
            release(message)
        } 
    }
};

function press(data) {
    if(lookupTable[""+data.scan_code])
    {
        lookupTable[data.scan_code].className = "key active"
        lookupTable[data.scan_code].querySelector(".keyOverlay").className = "keyOverlay active"
    }
}
function release(data) {
    if(lookupTable[data.scan_code])
    {
        lookupTable[data.scan_code].className = "key"
        lookupTable[data.scan_code].querySelector(".keyOverlay").className = "keyOverlay inactive"
    }
}