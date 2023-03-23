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
    {% if scroll_to %}
    // Scroll to the position with x=0 and y={{ scroll_to }} before the html is loaded to prevent flickering
    window.scrollTo(0, {{ scroll_to }});
    {% elif line_to %}
    // Scroll to the line before the html is loaded to prevent flickering
    jumpToLine({{ line_to }});
    {% endif %}
};
