window.wx_msg.postMessage('This is a message body');
window.wx_msg.postMessage('This is a message body again'); 

function sendScrollPos() {
    var scrollPos = window.scrollY;
    window.wx_msg.postMessage(`we are scrolling at ${scrollPos}`)
    // send scrollpos as json
    window.wx_msg.postMessage({scrollPos: scrollPos})
}

window.addEventListener('scroll', sendScrollPos);

function scrollToPos(scrollPos) {
    window.scrollTo(0, scrollPos);
}