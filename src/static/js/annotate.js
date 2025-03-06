function annotateSteps(){
    window.resetMaincount = resetMaincount;
    const chatContainer = document.getElementById('messages');


    // List of annotation steps based on message order
    const annotationSteps = [
        "1. Warm-up (Priming)",
        "2. Context Exploration",
        "3. Stress Indicator Check",
        "4. Reflection & Encouragement",
        "5. Supportive Response",
        "6. Closing Prompt",
        "7. Graceful Exit"
    ];

    let currentIndex =  getChatIndex()
    let isChatbotRunning = getIsChatRunning();
    let maincount = 0
    function annotateMessage(message) {
        if(message.textContent === '...'){
            return null
        }
        let label = document.createElement('span') 
        label.textContent = annotationSteps[maincount]
        label.classList.add('tooltipHelper');
        message.prepend(label)
        maincount++
    }

    function resetMaincount(){
        maincount = 0
    }

    // Check for updates within the send
    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            // checking for elements <p>
            mutation.addedNodes.forEach(node => {
                if (node.nodeType === 1 && node.classList.contains('send')) {
                    annotateMessage(node);
                }
            });
        });
    });

    observer.observe(chatContainer, { childList: true, subtree: true });
}


