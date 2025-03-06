document.addEventListener('DOMContentLoaded', function() {
    const messagesContainer = document.getElementById('messages');
    let isSender = true;
    const timeFrame = 3 * 60 * 1000; // 3 minutes in milliseconds
    window.initChat = initChat; // global
    window.nextChat = nextChat;
    window.getChatIndex = getChatIndex;
    window.getIsChatRunning = getIsChatRunning;
    let chatIndex = -1
    let scenarioData = []
    let isChatRunning = true

    let lastdisplayedmessage

    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // append a message element
    function appendMessage(type, text, timestamp) {
        const messageElement = document.createElement('p');
        messageElement.className = type;
        
        messageElement.dataset.timestamp = timestamp;
        if(text === '...'){
            messageElement.classList.add('thinking')
            messageElement.textContent = "...";
        }else{
            messageElement.textContent = text;
        }
        const lastMessage = messagesContainer.lastElementChild;
        const currentTime = new Date(timestamp).getTime();

        // Check if the last message is of the same type and within the timeframe
        if (lastMessage && lastMessage.classList.contains(type)) {
            const lastMessageTime = new Date(lastMessage.dataset.timestamp).getTime();
            if (currentTime - lastMessageTime <= timeFrame) {
                lastMessage.classList.add('consecutive');
                messageElement.classList.add('consecutive');
                lastMessage.classList.remove('no-top-margin');
            }
        }

        // Append new message
        messagesContainer.appendChild(messageElement);
        lastdisplayedmessage = messageElement
        scrollToBottom(); 

        // only last item should have the flick in a multimessage
        updateConsecutiveClasses(messageElement);
    }

    // Setting style depending on position in message stack
    function updateConsecutiveClasses(newMessage) {
        const lastMessage = newMessage.previousElementSibling;

        if (lastMessage && lastMessage.classList.contains('consecutive')) {
            lastMessage.classList.add('not-last');
        }

        if (newMessage.classList.contains('consecutive')) {
            const nextMessage = newMessage.nextElementSibling;
            if (!nextMessage || !nextMessage.classList.contains('consecutive')) {
                newMessage.classList.add('no-top-margin');
                newMessage.classList.remove('consecutive');
            }
        }
    }

    // Function to send a message
    function sendMessage(message, sender) {
        const timestamp = new Date().toISOString();
        const senderstate = sender ? 'send' : 'receive'
        if(lastdisplayedmessage && lastdisplayedmessage.classList.contains(senderstate)){
            lastdisplayedmessage.remove();
        }
        appendMessage(senderstate, message, timestamp);
    }

    // Simulate fetching messages from a JSON file
    // fetch('messages.json')
    //     .then(response => response.json())
    //     .then(data => {
    //         data.forEach(message => {
    //             appendMessage(message.type, message.text, message.timestamp);
    //         });
    //     });
    // Load user message data
    function loadUserMessages(scenario){
        return new Promise((resolve) => {
            try {
                fetch(`/chat/${scenario}`)
                .then(response => response.json())
                .then(data => {
                    resolve(data);
                })
            } catch (error) {
                resolve(error);
            }
        })
    }

    async function initChat(scenario) {
        disableNavigation();
        console.log(`Selected Scenario: ${scenario}`)
        document.getElementsByClassName("container-right")[0].style.width = "70vw";
        let chatContainer = document.getElementById("chatContainer");
        chatContainer.style.display = "flex";
        await new Promise(resolve => setTimeout(resolve, 50));
        chatContainer.style.opacity = "1";
        chatContainer.style.transform = "scale(1)";
        data = await loadUserMessages(scenario);
        console.log(data)
        scenarioData = data
        await resetChatbot();
        updateGUI(data);
        createMessage(chatIndex);
        // Prevent reloading and resending to the server
        await new Promise(resolve => setTimeout(resolve, 2000));
        enableNavigation();
    }

    function disableNavigation(){
        navElements = document.getElementsByClassName('box');
        for (let index = 0; index < navElements.length; index++) {
            navElements[index].classList.add('blocked')
        }
    }

    function enableNavigation(){
        navElements = document.getElementsByClassName('box');
        for (let index = 0; index < navElements.length; index++) {
            navElements[index].classList.remove('blocked')
        }
    }

    // Update header
    function updateGUI(data){
        chatTitle = document.getElementById("chat-name")
        chatTitle.textContent = data.title;
        // TODO update IMAGE
    }

    async function createMessage(chatMessageIndex){
        isChatRunning = true
        isInit = (chatMessageIndex === -1) // If startup dont show user
        let chatMSG
        if (!isInit) {
            sendMessage('...', true);
            chatMSG = scenarioData.messages[chatMessageIndex];
            sendMessage(chatMSG, true)
        }else{
            chatMSG = 'initalisation'
        }
        sendMessage('...', false);
        await new Promise(resolve => setTimeout(resolve, 2000));
        response = await sendToChatbot(chatMSG)
        console.log(response)
        sendMessage(response.response, false)
        if(response.stressLevel) highlightStressor(response.stressLevel);
        if(scenarioData.messages.length <= chatIndex){
            // Last item
            endChat()
        }
        isChatRunning = false
    }

    function highlightStressor(stresslevel){
        messages = document.getElementById('messages').getElementsByClassName('send');
        lastMessage = messages.length - 1

        let stressor = document.createElement('span') 
        stressor.textContent = '⚠️';
        stressor.classList.add('stress');
        let tooltip = document.createElement('span')
        stressText = stresslevel.split('_').join(' ');
        tooltip.textContent = `This user is showing signs of ${stressText}`;
        tooltip.classList.add('tooltip');
        stressor.appendChild(tooltip);
        messages[lastMessage].prepend(stressor)

    }

    async function resetChatbot(){
        await ajaxRequesterPOST("/reset", null)
        document.getElementById('messages').innerHTML = '';
        chatIndex = -1;
        document.getElementById("next-message").style.display = 'flex';
    }

    async function sendToChatbot(message){
        console.log(`Sending: ${message}`)
        response = await ajaxRequesterPOST("/chat", {message: message})
        if(response.success){
            chatIndex++
            return response.data
        }else{
            console.error('Unable to send to chatbot')
            return false
        }

    }

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
                    resolve( {'success': true, 'error': '', 'data': data})
                }).catch(error => {
                    console.error("Error sending message:", error);
                    resolve({'success': false, 'error': error, 'data': ''})
                });
            } catch (error) {
                resolve( {'success': false, 'error': error, 'data': ''})
            }
        })
    }

    async function nextChat(){
        if(!isChatRunning){
            await createMessage(chatIndex)
        }else{
            console.warn('Chat is currently running')
        }
    }

    function endChat(){
        document.getElementById("next-message").style.display = 'none';
    }

    function getChatIndex(){
        return chatIndex
    }

    function getIsChatRunning(){
        return isChatRunning;
    }
});
