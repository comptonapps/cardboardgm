class ModalWindow {
    constructor() {
        this.modalWindow = document.createElement('div')
        this.closeButton = document.createElement('button')
        this.init()
    
    }

    init() {
        this.setupModalWindow();
        this.setupCloseButton();
        console.log(this.modalWindow)
    }

    setupModalWindow() {
        this.modalWindow.classList.add('modal-window')
        this.modalWindow.append(this.closeButton)
    }

    setupCloseButton() {
        this.closeButton.classList.add('close-btn')
        this.closeButton.innerText = "CLOSE"
        this.closeButton.addEventListener('click', () => {
            this.modalWindow.remove();
        })
    }
}

class AlertController {
    constructor(title, msg, callback) {
        this.ac;
        this.title = title;
        this.msg = msg;
        this.callback = callback;
        this.init();
    }

    init() {
        this.ac = new ModalWindow().modalWindow;
        this.addContentToModalWindow()
    }

    addContentToModalWindow() {
        this.ac.append(this.getFormContainer())
    }

    getFormContainer() {
        let container = this.newElement('div');
        container.classList.add('form-container');
        container.append(this.getFormTitle());
        container.append(this.getFormMessage());
        container.append(this.getCancelButton());
        container.append(this.getActionButton());
        return container;
    }

    getFormTitle() {
        const h1 = this.newElement('h1');
        h1.innerText = this.title;
        return h1;
    }

    getFormMessage() {
        const messageP = this.newElement('p');
        messageP.innerText = this.msg;
        return messageP;
    }

    getCancelButton() {
        const cancelBtn = this.newElement('button');
        cancelBtn.innerText = "CANCEL";
        cancelBtn.classList.add('form-btn', 'blue');
        cancelBtn.addEventListener('click', () => {
            this.ac.remove();
        })
        return cancelBtn;
    }

    getActionButton() {
        const actionBtn = this.newElement('button');
        actionBtn.innerText = "ALERT"
        actionBtn.classList.add('form-btn', 'red');
        actionBtn.addEventListener('click', () => {
            this.callback();
        })
        return actionBtn;
    }

    newElement(type) {
        return document.createElement(type)
    }
}