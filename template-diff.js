// window.wx_msg.postMessage('This is a message body');
window.wx_msg.postMessage('!!!! This is a message body from template-diff');

function jumpTo(filePath, lineNum) {
    window.wx_msg.postMessage({ command: 'jump_to_file', filePath: filePath, lineNum: lineNum });
}


// function sendScrollPos() {
//     var scrollPos = window.scrollY;
//     // window.wx_msg.postMessage(`we are scrolling at ${scrollPos}`)

//     // send scrollpos as json
//     window.wx_msg.postMessage({scrollPos: scrollPos})
// }

// window.addEventListener('scroll', sendScrollPos);

// function scrollToPos(scrollPos) { // not used
//     window.scrollTo(0, scrollPos);
// }
