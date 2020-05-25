outputJson = []
lookupTable = {}
function initKeyboardFromJSON(url)
{
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.responseType = 'json';
        xhr.onload = function() {
            var status = xhr.status;
            if (status === 200) 
            {
                var keyboardElement = document.getElementById("keyboard");
                keyboard = xhr.response
                for(row = 0; row < keyboard.length; row++)
                {
                    var rowElement = document.createElement("div");
                    rowElement.className = "row";
                    currentRow = keyboard[row]
                    for (key = 0; key < currentRow.length; key++)
                    {
                        currentKey = currentRow[key];
                        if (currentKey.keyCode == -1)
                        {
                            let keyElement = document.createElement("div");
                            keyElement.className = "keySpacer";
                            keyElement.innerHTML = "&nbsp;".repeat(currentKey.width)+currentKey.displayText.toUpperCase() +"&nbsp;".repeat(currentKey.width)
                            rowElement.appendChild(keyElement)
                            continue
                        }
                        let keyElement = document.createElement("div");
                        keyElement.className = "key";
                        keyElement.innerHTML = "&nbsp;".repeat(currentKey.width)+currentKey.displayText.toUpperCase() +"&nbsp;".repeat(currentKey.width)
                        keyElement.setAttribute("style", currentKey.style);

                        let keyOverlay = document.createElement("div");
                        keyOverlay.className = "keyOverlay inactive";
                        keyOverlay.setAttribute("style", currentKey.overlayStyle);
                        keyElement.appendChild(keyOverlay)
                        lookupTable[currentKey.keyCode] = keyElement
                        rowElement.appendChild(keyElement)
                    }
                    keyboardElement.appendChild(rowElement);
                }

            }
        };
        xhr.send();
}
keyboardUrl = window.location.search.split("=")[1];
if (keyboardUrl == ""){keyboardUrl = "keyboard"}
initKeyboardFromJSON("./keyboards/"+keyboardUrl+".json")