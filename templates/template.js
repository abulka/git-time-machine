window.wx_msg.postMessage('This is a message body');

// MAINTAINING SCROLL POSITION

function sendScrollPos() {
    var scrollPos = window.scrollY;
    window.wx_msg.postMessage({ scrollPos: scrollPos })
}

window.addEventListener('scroll', sendScrollPos);

// JUMPING TO LINE

function scrollToPos(scrollPos) {
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
  }

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