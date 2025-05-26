/**
 * @fileoverview Annotation module for visual stressor feedback
 * @author Oliver Chetcuti
 */

/**
 * Main annotation function, mutator watching using EH
 */
function annotateSteps(){
    // reset for each chat
    window.resetMaincount = resetMaincount;
    const chatContainer = document.getElementById('messages');


    // List of annotation steps based on message order
    const annotationSteps = [
        "1. Warm-up (Priming)",
        "2. Context Exploration",
        "3. Stress Indicator Check",
        "4. Reflection & Encouragement",
        "5. Supportive Response",
        "6. Closing Prompt"
    ];

    let maincount = 0;
    /**
     * adds the black annotation box
     * @param {object} message - message element to be anotatted
     */
    function annotateMessage(message) {
        if(message.textContent === '...'){
            return null
        }
        let label = document.createElement('span') 
        label.textContent = annotationSteps[maincount];
        label.classList.add('tooltipHelper');
        message.prepend(label);
        maincount++;
    };

    function resetMaincount(){
        maincount = 0;
    };

    // Check for updates within the send
    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            // checking for elements <p>
            mutation.addedNodes.forEach(node => {
                // element <p> and is a sender
                if (node.nodeType === 1 && node.classList.contains('send')) {
                    annotateMessage(node);
                }
            });
        });
    });
    //https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver/observe
    // observe all P values, monitor for new additions
    observer.observe(chatContainer, { childList: true, subtree: true });
};

    /**
     * adds warning annotation for visual feedback
     * @param {string} stresslevel - stress level as a string 'moderate' 'high' 'low'
     */
function highlightStressor(stresslevel){
    messages = document.getElementById('messages').getElementsByClassName('send');
    lastMessage = messages.length - 1
    if (lastMessage < 0) return; // no senders
    let stressor = document.createElement('span');
    stressor.textContent = '⚠️';
    stressor.classList.add('stress');
    let tooltip = document.createElement('span');
    // no spaces to spaces
    stressText = stresslevel.split('_').join(' ');
    tooltip.textContent = `This user is showing signs of ${stressText}`;
    tooltip.classList.add('tooltip');
    stressor.appendChild(tooltip);
    console.log(messages);
    messages[lastMessage].prepend(stressor);
};