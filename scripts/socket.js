/*
    This is all the socket logic... I dont think you want to touch this, but if you do I would recommend only looking at the
    on press and on release functions
*/
const socket = io("http://localhost:8080");

socket.on('connect', () => {
    socket.send('hi');
});
socket.on("message", function(data) {
    setTimeout(function(){socket.send('hi');},25)
});

socket.on("press", function(data) {
    if(lookupTable[""+data.scan_code])
    {
        lookupTable[data.scan_code].className = "key active"
        lookupTable[data.scan_code].querySelector(".keyOverlay").className = "keyOverlay active"
    }
});
socket.on("release", function(data) {
    data = data.replace(/\'|\"/g,"")
    if(lookupTable[data])
    {
        lookupTable[data].className = "key"
        lookupTable[data].querySelector(".keyOverlay").className = "keyOverlay inactive"
    }
});