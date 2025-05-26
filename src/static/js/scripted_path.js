/**
 * @fileoverview Scripted specific javascript client functions
 * @author Oliver Chetcuti
 */

/**
 * DOM loaded actions - post page init
 */
document.addEventListener('DOMContentLoaded', function() {
    // attach functions to global window
    window.isSender = true;
    window.initScriptedChat = initChat; // global
    window.nextChat = nextChat;
    window.getChatIndex = getChatIndex;
    window.getIsChatRunning = getIsChatRunning;
    // mix of local and global variables
    let chatIndex = -1
    let scenarioData = []
    let isChatRunning = true
    let isAutoPlaying = false;
    let autoPlayInterval = null;






    // Simulate fetching messages from a JSON file
    // fetch('messages.json')
    //     .then(response => response.json())
    //     .then(data => {
    //         data.forEach(message => {
    //             appendMessage(message.type, message.text, message.timestamp);
    //         });
    //     });
    // Load user message data
    /**
     * Load messages from server for client side scripted conversation (GET)
     * @param {string} scenario - string definition of the chat selected 'doctor'
     */
    function loadUserMessages(scenario){
        return new Promise((resolve) => {
            try {
                fetch(`/scripted/chat/${scenario}`)
                .then(response => response.json())
                .then(data => {
                    resolve(data);
                })
            } catch (error) {
                resolve(error);
            }
        })
    }

    /**
     * start chat, reset gui and sent first message
     * @param {string} scenario - string definition of the chat selected 'doctor'
     */
    async function initChat(scenario) {
        disableNavigation();
        console.log(`Selected Scenario: ${scenario}`);
        chatIndex = -1;
        document.getElementsByClassName("container-right")[0].style.width = "70vw";
        let chatContainer = document.getElementById("chatContainer");
        chatContainer.style.display = "flex";
        await new Promise(resolve => setTimeout(resolve, 50));
        chatContainer.style.opacity = "1";
        chatContainer.style.transform = "scale(1)";
        data = await loadUserMessages(scenario);
        document.getElementById("input-area").style.display = 'none';
        document.getElementById("play-button").style.display = 'flex';
        console.log(data);
        scenarioData = data;
        await resetChatbot("/scripted/reset");
        updateGUI(data);
        createMessage(chatIndex);
        // Prevent reloading and resending to the server
        await new Promise(resolve => setTimeout(resolve, 2000));
        enableNavigation();
    };
    /**
     * generates the chat messages and sends to shared functions to communicate with server and gui. Disables/updates play button
     * @param {int} chatMessageIndex - client side index of chat position
     */
    async function createMessage(chatMessageIndex){
        isChatRunning = true;
        isInit = (chatMessageIndex === -1) // If startup dont show user
        let chatMSG;
        if (!isInit) {
            sendMessage('...', true);
            chatMSG = scenarioData.messages[chatMessageIndex];
            sendMessage(chatMSG, true);
        }else{
            chatMSG = 'initalisation';
        };
        sendMessage('...', false);
        await new Promise(resolve => setTimeout(resolve, 2000));
        response = await sendToChatbot(chatMSG);
        console.log(response);
        sendMessage(response.response, false);
        if(response.stressLevel) highlightStressor(response.stressLevel);
        if(scenarioData.messages.length <= chatIndex){
            // Last item
            endChat();
            isAutoPlaying = false;
            clearInterval(autoPlayInterval);
            document.getElementById("play-button").textContent = playbttn;
        };
        isChatRunning = false;
    };
    /**
     * helper to send to chatbot with erorr catching for graceful exit
     * @param {string} message - pre-defined message string
     */
    async function sendToChatbot(message){
        console.log(`Sending: ${message}`);
        response = await ajaxRequesterPOST("/scripted/chat", {message: message});
        if(response.success){
            chatIndex++;
            return response.data;
        }else{
            console.error('Unable to send to chatbot');
            return false;
        };

    };
    /**
     * used to avoid spamming on the chatbot / oversending or skipping messages
     */
    async function nextChat(){
        if(!isChatRunning){
            await createMessage(chatIndex);
        }else{
            console.warn('Chat is currently running');
        };
    };
    /**
     * end of the chat, hide the play button
     */
    function endChat(){
        document.getElementById("play-button").style.display = 'none';
    };
    /**
     * getters
     */
    function getChatIndex(){
        return chatIndex;
    };

    function getIsChatRunning(){
        return isChatRunning;
    };

    /**
     * manages the state of the play button between each message block, called as its own function and will set the inverse.
     */
    function toggleAutoPlay() {
        const button = document.getElementById("play-button");
        
        if (!isAutoPlaying) {
            isAutoPlaying = true;
            button.textContent = pausebttn; // Change icon to pause

            autoPlayInterval = setInterval(() => {
                if (!isChatRunning && chatIndex < scenarioData.messages.length) {
                    createMessage(chatIndex);
                } else if (chatIndex >= scenarioData.messages.length) {
                    clearInterval(autoPlayInterval);
                    isAutoPlaying = false;
                    button.textContent = playbttn; // Reset icon
                };
            }, 3000); // Wait time between steps
        } else {
            isAutoPlaying = false;
            clearInterval(autoPlayInterval);
            button.textContent = playbttn;
        };
    };
    window.toggleAutoPlay = toggleAutoPlay;
});

/**
 * displays all message options at the start all (GET)
 */
function loadScenarioBoxes() {
    fetch('/scripted/scenarios')
        .then(response => response.json())
        .then(scenarios => {
            const container = document.getElementById('scripted');

            for (const [key, value] of Object.entries(scenarios)) {
                const div = document.createElement('div');
                div.className = 'box';
                div.onclick = () => {
                    chatIndex = -1
                    initScriptedChat(key);
                    resetMaincount();
                };

                const img = document.createElement('img');
                img.src = `/static/img/${value.image}`;
                img.alt = value.title;
                img.classList.add('scenario-thumbnail');  // Optional styling
                const textsubdiv = document.createElement('div');
                textsubdiv.className = 'textbox';
                const title = document.createElement('h3');
                title.textContent = value.title;
                textsubdiv.appendChild(title);
                div.appendChild(textsubdiv);

                const imgsubdiv = document.createElement('div');
                imgsubdiv.className = 'imgbox';
                imgsubdiv.appendChild(img);
                div.appendChild(imgsubdiv);
                container.appendChild(div);
            }
        }).catch(error => {
            console.error('Error loading scenarios:', error);
        });
};