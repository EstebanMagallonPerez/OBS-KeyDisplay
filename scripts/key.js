//This is the key class that helps us with initialization of the keyboard. It is also used to generate the JSON in the generator
class Key
{
    constructor(displayText, keyCode, width, style, overlayStyle) 
    {
        this.displayText = displayText
        this.width = width;
        this.style = style;
        this.overlayStyle = overlayStyle;
        this.keyCode = keyCode;
    }
}