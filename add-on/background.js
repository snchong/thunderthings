/* **************************************************************
 *
 * Set up listeners, menus, and event handlers
 */

// Enable browser action button depending on how many emails are selected
browser.mailTabs.onSelectedMessagesChanged.addListener(async (tab, messageList) => {
    let messageCount = messageList.messages.length;
    if (messageCount == 1) {
	browser.browserAction.enable(tab.id);
    } else {
	browser.browserAction.disable(tab.id);
    }
});


// Dispatch appropriately based on events
browser.browserAction.onClicked.addListener((tab, info) => {  processAddToThingsAction(info, tab); } );
browser.commands.onCommand.addListener((command) => {
    if (command === "add_to_things_command") handleAddToThingsCommand();
    if (command === "copy_msg_link_command") handleCopyMsgLinkCommand();
} );



// Set up context menu item
browser.menus.create({
    id: "add_to_things",
    title: "Add to Things",
    contexts: ["message_list","page"],
    async onclick(info, tab) { processAddToThingsAction(info, tab); },
});

browser.menus.create({
    id: "copy_msg_link",
    title: "Copy as link",
    contexts: ["message_list","page"],
    async onclick(info, tab) { processCopyMsgLinkAction(info, tab); },
});

browser.menus.onShown.addListener((info) => {  
    let oneMessage = true;
    if (info.selectedMessages) {
	// Invoked from a message list, as opposed to a page
	oneMessage = info.selectedMessages.messages.length == 1;
    }
    
    browser.menus.update("add_to_things", { enabled: oneMessage });
    browser.menus.update("copy_msg_link", { enabled: oneMessage });
    browser.menus.refresh();
});


/* **************************************************************
 *
 * Handle Add to Things actions/commands
 */

// Handle Add to Things command
async function handleAddToThingsCommand() {
    // get the current active tab, and try to get a message from there
    //let tab = await browser.tabs.getCurrent();
    let tabs = await browser.tabs.query({active: true, currentWindow:true});
    console.log("ThunderThings: command invoked");
    if (tabs && tabs.length == 1) {
	processAddToThingsAction(null, tabs[0]);
    }
}

// Process "Add to Things" action on tab
async function processAddToThingsAction(info, tab) {
    let message = null;
    if (info && info.selectedMessages && info.selectedMessages.length == 1) {
	message = info.selectedMessages.messages[0];
    }
    else if (tab != null) {
	message = await browser.messageDisplay.getDisplayedMessage(tab.id);
    }

    if (message != null) {
	console.log("ThunderThings: got notified of a message! " + message.headerMessageId);
	addToThings(message);
    }
}


/**
 * Add an item to Things
 */
function addToThings(message) {
    let notes = "[Email](mid:" + message.headerMessageId + ")"
    browser.runtime.sendNativeMessage(
	"thunderthings",
	{ name: message.subject, notes: notes },
	function(response) {
	    if (chrome.runtime.lastError) {
		console.error("ERROR: " + chrome.runtime.lastError.message);
		console.error("ThunderThings was unable to comunicate with Things to create the item.\n"+
			     "Please make sure that the ThunderThings application is installed and has been run. " +
			     "See https://github.com/snchong/ThunderThings for more details.");
	    } else {
		console.log("Messaging host says: ", response);
	    }
	});
    
}


/* **************************************************************
 *
 * Handle Copy as Link actions/commands
 */

// Handle Copy as Link command
async function handleCopyMsgLinkCommand() {
    // get the current active tab, and try to get a message from there
    //let tab = await browser.tabs.getCurrent();
    let tabs = await browser.tabs.query({active: true, currentWindow:true});
    console.log("ThunderThings: copy link command invoked");
    if (tabs && tabs.length == 1) {
	processCopyMsgLinkAction(null, tabs[0]);
    }
}

async function processCopyMsgLinkAction(info, tab) {
    let message = null;
    if (info && info.selectedMessages && info.selectedMessages.length == 1) {
	message = info.selectedMessages.messages[0];
    }
    else if (tab != null) {
	message = await browser.messageDisplay.getDisplayedMessage(tab.id);
    }

    if (message != null) {
	console.log("ThunderThings: copy msg as link " + message.headerMessageId);
	copyAsLink(message);
    }
}


/**
 * Copy message as link
 */
function copyAsLink(message) {
    let link = "[Email](mid:" + message.headerMessageId+")";
    navigator.clipboard.writeText(link).then(function() {
	console.log("ThunderThings: copied msg link to clipboard");
    }, function() {
	console.log("ThunderThings: failed to copy msg link to clipboard");
	
    });
    
}
