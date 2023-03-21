// window.wx_msg.postMessage('This is a message body');
// window.wx_msg.postMessage('This is a message body again'); 

function sendScrollPos() {
    var scrollPos = window.scrollY;
    // window.wx_msg.postMessage(`we are scrolling at ${scrollPos}`)

    // send scrollpos as json
    window.wx_msg.postMessage({ scrollPos: scrollPos })
}

window.addEventListener('scroll', sendScrollPos);

function scrollToPos(scrollPos) { // not used
    window.scrollTo(0, scrollPos);
}

function jumpToLine(lineNumber) {
    // Find the pre element
    var preElement = document.querySelector("pre");
  
    // Get the height of each line
    var lineHeight = parseInt(getComputedStyle(preElement).lineHeight);
  
    // Get the line number spans
    var lineNumSpans = preElement.parentElement.querySelectorAll(".line-numbers-rows span");
  
    // Get the total number of lines
    var totalLines = lineNumSpans.length;
  
    // Clamp the line number to the valid range
    var clampedLineNumber = Math.max(1, Math.min(totalLines, lineNumber));
    
    // Get the position of the specified line
    var position = (clampedLineNumber - 1) * lineHeight;
  
    // Scroll to the position
    scrollToPos(position);
    // preElement.parentElement.scrollTo({
    //   top: position,
    //   behavior: 'smooth'
    // });
  }
  
// function jumpToLine(lineNumber) {
//     // Get the element with the corresponding line number ID
//     var lineElement = document.getElementById("line" + lineNumber);
//     // alert(lineNumber);

//     // If the element exists, scroll to it
//     if (lineElement) {
//         lineElement.scrollIntoView({ behavior: "smooth" });
//     }
//     else {
//         // The reason it doesn't exist is because prism code highlighting is
//         // stripping the span tags from the code. 
        
//         // alert("Line number " + lineNumber + " does not exist.");
//     }
// }

window.onload = function () {
    scroll_or_jump = "0000";  // 0000 will be replaced with "scroll" or "jump"

    if (scroll_or_jump == "scroll") {
        // Scroll to the position with x=0 and y=500 before the html on loaded meaning no flickering
        window.scrollTo(0, 9999);  // 9999 will be replaced by the scrollPos by python
    }
    else if (scroll_or_jump == "jump") {
        // Scroll to the line before the html on loaded meaning no flickering
        jumpToLine(8888);
    }
};