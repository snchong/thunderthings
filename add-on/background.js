//browser.browserAction.disable();

browser.mailTabs.onSelectedMessagesChanged.addListener(async (tab, messageList) => {
    let messageCount = messageList.messages.length;
    if (messageCount == 1) {
	browser.browserAction.enable(tab.id);
    } else {
	browser.browserAction.disable(tab.id);
    }
});

async function handleClick(info, tab) {
    let message = null;
    if (info && info.selectedMessages && info.selectedMessates.length == 1) {
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

async function handleCommand() {
    // get the current active tab, and try to get a message from there
    //let tab = await browser.tabs.getCurrent();
    let tabs = await browser.tabs.query({active: true, currentWindow:true});
    console.log("ThunderThings: command invoked");
    if (tabs && tabs.length == 1) {
	handleClick(null, tabs[0]);
    }
}


browser.menus.create({
    id: "add_to_things",
    title: "Add to Things",
    contexts: ["message_list","page"],
    async onclick(info, tab) { handleClick(info, tab); },
});


browser.browserAction.onClicked.addListener((tab, info) => {  handleClick(info, tab); } );
browser.commands.onCommand.addListener((command) => {  if (command === "add_to_things_action") handleCommand(); } );

/**
 * Add an item to Things
 */
function addToThings(message) {
    let notes = "[url=mid:" + message.headerMessageId + "]Email[/url]"
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

browser.menus.onShown.addListener((info) => {  
    let oneMessage = true;
    if (info.selectedMessages) {
	// Invoked from a message list, as opposed to a page
	oneMessage = info.selectedMessages.messages.length == 1;
    }
    
    browser.menus.update("add_to_things", { enabled: oneMessage });
    browser.menus.refresh();
});

