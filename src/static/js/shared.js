/**
 * @fileoverview Shared javascript functions used with both semantic and scripted routes
 * @author Oliver Chetcuti
 */
const playbttn = '\u23F5'
const pausebttn = '\u23F8'
let lastdisplayedmessage

/**
 * Sents request using AJAX to the backend
 * @param {string} url - full url of backend
 * @param {list} bodydata - array containing message 
 * @returns {Promise<Object>} Chatbot response object.
 */
function ajaxRequesterPOST(url, bodydata){
    return new Promise((resolve) => {
        try {
            fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(bodydata)
            }).then(response => response.json()).then(data => {
                resolve( {'success': true, 'error': '', 'data': data});
            }).catch(error => {
                console.error("Error sending message:", error);
                resolve({'success': false, 'error': error, 'data': ''});
            });
        } catch (error) {
            resolve( {'success': false, 'error': error, 'data': ''});
        };
    })
};
/**
 * Disables user nagivation while the chatbot is loading or resetting
 */
function disableNavigation(){
    navElements = document.getElementsByClassName('box');
    for (let index = 0; index < navElements.length; index++) {
        navElements[index].classList.add('blocked');
    };
};
/**
 * Enables user nagivation post chatbot load or reset
 */
function enableNavigation(){
    navElements = document.getElementsByClassName('box');
    for (let index = 0; index < navElements.length; index++) {
        navElements[index].classList.remove('blocked');
    };
}
/**
 * Complete frontent reset for chatbot sync
 * @param {string} url - full url of backend
 */
async function resetChatbot(url){
    await ajaxRequesterPOST(url, null);
    document.getElementById('messages').innerHTML = '';
    chatIndex = -1;
    resetMaincount();
    const playButton = document.getElementById("play-button");
    if (playButton) {
        playButton.style.display = 'flex';
        playButton.textContent = playbttn;
    };

    const nextButton = document.getElementById("next-message");
    if (nextButton) {
        nextButton.style.display = 'none';
    };
}
/**
 * Change message screen to approprate data given user selection
 * @param {list} data - data passed from the server loaded on the client UI
 */
function updateGUI(data){
    const chatTitle = document.getElementById("chat-name");
    chatTitle.textContent = data.title;

    const chatImage = document.querySelector("#chat-icon img");
    chatImage.src = `/static/img/${data.image}`;
    chatImage.alt = data.title;
}
/**
 * Adds message from either sender to reciever to the gui
 * @param {string} type - either 'sender' or 'reciever'.
 * @param {string} text - message content
 */
function appendMessage(type, text) {
    const messagesContainer = document.getElementById('messages');
    const messageElement = document.createElement('p');
    messageElement.className = type;
    
    if(text === '...'){
        messageElement.classList.add('thinking')
        messageElement.textContent = "...";
    }else{
        messageElement.textContent = text;
    };
    // Append new message
    messagesContainer.appendChild(messageElement);
    lastdisplayedmessage = messageElement
    scrollToBottom(); 
};
/**
 * scrolls user to message at bottom (sometimes does not work)
 */
function scrollToBottom() {
    const messagesContainer = document.getElementById('messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
};

/**
 * cleans gui to ensure correct message order then adds the new message
 * @param {string} sender - either 'sender' or 'reciever'.
 * @param {string} message - message content
 */
function sendMessage(message, sender) {
    const senderstate = sender ? 'send' : 'receive';
    if(lastdisplayedmessage && lastdisplayedmessage.classList.contains(senderstate)){
        lastdisplayedmessage.remove();
    };
    appendMessage(senderstate, message);
};