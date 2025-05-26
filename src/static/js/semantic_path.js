/**
 * @fileoverview Semantic specific javascript functions
 * @author Oliver Chetcuti
 */

/**
 * adds the main item to be selected from the home screen
 */
function loadSemanticScenarioBox() {
    const container = document.getElementById('freeform');
    
    const div = document.createElement('div');
    div.className = 'box';
    div.onclick = () => {
        initSemanticChat('semantic');
    };

    const img = document.createElement('img');
    img.src = ``;
    img.alt = ``;
    img.classList.add('scenario-thumbnail');
    const textsubdiv = document.createElement('div');
    textsubdiv.className = 'textbox';
    const title = document.createElement('h3');
    title.textContent = `Freeform User Input with Sentence Transformer model`;
    textsubdiv.appendChild(title);
    div.appendChild(textsubdiv);

    const imgsubdiv = document.createElement('div');
    imgsubdiv.className = 'imgbox';
    imgsubdiv.appendChild(img);
    div.appendChild(imgsubdiv);
    container.appendChild(div);
}

/**
 * DOM loaded actions - post page init
 */
document.addEventListener('DOMContentLoaded', function() {
    let scenarioData = {
        messages: []
    };
    let chatIndex = -1;
    window.initSemanticChat = initChat;
    let lastdisplayedmessage;
    /**
     * Intialise the chat - reset global variables
     * @param {string} scenario - string definition of the chat selected 'doctor'
     */
    async function initChat(scenario) {
        disableNavigation();
        chatIndex = -1;
        scenarioData = {
            messages: []
        };
        console.log(`Selected Scenario: ${scenario}`);
        // give text box space
        document.getElementsByClassName("container-right")[0].style.width = "70vw";
        let chatContainer = document.getElementById("chatContainer");
        chatContainer.style.display = "flex";
        //sleep functions inline - sleep to have slide animations
        await new Promise(resolve => setTimeout(resolve, 50));
        chatContainer.style.opacity = "1";
        chatContainer.style.transform = "scale(1)";
        await resetChatbot("/semantic/reset");
        document.getElementById("play-button").style.display = 'none';
        document.getElementById("input-area").style.display = 'flex';
        // Manual name as freeform
        let data = {};
        data.title = `Freeform User Input with Sentence Transformer model`;
        data.image = ``;
        updateGUI(data);
        console.log(chatIndex);
        // wont display to the user
        createMessage(chatIndex);
        // Prevent reloading and resending to the server
        await new Promise(resolve => setTimeout(resolve, 2000));
        enableNavigation();
    }

    /**
     * chat specific message handler, sends message to gui and backend
     * @async
     * @param {int} chatMessageIndex - client tracked index of chatbot
     */
    async function createMessage(chatMessageIndex){
        isChatRunning = true;
        isInit = (chatMessageIndex === -1) // If startup dont show user
        let chatMSG;
        if (!isInit) {
            sendMessage('...', true);
            chatMSG = scenarioData.messages[chatMessageIndex];
            console.log(scenarioData.messages)
            sendMessage(chatMSG, true)
        }else{
            chatMSG = 'initalisation'
        };
        sendMessage('...', false);
        // fake wait time
        await new Promise(resolve => setTimeout(resolve, 2000));
        response = await sendToChatbot(chatMSG);

        if (response.error){
            alert('Unable to load chatbot, please try another scenario')
            return false
        }
        if(response.stressLevel) highlightStressor(response.stressLevel);
        if(response.endChat){
            // Last item
            endChat();
        };
        console.log(response);
        sendMessage(response.response, false);
        // global chat message tracker
        isChatRunning = false;
    }
    /**
     * packages and error handles message to chatbot
     * @async
     * @param {string} message - user message
     */
    async function sendToChatbot(message){
        console.log(`Sending: ${message}`)
        response = await ajaxRequesterPOST("/semantic/chat", {message: message});
        if(response.success){
            chatIndex++;
            return response.data;
        }else{
            console.error('Unable to send to chatbot')
            return false;
        };
    };

    document.getElementById('message-input').addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            getUserMessage();
        };
    });

    document.getElementById('send-button').addEventListener('click', () => {
        getUserMessage();
    });
    /**
     * gets semantic message when user sends message, clearing the input
     */
    function getUserMessage(){
        if(!isChatRunning){
            const inputField = document.getElementById('message-input');
            const messageText = inputField.value.trim();

            if (messageText !== '') {
                // scenarioData.messages
                scenarioData.messages.push(messageText);
                createMessage(chatIndex);
                inputField.value = '';
            }
        }else{
            console.warn('Chat is currently running')
        }
    }
    /**
     * ends chat hides user input
     */
    function endChat(){
        document.getElementById("input-area").style.display = 'none';
    };

});